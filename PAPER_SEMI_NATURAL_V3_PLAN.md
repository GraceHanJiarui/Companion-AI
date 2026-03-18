# Semi-Natural V3 Plan

## Goal

`semi-natural v3` is intended to become the first paper-facing generalization set.

Its job is not to replace the controlled oracle mechanism set. Its job is to answer
a narrower question:

- do the main deploy-side conclusions still hold when the user-side interaction paths
  are written with substantially less template regularity?

The target conclusion is therefore:

- **generalization support**
- not **oracle-style mechanism diagnosis**

## What V3 Must Be Better Than

`semi_natural_v1` and `semi_natural_v2` failed mainly because they remained too close
to the oracle case skeleton.

V3 must improve on them in four concrete ways:

1. family-defining signals must appear at different positions
2. trajectory shape must vary across cases within the same family
3. ordinary topics must be drawn from a much broader distribution
4. user wording must sound less like ontology annotation in disguise

## Recommended Dataset Size

Recommended first paper-facing version:

- `24` cases total

Proposed allocation:

- `warming_trajectory` x4
- `vulnerability_with_correction` x4
- `cooling_trajectory` x4
- `mixed_signal_trajectory` x4
- `boundary_repair` x4
- `ordinary_neutral` x4

This is large enough to diversify trajectory shapes, while still being cheap enough
to run with a restricted mode set.

## Mode Scope

V3 should not be used for full route/bridge/oracle analysis.

Recommended modes:

- `baseline_relational_instruction`
- `baseline_relational_instruction_to_interface_i7_sc_vA`
- `explicit_rel_state_rel_to_interface_i7_sc_vA`

Optional:

- one small human-blind subset

Not recommended for V3:

- oracle behavior routes
- bridge-heavy route comparisons
- ontology family sweeps

## Structural Rule: Six Turns Are Allowed, Fixed Functional Slots Are Not

For convenience and comparability, V3 may still use six user turns.

However, the six turns must not be interpreted as:

- fixed phase semantics
- fixed family cue positions
- fixed final continuation probes

V3 should therefore use generic turn labels in generation drafts, such as:

- `turn_1`
- `turn_2`
- `turn_3`
- `turn_4`
- `turn_5`
- `turn_6`

If later converted to the existing paper schema, those labels should be treated as
indexing convenience only, not as evidence that the functional skeleton still holds.

## Trajectory Shape Buckets

Each family should be represented by multiple internal shapes. We should avoid
repeating the same path even within the same family.

### Shape A: Early Signal, Later Narrowing

Pattern:

- weak family-defining signal appears early
- later turns constrain its meaning

Good for:

- `warm`
- `mixed`
- `vulnerability`

### Shape B: Late Signal

Pattern:

- early turns are ordinary or low-information
- the meaningful relation signal appears only at turn 4 or later

Good for:

- `warm`
- `cool`
- `ordinary_neutral`

### Shape C: Correction-First

Pattern:

- the user first reacts against a perceived interaction style
- later clarifies what would be acceptable instead

Good for:

- `boundary_repair`
- `cool`
- `vulnerability`

### Shape D: Soft Oscillation

Pattern:

- user moves one step warmer or cooler
- then partially retracts
- later settles in a narrow middle band

Good for:

- `mixed`
- `warm`

### Shape E: Failed Topic Shift

Pattern:

- user tries to move into ordinary talk
- but a family-relevant signal reappears later

Good for:

- `vulnerability`
- `repair`
- `mixed`

### Shape F: No Explicit Final Probe

Pattern:

- final turn does not ask to "keep chatting this way"
- instead ends on:
  - a topic shift
  - low-energy trailing-off
  - a vague maybe-later continuation

Good for all families.

At least half of V3 should use `Shape F`.

## Topic Buckets

To avoid reusing the same "empty evening / can't sleep" domain, V3 should draw from
broader ordinary-life contexts.

