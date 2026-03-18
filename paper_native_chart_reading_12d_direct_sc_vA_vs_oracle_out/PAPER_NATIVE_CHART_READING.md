# Native Chart Reading

## Goal

- Learn a native latent only from `behavior_8d + i7_numeric + language_features`.
- Then ask how well the existing charts can be read out from that latent.
- This treats `raw4`, `8D behavior`, and `i7` as candidate charts over the native latent, rather than as the starting ontology.

## Dataset: `explicit_rel_state_rel_to_interface_i7_sc_vA`

- latent_dim: `12`
- samples: `180`

### Chart readout

- `relation_raw4`: mae=`0.023`, rmse=`0.0311`, corr=`0.9864`
- `behavior_8d`: mae=`0.0051`, rmse=`0.0071`, corr=`0.9982`
- `i7_numeric`: mae=`0.0112`, rmse=`0.0331`, corr=`0.9862`

### Chart geometry alignment with native latent

- `relation_raw4`: `0.2`
- `behavior_8d`: `0.4002`
- `i7_numeric`: `0.3289`

## Dataset: `explicit_rel_state_projected_oracle_i7`

- latent_dim: `12`
- samples: `180`

### Chart readout

- `relation_raw4`: mae=`0.0226`, rmse=`0.0305`, corr=`0.9869`
- `behavior_8d`: mae=`0.0039`, rmse=`0.0055`, corr=`0.9989`
- `i7_numeric`: mae=`0.0095`, rmse=`0.0255`, corr=`0.9987`

### Chart geometry alignment with native latent

- `relation_raw4`: `0.2369`
- `behavior_8d`: `0.5505`
- `i7_numeric`: `0.2779`
