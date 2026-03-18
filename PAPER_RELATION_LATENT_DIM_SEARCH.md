# Relation Latent Dimensionality Search

## Scope

This experiment deliberately avoids hand-defining new 5D/6D relation factors first.

Instead it asks a narrower question:

- if we allow a richer latent basis derived from the current raw4 labels,
- what latent dimensionality best explains oracle behavior?

This is meant to avoid prematurely imposing semantic interpretations on extra factors.

## Setup

Data:

- `180` oracle rows from:
  - [paper_cases_oracle_state_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v3.json)

Source variables:

- current raw4 relation labels:
  - `bond`
  - `care`
  - `trust`
  - `stability`

Shared higher-order feature space:

- `17` features built from raw4
- including:
  - first-order terms
  - pairwise interactions
  - squared terms
  - `fragility`
  - `warm_core`
  - `permission_core`

Method:

- fit unsupervised PCA-style latent bases of size:
  - `2D`
  - `3D`
  - `4D`
  - `5D`
  - `6D`
- then regress latent coordinates to the 8D oracle behavior target
- evaluate with LOOCV MAE

## Results

LOOCV overall MAE:

- latent `2`: `0.0235`
- latent `3`: `0.0230`
- latent `4`: `0.0214`
- latent `5`: `0.0200`
- latent `6`: `0.0200`

Ranking:

1. `5D`
2. `6D`
3. `4D`
4. `3D`
5. `2D`

## Main reading

Three things look robust:

1. `2D/3D` are clearly weaker than `4D`
2. `4D` remains a strong latent dimensionality, not an obviously over-large one
3. `5D/6D` provide a small but real improvement over `4D`

This is a more informative result than the earlier deterministic 5D/6D augmentation test.

The earlier test only showed:

- simple hand-constructed extra coordinates did not beat raw4

The current latent search shows something stronger:

- a slightly richer latent basis **can** improve explanatory fit,
- but the gain is modest rather than dramatic.

## What this supports

- the current 4D relation space is a robust explanatory basis;
- however, it is probably not the final optimum if the goal is pure explanation of oracle behavior;
- a latent space around `5D` looks like the current best candidate for further investigation.

## What this does not yet support

- that there is already a human-readable 5D ontology;
- that the extra latent dimension has a settled semantic meaning;
- that the project should immediately replace raw4 with a new deployed 5D controller.

## Current best use of this result

The cleanest next move is:

1. keep `raw4` as the paper's current interpretable explanatory basis;
2. acknowledge that a `5D` latent basis gives a modest explanatory gain;
3. only now begin inspecting the learned latent structure to ask whether a genuinely new semantic factor is present.
