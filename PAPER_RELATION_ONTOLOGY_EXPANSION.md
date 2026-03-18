# Relation Ontology Expansion

## Goal

The current 4D relation space now looks robust enough to keep, but not robust enough to declare final.

The next step is therefore not a blind latent-space search. It is a **new annotated ontology step**:

- propose a small number of genuinely new relation factors;
- relabel the expanded oracle substrate;
- test whether the richer ontology materially improves explanation.

This should be treated as a validation of ontology quality, not just another curve-fitting exercise.

## Why this is now justified

The current evidence supports three claims simultaneously:

1. the present 4D basis is stronger than all tested 2D/3D subsets on the 180-row oracle set;
2. the current fitted interpretation remains close to the original semantic design;
3. the current 5D/6D deterministic augmentations do not beat the raw 4D basis.

Together, these mean:

- the current 4D basis is not arbitrary;
- but its apparent semantic validity should still be stress-tested against a richer manually annotated ontology.

## What should count as a valid >4D ontology

The next ontology should **not** simply append deterministic transforms like:

- `permission = 0.45 * trust + 0.35 * bond + 0.20 * care`
- `warmth_affordance = 0.60 * care + 0.40 * bond`

Those are useful analysis aids, but they are not genuinely new relation dimensions.

A valid >4D ontology should add factors that are:

- semantically distinct from the current four labels;
- manually annotatable from the dialogue context;
- plausibly stable across multiple turns;
- not reducible to one linear combination of the existing four axes.

## Recommended ontology candidates

Two candidate directions are worth testing first.

### Candidate A: 5D functional ontology

Keep the current four axes and add:

- `interactional_permission`

Meaning:

- whether the user currently permits the system to continue moving the interaction forward;
- this includes permission for:
  - clarifying follow-up,
  - affective checking-in,
  - mild initiative,
  - slight relational movement.

Why this is worth testing:

- the fitted 4D bridge repeatedly behaves as if one hidden factor is “permission to continue”;
- adding it explicitly tests whether that factor deserves to become a first-class relation variable rather than staying distributed across `bond/care/trust`.

### Candidate B: 6D functional ontology

Keep the current four axes and add:

- `interactional_permission`
- `boundary_firmness`

Meaning of `boundary_firmness`:

- how strongly the user is currently marking a desired ceiling on warmth, care, or initiative;
- this is not identical to low bond/trust/care, because boundary-setting can coexist with trust or ongoing interaction.

Why this is worth testing:

- the current 4D interpretation treats `stability` as a brake;
- but some difficult cases, especially `boundary_repair` and some `mixed_signal` turns, look more like explicit boundary-calibration than mere stability.

## Alternative basis interpretation

Even if the project keeps the original variable names for continuity, the current fitted reading already suggests a more functional reinterpretation:

- `bond` -> interactional closeness
- `care` -> soft receptivity
- `trust` -> permission to continue
- `stability` -> anti-overshoot stabilizer

The ontology expansion should therefore test whether:

1. the original names still suffice if read functionally;
2. or whether some of those functions should become separate explicit factors.

## Annotation protocol

The ontology expansion should operate on the full 180-row oracle substrate.

Recommended annotation unit:

- one row per phase turn

For each row:

1. preserve the original 4D oracle relation labels
2. add one or two new fields depending on the candidate ontology
3. annotate them independently rather than deriving them from the old four labels

## Evaluation protocol

For each candidate ontology:

1. fit `relation -> behavior` on the full oracle set
2. compare against current raw4 on:
   - train MAE
   - LOOCV MAE
   - per-dimension MAE
3. only treat an ontology as materially better if:
   - it improves overall LOOCV;
   - and it improves the currently sensitive behavior dimensions, especially:
     - `Q_aff`
     - `Q_clarify`
     - `Initiative`
     - `E`

## What this experiment can and cannot show

What it can show:

- whether the current 4D ontology is already close to sufficient;
- whether one or two genuinely new relation factors improve explanatory power;
- whether the current functional interpretation deserves to become a revised ontology.

What it cannot show by itself:

- that any one ontology is universally correct across all models;
- that the resulting factors are human relationship theory;
- that annotation choices are free of researcher bias.

## Recommended next move

Start with two explicit relabeling passes on the same 180 rows:

1. `raw4 + interactional_permission`
2. `raw4 + interactional_permission + boundary_firmness`

This is the smallest ontology expansion that is:

- genuinely new,
- semantically motivated by the current results,
- and still feasible to annotate.
