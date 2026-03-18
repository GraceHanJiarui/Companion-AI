# Paper Experiment Registry

## Purpose

This file is the working experiment index for the relation-state paper line.
It is meant to support two use cases:

1. Reproducing prior experiments end to end
2. Referencing concrete files, commands, and conclusions when drafting the paper

It is not the main proposal document. It is the experiment logbook / registry.

## Archived-note sources already absorbed here

The following older working notes have now been functionally absorbed by the registry and/or the main paper documents:

- `PAPER_PROMPT_BRIDGING_EXPERIMENT.md`
- `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`
- `PAPER_STAGE2_I7_STATUS.md`

They may still be kept for archival traceability, but they should no longer be treated as separate sources of truth.

## Core Scripts

- Run experiments: [paper_run_experiment.py](d:/My%20Project/companion-ai/paper_run_experiment.py)
- Aggregate and export eval inputs: [paper_eval.py](d:/My%20Project/companion-ai/paper_eval.py)
- Render judge prompts: [paper_build_judge_prompts.py](d:/My%20Project/companion-ai/paper_build_judge_prompts.py)

## Core Case Files

- Initial full paper cases: [paper_cases_v1.json](d:/My%20Project/companion-ai/paper_cases_v1.json)
- Short smoke cases: [paper_cases_smoke.json](d:/My%20Project/companion-ai/paper_cases_smoke.json)
- Long-range cases: [paper_cases_long_v1.json](d:/My%20Project/companion-ai/paper_cases_long_v1.json)
- Oracle long cases: [paper_cases_oracle_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_v1.json)
- Oracle cooling add-on: [paper_cases_oracle_cooling_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_cooling_v1.json)
- Oracle execution-interface cases: [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)
- Generalization trajectory spec: [PAPER_GENERALIZATION_CASE_SPEC.md](d:/My%20Project/companion-ai/PAPER_GENERALIZATION_CASE_SPEC.md)
- Semi-natural v3 plan: [PAPER_SEMI_NATURAL_V3_PLAN.md](d:/My%20Project/companion-ai/PAPER_SEMI_NATURAL_V3_PLAN.md)
- Semi-natural v3 seed set: [paper_cases_semi_natural_v3_seed6.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v3_seed6.json)
- Revised eval-bucket taxonomy: [PAPER_REVISED_EVAL_BUCKET_TAXONOMY.md](d:/My%20Project/companion-ai/PAPER_REVISED_EVAL_BUCKET_TAXONOMY.md)
- Revised bucket seed set: [paper_cases_revised_bucket_seed10.json](d:/My%20Project/companion-ai/paper_cases_revised_bucket_seed10.json)

## Mode Naming Notes

- Old `method` was later replaced by:
  - `explicit_rel_state_direct`
  - `explicit_rel_state_projected`
- Oracle modes mean:
  - same generation model
  - same prompt-family realization
  - but relational / behavior control signals are hand-authored in the case file

## Shared Eval Outputs

Most eval directories contain:

- `global_summary.json`
- `case_mode_summary.json`
- `phase_level_summary.json` for long/phase-aware runs
- `case_level_judge_inputs.json`
- `pairwise_judge_inputs.json`
- sometimes `manual_judge_results.md`

## Experiment Timeline

### Dataset Positioning Note

The current case program should be read in two layers:

- **controlled mechanism set**
  - primarily [paper_cases_oracle_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v3.json)
  - and [paper_cases_long_v1.json](d:/My%20Project/companion-ai/paper_cases_long_v1.json)
- **future generalization set**
  - not yet paper-ready
  - should be rebuilt from [PAPER_GENERALIZATION_CASE_SPEC.md](d:/My%20Project/companion-ai/PAPER_GENERALIZATION_CASE_SPEC.md)

Important current boundary:

- [paper_cases_semi_natural_v1.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v1.json)
- [paper_cases_semi_natural_v2.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v2.json)

should currently be treated as exploratory drafts only, not as finalized paper-facing
generalization evidence. Their main problem is not literal duplication but continued
dependence on the same six-phase functional skeleton used by the controlled mechanism set.

### E0. Full Pipeline Shakeout

Purpose:
- Verify the original experiment pipeline runs end to end
- Compare early `method` against prompt baselines

Input:
- [paper_cases_v1.json](d:/My%20Project/companion-ai/paper_cases_v1.json)

Run:

```bash
python paper_run_experiment.py --cases-json paper_cases_v1.json --output paper_results_v1.jsonl
python paper_eval.py --input paper_results_v1.jsonl --out-dir paper_eval_out
```

Primary outputs:
- [paper_results_v1.jsonl](d:/My%20Project/companion-ai/paper_results_v1.jsonl)
- [paper_eval_out](d:/My%20Project/companion-ai/paper_eval_out)

Main conclusion:
- Pipeline worked, but these results were mainly infrastructure-level
- Boundary-style metrics were not useful as the main research evaluation
- `method` differed from baselines, but this did not yet validate the paper question

### E1. Short Smoke Comparison

Purpose:
- Cheap sanity check on shortened case set
- Verify new baseline family and simplified experimental structure

Input:
- [paper_cases_smoke.json](d:/My%20Project/companion-ai/paper_cases_smoke.json)

Representative outputs:
- [paper_results_smoke.jsonl](d:/My%20Project/companion-ai/paper_results_smoke.jsonl)
- [paper_results_smoke_v2.jsonl](d:/My%20Project/companion-ai/paper_results_smoke_v2.jsonl)
- [paper_eval_smoke_out](d:/My%20Project/companion-ai/paper_eval_smoke_out)
- [paper_eval_smoke_v2_out](d:/My%20Project/companion-ai/paper_eval_smoke_v2_out)

Main conclusion:
- Short smoke cases were useful for pipeline smoke only
- They were too short to support a serious claim about relational coherence
- This directly motivated the long-range case design

### E2. Long-Range Single-Case Probe

Purpose:
- Test whether long cases reveal relational coherence differences better than 3-turn smoke

Input:
- [paper_cases_long_v1.json](d:/My%20Project/companion-ai/paper_cases_long_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_long_v1.json --max-cases 1 --output paper_results_long_smoke_1case.jsonl
python paper_eval.py --input paper_results_long_smoke_1case.jsonl --out-dir paper_eval_long_smoke_1case_out
```

Primary outputs:
- [paper_results_long_smoke_1case.jsonl](d:/My%20Project/companion-ai/paper_results_long_smoke_1case.jsonl)
- [paper_eval_long_smoke_1case_out](d:/My%20Project/companion-ai/paper_eval_long_smoke_1case_out)

Main conclusion:
- Long cases are much more informative than short smoke
- Internal relational state can evolve slowly and plausibly
- But language-layer superiority over strong baselines did not automatically appear
- This pushed the project toward `realization gap` framing

### E3. Prompt-Bridging Diagnosis

Purpose:
- Test whether weak language performance was mostly caused by how explicit state was phrased in the prompt
- Compare:
  - `vA`: original state presentation
  - `vB`: state + natural-language bridge
  - `vC`: natural-language summary only

Input:
- long cases, 2-case diagnostic subset

Primary outputs:
- [paper_results_prompt_bridge_2cases.jsonl](d:/My%20Project/companion-ai/paper_results_prompt_bridge_2cases.jsonl)
- [paper_eval_prompt_bridge_2cases_out](d:/My%20Project/companion-ai/paper_eval_prompt_bridge_2cases_out)
- [PAPER_PROMPT_BRIDGING_EXPERIMENT.md](d:/My%20Project/companion-ai/PAPER_PROMPT_BRIDGING_EXPERIMENT.md)

Main conclusion:
- Prompt presentation is not neutral
- Better bridging reduces over-heavy expression
- But prompt bridge alone did not create clear stable superiority over strong baselines
- Working interpretation:
  - prompt realization matters
  - but it is not the primary bottleneck

### E4. Oracle State Experiment

Purpose:
- Remove the real updater as the main suspect
- Ask: if relational / behavior summaries are already ideal, does the language layer improve?

Input:
- [paper_cases_oracle_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_oracle_v1.jsonl --modes explicit_rel_state_direct_oracle explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_oracle_v1.jsonl --out-dir paper_eval_oracle_v1_out
```

Primary outputs:
- [paper_results_oracle_v1.jsonl](d:/My%20Project/companion-ai/paper_results_oracle_v1.jsonl)
- [paper_eval_oracle_v1_out](d:/My%20Project/companion-ai/paper_eval_oracle_v1_out)

Main conclusion:
- `projected_oracle > direct_oracle`
- Upstream state updating is not the main explanation
- Two-layer control has real potential even when both variants are still prompt-realized
- This made `single-layer vs two-layer` a meaningful research axis

### E5. Scheme B: Strong Baseline vs Real / Oracle Projected

Purpose:
- Compare:
  - `baseline_relational_instruction`
  - `explicit_rel_state_projected`
  - `explicit_rel_state_projected_oracle`

Question:
- How far is ideal two-layer control from strong baseline?
- How much potential is lost in the real chain?

Input:
- [paper_cases_oracle_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_scheme_b_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_scheme_b_v1.jsonl --out-dir paper_eval_scheme_b_v1_out
```

Primary outputs:
- [paper_results_scheme_b_v1.jsonl](d:/My%20Project/companion-ai/paper_results_scheme_b_v1.jsonl)
- [paper_eval_scheme_b_v1_out](d:/My%20Project/companion-ai/paper_eval_scheme_b_v1_out)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_scheme_b_v1_out/manual_judge_results.md)

Main conclusion:
- `projected_oracle > projected`
- `projected_oracle` did not stably dominate strong baseline
- Strong baseline remained highly competitive
- This is one of the main pieces of evidence for the current Stage 1 framing:
  - two-layer structure has potential
  - but strong baseline already captures much of the visible language-layer benefit

### E6. Cooling Replication of Scheme B

Purpose:
- Check whether the same `projected_oracle > projected` pattern repeats in a cooling trajectory

Input:
- [paper_cases_oracle_cooling_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_cooling_v1.json)

Primary outputs:
- [paper_results_scheme_b_cooling_v1.jsonl](d:/My%20Project/companion-ai/paper_results_scheme_b_cooling_v1.jsonl)
- [paper_eval_scheme_b_cooling_v1_out](d:/My%20Project/companion-ai/paper_eval_scheme_b_cooling_v1_out)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_scheme_b_cooling_v1_out/manual_judge_results.md)

Main conclusion:
- `projected_oracle > projected` repeated again
- `projected_oracle` vs strong baseline was again approximately `tie`
- This strengthened the interpretation that:
  - two-layer potential is real
  - strong baseline remains difficult to beat cleanly

### E7. Control-Alignment Experiment

Purpose:
- Test whether `projected_oracle` is just “another good prompt”
- Compare:
  - `explicit_rel_state_projected_oracle`
  - `baseline_relational_instruction_oracle_collapsed`
- Both use the same oracle content, but:
  - one keeps relation/behavior split
  - the other collapses it into a single-layer instruction

Input:
- [paper_cases_oracle_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_control_alignment_v1.jsonl --modes baseline_relational_instruction_oracle_collapsed explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_control_alignment_v1.jsonl --out-dir paper_eval_control_alignment_v1_out
```

Primary outputs:
- [paper_results_control_alignment_v1.jsonl](d:/My%20Project/companion-ai/paper_results_control_alignment_v1.jsonl)
- [paper_eval_control_alignment_v1_out](d:/My%20Project/companion-ai/paper_eval_control_alignment_v1_out)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_control_alignment_v1_out/manual_judge_results.md)

Main conclusion:
- `projected_oracle > oracle-collapsed-single-layer`
- Therefore `projected_oracle` cannot be reduced to “just a better single-layer prompt”
- Stronger interpretation:
  - prompt-based realization is shared
  - but the control interface structure still matters

### E8. Oracle Execution-Interface Family Screening, Round 1

Purpose:
- Start Stage 2 interface-design study
- Test whether interface count / semantic split affects behavior realization
- Compare oracle projected family:
  - `i4`
  - `i6`
  - `i7`
  - `i8`

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_oracle_family_v1.jsonl --modes explicit_rel_state_projected_oracle_i4 explicit_rel_state_projected_oracle_i6 explicit_rel_state_projected_oracle_i7 explicit_rel_state_projected_oracle_i8
python paper_eval.py --input paper_results_exec_oracle_family_v1.jsonl --out-dir paper_eval_exec_oracle_family_v1_out
```

Primary outputs:
- [paper_results_exec_oracle_family_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_oracle_family_v1.jsonl)
- [paper_eval_exec_oracle_family_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v1_out)

Main conclusion:
- `i4` looked too coarse
- `i6` looked over-merged
- `i7/i8` looked more promising
- However, the run was still badly polluted by `E_ordinary_continuation` and `F_final_probe`
- This motivated two concrete implementation changes:
  - B: force strict prompt separation between relationship stance and expression constraints
  - C: add phase-sensitive hard constraints, especially on `E` and `F`

### E9. Oracle Execution-Interface Family Screening, Round 2

Purpose:
- Re-run the interface family after implementing:
  - Change B: strict separation of relationship stance vs expression constraints
  - Change C: hard constraints on continuation / final-probe phases

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_oracle_family_v2.jsonl --modes explicit_rel_state_projected_oracle_i4 explicit_rel_state_projected_oracle_i6 explicit_rel_state_projected_oracle_i7 explicit_rel_state_projected_oracle_i8
python paper_eval.py --input paper_results_exec_oracle_family_v2.jsonl --out-dir paper_eval_exec_oracle_family_v2_out
```

Primary outputs:
- [paper_results_exec_oracle_family_v2.jsonl](d:/My%20Project/companion-ai/paper_results_exec_oracle_family_v2.jsonl)
- [paper_eval_exec_oracle_family_v2_out](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v2_out)

Main conclusion:
- B/C were effective
- `E/F` inflation was substantially reduced
- Interface-family ranking changed:
  - `i8` no longer looked like the obvious strongest option
  - `i6` and `i7` became the best candidates
- Current working interpretation:
  - prompt / layout / phase hard constraints are part of the interface, not separate from it
  - `i6` is the strongest coarse executable candidate
  - `i7` is the strongest semantically faithful candidate

## Manual Judge Files Produced So Far

- Scheme B warm/vulnerability: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_scheme_b_v1_out/manual_judge_results.md)
- Scheme B cooling: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_scheme_b_cooling_v1_out/manual_judge_results.md)
- Control alignment: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_control_alignment_v1_out/manual_judge_results.md)

