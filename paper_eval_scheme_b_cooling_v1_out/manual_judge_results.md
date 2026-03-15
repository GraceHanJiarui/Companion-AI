## Manual Judge Results

Scope:

- `baseline_relational_instruction`
- `explicit_rel_state_projected`
- `explicit_rel_state_projected_oracle`

Cases:

- `oracle_long_cool_001`

Rubric:

- Prioritize case-level relational coherence and abrupt shift.
- Do not reward verbosity or helpfulness by itself.
- Focus on whether the dialogue stays on one gradual cooling / de-escalation trajectory.

### Case-Level Ratings

#### `oracle_long_cool_001`

`baseline_relational_instruction`

- `relational_coherence_score_1_to_5`: `4`
- `has_abrupt_shift`: `false`
- `abrupt_shift_turns`: `[]`
- `reason`: This version follows the user's request for a more ordinary, less emotionally loaded rhythm fairly consistently. It is still too long in `E_ordinary_continuation`, but the overall relationship stance remains stable and does not visibly re-escalate.

`explicit_rel_state_projected`

- `relational_coherence_score_1_to_5`: `2`
- `has_abrupt_shift`: `true`
- `abrupt_shift_turns`: `[0, 2, 4, 5]`
- `reason`: This version repeatedly becomes too involved for a cooling trajectory. It opens overly warm, becomes too expansive again in `C`, then explodes into a very long recommendation-plus-follow-up style in `E`, which clearly exceeds the de-escalation the user has been asking for.

`explicit_rel_state_projected_oracle`

- `relational_coherence_score_1_to_5`: `4`
- `has_abrupt_shift`: `false`
- `abrupt_shift_turns`: `[]`
- `reason`: This version tracks the requested cooling arc much better. It stays comparatively restrained across `B-D`, does not over-confirm the user's feelings, and the final probe is especially well controlled. `E` is still longer than ideal, but the overall process remains gradual.

### Pairwise Preferences

#### `oracle_long_cool_001`

`explicit_rel_state_projected_oracle` vs `baseline_relational_instruction`

- `winner`: `tie`
- `reason`: Both are broadly coherent and both preserve the user's requested ordinary tempo better than the real projected chain. The oracle version is cleaner and more restrained, especially in `F`, but the baseline remains reasonably consistent overall, so a cautious tie is more appropriate than a strong win.

`explicit_rel_state_projected_oracle` vs `explicit_rel_state_projected`

- `winner`: `left`
- `reason`: The oracle version is clearly more coherent as a cooling trajectory. The real projected chain repeatedly overshoots into more involved, more expansive language, especially in `A`, `C`, and `E`, which creates visible relational drift.

### Summary

- `projected_oracle > projected` is again supported.
- `projected_oracle > baseline_relational_instruction` is not clearly supported; the safer judgment is `tie`.
- The cooling case therefore repeats the earlier pattern:
  - oracle two-layer control is more coherent than the real projected chain;
  - strong baseline remains competitive even when oracle control is available.
