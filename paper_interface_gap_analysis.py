import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from app.generation.execution_interface import build_execution_interface
from app.relational.projector import RelState, project_behavior


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def is_oracle_state_mode(mode: str) -> bool:
    return "oracle_state" in mode


def parse_projector_profile(experiment_mode: str) -> str:
    for suffix in [
        "fitlinear",
        "fitpoly2",
        "fitmlp_h4",
        "fitmlp_h8",
        "fitmlp_h12",
        "v3a",
        "v3b",
        "legacy",
        "balanced",
        "conservative",
        "sparse",
    ]:
        if experiment_mode.endswith(f"_p{suffix}"):
            return suffix
    return "legacy"


def reconstruct_behavior_from_oracle_rel(row: dict[str, Any]) -> dict[str, Any]:
    rel = row.get("oracle_rel_effective") or {}
    if not isinstance(rel, dict) or not rel:
        return {}
    rel_state = RelState(
        bond=float(rel.get("bond", 0.25)),
        care=float(rel.get("care", 0.25)),
        trust=float(rel.get("trust", 0.25)),
        stability=float(rel.get("stability", 0.60)),
    )
    beh = project_behavior(
        rel_state,
        active_boundary_keys=[],
        scene=[],
        profile=parse_projector_profile(str(row.get("experiment_mode") or "")),
    )
    return {
        "E": beh.E,
        "Q_clarify": beh.Q_clarify,
        "Directness": beh.Directness,
        "T_w": beh.T_w,
        "Q_aff": beh.Q_aff,
        "Initiative": beh.Initiative,
        "Disclosure_Content": beh.Disclosure_Content,
        "Disclosure_Style": beh.Disclosure_Style,
    }


def get_assistant_len(row: dict[str, Any]) -> int:
    return len((row.get("assistant_text") or "").strip())


def analyze(rows: list[dict[str, Any]], variant: str) -> dict[str, Any]:
    dim_abs = defaultdict(float)
    dim_signed = defaultdict(float)
    dim_count = defaultdict(int)
    mismatch_counter: Counter[str] = Counter()
    mismatch_by_case_phase: list[dict[str, Any]] = []
    total_rows = 0

    for row in rows:
        mode = str(row.get("experiment_mode") or "")
        if not is_oracle_state_mode(mode):
            continue
        pred = row.get("behavior_effective") or {}
        oracle = row.get("oracle_behavior_effective") or {}
        if (not isinstance(pred, dict) or not pred) and isinstance(oracle, dict) and oracle:
            pred = reconstruct_behavior_from_oracle_rel(row)
        if not isinstance(pred, dict) or not isinstance(oracle, dict) or not pred or not oracle:
            continue
        total_rows += 1

        for key in sorted(set(pred.keys()) | set(oracle.keys())):
            pv = float(pred.get(key, 0.0) or 0.0)
            ov = float(oracle.get(key, 0.0) or 0.0)
            delta = pv - ov
            dim_signed[key] += delta
            dim_abs[key] += abs(delta)
            dim_count[key] += 1

        pred_i = build_execution_interface(pred, variant=variant, phase=row.get("phase"))
        oracle_i = build_execution_interface(oracle, variant=variant, phase=row.get("phase"))
        mismatched_fields = [k for k in sorted(set(pred_i) | set(oracle_i)) if pred_i.get(k) != oracle_i.get(k)]
        for field in mismatched_fields:
            mismatch_counter[field] += 1
        mismatch_by_case_phase.append(
            {
                "case_id": row.get("case_id"),
                "phase": row.get("phase"),
                "assistant_len": get_assistant_len(row),
                "mismatch_count": len(mismatched_fields),
                "mismatched_fields": mismatched_fields,
                "pred_interface": pred_i,
                "oracle_interface": oracle_i,
            }
        )

    mismatch_by_case_phase.sort(key=lambda x: (-x["mismatch_count"], -x["assistant_len"], str(x["case_id"]), str(x["phase"])))

    dim_summary = {
        key: {
            "avg_abs_delta": round(dim_abs[key] / max(1, dim_count[key]), 4),
            "avg_signed_delta": round(dim_signed[key] / max(1, dim_count[key]), 4),
            "count": dim_count[key],
        }
        for key in sorted(dim_count)
    }

    return {
        "variant": variant,
        "oracle_state_rows_analyzed": total_rows,
        "dimension_deltas": dim_summary,
        "interface_mismatch_counts": dict(mismatch_counter),
        "top_mismatch_examples": mismatch_by_case_phase[:12],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--variant", default="i7")
    parser.add_argument("--out-json", default="")
    args = parser.parse_args()

    rows = load_rows(args.input)
    report = analyze(rows, args.variant)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out_json:
        Path(args.out_json).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
