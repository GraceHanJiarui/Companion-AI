import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


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


def load_oracle_rows(path: str) -> list[dict[str, Any]]:
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
                    "rel": [float(rel.get(k, 0.0)) for k in REL_KEYS],
                    "beh": [float(beh.get(k, 0.0)) for k in BEH_KEYS],
                }
            )
    return rows


def build_feature_matrix(X: np.ndarray, feature_set: str) -> tuple[np.ndarray, list[str]]:
    b = X[:, 0]
    c = X[:, 1]
    t = X[:, 2]
    s = X[:, 3]

    cols = [np.ones(len(X))]
    names = ["bias"]

    if feature_set in {"linear", "poly2"}:
        cols.extend([b, c, t, s])
        names.extend(REL_KEYS)

    if feature_set == "poly2":
        engineered = {
            "bond_care": b * c,
            "bond_trust": b * t,
            "care_trust": c * t,
            "trust_stability": t * s,
            "care_stability": c * s,
            "fragility": 1.0 - s,
            "warm_core": 0.6 * c + 0.4 * b,
            "permission_core": 0.45 * t + 0.35 * b + 0.20 * c,
            "bond_sq": b * b,
            "care_sq": c * c,
            "trust_sq": t * t,
            "stability_sq": s * s,
        }
        for k, v in engineered.items():
            cols.append(v)
            names.append(k)

    Phi = np.stack(cols, axis=1)
    return Phi, names


def fit_linear(Phi: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> np.ndarray:
    eye = np.eye(Phi.shape[1], dtype=float)
    eye[0, 0] = 0.0
    return np.linalg.solve(Phi.T @ Phi + ridge * eye, Phi.T @ Y)


def predict(Phi: np.ndarray, W: np.ndarray) -> np.ndarray:
    pred = Phi @ W
    return np.clip(pred, 0.0, 1.0)


def eval_predictions(Y_true: np.ndarray, Y_pred: np.ndarray) -> dict[str, Any]:
    abs_err = np.abs(Y_true - Y_pred)
    mae_per_dim = {k: round(float(abs_err[:, i].mean()), 4) for i, k in enumerate(BEH_KEYS)}
    return {
        "overall_mae": round(float(abs_err.mean()), 4),
        "mae_per_dim": mae_per_dim,
    }


def _standardize_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, keepdims=True)
    std = np.where(std < 1e-6, 1.0, std)
    return (X - mean) / std, mean, std


