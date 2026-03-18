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

### latent_9

- `behavior_8d` reconstruction: mae=`0.2031`, rmse=`0.2741`, corr=`0.9617`
- `i7_numeric` reconstruction: mae=`0.035`, rmse=`0.0982`, corr=`0.9805`
- `language_features` reconstruction: mae=`0.1661`, rmse=`0.2501`, corr=`0.9682`
- family probe: loocv_accuracy=`0.5111`, neighbor_purity_at_k=`0.4578`
- trajectory: avg_step=`4.5193`, step/global_median=`0.8949`, avg_turning=`1.3263`
- relation readout: mae=`0.0278`, rmse=`0.0374`, corr=`0.9802`

### latent_10

- `behavior_8d` reconstruction: mae=`0.1694`, rmse=`0.2236`, corr=`0.9747`
- `i7_numeric` reconstruction: mae=`0.0308`, rmse=`0.0902`, corr=`0.9836`
- `language_features` reconstruction: mae=`0.1347`, rmse=`0.2139`, corr=`0.9769`
- family probe: loocv_accuracy=`0.5056`, neighbor_purity_at_k=`0.4722`
- trajectory: avg_step=`4.59`, step/global_median=`0.8928`, avg_turning=`1.3519`
- relation readout: mae=`0.0248`, rmse=`0.0334`, corr=`0.9842`

### latent_11

- `behavior_8d` reconstruction: mae=`0.1635`, rmse=`0.216`, corr=`0.9764`
- `i7_numeric` reconstruction: mae=`0.03`, rmse=`0.0892`, corr=`0.984`
- `language_features` reconstruction: mae=`0.0625`, rmse=`0.1143`, corr=`0.9934`
- family probe: loocv_accuracy=`0.5111`, neighbor_purity_at_k=`0.4678`
- trajectory: avg_step=`4.6722`, step/global_median=`0.8947`, avg_turning=`1.3533`
- relation readout: mae=`0.0248`, rmse=`0.0334`, corr=`0.9842`

### latent_12

- `behavior_8d` reconstruction: mae=`0.1332`, rmse=`0.178`, corr=`0.984`
- `i7_numeric` reconstruction: mae=`0.0301`, rmse=`0.0888`, corr=`0.9841`
- `language_features` reconstruction: mae=`0.0438`, rmse=`0.0807`, corr=`0.9967`
- family probe: loocv_accuracy=`0.5056`, neighbor_purity_at_k=`0.4711`
- trajectory: avg_step=`4.7137`, step/global_median=`0.8974`, avg_turning=`1.3574`
- relation readout: mae=`0.023`, rmse=`0.0311`, corr=`0.9864`

### latent_13

- `behavior_8d` reconstruction: mae=`0.1082`, rmse=`0.1476`, corr=`0.989`
- `i7_numeric` reconstruction: mae=`0.0236`, rmse=`0.0732`, corr=`0.9892`
- `language_features` reconstruction: mae=`0.0236`, rmse=`0.0452`, corr=`0.999`
- family probe: loocv_accuracy=`0.5111`, neighbor_purity_at_k=`0.4722`
- trajectory: avg_step=`4.7368`, step/global_median=`0.897`, avg_turning=`1.3566`
- relation readout: mae=`0.0228`, rmse=`0.0308`, corr=`0.9866`

### latent_14

- `behavior_8d` reconstruction: mae=`0.0709`, rmse=`0.104`, corr=`0.9946`
- `i7_numeric` reconstruction: mae=`0.0129`, rmse=`0.0396`, corr=`0.9969`
- `language_features` reconstruction: mae=`0.0087`, rmse=`0.0292`, corr=`0.9996`
- family probe: loocv_accuracy=`0.5167`, neighbor_purity_at_k=`0.4733`
- trajectory: avg_step=`4.7746`, step/global_median=`0.8988`, avg_turning=`1.3647`
- relation readout: mae=`0.0218`, rmse=`0.0297`, corr=`0.9876`

### latent_15

- `behavior_8d` reconstruction: mae=`0.0513`, rmse=`0.072`, corr=`0.9974`
- `i7_numeric` reconstruction: mae=`0.008`, rmse=`0.0233`, corr=`0.9989`
- `language_features` reconstruction: mae=`0.0073`, rmse=`0.0286`, corr=`0.9996`
- family probe: loocv_accuracy=`0.5167`, neighbor_purity_at_k=`0.4822`
- trajectory: avg_step=`4.7841`, step/global_median=`0.8982`, avg_turning=`1.3665`
- relation readout: mae=`0.0212`, rmse=`0.0289`, corr=`0.9883`

### latent_16

- `behavior_8d` reconstruction: mae=`0.0221`, rmse=`0.0432`, corr=`0.9991`
- `i7_numeric` reconstruction: mae=`0.0019`, rmse=`0.0052`, corr=`0.9999`
- `language_features` reconstruction: mae=`0.0043`, rmse=`0.0281`, corr=`0.9996`
- family probe: loocv_accuracy=`0.5167`, neighbor_purity_at_k=`0.48`
- trajectory: avg_step=`4.79`, step/global_median=`0.898`, avg_turning=`1.3666`
- relation readout: mae=`0.0204`, rmse=`0.0274`, corr=`0.9894`

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

