# Native Chart Reading

## Core question

Once a native latent is learned directly from:

- `behavior_8d`
- `i7_numeric`
- `language_features`

the next question is:

- how should existing charts such as `raw4`, `8D behavior`, and `i7` be read relative to that native latent?

## Goal

Do not treat `raw4 / 8D / i7` as the starting ontology.

Instead:

1. learn a native latent from multi-view realized structure;
2. treat current charts as candidate projections or readouts of that latent;
3. compare which charts are:
   - easiest to read out from the latent;
   - geometrically closest to the latent structure.

## Reading logic

- if `i7` is easiest to read out and most geometrically aligned, it is behaving like the strongest deploy chart;
- if `8D behavior` is also strongly readable, it remains a useful analytic chart;
- if `raw4` is readable but coarser, it is best interpreted as a compressed relation chart rather than the full native structure.
