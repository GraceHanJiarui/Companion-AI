import argparse
import itertools
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
                    "rel_dict": {k: float(rel.get(k, 0.0)) for k in RAW_REL_KEYS},
                    "beh": [float(beh.get(k, 0.0)) for k in BEH_KEYS],
                }
            )
    return rows


def build_representation(row: dict[str, Any], rep_name: str) -> tuple[list[float], list[str]]:
    rel = row["rel_dict"]
    b = rel["bond"]
    c = rel["care"]
    t = rel["trust"]
    s = rel["stability"]

    if rep_name.startswith("subset_"):
        keys = rep_name.split("_", 1)[1].split("+")
        return [rel[k] for k in keys], keys

    if rep_name == "raw4":
        return [b, c, t, s], RAW_REL_KEYS

    if rep_name == "aug5_permission":
        names = ["bond", "care", "trust", "stability", "permission"]
        permission = 0.45 * t + 0.35 * b + 0.20 * c
        return [b, c, t, s, permission], names

    if rep_name == "aug6_permission_warmth":
        names = ["bond", "care", "trust", "stability", "permission", "warmth_affordance"]
        permission = 0.45 * t + 0.35 * b + 0.20 * c
        warmth_affordance = 0.60 * c + 0.40 * b
        return [b, c, t, s, permission, warmth_affordance], names

    raise ValueError(f"Unknown representation: {rep_name}")


def build_feature_matrix(X: np.ndarray, feature_names: list[str], feature_set: str) -> tuple[np.ndarray, list[str]]:
    cols = [np.ones(len(X))]
    names = ["bias"]

    if feature_set in {"linear", "poly2"}:
        for idx, name in enumerate(feature_names):
            cols.append(X[:, idx])
            names.append(name)

    if feature_set == "poly2":
        n = X.shape[1]
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    cols.append(X[:, i] * X[:, j])
                    names.append(f"{feature_names[i]}_sq")
                else:
                    cols.append(X[:, i] * X[:, j])
                    names.append(f"{feature_names[i]}__{feature_names[j]}")

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
    return {
        "overall_mae": round(float(abs_err.mean()), 4),
        "mae_per_dim": {k: round(float(abs_err[:, i].mean()), 4) for i, k in enumerate(BEH_KEYS)},
    }


def loocv(Phi: np.ndarray, Y: np.ndarray, ridge: float = 1e-6) -> dict[str, Any]:
    preds = []
    for i in range(len(Phi)):
        mask = np.ones(len(Phi), dtype=bool)
        mask[i] = False
        W = fit_linear(Phi[mask], Y[mask], ridge=ridge)
        preds.append(predict(Phi[i : i + 1], W)[0])
    pred = np.array(preds, dtype=float)
    return eval_predictions(Y, pred)


def evaluate_representation(rows: list[dict[str, Any]], rep_name: str) -> dict[str, Any]:
    X_rows = []
    feature_names: list[str] | None = None
    for row in rows:
        x, names = build_representation(row, rep_name)
        X_rows.append(x)
        if feature_names is None:
            feature_names = names
    assert feature_names is not None

    X = np.array(X_rows, dtype=float)
    Y = np.array([row["beh"] for row in rows], dtype=float)

    out: dict[str, Any] = {
        "representation": rep_name,
        "num_dims": len(feature_names),
        "base_features": feature_names,
    }
    for feature_set in ["linear", "poly2"]:
        Phi, derived_names = build_feature_matrix(X, feature_names, feature_set)
        W = fit_linear(Phi, Y)
        train_pred = predict(Phi, W)
        out[feature_set] = {
            "num_model_features": len(derived_names),
            "train": eval_predictions(Y, train_pred),
            "loocv": loocv(Phi, Y),
        }
    return out


