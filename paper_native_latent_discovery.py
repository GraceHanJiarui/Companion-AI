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


def reconstruct_pca(Z: np.ndarray, pca: dict[str, Any]) -> np.ndarray:
    Xs_rec = Z @ pca["components"].T
    return Xs_rec * pca["std"] + pca["mean"]


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


def fit_linear(Z: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    eye = np.eye(Zb.shape[1], dtype=float)
    eye[0, 0] = 0.0
    return np.linalg.solve(Zb.T @ Zb + ridge * eye, Zb.T @ Y)


def predict_linear(Z: np.ndarray, W: np.ndarray) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    return Zb @ W


def trajectory_smoothness(samples: list[dict[str, Any]], Z: np.ndarray) -> dict[str, Any]:
    by_case: dict[str, list[tuple[int, int]]] = {}
    for idx, sample in enumerate(samples):
        by_case.setdefault(str(sample["case_id"]), []).append((int(sample["turn_idx"]), idx))

    global_vals: list[float] = []
    for i in range(len(Z)):
        for j in range(i + 1, len(Z)):
            global_vals.append(float(np.linalg.norm(Z[i] - Z[j])))
    global_median = float(np.median(global_vals)) if global_vals else float("nan")

    step_distances: list[float] = []
    turning_angles: list[float] = []
    for _, seq in by_case.items():
        seq.sort()
        indices = [idx for _, idx in seq]
        for a, b in zip(indices[:-1], indices[1:]):
            step_distances.append(float(np.linalg.norm(Z[a] - Z[b])))
        for a, b, c in zip(indices[:-2], indices[1:-1], indices[2:]):
            v1 = Z[b] - Z[a]
            v2 = Z[c] - Z[b]
            n1 = float(np.linalg.norm(v1))
            n2 = float(np.linalg.norm(v2))
            if n1 < 1e-12 or n2 < 1e-12:
                continue
            cos_sim = float(np.dot(v1, v2) / (n1 * n2))
            turning_angles.append(1.0 - max(-1.0, min(1.0, cos_sim)))

    avg_step = float(np.mean(step_distances)) if step_distances else float("nan")
    ratio = (
        avg_step / global_median
        if global_median and not math.isnan(global_median) and global_median > 1e-12
        else float("nan")
    )
    avg_turning = float(np.mean(turning_angles)) if turning_angles else float("nan")
    return {
        "avg_step_distance": round(avg_step, 4) if not math.isnan(avg_step) else None,
        "avg_step_over_global_median": round(ratio, 4) if not math.isnan(ratio) else None,
        "avg_turning": round(avg_turning, 4) if not math.isnan(avg_turning) else None,
    }


def family_probe(samples: list[dict[str, Any]], Z: np.ndarray, k: int) -> dict[str, Any]:
    families = [str(sample.get("family") or "other") for sample in samples]
    unique = sorted(set(families))
    if len(unique) < 2:
        return {"loocv_accuracy": None, "neighbor_purity_at_k": None}

    correct = 0
    purity_scores: list[float] = []
    for i in range(len(Z)):
        mask = np.ones(len(Z), dtype=bool)
        mask[i] = False
        train_Z = Z[mask]
        train_fam = [fam for j, fam in enumerate(families) if j != i]

        centroids: dict[str, np.ndarray] = {}
        for fam in unique:
            points = train_Z[[j for j, tf in enumerate(train_fam) if tf == fam]]
            if len(points) == 0:
                continue
            centroids[fam] = points.mean(axis=0)

        pred = min(
            centroids.items(),
            key=lambda item: float(np.linalg.norm(Z[i] - item[1])),
        )[0]
        if pred == families[i]:
            correct += 1

        distances = []
        for j in range(len(Z)):
            if i == j:
                continue
            distances.append((float(np.linalg.norm(Z[i] - Z[j])), families[j]))
        distances.sort(key=lambda item: item[0])
        neighbors = [fam for _, fam in distances[:k]]
        purity_scores.append(sum(1 for fam in neighbors if fam == families[i]) / float(len(neighbors)))

    return {
        "loocv_accuracy": round(correct / float(len(Z)), 4),
        "neighbor_purity_at_k": round(sum(purity_scores) / len(purity_scores), 4),
    }


def evaluate_dataset(dataset: dict[str, Any], latent_dims: list[int], knn_k: int) -> dict[str, Any]:
    samples = dataset.get("samples", [])
    X_views = {key: matrix_from_samples(samples, key) for key in VIEW_KEYS}
    X_blocks = []
    meta: dict[str, dict[str, int]] = {}
    start = 0
    for key in VIEW_KEYS:
        Xs, _, _ = standardize_fit(X_views[key])
        end = start + Xs.shape[1]
        X_blocks.append(Xs)
        meta[key] = {"start": start, "end": end}
        start = end
    X_joint = np.concatenate(X_blocks, axis=1)

    results: dict[str, Any] = {}
    Y_rel = matrix_from_samples(samples, "relation_raw4") if samples and "relation_raw4" in samples[0] else None
    for latent_dim in latent_dims:
        pca = fit_pca(X_joint, latent_dim)
        Z = transform_pca(X_joint, pca)
        X_rec = reconstruct_pca(Z, pca)

        recon = {}
        for key in VIEW_KEYS:
            block = X_joint[:, meta[key]["start"] : meta[key]["end"]]
            block_rec = X_rec[:, meta[key]["start"] : meta[key]["end"]]
            recon[key] = {
                "mae_standardized": round(mae(block, block_rec), 4),
                "rmse_standardized": round(rmse(block, block_rec), 4),
                "corr_standardized": round(corr_flat(block, block_rec), 4),
            }

        out = {
            "reconstruction": recon,
            "family_probe": family_probe(samples, Z, knn_k),
            "latent_trajectory_smoothness": trajectory_smoothness(samples, Z),
        }

        if Y_rel is not None:
            W = fit_linear(Z, Y_rel)
            Y_pred = predict_linear(Z, W)
            out["relation_prediction"] = {
                "mae": round(mae(Y_rel, Y_pred), 4),
                "rmse": round(rmse(Y_rel, Y_pred), 4),
                "corr": round(corr_flat(Y_rel, Y_pred), 4),
            }

        results[str(latent_dim)] = out

    return {
        "experiment_mode": dataset.get("experiment_mode"),
        "num_samples": len(samples),
        "families": sorted({str(sample.get("family") or "other") for sample in samples}),
        "latent_results": results,
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Native Latent Discovery", ""]
    lines.append("## Goal")
    lines.append("")
    lines.append("- Learn latent interaction structure directly from `behavior_8d + i7_numeric + language_features`.")
    lines.append("- Use dimensionality sweeps to ask how many latent dimensions are actually needed before reconstruction, family structure, and trajectory structure saturate.")
    lines.append("- Treat `relation_raw4` only as an optional readout target afterwards, not as a latent-construction input.")
    lines.append("")
    for block in report["dataset_reports"]:
        lines.append(f"## Dataset: `{block['experiment_mode']}`")
        lines.append("")
        lines.append(f"- samples: `{block['num_samples']}`")
        lines.append(f"- families: `{', '.join(block['families'])}`")
        lines.append("")
        for latent_dim, info in block["latent_results"].items():
            lines.append(f"### latent_{latent_dim}")
            lines.append("")
            for key, metrics in info["reconstruction"].items():
                lines.append(
                    f"- `{key}` reconstruction: mae=`{metrics['mae_standardized']}`, rmse=`{metrics['rmse_standardized']}`, corr=`{metrics['corr_standardized']}`"
                )
            fam = info["family_probe"]
            lines.append(
                f"- family probe: loocv_accuracy=`{fam['loocv_accuracy']}`, neighbor_purity_at_k=`{fam['neighbor_purity_at_k']}`"
            )
            smooth = info["latent_trajectory_smoothness"]
            lines.append(
                f"- trajectory: avg_step=`{smooth['avg_step_distance']}`, step/global_median=`{smooth['avg_step_over_global_median']}`, avg_turning=`{smooth['avg_turning']}`"
            )
            if "relation_prediction" in info:
                rel = info["relation_prediction"]
                lines.append(
                    f"- relation readout: mae=`{rel['mae']}`, rmse=`{rel['rmse']}`, corr=`{rel['corr']}`"
                )
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-jsons", nargs="+", required=True)
    parser.add_argument("--latent-dims", nargs="+", type=int, default=[2, 3, 4, 5, 6, 7, 8])
    parser.add_argument("--knn-k", type=int, default=5)
    parser.add_argument("--out-dir", default="paper_native_latent_discovery_out")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    reports = []
    for path in args.dataset_jsons:
        dataset = load_dataset(path)
        reports.append(evaluate_dataset(dataset, args.latent_dims, args.knn_k))

    full_report = {
        "latent_dims": args.latent_dims,
        "knn_k": args.knn_k,
        "dataset_reports": reports,
    }
    (out_dir / "native_latent_discovery_report.json").write_text(
        json.dumps(full_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "PAPER_NATIVE_LATENT_DISCOVERY.md").write_text(
        build_markdown(full_report),
        encoding="utf-8",
    )
    print(f"Wrote {out_dir.resolve()}")


if __name__ == "__main__":
    main()
