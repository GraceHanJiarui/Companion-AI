# Native Latent Discovery

## Core question

The core research question is no longer:

- whether `4D relation -> 8D behavior -> i7` is the final true ontology.

It is now better stated as:

- can we learn a lower-dimensional latent interaction structure directly from:
  - `behavior_8d`
  - `i7_numeric`
  - `language_features`
- and then ask how existing charts such as `raw4`, `8D behavior`, and `i7` relate to that latent?

## Why this is the right next step

This is the more native version of the question that has been motivating the manifold line all along:

- do not start from hand-defined relation dimensions and then prove them against downstream views;
- instead start from the multi-view structure that is already closest to realized interaction:
  - analytic behavior
  - deploy chart
  - realized language
- then ask how many latent dimensions are actually needed before reconstruction quality, family structure, and trajectory structure saturate.

## Minimal first-pass experiment

Learn a latent only from:

- `behavior_8d`
- `i7_numeric`
- `language_features`

Do not use `relation_raw4` to construct the latent.

Then sweep latent dimensionality:

- `2D`
- `3D`
- `4D`
- `5D`
- `6D`
- `7D`
- `8D`

For each latent size, evaluate:

1. reconstruction quality for:
   - `behavior_8d`
   - `i7_numeric`
   - `language_features`
2. family structure:
   - leave-one-out family prediction
   - neighbor purity
3. trajectory structure:
   - average path step size
   - average turning
4. optional auxiliary reading:
   - how well `relation_raw4` can be predicted back afterwards

## Main decision rule

The key question is:

- at what latent dimensionality do we get most of the recoverable multi-view interaction structure?

Interpretation:

- if a very small latent works, the system may be overparameterized at the chart level;
- if a medium latent such as `5D-6D` works best, that suggests a richer shared structure than the current `raw4` chart captures;
- if reconstruction improves but family / trajectory structure does not, then the latent may be fitting noise rather than a meaningful interaction manifold.

## Project role

This line should now be treated as the main theory-facing continuation of the paper.

By contrast:

- further deploy-interface micro-variation work should be treated as lower-priority applied follow-up;
- the current `4D / 8D / i7` stack should be retained as a useful chart decomposition, not as the final ontological commitment.
