# Shared Latent Manifold M2

## What M2 adds beyond M1

- M1 only asks whether views have similar pairwise geometry.
- M2 asks whether one low-dimensional latent can jointly reconstruct behavior, deploy-chart structure, and language-side realization.
- In this implementation, relation is not used to build the latent itself; relation is predicted back from the shared latent afterwards.
- Therefore, if relation can be predicted from the shared latent, that is stronger evidence of a genuinely shared structure rather than a mere coding artifact.

## Dataset: `explicit_rel_state_rel_to_interface_i7_sc_vA`

- ontology variant: `A`
- samples: `180`

### latent_2

#### reconstruction

- `behavior_8d`: mae=`0.2946`, rmse=`0.4178`, corr=`0.9086`
- `i7_numeric`: mae=`0.1293`, rmse=`0.3591`, corr=`0.6958`
- `language_features`: mae=`0.5147`, rmse=`0.8043`, corr=`0.5942`

#### relation prediction from shared latent

- mae=`0.0363`, rmse=`0.0484`, corr=`0.9667`

#### latent trajectory smoothness

- avg_step=`2.9515`, step/global_median=`0.9042`

### latent_3

#### reconstruction

- `behavior_8d`: mae=`0.279`, rmse=`0.3851`, corr=`0.9229`
- `i7_numeric`: mae=`0.1218`, rmse=`0.3309`, corr=`0.7497`
- `language_features`: mae=`0.4972`, rmse=`0.7255`, corr=`0.6882`

#### relation prediction from shared latent

- mae=`0.0357`, rmse=`0.048`, corr=`0.9672`

#### latent trajectory smoothness

- avg_step=`3.4114`, step/global_median=`0.9214`

### latent_4

#### reconstruction

- `behavior_8d`: mae=`0.2627`, rmse=`0.361`, corr=`0.9326`
- `i7_numeric`: mae=`0.1123`, rmse=`0.2904`, corr=`0.8141`
- `language_features`: mae=`0.4298`, rmse=`0.6413`, corr=`0.7673`

#### relation prediction from shared latent

- mae=`0.0347`, rmse=`0.0464`, corr=`0.9693`

#### latent trajectory smoothness

- avg_step=`3.7092`, step/global_median=`0.918`

### latent_5

#### reconstruction

- `behavior_8d`: mae=`0.233`, rmse=`0.3099`, corr=`0.9508`
- `i7_numeric`: mae=`0.1075`, rmse=`0.2814`, corr=`0.8266`
- `language_features`: mae=`0.3729`, rmse=`0.5642`, corr=`0.8257`

#### relation prediction from shared latent

- mae=`0.0336`, rmse=`0.0452`, corr=`0.971`

#### latent trajectory smoothness

- avg_step=`3.9947`, step/global_median=`0.9154`

### latent_6

#### reconstruction

- `behavior_8d`: mae=`0.2298`, rmse=`0.3057`, corr=`0.9521`
- `i7_numeric`: mae=`0.1017`, rmse=`0.2697`, corr=`0.8421`
- `language_features`: mae=`0.3188`, rmse=`0.4624`, corr=`0.8867`

#### relation prediction from shared latent

- mae=`0.0333`, rmse=`0.0448`, corr=`0.9715`

#### latent trajectory smoothness

- avg_step=`4.1992`, step/global_median=`0.9022`

## Dataset: `explicit_rel_state_projected_oracle_i7`

- ontology variant: `A`
- samples: `180`

### latent_2

#### reconstruction

- `behavior_8d`: mae=`0.2979`, rmse=`0.4204`, corr=`0.9074`
- `i7_numeric`: mae=`0.1816`, rmse=`0.3709`, corr=`0.7957`
- `language_features`: mae=`0.4758`, rmse=`0.7525`, corr=`0.6586`

#### relation prediction from shared latent

- mae=`0.0351`, rmse=`0.0471`, corr=`0.9684`

#### latent trajectory smoothness

- avg_step=`3.07`, step/global_median=`0.9257`

### latent_3

#### reconstruction

- `behavior_8d`: mae=`0.2941`, rmse=`0.4177`, corr=`0.9086`
- `i7_numeric`: mae=`0.1226`, rmse=`0.2599`, corr=`0.9055`
- `language_features`: mae=`0.4511`, rmse=`0.6887`, corr=`0.725`

#### relation prediction from shared latent

- mae=`0.0342`, rmse=`0.0462`, corr=`0.9696`

#### latent trajectory smoothness

- avg_step=`3.4992`, step/global_median=`0.9219`

### latent_4

#### reconstruction

- `behavior_8d`: mae=`0.2874`, rmse=`0.3943`, corr=`0.919`
- `i7_numeric`: mae=`0.1192`, rmse=`0.2526`, corr=`0.911`
- `language_features`: mae=`0.3883`, rmse=`0.5921`, corr=`0.8058`

#### relation prediction from shared latent

- mae=`0.0335`, rmse=`0.0455`, corr=`0.9705`

#### latent trajectory smoothness

- avg_step=`3.8505`, step/global_median=`0.9216`

### latent_5

#### reconstruction

- `behavior_8d`: mae=`0.2828`, rmse=`0.3899`, corr=`0.9208`
- `i7_numeric`: mae=`0.1172`, rmse=`0.2486`, corr=`0.9139`
- `language_features`: mae=`0.3439`, rmse=`0.4954`, corr=`0.8687`

#### relation prediction from shared latent

- mae=`0.0335`, rmse=`0.0454`, corr=`0.9706`

#### latent trajectory smoothness

- avg_step=`4.0676`, step/global_median=`0.9377`

### latent_6

#### reconstruction

- `behavior_8d`: mae=`0.2248`, rmse=`0.2957`, corr=`0.9553`
- `i7_numeric`: mae=`0.1106`, rmse=`0.227`, corr=`0.9288`
- `language_features`: mae=`0.2979`, rmse=`0.4498`, corr=`0.8931`

#### relation prediction from shared latent

- mae=`0.03`, rmse=`0.0403`, corr=`0.977`

#### latent trajectory smoothness

- avg_step=`4.245`, step/global_median=`0.9148`
