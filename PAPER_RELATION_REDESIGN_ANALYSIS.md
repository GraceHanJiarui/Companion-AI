# Relation Redesign Reverse Analysis

## Summary

- `num_rows`: `18`
- `num_pairs`: `153`
- `close_rel_large_beh_pair_count`: `15`

## Behavior Dims That Most Often Diverge Despite Similar Relation

- `E`: `9`
- `Q_clarify`: `12`
- `Directness`: `6`
- `T_w`: `12`
- `Q_aff`: `15`
- `Initiative`: `12`
- `Disclosure_Content`: `1`
- `Disclosure_Style`: `1`

## Average Neighbor Behavior Variance

- `E`: `0.0012`
- `Q_clarify`: `0.0008`
- `Directness`: `0.0015`
- `T_w`: `0.0017`
- `Q_aff`: `0.0013`
- `Initiative`: `0.0007`
- `Disclosure_Content`: `0.0001`
- `Disclosure_Style`: `0.0001`

## Most Diagnostic Similar-Relation / Different-Behavior Pairs

- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_warm_001:E_ordinary_continuation` | rel_dist=`0.03` beh_dist=`0.08`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_vuln_001:D_counter_signal_or_refinement` | rel_dist=`0.0325` beh_dist=`0.0825`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_warm_001:F_final_probe` | rel_dist=`0.035` beh_dist=`0.095`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_vuln_001:C_stabilization` | rel_dist=`0.0375` beh_dist=`0.095`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_vuln_001:E_ordinary_continuation` | rel_dist=`0.0425` beh_dist=`0.1125`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_vuln_001:F_final_probe` | rel_dist=`0.045` beh_dist=`0.1125`
- `oracle_exec_warm_001:D_counter_signal_or_refinement` vs `oracle_exec_vuln_001:E_ordinary_continuation` | rel_dist=`0.05` beh_dist=`0.0875`
- `oracle_exec_warm_001:D_counter_signal_or_refinement` vs `oracle_exec_vuln_001:F_final_probe` | rel_dist=`0.0525` beh_dist=`0.0975`
- `oracle_exec_warm_001:A_initial_contact` vs `oracle_exec_cool_001:A_initial_contact` | rel_dist=`0.0575` beh_dist=`0.0875`
- `oracle_exec_warm_001:B_first_relational_signal` vs `oracle_exec_vuln_001:B_first_relational_signal` | rel_dist=`0.0575` beh_dist=`0.0875`

## Interpretation Draft

- If close relation states still require meaningfully different behavior targets, current relation dimensions are unlikely to be sufficient as a unique deterministic explanation of behavior.
- The most recurrent divergent behavior dimensions should be the first candidates for relation-space redesign.
- This analysis is not a proof that pure relation is impossible; it is evidence about where the current relation space appears under-specified.
