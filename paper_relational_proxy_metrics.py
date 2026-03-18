import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


WARMTH_MARKERS = [
    "我在这里",
    "陪着你",
    "愿意陪",
    "静静陪",
    "不麻烦",
    "理解你",
    "谢谢你",
    "没关系",
]

DISTANCE_MARKERS = [
    "普通聊天",
    "普通对话",
    "简短",
    "直接",
    "克制",
    "保持现在",
    "不追求亲近",
    "不主动推进",
]

INITIATIVE_MARKERS = [
    "要不要",
    "你可以",
    "不如",
    "想不想",
    "愿不愿意",
    "可以先",
    "可以试试",
]

META_CONTROL_MARKERS = [
    "我会",
    "保持",
    "按现在",
    "继续保持",
    "这种方式",
    "这个风格",
]

COOLING_USER_CUES = [
    "普通聊聊",
    "别太认真",
    "不太想被照顾",
    "正常一点",
    "别像心理咨询",
    "不太想聊得太近",
    "保持现在这样",
    "不用太有在场感",
]


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def count_markers(text: str, markers: list[str]) -> int:
    return sum(text.count(m) for m in markers)


def bullet_count(text: str) -> int:
    return text.count("- ") + text.count("•") + text.count("1.")


def has_any(text: str, markers: list[str]) -> bool:
    return any(m in text for m in markers)


def compute_turn_proxy(row: dict[str, Any], prev_row: dict[str, Any] | None) -> dict[str, Any]:
    assistant = str(row.get("assistant_text") or "")
    user = str(row.get("user_text") or "")

    reply_len = len(assistant)
    question_count = assistant.count("？") + assistant.count("?")
    warmth = count_markers(assistant, WARMTH_MARKERS)
    distance = count_markers(assistant, DISTANCE_MARKERS)
    initiative = question_count + count_markers(assistant, INITIATIVE_MARKERS)
    meta_control = count_markers(assistant, META_CONTROL_MARKERS)
    bullets = bullet_count(assistant)
    polarity = warmth - distance

    if prev_row is None:
        return {
            "reply_len_chars": reply_len,
            "question_count": question_count,
            "warmth_score": warmth,
            "distance_score": distance,
            "initiative_score": initiative,
            "meta_control_score": meta_control,
            "bullet_count": bullets,
            "polarity_score": polarity,
            "length_spike": False,
            "warmth_jump": False,
            "unexpected_polarity_flip": False,
            "unsupported_initiative_jump": False,
            "abrupt_shift_proxy": False,
        }

    prev = prev_row.get("proxy") or {}
    prev_len = int(prev.get("reply_len_chars") or 0)
    prev_warmth = int(prev.get("warmth_score") or 0)
    prev_initiative = int(prev.get("initiative_score") or 0)
    prev_polarity = int(prev.get("polarity_score") or 0)

    length_spike = prev_len > 0 and reply_len >= int(prev_len * 1.8) and (reply_len - prev_len) >= 40
    warmth_jump = abs(warmth - prev_warmth) >= 2
    unexpected_polarity_flip = (prev_polarity != 0 and polarity != 0 and ((prev_polarity > 0) != (polarity > 0)) and abs(polarity - prev_polarity) >= 2)
    unsupported_initiative_jump = has_any(user, COOLING_USER_CUES) and (initiative - prev_initiative) >= 2

    abrupt_votes = sum(
        1
        for x in [length_spike, warmth_jump, unexpected_polarity_flip, unsupported_initiative_jump]
        if x
    )
    abrupt_shift_proxy = abrupt_votes >= 2 or unexpected_polarity_flip or unsupported_initiative_jump

    return {
        "reply_len_chars": reply_len,
        "question_count": question_count,
        "warmth_score": warmth,
        "distance_score": distance,
        "initiative_score": initiative,
        "meta_control_score": meta_control,
        "bullet_count": bullets,
        "polarity_score": polarity,
        "length_spike": length_spike,
        "warmth_jump": warmth_jump,
        "unexpected_polarity_flip": unexpected_polarity_flip,
        "unsupported_initiative_jump": unsupported_initiative_jump,
        "abrupt_shift_proxy": abrupt_shift_proxy,
    }


