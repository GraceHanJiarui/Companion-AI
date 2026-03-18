import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


VIEW_KEYS = ["behavior_8d", "i7_numeric", "language_features"]
TARGET_KEY = "relation_raw4"


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


def reconstruct_pca(Z: np.ndarray, pca: dict[str, Any]) -> np.ndarray:
    Xs_rec = Z @ pca["components"].T
    return Xs_rec * pca["std"] + pca["mean"]


def fit_linear(Z: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    eye = np.eye(Zb.shape[1], dtype=float)
    eye[0, 0] = 0.0
    return np.linalg.solve(Zb.T @ Zb + ridge * eye, Zb.T @ Y)


def predict_linear(Z: np.ndarray, W: np.ndarray) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    return Zb @ W


def mae(Y_true: np.ndarray, Y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(Y_true - Y_pred)))


def rmse(Y_true: np.ndarray, Y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((Y_true - Y_pred) ** 2)))


def corr_flat(a: np.ndarray, b: np.ndarray) -> float:
    x = a.reshape(-1).astype(float)
    y = b.reshape(-1).astype(float)
    x0 = x - x.mean()
    y0 = y - y.mean()
    denom = math.sqrt(float(np.sum(x0 * x0) * np.sum(y0 * y0)))
    if denom < 1e-12:
        return float("nan")
    return float(np.sum(x0 * y0) / denom)


def trajectory_smoothness(samples: list[dict[str, Any]], Z: np.ndarray) -> dict[str, Any]:
    row_index = {(sample["case_id"], sample["turn_idx"]): idx for idx, sample in enumerate(samples)}
    by_case: dict[str, list[tuple[int, int]]] = {}
    for sample in samples:
        by_case.setdefault(str(sample["case_id"]), []).append((int(sample["turn_idx"]), row_index[(sample["case_id"], sample["turn_idx"])]))
    step_distances: list[float] = []
    global_vals: list[float] = []
    for i in range(len(Z)):
        for j in range(i + 1, len(Z)):
            global_vals.append(float(np.linalg.norm(Z[i] - Z[j])))
    global_median = float(np.median(global_vals)) if global_vals else float("nan")
    for _, seq in by_case.items():
        seq.sort()
        for (_, a), (_, b) in zip(seq[:-1], seq[1:]):
            step_distances.append(float(np.linalg.norm(Z[a] - Z[b])))
    if not step_distances:
        return {"avg_step_distance": None, "avg_step_over_global_median": None}
    avg_step = float(sum(step_distances) / len(step_distances))
    ratio = avg_step / global_median if global_median and not math.isnan(global_median) and global_median > 1e-12 else float("nan")
    return {
        "avg_step_distance": round(avg_step, 4),
        "avg_step_over_global_median": round(ratio, 4) if not math.isnan(ratio) else None,
    }


