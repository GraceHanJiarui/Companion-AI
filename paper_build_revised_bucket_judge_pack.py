import argparse
import json
from pathlib import Path

from paper_eval import (
    build_focused_case_level_judge_inputs,
    build_focused_pairwise_judge_inputs,
    compute_turn_level_metrics,
    group_rows,
    load_rows,
)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-main", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = compute_turn_level_metrics(load_rows(args.input_main))
    grouped = group_rows(rows)

    modes = [
        "baseline_relational_instruction",
        "baseline_relational_instruction_to_interface_i7_sc_vA",
        "explicit_rel_state_rel_to_interface_i7_sc_vA",
        "explicit_rel_state_projected_oracle_i7",
    ]

    compare_pairs = [
        (
            "baseline_relational_instruction",
            "baseline_relational_instruction_to_interface_i7_sc_vA",
            "baseline_vs_baseline_to_i7",
        ),
        (
            "baseline_relational_instruction_to_interface_i7_sc_vA",
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "baseline_to_i7_vs_explicit_relation_to_i7",
        ),
        (
            "baseline_relational_instruction",
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "baseline_vs_explicit_relation_to_i7",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "explicit_rel_state_projected_oracle_i7",
            "explicit_relation_to_i7_vs_oracle_i7",
        ),
    ]

    write_json(
        out_dir / "revised_bucket_case_level_judge_inputs.json",
        build_focused_case_level_judge_inputs(grouped, modes=modes),
    )
    write_json(
        out_dir / "revised_bucket_pairwise_judge_inputs.json",
        build_focused_pairwise_judge_inputs(grouped, compare_pairs=compare_pairs),
    )


if __name__ == "__main__":
    main()
