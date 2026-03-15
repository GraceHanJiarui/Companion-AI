## Manual Judge Results

Scope:

- `baseline_relational_instruction`
- `explicit_rel_state_projected`
- `explicit_rel_state_projected_oracle`

Cases:

- `oracle_long_warm_001`
- `oracle_long_vuln_001`

Rubric:

- Prioritize case-level relational coherence and abrupt shift.
- Do not treat verbosity or helpfulness alone as the target.
- Focus on whether the dialogue feels like one continuous relational process.

### Case-Level Ratings

#### `oracle_long_warm_001`

`baseline_relational_instruction`

- `relational_coherence_score_1_to_5`: `4`
- `has_abrupt_shift`: `false`
- `abrupt_shift_turns`: `[]`
- `reason`: Overall the dialogue stays on one stable, mildly warm trajectory. It is verbose and sometimes over-elaborate, especially in `E_ordinary_continuation`, but the relationship stance does not visibly jerk from one phase to another.

`explicit_rel_state_projected`

- `relational_coherence_score_1_to_5`: `3`
- `has_abrupt_shift`: `true`
- `abrupt_shift_turns`: `[3, 4, 5]`
- `reason`: The dialogue starts plausibly, but from `D_counter_signal_or_refinement` onward it becomes too explanatory and too controlling. In `E` and `F` it drifts into option-heavy, over-involved language that feels more active than the prior trajectory supports.

`explicit_rel_state_projected_oracle`

- `relational_coherence_score_1_to_5`: `4`
- `has_abrupt_shift`: `false`
- `abrupt_shift_turns`: `[]`
- `reason`: The dialogue stays notably more restrained and gradual. It tracks the user's requested lighter tempo well, and although `E_ordinary_continuation` still expands, the overall relation process remains coherent.

#### `oracle_long_vuln_001`

`baseline_relational_instruction`

- `relational_coherence_score_1_to_5`: `3`
- `has_abrupt_shift`: `true`
- `abrupt_shift_turns`: `[4]`
- `reason`: The early phases are reasonably aligned with the user's request for quiet presence, but `E_ordinary_continuation` jumps back into a long intervention list. That shift feels more active and therapeutic than the preceding trajectory supports.

`explicit_rel_state_projected`

- `relational_coherence_score_1_to_5`: `2`
- `has_abrupt_shift`: `true`
- `abrupt_shift_turns`: `[0, 3, 4, 5]`
- `reason`: This version is the least coherent. It opens too heavy, keeps slipping into over-guidance, and repeatedly re-expands after the user has asked for a simpler, less counseling-like style.

`explicit_rel_state_projected_oracle`

- `relational_coherence_score_1_to_5`: `4`
- `has_abrupt_shift`: `false`
- `abrupt_shift_turns`: `[]`
- `reason`: This version best preserves a calm, low-pressure companionship style. It remains sparse and restrained through `A-D`, and although `E` becomes somewhat instructional, the overall trajectory is still much more continuous than the alternatives.

### Pairwise Preferences

#### `oracle_long_warm_001`

`explicit_rel_state_projected_oracle` vs `baseline_relational_instruction`

- `winner`: `tie`
- `reason`: Both dialogues are broadly coherent and follow one warm-but-gradual trajectory. The oracle version is cleaner and more restrained, but the baseline remains reasonably continuous despite being verbose, so there is not enough evidence here for a strong preference.

`explicit_rel_state_projected_oracle` vs `explicit_rel_state_projected`

- `winner`: `left`
- `reason`: The oracle version stays more gradual and avoids the later over-involved drift visible in the real projected chain. The non-oracle projected version becomes too heavy from `D` onward and feels less like one stable relational process.

#### `oracle_long_vuln_001`

`explicit_rel_state_projected_oracle` vs `baseline_relational_instruction`

- `winner`: `left`
- `reason`: The oracle version better maintains the user's requested low-pressure, non-therapeutic tone. The baseline holds up early, but `E_ordinary_continuation` reintroduces a stronger intervention style and weakens continuity.

`explicit_rel_state_projected_oracle` vs `explicit_rel_state_projected`

- `winner`: `left`
- `reason`: The oracle version is substantially more coherent across the whole case. The real projected version repeatedly shifts into over-guidance and over-explanation, which creates visible relational drift.

### Summary

- `projected_oracle > projected` is supported in both cases.
- `projected_oracle > baseline_relational_instruction` is supported in the vulnerability case, but only `tie` in the warming case.
- Current manual judgment therefore supports this cautious conclusion:
  - oracle two-layer control shows real potential;
  - real projected control does not yet reliably realize that potential;
  - strong baseline remains competitive, especially in non-vulnerability trajectories.
