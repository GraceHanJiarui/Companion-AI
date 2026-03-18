# Relational Coherence Operationalization

## Purpose

This file strengthens the paper's treatment of relational coherence by separating:

1. the main judge-centered construct
2. a structured label layer
3. a semi-formal heuristic layer
4. a lightweight automatic proxy layer

The paper should still treat relational coherence as a judge-centered endpoint.
However, this file makes the construct less soft and more reproducible than a
purely verbal description.

## A. Judge-Centered Core Definition

Relational coherence means:

- a multi-turn dialogue still feels like one ongoing relationship process
- stance changes remain supported by prior trajectory and current user signal
- ordinary continuation and final-probe turns do not reopen or escalate the interaction without support

Abrupt relational shift means:

- a stance change in direction or magnitude that exceeds what the previous trajectory and current user signal support

This remains the paper's main endpoint and is judged through the frozen appendix prompt.

## B. Structured Label Layer

The paper should no longer rely only on one overall coherence score.
The main case-level judge should also emit binary structured labels for:

- `unsupported_warmth_increase`
- `unsupported_distance_increase`
- `unsupported_initiative_jump`
- `continuation_reopen_after_cooling`
- `final_probe_overshoot`
- `trajectory_reset_present`
- `has_abrupt_shift`

These labels are intentionally simpler than a full theory of relationship, but they
make the evaluation more auditable:

- a reader can inspect which failure mode caused a low coherence judgment
- agreement can be reported on observable failure categories
- the final claim is no longer carried by a single scalar alone

## C. Semi-Formal Heuristic Components

These are not treated as full replacements for judge, but as structured diagnostics.

### 1. Warmth jump

Heuristic meaning:

- a turn-to-turn increase or decrease in warmth markers beyond a modest threshold

Paper-facing shorthand:

- `Δ warmth per turn`

Example interpretation:

- large sudden increase after user cooling cues
- sudden disappearance of warmth after a stable warmer trajectory

### 2. Unexpected polarity flip

Heuristic meaning:

- a sign flip between warmth-leaning and distance-leaning language with nontrivial magnitude

Paper-facing shorthand:

- `unexpected polarity flip`

Example interpretation:

- the assistant moves from companion-like presence to distance-management language, or vice versa, without sufficient build-up

### 3. Unsupported initiative jump

Heuristic meaning:

- initiative-related behavior rises sharply after a user signal that requests ordinary, lower-pressure, or lower-care interaction

Paper-facing shorthand:

- `unsupported initiative jump`

Example interpretation:

- user asks for normal/light interaction
- assistant suddenly adds follow-up questions, suggestions, or strong guidance

### 4. Response length spike

Heuristic meaning:

- current reply length rises sharply relative to the previous turn

Paper-facing shorthand:

- `response length spike`

This is not itself a coherence metric, but is useful because many project failures
showed up as continuation inflation and over-expansion.

## D. Automatic Proxy Layer

The project now includes a lightweight automatic proxy script:

- [paper_relational_proxy_metrics.py](d:/My%20Project/companion-ai/paper_relational_proxy_metrics.py)

Current heuristic outputs include:

- `reply_len_chars`
- `question_count`
- `warmth_score`
- `distance_score`
- `initiative_score`
- `meta_control_score`
- `bullet_count`
- `polarity_score`
- `length_spike`
- `warmth_jump`
- `unexpected_polarity_flip`
- `unsupported_initiative_jump`
- `abrupt_shift_proxy`

## E. Current Heuristic Definitions

The current script uses intentionally simple rules.

### `length_spike`

True when:

- current reply length >= 1.8x previous reply length
- and current reply is at least 40 characters longer

### `warmth_jump`

True when:

- absolute turn-to-turn change in warmth-marker count >= 2

### `unexpected_polarity_flip`

True when:

- polarity score flips sign
- and the magnitude change is >= 2

### `unsupported_initiative_jump`

True when:

- the user turn contains a cooling / boundary cue
- and assistant initiative score increases by >= 2

### `abrupt_shift_proxy`

True when:

- at least two heuristic votes are active
- or any polarity flip occurs
- or any unsupported initiative jump occurs

## F. Paper-Facing Use

Recommended use in the paper:

- the paper's main evaluation should be a multi-evidence package:
  - structured case-level judge labels
  - pairwise judge preference
  - agreement
  - automatic proxy diagnostics
- overall coherence remains the top-line judge-centered endpoint
- structured labels explain which failure types are present
- semi-formal heuristics help define what kinds of shifts we care about
- automatic proxies are reported only as secondary diagnostics

This gives the paper a stronger evaluation story:

- not purely subjective narrative
- but also not falsely claiming that the whole construct is solved by a scalar metric

## G. What Not To Claim

The paper should not claim that these proxies are:

- the ground-truth definition of relational coherence
- model-internal measurements
- complete replacements for case-level coherence judging

The correct framing is:

- structured heuristics that partially operationalize abrupt shift and trajectory instability
- useful for reproducibility and diagnostics
- subordinate to the judge-centered endpoint
