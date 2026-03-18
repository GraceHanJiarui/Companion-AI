import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np

from app.generation.execution_interface import (
    _interactional_ontology,
    _permission_ontology,
    build_execution_interface,
    build_execution_interface_from_rel,
)


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

LANG_KEYS = [
    "char_len",
    "line_count",
    "question_count",
    "list_marker_count",
    "advice_marker_count",
    "reassurance_marker_count",
    "presence_marker_count",
    "meta_control_marker_count",
    "first_person_count",
]

I7_A_KEYS = [
    "reply_scope",
    "clarify_followup",
    "affective_followup",
    "initiative_level",
    "warmth_level",
    "relational_push",
    "support_mode",
    "meta_talk",
]
I7_B_KEYS = [
    "response_extent",
    "curiosity",
    "emotional_checkin",
    "forward_pacing",
    "temperature",
    "interaction_pressure",
    "support_posture",
]
I7_C_KEYS = [
    "response_extent_limit",
    "clarification_permission",
    "emotional_permission",
    "forward_pressure_limit",
    "social_temperature_cap",
    "relational_movement_limit",
    "support_allowance",
]

I7_VALUE_MAPS: dict[str, dict[str, int]] = {
    "reply_scope": {"minimal": 0, "brief": 1, "moderate": 2},
    "clarify_followup": {"none": 0, "optional_light": 1, "one_light": 2},
    "affective_followup": {"none": 0, "optional_light": 1, "one_light": 2},
    "initiative_level": {"hold": 0, "light_push": 1, "open_new_branch": 2},
    "warmth_level": {"low": 0, "gentle": 1, "warm": 2},
    "directness_level": {"soft": 0, "balanced": 1, "direct": 2},
    "relational_push": {"avoid": 0, "hold": 1, "slight": 2},
    "support_mode": {"presence_only": 0, "light_practical": 1, "practical_ok": 2},
    "meta_talk": {"avoid": 0},
    "response_extent": {"minimal": 0, "brief": 1, "moderate": 2},
    "curiosity": {"off": 0, "low": 1, "medium": 2, "high": 3},
    "emotional_checkin": {"none": 0, "low": 1, "medium": 2, "high": 3},
    "forward_pacing": {"hold": 0, "light_push": 1, "open_new_branch": 2},
    "temperature": {"low": 0, "gentle": 1, "warm": 2},
    "interaction_pressure": {"avoid": 0, "hold": 1, "slight": 2},
    "support_posture": {"presence_only": 0, "light_practical": 1, "practical_ok": 2},
    "response_extent_limit": {"minimal": 0, "brief": 1, "moderate": 2},
    "clarification_permission": {"none": 0, "optional_light": 1, "one_light": 2},
    "emotional_permission": {"none": 0, "optional_light": 1, "one_light": 2},
    "forward_pressure_limit": {"hold": 0, "light_push": 1, "open_new_branch": 2},
    "social_temperature_cap": {"low": 0, "gentle": 1, "warm": 2},
    "relational_movement_limit": {"avoid": 0, "hold": 1, "slight": 2},
    "support_allowance": {"presence_only": 0, "light_practical": 1, "practical_ok": 2},
}


