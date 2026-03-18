import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


RAW_REL_KEYS = ["bond", "care", "trust", "stability"]
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
                    "rel": [float(rel.get(k, 0.0)) for k in RAW_REL_KEYS],
                    "beh": [float(beh.get(k, 0.0)) for k in BEH_KEYS],
                }
            )
    return rows


def build_raw4_matrix(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.array([row["rel"] for row in rows], dtype=float)


def build_poly_feature_matrix(X: np.ndarray) -> tuple[np.ndarray, list[str]]:
    b = X[:, 0]
    c = X[:, 1]
    t = X[:, 2]
    s = X[:, 3]
    cols = [b, c, t, s]
    names = list(RAW_REL_KEYS)

    engineered = {
        "bond_care": b * c,
        "bond_trust": b * t,
        "bond_stability": b * s,
        "care_trust": c * t,
        "care_stability": c * s,
        "trust_stability": t * s,
        "bond_sq": b * b,
        "care_sq": c * c,
        "trust_sq": t * t,
        "stability_sq": s * s,
        "fragility": 1.0 - s,
        "warm_core": 0.6 * c + 0.4 * b,
        "permission_core": 0.45 * t + 0.35 * b + 0.20 * c,
    }
    for k, v in engineered.items():
        cols.append(v)
        names.append(k)

    Phi = np.stack(cols, axis=1)
    return Phi, names


def standardize_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, keepdims=True)
    std = np.where(std < 1e-6, 1.0, std)
    return (X - mean) / std, mean, std


