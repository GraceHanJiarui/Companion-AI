import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


def load_json(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def key_case_level(item: dict[str, Any]) -> tuple[str, str]:
    return str(item.get("case_id")), str(item.get("experiment_mode"))


def key_pairwise(item: dict[str, Any]) -> tuple[str, str]:
    return str(item.get("case_id")), str(item.get("comparison_type"))


def compute_case_agreement(j1: list[dict[str, Any]], j2: list[dict[str, Any]]) -> dict[str, Any]:
    left = {key_case_level(x): x for x in j1}
    right = {key_case_level(x): x for x in j2}
    keys = sorted(set(left.keys()) & set(right.keys()))
    if not keys:
        return {"num_shared_items": 0}

    exact_score = 0
    abrupt = 0
    binned = 0
    label_fields = [
        "unsupported_warmth_increase",
        "unsupported_distance_increase",
        "unsupported_initiative_jump",
        "continuation_reopen_after_cooling",
        "final_probe_overshoot",
        "trajectory_reset_present",
    ]
    label_matches = {field: 0 for field in label_fields}
    for k in keys:
        a = left[k]
        b = right[k]
        sa = int(a.get("overall_relational_coherence_1_to_5") or a.get("relational_coherence_score_1_to_5") or 0)
        sb = int(b.get("overall_relational_coherence_1_to_5") or b.get("relational_coherence_score_1_to_5") or 0)
        if sa == sb:
            exact_score += 1
        ba = "low" if sa <= 2 else ("mid" if sa == 3 else "high")
        bb = "low" if sb <= 2 else ("mid" if sb == 3 else "high")
        if ba == bb:
            binned += 1
        if bool(a.get("has_abrupt_shift")) == bool(b.get("has_abrupt_shift")):
            abrupt += 1
        for field in label_fields:
            if bool(a.get(field)) == bool(b.get(field)):
                label_matches[field] += 1
    n = len(keys)
    out = {
        "num_shared_items": n,
        "exact_coherence_score_agreement": round(exact_score / n, 4),
        "binned_coherence_score_agreement": round(binned / n, 4),
        "abrupt_shift_agreement": round(abrupt / n, 4),
    }
    for field, matched in label_matches.items():
        out[f"{field}_agreement"] = round(matched / n, 4)
    return out


def compute_pairwise_agreement(j1: list[dict[str, Any]], j2: list[dict[str, Any]]) -> dict[str, Any]:
    left = {key_pairwise(x): x for x in j1}
    right = {key_pairwise(x): x for x in j2}
    keys = sorted(set(left.keys()) & set(right.keys()))
    if not keys:
        return {"num_shared_items": 0}
    same = 0
    axis_fields = [
        "better_on_trajectory_continuity",
        "better_on_request_preservation",
        "better_on_shift_control",
    ]
    axis_matches = {field: 0 for field in axis_fields}
    for k in keys:
        if str(left[k].get("winner")) == str(right[k].get("winner")):
            same += 1
        for field in axis_fields:
            if str(left[k].get(field) or "tie") == str(right[k].get(field) or "tie"):
                axis_matches[field] += 1
    n = len(keys)
    out = {
        "num_shared_items": n,
        "winner_agreement": round(same / n, 4),
    }
    for field, matched in axis_matches.items():
        out[f"{field}_agreement"] = round(matched / n, 4)
    return out


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def average_reports(reports: list[dict[str, Any]]) -> dict[str, Any]:
    if not reports:
        return {"num_pairs": 0}
    keys = sorted(
        {
            k
            for report in reports
            for k in report.keys()
            if k not in {"num_shared_items", "files"}
        }
    )
    out: dict[str, Any] = {
        "num_pairs": len(reports),
        "pair_details": reports,
    }
    for key in keys:
        vals = [
            float(report[key])
            for report in reports
            if key in report and isinstance(report[key], (int, float))
        ]
        if vals:
            out[f"avg_{key}"] = round(sum(vals) / len(vals), 4)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge1-case")
    parser.add_argument("--judge2-case")
    parser.add_argument("--judge1-pairwise")
    parser.add_argument("--judge2-pairwise")
    parser.add_argument("--case-files", nargs="*")
    parser.add_argument("--pairwise-files", nargs="*")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report: dict[str, Any] = {}
    if args.case_files and len(args.case_files) >= 2:
        case_reports: list[dict[str, Any]] = []
        for a, b in combinations(args.case_files, 2):
            case_reports.append(
                {
                    "files": [a, b],
                    **compute_case_agreement(load_json(a), load_json(b)),
                }
            )
        report["case_level"] = average_reports(case_reports)
    elif args.judge1_case and args.judge2_case:
        report["case_level"] = compute_case_agreement(load_json(args.judge1_case), load_json(args.judge2_case))
    if args.pairwise_files and len(args.pairwise_files) >= 2:
        pairwise_reports: list[dict[str, Any]] = []
        for a, b in combinations(args.pairwise_files, 2):
            pairwise_reports.append(
                {
                    "files": [a, b],
                    **compute_pairwise_agreement(load_json(a), load_json(b)),
                }
            )
        report["pairwise"] = average_reports(pairwise_reports)
    elif args.judge1_pairwise and args.judge2_pairwise:
        report["pairwise"] = compute_pairwise_agreement(load_json(args.judge1_pairwise), load_json(args.judge2_pairwise))

    write_json(Path(args.out), report)


if __name__ == "__main__":
    main()