### E10. Oracle Interface Candidates vs Strong Baseline

Purpose:
- Narrow Stage 2 candidate interfaces to the most promising oracle-executable family members
- Compare:
  - `baseline_relational_instruction`
  - `explicit_rel_state_projected_oracle_i6`
  - `explicit_rel_state_projected_oracle_i7`

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_oracle_family_v3.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_oracle_i6 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_oracle_family_v3.jsonl --out-dir paper_eval_exec_oracle_family_v3_out
```

Primary outputs:
- [paper_results_exec_oracle_family_v3.jsonl](d:/My%20Project/companion-ai/paper_results_exec_oracle_family_v3.jsonl)
- [paper_eval_exec_oracle_family_v3_out](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v3_out)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v3_out/manual_judge_results.md)

Main conclusion:
- `i6 > baseline`
- `i7 > baseline`
- `i7 >= i6`
- `i7` became the preferred Stage-2 interface candidate

### E11. Real i7 vs Oracle i7 vs Strong Baseline

Purpose:
- Test whether the preferred Stage-2 interface candidate (`i7`) survives contact with the real chain
- Compare:
  - `baseline_relational_instruction`
  - `explicit_rel_state_projected_i7`
  - `explicit_rel_state_projected_oracle_i7`

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_real_vs_oracle_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_real_vs_oracle_v1.jsonl --out-dir paper_eval_exec_i7_real_vs_oracle_v1_out
```

Primary outputs:
- [paper_results_exec_i7_real_vs_oracle_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_real_vs_oracle_v1.jsonl)
- [paper_eval_exec_i7_real_vs_oracle_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_i7_real_vs_oracle_v1_out)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_exec_i7_real_vs_oracle_v1_out/manual_judge_results.md)

Main conclusion:
- `oracle i7 > real i7 > strong baseline`
- `real i7` preserves a substantial part of the oracle advantage
- a meaningful realization gap still remains between the real chain and oracle execution

### E12. Repeated Sampling Stability Check for i7

Purpose:
- Validate whether the Stage-2 ranking
  - `oracle i7 > real i7 > baseline`
  is stable across repeated runs

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative runs:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl --out-dir paper_eval_exec_i7_real_vs_oracle_repeat_1_out

python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl --out-dir paper_eval_exec_i7_real_vs_oracle_repeat_2_out

python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl --modes baseline_relational_instruction explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl --out-dir paper_eval_exec_i7_real_vs_oracle_repeat_3_out
```

Primary outputs:
- [paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl)
- [paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl)
- [paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl)
- [PAPER_REPEATED_SAMPLING_I7_SUMMARY.md](d:/My%20Project/companion-ai/PAPER_REPEATED_SAMPLING_I7_SUMMARY.md)

Main conclusion:
- The ranking `oracle i7 > real i7 > baseline` is stable across 3 repeated runs
- This is currently the strongest Stage-2 stability result

### E13. Hybrid Gap Diagnosis for i7

Purpose:
- Localize the remaining `real i7 -> oracle i7` gap
- Compare:
  - `explicit_rel_state_projected_i7`
  - `explicit_rel_state_projected_oracle_rel_i7`
  - `explicit_rel_state_projected_oracle_behavior_i7`
  - `explicit_rel_state_projected_oracle_i7`

Question:
- Is the remaining loss mainly coming from:
  - relation summary / stance side
  - behavior / execution interface side
  - or final realization after both are already aligned

Input:
- [paper_cases_oracle_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v1.json --output paper_results_exec_i7_hybrid_gap_v1.jsonl --modes explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_rel_i7 explicit_rel_state_projected_oracle_behavior_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_hybrid_gap_v1.jsonl --out-dir paper_eval_exec_i7_hybrid_gap_v1_out
```

Primary outputs:
- [paper_results_exec_i7_hybrid_gap_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_hybrid_gap_v1.jsonl)
- [paper_eval_exec_i7_hybrid_gap_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_i7_hybrid_gap_v1_out)
- gap diagnostic summary: [gap_diagnosis_i7.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_real_vs_oracle_v1_out/gap_diagnosis_i7.json)
- manual judge: [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_exec_i7_hybrid_gap_v1_out/manual_judge_results.md)

Main quantitative result:
- global average reply length:
  - `real i7`: `59.00`
  - `oracle_rel_i7`: `49.33`
  - `oracle_behavior_i7`: `31.72`
  - `oracle_i7`: `33.50`

Main conclusion:
- Swapping in oracle relation summaries helps only modestly
- Swapping in oracle behavior / execution constraints yields a much larger improvement
- `oracle_behavior_i7` is already close to `oracle_i7`
- Current interpretation:
  - the main remaining loss is more likely on the behavior / execution-interface side
  - final realization still contributes some noise, but does not currently look like the dominant bottleneck

### E14. Oracle Relation State + Real Projection

Purpose:
- Separate updater quality from projection-mapping quality
- Ask:
  - if relational state itself is already correct,
  - can the current real `project_behavior(...)` mapping produce a behavior control signal close to oracle?

Compare:
- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_state_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

Input:
- [paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json)

