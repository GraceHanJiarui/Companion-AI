# Analytic Layer vs Deploy Layer

## Working Thesis

Many LLM control problems may require separating two different objects that are often conflated:

1. an **analytic latent layer**
2. a **deployable execution interface**

The analytic layer is optimized for:

- interpretability
- compact explanatory structure
- fitting or reconstructing oracle targets

The deploy layer is optimized for:

- prompt executability
- robustness under stochastic realization
- stable downstream language behavior

The current companion-dialogue work suggests these two layers need not be identical.

## Why this matters

A latent representation can be:

- explanatory in oracle space
- numerically fit-able
- semantically meaningful to researchers

and still fail as a direct deployment interface for an LLM.

This implies a more general design principle:

> Do not assume that the best explanatory middle layer is also the best deployable control layer.

## Current evidence from the companion project

The current project supports the following pattern:

1. `relation -> behavior` can be fit reasonably well in oracle space.
2. `oracle_behavior -> deployed i7 -> language` can work comparatively well.
3. But `relation -> fitted behavior -> i7 -> language` can still fail badly.

This suggests the main unresolved problem is not only:

- finding a good latent representation

but also:

- constructing a deploy layer that preserves the useful structure of that latent representation.

## General research program

A general middle-layer training / control program could look like this:

1. Define an **analytic latent layer** for the domain.
2. Construct oracle targets for that layer and for downstream behavior.
3. Fit mappings in oracle space.
4. Separately design or learn a **deployable interface layer**.
5. Measure the gap between:
   - oracle-space explanatory fit
   - deploy-time controllability
6. Treat this gap as a first-class research object.

## Candidate applications beyond companion dialogue

This framework may generalize to:

- long-horizon tutoring
- supportive dialogue
- negotiation / de-escalation
- planning and deliberative agents
- task-oriented dialogue with latent policy states
- safety or style control where latent concepts are easier to define than deployable prompts

## Core methodological question

The general question is:

> When should an explicit middle layer be used as an analytic object, and when should it be replaced or mediated by a separate deploy layer?

This is different from simply asking whether a latent state can be fit.

## What would make this a strong future paper

To make this into a separate paper, the following would likely be needed:

1. At least two domains, not just companion dialogue.
2. Clear distinction between:
   - analytic fit
   - deployable control quality
3. Competing deploy-layer constructions:
   - direct interface
   - mediated interface
   - continuous vs discrete interfaces
4. Evidence that the same pattern appears across more than one model family.

## Current scope guidance

This idea is promising, but it is larger than the current companion paper.

For the current paper, the safe use of this idea is:

- as a discussion-level interpretation
- as a framing for why the deploy gap matters

For a future paper, it could become the main contribution:

- a general method for separating explanatory latent layers from deployable LLM control interfaces.
