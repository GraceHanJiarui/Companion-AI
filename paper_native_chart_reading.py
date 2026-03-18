import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


NATIVE_KEYS = ["behavior_8d", "i7_numeric", "language_features"]
CHART_KEYS = ["relation_raw4", "behavior_8d", "i7_numeric"]


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


def pairwise_distance_matrix(X: np.ndarray) -> np.ndarray:
    Xs, _, _ = standardize_fit(X)
    diffs = Xs[:, None, :] - Xs[None, :, :]
    return np.sqrt(np.sum(diffs * diffs, axis=2))


def upper_triangle_values(D: np.ndarray) -> np.ndarray:
    idx = np.triu_indices_from(D, k=1)
    return D[idx]


def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    a0 = a - a.mean()
    b0 = b - b.mean()
    denom = math.sqrt(float(np.sum(a0 * a0) * np.sum(b0 * b0)))
    if denom < 1e-12:
        return float("nan")
    return float(np.sum(a0 * b0) / denom)


def evaluate_dataset(dataset: dict[str, Any], latent_dim: int) -> dict[str, Any]:
    samples = dataset.get("samples", [])
    native_blocks = [matrix_from_samples(samples, key) for key in NATIVE_KEYS]
    X_native = np.concatenate(native_blocks, axis=1)
    pca = fit_pca(X_native, latent_dim)
    Z = transform_pca(X_native, pca)

    chart_readouts: dict[str, Any] = {}
    chart_geometry_alignment: dict[str, Any] = {}
    D_latent = pairwise_distance_matrix(Z)
    for key in CHART_KEYS:
        Y = matrix_from_samples(samples, key)
        W = fit_linear(Z, Y)
        Y_pred = predict_linear(Z, W)
        chart_readouts[key] = {
            "mae": round(mae(Y, Y_pred), 4),
            "rmse": round(rmse(Y, Y_pred), 4),
            "corr": round(corr_flat(Y, Y_pred), 4),
        }
        D_chart = pairwise_distance_matrix(Y)
        chart_geometry_alignment[key] = round(
            pearson_corr(upper_triangle_values(D_latent), upper_triangle_values(D_chart)),
            4,
        )

    return {
        "experiment_mode": dataset.get("experiment_mode"),
        "num_samples": len(samples),
        "latent_dim": latent_dim,
        "chart_readouts": chart_readouts,
        "chart_geometry_alignment": chart_geometry_alignment,
    }


def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Native Chart Reading", ""]
    lines.append("## Goal")
    lines.append("")
    lines.append("- Learn a native latent only from `behavior_8d + i7_numeric + language_features`.")
    lines.append("- Then ask how well the existing charts can be read out from that latent.")
    lines.append("- This treats `raw4`, `8D behavior`, and `i7` as candidate charts over the native latent, rather than as the starting ontology.")
    lines.append("")
    for block in report["dataset_reports"]:
        lines.append(f"## Dataset: `{block['experiment_mode']}`")
        lines.append("")
        lines.append(f"- latent_dim: `{block['latent_dim']}`")
        lines.append(f"- samples: `{block['num_samples']}`")
        lines.append("")
        lines.append("### Chart readout")
        lines.append("")
        for key, metrics in block["chart_readouts"].items():
            lines.append(
                f"- `{key}`: mae=`{metrics['mae']}`, rmse=`{metrics['rmse']}`, corr=`{metrics['corr']}`"
            )
        lines.append("")
        lines.append("### Chart geometry alignment with native latent")
        lines.append("")
        for key, value in block["chart_geometry_alignment"].items():
            lines.append(f"- `{key}`: `{value}`")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-jsons", nargs="+", required=True)
    parser.add_argument("--latent-dim", type=int, default=8)
    parser.add_argument("--out-dir", default="paper_native_chart_reading_out")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    reports = [evaluate_dataset(load_dataset(path), args.latent_dim) for path in args.dataset_jsons]
    full_report = {"dataset_reports": reports, "latent_dim": args.latent_dim}
    (out_dir / "native_chart_reading_report.json").write_text(
        json.dumps(full_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "PAPER_NATIVE_CHART_READING.md").write_text(
        build_markdown(full_report),
        encoding="utf-8",
    )
    print(f"Wrote {out_dir.resolve()}")


if __name__ == "__main__":
    main()