Representative run:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_state_exec_v1.json --output paper_results_exec_i7_state_gap_v1.jsonl --modes explicit_rel_state_projected_i7 explicit_rel_state_projected_oracle_state_i7 explicit_rel_state_projected_oracle_behavior_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_state_gap_v1.jsonl --out-dir paper_eval_exec_i7_state_gap_v1_out
```

Primary outputs:
- [paper_results_exec_i7_state_gap_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_state_gap_v1.jsonl)
- [paper_eval_exec_i7_state_gap_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_v1_out)

Main quantitative result:
- global average reply length:
  - `real i7`: `59.28`
  - `oracle_state_i7`: `116.72`
  - `oracle_behavior_i7`: `28.94`
  - `oracle_i7`: `37.22`

Case-level pattern:
- warm:
  - `real i7`: `56.5`
  - `oracle_state_i7`: `105.17`
  - `oracle_behavior_i7`: `35.5`
  - `oracle_i7`: `47.17`
- vulnerability:
  - `real i7`: `65.33`
  - `oracle_state_i7`: `108.5`
  - `oracle_behavior_i7`: `28.67`
  - `oracle_i7`: `26.33`
- cooling:
  - `real i7`: `56.0`
  - `oracle_state_i7`: `136.5`
  - `oracle_behavior_i7`: `22.67`
  - `oracle_i7`: `38.17`

Main conclusion:
- Merely replacing the relational state with oracle values does **not** close the gap.
- In fact, `oracle_state_i7` is often worse than `real i7`.
- `oracle_behavior_i7` remains close to `oracle_i7`.
- Current interpretation:
  - the dominant bottleneck is no longer best described as updater quality;
  - it is more likely located in the **relation -> behavior projection mapping** itself;
  - final realization still matters, but it is not the main source of the current gap.

### E15. Pure-Relation Projector Redesign (`v3a` / `v3b`)

Purpose:
- test whether the current failure can still be explained as a bad projector family;
- keep the two-layer design and continuous `relation -> behavior` mapping;
- avoid promoting `scene/phase` into the default answer too early.

Variants:
- `v3a`: conservative decoupled linear pure-relation projector
- `v3b`: nonlinear gated pure-relation projector

Input:
- [paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json)

Representative runs:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_state_exec_v1.json --output paper_results_exec_i7_state_gap_pv3a_v1.jsonl --modes explicit_rel_state_projected_i7_pv3a explicit_rel_state_projected_oracle_state_i7_pv3a explicit_rel_state_projected_oracle_behavior_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_state_gap_pv3a_v1.jsonl --out-dir paper_eval_exec_i7_state_gap_pv3a_v1_out

python paper_run_experiment.py --cases-json paper_cases_oracle_state_exec_v1.json --output paper_results_exec_i7_state_gap_pv3b_v1.jsonl --modes explicit_rel_state_projected_i7_pv3b explicit_rel_state_projected_oracle_state_i7_pv3b explicit_rel_state_projected_oracle_behavior_i7 explicit_rel_state_projected_oracle_i7
python paper_eval.py --input paper_results_exec_i7_state_gap_pv3b_v1.jsonl --out-dir paper_eval_exec_i7_state_gap_pv3b_v1_out
```

Primary outputs:
- [paper_results_exec_i7_state_gap_pv3a_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_state_gap_pv3a_v1.jsonl)
- [paper_eval_exec_i7_state_gap_pv3a_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pv3a_v1_out)
- [paper_results_exec_i7_state_gap_pv3b_v1.jsonl](d:/My%20Project/companion-ai/paper_results_exec_i7_state_gap_pv3b_v1.jsonl)
- [paper_eval_exec_i7_state_gap_pv3b_v1_out](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pv3b_v1_out)
- spec note: [PAPER_PURE_RELATION_PROJECTOR_V3.md](d:/My%20Project/companion-ai/PAPER_PURE_RELATION_PROJECTOR_V3.md)

Main quantitative results:

- `v3a`
  - `real i7_pv3a`: `37.22`
  - `oracle_state i7_pv3a`: `121.61`
  - `oracle_behavior i7`: `37.17`
  - `oracle i7`: `36.22`
- `v3b`
  - `real i7_pv3b`: `33.28`
  - `oracle_state i7_pv3b`: `129.61`
  - `oracle_behavior i7`: `36.33`
  - `oracle i7`: `34.89`

Main conclusion:
- both redesigned pure-relation projector families improve the real chain;
- neither brings `oracle_state_i7` meaningfully closer to `oracle_behavior_i7`;
- “the old projector is just too bad” is now a weaker explanation;
- the pure-relation hypothesis is not logically falsified, but it is materially weakened under the current relation representation;
- the next priority should shift to:
  - `relation redesign / reverse analysis`
  - and later `conditioned projector` as a necessity test.

### E16. Supervised Fit Baseline: `oracle_rel_effective -> oracle_behavior_effective`

Purpose:
- estimate the best-fit explanatory upper bound of the current 4D relation space before introducing `scene/phase`;
- distinguish between:
  - “current relation space is under-specified”
  - and “current hand-designed projector family is simply poor”.

Input:
- [paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json)

Representative run:

```bash
python paper_fit_relation_to_behavior.py --cases-json paper_cases_oracle_state_exec_v1.json --out-json paper_relation_behavior_fit_v1.json --out-md PAPER_RELATION_BEHAVIOR_FIT.md
```

Primary outputs:
- [paper_relation_behavior_fit_v1.json](d:/My%20Project/companion-ai/paper_relation_behavior_fit_v1.json)
- [PAPER_RELATION_BEHAVIOR_FIT.md](d:/My%20Project/companion-ai/PAPER_RELATION_BEHAVIOR_FIT.md)

Main quantitative results:

- linear 4D fit
  - `train_overall_mae = 0.0178`
  - `loocv_overall_mae = 0.0254`
- poly2 4D fit
  - `train_overall_mae = 0.0089`
  - `loocv_overall_mae = 0.0219`

Key LOOCV errors:
- linear
  - `E = 0.0375`
  - `Q_aff = 0.0333`
  - `Directness = 0.0319`
  - `T_w = 0.0288`
  - `Q_clarify = 0.0259`
  - `Initiative = 0.0239`
- poly2
  - `E = 0.0444`
  - `Directness = 0.0417`
  - `T_w = 0.0270`
  - `Q_clarify = 0.0182`
  - `Q_aff = 0.0164`
  - `Initiative = 0.0134`

Main conclusion:
- this result significantly weakens the claim that the current 4D relation space is obviously insufficient;
- with supervised best-fit regression, the current 4D relation variables can already explain oracle behavior surprisingly well;
- therefore the current crisis is more consistent with:
  - poor hand-designed projector families,
  - poor parameterization,
  - or an overly rigid projector design,
  rather than immediate proof that more relation dimensions are required;
- relation redesign remains possible, but it is no longer the next unavoidable step.

### E17. Unrestricted-Capacity Fit Comparison

Purpose:
- compare 4D explicit fits against higher-capacity function classes before introducing new relation dimensions;
- test whether the current 4D relation space hits a hard ceiling, or whether projector expressiveness is the bigger issue.

Primary outputs:
- [paper_relation_behavior_fit_v2.json](d:/My%20Project/companion-ai/paper_relation_behavior_fit_v2.json)
- [PAPER_RELATION_BEHAVIOR_FIT_V2.md](d:/My%20Project/companion-ai/PAPER_RELATION_BEHAVIOR_FIT_V2.md)

Compared models:
- `linear`
- `poly2`
- `mlp_h4`
- `mlp_h8`
- `mlp_h12`

Main LOOCV results:
- `linear`: `0.0254`
- `poly2`: `0.0219`
- `mlp_h4`: `0.0249`
- `mlp_h8`: `0.0269`
- `mlp_h12`: `0.0269`

Main conclusion:
- increasing hidden capacity does not beat the `poly2` 4D baseline on LOOCV;
- the strongest current fit remains a modestly richer 4D explicit function class, not a larger unconstrained network;
- this further supports the interpretation that:
  - the current 4D relation space is not obviously too weak,
  - and the next priority should be better projector fitting and deployment,
  - rather than immediately adding dimensions or introducing `scene/phase`.

Important boundary:
- this is still a small-sample result on the current oracle dataset (`18` rows);
- therefore it should be interpreted as:
  - "the current 4D explicit fit is already very competitive,"
  - not as:
  - "higher-capacity models can never outperform explicit low-order fits."
- plausible alternative explanations for `poly2`'s current advantage include:
  - small-sample stability,
  - current case distribution,
  - and the possibility that the present oracle labeling style is itself close to a low-order explicit function.

### E18. Deployable Fitted Projector Gap Test (`pfitlinear` / `pfitpoly2`)

Purpose:
- test whether a numerically strong fitted projector also improves the deployed end-to-end `oracle_state -> behavior -> language` chain;
- separate:
  - oracle-space regression quality,
  - from deployed projector quality inside the real `i7` execution stack.

Primary outputs:
- [paper_eval_exec_i7_state_gap_pfitlinear_v1_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pfitlinear_v1_out/global_summary.json)
- [paper_eval_exec_i7_state_gap_pfitpoly2_v1_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pfitpoly2_v1_out/global_summary.json)

Main results:
- `pfitlinear`
  - `real i7 = 55.28`
  - `oracle_state i7 = 136.78`
  - `oracle_behavior i7 = 36.67`
  - `oracle i7 = 32.28`
- `pfitpoly2`
  - `real i7 = 59.33`
  - `oracle_state i7 = 117.22`
  - `oracle_behavior i7 = 28.89`
  - `oracle i7 = 33.78`

Current interpretation:
- good oracle-space fit does **not** automatically transfer into good deployed projector behavior;
- both fitted projector variants still leave `oracle_state_i7` far from `oracle_behavior_i7 / oracle_i7`;
- therefore:
  - projector regression error is not the only issue,
  - and projector outputs must also be compatible with the downstream `i7` execution interface and realization stack.

### E19. Deployable Fitted Projector Family Extension (`pfitmlp_h4` / `pfitmlp_h8`)

Purpose:
- extend the deployable gap comparison from explicit fitted projectors to stronger fitted families;
- test whether better regression capacity helps once the projector is deployed into the actual `i7` execution stack.

Primary outputs:
- [paper_eval_exec_i7_state_gap_pfitmlp_h4_v2_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pfitmlp_h4_v2_out/global_summary.json)
- [paper_eval_exec_i7_state_gap_pfitmlp_h8_v2_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_exec_i7_state_gap_pfitmlp_h8_v2_out/global_summary.json)

Main results:
- `pfitmlp_h4`
  - `real i7 = 58.00`
  - `oracle_state i7 = 138.94`
  - `oracle_behavior i7 = 35.67`
  - `oracle i7 = 34.78`
- `pfitmlp_h8`
  - `real i7 = 61.83`
  - `oracle_state i7 = 131.17`
  - `oracle_behavior i7 = 37.33`
  - `oracle i7 = 34.67`

Current interpretation:
- stronger fitted projector families still do not rescue deployed `oracle_state_i7`;
- therefore the deployment gap is not solved simply by increasing function capacity inside the oracle-space fit;
- this further supports a distinction between:
  - relation-space explanatory fit,
  - and deployable controller compatibility.

Implementation note:
- current summary outputs contain a naming typo for the oracle-state fitted MLP modes (`pfitmpl_h4/h8` instead of `pfitmlp_h4/h8`);
- the results remain readable, but downstream tooling should avoid assuming the corrected spelling until the naming bug is fixed.

### E20. Fitted Projector Deployment Fix and Route Gap Recheck (`pfitpoly2 v3`)

Purpose:
- repair the fitted-projector deployment path so that `fitpoly2` actually uses the exported regression weights;
- re-evaluate whether `relation -> fitted 8D -> i7` still fails after the implementation fix;
- quantify whether `8D -> i7` is a large distortion source or only a local sensitivity source.

Primary outputs:
- `paper_results_gap_rel8_i7_pfitpoly2_v3.jsonl`
- `paper_eval_gap_rel8_i7_pfitpoly2_v3_out/global_summary.json`
- `paper_interface_gap_rel8_i7_pfitpoly2_v3.json`

