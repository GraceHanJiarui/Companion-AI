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
        "explicit_rel_state_projected_i7_pfitpoly2_sa_vA",
        "explicit_rel_state_projected_i7_pfitpoly2_sc_vA",
        "explicit_rel_state_projected_i7_pfitpoly2_sa_vC",
        "explicit_rel_state_projected_i7_pfitpoly2_sc_vC",
        "explicit_rel_state_rel_to_interface_i7_sa_vA",
        "explicit_rel_state_rel_to_interface_i7_sc_vA",
        "explicit_rel_state_rel_to_interface_i7_sa_vC",
        "explicit_rel_state_rel_to_interface_i7_sc_vC",
        "explicit_rel_state_projected_oracle_i7",
    ]

    compare_pairs = [
        (
            "explicit_rel_state_rel_to_interface_i7_sa_vA",
            "explicit_rel_state_rel_to_interface_i7_sa_vC",
            "main_direct_sa_vA_vs_sa_vC",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "explicit_rel_state_rel_to_interface_i7_sc_vC",
            "main_direct_sc_vA_vs_sc_vC",
        ),
        (
            "explicit_rel_state_projected_i7_pfitpoly2_sa_vA",
            "explicit_rel_state_projected_i7_pfitpoly2_sa_vC",
            "main_projected_sa_vA_vs_sa_vC",
        ),
        (
            "explicit_rel_state_projected_i7_pfitpoly2_sc_vA",
            "explicit_rel_state_projected_i7_pfitpoly2_sc_vC",
            "main_projected_sc_vA_vs_sc_vC",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sa_vA",
            "explicit_rel_state_projected_i7_pfitpoly2_sa_vA",
            "main_direct_vs_projected_sa_vA",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "explicit_rel_state_projected_i7_pfitpoly2_sc_vA",
            "main_direct_vs_projected_sc_vA",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sa_vC",
            "explicit_rel_state_projected_i7_pfitpoly2_sa_vC",
            "main_direct_vs_projected_sa_vC",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sc_vC",
            "explicit_rel_state_projected_i7_pfitpoly2_sc_vC",
            "main_direct_vs_projected_sc_vC",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sa_vA",
            "explicit_rel_state_projected_oracle_i7",
            "main_direct_sa_vA_vs_oracle_i7",
        ),
        (
            "explicit_rel_state_rel_to_interface_i7_sc_vA",
            "explicit_rel_state_projected_oracle_i7",
            "main_direct_sc_vA_vs_oracle_i7",
        ),
    ]

    write_json(
        out_dir / "interface_ontology_main_case_level_judge_inputs.json",
        build_focused_case_level_judge_inputs(grouped, modes=modes),
    )
    write_json(
        out_dir / "interface_ontology_main_pairwise_judge_inputs.json",
        build_focused_pairwise_judge_inputs(grouped, compare_pairs=compare_pairs),
    )


if __name__ == "__main__":
    main()