def _standardize_apply(X: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (X - mean) / std


def _mlp_forward(X: np.ndarray, params: dict[str, np.ndarray]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    z1 = X @ params["W1"] + params["b1"]
    h1 = np.tanh(z1)
    out = h1 @ params["W2"] + params["b2"]
    cache = {"X": X, "z1": z1, "h1": h1}
    return out, cache


def fit_mlp(
    X: np.ndarray,
    Y: np.ndarray,
    *,
    hidden_dim: int,
    seed: int = 7,
    steps: int = 4000,
    lr: float = 0.03,
    weight_decay: float = 1e-4,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    Xs, x_mean, x_std = _standardize_fit(X)
    Ys, y_mean, y_std = _standardize_fit(Y)

    W1 = rng.normal(0.0, 0.25, size=(Xs.shape[1], hidden_dim))
    b1 = np.zeros((1, hidden_dim), dtype=float)
    W2 = rng.normal(0.0, 0.25, size=(hidden_dim, Ys.shape[1]))
    b2 = np.zeros((1, Ys.shape[1]), dtype=float)

    params = {"W1": W1, "b1": b1, "W2": W2, "b2": b2}
    grads_sq = {k: np.zeros_like(v) for k, v in params.items()}

    for _ in range(steps):
        pred, cache = _mlp_forward(Xs, params)
        err = pred - Ys
        n = len(Xs)

        d_out = (2.0 / n) * err
        gW2 = cache["h1"].T @ d_out + weight_decay * params["W2"]
        gb2 = d_out.sum(axis=0, keepdims=True)
        dh = d_out @ params["W2"].T
        dz1 = dh * (1.0 - np.tanh(cache["z1"]) ** 2)
        gW1 = cache["X"].T @ dz1 + weight_decay * params["W1"]
        gb1 = dz1.sum(axis=0, keepdims=True)

        grads = {"W1": gW1, "b1": gb1, "W2": gW2, "b2": gb2}
        for k in params:
            grads_sq[k] = 0.95 * grads_sq[k] + 0.05 * (grads[k] ** 2)
            params[k] -= lr * grads[k] / (np.sqrt(grads_sq[k]) + 1e-8)

    return {
        "params": params,
        "x_mean": x_mean,
        "x_std": x_std,
        "y_mean": y_mean,
        "y_std": y_std,
        "hidden_dim": hidden_dim,
    }


def predict_mlp(X: np.ndarray, model: dict[str, Any]) -> np.ndarray:
    Xs = _standardize_apply(X, model["x_mean"], model["x_std"])
    pred_s, _ = _mlp_forward(Xs, model["params"])
    pred = pred_s * model["y_std"] + model["y_mean"]
    return np.clip(pred, 0.0, 1.0)


def loocv_mlp(
    X: np.ndarray,
    Y: np.ndarray,
    *,
    hidden_dim: int,
    seed: int = 7,
) -> dict[str, Any]:
    preds = []
    for i in range(len(X)):
        mask = np.ones(len(X), dtype=bool)
        mask[i] = False
        model = fit_mlp(X[mask], Y[mask], hidden_dim=hidden_dim, seed=seed + i)
        preds.append(predict_mlp(X[i : i + 1], model)[0])
    pred = np.array(preds, dtype=float)
    return eval_predictions(Y, pred)


def loocv(Phi: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> dict[str, Any]:
    preds = []
    for i in range(len(Phi)):
        mask = np.ones(len(Phi), dtype=bool)
        mask[i] = False
        W = fit_linear(Phi[mask], Y[mask], ridge=ridge)
        preds.append(predict(Phi[i : i + 1], W)[0])
    pred = np.array(preds, dtype=float)
    return eval_predictions(Y, pred)


def summarize_weights(W: np.ndarray, feature_names: list[str]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for j, beh_name in enumerate(BEH_KEYS):
        weights = {feature_names[i]: round(float(W[i, j]), 4) for i in range(len(feature_names))}
        out[beh_name] = weights
    return out


def build_markdown(results: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Relation-to-Behavior Fit Baseline")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("- Estimate the best-fit explanatory upper bound of the current 4D relation space before introducing `scene/phase`.")
    lines.append("- This experiment does not prove the relation space is correct; it tests how much oracle behavior it can explain under supervised fitting.")
    lines.append("")
    for model_name in [k for k in ["linear", "poly2", "mlp_h4", "mlp_h8", "mlp_h12"] if k in results]:
        block = results[model_name]
        lines.append(f"## {model_name}")
        lines.append("")
        lines.append(f"- `train_overall_mae`: `{block['train']['overall_mae']}`")
        lines.append(f"- `loocv_overall_mae`: `{block['loocv']['overall_mae']}`")
        lines.append("")
        lines.append("### LOOCV MAE per behavior dim")
        lines.append("")
        for k, v in block["loocv"]["mae_per_dim"].items():
            lines.append(f"- `{k}`: `{v}`")
        lines.append("")
    lines.append("## Interpretation Draft")
    lines.append("")
    lines.append("- If even a stronger pure-relation fit still leaves large error on the key behavior dimensions, the current relation space is likely under-specified.")
    lines.append("- If fit quality is already strong, the remaining issue is more likely projector family design than relation dimensionality.")
    lines.append("- The main value of this step is to establish a cleaner baseline before introducing `scene/phase` conditioning.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-json", default="paper_cases_oracle_state_exec_v1.json")
    parser.add_argument("--out-json", default="paper_relation_behavior_fit_v1.json")
    parser.add_argument("--out-md", default="PAPER_RELATION_BEHAVIOR_FIT.md")
    args = parser.parse_args()

    rows = load_oracle_rows(args.cases_json)
    X = np.array([r["rel"] for r in rows], dtype=float)
    Y = np.array([r["beh"] for r in rows], dtype=float)

    results: dict[str, Any] = {"num_rows": len(rows)}
    for feature_set in ["linear", "poly2"]:
        Phi, feature_names = build_feature_matrix(X, feature_set)
        W = fit_linear(Phi, Y)
        train_pred = predict(Phi, W)
        results[feature_set] = {
            "features": feature_names,
            "train": eval_predictions(Y, train_pred),
            "loocv": loocv(Phi, Y),
            "weights": summarize_weights(W, feature_names),
            "deployable": {
                "type": "linear",
                "features": feature_names,
                "weights_matrix": [[float(x) for x in row] for row in W.tolist()],
            },
        }

    for hidden_dim in [4, 8, 12]:
        model_name = f"mlp_h{hidden_dim}"
        model = fit_mlp(X, Y, hidden_dim=hidden_dim, seed=7 + hidden_dim)
        train_pred = predict_mlp(X, model)
        results[model_name] = {
            "hidden_dim": hidden_dim,
            "train": eval_predictions(Y, train_pred),
            "loocv": loocv_mlp(X, Y, hidden_dim=hidden_dim, seed=7 + hidden_dim),
            "deployable": {
                "type": "mlp",
                "hidden_dim": hidden_dim,
                "x_mean": [float(x) for x in model["x_mean"].reshape(-1).tolist()],
                "x_std": [float(x) for x in model["x_std"].reshape(-1).tolist()],
                "y_mean": [float(x) for x in model["y_mean"].reshape(-1).tolist()],
                "y_std": [float(x) for x in model["y_std"].reshape(-1).tolist()],
                "params": {
                    "W1": [[float(x) for x in row] for row in model["params"]["W1"].tolist()],
                    "b1": [float(x) for x in model["params"]["b1"].reshape(-1).tolist()],
                    "W2": [[float(x) for x in row] for row in model["params"]["W2"].tolist()],
                    "b2": [float(x) for x in model["params"]["b2"].reshape(-1).tolist()],
                },
            },
        }

    Path(args.out_json).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text(build_markdown(results), encoding="utf-8")
    print(f"Wrote {Path(args.out_json).resolve()}")
    print(f"Wrote {Path(args.out_md).resolve()}")


if __name__ == "__main__":
    main()
