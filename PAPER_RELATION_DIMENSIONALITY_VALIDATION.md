# Relation Dimensionality Validation

## Goal

- Test whether the current 4D relation space remains competitive after oracle expansion.
- Compare lower-dimensional subsets against the current 4D relation space.
- Compare the current 4D relation space against modestly augmented 5D/6D bases derived from the same four primitives.
- This is a robustness validation, not yet a proof of the true optimal relation ontology.

## Data

- oracle rows: `180`

## Ranking by LOOCV overall MAE

### linear

1. `raw4` (dims=`4`, loocv=`0.0216`)
2. `aug5_permission` (dims=`5`, loocv=`0.0216`)
3. `aug6_permission_warmth` (dims=`6`, loocv=`0.0216`)
4. `subset_bond+care+trust` (dims=`3`, loocv=`0.022`)
5. `subset_bond+care+stability` (dims=`3`, loocv=`0.0232`)
6. `subset_care+trust+stability` (dims=`3`, loocv=`0.0233`)
7. `subset_care+stability` (dims=`2`, loocv=`0.0235`)
8. `subset_bond+trust+stability` (dims=`3`, loocv=`0.024`)
9. `subset_bond+stability` (dims=`2`, loocv=`0.0244`)
10. `subset_trust+stability` (dims=`2`, loocv=`0.0249`)
11. `subset_bond+care` (dims=`2`, loocv=`0.025`)
12. `subset_care+trust` (dims=`2`, loocv=`0.0252`)
13. `subset_bond+trust` (dims=`2`, loocv=`0.0259`)

### poly2

1. `raw4` (dims=`4`, loocv=`0.0158`)
2. `aug5_permission` (dims=`5`, loocv=`0.0158`)
3. `aug6_permission_warmth` (dims=`6`, loocv=`0.0158`)
4. `subset_care+trust+stability` (dims=`3`, loocv=`0.0169`)
5. `subset_bond+care+stability` (dims=`3`, loocv=`0.0171`)
6. `subset_bond+care+trust` (dims=`3`, loocv=`0.0197`)
7. `subset_care+stability` (dims=`2`, loocv=`0.0198`)
8. `subset_bond+trust+stability` (dims=`3`, loocv=`0.0205`)
9. `subset_care+trust` (dims=`2`, loocv=`0.0213`)
10. `subset_bond+stability` (dims=`2`, loocv=`0.0215`)
11. `subset_bond+care` (dims=`2`, loocv=`0.023`)
12. `subset_trust+stability` (dims=`2`, loocv=`0.0235`)
13. `subset_bond+trust` (dims=`2`, loocv=`0.0242`)

## Detailed results

### subset_bond+care

- dims: `2`
- base features: `bond, care`
- linear loocv: `0.025`
- poly2 loocv: `0.023`

### subset_bond+trust

- dims: `2`
- base features: `bond, trust`
- linear loocv: `0.0259`
- poly2 loocv: `0.0242`

### subset_bond+stability

- dims: `2`
- base features: `bond, stability`
- linear loocv: `0.0244`
- poly2 loocv: `0.0215`

### subset_care+trust

- dims: `2`
- base features: `care, trust`
- linear loocv: `0.0252`
- poly2 loocv: `0.0213`

### subset_care+stability

- dims: `2`
- base features: `care, stability`
- linear loocv: `0.0235`
- poly2 loocv: `0.0198`

### subset_trust+stability

- dims: `2`
- base features: `trust, stability`
- linear loocv: `0.0249`
- poly2 loocv: `0.0235`

### subset_bond+care+trust

- dims: `3`
- base features: `bond, care, trust`
- linear loocv: `0.022`
- poly2 loocv: `0.0197`

### subset_bond+care+stability

- dims: `3`
- base features: `bond, care, stability`
- linear loocv: `0.0232`
- poly2 loocv: `0.0171`

### subset_bond+trust+stability

- dims: `3`
- base features: `bond, trust, stability`
- linear loocv: `0.024`
- poly2 loocv: `0.0205`

### subset_care+trust+stability

- dims: `3`
- base features: `care, trust, stability`
- linear loocv: `0.0233`
- poly2 loocv: `0.0169`

### raw4

- dims: `4`
- base features: `bond, care, trust, stability`
- linear loocv: `0.0216`
- poly2 loocv: `0.0158`

### aug5_permission

- dims: `5`
- base features: `bond, care, trust, stability, permission`
- linear loocv: `0.0216`
- poly2 loocv: `0.0158`

### aug6_permission_warmth

- dims: `6`
- base features: `bond, care, trust, stability, permission, warmth_affordance`
- linear loocv: `0.0216`
- poly2 loocv: `0.0158`

## Reading guide

- If a 2D/3D subset is close to or better than the full 4D basis, the current space may be over-specified.
- If the full 4D basis remains clearly better than all 2D/3D subsets, that supports the necessity of retaining all four current axes.
- If modest 5D/6D augmented bases meaningfully outperform the raw 4D basis, the current four dimensions may still be missing a reusable latent factor.
- Because 5D/6D here are derived from the existing 4D labels, they do not yet prove a truly new annotated ontology; they only test whether a slightly richer basis helps.

## Important boundary

- The 2D and 3D subset comparisons are the strongest part of this experiment.
- The current 5D/6D augmented representations are built by adding linear combinations of the original 4D variables:
  - `permission`
  - `warmth_affordance`
- Under the current linear / quadratic model family, those augmented representations are largely expressively redundant with the raw 4D basis.
- Therefore the present `5D/6D ~= 4D` result should **not** be over-read as proof that richer relation ontologies are unnecessary.
- What this experiment does support much more strongly is:
  - the current 4D space outperforms all tested 2D/3D subsets on the expanded 180-row oracle set;
  - therefore dropping one of the four current axes incurs a real explanatory cost.
