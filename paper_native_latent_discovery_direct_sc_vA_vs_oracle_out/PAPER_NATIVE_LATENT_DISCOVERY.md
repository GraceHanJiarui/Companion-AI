# Native Latent Discovery

## Goal

- Learn latent interaction structure directly from `behavior_8d + i7_numeric + language_features`.
- Use dimensionality sweeps to ask how many latent dimensions are actually needed before reconstruction, family structure, and trajectory structure saturate.
- Treat `relation_raw4` only as an optional readout target afterwards, not as a latent-construction input.

## Dataset: `explicit_rel_state_rel_to_interface_i7_sc_vA`

- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### latent_2

- `behavior_8d` reconstruction: mae=`0.2946`, rmse=`0.4178`, corr=`0.9086`
- `i7_numeric` reconstruction: mae=`0.1293`, rmse=`0.3591`, corr=`0.6958`
- `language_features` reconstruction: mae=`0.5147`, rmse=`0.8043`, corr=`0.5942`
- family probe: loocv_accuracy=`0.4111`, neighbor_purity_at_k=`0.4433`
- trajectory: avg_step=`2.9515`, step/global_median=`0.9042`, avg_turning=`1.3273`
- relation readout: mae=`0.0363`, rmse=`0.0484`, corr=`0.9667`

### latent_3

- `behavior_8d` reconstruction: mae=`0.279`, rmse=`0.3851`, corr=`0.9229`
- `i7_numeric` reconstruction: mae=`0.1218`, rmse=`0.3309`, corr=`0.7497`
- `language_features` reconstruction: mae=`0.4972`, rmse=`0.7255`, corr=`0.6882`
- family probe: loocv_accuracy=`0.3944`, neighbor_purity_at_k=`0.4233`
- trajectory: avg_step=`3.4114`, step/global_median=`0.9214`, avg_turning=`1.3275`
- relation readout: mae=`0.0357`, rmse=`0.048`, corr=`0.9672`

### latent_4

- `behavior_8d` reconstruction: mae=`0.2627`, rmse=`0.361`, corr=`0.9326`
- `i7_numeric` reconstruction: mae=`0.1123`, rmse=`0.2904`, corr=`0.8141`
- `language_features` reconstruction: mae=`0.4298`, rmse=`0.6413`, corr=`0.7673`
- family probe: loocv_accuracy=`0.4778`, neighbor_purity_at_k=`0.4667`
- trajectory: avg_step=`3.7092`, step/global_median=`0.918`, avg_turning=`1.3375`
- relation readout: mae=`0.0347`, rmse=`0.0464`, corr=`0.9693`

### latent_5

- `behavior_8d` reconstruction: mae=`0.233`, rmse=`0.3099`, corr=`0.9508`
- `i7_numeric` reconstruction: mae=`0.1075`, rmse=`0.2814`, corr=`0.8266`
- `language_features` reconstruction: mae=`0.3729`, rmse=`0.5642`, corr=`0.8257`
- family probe: loocv_accuracy=`0.4667`, neighbor_purity_at_k=`0.4556`
- trajectory: avg_step=`3.9947`, step/global_median=`0.9154`, avg_turning=`1.3202`
- relation readout: mae=`0.0336`, rmse=`0.0452`, corr=`0.971`

### latent_6

- `behavior_8d` reconstruction: mae=`0.2298`, rmse=`0.3057`, corr=`0.9521`
- `i7_numeric` reconstruction: mae=`0.1017`, rmse=`0.2697`, corr=`0.8421`
- `language_features` reconstruction: mae=`0.3188`, rmse=`0.4624`, corr=`0.8867`
- family probe: loocv_accuracy=`0.4778`, neighbor_purity_at_k=`0.4489`
- trajectory: avg_step=`4.1992`, step/global_median=`0.9022`, avg_turning=`1.3306`
- relation readout: mae=`0.0333`, rmse=`0.0448`, corr=`0.9715`

### latent_7

- `behavior_8d` reconstruction: mae=`0.2147`, rmse=`0.2907`, corr=`0.9568`
- `i7_numeric` reconstruction: mae=`0.0753`, rmse=`0.1993`, corr=`0.9171`
- `language_features` reconstruction: mae=`0.2661`, rmse=`0.3946`, corr=`0.9188`
- family probe: loocv_accuracy=`0.4778`, neighbor_purity_at_k=`0.4522`
- trajectory: avg_step=`4.3197`, step/global_median=`0.8938`, avg_turning=`1.3265`
- relation readout: mae=`0.03`, rmse=`0.0408`, corr=`0.9764`

### latent_8

- `behavior_8d` reconstruction: mae=`0.2101`, rmse=`0.2838`, corr=`0.9589`
- `i7_numeric` reconstruction: mae=`0.0555`, rmse=`0.1382`, corr=`0.961`
- `language_features` reconstruction: mae=`0.2285`, rmse=`0.3277`, corr=`0.9448`
- family probe: loocv_accuracy=`0.4944`, neighbor_purity_at_k=`0.4467`
- trajectory: avg_step=`4.4365`, step/global_median=`0.895`, avg_turning=`1.3251`
- relation readout: mae=`0.0294`, rmse=`0.0399`, corr=`0.9774`