def standardize_apply(X: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return (X - mean) / std


def fit_pca_basis(X: np.ndarray, latent_dim: int) -> dict[str, Any]:
    Xs, mean, std = standardize_fit(X)
    _, _, vh = np.linalg.svd(Xs, full_matrices=False)
    components = vh[:latent_dim].T
    return {
        "mean": mean,
        "std": std,
        "components": components,
    }


def transform_pca(X: np.ndarray, basis: dict[str, Any]) -> np.ndarray:
    Xs = standardize_apply(X, basis["mean"], basis["std"])
    return Xs @ basis["components"]


def fit_linear(Z: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    eye = np.eye(Zb.shape[1], dtype=float)
    eye[0, 0] = 0.0
    return np.linalg.solve(Zb.T @ Zb + ridge * eye, Zb.T @ Y)


def predict_linear(Z: np.ndarray, W: np.ndarray) -> np.ndarray:
    Zb = np.concatenate([np.ones((len(Z), 1)), Z], axis=1)
    pred = Zb @ W
    return np.clip(pred, 0.0, 1.0)


def eval_predictions(Y_true: np.ndarray, Y_pred: np.ndarray) -> dict[str, Any]:
    abs_err = np.abs(Y_true - Y_pred)
    return {
        "overall_mae": round(float(abs_err.mean()), 4),
        "mae_per_dim": {k: round(float(abs_err[:, i].mean()), 4) for i, k in enumerate(BEH_KEYS)},
    }


def loocv_latent(X_feat: np.ndarray, Y: np.ndarray, latent_dim: int) -> dict[str, Any]:
    preds = []
    for i in range(len(X_feat)):
        mask = np.ones(len(X_feat), dtype=bool)
        mask[i] = False
        basis = fit_pca_basis(X_feat[mask], latent_dim)
        Z_train = transform_pca(X_feat[mask], basis)
        W = fit_linear(Z_train, Y[mask])
        Z_test = transform_pca(X_feat[i : i + 1], basis)
        preds.append(predict_linear(Z_test, W)[0])
    pred = np.array(preds, dtype=float)
    return eval_predictions(Y, pred)


def fit_and_eval(X_feat: np.ndarray, Y: np.ndarray, latent_dim: int) -> dict[str, Any]:
    basis = fit_pca_basis(X_feat, latent_dim)
    Z = transform_pca(X_feat, basis)
    W = fit_linear(Z, Y)
    train_pred = predict_linear(Z, W)
    return {
        "train": eval_predictions(Y, train_pred),
        "loocv": loocv_latent(X_feat, Y, latent_dim),
        "basis_feature_count": int(X_feat.shape[1]),
    }


def build_markdown(results: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Relation Latent Dimensionality Search")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("- Search `2D/3D/4D/5D/6D` relation latents without hand-naming new factors first.")
    lines.append("- Use a shared higher-order feature space from the current raw4 labels, then learn unsupervised latent bases.")
    lines.append("- This tests whether a richer latent basis materially helps before any semantic interpretation is imposed.")
    lines.append("")
    lines.append("## Important boundary")
    lines.append("")
    lines.append("- These are not newly annotated relation ontologies.")
    lines.append("- `5D/6D` here mean learned latent coordinates in a higher-order feature space derived from the current raw4 labels.")
    lines.append("- Therefore this experiment can test whether richer latent dimensionality helps, but it cannot by itself discover a final human-readable ontology.")
    lines.append("")
    lines.append("## Data")
    lines.append("")
    lines.append(f"- oracle rows: `{results['num_rows']}`")
    lines.append(f"- source raw dimensions: `{results['raw_dim_count']}`")
    lines.append(f"- higher-order feature count: `{results['feature_count']}`")
    lines.append("")
    lines.append("## Ranking by LOOCV overall MAE")
    lines.append("")
    for item in results["ranking"]:
        lines.append(
            f"- latent `{item['latent_dim']}`: loocv `{item['loocv_overall_mae']}`"
        )
    lines.append("")
    lines.append("## Detailed results")
    lines.append("")
    for latent_dim, block in results["latent_results"].items():
        lines.append(f"### latent_{latent_dim}")
        lines.append("")
        lines.append(f"- train overall MAE: `{block['train']['overall_mae']}`")
        lines.append(f"- loocv overall MAE: `{block['loocv']['overall_mae']}`")
        lines.append("")
    lines.append("## Reading guide")
    lines.append("")
    lines.append("- If 5D/6D materially beat 4D, the current ontology may be missing explanatory structure.")
    lines.append("- If 4D is already at or near the optimum, then a stronger case exists for keeping the current four axes and interpreting them more carefully rather than immediately expanding the ontology.")
    lines.append("- If 2D/3D remain clearly weaker here as well, that strengthens the earlier subset-based result.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-json", default="paper_cases_oracle_state_exec_v3.json")
    parser.add_argument("--out-json", default="paper_relation_latent_dim_search_v1.json")
    parser.add_argument("--out-md", default="PAPER_RELATION_LATENT_DIM_SEARCH.md")
    args = parser.parse_args()

    rows = load_oracle_rows(args.cases_json)
    X_raw = build_raw4_matrix(rows)
    Y = np.array([row["beh"] for row in rows], dtype=float)
    X_feat, feature_names = build_poly_feature_matrix(X_raw)

    latent_results: dict[str, Any] = {}
    for latent_dim in [2, 3, 4, 5, 6]:
        latent_results[str(latent_dim)] = fit_and_eval(X_feat, Y, latent_dim)

    ranking = sorted(
        (
            {
                "latent_dim": int(k),
                "loocv_overall_mae": v["loocv"]["overall_mae"],
            }
            for k, v in latent_results.items()
        ),
        key=lambda x: x["loocv_overall_mae"],
    )

    results = {
        "num_rows": len(rows),
        "raw_dim_count": int(X_raw.shape[1]),
        "feature_count": int(X_feat.shape[1]),
        "feature_names": feature_names,
        "latent_results": latent_results,
        "ranking": ranking,
    }

    Path(args.out_json).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text(build_markdown(results), encoding="utf-8")
    print(f"Wrote {Path(args.out_json).resolve()}")
    print(f"Wrote {Path(args.out_md).resolve()}")


if __name__ == "__main__":
    main()
