# Route-Focused Manual Judge Results

This note records a first-pass human reading of the route-focused judge package:

- `relation -> direct i7`
- `relation -> fitted 8D -> i7`

The goal is not to decide which route is shorter or more helpful in the abstract, but which route more reliably preserves a coherent relational trajectory.

## Scope and caveat

The most trustworthy pairwise comparisons in the current export are:

- `route_real_direct_i7_vs_real_rel8_to_i7`
- `route_oracle_state_direct_i7_vs_oracle_state_rel8_to_i7`

The route comparisons against `explicit_rel_state_projected_oracle_i7` currently include duplicated turn entries in some exported items. Those are useful as weak qualitative references, but they should not yet be treated as hard route-selection evidence until the export is cleaned.

## Real route

### `route_real_direct_i7_vs_real_rel8_to_i7`

#### `oracle_exec_warm_001`
- winner: `left`
- interpretation:
  - direct `relation -> i7` stays slightly more restrained and cleaner in the later turns.
  - the fitted `8D -> i7` route is still coherent, but it reintroduces a bit more steering in `C` and more practical expansion in `E`.

#### `oracle_exec_vuln_001`
- winner: `tie`
- interpretation:
  - direct `relation -> i7` is less pushy, but it also produces an awkward meta-style explanation in `E`.
  - the fitted `8D -> i7` route is more behaviorally plausible, but it over-opens follow-up space and drifts toward option-giving.
  - neither side wins cleanly on relational coherence.

#### `oracle_exec_cool_001`
- winner: `left`
- interpretation:
  - direct `relation -> i7` better preserves the user's request for ordinary, low-presence interaction.
  - the fitted `8D -> i7` route stays acceptable, but it becomes slightly more service-oriented and reopens interaction more than needed.

### Current read of the real route

- Direct `relation -> i7` currently looks better in `warm` and `cool`.
- `vulnerability` remains mixed.
- This means the direct route is a serious candidate for the main deployable controller, but it does not yet dominate across all cases.

## Oracle-state route

### `route_oracle_state_direct_i7_vs_oracle_state_rel8_to_i7`

#### `oracle_exec_warm_001`
- winner: `left`
- interpretation:
  - direct `relation -> i7` feels slightly cleaner and less inflated.
  - the fitted `8D -> i7` route is still coherent, but it adds a bit more soothing and a somewhat more expanded `E` answer than needed.

#### `oracle_exec_vuln_001`
- winner: `right`
- interpretation:
  - direct `relation -> i7` becomes too meta and less natural in `E`.
  - the fitted `8D -> i7` route is still somewhat practical, but it stays much closer to an acceptable supportive trajectory.

#### `oracle_exec_cool_001`
- winner: `right`
- interpretation:
  - direct `relation -> i7` contains slightly awkward control-surface phrasing such as explicit restraint/commitment language.
  - the fitted `8D -> i7` route preserves distance while sounding more like ordinary dialogue.

### Current read of the oracle-state route

- `warm` favors direct `relation -> i7`.
- `vulnerability` favors `relation -> fitted 8D -> i7`.
- `cool` also currently favors `relation -> fitted 8D -> i7`.

## Working takeaway

At this point:

- direct `relation -> i7` is simpler and looks strong on the real route;
- corrected `relation -> fitted 8D -> i7` is now genuinely competitive rather than obviously broken;
- no route has yet earned an across-the-board win.

The cleanest current interpretation is:

1. the 8D behavior layer should no longer be dismissed as the main source of deployment failure;
2. direct `relation -> i7` remains attractive as a simple deployable route;
3. final route selection still needs one more cleaned comparison step, especially for the oracle-full reference export.
