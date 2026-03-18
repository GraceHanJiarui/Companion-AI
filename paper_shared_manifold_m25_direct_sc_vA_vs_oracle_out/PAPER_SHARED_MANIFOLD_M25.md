# Shared Latent Manifold M2.5

## What M2.5 adds

- M2 showed that a latent learned from `behavior + i7 + language` can reconstruct those views and predict `relation_raw4` back strongly.
- M2.5 adds a more direct inverse-manifold probe: does that same latent also preserve case-family structure and trajectory continuity?
- This is still a controlled probe rather than a final manifold claim. It is meant to test whether the shared latent is stable enough to justify deeper manifold work.

## Dataset: `explicit_rel_state_rel_to_interface_i7_sc_vA`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### latent_2

#### reconstruction

- `behavior_8d`: mae=`0.2946`, rmse=`0.4178`, corr=`0.9086`
- `i7_numeric`: mae=`0.1293`, rmse=`0.3591`, corr=`0.6958`
- `language_features`: mae=`0.5147`, rmse=`0.8043`, corr=`0.5942`

#### relation prediction from shared latent

- mae=`0.0363`, rmse=`0.0484`, corr=`0.9667`

#### family structure probe

- loocv_family_accuracy=`0.4111`, neighbor_purity_at_k=`0.4433`

#### latent trajectory smoothness

- avg_step=`2.9515`, step/global_median=`0.9042`, avg_turning=`1.3273`

### latent_3

#### reconstruction

- `behavior_8d`: mae=`0.279`, rmse=`0.3851`, corr=`0.9229`
- `i7_numeric`: mae=`0.1218`, rmse=`0.3309`, corr=`0.7497`
- `language_features`: mae=`0.4972`, rmse=`0.7255`, corr=`0.6882`

#### relation prediction from shared latent

- mae=`0.0357`, rmse=`0.048`, corr=`0.9672`

#### family structure probe

- loocv_family_accuracy=`0.3944`, neighbor_purity_at_k=`0.4233`

#### latent trajectory smoothness

- avg_step=`3.4114`, step/global_median=`0.9214`, avg_turning=`1.3275`

### latent_4

#### reconstruction

- `behavior_8d`: mae=`0.2627`, rmse=`0.361`, corr=`0.9326`
- `i7_numeric`: mae=`0.1123`, rmse=`0.2904`, corr=`0.8141`
- `language_features`: mae=`0.4298`, rmse=`0.6413`, corr=`0.7673`

#### relation prediction from shared latent

- mae=`0.0347`, rmse=`0.0464`, corr=`0.9693`

#### family structure probe

- loocv_family_accuracy=`0.4778`, neighbor_purity_at_k=`0.4667`

#### latent trajectory smoothness

- avg_step=`3.7092`, step/global_median=`0.918`, avg_turning=`1.3375`

### latent_5

#### reconstruction

- `behavior_8d`: mae=`0.233`, rmse=`0.3099`, corr=`0.9508`
- `i7_numeric`: mae=`0.1075`, rmse=`0.2814`, corr=`0.8266`
- `language_features`: mae=`0.3729`, rmse=`0.5642`, corr=`0.8257`

#### relation prediction from shared latent

- mae=`0.0336`, rmse=`0.0452`, corr=`0.971`

#### family structure probe

- loocv_family_accuracy=`0.4667`, neighbor_purity_at_k=`0.4556`

#### latent trajectory smoothness

- avg_step=`3.9947`, step/global_median=`0.9154`, avg_turning=`1.3202`

### latent_6

#### reconstruction

- `behavior_8d`: mae=`0.2298`, rmse=`0.3057`, corr=`0.9521`
- `i7_numeric`: mae=`0.1017`, rmse=`0.2697`, corr=`0.8421`
- `language_features`: mae=`0.3188`, rmse=`0.4624`, corr=`0.8867`

#### relation prediction from shared latent