def candidate_representations() -> list[str]:
    reps: list[str] = []
    for k in [2, 3]:
        for combo in itertools.combinations(RAW_REL_KEYS, k):
            reps.append("subset_" + "+".join(combo))
    reps.extend(["raw4", "aug5_permission", "aug6_permission_warmth"])
    return reps


def build_markdown(results: dict[str, Any]) -> str:
    ranking = results["ranking"]
    reps = results["representations"]
    lines: list[str] = []
    lines.append("# Relation Dimensionality Validation")
    lines.append("")
    lines.append("## Goal")
    lines.append("")
    lines.append("- Test whether the current 4D relation space remains competitive after oracle expansion.")
    lines.append("- Compare lower-dimensional subsets against the current 4D relation space.")
    lines.append("- Compare the current 4D relation space against modestly augmented 5D/6D bases derived from the same four primitives.")
    lines.append("- This is a robustness validation, not yet a proof of the true optimal relation ontology.")
    lines.append("")
    lines.append("## Data")
    lines.append("")
    lines.append(f"- oracle rows: `{results['num_rows']}`")
    lines.append("")
    lines.append("## Ranking by LOOCV overall MAE")
    lines.append("")
    for feature_set in ["linear", "poly2"]:
        lines.append(f"### {feature_set}")
        lines.append("")
        for idx, item in enumerate(ranking[feature_set], start=1):
            lines.append(
                f"{idx}. `{item['representation']}` "
                f"(dims=`{item['num_dims']}`, loocv=`{item['loocv_overall_mae']}`)"
            )
        lines.append("")

    lines.append("## Detailed results")
    lines.append("")
    for rep_name, block in reps.items():
        lines.append(f"### {rep_name}")
        lines.append("")
        lines.append(f"- dims: `{block['num_dims']}`")
        lines.append(f"- base features: `{', '.join(block['base_features'])}`")
        lines.append(f"- linear loocv: `{block['linear']['loocv']['overall_mae']}`")
        lines.append(f"- poly2 loocv: `{block['poly2']['loocv']['overall_mae']}`")
        lines.append("")

    lines.append("## Reading guide")
    lines.append("")
    lines.append("- If a 2D/3D subset is close to or better than the full 4D basis, the current space may be over-specified.")
    lines.append("- If the full 4D basis remains clearly better than all 2D/3D subsets, that supports the necessity of retaining all four current axes.")
    lines.append("- If modest 5D/6D augmented bases meaningfully outperform the raw 4D basis, the current four dimensions may still be missing a reusable latent factor.")
    lines.append("- Because 5D/6D here are derived from the existing 4D labels, they do not yet prove a truly new annotated ontology; they only test whether a slightly richer basis helps.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-json", default="paper_cases_oracle_state_exec_v3.json")
    parser.add_argument("--out-json", default="paper_relation_dimensionality_validation_v1.json")
    parser.add_argument("--out-md", default="PAPER_RELATION_DIMENSIONALITY_VALIDATION.md")
    args = parser.parse_args()

    rows = load_oracle_rows(args.cases_json)
    rep_results: dict[str, Any] = {}
    for rep_name in candidate_representations():
        rep_results[rep_name] = evaluate_representation(rows, rep_name)

    ranking: dict[str, list[dict[str, Any]]] = {}
    for feature_set in ["linear", "poly2"]:
        ordered = sorted(
            (
                {
                    "representation": rep_name,
                    "num_dims": block["num_dims"],
                    "loocv_overall_mae": block[feature_set]["loocv"]["overall_mae"],
                }
                for rep_name, block in rep_results.items()
            ),
            key=lambda x: x["loocv_overall_mae"],
        )
        ranking[feature_set] = ordered

    results = {
        "num_rows": len(rows),
        "representations": rep_results,
        "ranking": ranking,
    }

    Path(args.out_json).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text(build_markdown(results), encoding="utf-8")
    print(f"Wrote {Path(args.out_json).resolve()}")
    print(f"Wrote {Path(args.out_md).resolve()}")


if __name__ == "__main__":
    main()
