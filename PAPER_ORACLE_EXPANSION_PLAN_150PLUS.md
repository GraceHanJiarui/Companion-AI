# Oracle Expansion Plan: 150+ Phase Points

## Goal

Expand the oracle evaluation substrate from the current:

- `5` oracle cases
- `30` phase points

to a scale that is more suitable for a paper-level frozen result.

## Target scale

Recommended target:

- **`24` oracle cases**
- `6` phases per case
- **`144` phase points**

Preferred stronger target:

- **`30` oracle cases**
- `6` phases per case
- **`180` phase points**

If overnight runtime is acceptable, the stronger target is better.

## Family design

Use the following 6 case families.

### 1. `warm`

Pattern:

- light positive signal
- user permits some warmth
- system must not over-upgrade the relationship

Target count:

- `4-5` cases

### 2. `vulnerability`

Pattern:

- user under stress
- wants presence more than active intervention
- system must not over-comfort or over-counsel

Target count:

- `4-5` cases

### 3. `cooling`

Pattern:

- user wants distance or lower involvement
- system must stay available without compensatory warmth

Target count:

- `4-5` cases

### 4. `mixed_signal`

Pattern:

- user gives partly positive and partly limiting cues
- system must not over-read one side and ignore the other

Target count:

- `4-5` cases

### 5. `ordinary_neutral`

Pattern:

- no strong relationship move
- mostly normal long-horizon companion maintenance
- system must avoid inventing intimacy

Target count:

- `4-5` cases

### 6. `boundary_repair`

Pattern:

- user corrects the system's tone, heat, or style
- system must calibrate without over-apology or over-compensation

Target count:

- `4-5` cases

## Recommended counts

### Practical strong target

- `6` families
- `4` cases per family
- `24` cases total
- `144` phase points

### Preferred final target

- `6` families
- `5` cases per family
- `30` cases total
- `180` phase points

## Priority order if writing cases in batches

If cases must still be created in waves, use this order:

1. `mixed_signal`
2. `vulnerability`
3. `boundary_repair`
4. `ordinary_neutral`
5. additional `warm`
6. additional `cooling`

Reason:

- the first three families are the most diagnostic for relational over-reading, over-support, and controller calibration;
- `warm` and `cooling` already have stronger initial coverage.

## Intended use after expansion

After expansion, rerun:

### Main frozen comparison

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7`
- `explicit_rel_state_projected_oracle_i7`

### Bridge sanity

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

### Repeated sampling subset

Do repeated sampling only on a focused subset:

- at least one case from each family
- especially:
  - `vulnerability`
  - `mixed_signal`
  - `boundary_repair`

## Why this scale matters

At the current `30` phase points, the frozen result is promising but still vulnerable to the criticism that:

- the cases are too hand-picked
- the family coverage is too narrow
- the result may be driven by a few especially favorable or unfavorable trajectories

Moving to `144-180` phase points does not fully solve external validity, but it materially improves:

- family coverage
- stability of pairwise judgments
- confidence in the frozen route decision

## Relation-dimension implication

This expansion is also a prerequisite for a stronger relation-dimension study.

If relation dimensionality is to be tested seriously, it should be tested on:

- a larger and more diverse oracle substrate,

not only on the original small set.

Therefore, the large expansion should come **before**:

- fewer/more relation dimensions
- redesigned relation bases
- more aggressive latent relation search
