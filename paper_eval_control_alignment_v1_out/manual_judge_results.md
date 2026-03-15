# Manual Judge Results: Control Alignment v1

## Scope

Comparison type:
- `oracle_two_layer_vs_collapsed_single_layer`

Compared modes:
- `explicit_rel_state_projected_oracle`
- `baseline_relational_instruction_oracle_collapsed`

Judging focus:
- case-level relational coherence
- abrupt relational shift
- whether the dialogue feels like one continuous relationship process

## oracle_long_warm_001

Decision:
- winner: `left`
- left = `explicit_rel_state_projected_oracle`
- right = `baseline_relational_instruction_oracle_collapsed`

Reason:
`projected_oracle` more consistently maintains a light, gradual, low-pressure interaction style across phases A-F. The collapsed single-layer version repeatedly expands into more enthusiastic and more interventionist turns, especially in phases D and E, which makes the relational stance feel less steady. Both trajectories are coherent overall, but `projected_oracle` shows fewer signs of compensatory warmth and less overshoot.

## oracle_long_vuln_001

Decision:
- winner: `left`
- left = `explicit_rel_state_projected_oracle`
- right = `baseline_relational_instruction_oracle_collapsed`

Reason:
In the vulnerability trajectory, `projected_oracle` stays closer to the requested low-pressure, non-counseling stance, especially in phases B-D and F. The collapsed single-layer version becomes heavier and more explanatory at key moments, especially A, E, and F, which introduces more relational overreach. This makes `projected_oracle` feel more like one continuous and well-bounded response style.

## Interim Conclusion

Across the two oracle cases in this control-alignment comparison:
- `explicit_rel_state_projected_oracle` > `baseline_relational_instruction_oracle_collapsed`

Interpretation:
- The two systems share the same prompt-based realization mechanism, but they do not behave equivalently.
- Collapsing oracle relation and behavior information into a single-layer instruction does not fully recover the coherence of the two-layer oracle interface.
- This supports the hypothesis that the layered control interface itself has practical value, not just the presence of good oracle content.

## Caution

This is still a small-sample manual judgment:
- only 2 oracle cases
- no repeated-sampling stability test yet
- no mixed-signal oracle case yet

So this should be treated as a strong intermediate signal, not a final claim.
