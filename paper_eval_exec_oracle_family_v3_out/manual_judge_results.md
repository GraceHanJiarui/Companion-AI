# Manual Judge Results: Stage 2 Focused Oracle Interface Comparison

Source files:
- `paper_eval_exec_oracle_family_v3_out/stage2_focused_case_level_judge_inputs.json`
- `paper_eval_exec_oracle_family_v3_out/stage2_focused_pairwise_judge_inputs.json`

Judging focus:
- relational coherence across the whole case
- abrupt relational shift
- especially whether `E_ordinary_continuation` and `F_final_probe` remain on the same trajectory

## Pairwise Judgments

### Case: `oracle_exec_warm_001`

- `explicit_rel_state_projected_oracle_i6` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i6` stays on a lighter and more continuous warming trajectory. The baseline keeps re-expanding into a heavier, more helpful style, especially in `E` and `F`, which makes the interaction feel more managed than gradually sustained.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i7` remains warm but restrained. The baseline is still coherent overall, but it drifts toward extra reassurance and continuation pressure, so `i7` feels more like a steady same-relationship process.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_oracle_i6`
  - winner: `tie`
  - reason: both are coherent and both control the later phases much better than the baseline. `i6` is slightly cleaner, while `i7` has slightly better relational texture; neither clearly dominates.

### Case: `oracle_exec_vuln_001`

- `explicit_rel_state_projected_oracle_i6` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i6` is more restrained and less likely to slide back into advice-heavy or meta-heavy support. The baseline remains understandable but still carries more explanatory and supportive weight than the user trajectory seems to support.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i7` keeps a gentle but lower-pressure presence. Compared with the baseline, it avoids heavier supportive framing and feels more aligned with the user's preference for a lighter, less managed interaction.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_oracle_i6`
  - winner: `left`
  - reason: `i7` keeps the same restraint as `i6` while sounding a bit less rigid and less system-like in the middle turns. It preserves continuity without flattening the interaction too much.

### Case: `oracle_exec_cool_001`

- `explicit_rel_state_projected_oracle_i6` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i6` respects the cooling trajectory more faithfully. The baseline repeatedly reintroduces extra framing, optionality, and future-oriented talk, which weakens the user's requested low-pressure distance.

- `explicit_rel_state_projected_oracle_i7` vs `baseline_relational_instruction`
  - winner: `left`
  - reason: `i7` is the most natural in the cooling setting. It remains brief, low-pressure, and non-compensatory, while the baseline continues to feel too elaborative and too eager to manage the interaction.

- `explicit_rel_state_projected_oracle_i7` vs `explicit_rel_state_projected_oracle_i6`
  - winner: `left`
  - reason: both are coherent, but `i7` feels slightly more natural and less menu-like. `i6` stays controlled, yet its wording is more rigid and instrument-like.

## Interim Interpretation

- Both `i6` and `i7` outperform `baseline_relational_instruction` on these oracle cases in case-level relational coherence.
- `i7` currently looks like the stronger Stage 2 oracle interface:
  - warm: `tie` with `i6`
  - vulnerability: `i7` better
  - cooling: `i7` better
- `i6` remains valuable as a stronger-clamp, lower-variance interface, especially for highly sensitive trajectories.
- The current evidence supports:
  - `projected oracle interface > strong baseline`
  - and within projected oracle interfaces, `i7` is the best current candidate.