Main results:
- `real projected_i7_pfitpoly2 = 42.00`
- `oracle_state projected_i7_pfitpoly2 = 33.72`
- `oracle_behavior_i7 = 37.06`
- `oracle_i7 = 28.17`

Interface-gap analysis:
- `oracle_state_rows_analyzed = 18`
- average per-dimension absolute deltas are small:
  - `Directness = 0.0194`
  - `E = 0.0184`
  - `T_w = 0.0115`
  - `Q_clarify = 0.0063`
  - `Q_aff = 0.0056`
  - `Initiative = 0.0049`
- `i7` bucket mismatches are rare:
  - only one substantial mismatch case was found,
  - concentrated in `oracle_exec_vuln_001 / E_ordinary_continuation`
  - and localized to:
    - `warmth_level`
    - `relational_push`
    - `support_mode`

Current interpretation:
- earlier deploy-gap readings for `pfit*` were partially polluted by implementation issues and should not be treated as final;
- after the fix, `relation -> fitted 8D -> i7` is no longer obviously broken;
- `8D -> i7` introduces some local sensitivity, but it does not currently look like the dominant distortion source;
- the corrected evidence now supports a stronger statement:
  - an analytic 8D behavior layer can be bridged into a deployable `i7` interface with relatively low loss under a good fitted projector.

Important caution:
- current deployable support is real for `fitlinear` / `fitpoly2`;
- current `fitmlp_*` artifacts remain evaluation-only, because deployable MLP parameters were not exported in `paper_relation_behavior_fit_v2.json`.

### E21. Direct Deploy Interface Route (`relation -> i7`)

Purpose:
- test whether bypassing the 8D behavior layer produces a cleaner deployable controller;
- compare:
  - `relation -> fitted 8D -> i7`
  - `relation -> direct i7`

Primary outputs:
- `paper_results_gap_rel_i7_direct_v1.jsonl`
- `paper_eval_gap_rel_i7_direct_v1_out/global_summary.json`

Main results:
- `real direct i7 = 29.78`
- `oracle_state direct i7 = 20.33`
- `oracle full i7 = 31.67`

Current interpretation:
- direct `relation -> i7` is clearly viable and should remain an active route candidate;
- however, after the `pfitpoly2 v3` fix, it is no longer justified to say that the 8D behavior layer is the main deploy problem by default;
- the main unresolved route question is now:
  - whether the project should treat 8D behavior as:
    - a true deployable bridge layer,
    - or mainly an analytic layer with direct-to-interface deployment as the simpler controller route.

### E22. Route-Focused Formal Judge Setup

Purpose:
- produce a clean judge package for the main control-route comparison;
- compare:
  - `relation -> direct i7`
  - `relation -> fitted 8D -> i7`
- do this both for the real route and for the oracle-state route.

Primary outputs:
- [paper_results_route_compare_v1.jsonl](d:/My%20Project/companion-ai/paper_results_route_compare_v1.jsonl)
- [paper_eval_route_compare_v1_out](d:/My%20Project/companion-ai/paper_eval_route_compare_v1_out)
- [route_focused_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_route_compare_v1_out/route_focused_case_level_judge_inputs.json)
- [route_focused_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_route_compare_v1_out/route_focused_pairwise_judge_inputs.json)
- [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_route_compare_v1_out/manual_judge_results.md)

First-pass manual reading:
- real-route comparison:
  - direct `relation -> i7` looks better in `warm` and `cool`
  - `vulnerability` is closer to a tie because the direct route has less push but also more awkward meta phrasing
- oracle-state comparison:
  - `warm` currently favors the direct route
  - `vulnerability` currently favors `relation -> fitted 8D -> i7`
  - `cool` currently favors `relation -> fitted 8D -> i7`
- this means no route has yet achieved a clean across-the-board win.

Important artifact note:
- the current route-focused comparisons against `explicit_rel_state_projected_oracle_i7` still include duplicated turn entries in some exports;
- those `...vs_oracle_full_i7` comparisons should therefore be treated as provisional until export cleanup is done.

### E23. Route-Compare Export Cleanup and Route-Freeze Recheck

Purpose:
- remove duplicated-turn pollution in route-focused comparisons against `explicit_rel_state_projected_oracle_i7`;
- regenerate a clean route-judge package;
- check whether route freeze can now be decided more cleanly.

Inputs:
- [paper_results_route_compare_v1.jsonl](d:/My%20Project/companion-ai/paper_results_route_compare_v1.jsonl)
- cleaned eval logic in [paper_eval.py](d:/My%20Project/companion-ai/paper_eval.py)

Run:

```bash
python paper_eval.py --input paper_results_route_compare_v1.jsonl --out-dir paper_eval_route_compare_v2_out
```

Primary outputs:
- [paper_eval_route_compare_v2_out](d:/My%20Project/companion-ai/paper_eval_route_compare_v2_out)
- [route_focused_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_route_compare_v2_out/route_focused_case_level_judge_inputs.json)
- [route_focused_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_route_compare_v2_out/route_focused_pairwise_judge_inputs.json)

Main conclusion:
- the route-focused package is now clean at the session level; duplicated `turn_idx` entries from `oracle_full_i7` exports are removed;
- the core route picture remains the same after cleanup:
  - on the real route, direct `relation -> i7` still looks better in `warm` and `cool`, with `vulnerability` close to a tie;
  - on the oracle-state route, `relation -> fitted 8D -> i7` remains genuinely competitive and still looks better in `vulnerability` and `cool`, while direct `relation -> i7` looks cleaner in `warm`;
- therefore the strongest current route-freeze interpretation is not a full winner-take-all freeze.

Working route-freeze read:
- `relation -> i7` should currently be treated as the simpler and stronger **main deployable controller candidate**;
- `relation -> fitted 8D -> i7` should be retained as the stronger **analytic-bridge candidate**, not discarded as a broken route;
- the paper should not currently claim that one route universally dominates the other across all cases and route conditions.

### E24. Post-Freeze Oracle Set Expansion (`v2`)

Purpose:
- expand the oracle evaluation set after route freeze without exploding scope;
- move beyond the original `warm / vulnerability / cool` trio;
- add `mixed_signal` coverage before the final frozen evaluation.

New files:
- [paper_cases_oracle_exec_v2.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v2.json)
- [paper_cases_oracle_state_exec_v2.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v2.json)

What changed:
- the base oracle execution set grows from 3 cases to 5 cases;
- two `mixed_signal_trajectory` cases are added:
  - `oracle_exec_mixed_001`
  - `oracle_exec_mixed_002`
- total oracle phase points increase from 18 to 30.

Design choice:
- this is a minimal intermediate expansion rather than the final large-sample study;
- the goal is to validate the freeze decision on a broader but still manageable oracle set before any much larger final run.

Recommended post-freeze runs:

Main frozen comparison:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_exec_v2.json --output paper_results_frozen_main_v2.jsonl --modes baseline_relational_instruction explicit_rel_state_rel_to_interface_i7 explicit_rel_state_projected_oracle_i7 --max-concurrency 2
python paper_eval.py --input paper_results_frozen_main_v2.jsonl --out-dir paper_eval_frozen_main_v2_out
```

Analytic-bridge sanity:

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_state_exec_v2.json --output paper_results_frozen_bridge_v2.jsonl --modes explicit_rel_state_projected_oracle_state_i7_pfitpoly2 explicit_rel_state_projected_oracle_behavior_i7 explicit_rel_state_projected_oracle_i7 --max-concurrency 2
python paper_eval.py --input paper_results_frozen_bridge_v2.jsonl --out-dir paper_eval_frozen_bridge_v2_out
```

Current role in the paper:
- `relation -> i7` remains the main deployable route to carry forward;
- `relation -> fitted 8D -> i7` remains the main analytic bridge to validate and interpret;
- the expanded `v2` oracle set is the recommended next-step evaluation substrate for both.

### E24. Same-Family Stronger-Model Sanity Check (`gpt-5-mini`)

Purpose:
- test whether the main ordering and the corrected `fitpoly2` bridge behavior still hold on a stronger same-family model;
- reduce the risk that the current findings are a `gpt-5-nano` artifact.

Primary outputs:
- [paper_eval_sanity_gpt5mini_main_v1_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_sanity_gpt5mini_main_v1_out/global_summary.json)
- [paper_eval_sanity_gpt5mini_gap_v1_out/global_summary.json](d:/My%20Project/companion-ai/paper_eval_sanity_gpt5mini_gap_v1_out/global_summary.json)

Main results:
- main route sanity:
  - `baseline_relational_instruction = 104.61`
  - `explicit_rel_state_projected_i7 = 58.17`
  - `explicit_rel_state_projected_oracle_i7 = 34.33`
- gap sanity:
  - `explicit_rel_state_projected_oracle_state_i7_pfitpoly2 = 38.72`
  - `explicit_rel_state_projected_oracle_behavior_i7 = 44.61`
  - `explicit_rel_state_projected_oracle_i7 = 45.56`

Current interpretation:
- the coarse main ordering `oracle > real > baseline` still appears on a stronger same-family model when using reply-length as a rough proxy;
- the corrected `fitpoly2` bridge remains viable rather than collapsing under the stronger model;
- this does not yet establish full cross-model generalization, but it substantially reduces the risk that the current mechanism findings are unique to `gpt-5-nano`.

## Current High-Level Conclusions

### What has been supported

- Relational state as a slow variable is internally plausible
- Strong baselines are genuinely competitive
- Prompt bridge matters, but does not appear to be the main bottleneck
- `projected_oracle > projected` is repeated evidence
- `projected_oracle > oracle-collapsed-single-layer` is repeated evidence
- Two-layer control has genuine structural potential
- `oracle i7 > real i7 > strong baseline` is now supported by both manual judge and repeated sampling
- `real i7 -> oracle i7` gap currently appears to be dominated more by behavior-side mismatch than by relation-summary mismatch
- `oracle relation state + real projection` further sharpens this result:
  - current projector quality now looks like the main bottleneck
  - not just relation wording, and not primarily updater quality

### What has not been supported

- Real `explicit_rel_state_projected` does not yet stably beat strong baseline
- It is not justified to claim that explicit state automatically yields better language-layer coherence
- It is not justified to say that the main problem is only upstream state updating
- It is not justified to claim that supplying better relational state alone is sufficient

### Working interpretation at the current point

- The main bottleneck is more likely in realization than in state existence
- Stage 1 established that:
  - the problem is real
  - strong baselines are hard to beat
  - two-layer control is worth deeper study
