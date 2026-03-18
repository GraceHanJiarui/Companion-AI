# Shared Latent Manifold Analysis Plan

## Why this is the next stage

The deploy chart line is now sufficiently frozen to support a cleaner next question:

- are `relation`, `behavior`, `i7`, and language-side realization better understood as different coordinate charts on a shared latent interaction manifold?

This is a better next-stage question than continuing to invent many more deploy ontologies, because:

- the current deploy story is already strong enough for the paper;
- the remaining open problem is less about one more prompt chart and more about the geometry of the underlying interaction structure;
- this framing reduces the risk of self-confirming chain-of-regression arguments.

## Frozen assumptions to carry forward

For the current paper-facing system, treat the following as frozen:

- main deploy route:
  - `relation -> i7 direct`
- default deploy ontology:
  - `vA`
- best current framing:
  - `sc`
- best current real candidate:
  - `direct sc_vA`
- analytic bridge:
  - `relation -> behavior(8D) -> i7`
- family-sensitive alternative to keep in view:
  - `vC`, especially for vulnerability-like cases

## Stage M1: geometry alignment

### Goal

Test whether the main representational spaces preserve similar local structure.

### Per-phase views to build

For each oracle phase point, create:

1. `relation_raw4`
2. `behavior_8d`
3. `i7_numeric`
4. `language_features`

### First-pass language features

Keep them external and low-interpretation:

- response length
- question count
- list / bullet tendency
- explicit advice tendency
- explicit reassurance tendency
- first-person / companion-presence markers
- explicit self-description / meta-control tendency

### Analyses

1. pairwise distance-matrix correlation
2. neighborhood overlap / kNN preservation
3. family-level cluster inspection
4. case-trajectory smoothness

### Questions answered

- is `i7` closer to `behavior` than to `relation_raw4`?
- is language closer to `i7` than to `behavior`?
- does `raw4` look like a coarse chart of the same local geometry, or a partially misaligned one?

## Stage M2: shared latent reconstruction

### Goal

Test whether a common latent `z_t` can jointly explain multiple views.

### Setup

Learn a low-dimensional latent code per phase and reconstruct:

- `behavior_8d`
- `i7_numeric`
- `language_features`

Optional later extension:

- include `relation_raw4` as either an encoder input or an auxiliary supervised target

### Questions answered

- does a shared latent interaction structure explain multiple views at once?
- how many latent dimensions are enough before gains saturate?
- which view is easiest / hardest to reconstruct from the shared latent?

## Stage M2.5: inverse-manifold probe

### Goal

Check whether the shared latent found in M2 is stable enough to support a stronger manifold reading, rather than merely a reconstruction story.

### Setup

Continue to learn the latent only from:

- `behavior_8d`
- `i7_numeric`
- `language_features`

Do **not** use `relation_raw4` to build the latent itself.

Then evaluate whether the learned latent:

- predicts `relation_raw4` back strongly;
- separates case families such as `warm`, `vulnerability`, `cooling`, and `boundary_repair`;
- preserves within-case trajectory smoothness.

### Questions answered

- is the learned latent stable enough to function as an inverse-manifold probe rather than only a reconstruction device?
- do family structure and trajectory continuity survive in the learned latent?
- does the best real route (`direct sc_vA`) look like a noisier version of the same latent structure as oracle, or a genuinely different one?

## Stage M3: trajectory-level manifold reading

### Goal

Move beyond static point similarity and study path structure.

### Analyses

1. within-case path smoothness
2. family-wise path shape comparison
3. chart distortion of path continuity

### Questions answered

- which chart best preserves the shape of an interaction trajectory?
- does `i7` preserve the interaction path better than `behavior`, or vice versa?
- does `vC` preserve vulnerability trajectories better than default `vA`?

## Stage M3-lite: trajectory-distortion probe

Before making a heavy M3 claim, run a lighter shared-latent trajectory comparison on a very small set of key routes:

- `direct sc_vA`
- `oracle_i7`
- optionally `oracle_state_i7_pfitpoly2`

### Goal

Fit one pooled latent basis across the selected routes and compare:

- within-route family path shapes;
- case-level path smoothness;
- path distortion between matched cases across routes.

### Questions answered

- does the best real route look like a noisier version of the same path geometry as oracle?
- where is path distortion concentrated:
  - vulnerability
  - cooling
  - boundary repair
- is the bridge route geometrically closer to oracle than to a tool-like detour?

## Minimal deliverables

The next implementation pass only needs to deliver:

1. one dataset builder that exports:
   - raw4
   - behavior 8D
   - numericized i7
   - language feature vectors
2. one M1 analysis script for:
   - distance-matrix correlation
   - neighborhood overlap
   - basic trajectory smoothness
3. one short writeup of:
   - what aligns with what
   - what clearly does not

## Decision rule after M1

### If `i7` and language align most strongly

Then the current interpretation strengthens:

- deploy charts should be chosen for execution geometry, not for closeness to analytic vectors

### If `behavior` and language align more strongly

Then we should revisit whether the bridge is being discretized too aggressively.

### If `raw4` aligns poorly with both

Then relation ontology discovery should be reopened later, but only after manifold evidence rather than before.

## Immediate next implementation after M2

The next concrete step is now:

1. run an inverse-manifold probe (`M2.5`) on:
   - the best current real route (`direct sc_vA`)
   - the current oracle route (`oracle_i7`)
2. compare:
   - relation prediction from latent
   - family-separation quality
   - latent trajectory smoothness
3. run an `M3-lite` pooled-latent trajectory comparison on the key routes.
4. only move to a heavier `M3` if these signals are stable enough to justify stronger manifold claims.
