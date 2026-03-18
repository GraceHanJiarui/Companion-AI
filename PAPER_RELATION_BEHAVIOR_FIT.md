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

## Interpretation Draft

- If even a stronger pure-relation fit still leaves large error on the key behavior dimensions, the current relation space is likely under-specified.
- If fit quality is already strong, the remaining issue is more likely projector family design than relation dimensionality.
- The main value of this step is to establish a cleaner baseline before introducing `scene/phase` conditioning.
