# Shared Latent Manifold M1

## Goal

- Compare the geometry of `relation`, `behavior`, `i7`, and language-side realization without assuming a one-way chain is correct.
- Treat this as an M1 geometry-alignment pass: distance structure, neighborhood structure, and trajectory smoothness.

## Important boundary

- This first pass uses oracle behavior as the fixed analytic view when available.
- The deploy view is mode-specific and is numericized from the mode's effective `i7` chart.
- This is a geometry sanity check, not yet a learned shared-latent model.

## Mode: `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### Distance-matrix correlation

- `behavior_8d__vs__i7_numeric`: `0.2404`
- `behavior_8d__vs__language_features`: `0.2223`
- `i7_numeric__vs__language_features`: `0.343`
- `relation_raw4__vs__behavior_8d`: `0.3048`
- `relation_raw4__vs__i7_numeric`: `0.3666`
- `relation_raw4__vs__language_features`: `0.0783`

### Neighbor overlap

- k: `5`
- `behavior_8d__vs__i7_numeric`: `0.1489`
- `behavior_8d__vs__language_features`: `0.1244`
- `i7_numeric__vs__language_features`: `0.07`
- `relation_raw4__vs__behavior_8d`: `0.5822`
- `relation_raw4__vs__i7_numeric`: `0.1411`
- `relation_raw4__vs__language_features`: `0.1144`

### Trajectory smoothness

- `behavior_8d`: avg_step=`2.1533`, step/global_median=`0.7707`
- `i7_numeric`: avg_step=`2.4358`, step/global_median=`0.756`
- `language_features`: avg_step=`3.5516`, step/global_median=`1.2358`
- `relation_raw4`: avg_step=`0.9187`, step/global_median=`0.3637`

## Mode: `explicit_rel_state_projected_oracle_behavior_i7`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### Distance-matrix correlation

- `behavior_8d__vs__i7_numeric`: `0.0745`
- `behavior_8d__vs__language_features`: `0.2067`
- `i7_numeric__vs__language_features`: `0.2983`
- `relation_raw4__vs__behavior_8d`: `0.3048`
- `relation_raw4__vs__i7_numeric`: `0.098`
- `relation_raw4__vs__language_features`: `0.0634`

### Neighbor overlap

- k: `5`
- `behavior_8d__vs__i7_numeric`: `0.0756`
- `behavior_8d__vs__language_features`: `0.1033`
- `i7_numeric__vs__language_features`: `0.06`
- `relation_raw4__vs__behavior_8d`: `0.5822`
- `relation_raw4__vs__i7_numeric`: `0.0589`
- `relation_raw4__vs__language_features`: `0.0967`

### Trajectory smoothness

- `behavior_8d`: avg_step=`2.1533`, step/global_median=`0.7707`
- `i7_numeric`: avg_step=`1.3416`, step/global_median=`0.5`
- `language_features`: avg_step=`3.6465`, step/global_median=`1.2881`
- `relation_raw4`: avg_step=`0.9187`, step/global_median=`0.3637`

## Mode: `explicit_rel_state_projected_oracle_i7`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### Distance-matrix correlation

- `behavior_8d__vs__i7_numeric`: `0.0745`
- `behavior_8d__vs__language_features`: `0.2389`
- `i7_numeric__vs__language_features`: `0.2863`
- `relation_raw4__vs__behavior_8d`: `0.3048`
- `relation_raw4__vs__i7_numeric`: `0.098`
- `relation_raw4__vs__language_features`: `0.0598`

### Neighbor overlap

- k: `5`
- `behavior_8d__vs__i7_numeric`: `0.0756`
- `behavior_8d__vs__language_features`: `0.1356`
- `i7_numeric__vs__language_features`: `0.0589`
- `relation_raw4__vs__behavior_8d`: `0.5822`
- `relation_raw4__vs__i7_numeric`: `0.0589`
- `relation_raw4__vs__language_features`: `0.1289`

### Trajectory smoothness

- `behavior_8d`: avg_step=`2.1533`, step/global_median=`0.7707`
- `i7_numeric`: avg_step=`1.3416`, step/global_median=`0.5`
- `language_features`: avg_step=`3.4867`, step/global_median=`1.239`
- `relation_raw4`: avg_step=`0.9187`, step/global_median=`0.3637`
