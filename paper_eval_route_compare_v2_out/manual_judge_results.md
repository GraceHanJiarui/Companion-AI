# Route-Freeze Manual Judge Results (Cleaned v2)

This note records the cleaned route-focused reading after fixing duplicated-turn export in the `...vs_oracle_full_i7` comparisons.

Compared routes:

- `relation -> direct i7`
- `relation -> fitted 8D -> i7`

The question is which route should be treated as the main deployable controller after the current freeze.

## Cleaned reading

### Real route

Comparison:
- `route_real_direct_i7_vs_real_rel8_to_i7`

Current reading:
- `oracle_exec_warm_001`: `left`
- `oracle_exec_vuln_001`: `tie`
- `oracle_exec_cool_001`: `left`

Interpretation:
- direct `relation -> i7` stays simpler and more restrained in `warm` and `cool`;
- the fitted `8D -> i7` bridge remains coherent, but more often drifts toward practical expansion or extra steering;
- `vulnerability` remains mixed rather than a clean win.

### Oracle-state route

Comparison:
- `route_oracle_state_direct_i7_vs_oracle_state_rel8_to_i7`

Current reading:
- `oracle_exec_warm_001`: `left`
- `oracle_exec_vuln_001`: `right`
- `oracle_exec_cool_001`: `right`

Interpretation:
- direct `relation -> i7` looks cleaner in `warm`;
- corrected `relation -> fitted 8D -> i7` sounds more natural in `vulnerability` and `cool`, where direct `relation -> i7` can become slightly too meta or too control-surface-like.

## Route freeze

The cleanest current freeze is:

1. Treat `relation -> i7` as the main deployable-controller candidate.
2. Retain `relation -> fitted 8D -> i7` as the main analytic-bridge candidate.
3. Do not claim that one route universally dominates the other across all route conditions.

## Why this is the right freeze

- The real route matters most for the primary deployable controller decision.
- On that route, direct `relation -> i7` is currently better in two of three cases and not clearly worse in the third.
- At the same time, corrected `relation -> fitted 8D -> i7` is now genuinely competitive and should not be dropped as a failed design.
- This supports a paper framing in which:
  - `relation -> i7` is the simpler deployment route;
  - `relation -> behavior(8D) -> i7` remains the stronger analytic bridge for studying how relational state maps into behavior before deployment.
