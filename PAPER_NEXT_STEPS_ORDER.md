# Next Steps Order

## Current principle

The paper still has a frozen empirical core:

- main deploy route: `relation -> i7`
- analytic bridge: `relation -> behavior(8D) -> i7`

However, the current conceptual priority has shifted.

The next steps should no longer treat `relation -> behavior -> i7` as the only natural chain.
Instead, they should increasingly treat:

- `relation`
- `behavior`
- `i7`
- and possibly language-level features

as different coordinate systems or projections over a shared latent interaction structure.

## Recommended order

### 1. Final judge write-up

Status:

- already executable now

Why first:

- confirms whether the frozen system is already good enough for the paper's core result
- prevents scope from expanding before the current result is fully written down

Deliverables:

- final judge rubric
- result tables
- draft-ready results section

### 2. Large data expansion

Why second:

- once the frozen result is clear, a much larger oracle set can increase confidence without changing the story
- it strengthens the same claim before reopening representation or interface questions

Recommended target:

- expand beyond the current `30` oracle phase points to at least `144`
- preferred target: `180` oracle phase points
- prioritize:
  - `mixed_signal`
  - `vulnerability`
  - `boundary_repair`
  - `ordinary_neutral`

### 3. Parameter interpretation of the 4D fitted model

Status:

- first-pass interpretation already completed

Why still third in the paper logic:

- parameter interpretation depends on the 8D route being kept in the paper
- after freeze, the 8D layer now has a clear role as the analytic bridge

What to interpret:

- which relation dimensions drive which behavior dimensions
- which quadratic terms matter most
- where the fitted mapping aligns with or departs from human intuition

Why not earlier:

- before route freeze, it was unclear whether this would be main-controller analysis or only auxiliary analysis

### 4. Deployable interface shape comparison

Examples:

- `8D -> i7-discrete`
- `8D -> continuous-interface`
- `relation -> direct-interface`

Why now promoted earlier:

- the current latent-basis search suggests the core problem may be better framed as a manifold / coordinate-system problem rather than a one-way layerwise regression problem;
- the deployable interface may therefore be a choice of coordinate chart, not merely the last step of a fixed chain.

Best use:

- compare which deployable interface family best preserves the useful structure in the shared latent control space.

### 5. Joint manifold / coordinate-structure analysis

Main question:

- are `relation`, `behavior`, `i7`, and language-side features better understood as different projections of a shared latent interaction manifold?

Why this matters:

- this avoids overcommitting to the hand-specified `relation -> behavior -> i7` chain;
- it makes the representation question less self-confirming;
- it better supports future generalization beyond companion AI.

### 6. Relation dimensionality search

Current role:

- now best treated as a supporting probe, not the whole story.

Examples:

- fewer than 4 relation dimensions
- learned 5D/6D latent bases
- redesigned bases

How to use it now:

- to test whether the present 4D ontology is robust;
- not yet to declare a final ontology.

## Practical decision rule

Current state update:

- final frozen result exists;
- large data expansion to `180` oracle phase points is complete;
- first interface-shape comparison is complete;
- naive continuous deploy chart (`c8`) is ruled out as a good default;
- latent-dimensionality search should now be treated as supporting evidence only, because it still depends on the current `raw4` ontology.

Therefore the next serious questions are:

1. among deploy charts, which softer or hybrid chart competes best with `i7`?
2. how much do axis wording and dimension naming affect execution?
3. after chart and wording are stabilized, what shared manifold structure remains across relation / behavior / interface?

## Experiment tiering rule

To control token cost and keep exploratory work clean, new experiments should no longer default to the largest oracle set.

### Tier 1. Small-sample screening

Use for:

- new interface families
- new deploy ontology candidates
- wording / naming / framing ablations
- exploratory representation ideas

Default substrate:

- `v1` oracle cases first

Promotion rule:

- only promote to a larger set if the candidate is:
  - clearly better than the current comparison target, or
  - at least competitive with the current best route/chart, or
  - directly necessary for a core paper claim

### Tier 2. Mid-sample confirmation

Use for:

- the top 1-2 candidates that survive screening
- experiments that look promising but are not yet part of the paper's frozen core

Default substrate:

- `v2` oracle cases

Purpose:

- confirm that the signal is not a tiny-sample artifact before spending `v3`-level cost

### Tier 3. Large-sample paper-grade evaluation

Use only for:

- frozen main comparison
- bridge sanity
- final judge packages
- experiments likely to appear in the main paper tables

Default substrate:

- `v3` oracle cases (`180` phase points)