- Stage 2 should focus on interface quality:
  - ideal two-layer vs strong baseline
  - real two-layer vs ideal two-layer
  - executable interface design
- Within Stage 2, the next concrete optimization target is:
  - the deterministic `relation -> behavior` projector

## Practical Reproduction Advice

If reproducing from scratch, use this order:

1. Reproduce long-case setup:
   - [paper_cases_long_v1.json](d:/My%20Project/companion-ai/paper_cases_long_v1.json)
2. Reproduce oracle-state comparison:
   - [paper_cases_oracle_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_v1.json)
3. Reproduce Scheme B:
   - baseline vs projected vs projected_oracle
4. Reproduce control-alignment:
   - projected_oracle vs oracle-collapsed-single-layer
5. Reproduce execution-interface family:
   - v1 and v2
6. Reproduce i7 gap diagnosis:
   - hybrid gap
   - oracle relation state + real projection

## Open TODOs

- Add the mixed-signal long case as the final Stage 1 closing replication
- Compare `i6` vs `i7` against `baseline_relational_instruction`
- Bring the strongest Stage 2 interface family back into real-chain testing
- Redesign and retest the deterministic projector against oracle behavior targets
- Run the final mixed-signal Stage-1 closing replication
- Decide whether Stage 2 main narrative should be:
  - ideal two-layer vs strong baseline
  - or executable interface family vs strong baseline


## E25. Final frozen manual judge

Inputs:
- [final_main_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/final_main_case_level_judge_inputs.json)
- [final_main_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/final_main_pairwise_judge_inputs.json)
- [final_bridge_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/final_bridge_case_level_judge_inputs.json)
- [final_bridge_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/final_bridge_pairwise_judge_inputs.json)

Manual reading record:
- [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/manual_judge_results.md)

Main frozen comparison:
- `direct relation -> i7` beats strong baseline on all 5 oracle cases (`warm`, `vulnerability`, `cooling`, `mixed_001`, `mixed_002`).
- `oracle_i7` also beats strong baseline on all 5 cases.
- `oracle_i7` vs direct `relation -> i7` is now mostly `tie` or slight oracle edge rather than a large gap.
- This supports freezing `relation -> i7` as the paper's main deployable controller.

Bridge sanity:
- corrected `oracle_state_i7_pfitpoly2` is manually very close to `oracle_behavior_i7` and `oracle_i7` on most cases;
- the main residual weakness is a small oracle edge on vulnerability-style supportive turns;
- this supports retaining `relation -> fitted 8D -> i7` as an analytic-bridge route rather than dropping it.

Paper-level reading after freeze:
- deploy route: `relation -> i7`
- analytic bridge: `relation -> behavior(8D) -> i7`
- current strongest claim is no longer only that a two-layer line has oracle potential, but that the frozen system now supports both a deployable controller and a near-oracle analytic bridge.


## E26. Final judge rubric and next-step ordering

Added:
- [PAPER_FINAL_JUDGE_PLAN.md](d:/My%20Project/companion-ai/PAPER_FINAL_JUDGE_PLAN.md)
- [PAPER_NEXT_STEPS_ORDER.md](d:/My%20Project/companion-ai/PAPER_NEXT_STEPS_ORDER.md)

Purpose:
- freeze a more credible endgame evaluation protocol centered on manual coherence judge and pairwise comparison rather than response length;
- freeze the recommended order of remaining work after route freeze.

Current recommended order:
1. final judge write-up
2. moderate data expansion
3. 4D fitted-parameter interpretation
4. deployable-interface shape comparison
5. relation dimensionality search


## E27. 4D fitted-model parameter interpretation

Added:
- [PAPER_4D_PARAMETER_INTERPRETATION.md](d:/My%20Project/companion-ai/PAPER_4D_PARAMETER_INTERPRETATION.md)

Current interpretation of the fitted `poly2` bridge:
- the 4D relation space does not behave like a naive "more closeness -> more warmth -> more expansion" rule;
- instead, the strongest cross-dimension pattern is a permission/receptivity-style structure:
  - `bond/care` mostly govern warmth;
  - `trust` plus interaction terms govern whether continued movement is permitted;
  - `stability` mostly suppresses over-expansion and over-pursuit.

This strengthens the analytic-bridge story while staying short of claiming a universal human theory of relationships.


## E28. Large oracle-expansion target and relation-dimension validation order

Added:
- [PAPER_ORACLE_EXPANSION_PLAN_150PLUS.md](d:/My%20Project/companion-ai/PAPER_ORACLE_EXPANSION_PLAN_150PLUS.md)
- updated [PAPER_NEXT_STEPS_ORDER.md](d:/My%20Project/companion-ai/PAPER_NEXT_STEPS_ORDER.md)

Decision:
- do not stop at a small incremental expansion;
- expand the oracle substrate to at least `144` phase points, with `180` as the preferred target;
- keep `mixed_signal` as a required family;
- after expansion, relation-dimensionality validation is now promoted ahead of deployable-interface shape comparison.


## E29. Oracle expansion to 180 phase points

Generated:
- [paper_generate_oracle_cases_v3.py](d:/My%20Project/companion-ai/paper_generate_oracle_cases_v3.py)
- [paper_cases_oracle_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v3.json)
- [paper_cases_oracle_state_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v3.json)

Expansion result:
- `30` oracle cases
- `180` oracle phase points
- `6` families, each with `5` cases:
  - `warming_trajectory`
  - `vulnerability_with_correction`
  - `cooling_trajectory`
  - `mixed_signal_trajectory`
  - `ordinary_neutral`
  - `boundary_repair`

This is now the main large-scale oracle substrate for the next frozen reruns and the later relation-dimensionality validation.


## E30. Post-expansion relation dimensionality validation on 180 oracle rows

Added:
- [paper_validate_relation_dimensionality.py](d:/My%20Project/companion-ai/paper_validate_relation_dimensionality.py)
- [paper_relation_dimensionality_validation_v1.json](d:/My%20Project/companion-ai/paper_relation_dimensionality_validation_v1.json)
- [PAPER_RELATION_DIMENSIONALITY_VALIDATION.md](d:/My%20Project/companion-ai/PAPER_RELATION_DIMENSIONALITY_VALIDATION.md)

Dataset:
- `180` oracle phase rows from `paper_cases_oracle_state_exec_v3.json`

Main result:
- on both `linear` and `poly2`, the current `raw4` relation space is the best-performing representation among all tested 2D and 3D subsets;
- best 3D subsets remain competitive but consistently worse:
  - `linear`: best 3D = `bond+care+trust`, LOOCV `0.0220` vs `raw4` `0.0216`
  - `poly2`: best 3D = `care+trust+stability`, LOOCV `0.0169` vs `raw4` `0.0158`
- therefore dropping one of the current four axes incurs a real explanatory cost on the expanded oracle substrate.

Important boundary:
- the current 5D/6D variants (`aug5_permission`, `aug6_permission_warmth`) are only linearly derived augmentations of the original 4D variables;
- under the current linear / quadratic model family they are largely expressively redundant with `raw4`;
- so the present `5D/6D ~= 4D` result should not be over-read as proof that richer relation ontologies are unnecessary.

Current paper-facing reading:
- the expanded data now supports a stronger claim that the current 4D relation space is not accidental or trivially over-specified;
- however, testing truly new >4D relation ontologies would still require genuinely new annotated factors rather than deterministic transforms of the existing 4D labels.


## E31. Next-step ontology expansion plan (>4D)

Added:
- [PAPER_RELATION_ONTOLOGY_EXPANSION.md](d:/My%20Project/companion-ai/PAPER_RELATION_ONTOLOGY_EXPANSION.md)
- [paper_build_relation_ontology_annotation_sheet.py](d:/My%20Project/companion-ai/paper_build_relation_ontology_annotation_sheet.py)
- [paper_relation_ontology_annotation_sheet_v1.csv](d:/My%20Project/companion-ai/paper_relation_ontology_annotation_sheet_v1.csv)
- [paper_relation_ontology_annotation_sheet_v1.json](d:/My%20Project/companion-ai/paper_relation_ontology_annotation_sheet_v1.json)

Decision:
- do not treat deterministic 5D/6D augmentations of the current 4D labels as the final answer;
- the next serious relation-representation step should be a genuinely new annotated ontology.

Current recommended candidates:
1. `raw4 + interactional_permission`
2. `raw4 + interactional_permission + boundary_firmness`

Rationale:
- the fitted bridge repeatedly behaves as if a latent “permission to continue” factor exists;
- difficult `mixed_signal` / `boundary_repair` cases suggest a distinct boundary-calibration factor may also be needed;
- these factors are semantically motivated, manually annotatable, and not reducible to a single linear transform of the existing 4D labels.


## E32. Unsupervised latent dimensionality search (2D-6D)

Added:
- [paper_relation_latent_dim_search.py](d:/My%20Project/companion-ai/paper_relation_latent_dim_search.py)
- [paper_relation_latent_dim_search_v1.json](d:/My%20Project/companion-ai/paper_relation_latent_dim_search_v1.json)
- [PAPER_RELATION_LATENT_DIM_SEARCH.md](d:/My%20Project/companion-ai/PAPER_RELATION_LATENT_DIM_SEARCH.md)

Purpose:
- avoid hand-defining new 5D/6D relation meanings too early;
- test whether a richer latent basis helps before any semantic interpretation is imposed.

Setup:
- source labels: current raw4 relation variables
- shared feature space: `17` higher-order features derived from raw4
- learned latent dimensionalities: `2D`, `3D`, `4D`, `5D`, `6D`
- target: 8D oracle behavior

LOOCV overall MAE:
- latent `2`: `0.0235`
- latent `3`: `0.0230`
- latent `4`: `0.0214`
- latent `5`: `0.0200`
- latent `6`: `0.0200`

Reading:
- `2D/3D` are clearly weaker than `4D`;
- `4D` remains a strong explanatory basis;
- `5D/6D` provide a modest but real gain over `4D`;
- therefore the present 4D ontology looks robust, but likely not fully explanation-optimal.

Important boundary:
- this experiment does **not** produce a human-readable 5D ontology by itself;
- it only shows that a slightly richer learned latent basis appears helpful.


## E33. First interface-shape comparison

Added:
- [paper_build_interface_shape_judge_pack.py](d:/My%20Project/companion-ai/paper_build_interface_shape_judge_pack.py)

Compared three deploy charts:
- `8D -> i7-discrete`
- `8D -> continuous-interface (c8)`
- `relation -> i7 direct`

