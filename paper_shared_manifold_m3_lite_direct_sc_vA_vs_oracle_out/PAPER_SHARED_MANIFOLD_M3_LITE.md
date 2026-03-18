# Shared Latent Manifold M3-lite

## Goal

- Fit one pooled latent basis across selected key routes.
- Compare case trajectories inside that shared latent space.
- Read M3-lite as a trajectory-distortion probe, not yet a full manifold claim.

- latent_dim: `6`

## Per-dataset trajectory summaries

### `explicit_rel_state_rel_to_interface_i7_sc_vA`

- cases: `30`
- family `boundary_repair`: num_cases=`5`, mean_step=`1.0828`, mean_turning=`1.4184`
- family `cooling`: num_cases=`5`, mean_step=`1.0631`, mean_turning=`1.1139`
- family `mixed_signal`: num_cases=`5`, mean_step=`1.193`, mean_turning=`1.1494`
- family `other`: num_cases=`5`, mean_step=`1.0362`, mean_turning=`1.3017`
- family `vulnerability`: num_cases=`5`, mean_step=`1.0835`, mean_turning=`1.0109`
- family `warm`: num_cases=`5`, mean_step=`1.2643`, mean_turning=`1.6029`

### `explicit_rel_state_projected_oracle_i7`

- cases: `30`
- family `boundary_repair`: num_cases=`5`, mean_step=`1.1548`, mean_turning=`1.5273`
- family `cooling`: num_cases=`5`, mean_step=`1.1749`, mean_turning=`1.4776`
- family `mixed_signal`: num_cases=`5`, mean_step=`1.1221`, mean_turning=`1.1517`
- family `other`: num_cases=`5`, mean_step=`0.9734`, mean_turning=`1.2637`
- family `vulnerability`: num_cases=`5`, mean_step=`1.2459`, mean_turning=`1.1929`
- family `warm`: num_cases=`5`, mean_step=`1.2472`, mean_turning=`1.6983`

## Pairwise path distortion

### `explicit_rel_state_rel_to_interface_i7_sc_vA` vs `explicit_rel_state_projected_oracle_i7`

- shared_cases: `30`
- overall_mean_case_path_distance: `0.7439`
- family `boundary_repair` mean_case_path_distance: `0.8781`
- family `cooling` mean_case_path_distance: `0.8873`
- family `mixed_signal` mean_case_path_distance: `0.5968`
- family `other` mean_case_path_distance: `0.7485`
- family `vulnerability` mean_case_path_distance: `0.6669`
- family `warm` mean_case_path_distance: `0.6858`