Rule:

- do not run exploratory families directly on `v3` unless there is a strong reason

## Current operating policy

From this point on:

1. new exploratory interface or ontology ideas should start on `v1`
2. only shortlisted candidates move to `v2`
3. `v3` should be reserved for:
   - frozen core results
   - near-final competing candidates
   - paper-facing confirmation runs

## Short version

Best current order:

1. freeze the deploy ontology conclusion
2. keep new exploratory interface / ontology ideas on `v1` unless they are needed for a paper-facing claim
3. reserve `v3` for frozen core and paper-facing comparisons
4. move next to shared latent manifold / coordinate-structure analysis
5. keep relation-dimensionality results as supporting evidence, not the mainline

## Shared latent manifold analysis: concrete next stage

Now that the deploy chart line is sufficiently frozen, the next primary research question becomes:

- are `relation`, `behavior`, `i7`, and language-side realization better understood as different coordinate charts on a shared latent interaction manifold?

### Stage M1. Geometry alignment

Construct per-phase representations for:

- current `raw4` relation labels
- `behavior` 8D vectors
- `i7` numericized chart vectors
- language-side feature vectors extracted from generated responses

First-pass language features should stay simple and externally observable, for example:

- response length
- question count
- list / bullet tendency
- explicit advice tendency
- explicit reassurance tendency
- first-person / companion-presence markers

Primary analyses:

- pairwise distance-matrix correlation
- neighborhood overlap / kNN preservation
- family-wise cluster structure
- case-trajectory smoothness

Question answered:

- which spaces look like lower-distortion charts of the same local structure?

### Stage M2. Shared latent reconstruction

Learn a low-dimensional latent `z_t` per phase and test whether a shared latent can jointly reconstruct:

- `behavior`
- numericized `i7`
- language-side features

Question answered:

- does a common latent interaction structure explain multiple views at once?

### Stage M2.5. Inverse-manifold probe

Keep the latent-learning setup from M2:

- learn from `behavior`
- learn from numericized `i7`
- learn from language-side features
- do **not** use `relation_raw4` to construct the latent

Then ask whether the learned latent:

- predicts `relation_raw4` back well;
- separates interaction families cleanly enough to support a manifold reading;
- preserves case-level trajectory smoothness.

Question answered:

- is the shared latent stable enough to be treated as an inverse-manifold probe, rather than only a reconstruction trick?

### Stage M3. Trajectory-level analysis

Use the case structure explicitly:

- same-case trajectories should evolve smoothly
- family-level cases should show partially shared path shapes
- good deploy charts should preserve those path shapes rather than distort them

Question answered:

- which chart best preserves interactional trajectory continuity over time?

### Stage M3-lite. Pooled-latent trajectory comparison

Before committing to full M3, run a lighter trajectory probe on only the key routes:

- `direct sc_vA`
- `oracle_i7`
- optionally `oracle_state_i7_pfitpoly2`

Use one pooled latent basis and compare:

- family-level path profiles
- case-level path smoothness
- matched-case path distortion across routes

Question answered:

- does the current best real route follow the same latent path geometry as oracle, just with more noise?

## Immediate practical plan

The next concrete work items should therefore be:

1. keep the current deploy ontology line frozen in the paper:
   - deploy route = `relation -> i7 direct`
   - default ontology = `vA`
   - best framing = `sc`
   - best real candidate = `direct sc_vA`
   - keep `vC` as a vulnerability-sensitive alternative
2. build the first-pass manifold dataset:
   - raw4 labels
   - behavior 8D
   - numericized `i7`
   - language-side feature vectors
3. run M1 geometry alignment before any more ontology invention
4. run M2 shared-latent reconstruction
5. run M2.5 inverse-manifold probe before committing to a heavier M3
6. run M3-lite pooled-latent trajectory comparison on the key routes

## New main theory-facing line

The next primary research line should now be treated as:

- learn latent interaction structure directly from:
  - `behavior_8d`
  - `i7_numeric`
  - `language_features`
- sweep latent dimensionality;
- ask where reconstruction quality, family structure, and trajectory structure saturate;
- only afterwards ask how current charts such as `raw4`, `8D behavior`, and `i7` relate to that native latent.

This is now preferable to continuing to treat the hand-defined `4D -> 8D -> i7` stack as the main ontological object.

Two immediate sub-lines follow from this:

1. native latent discovery:
   - how many latent dimensions are actually needed?
2. native chart reading:
   - how should `raw4`, `8D behavior`, and `i7` be understood as charts or readouts of that native latent?
