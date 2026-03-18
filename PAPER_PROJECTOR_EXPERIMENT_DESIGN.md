# Projector Experiment Design

## Goal

Design the next-stage experiments for three competing explanations of the current projector failure:

1. `pure relation projector`
2. `conditioned projector`
3. `relation redesign / reverse analysis`

These three lines are not meant to run fully in parallel forever.
They are ordered so the cleaner explanation is tested first.

## Current starting point

Already supported:

- `oracle i7 > real i7 > baseline`
- `oracle_behavior_i7 ~= oracle_i7`
- `oracle_state_i7 << oracle_behavior_i7`
- profile tuning (`balanced / conservative / sparse`) did not fix `oracle_state_i7`

Current interpretation:

- the main bottleneck is the deterministic `relation -> behavior` projector
- not prompt bridge
- not mainly the updater
- not mainly final realization
- but projector quality must now be split into two questions:
  - oracle-space fit quality,
  - and deployed compatibility with the `i7` execution interface / language stack

## Shared evaluation protocol

All three lines should use the same main evaluation lens whenever possible.

### Main case set

Use:

- `warm`
- `vulnerability`
- `cooling`
- `mixed_signal` once finished

Prefer:

- oracle execution cases for diagnosis
- then real-chain cases for confirmation

### Main comparisons

Keep the main comparison frame stable:

- `baseline_relational_instruction`
- `explicit_rel_state_projected_i7`
- relevant oracle / hybrid variants

### Main metrics

Primary:

- case-level relational coherence
- abrupt relational shift
- phase-aware coherence

Secondary:

- average reply length
- phase-level over-expansion
- repeated-sampling stability

## Line A. Pure relation projector

### Research question

Can a better deterministic projector

- `behavior = f(relation)`

close most of the current `real i7 -> oracle i7` gap without introducing external conditioning variables?

### Why this line matters

This is the strongest and most elegant version of the research claim.
If it works, the paper can still argue that explicit relational state itself is a meaningful explanatory substrate.

### Hypothesis

The current failure is caused by a poor mapping function, not by the impossibility of pure relation-based projection.

### Minimal implementation strategy

Do **not** jump to discrete hard-coded behavior answers.
Instead, redesign the projector while keeping:

- continuous relation state
- continuous or smoothly interpretable behavior targets
- deterministic mapping

Recommended substeps:

1. reduce global over-activation of:
   - expansion
   - affective follow-up
   - initiative
   - disclosure

2. decouple:
   - warmth
   - relational push

3. reduce behavior coupling:
   - relation increase should not automatically imply more questions and more initiative

4. test non-linear but still deterministic mapping
   - thresholds
   - saturation
   - gated interaction terms

### Experimental variants

Recommended variants:

- `projector_v3a`: lower-coupling deterministic mapping
- `projector_v3b`: thresholded deterministic mapping
- `projector_v3c`: relation-only non-linear mapping with stronger suppression

### Required comparisons

For each pure projector candidate, compare:

- `explicit_rel_state_projected_i7_[candidate]`
- `explicit_rel_state_projected_oracle_state_i7_[candidate]`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

### Success criterion

This line is supported if:

- `oracle_state_i7_[candidate]` moves substantially toward `oracle_behavior_i7`
- and no longer performs worse than `real i7`

Strong version:

- `oracle_state_i7_[candidate] ~= oracle_behavior_i7`

### Failure criterion

This line weakens if:

- several redesigned pure projectors still leave `oracle_state_i7` far from `oracle_behavior_i7`
- especially if the residual gap remains large across all case types

### Updated note after fitted-projector deployment

- supervised `fitlinear` / `fitpoly2` baselines showed that 4D relation can explain oracle behavior surprisingly well in regression space;
- however, deployable `pfitlinear` / `pfitpoly2` still failed to bring `oracle_state_i7` close to `oracle_behavior_i7 / oracle_i7`;
- therefore future projector work must distinguish:
  - "better function fit in oracle space"
  - from
  - "better deployed projector inside the actual execution stack."

## Line B. Conditioned projector

### Research question

Does adding explicit conditioning variables yield large, stable, and non-redundant gains?

Form:

- `behavior = f(relation, scene, phase)`

### Why this line matters

This is a necessity test, not the default answer.
It checks whether the pure-relation projector is missing genuinely indispensable information.

### Hypothesis

Some behavior distinctions cannot be recovered from the current relation space alone.
`scene` and `phase` may carry irreducible information for correct projection.

### Minimal implementation strategy

Use the lightest possible conditioning first.

#### Condition set

Start with:

- `scene`
  - `warm`
  - `vulnerability`
  - `cooling`
  - `mixed_signal`
- `phase`
  - `A/B/C/D/E/F`

#### Important restriction

Conditioning should modify the projector, not replace it with a manually authored final answer.

Good form:

- relation-driven mapping plus conditioned modulation

Bad form:

- large hand-written rules that directly dictate final behavior outputs independent of relation

### Experimental variants

Recommended staged variants:

- `cond_v1`: phase-only modulation
- `cond_v2`: scene-only modulation
- `cond_v3`: scene + phase modulation

### Required comparisons

Compare each conditioned variant against:

- best pure-relation projector candidate
- `baseline_relational_instruction`
- `oracle_behavior_i7`
- `oracle_i7`

### Success criterion

This line is supported only if:

- conditioned projector yields large and repeatable gains over the best pure-relation projector
- and the gains appear across multiple case families, not just one

### Promotion criterion

`scene/phase` should only be promoted into the main design if:

- pure-relation projector improvements stall
- and conditioned projector gains are large, stable, and clearly non-redundant

## Line C. Relation redesign / reverse analysis

### Research question

Is the current relation representation itself insufficient?

Instead of assuming that `scene/phase` are necessary, ask:

- can a redesigned relation space absorb what conditioned projector variants seem to need?

### Why this line matters

This line preserves the explanatory ambition of the project.
It treats projector failure as a possible representation problem, not automatically as evidence for external labels.

### Hypothesis

Current relation dimensions may be missing latent structure needed to determine behavior.

Examples of missing relational semantics could include:

- openness-to-guidance
- task-coordination readiness
- support receptivity
- conversational momentum
- repair sensitivity

These are only examples, not committed final dimensions.

### Minimal implementation strategy

Use reverse analysis from oracle behavior residuals.

### Current first-pass finding

We now have an initial oracle-only reverse analysis from:

- [paper_relation_reverse_analysis_v1.json](d:/My%20Project/companion-ai/paper_relation_reverse_analysis_v1.json)
- [PAPER_RELATION_REDESIGN_ANALYSIS.md](d:/My%20Project/companion-ai/PAPER_RELATION_REDESIGN_ANALYSIS.md)

The current signal is:

- there are multiple pairs of turns with very similar relation states but noticeably different oracle behavior targets;
- the most recurrent divergent behavior dimensions are:
  - `Q_aff`
  - `Q_clarify`
  - `T_w`
  - `Initiative`
  - and, secondarily, `E`

This suggests that the current relation space is more likely under-specified for:

- follow-up style,
- support intensity,
- and proactive interaction tendency.

At the current stage, disclosure dimensions look less like the main source of representational insufficiency.

#### Step 1. Residual clustering

Collect turns where:

- oracle behavior differs most from projected behavior

Cluster by:

- scene
- phase
- relation values
- oracle behavior pattern

#### Step 2. Behavioral mismatch types

Label major mismatch families, such as:

- too much clarify-followup
- too much affective-followup
- too much initiative
- wrong support mode
- wrong expansion despite reasonable warmth

#### Step 3. Candidate latent-factor proposals

Propose alternative relation factors that might explain these mismatches.

#### Step 4. Test redesigned relation space

Build a small candidate relation redesign and see whether:

- a pure projector over the redesigned relation space
- closes more gap than conditioned projector baselines

### Success criterion

This line is supported if:

- a redesigned relation space materially reduces the need for scene/phase conditioning

### Failure criterion

This line weakens if:

- redesigned relation spaces do not improve projection,
- while conditioned projectors do

## Recommended execution order

### Phase 0

Run a supervised fit from:

- `oracle_rel_effective`
- to `oracle_behavior_effective`

before introducing `scene/phase`.

This fit does not prove that the current relation space is correct, but it gives a cleaner upper bound on how much of oracle behavior can be explained by the current relation variables alone.

Recommended order inside Phase 0:

1. fit a 4D baseline using the current relation dimensions
2. test stronger pure-relation function classes on the same 4D input
3. only then ask whether external conditioning variables are needed

This ordering prevents `scene/phase` from being promoted too early when the current relation space has not yet been given a fair best-fit baseline.

### Phase 1

Run Line A first:

- pure relation projector redesign

### Updated note after first supervised-fit baseline

The 4D supervised fit baseline now shows:

- linear LOOCV overall MAE: `0.0254`
- poly2 LOOCV overall MAE: `0.0219`

This means the current 4D relation space is not obviously too weak to explain oracle behavior.

Therefore, after the initial reverse-analysis pass, the practical order should now be interpreted as:

1. best-fit baseline over the current 4D relation space
2. improved projector family / projector parameterization
3. only then:
   - conditioned projector necessity tests
   - or more aggressive relation redesign

### Updated note after unrestricted-capacity comparison

We also compared higher-capacity fit families:

- `mlp_h4`
- `mlp_h8`
- `mlp_h12`

Current LOOCV results:

- `linear = 0.0254`
- `poly2 = 0.0219`
- `mlp_h4 = 0.0249`
- `mlp_h8 = 0.0269`
- `mlp_h12 = 0.0269`

Interpretation:

- simply increasing hidden capacity does not beat the stronger explicit 4D baseline;
- therefore the immediate next step should not be arbitrary capacity growth;
- instead, the best current target is to operationalize the better fitted 4D mapping as a deployable projector baseline.

### Phase 2

Only after A has credible attempts, run Line B:

- conditioned projector necessity test

### Phase 3

Run Line C as the interpretive follow-up:

- relation redesign / reverse analysis

This order preserves the stronger research claim for as long as the data supports it.

## Decision table

### Outcome 1

- pure relation projector closes most of the gap

Interpretation:

- explicit relation state remains a strong explanatory substrate
- `scene/phase` are not necessary main inputs

### Outcome 2

- pure relation projector helps, but conditioned projector clearly helps more

Interpretation:

- `scene/phase` may carry necessary extra information
- but relation state still matters

### Outcome 3

- conditioned projector wins strongly
- redesigned relation space fails to absorb the difference

Interpretation:

- external conditioning is likely necessary

### Outcome 4

- redesigned relation space reduces most of the apparent scene/phase benefit

Interpretation:

- current failure was mainly due to poor relation representation, not mandatory external conditioning

## Current immediate recommendation

The next concrete step should be:

1. implement at least one serious pure-relation projector redesign
2. compare it to the current best `oracle_state_i7`
3. only then move to conditioned projector variants