def load_rows(path: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_oracle_rel_lookup(path: str) -> dict[tuple[str, str], dict[str, float]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lookup: dict[tuple[str, str], dict[str, float]] = {}
    for case in data:
        case_id = str(case.get("case_id") or "")
        for item in case.get("phases", []):
            phase = str(item.get("phase") or "")
            rel = item.get("oracle_rel_effective") or {}
            if not isinstance(rel, dict) or not rel:
                continue
            lookup[(case_id, phase)] = {k: float(rel.get(k, 0.0) or 0.0) for k in REL_KEYS}
    return lookup


def family_from_case_id(case_id: str) -> str:
    lower = case_id.lower()
    if "warm" in lower:
        return "warm"
    if "vuln" in lower:
        return "vulnerability"
    if "cool" in lower:
        return "cooling"
    if "mixed" in lower:
        return "mixed_signal"
    if "ordinary" in lower:
        return "ordinary_neutral"
    if "repair" in lower or "boundary" in lower:
        return "boundary_repair"
    return "other"


def parse_ontology_variant(mode: str) -> str:
    for suffix in ("_vA", "_vB", "_vC"):
        if mode.endswith(suffix):
            return suffix[-1]
    return "A"


def build_relation_vec(row: dict[str, Any], oracle_rel_lookup: dict[tuple[str, str], dict[str, float]]) -> list[float] | None:
    key = (str(row.get("case_id") or ""), str(row.get("phase") or ""))
    rel = oracle_rel_lookup.get(key) or row.get("oracle_rel_effective") or row.get("rel_effective") or {}
    if not isinstance(rel, dict) or not rel:
        return None
    return [float(rel.get(k, 0.0) or 0.0) for k in REL_KEYS]


def build_behavior_vec(row: dict[str, Any]) -> list[float] | None:
    # First-pass M1 uses oracle behavior as the fixed analytic view whenever available.
    beh = row.get("oracle_behavior_effective") or row.get("behavior_effective") or {}
    if not isinstance(beh, dict) or not beh:
        return None
    return [float(beh.get(k, 0.0) or 0.0) for k in BEH_KEYS]


def build_raw_i7_interface(row: dict[str, Any]) -> dict[str, str] | None:
    mode = str(row.get("experiment_mode") or "")
    phase = row.get("phase")
    if "rel_to_interface" in mode:
        rel = row.get("oracle_rel_effective") or row.get("rel_effective") or {}
        if not isinstance(rel, dict) or not rel:
            return None
        return build_execution_interface_from_rel(rel, variant="i7", phase=phase)

    beh = row.get("behavior_effective") or row.get("oracle_behavior_effective") or {}
    if not isinstance(beh, dict) or not beh:
        return None
    return build_execution_interface(beh, variant="i7", phase=phase)


def project_ontology_chart(raw_i7: dict[str, str], ontology_variant: str) -> tuple[list[str], dict[str, str]]:
    if ontology_variant == "A":
        keys = I7_A_KEYS
        return keys, {k: raw_i7.get(k, "") for k in keys}
    if ontology_variant == "B":
        chart = _interactional_ontology(raw_i7)
        keys = I7_B_KEYS
        return keys, {k: chart.get(k, "") for k in keys}
    if ontology_variant == "C":
        chart = _permission_ontology(raw_i7)
        keys = I7_C_KEYS
        return keys, {k: chart.get(k, "") for k in keys}
    raise ValueError(f"Unsupported ontology variant: {ontology_variant}")


def numericize_chart(keys: list[str], chart: dict[str, str]) -> list[float]:
    out: list[float] = []
    for key in keys:
        raw = str(chart.get(key, "") or "")
        mapping = I7_VALUE_MAPS.get(key, {})
        out.append(float(mapping.get(raw, -1)))
    return out


def count_matches(text: str, patterns: list[str]) -> int:
    total = 0
    for pat in patterns:
        total += len(re.findall(pat, text))
    return total


def build_language_features(text: str) -> list[float]:
    t = (text or "").strip()
    char_len = len(t)
    line_count = max(1, t.count("\n") + 1) if t else 0
    question_count = t.count("?") + t.count("？")
    list_marker_count = count_matches(t, [r"(?m)^\s*-\s", r"(?m)^\s*\d+[\.、)]", r"(?m)^\s*[•·]"])
    advice_marker_count = count_matches(t, [r"可以", r"建议", r"试试", r"不妨", r"常见", r"做法", r"办法"])
    reassurance_marker_count = count_matches(t, [r"没事", r"不必", r"不用", r"理解", r"明白", r"可以的", r"收到"])
    presence_marker_count = count_matches(t, [r"我在这里", r"我在这", r"陪着你", r"听着", r"陪你", r"我会在"])
    meta_control_marker_count = count_matches(t, [r"我会", r"保持", r"按.*方式", r"语气", r"回应方式", r"收住", r"克制"])
    first_person_count = count_matches(t, [r"我"])
    return [
        float(char_len),
        float(line_count),
        float(question_count),
        float(list_marker_count),
        float(advice_marker_count),
        float(reassurance_marker_count),
        float(presence_marker_count),
        float(meta_control_marker_count),
        float(first_person_count),
    ]


def build_mode_dataset(
    rows: list[dict[str, Any]],
    mode: str,
    oracle_rel_lookup: dict[tuple[str, str], dict[str, float]],
) -> dict[str, Any]:
    filtered = [row for row in rows if str(row.get("experiment_mode") or "") == mode]
    ontology_variant = parse_ontology_variant(mode)
    samples: list[dict[str, Any]] = []
    for row in filtered:
        rel_vec = build_relation_vec(row, oracle_rel_lookup)
        beh_vec = build_behavior_vec(row)
        raw_i7 = build_raw_i7_interface(row)
        if rel_vec is None or beh_vec is None or raw_i7 is None:
            continue
        chart_keys, ontology_chart = project_ontology_chart(raw_i7, ontology_variant)
        i7_vec = numericize_chart(chart_keys, ontology_chart)
        lang_vec = build_language_features(str(row.get("assistant_text") or ""))
        samples.append(
            {
                "case_id": row.get("case_id"),
                "family": family_from_case_id(str(row.get("case_id") or "")),
                "turn_idx": int(row.get("turn_idx", 0) or 0),
                "phase": row.get("phase"),
                "relation_raw4": rel_vec,
                "behavior_8d": beh_vec,
                "i7_numeric": i7_vec,
                "language_features": lang_vec,
            }
        )
    samples.sort(key=lambda x: (str(x["case_id"]), int(x["turn_idx"])))
    return {
        "experiment_mode": mode,
        "ontology_variant": ontology_variant,
        "i7_keys": chart_keys if samples else [],
        "language_feature_keys": LANG_KEYS,
        "samples": samples,
    }


def matrix_from_samples(samples: list[dict[str, Any]], key: str) -> np.ndarray:
    return np.array([sample[key] for sample in samples], dtype=float)


def zscore(X: np.ndarray) -> np.ndarray:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, keepdims=True)
    std = np.where(std < 1e-6, 1.0, std)
    return (X - mean) / std


def pairwise_distance_matrix(X: np.ndarray) -> np.ndarray:
    Xn = zscore(X)
    diffs = Xn[:, None, :] - Xn[None, :, :]
    return np.sqrt(np.sum(diffs * diffs, axis=2))


def upper_triangle_values(D: np.ndarray) -> np.ndarray:
    idx = np.triu_indices_from(D, k=1)
    return D[idx]


def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) != len(b) or len(a) == 0:
        return float("nan")
    a0 = a - a.mean()
    b0 = b - b.mean()
    denom = math.sqrt(float(np.sum(a0 * a0) * np.sum(b0 * b0)))
    if denom < 1e-12:
        return float("nan")
    return float(np.sum(a0 * b0) / denom)