Main run (`180` turns):
- `explicit_rel_state_projected_i7_pfitpoly2 = 41.79`
- `explicit_rel_state_projected_c8_pfitpoly2 = 112.24`
- `explicit_rel_state_rel_to_interface_i7 = 25.07`
- `explicit_rel_state_projected_oracle_i7 = 30.41`

Bridge run (`180` turns):
- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2 = 33.05`
- `explicit_rel_state_projected_oracle_state_c8_pfitpoly2 = 94.43`
- `explicit_rel_state_rel_to_interface_oracle_state_i7 = 23.48`
- `explicit_rel_state_projected_oracle_behavior_i7 = 32.92`
- `explicit_rel_state_projected_oracle_i7 = 31.66`

Reading:
- the first continuous deploy chart is clearly unstable and systematically over-expansive;
- the best current deploy chart remains direct `relation -> i7`;
- the best current analytic bridge remains `relation -> fitted 8D behavior -> i7`;
- therefore the current paper should not treat “more continuous” as automatically “more faithful” at deployment time.

Current boundary:
- this comparison only rules out the first naive continuous chart (`c8`);
- it does **not** yet imply that all softer or semi-continuous charts are worse than `i7`.


## E34. Interface-shape comparison v2 scaffolding

Added in code:
- support for three additional projected interface charts:
  - `o8` = ordinal-soft
  - `b8` = banded-continuous
  - `h8` = hybrid

Purpose:
- test whether the weakness of `c8` comes from continuity itself, or from giving raw continuous controls too directly to the model.

Current paper-facing reading:
- the current interface question is no longer just `discrete vs continuous`;
- it is now a deploy-chart search problem:
  - hard discrete chart (`i7`)
  - soft ordinal chart (`o8`)
  - banded chart (`b8`)
  - hybrid chart (`h8`)
  - naive continuous chart (`c8`)


## E35. Current status correction on latent-dimensionality search

Important correction:
- the current `paper_relation_latent_dim_search_v1.json` result should be treated only as a supporting probe around the existing `raw4` ontology;
- because its feature space is still constructed from the current four labeled axes, it is **not** a truly ontology-free factor-discovery experiment.

Therefore:
- do not treat `2D-6D latent` from that run as the new mainline;
- use it only as a local signal that:
  - current `4D` is robust,
  - a slightly richer latent basis may exist,
  - but true manifold / factor discovery still remains open.


## E36. Main deploy ontology / wording ablation (`vA/vB/vC`, `sa/sb/sc`)

Compared on the expanded `v3` main substrate:

- ontology variants:
  - `vA` = current `i7` ontology
  - `vB` = interactional-7 ontology
  - `vC` = permission-7 ontology
- wording variants:
  - `sa`
  - `sb`
  - `sc`

Main diagnostic summary:

- projected route:
  - `sa_vA = 44.26`
  - `sb_vA = 43.69`
  - `sc_vA = 44.92`
  - `sa_vB = 47.28`
  - `sb_vB = 52.69`
  - `sc_vB = 51.67`
  - `sa_vC = 46.32`
  - `sb_vC = 52.37`
  - `sc_vC = 44.99`
- direct route:
  - `sa_vA = 21.69`
  - `sb_vA = 25.30`
  - `sc_vA = 23.51`
  - `sa_vB = 29.59`
  - `sb_vB = 34.67`
  - `sc_vB = 27.79`
  - `sa_vC = 22.31`
  - `sb_vC = 28.49`
  - `sc_vC = 22.61`

Reading:

- ontology effects appear larger than pure naming / framing effects;
- current `vA` remains the most stable deploy ontology;
- `vC` remains the only serious alternative worth keeping;
- `vB` does not currently show a convincing advantage on the main deploy route;
- `sb` systematically tends to expand more than `sa` / `sc`;
- therefore the current mainline candidates are:
  - `vA + sa/sc`
  - `vC + sa/sc`

Important boundary:

- these are still proxy-level readings;
- length alone cannot settle whether `vC` is genuinely worse, or merely slightly longer but more coherent;
- therefore the next required step is focused manual judge.


## E37. Bridge ontology / wording sanity (`v1` small sample)

Compared on the `v1` oracle-state bridge substrate (`18` turns):

- projected oracle-state bridge:
  - `sa_vA = 37.22`
  - `sb_vA = 37.44`
  - `sc_vA = 33.50`
  - `sa_vB = 39.56`
  - `sb_vB = 48.17`
  - `sc_vB = 38.44`
  - `sa_vC = 40.67`
  - `sb_vC = 44.33`
  - `sc_vC = 42.39`
- direct oracle-state route:
  - `sa_vA = 26.06`
  - `sb_vA = 22.78`
  - `sc_vA = 24.44`
  - `sa_vB = 30.78`
  - `sb_vB = 35.56`
  - `sc_vB = 24.94`
  - `sa_vC = 22.00`
  - `sb_vC = 29.61`
  - `sc_vC = 17.28`

Reading:

- no bridge-side reversal was observed;
- `vA` remains the most stable ontology on the projected bridge;
- `sc_vA` is the single strongest bridge-facing wording configuration in this small-sample sanity check;
- `vC` remains interesting, but did not displace `vA`;
- `vB` again fails to show a convincing bridge advantage.

Current working conclusion:

- main deploy ontology:
  - current best = `vA`
  - keep `vC` as the only serious alternative
- wording:
  - retain `sa` and `sc`
  - deprioritize `sb`
- next step:
  - run focused manual judge on the shortlisted candidates rather than relying further on length proxy alone.


## E38. Collaborative preliminary manual judge update

Collaborative manual reading has now covered representative `main` pairwise cases from:

- `oracle_exec_warm_001`
- `oracle_exec_vuln_001`
- `oracle_exec_cool_001`
- `oracle_exec_repair_002`

Current reading update:

- `vA` remains the best default deploy ontology across families.
- `vC` should not be treated as a uniformly worse ontology; it now looks more like a vulnerability-sensitive alternative that can sound softer / more tender in `vuln` cases.
- `sc` is now the most promising framing variant overall.
- `sa_vA` should not be described as strongly tool-like; its main weakness is lower temperature / weaker relationship presence, not projected-style explanatory behavior.
- the projected route's main failure is not just scalar over-expansion, but a broader drift toward tool-like, explanatory, and less person-like interaction.
- `relation -> i7 direct` remains the strongest deploy route.
- the strongest current real candidate is:
  - `explicit_rel_state_rel_to_interface_i7_sc_vA`

Project-level interpretation update:

- `vA` = default deploy ontology
- `vC` = family-sensitive alternative worth retaining, especially for vulnerability-like settings
- `sc` = best current semantic framing
- projected route = retain as analytic bridge, not main deployment route


## E39. Deploy ontology line frozen; manifold analysis becomes next mainline

After the collaborative manual reading, the deploy ontology line is now considered sufficiently frozen for the paper:

- main deploy route:
  - `relation -> i7 direct`
- default deploy ontology:
  - `vA`
- best framing:
  - `sc`
- best current real candidate:
  - `direct sc_vA`
- keep `vC` as a vulnerability-sensitive alternative
- keep `relation -> behavior(8D) -> i7` as the analytic bridge

Next mainline research stage:

- move from ontology invention toward shared latent manifold / coordinate-structure analysis;
- test whether `relation`, `behavior`, `i7`, and language features behave like different charts on a shared latent interaction manifold.


## E40. Shared latent manifold M1 scaffolding

Implemented first-pass M1 geometry-alignment tooling:

- [paper_shared_manifold_m1.py](d:/My%20Project/companion-ai/paper_shared_manifold_m1.py)

What the script does:

- takes an existing experiment result JSONL plus one or more selected modes;
- exports per-phase datasets containing:
  - relation raw4 view
  - behavior 8D view
  - mode-specific numericized `i7` chart
  - language-side feature vectors
- computes:
  - distance-matrix correlations across views
  - kNN neighborhood overlap across views
  - per-view trajectory smoothness over case phases

Important boundary of this first pass:

- oracle behavior is used as the default analytic behavior view when available;
- this is an M1 geometry sanity check, not yet a learned shared-latent model.


## E41. Shared latent manifold M1 results

On the frozen best real candidate (`direct sc_vA`), the corrected M1 analysis supports:

- `raw4 relation` and `behavior_8d` share the strongest local neighborhood alignment;
- `i7` is more closely aligned with language realization than `behavior_8d` is;
- `behavior_8d` and `i7` are not simply the same chart under light compression;
- trajectory smoothness follows a plausible hierarchy:
  - relation smoothest
  - `i7` next
  - language most noisy

Important boundary:

- these are geometry-level consistency checks;
- because the current behavior ontology was designed within the same research program, M1 should not be over-read as an external validation of the ontology itself.


## E42. Shared latent manifold M2 results

Implemented:

- [paper_shared_manifold_m2.py](d:/My%20Project/companion-ai/paper_shared_manifold_m2.py)

M2 learns a low-dimensional latent from:

- `behavior`
- `i7`
- language features

and then predicts `relation_raw4` back from that latent afterwards.

Current reading:

- a shared latent can jointly reconstruct `behavior`, `i7`, and language features with high accuracy;
- the same latent can also predict `relation_raw4` strongly;
- this is stronger than the M1 consistency check because relation is not used to build the latent itself;
- the oracle route organizes the shared latent more cleanly than the current best real route, especially on the `i7` and language sides.

Current interpretation:

- the main open problem is no longer best described as whether relation state exists at all;
- it is better described as how faithfully the shared interaction structure is preserved from analytic views into deploy realization.


## E43. Shared latent manifold M2.5 scaffold

Implemented:

- [paper_shared_manifold_m25.py](d:/My%20Project/companion-ai/paper_shared_manifold_m25.py)

Purpose:

- move one step beyond M2 without jumping directly into a heavy M3 trajectory-manifold claim;
- keep learning the latent only from:
  - `behavior`
  - `i7`
  - language features
- avoid using `relation_raw4` to build the latent itself;
- then test whether the learned latent is stable enough to support:
  - strong relation prediction back from the latent,
  - family-level separability,
  - within-case trajectory smoothness.

Current role in the project:

- this is the first explicit inverse-manifold probe in the new line;
- it is meant to answer whether the latent discovered from downstream views is strong enough to justify treating `4D / 8D / i7` as different charts over a shared interaction structure;
- if M2.5 is weak, the paper should stop at the more modest M1/M2 interpretation;
- if M2.5 is strong, then a heavier M3 trajectory-level manifold study becomes justified.


## E44. Shared latent manifold M3-lite scaffold

Implemented:

- [paper_shared_manifold_m3_lite.py](d:/My%20Project/companion-ai/paper_shared_manifold_m3_lite.py)

Purpose:

- avoid jumping directly from M2.5 to a very broad full-M3 claim;
- fit one pooled latent basis across a very small set of key routes;
- compare trajectory behavior directly inside that shared latent space.

Current intended use:

- primary comparison:
  - `direct sc_vA`
  - `oracle_i7`
- optional bridge comparison:
  - `oracle_state_i7_pfitpoly2`

Current questions:

- does the best real route follow the same latent path geometry as oracle, just with more noise?
- where is path distortion concentrated across families such as vulnerability, cooling, and boundary repair?
- is the bridge route path geometry closer to oracle than to a merely tool-like detour?


## E45. Shared latent manifold M3-lite results

Run on:

- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_projected_oracle_i7`

