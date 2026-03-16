import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from app.generation.execution_interface import build_execution_interface


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def idx_rows(rows: list[dict[str, Any]], mode: str) -> dict[tuple[str, int], dict[str, Any]]:
    out: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        if row.get("experiment_mode") == mode:
            out[(str(row.get("case_id")), int(row.get("turn_idx") or 0))] = row
    return out


def summarize(input_path: str, out_path: str) -> None:
    rows = load_rows(input_path)
    real_mode = "explicit_rel_state_projected_i7"
    oracle_mode = "explicit_rel_state_projected_oracle_i7"

    real_rows = idx_rows(rows, real_mode)
    oracle_rows = idx_rows(rows, oracle_mode)
    keys = sorted(set(real_rows.keys()) & set(oracle_rows.keys()))

    dim_mismatch_counts: Counter[str] = Counter()
    case_totals: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "num_turns": 0,
        "exact_interface_match_turns": 0,
        "avg_dim_mismatches": 0.0,
        "avg_real_reply_len": 0.0,
        "avg_oracle_reply_len": 0.0,
    })
    per_turn: list[dict[str, Any]] = []
    total_dim_mismatches = 0
    total_turns = 0
    exact_matches = 0

    for key in keys:
        case_id, turn_idx = key
        real_row = real_rows[key]
        oracle_row = oracle_rows[key]
        phase = real_row.get("phase")

        real_behavior = real_row.get("behavior_effective") or {}
        oracle_behavior = oracle_row.get("oracle_behavior_effective") or oracle_row.get("behavior_effective") or {}

        real_interface = build_execution_interface(real_behavior, variant="i7", phase=phase)
        oracle_interface = build_execution_interface(oracle_behavior, variant="i7", phase=phase)

        mismatches = [k for k in sorted(set(real_interface) | set(oracle_interface)) if real_interface.get(k) != oracle_interface.get(k)]
        for dim in mismatches:
            dim_mismatch_counts[dim] += 1
        mismatch_count = len(mismatches)
        total_dim_mismatches += mismatch_count
        total_turns += 1
        if mismatch_count == 0:
            exact_matches += 1

        real_len = len(str(real_row.get("assistant_text") or ""))
        oracle_len = len(str(oracle_row.get("assistant_text") or ""))

        case_totals[case_id]["num_turns"] += 1
        case_totals[case_id]["avg_dim_mismatches"] += mismatch_count
        case_totals[case_id]["avg_real_reply_len"] += real_len
        case_totals[case_id]["avg_oracle_reply_len"] += oracle_len
        if mismatch_count == 0:
            case_totals[case_id]["exact_interface_match_turns"] += 1

        per_turn.append(
            {
                "case_id": case_id,
                "turn_idx": turn_idx,
                "phase": phase,
                "real_interface": real_interface,
                "oracle_interface": oracle_interface,
                "mismatch_dims": mismatches,
                "real_reply_len": real_len,
                "oracle_reply_len": oracle_len,
            }
        )

    for case_id, summary in case_totals.items():
        n = max(1, int(summary["num_turns"]))
        summary["avg_dim_mismatches"] = round(summary["avg_dim_mismatches"] / n, 2)
        summary["avg_real_reply_len"] = round(summary["avg_real_reply_len"] / n, 2)
        summary["avg_oracle_reply_len"] = round(summary["avg_oracle_reply_len"] / n, 2)
        summary["exact_interface_match_rate"] = round(summary["exact_interface_match_turns"] / n, 4)

    exact_match_rate = round(exact_matches / total_turns, 4) if total_turns else 0.0
    avg_dim_mismatches = round(total_dim_mismatches / total_turns, 2) if total_turns else 0.0

    interpretation: list[str] = []
    if exact_match_rate >= 0.5:
        interpretation.append("A large fraction of turns already match at the i7 interface level; remaining gap is likely dominated by final realization.")
    else:
        interpretation.append("A substantial share of the gap appears before final generation, because real and oracle i7 interfaces often disagree.")
    interpretation.append("This script does not fully separate updater vs projection mapping. It localizes the gap into: pre-realization control mismatch vs post-interface realization.")
    interpretation.append("To separate updater from projection mapping, add structured oracle relational state (e.g. oracle_rel_effective) and run a hybrid mode that uses oracle relation state with the real projection function.")

    payload = {
        "input": input_path,
        "compared_modes": [real_mode, oracle_mode],
        "summary": {
            "num_compared_turns": total_turns,
            "exact_interface_match_turns": exact_matches,
            "exact_interface_match_rate": exact_match_rate,
            "avg_dim_mismatches_per_turn": avg_dim_mismatches,
            "dimension_mismatch_counts": dict(dim_mismatch_counts),
        },
        "by_case": case_totals,
        "per_turn": per_turn,
        "interpretation": interpretation,
    }

    Path(out_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote gap diagnosis to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    summarize(args.input, args.out)


if __name__ == "__main__":
    main()