def topk_neighbors(D: np.ndarray, k: int) -> list[list[int]]:
    neighbors: list[list[int]] = []
    for i in range(len(D)):
        order = np.argsort(D[i])
        keep = [int(j) for j in order if int(j) != i][:k]
        neighbors.append(keep)
    return neighbors


def avg_neighbor_overlap(D1: np.ndarray, D2: np.ndarray, k: int) -> float:
    n1 = topk_neighbors(D1, k)
    n2 = topk_neighbors(D2, k)
    overlaps = []
    for a, b in zip(n1, n2):
        if not a or not b:
            continue
        sa = set(a)
        sb = set(b)
        overlaps.append(len(sa & sb) / float(k))
    if not overlaps:
        return float("nan")
    return float(sum(overlaps) / len(overlaps))


def trajectory_smoothness(samples: list[dict[str, Any]], D: np.ndarray) -> dict[str, Any]:
    global_vals = upper_triangle_values(D)
    global_median = float(np.median(global_vals)) if len(global_vals) else float("nan")
    row_index = {(sample["case_id"], sample["turn_idx"]): idx for idx, sample in enumerate(samples)}
    step_distances: list[float] = []
    by_case: dict[str, list[tuple[int, int]]] = {}
    for sample in samples:
        by_case.setdefault(str(sample["case_id"]), []).append((int(sample["turn_idx"]), row_index[(sample["case_id"], sample["turn_idx"])]))
    for _, seq in by_case.items():
        seq.sort()
        for (_, a), (_, b) in zip(seq[:-1], seq[1:]):
            step_distances.append(float(D[a, b]))
    if not step_distances:
        return {"avg_step_distance": float("nan"), "avg_step_over_global_median": float("nan")}
    avg_step = float(sum(step_distances) / len(step_distances))
    ratio = avg_step / global_median if global_median and not math.isnan(global_median) and global_median > 1e-12 else float("nan")
    return {
        "avg_step_distance": round(avg_step, 4),
        "avg_step_over_global_median": round(ratio, 4) if not math.isnan(ratio) else None,
    }


