# Relation-to-Behavior Fit Baseline

## Goal

- Estimate the best-fit explanatory upper bound of the current 4D relation space before introducing `scene/phase`.
- This experiment does not prove the relation space is correct; it tests how much oracle behavior it can explain under supervised fitting.

## linear

- `train_overall_mae`: `0.0178`
- `loocv_overall_mae`: `0.0254`

### LOOCV MAE per behavior dim

- `E`: `0.0375`
- `Q_clarify`: `0.0259`
- `Directness`: `0.0319`
- `T_w`: `0.0288`
- `Q_aff`: `0.0333`
- `Initiative`: `0.0239`
- `Disclosure_Content`: `0.0111`
- `Disclosure_Style`: `0.0111`

## poly2

- `train_overall_mae`: `0.0089`
- `loocv_overall_mae`: `0.0219`

### LOOCV MAE per behavior dim

- `E`: `0.0444`
- `Q_clarify`: `0.0182`
- `Directness`: `0.0417`
- `T_w`: `0.027`
- `Q_aff`: `0.0164`
- `Initiative`: `0.0134`
- `Disclosure_Content`: `0.0072`
- `Disclosure_Style`: `0.0072`

## mlp_h4

- `train_overall_mae`: `0.0101`
- `loocv_overall_mae`: `0.0249`

### LOOCV MAE per behavior dim

- `E`: `0.0438`
- `Q_clarify`: `0.0155`
- `Directness`: `0.0514`
- `T_w`: `0.0401`
- `Q_aff`: `0.0195`
- `Initiative`: `0.0149`
- `Disclosure_Content`: `0.007`
- `Disclosure_Style`: `0.007`

## mlp_h8

- `train_overall_mae`: `0.0057`
- `loocv_overall_mae`: `0.0269`

### LOOCV MAE per behavior dim

- `E`: `0.064`
- `Q_clarify`: `0.0105`
- `Directness`: `0.0654`
- `T_w`: `0.0288`
- `Q_aff`: `0.0228`
- `Initiative`: `0.0119`
- `Disclosure_Content`: `0.0059`
- `Disclosure_Style`: `0.0059`

## mlp_h12

- `train_overall_mae`: `0.0047`
- `loocv_overall_mae`: `0.0269`

### LOOCV MAE per behavior dim

- `E`: `0.0537`
- `Q_clarify`: `0.0187`
- `Directness`: `0.0529`
- `T_w`: `0.0362`
- `Q_aff`: `0.0211`
- `Initiative`: `0.0157`
- `Disclosure_Content`: `0.0083`
- `Disclosure_Style`: `0.0083`

## Interpretation Draft

- If even a stronger pure-relation fit still leaves large error on the key behavior dimensions, the current relation space is likely under-specified.
- If fit quality is already strong, the remaining issue is more likely projector family design than relation dimensionality.
- The main value of this step is to establish a cleaner baseline before introducing `scene/phase` conditioning.

## Boundary Of This Result

- The current dataset is still small (`18` oracle rows), so this result should be read as a strong small-sample signal, not as proof that higher-capacity models can never do better.
- `poly2` outperforming the current MLP baselines may partly reflect:
  - small-sample stability,
  - current oracle case distribution,
  - and the fact that the present oracle labeling style may itself be closer to a low-order explicit function.
- Therefore the present result supports:
  - "a simple explicit 4D fit already explains oracle behavior surprisingly well,"
  - and "we do not need to immediately blame missing relation dimensions or insufficient model capacity."
- It does **not** yet prove:
  - that `poly2` is globally optimal,
  - that 4D relation is the uniquely correct representation,
  - or that higher-capacity fits would not win under larger-scale data.
