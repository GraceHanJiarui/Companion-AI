import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


VIEW_KEYS = ["behavior_8d", "i7_numeric", "language_features"]


def load_dataset(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def matrix_from_samples(samples: list[dict[str, Any]], key: str) -> np.ndarray:
    return np.array([sample[key] for sample in samples], dtype=float)


def standardize_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, keepdims=True)
    std = np.where(std < 1e-6, 1.0, std)
    return (X - mean) / std, mean, std


def standardize_apply(X: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (X - mean) / std


def fit_pca(X: np.ndarray, latent_dim: int) -> dict[str, Any]:
    Xs, mean, std = standardize_fit(X)
    _, _, vh = np.linalg.svd(Xs, full_matrices=False)
    components = vh[:latent_dim].T
    return {"mean": mean, "std": std, "components": components}


def transform_pca(X: np.ndarray, pca: dict[str, Any]) -> np.ndarray:
    Xs = standardize_apply(X, pca["mean"], pca["std"])
    return Xs @ pca["components"]


def pooled_view_matrix(datasets: list[dict[str, Any]]) -> np.ndarray:
    blocks = []
    for dataset in datasets:
        samples = dataset.get("samples", [])
        if not samples:
            continue
        views = [matrix_from_samples(samples, key) for key in VIEW_KEYS]
        blocks.append(np.concatenate(views, axis=1))
    if not blocks:
        raise ValueError("No samples found across datasets.")
    return np.concatenate(blocks, axis=0)


def dataset_joint_matrix(dataset: dict[str, Any]) -> np.ndarray:
    samples = dataset.get("samples", [])
    views = [matrix_from_samples(samples, key) for key in VIEW_KEYS]
    return np.concatenate(views, axis=1)


def group_case_indices(samples: list[dict[str, Any]]) -> dict[str, list[int]]:
    by_case: dict[str, list[tuple[int, int]]] = {}
    for idx, sample in enumerate(samples):
        by_case.setdefault(str(sample["case_id"]), []).append((int(sample["turn_idx"]), idx))
    out: dict[str, list[int]] = {}
    for case_id, seq in by_case.items():
        seq.sort()
        out[case_id] = [idx for _, idx in seq]
    return out


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


def normalize_path(path: np.ndarray) -> np.ndarray:
    centered = path - path.mean(axis=0, keepdims=True)
    norm = float(np.sqrt(np.mean(np.sum(centered * centered, axis=1))))
    if norm < 1e-12:
        return centered
    return centered / norm


def path_metrics(path: np.ndarray) -> dict[str, Any]:
    steps = [float(np.linalg.norm(path[i + 1] - path[i])) for i in range(len(path) - 1)]
    turns: list[float] = []
    for a, b, c in zip(path[:-2], path[1:-1], path[2:]):
        v1 = b - a
        v2 = c - b
        n1 = float(np.linalg.norm(v1))
        n2 = float(np.linalg.norm(v2))
        if n1 < 1e-12 or n2 < 1e-12:
            continue
        cos_sim = float(np.dot(v1, v2) / (n1 * n2))
        turns.append(1.0 - max(-1.0, min(1.0, cos_sim)))
    return {
        "mean_step": round(float(np.mean(steps)) if steps else 0.0, 4),
        "mean_turning": round(float(np.mean(turns)) if turns else 0.0, 4),
        "steps": [round(x, 4) for x in steps],
    }


def dataset_trajectory_summary(dataset: dict[str, Any], Z: np.ndarray) -> dict[str, Any]:
    samples = dataset.get("samples", [])
    case_indices = group_case_indices(samples)
    case_metrics: dict[str, Any] = {}
    family_aggregate: dict[str, list[np.ndarray]] = {}
    for case_id, indices in case_indices.items():
        path = Z[indices]
        fam = family_from_case_id(case_id)
        case_metrics[case_id] = {
            "family": fam,
            "num_points": len(indices),
            "path_metrics": path_metrics(path),
        }
        family_aggregate.setdefault(fam, []).append(path)

    family_profiles: dict[str, Any] = {}
    for fam, paths in family_aggregate.items():
        min_len = min(len(path) for path in paths)
        trimmed = [normalize_path(path[:min_len]) for path in paths]
        proto = np.mean(np.stack(trimmed, axis=0), axis=0)
        family_profiles[fam] = {
            "num_cases": len(paths),
            "path_metrics": path_metrics(proto),
        }

    return {
        "num_cases": len(case_metrics),
        "case_metrics": case_metrics,
        "family_profiles": family_profiles,
    }


def pairwise_dataset_path_distortion(
    left_name: str,
    left_samples: list[dict[str, Any]],
    left_Z: np.ndarray,
    right_name: str,
    right_samples: list[dict[str, Any]],
    right_Z: np.ndarray,
) -> dict[str, Any]:
    left_cases = group_case_indices(left_samples)
    right_cases = group_case_indices(right_samples)
    shared_cases = sorted(set(left_cases) & set(right_cases))

    case_distances: dict[str, float] = {}
    family_distances: dict[str, list[float]] = {}
    for case_id in shared_cases:
        left_path = left_Z[left_cases[case_id]]
        right_path = right_Z[right_cases[case_id]]
        m = min(len(left_path), len(right_path))
        if m < 2:
            continue
        left_norm = normalize_path(left_path[:m])
        right_norm = normalize_path(right_path[:m])
        dist = float(np.mean(np.linalg.norm(left_norm - right_norm, axis=1)))
        case_distances[case_id] = round(dist, 4)
        fam = family_from_case_id(case_id)
        family_distances.setdefault(fam, []).append(dist)

    family_summary = {
        fam: round(float(np.mean(vals)), 4) for fam, vals in sorted(family_distances.items()) if vals
    }
    overall = round(float(np.mean(list(case_distances.values()))), 4) if case_distances else None
    return {
        "left": left_name,
        "right": right_name,
        "num_shared_cases": len(case_distances),
        "overall_mean_case_path_distance": overall,
        "family_mean_case_path_distance": family_summary,
        "case_path_distance": case_distances,
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Shared Latent Manifold M3-lite")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("- Fit one pooled latent basis across selected key routes.")
    lines.append("- Compare case trajectories inside that shared latent space.")
    lines.append("- Read M3-lite as a trajectory-distortion probe, not yet a full manifold claim.")
    lines.append("")
    lines.append(f"- latent_dim: `{report['latent_dim']}`")
    lines.append("")
    lines.append("## Per-dataset trajectory summaries")
    lines.append("")
    for block in report["dataset_summaries"]:
        lines.append(f"### `{block['experiment_mode']}`")
        lines.append("")
        lines.append(f"- cases: `{block['num_cases']}`")
        for fam, info in sorted(block["family_profiles"].items()):
            metrics = info["path_metrics"]
            lines.append(
                f"- family `{fam}`: num_cases=`{info['num_cases']}`, mean_step=`{metrics['mean_step']}`, mean_turning=`{metrics['mean_turning']}`"
            )
        lines.append("")
    lines.append("## Pairwise path distortion")
    lines.append("")
    for comp in report["pairwise_distortion"]:
        lines.append(f"### `{comp['left']}` vs `{comp['right']}`")
        lines.append("")
        lines.append(f"- shared_cases: `{comp['num_shared_cases']}`")
        lines.append(f"- overall_mean_case_path_distance: `{comp['overall_mean_case_path_distance']}`")
        for fam, value in comp["family_mean_case_path_distance"].items():
            lines.append(f"- family `{fam}` mean_case_path_distance: `{value}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-jsons", nargs="+", required=True)
    parser.add_argument("--latent-dim", type=int, default=6)
    parser.add_argument("--out-dir", default="paper_shared_manifold_m3_lite_out")
    args = parser.parse_args()

    datasets = [load_dataset(path) for path in args.dataset_jsons]
    pooled = pooled_view_matrix(datasets)
    pca = fit_pca(pooled, args.latent_dim)

    dataset_summaries = []
    dataset_latents: list[tuple[str, list[dict[str, Any]], np.ndarray]] = []
    for dataset in datasets:
        joint = dataset_joint_matrix(dataset)
        Z = transform_pca(joint, pca)
        summary = dataset_trajectory_summary(dataset, Z)
        summary["experiment_mode"] = dataset.get("experiment_mode")
        dataset_summaries.append(summary)
        dataset_latents.append((str(dataset.get("experiment_mode")), dataset.get("samples", []), Z))

    pairwise = []
    for i in range(len(dataset_latents)):
        for j in range(i + 1, len(dataset_latents)):
            left_name, left_samples, left_Z = dataset_latents[i]
            right_name, right_samples, right_Z = dataset_latents[j]
            pairwise.append(
                pairwise_dataset_path_distortion(
                    left_name,
                    left_samples,
                    left_Z,
                    right_name,
                    right_samples,
                    right_Z,
                )
            )

    report = {
        "latent_dim": args.latent_dim,
        "dataset_summaries": dataset_summaries,
        "pairwise_distortion": pairwise,
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "shared_manifold_m3_lite_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "PAPER_SHARED_MANIFOLD_M3_LITE.md").write_text(
        build_markdown(report),
        encoding="utf-8",
    )
    print(f"Wrote {out_dir.resolve()}")


if __name__ == "__main__":
    main()
