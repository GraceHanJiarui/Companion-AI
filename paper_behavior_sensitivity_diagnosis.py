import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from app.generation.execution_interface import build_execution_interface


BEHAVIOR_DIMS = [
    "E",
    "Q_clarify",
    "Directness",
    "T_w",
    "Q_aff",
    "Initiative",
    "Disclosure_Content",
    "Disclosure_Style",
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


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx = mean(xs)
    my = mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = sum((x - mx) ** 2 for x in xs)
    den_y = sum((y - my) ** 2 for y in ys)
    den = (den_x * den_y) ** 0.5
    if den <= 1e-12:
        return None
    return num / den


def summarize_file(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (str(row["case_id"]), int(row["turn_idx"]))
        by_key[key][str(row["experiment_mode"])] = row

    mode_state = None
    for row in rows:
        mode = str(row["experiment_mode"])
        if "_oracle_state_i7_" in mode:
            mode_state = mode
            break
    if not mode_state:
        raise ValueError("Could not find oracle_state mode in result file")
    mode_behavior = "explicit_rel_state_projected_oracle_behavior_i7"
    mode_oracle = "explicit_rel_state_projected_oracle_i7"

    signed_deltas: dict[str, list[float]] = defaultdict(list)
    abs_deltas: dict[str, list[float]] = defaultdict(list)
    len_gaps_state_vs_behavior: list[float] = []
    len_gaps_state_vs_oracle: list[float] = []
    dim_signed_for_corr: dict[str, list[float]] = defaultdict(list)
    dim_abs_for_corr: dict[str, list[float]] = defaultdict(list)
    interface_mismatch_counts: dict[str, int] = defaultdict(int)
    interface_pair_count = 0
    examples: list[dict[str, Any]] = []

    for (case_id, turn_idx), group in by_key.items():
        state_row = group.get(mode_state)
        behavior_row = group.get(mode_behavior)
        oracle_row = group.get(mode_oracle)
        if not state_row or not behavior_row or not oracle_row:
            continue

        state_behavior = state_row.get("behavior_effective") or {}
        oracle_behavior = behavior_row.get("behavior_effective") or {}
        if not isinstance(state_behavior, dict) or not isinstance(oracle_behavior, dict):
            continue

        phase = state_row.get("phase")
        state_iface = build_execution_interface(state_behavior, variant="i7", phase=phase)
        oracle_iface = build_execution_interface(oracle_behavior, variant="i7", phase=phase)
        interface_pair_count += 1
        for key in sorted(set(state_iface.keys()) | set(oracle_iface.keys())):
            if state_iface.get(key) != oracle_iface.get(key):
                interface_mismatch_counts[key] += 1

        state_len = len(str(state_row.get("assistant_text") or ""))
        behavior_len = len(str(behavior_row.get("assistant_text") or ""))
        oracle_len = len(str(oracle_row.get("assistant_text") or ""))
        gap_sb = state_len - behavior_len
        gap_so = state_len - oracle_len
        len_gaps_state_vs_behavior.append(gap_sb)
        len_gaps_state_vs_oracle.append(gap_so)

        turn_delta_map: dict[str, float] = {}
        for dim in BEHAVIOR_DIMS:
            delta = float(state_behavior.get(dim, 0.0)) - float(oracle_behavior.get(dim, 0.0))
            signed_deltas[dim].append(delta)
            abs_deltas[dim].append(abs(delta))
            dim_signed_for_corr[dim].append(delta)
            dim_abs_for_corr[dim].append(abs(delta))
            turn_delta_map[dim] = delta

        examples.append(
            {
                "case_id": case_id,
                "turn_idx": turn_idx,
                "phase": phase,
                "len_gap_state_vs_behavior": gap_sb,
                "len_gap_state_vs_oracle": gap_so,
                "top_signed_deltas": sorted(
                    turn_delta_map.items(), key=lambda kv: abs(kv[1]), reverse=True
                )[:4],
            }
        )

    dim_summary: dict[str, Any] = {}
    for dim in BEHAVIOR_DIMS:
        dim_summary[dim] = {
            "mean_signed_delta_state_minus_oracle_behavior": round(mean(signed_deltas[dim]), 4) if signed_deltas[dim] else None,
            "mean_abs_delta_state_minus_oracle_behavior": round(mean(abs_deltas[dim]), 4) if abs_deltas[dim] else None,
            "corr_signed_delta_with_len_gap_state_vs_behavior": (
                round(pearson(dim_signed_for_corr[dim], len_gaps_state_vs_behavior), 4)
                if pearson(dim_signed_for_corr[dim], len_gaps_state_vs_behavior) is not None
                else None
            ),
            "corr_abs_delta_with_len_gap_state_vs_behavior": (
                round(pearson(dim_abs_for_corr[dim], len_gaps_state_vs_behavior), 4)
                if pearson(dim_abs_for_corr[dim], len_gaps_state_vs_behavior) is not None
                else None
            ),
        }

    examples_sorted = sorted(examples, key=lambda x: x["len_gap_state_vs_behavior"], reverse=True)[:8]
    ranked_by_abs = sorted(
        (
            (
                dim,
                dim_summary[dim]["mean_abs_delta_state_minus_oracle_behavior"],
                dim_summary[dim]["corr_abs_delta_with_len_gap_state_vs_behavior"],
            )
            for dim in BEHAVIOR_DIMS
        ),
        key=lambda item: (item[1] if item[1] is not None else -1),
        reverse=True,
    )

    return {
        "oracle_state_mode": mode_state,
        "num_pairs": interface_pair_count,
        "avg_len_gap_state_vs_behavior": round(mean(len_gaps_state_vs_behavior), 2) if len_gaps_state_vs_behavior else None,
        "avg_len_gap_state_vs_oracle": round(mean(len_gaps_state_vs_oracle), 2) if len_gaps_state_vs_oracle else None,
        "behavior_dim_summary": dim_summary,
        "interface_mismatch_counts": dict(sorted(interface_mismatch_counts.items())),
        "ranked_dims_by_mean_abs_delta": ranked_by_abs,
        "largest_gap_examples": examples_sorted,
    }


def write_md(path: Path, payload: dict[str, Any]) -> None:
    sections: list[str] = []
    sections.append("# Conservative Behavior Sensitivity Diagnosis")
    sections.append("")
    sections.append("This is a small-sample diagnostic analysis.")
    sections.append("It should be read as directional evidence for debugging and next-step design, not as a final causal claim.")
    sections.append("")
    sections.append(f"- `oracle_state_mode`: `{payload['oracle_state_mode']}`")
    sections.append(f"- `num_pairs`: `{payload['num_pairs']}`")
    sections.append(f"- `avg_len_gap_state_vs_behavior`: `{payload['avg_len_gap_state_vs_behavior']}`")
    sections.append(f"- `avg_len_gap_state_vs_oracle`: `{payload['avg_len_gap_state_vs_oracle']}`")
    sections.append("")
    sections.append("## Ranked Behavior Dims By Mean Absolute Delta")
    sections.append("")
    for dim, mean_abs_delta, corr_abs in payload["ranked_dims_by_mean_abs_delta"]:
        sections.append(f"- `{dim}`: mean_abs_delta=`{mean_abs_delta}`, corr_abs_delta_with_len_gap=`{corr_abs}`")
    sections.append("")
    sections.append("## Interface Bucket Mismatch Counts")
    sections.append("")
    for key, value in payload["interface_mismatch_counts"].items():
        sections.append(f"- `{key}`: `{value}`")
    sections.append("")
    sections.append("## Largest Gap Examples")
    sections.append("")
    for item in payload["largest_gap_examples"]:
        sections.append(
            f"- `{item['case_id']}` turn `{item['turn_idx']}` phase `{item['phase']}`: "
            f"len_gap_state_vs_behavior=`{item['len_gap_state_vs_behavior']}`, "
            f"len_gap_state_vs_oracle=`{item['len_gap_state_vs_oracle']}`, "
            f"top_deltas=`{item['top_signed_deltas']}`"
        )
    path.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out-json", default="paper_behavior_sensitivity_diagnosis_v1.json")
    parser.add_argument("--out-md", default="PAPER_BEHAVIOR_SENSITIVITY_DIAGNOSIS.md")
    args = parser.parse_args()

    full_payload: dict[str, Any] = {}
    for path_str in args.inputs:
        path = Path(path_str)
        rows = load_rows(str(path))
        full_payload[path.name] = summarize_file(rows)

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.write_text(json.dumps(full_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md_sections: list[str] = []
    for filename, payload in full_payload.items():
        tmp_path = Path("_tmp_behavior_diag.md")
        write_md(tmp_path, payload)
        md_sections.append(f"## {filename}\n")
        md_sections.append(tmp_path.read_text(encoding="utf-8"))
        tmp_path.unlink(missing_ok=True)
    out_md.write_text("\n".join(md_sections), encoding="utf-8")

    print(f"Wrote {out_json.resolve()}")
    print(f"Wrote {out_md.resolve()}")


if __name__ == "__main__":
    main()