def group_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[str(row.get("case_id") or "unknown_case")][str(row.get("experiment_mode") or "unknown_mode")].append(row)
    for case_id in grouped:
        for mode in grouped[case_id]:
            grouped[case_id][mode] = sorted(grouped[case_id][mode], key=lambda x: int(x.get("turn_idx") or 0))
    return grouped


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    prox = [r["proxy"] for r in rows]
    return {
        "num_turns": len(rows),
        "avg_reply_len_chars": round(mean(p["reply_len_chars"] for p in prox), 2),
        "avg_warmth_score": round(mean(p["warmth_score"] for p in prox), 3),
        "avg_initiative_score": round(mean(p["initiative_score"] for p in prox), 3),
        "avg_meta_control_score": round(mean(p["meta_control_score"] for p in prox), 3),
        "length_spike_turns": sum(1 for p in prox if p["length_spike"]),
        "warmth_jump_turns": sum(1 for p in prox if p["warmth_jump"]),
        "unexpected_polarity_flip_turns": sum(1 for p in prox if p["unexpected_polarity_flip"]),
        "unsupported_initiative_jump_turns": sum(1 for p in prox if p["unsupported_initiative_jump"]),
        "abrupt_shift_proxy_turns": sum(1 for p in prox if p["abrupt_shift_proxy"]),
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_markdown(path: Path, global_summary: dict[str, Any]) -> None:
    lines = [
        "# Relational Proxy Metrics",
        "",
        "This file reports heuristic automatic proxies for trajectory instability.",
        "",
        "These proxies are not treated as ground-truth coherence metrics.",
        "They are intended as structured secondary diagnostics alongside judge-based evaluation.",
        "",
        "## Heuristic definitions",
        "",
        "- `length_spike`: current reply length is at least 1.8x the previous turn and at least 40 chars longer",
        "- `warmth_jump`: absolute change in warmth-marker count >= 2",
        "- `unexpected_polarity_flip`: polarity score flips sign with magnitude change >= 2",
        "- `unsupported_initiative_jump`: user expresses cooling / boundary cue and assistant initiative score jumps by >= 2",
        "- `abrupt_shift_proxy`: at least two heuristic votes, or any polarity flip / unsupported initiative jump",
        "",
        "## Global summary",
        "",
    ]
    for mode, summary in global_summary.items():
        lines.append(f"### {mode}")
        for k, v in summary.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    rows = load_rows(args.input)
    grouped = group_rows(rows)

    turn_rows: list[dict[str, Any]] = []
    case_summary: dict[str, dict[str, Any]] = {}
    global_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for case_id, by_mode in grouped.items():
        case_summary[case_id] = {}
        for mode, mode_rows in by_mode.items():
            prev = None
            enriched: list[dict[str, Any]] = []
            for row in mode_rows:
                item = dict(row)
                item["proxy"] = compute_turn_proxy(item, prev)
                enriched.append(item)
                turn_rows.append(item)
                prev = item
            case_summary[case_id][mode] = summarize(enriched)
            global_buckets[mode].extend(enriched)

    global_summary = {mode: summarize(mode_rows) for mode, mode_rows in global_buckets.items()}

    out_dir = Path(args.out_dir)
    write_json(out_dir / "relational_proxy_turn_rows.json", turn_rows)
    write_json(out_dir / "relational_proxy_case_summary.json", case_summary)
    write_json(out_dir / "relational_proxy_global_summary.json", global_summary)
    write_markdown(out_dir / "PAPER_RELATIONAL_PROXY_METRICS.md", global_summary)


if __name__ == "__main__":
    main()
