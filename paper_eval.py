import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


BOUNDARY_VIOLATION_RULES = {
    "no_unsolicited_emotion_questions": [
        "你是不是很难受",
        "你现在心情怎么样",
        "你是不是压力很大",
        "你是不是不开心",
        "你是不是很痛苦",
        "你现在情绪怎么样",
    ],
}


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def contains_any(text: str, phrases: list[str]) -> bool:
    return any(p in text for p in phrases)


def boundary_violations(boundary_keys: list[str], assistant_text: str) -> dict[str, bool]:
    out: dict[str, bool] = {}
    for key in boundary_keys:
        phrases = BOUNDARY_VIOLATION_RULES.get(key, [])
        out[key] = contains_any(assistant_text, phrases)
    return out


def basic_row_metrics(row: dict[str, Any]) -> dict[str, Any]:
    assistant_text = str(row.get("assistant_text") or "")
    boundary_keys = [str(x) for x in (row.get("boundary_keys") or [])]
    rel_effective = row.get("rel_effective") or {}
    behavior_effective = row.get("behavior_effective") or {}

    violations = boundary_violations(boundary_keys, assistant_text)
    boundary_violation = any(violations.values()) if violations else False

    return {
        "reply_len_chars": len(assistant_text),
        "has_boundary_keys": bool(boundary_keys),
        "boundary_violation": boundary_violation,
        "boundary_violation_detail": violations,
        "has_rel_state": bool(rel_effective),
        "has_behavior_state": bool(behavior_effective),
        "elapsed_s": float(row.get("elapsed_s") or 0.0),
    }


def compute_turn_level_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        merged = dict(row)
        merged["metrics"] = basic_row_metrics(row)
        out.append(merged)
    return out


def compute_group_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}

    elapsed = [float((r.get("metrics") or {}).get("elapsed_s") or 0.0) for r in rows]
    reply_lens = [int((r.get("metrics") or {}).get("reply_len_chars") or 0) for r in rows]
    boundary_cases = [r for r in rows if (r.get("metrics") or {}).get("has_boundary_keys")]
    boundary_violations_count = sum(1 for r in boundary_cases if (r.get("metrics") or {}).get("boundary_violation"))

    return {
        "num_turns": len(rows),
        "avg_elapsed_s": round(mean(elapsed), 4) if elapsed else 0.0,
        "avg_reply_len_chars": round(mean(reply_lens), 2) if reply_lens else 0.0,
        "boundary_turns": len(boundary_cases),
        "boundary_violation_turns": boundary_violations_count,
        "boundary_violation_rate": round(boundary_violations_count / len(boundary_cases), 4) if boundary_cases else None,
    }


def group_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        case_id = str(row.get("case_id") or "unknown_case")
        mode = str(row.get("experiment_mode") or "unknown_mode")
        grouped[case_id][mode].append(row)

    for case_id in grouped:
        for mode in grouped[case_id]:
            grouped[case_id][mode] = sorted(grouped[case_id][mode], key=lambda x: int(x.get("turn_idx") or 0))
    return grouped


def build_judge_examples(grouped: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    """
    Export minimal examples for future LLM judge / human evaluation.
    This script does not call a judge model yet.
    """
    examples: list[dict[str, Any]] = []
    for case_id, by_mode in grouped.items():
        modes = sorted(by_mode.keys())
        if len(modes) < 2:
            continue

        example = {
            "case_id": case_id,
            "comparison_modes": modes,
            "items": [],
        }

        for mode in modes:
            turns_payload = []
            for row in by_mode[mode]:
                turns_payload.append(
                    {
                        "turn_idx": row.get("turn_idx"),
                        "user_text": row.get("user_text"),
                        "assistant_text": row.get("assistant_text"),
                        "rel_effective": row.get("rel_effective") or {},
                        "behavior_effective": row.get("behavior_effective") or {},
                        "boundary_keys": row.get("boundary_keys") or [],
                    }
                )
            example["items"].append({"experiment_mode": mode, "turns": turns_payload})
        examples.append(example)
    return examples


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="paper_results_v1.jsonl")
    parser.add_argument("--out-dir", default="paper_eval_out")
    args = parser.parse_args()

    rows = load_rows(args.input)
    turn_rows = compute_turn_level_metrics(rows)
    grouped = group_rows(turn_rows)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_json(out_dir / "turn_level_metrics.json", turn_rows)

    case_mode_summary: dict[str, dict[str, Any]] = {}
    for case_id, by_mode in grouped.items():
        case_mode_summary[case_id] = {}
        for mode, mode_rows in by_mode.items():
            case_mode_summary[case_id][mode] = compute_group_summary(mode_rows)
    write_json(out_dir / "case_mode_summary.json", case_mode_summary)

    global_by_mode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _, by_mode in grouped.items():
        for mode, mode_rows in by_mode.items():
            global_by_mode[mode].extend(mode_rows)
    global_summary = {mode: compute_group_summary(mode_rows) for mode, mode_rows in global_by_mode.items()}
    write_json(out_dir / "global_summary.json", global_summary)

    judge_examples = build_judge_examples(grouped)
    write_json(out_dir / "judge_examples.json", judge_examples)

    print(f"Wrote evaluation artifacts to {out_dir.resolve()}")


if __name__ == "__main__":
    main()
