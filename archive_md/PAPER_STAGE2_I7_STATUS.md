# Stage 2 Status: i7 Interface

## Current strongest result

The strongest Stage-2 finding so far is:

- `explicit_rel_state_projected_oracle_i7`
- `explicit_rel_state_projected_i7`
- `baseline_relational_instruction`

with the current ordering:

- `oracle i7 > real i7 > baseline`

## Evidence supporting this

### 1. Focused manual judge

Files:

- [paper_eval_exec_i7_real_vs_oracle_v1_out/manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_exec_i7_real_vs_oracle_v1_out/manual_judge_results.md)

Focused pairwise judgments support:

- `real i7 > baseline`
- `oracle i7 > baseline`
- `oracle i7 > real i7`

across:

- `oracle_exec_warm_001`
- `oracle_exec_vuln_001`
- `oracle_exec_cool_001`

### 2. Repeated sampling

Files:

- [PAPER_REPEATED_SAMPLING_I7_SUMMARY.md](d:/My%20Project/companion-ai/PAPER_REPEATED_SAMPLING_I7_SUMMARY.md)

Three repeated runs preserved the same coarse ranking:

- repeat 1: `oracle 24.78 < real 59.06 < baseline 92.78`
- repeat 2: `oracle 29.06 < real 52.56 < baseline 95.44`
- repeat 3: `oracle 30.50 < real 60.39 < baseline 97.39`

This supports a stable Stage-2 ordering:

- `oracle i7 > real i7 > baseline`

## Gap diagnosis: real i7 -> oracle i7

Files:

- [paper_gap_diagnose_i7.py](d:/My%20Project/companion-ai/paper_gap_diagnose_i7.py)
- [paper_eval_exec_i7_real_vs_oracle_v1_out/gap_diagnosis_i7.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_real_vs_oracle_v1_out/gap_diagnosis_i7.json)

Current diagnosis result:

- `exact_interface_match_rate = 0.1667`
- `avg_dim_mismatches_per_turn = 3.78`

Most common mismatch dimensions:

- `clarify_followup`
- `affective_followup`
- `initiative_level`
- `reply_scope`

## Current interpretation

The `real i7 -> oracle i7` gap does not look like a pure final-language realization problem.

Instead, a substantial share of the gap already appears before final generation:

- real and oracle `i7` execution interfaces frequently disagree

So the current decomposition is:

1. **pre-realization control mismatch**
2. **post-interface realization gap**

What we still cannot fully separate yet is:

- updater error
- projection mapping error

To separate those two, the next experiment should add:

- structured `oracle_rel_effective`
- a hybrid mode that uses oracle relation state with the real projection function

## What this means for the paper

At this point, the paper no longer needs to argue only that:

- explicit state exists

It can now argue something more specific:

1. a two-layer executable interface can outperform a strong relational baseline
2. the real chain preserves part of this gain
3. the remaining gap is not just a language-model end-stage issue
4. a meaningful part of the loss happens before final realization