## Dataset: `explicit_rel_state_projected_oracle_i7`

- samples: `180`
- families: `boundary_repair, cooling, mixed_signal, other, vulnerability, warm`

### latent_2

- `behavior_8d` reconstruction: mae=`0.2979`, rmse=`0.4204`, corr=`0.9074`
- `i7_numeric` reconstruction: mae=`0.1816`, rmse=`0.3709`, corr=`0.7957`
- `language_features` reconstruction: mae=`0.4758`, rmse=`0.7525`, corr=`0.6586`
- family probe: loocv_accuracy=`0.3889`, neighbor_purity_at_k=`0.4922`
- trajectory: avg_step=`3.07`, step/global_median=`0.9257`, avg_turning=`1.343`
- relation readout: mae=`0.0351`, rmse=`0.0471`, corr=`0.9684`

### latent_3

- `behavior_8d` reconstruction: mae=`0.2941`, rmse=`0.4177`, corr=`0.9086`
- `i7_numeric` reconstruction: mae=`0.1226`, rmse=`0.2599`, corr=`0.9055`
- `language_features` reconstruction: mae=`0.4511`, rmse=`0.6887`, corr=`0.725`
- family probe: loocv_accuracy=`0.3889`, neighbor_purity_at_k=`0.4733`
- trajectory: avg_step=`3.4992`, step/global_median=`0.9219`, avg_turning=`1.4083`
- relation readout: mae=`0.0342`, rmse=`0.0462`, corr=`0.9696`

### latent_4

- `behavior_8d` reconstruction: mae=`0.2874`, rmse=`0.3943`, corr=`0.919`
- `i7_numeric` reconstruction: mae=`0.1192`, rmse=`0.2526`, corr=`0.911`
- `language_features` reconstruction: mae=`0.3883`, rmse=`0.5921`, corr=`0.8058`
- family probe: loocv_accuracy=`0.3778`, neighbor_purity_at_k=`0.4422`
- trajectory: avg_step=`3.8505`, step/global_median=`0.9216`, avg_turning=`1.3603`
- relation readout: mae=`0.0335`, rmse=`0.0455`, corr=`0.9705`

### latent_5

- `behavior_8d` reconstruction: mae=`0.2828`, rmse=`0.3899`, corr=`0.9208`
- `i7_numeric` reconstruction: mae=`0.1172`, rmse=`0.2486`, corr=`0.9139`
- `language_features` reconstruction: mae=`0.3439`, rmse=`0.4954`, corr=`0.8687`
- family probe: loocv_accuracy=`0.3778`, neighbor_purity_at_k=`0.4289`
- trajectory: avg_step=`4.0676`, step/global_median=`0.9377`, avg_turning=`1.3749`
- relation readout: mae=`0.0335`, rmse=`0.0454`, corr=`0.9706`

### latent_6

- `behavior_8d` reconstruction: mae=`0.2248`, rmse=`0.2957`, corr=`0.9553`
- `i7_numeric` reconstruction: mae=`0.1106`, rmse=`0.227`, corr=`0.9288`
- `language_features` reconstruction: mae=`0.2979`, rmse=`0.4498`, corr=`0.8931`
- family probe: loocv_accuracy=`0.4167`, neighbor_purity_at_k=`0.4811`
- trajectory: avg_step=`4.245`, step/global_median=`0.9148`, avg_turning=`1.3621`
- relation readout: mae=`0.03`, rmse=`0.0403`, corr=`0.977`

### latent_7

- `behavior_8d` reconstruction: mae=`0.2007`, rmse=`0.2711`, corr=`0.9626`
- `i7_numeric` reconstruction: mae=`0.05`, rmse=`0.1179`, corr=`0.9813`
- `language_features` reconstruction: mae=`0.255`, rmse=`0.3903`, corr=`0.9207`
- family probe: loocv_accuracy=`0.4278`, neighbor_purity_at_k=`0.4733`
- trajectory: avg_step=`4.3921`, step/global_median=`0.9075`, avg_turning=`1.3635`
- relation readout: mae=`0.0275`, rmse=`0.0373`, corr=`0.9803`

### latent_8

- `behavior_8d` reconstruction: mae=`0.1943`, rmse=`0.2588`, corr=`0.9659`
- `i7_numeric` reconstruction: mae=`0.0461`, rmse=`0.1144`, corr=`0.9824`
- `language_features` reconstruction: mae=`0.1754`, rmse=`0.2929`, corr=`0.9561`
- family probe: loocv_accuracy=`0.4167`, neighbor_purity_at_k=`0.4544`
- trajectory: avg_step=`4.5237`, step/global_median=`0.9122`, avg_turning=`1.367`
- relation readout: mae=`0.0271`, rmse=`0.0362`, corr=`0.9815`
