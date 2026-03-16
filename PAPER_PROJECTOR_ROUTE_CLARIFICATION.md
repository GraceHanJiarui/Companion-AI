# Projector Route Clarification

## Purpose

This note records the design discussion after the `oracle_state_i7` gap experiments.
Its purpose is to prevent the projector redesign from drifting into a weaker research framing.

It should be read as an addendum to:

- `PAPER_PROPOSAL_RELATION_STATE.md`
- `PAPER_EXECUTION_PLAN.md`
- `PAPER_EXPERIMENT_REGISTRY.md`

## Background

Current experiments support all of the following:

- `oracle i7 > real i7 > baseline`
- `oracle_behavior_i7 ~= oracle_i7`
- `oracle_state_i7 << oracle_behavior_i7`
- `oracle_state_i7` can even be worse than `real i7`

This strongly suggests that the current bottleneck is the deterministic
`relation -> behavior` projector.

However, this does **not** yet justify immediately replacing the second layer
with a heavily hand-written discrete controller, nor does it justify treating
`scene` and `phase` as already-proven mandatory inputs.

## What the paper is still trying to study

The main research object should remain:

1. an explicit relational state
2. an explicit behavior layer
3. a two-layer mapping from relation to behavior
4. a language realization stage

The stronger and more elegant claim is still:

- an explicit relational state may explain and constrain behavioral progression
- a two-layer continuous design may be meaningful

The project should avoid prematurely collapsing into:

- pure prompt engineering
- a hand-built controller that simply encodes desired answers

## Key clarification

The following move is **not** yet the default answer:

- `behavior = f(relation, scene, phase)`

It may become necessary, but at this point it should be treated as a
competing hypothesis to test, not as an assumed truth.

The central unresolved question is:

- is the current failure caused by a poor mapping from relation to behavior?
- or by an insufficient relation representation?
- or by genuinely irreducible information carried by `scene` and `phase`?

## Three experiment branches

### Branch A. Pure relation projector

Form:

- `behavior = f(relation)`

Goal:

- preserve the strongest explanatory claim
- test whether a better deterministic projector can work without extra context variables

Interpretation:

- if this branch succeeds, then explicit relational state remains a strong explanatory substrate

### Branch B. Conditioned projector

Form:

- `behavior = f(relation, scene, phase)`

Goal:

- test whether `scene` and `phase` provide large, stable, and non-redundant gains

Interpretation:

- this branch is a necessity test
- it should only be promoted if it clearly outperforms improved pure-relation projectors

### Branch C. Relation redesign / reverse analysis

Form:

- redesign the relation dimensions themselves using behavior residual analysis

Goal:

- test whether current relation dimensions are insufficient
- ask whether what looks like `scene/phase` information can instead be absorbed into a better relation space

Interpretation:

- this branch preserves the original scientific ambition better than immediately introducing more external conditioning variables

## Current agreed research position

The project should proceed in this order:

1. improve `behavior = f(relation)`
2. test `behavior = f(relation, scene, phase)` as a necessity branch
3. investigate whether relation-space redesign can absorb apparent scene/phase effects

This means:

- `scene` and `phase` are not rejected
- but they are not treated as default mandatory inputs
- they must be shown to be necessary and non-replaceable

## Why this matters

If `scene/phase` are introduced too early as default inputs, the work risks becoming:

- less elegant
- less explanatory
- more dependent on hand-labeled context variables
- closer to a manually engineered controller than to an explicit relational-control study

By keeping them as a tested alternative instead of a default assumption, the paper preserves a stronger research claim:

- explicit relational state may still explain behavioral progression
- if it cannot, the failure should be shown rather than assumed

## Planned experiments

### Immediate next design goal

Design a stronger pure-relation projector before declaring `scene/phase` necessary.

### Then compare

1. improved pure-relation projector
2. conditioned projector
3. relation-redesign hypotheses

### Decision rule

Only promote `scene/phase` into the main design if:

- improved pure-relation projectors still fail substantially, and
- conditioned projectors show large and stable gains that cannot plausibly be recovered by relation redesign

## Status

Current status after the latest discussion:

- the team accepts the three-branch route
- the main paper framing should continue to treat the pure two-layer route as the preferred hypothesis
- conditioned projector is now explicitly a necessity-test branch, not the presumed final answer
