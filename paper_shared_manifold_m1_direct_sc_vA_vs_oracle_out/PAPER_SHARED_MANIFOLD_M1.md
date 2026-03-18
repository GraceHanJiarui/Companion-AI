# Shared Latent Manifold M1

## Goal

- Compare the geometry of `relation`, `behavior`, `i7`, and language-side realization without assuming a one-way chain is correct.
- Treat this as an M1 geometry-alignment pass: distance structure, neighborhood structure, and trajectory smoothness.

## Important boundary

- This first pass uses oracle behavior as the fixed analytic view when available.
- The deploy view is mode-specific and is numericized from the mode's effective `i7` chart.
- This is a geometry sanity check, not yet a learned shared-latent model.

## Mode: `explicit_rel_state_rel_to_interface_i7_sc_vA`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### Distance-matrix correlation

- `behavior_8d__vs__i7_numeric`: `0.06`
- `behavior_8d__vs__language_features`: `0.1148`
- `i7_numeric__vs__language_features`: `0.2191`
- `relation_raw4__vs__behavior_8d`: `0.3048`
- `relation_raw4__vs__i7_numeric`: `0.0837`
- `relation_raw4__vs__language_features`: `-0.0142`

### Neighbor overlap

- k: `5`
- `behavior_8d__vs__i7_numeric`: `0.0711`
- `behavior_8d__vs__language_features`: `0.0844`
- `i7_numeric__vs__language_features`: `0.0489`
- `relation_raw4__vs__behavior_8d`: `0.5822`
- `relation_raw4__vs__i7_numeric`: `0.0633`
- `relation_raw4__vs__language_features`: `0.0744`

### Trajectory smoothness

- `behavior_8d`: avg_step=`2.1533`, step/global_median=`0.7707`
- `i7_numeric`: avg_step=`1.2956`, step/global_median=`0.4828`
- `language_features`: avg_step=`3.6235`, step/global_median=`1.0844`
- `relation_raw4`: avg_step=`0.9187`, step/global_median=`0.3637`

## Mode: `explicit_rel_state_projected_oracle_i7`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### Distance-matrix correlation

- `behavior_8d__vs__i7_numeric`: `0.0745`
- `behavior_8d__vs__language_features`: `0.2516`
- `i7_numeric__vs__language_features`: `0.2537`
- `relation_raw4__vs__behavior_8d`: `0.3048`
- `relation_raw4__vs__i7_numeric`: `0.098`
- `relation_raw4__vs__language_features`: `0.0618`

### Neighbor overlap

- k: `5`
- `behavior_8d__vs__i7_numeric`: `0.0756`
- `behavior_8d__vs__language_features`: `0.1044`
- `i7_numeric__vs__language_features`: `0.05`
- `relation_raw4__vs__behavior_8d`: `0.5822`
- `relation_raw4__vs__i7_numeric`: `0.0589`
- `relation_raw4__vs__language_features`: `0.0967`

### Trajectory smoothness

- `behavior_8d`: avg_step=`2.1533`, step/global_median=`0.7707`
- `i7_numeric`: avg_step=`1.3416`, step/global_median=`0.5`
- `language_features`: avg_step=`3.6497`, step/global_median=`1.3103`
- `relation_raw4`: avg_step=`0.9187`, step/global_median=`0.3637`