using one pooled latent basis of size `6D`.

Current reading:

- the best real route and the oracle route occupy broadly similar trajectory geometry rather than two unrelated path systems;
- the real route is better read as a noisier or flattened version of the oracle path structure;
- the strongest path distortion appears in:
  - `cooling`
  - `boundary_repair`
- path distortion is smaller in:
  - `mixed_signal`
  - `vulnerability`
  - `warm`

Most useful implication:

- the remaining deploy gap is not best described as a wrong overall route;
- it is better described as a trajectory-distortion or structure-preservation problem, with the sharpest failures in cooling and repair-like families.

Research-facing consequence:

- this supports keeping the current deploy story frozen;
- it does **not** strongly motivate another round of highly applied interface tweaking as the main next step;
- instead it supports a more theory-facing reading in which current charts are useful views over a shared interaction structure, while the next research question is how that structure should be inferred and represented more natively.


## E46. Native latent discovery scaffold

Implemented:

- [paper_native_latent_discovery.py](d:/My%20Project/companion-ai/paper_native_latent_discovery.py)
- [PAPER_NATIVE_LATENT_DISCOVERY.md](d:/My%20Project/companion-ai/PAPER_NATIVE_LATENT_DISCOVERY.md)

Purpose:

- treat the real theory-facing question directly:
  - learn latent interaction structure from
    - `behavior_8d`
    - `i7_numeric`
    - `language_features`
  - without using `relation_raw4` to build the latent;
- sweep latent dimensionality;
- test not only reconstruction quality but also:
  - family structure
  - trajectory smoothness
  - optional relation readout afterwards.

Current role:

- this is the clearest current path toward the question that motivated the manifold line from the start;
- it shifts emphasis away from proving the hand-defined `4D / 8D / i7` stack as final ontology;
- instead it asks what native latent structure is suggested by the jointly observed analytic, deploy, and realization views.


## E47. Native chart reading scaffold

Implemented:

- [paper_native_chart_reading.py](d:/My%20Project/companion-ai/paper_native_chart_reading.py)
- [PAPER_NATIVE_CHART_READING.md](d:/My%20Project/companion-ai/PAPER_NATIVE_CHART_READING.md)

Purpose:

- once a native latent is learned from `behavior + i7 + language`, stop treating `raw4 / 8D / i7` as starting ontology;
- instead treat them as candidate charts or readouts of that latent;
- compare:
  - readout quality from native latent;
  - geometry alignment with native latent.


## E48. Native latent discovery extended to 16D

Run on:

- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_projected_oracle_i7`

with latent dimensionalities:

- `2D` through `16D`

Current reading:

- reconstruction quality continues to improve through `16D` on both the best real route and the oracle route;
- therefore the native latent suggested by the current multi-view data is clearly richer than:
  - `4D`
  - `6D`
  - `8D`
  - `12D`
- by contrast, family-prediction and local-neighbor purity change only modestly across the same range;
- trajectory diagnostics also remain comparatively stable once the latent reaches a medium-dimensional regime.

Current implication:

- the native interaction structure does not currently look like a small low-dimensional ontology;
- the project should therefore stop treating `raw4` as a candidate for the native latent itself;
- instead `raw4` should be treated as a coarse chart over a richer underlying structure.


## E49. Native chart reading results

Run at:

- `latent_dim = 12`

on:

- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_projected_oracle_i7`

Current reading:

- all three current charts can be read back from the native latent with high accuracy;
- however, their geometry aligns differently with the latent itself.

Most important result:

- among the current hand-defined charts, `behavior_8d` is the one whose geometry is most aligned with the native latent;
- `i7` is more compressed but remains the best deploy chart;
- `raw4 relation` is readable from the latent but is the coarsest chart geometrically.

Current interpretation:

- the present `4D / 8D / i7` stack is best understood as a useful chart decomposition rather than a final ontological decomposition;
- `8D behavior` is the most native analytic chart among the current hand-defined views;
- `i7` is the strongest deploy chart;
- `raw4` is a coarse relation chart.


## E50. Paper-line synthesis and draft tightening

Added:

- [PAPER_PAPERLINE_SYNTHESIS.md](d:/My%20Project/companion-ai/PAPER_PAPERLINE_SYNTHESIS.md)

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL.md)

Purpose:

- freeze the paper-facing research line now that the project has effectively converged;
- distinguish the main paper claims from the later, more conservative chart-structure analyses;
- make the writing stance explicit:
  - deploy result;
  - analytic bridge result;
  - ontology/framing result;
  - conservative manifold/native-latent interpretation.

Frozen writing stance:

- the paper is about explicit relational control under a strong baseline, not about recovering the model's true internal ontology;
- the strongest current deploy route is direct `relation -> i7`;
- the strongest current real configuration is `direct sc_vA`;
- `relation -> behavior(8D) -> i7` is retained as an analytic bridge;
- the manifold/native-latent line should be written as chart-role clarification rather than ontology discovery.

## E51. Draft rewrite into cleaner paper-facing V2

Added:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)

Purpose:

- produce a cleaner paper-facing draft that follows the frozen paper line directly;
- avoid the older draft's duplicated late-stage sections and mixed-strength claims;
- make the current paper stance explicit:
  - main deploy result;
  - analytic bridge result;
  - ontology/framing freeze;
  - conservative chart-structure reading.

Current role:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md` should now be treated as the primary draft to continue writing;
- the older draft remains useful as a trace document but no longer as the cleanest paper-facing source.

## E52. V2 draft expanded with related-work and judge framing

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)

Added in the draft:

- a paper-facing `Related Work` section;
- an explicit `Judge Protocol` subsection in experimental design.

Purpose:

- make the draft look more like a submission-ready paper rather than an internal result memo;
- clarify that final claims rest on relational judge and pairwise comparison rather than proxy length summaries;
- locate the work relative to controllable dialogue, long-term dialogue consistency, social-signal modeling, and conservative chart-structure analysis.

## E53. V2 draft upgraded with table and citation placeholders

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)

Added in the draft:

- explicit main-paper table placeholders for:
  - frozen main comparison
  - bridge sanity
  - ontology/framing freeze
- appendix-style table placeholders for the conservative geometric reading
- citation placeholders in `Related Work`

Purpose:

- make the draft easier to convert into a submission without re-deciding the table plan later;
- separate main-result tables from supporting appendix material;
- make literature insertion straightforward.

## E54. Paper assembly support files added

Added:

- [PAPER_TABLE_DRAFTS.md](d:/My%20Project/companion-ai/PAPER_TABLE_DRAFTS.md)
- [PAPER_RELATED_WORK_CITATION_PLAN.md](d:/My%20Project/companion-ai/PAPER_RELATED_WORK_CITATION_PLAN.md)

Purpose:

- create one place for the main-paper tables and appendix-style tables;
- create one place for mapping the remaining citation placeholders to literature buckets;
- reduce friction in converting the draft into a submission package.

## E55. First-pass paper tables filled

Updated:

- [PAPER_TABLE_DRAFTS.md](d:/My%20Project/companion-ai/PAPER_TABLE_DRAFTS.md)

What was filled:

- frozen main comparison global row
- bridge sanity global row
- deploy ontology/framing freeze summary row
- aggregate pairwise summary in first-pass form
- secondary diagnostics summary row
- appendix-style conservative geometry summary row

Important boundary:

- several rows remain deliberately marked as `prelim`, `TBD`, or family-level qualitative placeholders;
- this is a paper-assembly draft, not a final adjudicated results table.

## E56. Draft/table alignment and citation candidates

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)
- [PAPER_RELATED_WORK_CITATION_PLAN.md](d:/My%20Project/companion-ai/PAPER_RELATED_WORK_CITATION_PLAN.md)

Added:

- explicit references in the draft to:
  - `Table 1`
  - `Table 2`
  - `Table 3`
  - `Appendix Table A`
- first-pass concrete citation candidates in the related-work planning file

Purpose:

- keep the prose draft aligned with the table-draft file;
- move the citation plan one step closer to a real bibliography without overcommitting before the final literature pass.

## E57. Submission gaps explicitly documented

Added:

- [PAPER_SUBMISSION_GAPS.md](d:/My%20Project/companion-ai/PAPER_SUBMISSION_GAPS.md)

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)

What was clarified:

- the current experiments do **not** yet fully isolate whether the gain comes from two-layer structure itself versus the strength of the `i7` deploy interface;
- the current judge package is central and meaningful, but not yet described at full submission-standard rigor;
- relational coherence remains only partially operationalized;
- the late geometry/native-latent line is interesting but should remain secondary and conservative.

Current implication:

- the project is sufficiently converged to write as a paper;
- but a stronger submission would still benefit from:
  - a no-relational-state `i7`-style control ablation,
  - more formal judge protocol reporting,
  - and cleaner operationalization language.

## E58. `baseline -> i7` control route implemented

Updated:

- [app/api/chat.py](d:/My%20Project/companion-ai/app/api/chat.py)
- [app/generation/execution_interface.py](d:/My%20Project/companion-ai/app/generation/execution_interface.py)
- [paper_run_experiment.py](d:/My%20Project/companion-ai/paper_run_experiment.py)

Added route:

- `baseline_relational_instruction_to_interface`

Purpose:

- provide the missing no-relational-state `i7`-style control ablation;
- compare:
  - strong baseline with no execution chart,
  - baseline heuristics rendered into `i7`,
  - explicit `relation -> i7`

Current status:

- code path implemented and syntax-checked
- result not yet run at paper-facing scale

## E59. Judge protocol frozen into appendix-ready specification

Added:

- [PAPER_JUDGE_PROTOCOL_APPENDIX.md](d:/My%20Project/companion-ai/PAPER_JUDGE_PROTOCOL_APPENDIX.md)

What it now freezes:

- fixed case-level judge prompt
- fixed pairwise judge prompt
- decoding recommendation (`0.0` or `0.2`)
- recommended sample count (`3`)
- blind-label requirement
- minimum multi-judge setup
- minimum agreement reporting

Purpose:

- move judge discussion from "evaluation philosophy" toward a reproducible appendix protocol
- close one of the most important remaining submission gaps

## E60. Draft reframed around chart decomposition rather than layered ontology

Updated:

- [PAPER_DRAFT_RELATIONAL_CONTROL_V2.md](d:/My%20Project/companion-ai/PAPER_DRAFT_RELATIONAL_CONTROL_V2.md)
- [PAPER_SUBMISSION_GAPS.md](d:/My%20Project/companion-ai/PAPER_SUBMISSION_GAPS.md)
- [PAPER_TABLE_DRAFTS.md](d:/My%20Project/companion-ai/PAPER_TABLE_DRAFTS.md)

What changed:

- the draft now states more explicitly that a richer one-layer manifold may exist in principle;
- the present `raw4 / behavior_8d / i7` stack is defended as a useful chart decomposition,
  not as proof of final ontological layering;
- a dedicated ablation table placeholder was added for:
  - baseline
  - baseline `-> i7`
  - explicit `relation -> i7`

Effect:

- the paper's theoretical claim is now tighter and less vulnerable to the criticism that all multi-layer structure can be absorbed by a richer one-layer manifold.

## E61. Structure-vs-interface `v1` ablation run

Input:

- `paper_cases_oracle_exec_v1.json`

Modes:

- `baseline_relational_instruction`
- `baseline_relational_instruction_to_interface_i7_sc_vA`
- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_projected_oracle_i7`

