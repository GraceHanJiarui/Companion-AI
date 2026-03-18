# Final Frozen Judge Results

## Scope

This note records a manual reading of the frozen final judge packs:

- `final_main_case_level_judge_inputs.json`
- `final_main_pairwise_judge_inputs.json`
- `final_bridge_case_level_judge_inputs.json`
- `final_bridge_pairwise_judge_inputs.json`

The reading criterion is relational coherence across the full multi-turn trajectory, with special attention to:

- whether the assistant keeps the same relationship trajectory across turns
- whether `E_ordinary_continuation` and `F_final_probe` remain controlled
- whether there are abrupt shifts, compensatory warmth, or renewed relational escalation

## A. Main Frozen Comparison

Compared modes:

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7`
- `explicit_rel_state_projected_oracle_i7`

### Pairwise reading

#### `direct i7` vs `baseline`

- `warm`: `direct i7` wins
- `vulnerability`: `direct i7` wins
- `cooling`: `direct i7` wins
- `mixed_001`: `direct i7` wins
- `mixed_002`: `direct i7` wins

Summary:

- `direct i7` is consistently more controlled and trajectory-faithful.
- The baseline repeatedly over-explains, over-offers, or reopens interaction in later turns.
- The biggest baseline weakness remains continuation and final-probe inflation.

#### `oracle i7` vs `baseline`

- `warm`: `oracle i7` wins
- `vulnerability`: `oracle i7` wins
- `cooling`: `oracle i7` wins
- `mixed_001`: `oracle i7` wins
- `mixed_002`: `oracle i7` wins

Summary:

- The oracle controller is also consistently more coherent than the baseline.
- This keeps the core paper claim intact: strong baseline is competitive, but the frozen controller line is better aligned with long-horizon relational continuity.

#### `oracle i7` vs `direct i7`

- `warm`: `tie` with slight oracle edge
- `vulnerability`: `oracle i7` slight win
- `cooling`: `tie`
- `mixed_001`: `oracle i7` slight win
- `mixed_002`: `tie`

Summary:

- `direct i7` is not collapsing relative to oracle.
- The oracle route remains slightly cleaner on a few delicate cases, especially where response wording needs to stay warm without reopening the interaction too much.
- However, the gap is now small enough that `relation -> i7` is a defendable frozen deploy route.

### Main-case reading

#### `baseline_relational_instruction`

- Typical coherence level: `2-3/5`
- Main issue: over-expansion and re-initiating behavior after the user has already specified a restrained interaction mode
- Abrupt-shift risk: visible in `warm`, `vulnerability`, and both `mixed` cases

#### `explicit_rel_state_rel_to_interface_i7`

- Typical coherence level: `4-5/5`
- Main strength: stable, concise, and phase-consistent control
- Abrupt-shift risk: low; mostly minor stylistic flatness rather than relational instability

#### `explicit_rel_state_projected_oracle_i7`

- Typical coherence level: `4-5/5`
- Main strength: similar stability to direct `i7`, sometimes with slightly better phrasing in delicate turns
- Abrupt-shift risk: very low

### Main frozen conclusion

The main frozen comparison supports the following final reading:

- `relation -> i7` direct should be frozen as the paper's main deployable controller.
- It clearly outperforms the strong baseline in relational coherence.
- It is close to the oracle route, with only small residual gaps on a subset of warm/vulnerability/mixed cases.

## B. Bridge Sanity

Compared modes:

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

### Pairwise reading

#### `oracle_state bridge` vs `oracle_behavior`

- `warm`: `tie`
- `vulnerability`: `tie`
- `cooling`: `tie`
- `mixed_001`: `tie`
- `mixed_002`: `tie`

Summary:

- The corrected fitted bridge is now very close to the oracle-behavior route.
- Differences are mostly stylistic or in response packaging, not in gross relational trajectory.

#### `oracle_state bridge` vs `oracle`

- `warm`: `tie`
- `vulnerability`: `oracle i7` slight win
- `cooling`: `tie`
- `mixed_001`: `tie`
- `mixed_002`: `tie`

Summary:

- The analytic bridge remains close to full oracle on most cases.
- The main residual weakness appears in vulnerability handling, where the bridge can still be slightly more explanatory or slightly less crisp than the oracle route.

#### `oracle_behavior` vs `oracle`

- `warm`: `tie`
- `vulnerability`: `oracle i7` slight win
- `cooling`: `tie`
- `mixed_001`: `tie`
- `mixed_002`: `tie`

Summary:

- Even oracle behavior does not uniformly dominate oracle full route in manual reading.
- This further supports the claim that the bridge is no longer the obviously broken part of the pipeline.

### Bridge-case reading

#### `oracle_state_i7_pfitpoly2`

- Typical coherence level: `4-5/5`
- Main strength: preserves the same relational trajectory while staying close to oracle behavior/oracle route
- Main residual issue: small remaining sensitivity in vulnerability-style supportive turns

#### `oracle_behavior_i7`

- Typical coherence level: `4-5/5`
- Main strength: highly stable and restrained
- Main residual issue: sometimes slightly generic or mechanically formatted

#### `oracle_i7`

- Typical coherence level: `4-5/5`
- Main strength: generally the cleanest upper-reference phrasing
- Main residual issue: only small case-specific advantages over the other two oracle-side routes

### Bridge sanity conclusion

The bridge sanity comparison supports the following final reading:

- `relation -> fitted 8D behavior -> i7` with `fitpoly2` remains a valid analytic bridge.
- It should not be discarded as a failed intermediate layer.
- Its current role is better framed as an analytic and explanatory bridge than as the paper's main deploy controller.

## Paper-ready takeaways

1. `relation -> i7` direct is the best frozen deployable controller in the current study.
2. The frozen controller line is clearly better than the strong baseline in relational coherence and continuity.
3. The corrected `4D relation -> fitted 8D behavior -> i7` bridge remains close to oracle-side behavior and oracle full route.
4. Therefore, the current paper can cleanly separate:
   - a deploy route: `relation -> i7`
   - an analytic bridge: `relation -> behavior(8D) -> i7`
5. This supports a stronger overall framing: the analytic layer and deploy layer are distinct objects, but they can be bridged well enough to support both explanation and deployment within one control framework.
