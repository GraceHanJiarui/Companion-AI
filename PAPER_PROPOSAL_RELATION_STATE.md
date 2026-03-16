# Paper Proposal: Two-Layer Relational Control

## 1. Research focus

This paper is no longer framed as a broad companion-system paper.
Its current focus is much narrower:

- long-horizon companion-style dialogue
- relational coherence across multiple turns
- explicit intermediate control
- the difference between:
  - single-layer relational control
  - two-layer relational-to-behavior control

The paper does **not** try to prove the entire product architecture.
It also does **not** attempt to solve all questions about relational representation.

## 2. Main question

The current main question is:

**Can a two-layer relational control architecture produce more coherent long-horizon companion dialogue than strong single-layer prompting, and if not fully, where does the remaining gap come from?**

This is studied through:

- strong baseline comparison
- oracle vs real-chain comparison
- single-layer vs two-layer comparison
- gap diagnosis between relational state, behavior control, and language realization

## 3. Why this question matters

Prompt-only systems can often produce locally fluent dialogue while still drifting relationally over time.
They may:

- become too warm too quickly
- over-explain
- over-offer help
- ask too much
- lose the sense of gradual progression

An explicit control architecture is attractive because it may:

- make relational progression more interpretable
- make dialogue behavior more controllable
- provide a better substrate for analysis and later training

But explicit control does **not** automatically imply better language behavior.
That empirical tension is now one of the main motivations of the paper.

## 4. Current paper framing

The paper is currently best framed around four connected claims:

1. strong baselines are highly competitive
2. single-layer relational control is weaker than two-layer control
3. oracle two-layer control shows clear structural potential
4. the main remaining bottleneck is not state existence, but how the control is mapped and realized

This is now a stronger and cleaner framing than the earlier, weaker question:

- "does explicit relational state help at all?"

## 5. Experimental design

### Systems compared

The current paper line centers on:

- `baseline_relational_instruction`
- `explicit_rel_state_direct`
- `explicit_rel_state_projected`
- oracle and hybrid variants of these systems

The most important Stage-2 interface candidate is currently:

- `i7`

### Evaluation target

The main target is not internal dimension recovery.
It is external dialogue quality at the level of long interaction cases:

- case-level relational coherence
- abrupt relational shift
- phase-aware continuity

### Long-range cases

The paper uses long-range structured cases rather than short 2-3 turn probes.
The important case families now include:

- warming
- vulnerability
- cooling
- mixed-signal remains the final planned closing case

## 6. Main findings so far

### 6.1 Strong baseline competitiveness

`baseline_relational_instruction` is not a weak baseline.
Across multiple experiments, it remains highly competitive and often absorbs much of the visible language-layer gain.

This is important because it prevents the paper from claiming a trivial win.

### 6.2 Single-layer vs two-layer

The current evidence supports:

- single-layer control is weaker
- two-layer control has real structural value

This is supported by:

- `direct` vs `projected`
- `direct_oracle` vs `projected_oracle`
- oracle two-layer vs collapsed single-layer controls

### 6.3 Stable ordering of the best current interface

For the current best execution interface candidate (`i7`), repeated sampling and manual judge support:

- `oracle i7 > real i7 > baseline`

This is one of the strongest current results in the paper line.

### 6.4 Gap localization

The most recent experiments now strongly suggest:

- the main bottleneck is the deterministic `relation -> behavior` projector
- not the mere existence of explicit relational state
- not prompt bridge alone
- not mainly the updater
- not primarily final realization

The critical result was:

- `oracle_state_i7` performed worse than `real i7`
- `oracle_behavior_i7` stayed close to `oracle_i7`

This indicates that the current projector is translating even good relational state into poor behavior control.

## 7. Current interpretation

The strongest current interpretation is:

- the two-layer route is supported, not weakened
- the failure point is in the current projector design
- a behavior layer is genuinely useful
- but the present mapping from relation to behavior is structurally flawed

This means the paper's current contribution is no longer just:

- "explicit state helps"

but rather:

- strong baselines are hard to beat
- single-layer control is insufficient
- two-layer structure has real potential
- and the main practical bottleneck lies in executable mapping quality

## 8. Guardrail on projector redesign

The next projector work should not collapse into a purely hand-written discrete controller.

The current preferred scientific route is still:

- improve a two-layer `behavior = f(relation)` design as far as possible

Only after that should the project ask whether:

- `scene`
- `phase`

are truly necessary and non-replaceable inputs.

So the current research order is:

1. improve pure relation projector
2. test conditioned projector as a necessity branch
3. investigate whether relation-space redesign can absorb apparent scene/phase effects

## 9. What this paper is not trying to do

This paper does not try to fully answer:

- what the optimal relational representation is
- why strong baselines are inherently so strong
- whether the full product control skeleton is better than zero-shot dialogue in every respect
- how to model human-human relationships in general

Those are legitimate future paper directions, but they would make the current paper lose focus.

## 10. Immediate next steps

The immediate technical next step is:

- continue diagnosing and redesigning the projector

The immediate paper next step is:

- keep the main writing centered on:
  - strong baseline competitiveness
  - single-layer vs two-layer comparison
  - `oracle i7 > real i7 > baseline`
  - projector as the current dominant bottleneck

## 11. Relationship to other documents

This file is the conceptual anchor.

Use:

- `PAPER_DRAFT_RELATIONAL_CONTROL.md`
  - for the writing-oriented paper draft
- `PAPER_EXECUTION_PLAN.md`
  - for next-step execution
- `PAPER_EXPERIMENT_REGISTRY.md`
  - for reproducible experiment history
- `PAPER_PROJECTOR_ANALYSIS.md`
  - for projector-specific technical diagnosis
