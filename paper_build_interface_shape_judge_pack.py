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
    parser.add_argument("--input-bridge", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    main_rows = compute_turn_level_metrics(load_rows(args.input_main))
    main_grouped = group_rows(main_rows)
    main_modes = [
        "explicit_rel_state_projected_i7_pfitpoly2",
        "explicit_rel_state_projected_c8_pfitpoly2",
        "explicit_rel_state_rel_to_interface_i7",
        "explicit_rel_state_projected_oracle_i7",
    ]
    main_pairs = [
        (
            "explicit_rel_state_rel_to_interface_i7",
            "explicit_rel_state_projected_i7_pfitpoly2",
            "shape_real_direct_i7_vs_real_rel8_to_i7",
        ),
        (
            "explicit_rel_state_projected_i7_pfitpoly2",
            "explicit_rel_state_projected_c8_pfitpoly2",
            "shape_real_i7_discrete_vs_real_c8_continuous",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7",
            "explicit_rel_state_projected_c8_pfitpoly2",
            "shape_real_direct_i7_vs_real_c8_continuous",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7",
            "explicit_rel_state_projected_oracle_i7",
            "shape_real_direct_i7_vs_oracle_i7",
        ),
    ]
    write_json(
        out_dir / "interface_shape_main_case_level_judge_inputs.json",
        build_focused_case_level_judge_inputs(main_grouped, modes=main_modes),
    )
    write_json(
        out_dir / "interface_shape_main_pairwise_judge_inputs.json",
        build_focused_pairwise_judge_inputs(main_grouped, compare_pairs=main_pairs),
    )

    bridge_rows = compute_turn_level_metrics(load_rows(args.input_bridge))
    bridge_grouped = group_rows(bridge_rows)
    bridge_modes = [
        "explicit_rel_state_projected_oracle_state_i7_pfitpoly2",
        "explicit_rel_state_projected_oracle_state_c8_pfitpoly2",
        "explicit_rel_state_rel_to_interface_oracle_state_i7",
        "explicit_rel_state_projected_oracle_behavior_i7",
        "explicit_rel_state_projected_oracle_i7",
    ]
    bridge_pairs = [
        (
            "explicit_rel_state_projected_oracle_state_i7_pfitpoly2",
            "explicit_rel_state_projected_oracle_state_c8_pfitpoly2",
            "shape_oracle_state_i7_discrete_vs_oracle_state_c8_continuous",
        ),
        (
            "explicit_rel_state_rel_to_interface_oracle_state_i7",
            "explicit_rel_state_projected_oracle_state_i7_pfitpoly2",
            "shape_oracle_state_direct_i7_vs_oracle_state_rel8_to_i7",
        ),
        (
            "explicit_rel_state_rel_to_interface_oracle_state_i7",
            "explicit_rel_state_projected_oracle_state_c8_pfitpoly2",
            "shape_oracle_state_direct_i7_vs_oracle_state_c8_continuous",
        ),
        (
            "explicit_rel_state_projected_oracle_state_i7_pfitpoly2",
            "explicit_rel_state_projected_oracle_i7",
            "shape_oracle_state_rel8_to_i7_vs_oracle_i7",
        ),
        (
            "explicit_rel_state_projected_oracle_state_c8_pfitpoly2",
            "explicit_rel_state_projected_oracle_i7",
            "shape_oracle_state_c8_vs_oracle_i7",
        ),
    ]
    write_json(
        out_dir / "interface_shape_bridge_case_level_judge_inputs.json",
        build_focused_case_level_judge_inputs(bridge_grouped, modes=bridge_modes),
    )
    write_json(
        out_dir / "interface_shape_bridge_pairwise_judge_inputs.json",
        build_focused_pairwise_judge_inputs(bridge_grouped, compare_pairs=bridge_pairs),
    )


if __name__ == "__main__":
    main()