### latent_9

- `behavior_8d` reconstruction: mae=`0.1927`, rmse=`0.2567`, corr=`0.9665`
- `i7_numeric` reconstruction: mae=`0.0455`, rmse=`0.1137`, corr=`0.9826`
- `language_features` reconstruction: mae=`0.1471`, rmse=`0.2131`, corr=`0.977`
- family probe: loocv_accuracy=`0.4111`, neighbor_purity_at_k=`0.4589`
- trajectory: avg_step=`4.5956`, step/global_median=`0.9164`, avg_turning=`1.3726`
- relation readout: mae=`0.0271`, rmse=`0.0361`, corr=`0.9816`

### latent_10

- `behavior_8d` reconstruction: mae=`0.1651`, rmse=`0.2208`, corr=`0.9753`
- `i7_numeric` reconstruction: mae=`0.0317`, rmse=`0.0829`, corr=`0.9908`
- `language_features` reconstruction: mae=`0.1197`, rmse=`0.1817`, corr=`0.9834`
- family probe: loocv_accuracy=`0.4222`, neighbor_purity_at_k=`0.4611`
- trajectory: avg_step=`4.6625`, step/global_median=`0.9174`, avg_turning=`1.3766`
- relation readout: mae=`0.0257`, rmse=`0.0343`, corr=`0.9834`

### latent_11

- `behavior_8d` reconstruction: mae=`0.148`, rmse=`0.1963`, corr=`0.9805`
- `i7_numeric` reconstruction: mae=`0.0274`, rmse=`0.0775`, corr=`0.992`
- `language_features` reconstruction: mae=`0.0565`, rmse=`0.1162`, corr=`0.9932`
- family probe: loocv_accuracy=`0.4167`, neighbor_purity_at_k=`0.4689`
- trajectory: avg_step=`4.7058`, step/global_median=`0.9161`, avg_turning=`1.3819`
- relation readout: mae=`0.0238`, rmse=`0.0322`, corr=`0.9854`

### latent_12

- `behavior_8d` reconstruction: mae=`0.1035`, rmse=`0.1448`, corr=`0.9895`
- `i7_numeric` reconstruction: mae=`0.0239`, rmse=`0.067`, corr=`0.994`
- `language_features` reconstruction: mae=`0.0454`, rmse=`0.1108`, corr=`0.9938`
- family probe: loocv_accuracy=`0.4167`, neighbor_purity_at_k=`0.4767`
- trajectory: avg_step=`4.7383`, step/global_median=`0.9161`, avg_turning=`1.3819`
- relation readout: mae=`0.0226`, rmse=`0.0305`, corr=`0.9869`

### latent_13

- `behavior_8d` reconstruction: mae=`0.0854`, rmse=`0.1177`, corr=`0.993`
- `i7_numeric` reconstruction: mae=`0.0211`, rmse=`0.0613`, corr=`0.995`
- `language_features` reconstruction: mae=`0.0365`, rmse=`0.0766`, corr=`0.9971`
- family probe: loocv_accuracy=`0.4222`, neighbor_purity_at_k=`0.4833`
- trajectory: avg_step=`4.7647`, step/global_median=`0.9194`, avg_turning=`1.3857`
- relation readout: mae=`0.0221`, rmse=`0.0299`, corr=`0.9874`

### latent_14

- `behavior_8d` reconstruction: mae=`0.0709`, rmse=`0.1034`, corr=`0.9946`
- `i7_numeric` reconstruction: mae=`0.0121`, rmse=`0.034`, corr=`0.9985`
- `language_features` reconstruction: mae=`0.0156`, rmse=`0.0364`, corr=`0.9993`
- family probe: loocv_accuracy=`0.4111`, neighbor_purity_at_k=`0.4822`
- trajectory: avg_step=`4.7881`, step/global_median=`0.9216`, avg_turning=`1.3933`
- relation readout: mae=`0.022`, rmse=`0.0297`, corr=`0.9876`

### latent_15

- `behavior_8d` reconstruction: mae=`0.0527`, rmse=`0.0744`, corr=`0.9972`
- `i7_numeric` reconstruction: mae=`0.0078`, rmse=`0.0212`, corr=`0.9994`
- `language_features` reconstruction: mae=`0.0111`, rmse=`0.0336`, corr=`0.9994`
- family probe: loocv_accuracy=`0.4111`, neighbor_purity_at_k=`0.4856`
- trajectory: avg_step=`4.7946`, step/global_median=`0.921`, avg_turning=`1.3938`
- relation readout: mae=`0.0217`, rmse=`0.0293`, corr=`0.9879`

### latent_16

- `behavior_8d` reconstruction: mae=`0.0238`, rmse=`0.044`, corr=`0.999`
- `i7_numeric` reconstruction: mae=`0.0035`, rmse=`0.0074`, corr=`0.9999`
- `language_features` reconstruction: mae=`0.0094`, rmse=`0.0326`, corr=`0.9995`
- family probe: loocv_accuracy=`0.4111`, neighbor_purity_at_k=`0.4889`
- trajectory: avg_step=`4.8005`, step/global_median=`0.9206`, avg_turning=`1.3941`
- relation readout: mae=`0.0208`, rmse=`0.0278`, corr=`0.9891`