Recommended topic buckets:

1. commute / transit
2. cooking / cleaning / showering
3. post-work decompression
4. weekend drift / idle afternoon
5. phone scrolling / passive distraction
6. errands / grocery / waiting
7. after-social-event decompression
8. low-energy household drift

Rule:

- no single topic bucket should cover more than 25% of the set

## Family-Specific Writing Requirements

### 1. Warming Trajectory

V3 requirement:

- at least 2 of 4 cases must delay the first clear positive relational signal until
  turn 3 or later
- at least 2 of 4 cases must avoid explicit phrases equivalent to:
  - "keep replying like this"
  - "don't get too serious"

We want the warmth trajectory to be inferred from the user's gradual relaxation,
not just from an explicit instruction.

### 2. Vulnerability With Correction

V3 requirement:

- at least 2 of 4 cases must begin with low-information vulnerability rather than
  explicit distress disclosure
- at least 2 of 4 cases must express the anti-therapy boundary only after a prior
  turn has already shown some relief

We want to test whether the model respects narrowing, not just whether it can
parrot "I won't therapize you."

### 3. Cooling Trajectory

V3 requirement:

- at least 2 of 4 cases must start without an explicit distance declaration
- at least 2 of 4 cases must show cooling through preference for ordinaryness rather
  than "don't care about me / don't accompany me" wording

We want more implicit cooling, not only explicit anti-warmth commands.

### 4. Mixed-Signal Trajectory

V3 requirement:

- all 4 cases must avoid textbook phrases like:
  - "don't overread this"
  - "I'm not sending a signal"
- at least 2 of 4 cases must show the mixed nature indirectly through contradictory
  or self-revising turns

This family should be the least didactic and the most realistically ambiguous.

### 5. Boundary Repair

V3 requirement:

- all 4 cases must make it clear that the user is reacting to a felt overstep
- at least 2 of 4 cases must avoid direct meta phrases like:
  - "you were too warm"
  - "you became too caring"

Instead, repair should sometimes be inferred from:

- "that was a bit much"
- "that kind of tone doesn't work for me"
- "let's pull it back a little"

### 6. Ordinary Neutral

V3 requirement:

- all 4 cases must avoid obvious family contamination
- no case should contain a line that sounds like weak `warm` or weak `cool`
  unless the point is precisely to test whether the system invents significance

This family is the cleanest anti-overinterpretation baseline.

## Rejection Rules

A draft case should be rejected if any of the following are true:

1. A reader can trivially map each turn to the old oracle phase functions.
2. The family is only visible because one line explicitly names the family tension.
3. The case could be summarized as "oracle case paraphrase with more colloquial wording."
4. The final turn simply restates "reply like this later" without any other plausible
   natural ending.
5. The topic is just another variant of the current evening / tired / sleepless cluster.

## Drafting Workflow

Recommended workflow:

1. assign family
2. assign trajectory shape bucket
3. assign topic bucket
4. write user-only six-turn draft with generic turn labels
5. run rejection check
6. manually edit for surface realism
7. only then convert into the evaluation JSON schema

This workflow is deliberately more constrained than the old semi-natural drafting flow.

## Minimum Acceptance Audit Before Running Experiments

Before V3 is used in experiments, run a lightweight audit:

1. family balance check
2. topic bucket balance check
3. shape bucket balance check
4. explicit-meta-phrase count
5. final-turn-probe rate

Desired targets:

- at least `4` different shape buckets represented
- final explicit "keep replying like this" turn in fewer than 50% of cases
- at least 6 topic buckets represented across 24 cases
- mixed-signal cases contain the lowest explicit meta rate

## Paper Positioning

If V3 is built successfully, it should be described in the paper as:

- a **semi-natural generalization set**
- built to reduce the phase-template regularity of the oracle mechanism set

It should not be described as:

- a naturalistic real-world corpus
- an externally sourced conversation dataset

Those would require a different data program.
