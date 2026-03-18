# Final Judge Plan

## Why length is not enough

Average response length was useful during exploration because many bad failures showed up as:

- continuation inflation
- over-explanation
- compensatory warmth
- unnecessary follow-up

But length alone cannot establish the paper's main claim. A shorter reply can still be:

- too cold
- too generic
- discontinuous with prior turns

And a slightly longer reply can still be:

- coherent
- well-calibrated
- relationally stable

Therefore, final paper claims should rely on judge-based relational evaluation, using length only as a secondary diagnostic statistic.

## Final judge goals

The final judge should evaluate whether a dialogue trajectory:

1. stays on one coherent relationship process
2. avoids abrupt relational shifts
3. keeps continuation and final-probe turns under control
4. preserves the user's requested interaction mode

## Final judge package

### Package A. Main frozen comparison

Modes:

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7`
- `explicit_rel_state_projected_oracle_i7`

Purpose:

- establish the main deployable result
- show whether the frozen real controller beats the strong baseline
- measure the remaining gap to oracle deploy route

### Package B. Bridge sanity

Modes:

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

Purpose:

- test whether the corrected analytic bridge remains close to oracle-side behavior
- justify keeping the 8D layer in the paper as an analytic bridge

## Final judge rubric

### A. Case-level coherence judge

For each full multi-turn case, score:

1. `relational_coherence_score_1_to_5`
2. `has_abrupt_shift`
3. `abrupt_shift_turns`
4. `reason`

Scoring rubric:

- `5`: highly coherent, same relational process throughout, no obvious shift
- `4`: coherent overall, minor roughness but no meaningful trajectory break
- `3`: acceptable but with one or two noticeable instabilities
- `2`: clearly unstable, at least one obvious relational shift or compensatory move
- `1`: badly fragmented, does not feel like one ongoing relationship trajectory

Judge emphasis:

- continuity across turns
- especially `B/C/D/F` transitions
- whether `E_ordinary_continuation` and `F_final_probe` reopen or re-escalate the interaction

### Coherence-first structured rubric

For final manual judging, prefer this structured reading order over length:

1. `trajectory_continuity_1_to_5`
2. `user-request-preservation_1_to_5`
3. `overinterpretation_1_to_5`
4. `continuation_probe_control_1_to_5`
5. `notes`

Interpretation:

- `trajectory_continuity`
  - does the dialogue still feel like one ongoing interactional process
- `user-request-preservation`
  - does the reply stay inside the interaction mode the user is implicitly or explicitly asking for
- `overinterpretation`
  - does the system over-read weak signals into warmth, curiosity, support, or relationship movement
- `continuation_probe_control`
  - do `E_ordinary_continuation` and `F_final_probe` remain controlled instead of reopening or escalating

These sub-scores should support the main coherence judgement, not replace it.

### B. Pairwise preference judge

For each case, compare two modes and return:

1. `winner = left | right | tie`
2. `reason`

Preference rule:

- prefer the trajectory that better preserves the same relationship process
- do not reward verbosity or generic helpfulness
- prioritize less abrupt shift, less overinterpretation, less compensatory warmth, and cleaner continuation/probe behavior

### C. Optional structured sub-scores

If a stronger final appendix table is needed, add four binary or 1-3 sub-scores:

1. `continuation_control`
2. `final_probe_control`
3. `distance_respect`
4. `warmth_calibration`

These should stay secondary to the main coherence score, not replace it.

## Result table structure

### Table 1. Main frozen comparison

Columns:

- `Case family`
- `Baseline coherence`
- `Direct relation->i7 coherence`
- `Oracle i7 coherence`
- `Direct vs Baseline pairwise`
- `Oracle vs Baseline pairwise`
- `Oracle vs Direct pairwise`
- `Notes`

Recommended case rows:

- `warm`
- `vulnerability`
- `cooling`
- `mixed_001`
- `mixed_002`

### Table 2. Bridge sanity

Columns:

- `Case family`
- `Oracle-state bridge coherence`
- `Oracle-behavior coherence`
- `Oracle full coherence`
- `State vs Behavior pairwise`
- `State vs Oracle pairwise`
- `Behavior vs Oracle pairwise`
- `Notes`

### Table 3. Aggregate pairwise summary

For each pairwise comparison, report:

- `wins`
- `ties`
- `losses`

Recommended rows:

- `Direct i7 vs Baseline`
- `Oracle i7 vs Baseline`
- `Oracle i7 vs Direct i7`
- `Oracle-state bridge vs Oracle-behavior`
- `Oracle-state bridge vs Oracle full`
- `Oracle-behavior vs Oracle full`

### Table 4. Secondary diagnostics

Keep this as a secondary table or appendix:

- mean reply length
- repeated sampling range / variance
- selected abrupt-shift examples

This table supports interpretation but should not carry the main claim.

## Final writing rule

In the paper text:

- lead with case-level coherence and pairwise judge
- use aggregate win/tie/loss summaries to support the main argument
- use length only as supporting evidence for over-expansion, never as the primary endpoint