def evaluate_dataset(dataset: dict[str, Any], latent_dims: list[int]) -> dict[str, Any]:
    samples = dataset.get("samples", [])
    X_views = {key: matrix_from_samples(samples, key) for key in VIEW_KEYS}
    Y_rel = matrix_from_samples(samples, TARGET_KEY)

    Xs_blocks = []
    block_meta: dict[str, dict[str, Any]] = {}
    start = 0
    for key in VIEW_KEYS:
        Xs, mean, std = standardize_fit(X_views[key])
        end = start + Xs.shape[1]
        Xs_blocks.append(Xs)
        block_meta[key] = {"mean": mean, "std": std, "start": start, "end": end}
        start = end
    X_joint = np.concatenate(Xs_blocks, axis=1)

    latent_results: dict[str, Any] = {}
    for latent_dim in latent_dims:
        pca = fit_pca(X_joint, latent_dim)
        Z = transform_pca(X_joint, pca)
        X_joint_rec = reconstruct_pca(Z, pca)

        recon_per_view: dict[str, Any] = {}
        for key in VIEW_KEYS:
            meta = block_meta[key]
            X_true = X_joint[:, meta["start"] : meta["end"]]
            X_rec = X_joint_rec[:, meta["start"] : meta["end"]]
            recon_per_view[key] = {
                "mae_standardized": round(mae(X_true, X_rec), 4),
                "rmse_standardized": round(rmse(X_true, X_rec), 4),
                "corr_standardized": round(corr_flat(X_true, X_rec), 4),
            }

        W_rel = fit_linear(Z, Y_rel)
        Y_rel_pred = predict_linear(Z, W_rel)
        relation_prediction = {
            "mae": round(mae(Y_rel, Y_rel_pred), 4),
            "rmse": round(rmse(Y_rel, Y_rel_pred), 4),
            "corr": round(corr_flat(Y_rel, Y_rel_pred), 4),
        }

        latent_results[str(latent_dim)] = {
            "reconstruction": recon_per_view,
            "relation_prediction": relation_prediction,
            "latent_trajectory_smoothness": trajectory_smoothness(samples, Z),
        }

    return {
        "experiment_mode": dataset.get("experiment_mode"),
        "ontology_variant": dataset.get("ontology_variant"),
        "num_samples": len(samples),
        "latent_results": latent_results,
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Shared Latent Manifold M2")
    lines.append("")
    lines.append("## What M2 adds beyond M1")
    lines.append("")
    lines.append("- M1 only asks whether views have similar pairwise geometry.")
    lines.append("- M2 asks whether one low-dimensional latent can jointly reconstruct behavior, deploy-chart structure, and language-side realization.")
    lines.append("- In this implementation, relation is not used to build the latent itself; relation is predicted back from the shared latent afterwards.")
    lines.append("- Therefore, if relation can be predicted from the shared latent, that is stronger evidence of a genuinely shared structure rather than a mere coding artifact.")
    lines.append("")
    for block in report["dataset_reports"]:
        lines.append(f"## Dataset: `{block['experiment_mode']}`")
        lines.append("")
        lines.append(f"- ontology variant: `{block['ontology_variant']}`")
        lines.append(f"- samples: `{block['num_samples']}`")
        lines.append("")
        for latent_dim, info in block["latent_results"].items():
            lines.append(f"### latent_{latent_dim}")
            lines.append("")
            lines.append("#### reconstruction")
            lines.append("")
            for key, metrics in info["reconstruction"].items():
                lines.append(
                    f"- `{key}`: mae=`{metrics['mae_standardized']}`, rmse=`{metrics['rmse_standardized']}`, corr=`{metrics['corr_standardized']}`"
                )
            lines.append("")
            rel = info["relation_prediction"]
            lines.append("#### relation prediction from shared latent")
            lines.append("")
            lines.append(
                f"- mae=`{rel['mae']}`, rmse=`{rel['rmse']}`, corr=`{rel['corr']}`"
            )
            smooth = info["latent_trajectory_smoothness"]
            lines.append("")
            lines.append("#### latent trajectory smoothness")
            lines.append("")
            lines.append(
                f"- avg_step=`{smooth['avg_step_distance']}`, step/global_median=`{smooth['avg_step_over_global_median']}`"
            )
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-jsons", nargs="+", required=True)
    parser.add_argument("--latent-dims", nargs="+", type=int, default=[2, 3, 4, 5, 6])
    parser.add_argument("--out-dir", default="paper_shared_manifold_m2_out")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_reports = []
    for path in args.dataset_jsons:
        dataset = load_dataset(path)
        report = evaluate_dataset(dataset, args.latent_dims)
        dataset_reports.append(report)

    full_report = {
        "dataset_reports": dataset_reports,
        "latent_dims": args.latent_dims,
    }
    (out_dir / "shared_manifold_m2_report.json").write_text(
        json.dumps(full_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "PAPER_SHARED_MANIFOLD_M2.md").write_text(
        build_markdown(full_report),
        encoding="utf-8",
    )
    print(f"Wrote {out_dir.resolve()}")


if __name__ == "__main__":
    main()