- mae=`0.0333`, rmse=`0.0448`, corr=`0.9715`

#### family structure probe

- loocv_family_accuracy=`0.4778`, neighbor_purity_at_k=`0.4489`

#### latent trajectory smoothness

- avg_step=`4.1992`, step/global_median=`0.9022`, avg_turning=`1.3306`

## Dataset: `explicit_rel_state_projected_oracle_i7`

- ontology variant: `A`
- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### latent_2

#### reconstruction

- `behavior_8d`: mae=`0.2979`, rmse=`0.4204`, corr=`0.9074`
- `i7_numeric`: mae=`0.1816`, rmse=`0.3709`, corr=`0.7957`
- `language_features`: mae=`0.4758`, rmse=`0.7525`, corr=`0.6586`

#### relation prediction from shared latent

- mae=`0.0351`, rmse=`0.0471`, corr=`0.9684`

#### family structure probe

- loocv_family_accuracy=`0.3889`, neighbor_purity_at_k=`0.4922`

#### latent trajectory smoothness

- avg_step=`3.07`, step/global_median=`0.9257`, avg_turning=`1.343`

### latent_3

#### reconstruction

- `behavior_8d`: mae=`0.2941`, rmse=`0.4177`, corr=`0.9086`
- `i7_numeric`: mae=`0.1226`, rmse=`0.2599`, corr=`0.9055`
- `language_features`: mae=`0.4511`, rmse=`0.6887`, corr=`0.725`

#### relation prediction from shared latent

- mae=`0.0342`, rmse=`0.0462`, corr=`0.9696`

#### family structure probe

- loocv_family_accuracy=`0.3889`, neighbor_purity_at_k=`0.4733`

#### latent trajectory smoothness

- avg_step=`3.4992`, step/global_median=`0.9219`, avg_turning=`1.4083`

### latent_4

#### reconstruction

- `behavior_8d`: mae=`0.2874`, rmse=`0.3943`, corr=`0.919`
- `i7_numeric`: mae=`0.1192`, rmse=`0.2526`, corr=`0.911`
- `language_features`: mae=`0.3883`, rmse=`0.5921`, corr=`0.8058`

#### relation prediction from shared latent

- mae=`0.0335`, rmse=`0.0455`, corr=`0.9705`

#### family structure probe

- loocv_family_accuracy=`0.3778`, neighbor_purity_at_k=`0.4422`

#### latent trajectory smoothness

- avg_step=`3.8505`, step/global_median=`0.9216`, avg_turning=`1.3603`

### latent_5

#### reconstruction

- `behavior_8d`: mae=`0.2828`, rmse=`0.3899`, corr=`0.9208`
- `i7_numeric`: mae=`0.1172`, rmse=`0.2486`, corr=`0.9139`
- `language_features`: mae=`0.3439`, rmse=`0.4954`, corr=`0.8687`

#### relation prediction from shared latent

- mae=`0.0335`, rmse=`0.0454`, corr=`0.9706`

#### family structure probe

- loocv_family_accuracy=`0.3778`, neighbor_purity_at_k=`0.4289`

#### latent trajectory smoothness

- avg_step=`4.0676`, step/global_median=`0.9377`, avg_turning=`1.3749`

### latent_6

#### reconstruction

- `behavior_8d`: mae=`0.2248`, rmse=`0.2957`, corr=`0.9553`
- `i7_numeric`: mae=`0.1106`, rmse=`0.227`, corr=`0.9288`
- `language_features`: mae=`0.2979`, rmse=`0.4498`, corr=`0.8931`

#### relation prediction from shared latent

- mae=`0.03`, rmse=`0.0403`, corr=`0.977`

#### family structure probe

- loocv_family_accuracy=`0.4167`, neighbor_purity_at_k=`0.4811`

#### latent trajectory smoothness

- avg_step=`4.245`, step/global_median=`0.9148`, avg_turning=`1.3621`
