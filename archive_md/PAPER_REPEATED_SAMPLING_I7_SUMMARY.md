# Repeated Sampling Summary: baseline vs real i7 vs oracle i7

## Goal

Validate whether the Stage-2 ranking

- `explicit_rel_state_projected_oracle_i7`
- `explicit_rel_state_projected_i7`
- `baseline_relational_instruction`

is stable across repeated runs on the same oracle execution cases.

## Input cases

- `paper_cases_oracle_exec_v1.json`

Cases included:

- `oracle_exec_warm_001`
- `oracle_exec_vuln_001`
- `oracle_exec_cool_001`

## Command template

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_real_vs_oracle_repeat_N.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_real_vs_oracle_repeat_N.jsonl --out-dir paper_eval_exec_i7_real_vs_oracle_repeat_N_out
```

## Repeats

Three independent repeats were run:

- `paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl`
- `paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl`
- `paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl`

with corresponding eval directories:

- `paper_eval_exec_i7_real_vs_oracle_repeat_1_out`
- `paper_eval_exec_i7_real_vs_oracle_repeat_2_out`
- `paper_eval_exec_i7_real_vs_oracle_repeat_3_out`

## Global summaries

### Repeat 1

- baseline: `92.78`
- real i7: `59.06`
- oracle i7: `24.78`

### Repeat 2

- baseline: `95.44`
- real i7: `52.56`
- oracle i7: `29.06`

### Repeat 3

- baseline: `97.39`
- real i7: `60.39`
- oracle i7: `30.50`

All three repeats preserve:

- `oracle i7 < real i7 < baseline`

when using average response length as a coarse proxy for over-expansion and compensatory relational drift.

## Case-level summaries

### Repeat 1

- warm: `oracle 34.33 < real 64.17 < baseline 90.67`
- vuln: `oracle 22.17 < real 69.83 < baseline 88.83`
- cool: `oracle 17.83 < real 43.17 < baseline 98.83`

### Repeat 2

- warm: `oracle 46.17 < real 53.67 < baseline 117.33`
- vuln: `oracle 24.67 < real 54.83 < baseline 94.83`
- cool: `oracle 16.33 < real 49.17 < baseline 74.17`

### Repeat 3

- warm: `oracle 45.17 < real 65.67 < baseline 96.00`
- vuln: `oracle 30.50 < real 64.83 < baseline 90.50`
- cool: `oracle 15.83 < real 50.67 < baseline 105.67`

Again, all three repeats preserve the same ordering on all three cases:

- `oracle i7 < real i7 < baseline`

## Interpretation

This repeated sampling supports a stable Stage-2 pattern:

1. `explicit_rel_state_projected_oracle_i7` remains the tightest and most controlled realization.
2. `explicit_rel_state_projected_i7` consistently retains part of the oracle advantage.
3. `baseline_relational_instruction` remains the most likely to over-expand, especially in later continuation phases.

## What this does and does not prove

This repeated sampling strengthens the claim that the ranking

- `oracle i7 > real i7 > baseline`

is stable as a coarse behavioral pattern.

It does **not** by itself replace case-level human or LLM judge preference scoring. A follow-up judge pass would still be needed if the paper needs a fully qualitative preference claim rather than a stability claim based on repeated runs and summary statistics.