def analyze_dataset(dataset: dict[str, Any], k: int) -> dict[str, Any]:
    samples = dataset["samples"]
    if not samples:
        return {
            "experiment_mode": dataset["experiment_mode"],
            "num_samples": 0,
            "error": "no samples available",
        }

    views = {
        "relation_raw4": matrix_from_samples(samples, "relation_raw4"),
        "behavior_8d": matrix_from_samples(samples, "behavior_8d"),
        "i7_numeric": matrix_from_samples(samples, "i7_numeric"),
        "language_features": matrix_from_samples(samples, "language_features"),
    }
    distances = {name: pairwise_distance_matrix(X) for name, X in views.items()}

    distance_corrs: dict[str, float | None] = {}
    neighbor_overlaps: dict[str, float | None] = {}
    names = list(views.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]
            key = f"{a}__vs__{b}"
            corr = pearson_corr(upper_triangle_values(distances[a]), upper_triangle_values(distances[b]))
            overlap = avg_neighbor_overlap(distances[a], distances[b], k)
            distance_corrs[key] = round(corr, 4) if not math.isnan(corr) else None
            neighbor_overlaps[key] = round(overlap, 4) if not math.isnan(overlap) else None

    smoothness = {name: trajectory_smoothness(samples, D) for name, D in distances.items()}

    return {
        "experiment_mode": dataset["experiment_mode"],
        "ontology_variant": dataset["ontology_variant"],
        "num_samples": len(samples),
        "families": sorted({sample["family"] for sample in samples}),
        "view_dims": {name: int(views[name].shape[1]) for name in views},
        "distance_matrix_correlations": distance_corrs,
        "neighbor_overlap_at_k": k,
        "neighbor_overlaps": neighbor_overlaps,
        "trajectory_smoothness": smoothness,
    }


def sanitize_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)


def build_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Shared Latent Manifold M1")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("- Compare the geometry of `relation`, `behavior`, `i7`, and language-side realization without assuming a one-way chain is correct.")
    lines.append("- Treat this as an M1 geometry-alignment pass: distance structure, neighborhood structure, and trajectory smoothness.")
    lines.append("")
    lines.append("## Important boundary")
    lines.append("")
    lines.append("- This first pass uses oracle behavior as the fixed analytic view when available.")
    lines.append("- The deploy view is mode-specific and is numericized from the mode's effective `i7` chart.")
    lines.append("- This is a geometry sanity check, not yet a learned shared-latent model.")
    lines.append("")
    for block in report["mode_reports"]:
        lines.append(f"## Mode: `{block['experiment_mode']}`")
        lines.append("")
        if block.get("error"):
            lines.append(f"- error: `{block['error']}`")
            lines.append("")
            continue
        lines.append(f"- ontology variant: `{block['ontology_variant']}`")
        lines.append(f"- samples: `{block['num_samples']}`")
        lines.append(f"- families: `{', '.join(block['families'])}`")
        lines.append("")
        lines.append("### Distance-matrix correlation")
        lines.append("")
        for key, value in sorted(block["distance_matrix_correlations"].items()):
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
        lines.append("### Neighbor overlap")
        lines.append("")
        lines.append(f"- k: `{block['neighbor_overlap_at_k']}`")
        for key, value in sorted(block["neighbor_overlaps"].items()):
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
        lines.append("### Trajectory smoothness")
        lines.append("")
        for key, value in sorted(block["trajectory_smoothness"].items()):
            lines.append(
                f"- `{key}`: avg_step=`{value['avg_step_distance']}`, "
                f"step/global_median=`{value['avg_step_over_global_median']}`"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--oracle-state-cases-json", default="paper_cases_oracle_state_exec_v3.json")
    parser.add_argument("--modes", nargs="+", required=True)
    parser.add_argument("--out-dir", default="paper_shared_manifold_m1_out")
    parser.add_argument("--knn-k", type=int, default=5)
    args = parser.parse_args()

    rows = load_rows(args.input_jsonl)
    oracle_rel_lookup = load_oracle_rel_lookup(args.oracle_state_cases_json)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    mode_reports: list[dict[str, Any]] = []
    for mode in args.modes:
        dataset = build_mode_dataset(rows, mode, oracle_rel_lookup)
        safe_name = sanitize_filename(mode)
        (out_dir / f"{safe_name}_dataset.json").write_text(
            json.dumps(dataset, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        mode_reports.append(analyze_dataset(dataset, args.knn_k))

    report = {
        "input_jsonl": str(args.input_jsonl),
        "knn_k": int(args.knn_k),
        "mode_reports": mode_reports,
    }
    (out_dir / "shared_manifold_m1_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "PAPER_SHARED_MANIFOLD_M1.md").write_text(
        build_markdown(report),
        encoding="utf-8",
    )
    print(f"Wrote {out_dir.resolve()}")


if __name__ == "__main__":
    main()
