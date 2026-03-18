import argparse
import json
import math
from pathlib import Path
from typing import Any


REL_KEYS = ["bond", "care", "trust", "stability"]
BEH_KEYS = [
    "E",
    "Q_clarify",
    "Directness",
    "T_w",
    "Q_aff",
    "Initiative",
    "Disclosure_Content",
    "Disclosure_Style",
]


def _l1_distance(a: dict[str, float], b: dict[str, float], keys: list[str]) -> float:
    return sum(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys) / max(len(keys), 1)


def load_rows(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows: list[dict[str, Any]] = []
    for case in data:
        case_id = case.get("case_id", "")
        category = case.get("category", "")
        for item in case.get("phases", []):
            rel = item.get("oracle_rel_effective") or {}
            beh = item.get("oracle_behavior_effective") or {}
            if not isinstance(rel, dict) or not isinstance(beh, dict):
                continue
            rows.append(
                {
                    "case_id": case_id,
                    "category": category,
                    "phase": item.get("phase"),
                    "user_text": item.get("user_text"),
                    "rel": {k: float(rel.get(k, 0.0)) for k in REL_KEYS},
                    "beh": {k: float(beh.get(k, 0.0)) for k in BEH_KEYS},
                }
            )
    return rows


def pairwise_analysis(rows: list[dict[str, Any]]) -> dict[str, Any]:
    pairs: list[dict[str, Any]] = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a = rows[i]
            b = rows[j]
            rel_dist = _l1_distance(a["rel"], b["rel"], REL_KEYS)
            beh_dist = _l1_distance(a["beh"], b["beh"], BEH_KEYS)
            pairs.append(
                {
                    "a_case": a["case_id"],
                    "a_phase": a["phase"],
                    "a_category": a["category"],
                    "b_case": b["case_id"],
                    "b_phase": b["phase"],
                    "b_category": b["category"],
                    "rel_dist": round(rel_dist, 4),
                    "beh_dist": round(beh_dist, 4),
                    "a_rel": a["rel"],
                    "b_rel": b["rel"],
                    "a_beh": a["beh"],
                    "b_beh": b["beh"],
                }
            )

    close_rel_large_beh = [
        p for p in pairs if p["rel_dist"] <= 0.08 and p["beh_dist"] >= 0.08
    ]
    close_rel_large_beh.sort(key=lambda x: (x["rel_dist"], -x["beh_dist"]))

    high_beh_diff_dims: dict[str, int] = {k: 0 for k in BEH_KEYS}
    for p in close_rel_large_beh:
        for k in BEH_KEYS:
            if abs(p["a_beh"][k] - p["b_beh"][k]) >= 0.08:
                high_beh_diff_dims[k] += 1

    nearest_neighbor_behavior_gap: list[dict[str, Any]] = []
    for idx, row in enumerate(rows):
        neighbors = []
        for j, other in enumerate(rows):
            if idx == j:
                continue
            neighbors.append(
                (
                    _l1_distance(row["rel"], other["rel"], REL_KEYS),
                    _l1_distance(row["beh"], other["beh"], BEH_KEYS),
                    other,
                )
            )
        neighbors.sort(key=lambda x: x[0])
        rel_dist, beh_dist, other = neighbors[0]
        nearest_neighbor_behavior_gap.append(
            {
                "case_id": row["case_id"],
                "phase": row["phase"],
                "category": row["category"],
                "nearest_case": other["case_id"],
                "nearest_phase": other["phase"],
                "nearest_category": other["category"],
                "rel_dist": round(rel_dist, 4),
                "beh_dist": round(beh_dist, 4),
            }
        )

    nearest_neighbor_behavior_gap.sort(key=lambda x: (-x["beh_dist"], x["rel_dist"]))

    per_dim_neighbor_var: dict[str, float] = {}
    for k in BEH_KEYS:
        vals = []
        for idx, row in enumerate(rows):
            neighbors = []
            for j, other in enumerate(rows):
                if idx == j:
                    continue
                neighbors.append((_l1_distance(row["rel"], other["rel"], REL_KEYS), other))
            neighbors.sort(key=lambda x: x[0])
            top = [row["beh"][k]] + [n[1]["beh"][k] for n in neighbors[:2]]
            mean = sum(top) / len(top)
            var = sum((x - mean) ** 2 for x in top) / len(top)
            vals.append(var)
        per_dim_neighbor_var[k] = round(sum(vals) / max(len(vals), 1), 4)

    return {
        "num_rows": len(rows),
        "num_pairs": len(pairs),
        "close_rel_large_beh_pairs": close_rel_large_beh[:20],
        "close_rel_large_beh_pair_count": len(close_rel_large_beh),
        "high_behavior_diff_dims_within_close_rel_pairs": high_beh_diff_dims,
        "nearest_neighbor_behavior_gap": nearest_neighbor_behavior_gap[:20],
        "avg_neighbor_behavior_variance_per_dim": per_dim_neighbor_var,
    }


def build_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Relation Redesign Reverse Analysis")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- `num_rows`: `{summary['num_rows']}`")
    lines.append(f"- `num_pairs`: `{summary['num_pairs']}`")
    lines.append(f"- `close_rel_large_beh_pair_count`: `{summary['close_rel_large_beh_pair_count']}`")
    lines.append("")
    lines.append("## Behavior Dims That Most Often Diverge Despite Similar Relation")
    lines.append("")
    for k, v in summary["high_behavior_diff_dims_within_close_rel_pairs"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines.append("")
    lines.append("## Average Neighbor Behavior Variance")
    lines.append("")
    for k, v in summary["avg_neighbor_behavior_variance_per_dim"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines.append("")
    lines.append("## Most Diagnostic Similar-Relation / Different-Behavior Pairs")
    lines.append("")
    for item in summary["close_rel_large_beh_pairs"][:10]:
        lines.append(
            f"- `{item['a_case']}:{item['a_phase']}` vs `{item['b_case']}:{item['b_phase']}`"
            f" | rel_dist=`{item['rel_dist']}` beh_dist=`{item['beh_dist']}`"
        )
    lines.append("")
    lines.append("## Interpretation Draft")
    lines.append("")
    lines.append("- If close relation states still require meaningfully different behavior targets, current relation dimensions are unlikely to be sufficient as a unique deterministic explanation of behavior.")
    lines.append("- The most recurrent divergent behavior dimensions should be the first candidates for relation-space redesign.")
    lines.append("- This analysis is not a proof that pure relation is impossible; it is evidence about where the current relation space appears under-specified.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-json", default="paper_cases_oracle_state_exec_v1.json")
    parser.add_argument("--out-json", default="paper_relation_reverse_analysis_v1.json")
    parser.add_argument("--out-md", default="PAPER_RELATION_REDESIGN_ANALYSIS.md")
    args = parser.parse_args()

    rows = load_rows(args.cases_json)
    summary = pairwise_analysis(rows)

    out_json = Path(args.out_json)
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    out_md = Path(args.out_md)
    out_md.write_text(build_markdown(summary), encoding="utf-8")

    print(f"Wrote {out_json.resolve()}")
    print(f"Wrote {out_md.resolve()}")


if __name__ == "__main__":
    main()
