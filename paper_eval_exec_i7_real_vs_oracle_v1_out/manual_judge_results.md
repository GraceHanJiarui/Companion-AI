# Manual Judge Results: Real i7 vs Oracle i7 vs Strong Baseline

Source files:
- `paper_eval_exec_i7_real_vs_oracle_v1_out/stage2_focused_case_level_judge_inputs.json`
- `paper_eval_exec_i7_real_vs_oracle_v1_out/stage2_focused_pairwise_judge_inputs.json`

Judging focus:
- case-level relational coherence
- abrupt shift
- especially whether `E_ordinary_continuation` and `F_final_probe` stay on the same trajectory

## Pairwise Judgments

### Case: `oracle_exec_warm_001`

- `explicit_rel_state_projected_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `real i7` still carries some extra suggestion structure, but it is much more restrained than the baseline and better preserves the user's requested light, gradual warming trajectory. The baseline remains coherent, yet it repeatedly expands into a heavier supportive style.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `oracle i7` is clearly more continuous and less compensatory. It keeps the warming trajectory gentle and avoids the baseline's tendency to over-elaborate in the later turns.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_i7`
  - winner: `left`
  - reason: both are coherent, but `oracle i7` is cleaner and lower-pressure. `real i7` still shows more explanation and option-giving than the trajectory really needs.

### Case: `oracle_exec_vuln_001`

- `explicit_rel_state_projected_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `real i7` stays much closer to the user's request for presence without over-comforting. The baseline repeatedly drifts back toward guided soothing and therapeutic framing, which weakens coherence.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `oracle i7` is the clearest fit for the vulnerability trajectory. It remains present, brief, and low-pressure, while the baseline keeps adding explanatory support and extra management.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_i7`
  - winner: `left`
  - reason: `real i7` is already much better than the baseline here, but `oracle i7` is still more consistent and less meta. The oracle version avoids the remaining friction of explicit self-positioning and over-structured response moves.

### Case: `oracle_exec_cool_001`

- `explicit_rel_state_projected_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `real i7` respects the cooling trajectory more faithfully. The baseline keeps reintroducing optionality, conversational management, and future-facing reassurance that soften the user's intended distance.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `oracle i7` is decisively more aligned with the requested low-pressure distance. It stays brief and non-compensatory, while the baseline remains too elaborative and too eager to maintain a managed rapport.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_i7`
  - winner: `left`
  - reason: `real i7` is already substantially improved over the baseline, but `oracle i7` is still cleaner and more exact in preserving the cooling stance. The difference is most visible in the later turns, where `real i7` still explains more than necessary.

## Interim Interpretation

- `explicit_rel_state_projected_i7` now shows a strong signal of outperforming `baseline_relational_instruction` across warm, vulnerability, and cooling oracle-trajectory cases.
- `explicit_rel_state_projected_oracle_i7` remains stronger than `explicit_rel_state_projected_i7` on all three cases.
- This suggests:
  - the `i7` two-layer interface survives contact with the real chain better than earlier projected variants,
  - but a meaningful realization gap still remains between real-chain execution and oracle execution.

## Current Stage-2 Takeaway

- `oracle i7 > real i7 > strong baseline`

This is the clearest Stage-2 result so far:
- the two-layer `i7` interface appears to be a real improvement over the strong baseline,
- and further gains are still plausibly available if the real chain can move closer to the oracle condition.
