# Manual Judge Results: Stage 2 Focused Oracle Interface Comparison

Input files:

- [stage2_focused_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v2_out/stage2_focused_case_level_judge_inputs.json)
- [stage2_focused_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_exec_oracle_family_v2_out/stage2_focused_pairwise_judge_inputs.json)

Important note:

- This run does **not** include `baseline_relational_instruction`.
- Therefore the current manual judgment can only assess:
  - `explicit_rel_state_projected_oracle_i6`
  - `explicit_rel_state_projected_oracle_i7`
- It cannot yet answer:
  - `i6` vs strong baseline
  - `i7` vs strong baseline

## Case-Level Judgments

### `oracle_exec_warm_001`

#### `explicit_rel_state_projected_oracle_i6`

- `relational_coherence_score_1_to_5 = 4`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  The trajectory is mostly coherent and keeps a warm-but-controlled progression. The main weakness is `E_ordinary_continuation`, where the answer expands into a fairly structured advice block and feels somewhat more “helpful-mode” than the earlier lightweight relational rhythm.

#### `explicit_rel_state_projected_oracle_i7`

- `relational_coherence_score_1_to_5 = 4`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  The progression is also coherent. It stays slightly more relationship-aware than `i6`, but `E_ordinary_continuation` still expands too much and becomes list-like. This weakens natural continuity, though not enough to count as a sharp relational shift.

#### Pairwise: `i7` vs `i6`

- `winner = tie`
- Reason:
  Both remain within the same relational trajectory and both are weakened by `E_ordinary_continuation`. `i6` is a bit cleaner, while `i7` is a bit more relationally responsive, but neither has a clear coherence advantage.

### `oracle_exec_vuln_001`

#### `explicit_rel_state_projected_oracle_i6`

- `relational_coherence_score_1_to_5 = 4`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  This version is controlled and stable across the vulnerability trajectory. It stays brief, does not over-analyze, and does not suddenly over-warm. The main weakness is a somewhat rigid, system-like tone in `E`.

#### `explicit_rel_state_projected_oracle_i7`

- `relational_coherence_score_1_to_5 = 3`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  It is still broadly coherent, but the wording becomes more meta and slightly less natural in the middle phases. In `E`, the “I am a dialogue system” phrasing weakens immersion and makes the continuation feel less humanly continuous even though it is not an abrupt relational jump.

#### Pairwise: `i7` vs `i6`

- `winner = right`
- Reason:
  `i6` is more stable and less meta in this vulnerability case. `i7` does not collapse, but its phrasing in later turns becomes more mechanical, which weakens the feeling of one smooth ongoing relational process.

### `oracle_exec_cool_001`

#### `explicit_rel_state_projected_oracle_i6`

- `relational_coherence_score_1_to_5 = 3`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  It respects distancing and stays controlled, but `E_ordinary_continuation` reverts to a menu-like option structure, which feels more assistant-like than relationship-consistent. The case stays coherent enough, but the continuation style is not ideal.

#### `explicit_rel_state_projected_oracle_i7`

- `relational_coherence_score_1_to_5 = 4`
- `has_abrupt_shift = false`
- `abrupt_shift_turns = []`
- Reason:
  This version keeps the cooling trajectory intact while sounding a bit more natural and less menu-driven than `i6`. The stance stays controlled through `F_final_probe` without re-escalating the relationship.

#### Pairwise: `i7` vs `i6`

- `winner = left`
- Reason:
  `i7` handles the cooling case more naturally. `i6` stays controlled but becomes too optionized in `E`, while `i7` preserves the same low-pressure distance with less structure leakage.

## Interim Summary

Across the three oracle cases:

- `oracle_exec_warm_001`: `i7` vs `i6` -> `tie`
- `oracle_exec_vuln_001`: `i6` better
- `oracle_exec_cool_001`: `i7` better

Current interpretation:

- Neither `i6` nor `i7` clearly dominates across all oracle cases.
- `i6` currently looks better for vulnerability-style support where stricter control and brevity are useful.
- `i7` currently looks better for cooling-style and slightly more nuanced relational trajectories.
- Warm trajectories remain unresolved: both still degrade in `E_ordinary_continuation`.

## What This Does and Does Not Establish

Supported:

- `i6` and `i7` are both plausible Stage 2 candidate interfaces.
- The choice between them likely depends on scenario type, not just on raw dimensionality.
- `E_ordinary_continuation` remains the main stress point even after change B/C.

Not established:

- No conclusion yet about `i6` or `i7` versus `baseline_relational_instruction`.
- No conclusion yet about which interface should become the single final Stage 2 winner.

## Immediate Next Step

Run the same Stage 2 focused comparison with:

- `baseline_relational_instruction`
- `explicit_rel_state_projected_oracle_i6`
- `explicit_rel_state_projected_oracle_i7`

so the focused judge export can answer the actual Stage 2 external comparison question.
