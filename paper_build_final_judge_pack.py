import argparse
import json
from pathlib import Path


MAIN_MODES = [
    "baseline_relational_instruction",
    "explicit_rel_state_rel_to_interface_i7",
    "explicit_rel_state_projected_oracle_i7",
]

BRIDGE_MODES = [
    "explicit_rel_state_projected_oracle_state_i7_pfitpoly2",
    "explicit_rel_state_projected_oracle_behavior_i7",
    "explicit_rel_state_projected_oracle_i7",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def index_case_rows(rows):
    out = {}
    for row in rows:
        out[(row["case_id"], row["experiment_mode"])] = row
    return out


def build_pairwise(rows_by_key, case_ids, mode_pairs, template):
    out = []
    for case_id in case_ids:
        for comparison_type, left_mode, right_mode in mode_pairs:
            left = rows_by_key.get((case_id, left_mode))
            right = rows_by_key.get((case_id, right_mode))
            if not left or not right:
                continue
            out.append(
                {
                    "case_id": case_id,
                    "judge_task": "pairwise_relational_coherence_preference",
                    "comparison_type": comparison_type,
                    "instructions": template,
                    "left": {
                        "experiment_mode": left_mode,
                        "turns": left["turns"],
                    },
                    "right": {
                        "experiment_mode": right_mode,
                        "turns": right["turns"],
                    },
                }
            )
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--main-eval-dir", required=True)
    parser.add_argument("--bridge-eval-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    main_dir = Path(args.main_eval_dir)
    bridge_dir = Path(args.bridge_eval_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    main_case_rows = load_json(main_dir / "case_level_judge_inputs.json")
    bridge_case_rows = load_json(bridge_dir / "case_level_judge_inputs.json")

    pairwise_template = load_json(main_dir / "stage2_focused_pairwise_judge_inputs.json")[0]["instructions"]

    main_selected = [r for r in main_case_rows if r["experiment_mode"] in MAIN_MODES]
    bridge_selected = [r for r in bridge_case_rows if r["experiment_mode"] in BRIDGE_MODES]

    main_case_ids = sorted({r["case_id"] for r in main_selected})
    bridge_case_ids = sorted({r["case_id"] for r in bridge_selected})

    main_by_key = index_case_rows(main_selected)
    bridge_by_key = index_case_rows(bridge_selected)

    main_pairwise = build_pairwise(
        main_by_key,
        main_case_ids,
        [
            ("frozen_main_i7_vs_baseline", "explicit_rel_state_rel_to_interface_i7", "baseline_relational_instruction"),
            ("frozen_main_oracle_vs_baseline", "explicit_rel_state_projected_oracle_i7", "baseline_relational_instruction"),
            ("frozen_main_oracle_vs_i7", "explicit_rel_state_projected_oracle_i7", "explicit_rel_state_rel_to_interface_i7"),
        ],
        pairwise_template,
    )

    bridge_pairwise = build_pairwise(
        bridge_by_key,
        bridge_case_ids,
        [
            ("frozen_bridge_state_vs_behavior", "explicit_rel_state_projected_oracle_state_i7_pfitpoly2", "explicit_rel_state_projected_oracle_behavior_i7"),
            ("frozen_bridge_state_vs_oracle", "explicit_rel_state_projected_oracle_state_i7_pfitpoly2", "explicit_rel_state_projected_oracle_i7"),
            ("frozen_bridge_behavior_vs_oracle", "explicit_rel_state_projected_oracle_behavior_i7", "explicit_rel_state_projected_oracle_i7"),
        ],
        pairwise_template,
    )

    write_json(out_dir / "final_main_case_level_judge_inputs.json", main_selected)
    write_json(out_dir / "final_main_pairwise_judge_inputs.json", main_pairwise)
    write_json(out_dir / "final_bridge_case_level_judge_inputs.json", bridge_selected)
    write_json(out_dir / "final_bridge_pairwise_judge_inputs.json", bridge_pairwise)


if __name__ == "__main__":
    main()
