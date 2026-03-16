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
