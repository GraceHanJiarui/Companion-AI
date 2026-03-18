import argparse
import csv
import json
from pathlib import Path
from typing import Any


RAW_KEYS = ["bond", "care", "trust", "stability"]


def load_cases(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = case.get("case_id", "")
        category = case.get("category", "")
        for idx, phase in enumerate(case.get("phases", [])):
            rel = phase.get("oracle_rel_effective") or {}
            beh = phase.get("oracle_behavior_effective") or {}
            row = {
                "case_id": case_id,
                "category": category,
                "turn_idx": idx,
                "phase": phase.get("phase", ""),
                "user_text": phase.get("user_text", ""),
                "oracle_relational_summary": phase.get("oracle_relational_summary", ""),
                "oracle_behavior_summary": phase.get("oracle_behavior_summary", ""),
            }
            for key in RAW_KEYS:
                row[f"raw4_{key}"] = rel.get(key, "")
            row["beh_Q_clarify"] = beh.get("Q_clarify", "")
            row["beh_Q_aff"] = beh.get("Q_aff", "")
            row["beh_Initiative"] = beh.get("Initiative", "")
            row["beh_E"] = beh.get("E", "")

            # New ontology annotation targets: intentionally blank for human labeling.
            row["cand5_interactional_permission"] = ""
            row["cand6_interactional_permission"] = ""
            row["cand6_boundary_firmness"] = ""

            # Short helper notes to reduce drift during annotation.
            row["annotation_hint_permission"] = (
                "How permitted is continued movement: clarify / affective follow-up / mild initiative?"
            )
            row["annotation_hint_boundary"] = (
                "How strongly is the user marking a ceiling on warmth, care, initiative, or meta-relational movement?"
            )
            rows.append(row)
    return rows


def write_csv(rows: list[dict[str, Any]], path: str) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict[str, Any]], path: str) -> None:
    Path(path).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-json", default="paper_cases_oracle_state_exec_v3.json")
    parser.add_argument(
        "--out-csv",
        default="paper_relation_ontology_annotation_sheet_v1.csv",
    )
    parser.add_argument(
        "--out-json",
        default="paper_relation_ontology_annotation_sheet_v1.json",
    )
    args = parser.parse_args()

    cases = load_cases(args.cases_json)
    rows = build_rows(cases)
    write_csv(rows, args.out_csv)
    write_json(rows, args.out_json)
    print(f"Wrote {Path(args.out_csv).resolve()}")
    print(f"Wrote {Path(args.out_json).resolve()}")


if __name__ == "__main__":
    main()
