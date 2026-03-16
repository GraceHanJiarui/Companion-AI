# Manual Judge Results: Hybrid Gap Diagnosis for i7

Source files:

- `paper_eval_exec_i7_hybrid_gap_v1_out/case_level_judge_inputs.json`
- `paper_eval_exec_i7_hybrid_gap_v1_out/judge_examples.json`

Judging focus:

- compare three main variants:
  - `explicit_rel_state_projected_i7`
  - `explicit_rel_state_projected_oracle_behavior_i7`
  - `explicit_rel_state_projected_oracle_i7`
- determine whether the remaining gap is more likely caused by:
  - relation-side mismatch
  - behavior-side mismatch
  - or final realization noise

## Pairwise-style manual judgments

### Case: `oracle_exec_warm_001`

- `oracle_behavior_i7` vs `real i7`
  - winner: `left`
  - reason: `oracle_behavior_i7` is more restrained and stays closer to the intended light warming trajectory. `real i7` remains coherent, but it keeps more optionality, more follow-up pressure, and a more expanded continuation style.

- `oracle_i7` vs `oracle_behavior_i7`
  - winner: `tie`
  - reason: these two are very close on overall coherence. `oracle_behavior_i7` is slightly shorter and cleaner in some places, while `oracle_i7` feels marginally more naturally warmed. The gap here is small.

- `oracle_rel_i7` vs `real i7`
  - winner: `tie`
  - reason: relation-only oracle replacement helps a little, but not enough to create a large separation. Both still carry noticeably more expansion than the oracle-behavior variants.

### Case: `oracle_exec_vuln_001`

- `oracle_behavior_i7` vs `real i7`
  - winner: `left`
  - reason: the behavior-oracle variant is much closer to low-pressure presence. `real i7` still drifts toward heavier support moves and over-structured continuation, especially when the user just wants simple presence.

- `oracle_i7` vs `oracle_behavior_i7`
  - winner: `tie`
  - reason: both are strong and low-pressure. `oracle_i7` is slightly more exact, but the difference is much smaller than the gap between `real i7` and `oracle_behavior_i7`.

- `oracle_rel_i7` vs `real i7`
  - winner: `left`
  - reason: relation-only oracle replacement improves things somewhat, but the improvement is still modest. The major drop in over-structuring only appears once oracle behavior constraints are used.

### Case: `oracle_exec_cool_001`

- `oracle_behavior_i7` vs `real i7`
  - winner: `left`
  - reason: this is the clearest case. `oracle_behavior_i7` preserves distance and low-pressure tone much better, while `real i7` still sounds too managed and too willing to keep the interaction open.

- `oracle_i7` vs `oracle_behavior_i7`
  - winner: `tie`
  - reason: the two are very close in cooling coherence. The full oracle remains slightly more exact, but the behavior-oracle version already captures most of the gain.

- `oracle_rel_i7` vs `real i7`
  - winner: `left`
  - reason: relation-only oracle replacement helps, but still leaves too much continuation softness. It does not close the gap nearly as much as oracle behavior replacement does.

## Interim interpretation

Across warm, vulnerability, and cooling:

- `oracle_behavior_i7` is consistently better than `real i7`
- `oracle_behavior_i7` is approximately tied with `oracle_i7`
- `oracle_rel_i7` is only modestly better than `real i7`, and sometimes only tied

## Current conclusion

The remaining `real i7 -> oracle i7` gap is more likely dominated by:

- behavior / execution-interface mismatch

rather than by:

- relation-summary mismatch

Final realization noise still exists, but it currently looks like a smaller residual gap rather than the primary bottleneck.