Observed proxy summary:

- baseline = `98.17`
- baseline `-> i7` = `41.33`
- explicit `relation -> i7` = `16.50`
- oracle `i7` = `25.50`

Interpretation:

- the `i7` deploy interface itself explains a large share of the gain;
- however, explicit relation-chart decomposition still appears to add additional value beyond interface-only `i7`;
- the strongest current causal reading is therefore mixed rather than binary:
  - interface quality matters a lot,
  - but explicit structured control still matters beyond that.

Status:

- proxy package complete
- focused judge still needed before using the stronger wording in the main paper

## E62. Structure-vs-interface focused judge pack added

Added:

- [paper_build_structure_vs_interface_judge_pack.py](d:/My%20Project/companion-ai/paper_build_structure_vs_interface_judge_pack.py)

Purpose:

- generate case-level and pairwise judge inputs for:
  - baseline
  - baseline `-> i7`
  - explicit `relation -> i7`
  - oracle `i7`

Intended comparisons:

- baseline vs baseline `-> i7`
- baseline `-> i7` vs explicit `relation -> i7`
- baseline vs explicit `relation -> i7`
- explicit `relation -> i7` vs oracle `i7`

## E63. Structure-vs-interface focused judge supports mixed attribution

Read cases:

- `oracle_exec_warm_001`
- `oracle_exec_vuln_001`
- `oracle_exec_cool_001`

Main reading:

- `baseline -> i7` consistently improves over the strong baseline;
- `explicit relation -> i7` usually improves further over `baseline -> i7`;
- the advantage is strongest in `warm` and `cool`, and smaller but still visible in `vulnerability`;
- `explicit relation -> i7` is already close to `oracle_i7`, with many reads landing in tie / small oracle-edge territory.

Paper-facing interpretation:

- the gain is mixed rather than single-cause;
- executable interface quality explains a large share of the improvement;
- explicit relation-chart decomposition still adds trajectory-level stabilization beyond interface-only control.

Quantified judge summary:

- `baseline -> i7` vs baseline: `9/9` pairwise wins for `baseline -> i7`
- explicit `relation -> i7` vs baseline: `8/9` pairwise wins for explicit `relation -> i7`
- explicit `relation -> i7` vs `baseline -> i7`: `6/9` pairwise wins for explicit `relation -> i7`
- explicit `relation -> i7` vs `oracle_i7`: near tie (`5/9` wins for real route, `4/9` for oracle)
- pairwise winner agreement: `0.7778`

Current reading:

- the `i7` interface itself explains a large share of the gain;
- explicit relation-chart decomposition still contributes a moderate but real additional advantage;
- the current real route is already close to oracle in this focused ablation.

## E64. Judge protocol hardened and agreement script added

Added:

- [PAPER_JUDGE_PROTOCOL_APPENDIX.md](d:/My%20Project/companion-ai/PAPER_JUDGE_PROTOCOL_APPENDIX.md)
- [paper_judge_agreement.py](d:/My%20Project/companion-ai/paper_judge_agreement.py)

What this adds:

- fixed judge prompt wording
- fixed decoding recommendation (`0.0` or `0.2`)
- recommended sample count (`3`)
- explicit blind-label requirement
- minimum multi-judge setup
- raw-agreement computation path

Purpose:

- address the criticism that evaluation is too subjective or not reproducible enough

## E65. Semi-formal coherence operationalization added

Added:

- [PAPER_RELATIONAL_COHERENCE_OPERATIONALIZATION.md](d:/My%20Project/companion-ai/PAPER_RELATIONAL_COHERENCE_OPERATIONALIZATION.md)
- [paper_relational_proxy_metrics.py](d:/My%20Project/companion-ai/paper_relational_proxy_metrics.py)

What this adds:

- semi-formal diagnostic components:
  - `Δ warmth per turn`
  - `unexpected polarity flip`
  - `unsupported initiative jump`
  - `response length spike`
- a lightweight automatic proxy layer for:
  - abrupt-shift-like behavior
  - expansion spikes
  - local trajectory instability

Boundary:

- these remain secondary diagnostics
- they do not replace the paper's judge-centered endpoint

## E66. Role clarification: `4D relation` vs `i7`

Paper-facing clarification added:

- `4D relation` is not the main deploy interface.
- Its role is to function as a coarse relation-state chart that records change over the interaction trajectory.
- `i7` is not the long-horizon state chart.
- Its role is to function as the deploy chart that converts the current relation state into a stable executable generation interface.

Consequence for the paper:

- `4D relation` and `i7` should not be described as competing alternatives;
- they perform different jobs inside the current decomposed controller;
- this strengthens the practical chart-decomposition reading of the paper.

## E66b. Interface-family ablation supplement (`i6 / i7 / i8`)

Purpose:

- strengthen the paper's response to the "manually designed `i7`" criticism;
- separate three narrower questions:
  - does an over-merged deploy chart degrade coherence?
  - does adding one more field automatically help?
  - is `i7` at least the strongest current tested deploy chart, even if not proven minimal?

Recommended source run:

- `paper_results_exec_oracle_family_v2.jsonl`

Focused supplement pack:

- `baseline_relational_instruction`
- `explicit_rel_state_projected_oracle_i6`
- `explicit_rel_state_projected_oracle_i7`
- `explicit_rel_state_projected_oracle_i8`

Focused pairwise comparisons:

- baseline vs `oracle_i6`
- baseline vs `oracle_i7`
- baseline vs `oracle_i8`
- `oracle_i6` vs `oracle_i7`
- `oracle_i7` vs `oracle_i8`

Interpretation target:

- `i6` = merged-family comparison
- `i8` = add-one-field comparison
- `i7` = best-tested deploy-chart candidate

Boundary:

- even if this supplement succeeds, it still supports only a best-tested-family claim;
- it does not by itself prove that the current seven-field `i7` decomposition is minimal or necessary.

## E67. Frozen-final multi-judge result hardened

Inputs:

- `paper_eval_frozen_final_judge_v1_out/final_main_case_level_judge_inputs.json`
- `paper_eval_frozen_final_judge_v1_out/final_main_pairwise_judge_inputs.json`
- `paper_judge_runs_v2/frozen_final/judge_agreement_report.json`

Main quantified result:

- direct `relation -> i7` vs strong baseline: `15/15` pairwise wins for direct `relation -> i7`
- `oracle_i7` vs strong baseline: `15/15` pairwise wins for `oracle_i7`
- `oracle_i7` vs direct `relation -> i7`: `13/15` pairwise wins for oracle, `2/15` for the real route
- pairwise winner agreement: `0.9111`

Paper-facing interpretation:

- the frozen deploy result is now strong enough to serve as the paper's main judge-backed empirical claim;
- direct `relation -> i7` clearly and consistently beats the strong baseline;
- `oracle_i7` remains a modest but consistent upper bound over the best current real route;

## E68. Semi-natural generalization set draft v1

Draft file:

- `paper_cases_semi_natural_v1.json`

Current status:

- first-pass semi-natural cases drafted in the same `phases` schema as the oracle execution sets;
- intended for lighter-weight generalization testing rather than oracle-heavy mechanism analysis;
- no oracle annotations are included in this draft, so it is naturally suited to:
  - `baseline_relational_instruction`
  - `baseline_relational_instruction_to_interface_i7_sc_vA`
  - `explicit_rel_state_rel_to_interface_i7_sc_vA`

Coverage in v1:

- `warming_trajectory`: 2 cases
- `vulnerability_with_correction`: 2 cases
- `cooling_trajectory`: 2 cases
- `mixed_signal_trajectory`: 2 cases
- `ordinary_neutral`: 2 cases
- `boundary_repair`: 2 cases

Recommended next step:

- human screening / light editing first;
- then run the final deploy-comparison subset on this semi-natural set before adding external/lightly adapted cases.

## E69. Semi-natural generalization set draft v2 (distribution-shifted)

Draft file:

- `paper_cases_semi_natural_v2.json`

Why v2 exists:

- `v1` remained too close to the original hand-crafted oracle template;
- `v2` is intentionally more distribution-shifted:
  - signal positions are less fixed,
  - topic domains are broader,
  - user corrections are less templatic,
  - and the trajectories should feel less like direct paraphrases of the oracle core.

Current coverage in v2:

- `warming_trajectory`: 2 cases
- `vulnerability_with_correction`: 2 cases
- `cooling_trajectory`: 2 cases
- `mixed_signal_trajectory`: 2 cases
- `ordinary_neutral`: 2 cases
- `boundary_repair`: 2 cases

Intended use:

- prefer `v2` over `v1` for paper-facing semi-natural generalization tests;
- keep the same lightweight mode subset:
  - `baseline_relational_instruction`
  - `baseline_relational_instruction_to_interface_i7_sc_vA`
  - `explicit_rel_state_rel_to_interface_i7_sc_vA`

Recommended next step:

- human screening / pruning first;
- then expand from `12` to `24+` if the style looks acceptable.
- the remaining gap should be described as small and stable, not as evidence that the real route fails.
