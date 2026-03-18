# 4D Fitted Model Parameter Interpretation

## Scope

This note interprets the current best explicit fitted mapping:

- `4D relation -> 8D behavior`
- model family: `poly2`

using the artifacts in:

- [paper_relation_behavior_fit_v2.json](d:/My%20Project/companion-ai/paper_relation_behavior_fit_v2.json)

This interpretation is meant to explain the current **analytic bridge**, not to claim that we have recovered the true human theory of relationships.

## What can and cannot be claimed

### What this interpretation can support

- which relation factors are most influential for each behavior dimension in the current fitted bridge
- which effects look monotonic and which are interaction-driven
- which parts of the mapping look intuitive versus model-specific

### What it cannot support

- that these coefficients are universal across all models
- that these coefficients describe human-human relationship dynamics directly
- that every coefficient should be read independently without considering feature interactions

## Feature meanings

Base relation variables:

- `bond`
- `care`
- `trust`
- `stability`

Engineered interaction features:

- `bond_care = bond * care`
- `bond_trust = bond * trust`
- `care_trust = care * trust`
- `trust_stability = trust * stability`
- `care_stability = care * stability`
- `fragility = 1 - stability`
- `warm_core = 0.6 * care + 0.4 * bond`
- `permission_core = 0.45 * trust + 0.35 * bond + 0.20 * care`
- squared terms for each base dimension

Important caution:

- the fitted model is genuinely interaction-heavy;
- therefore a single positive or negative coefficient should not be read in isolation.

## Overall fit signal

Current `poly2` performance:

- train overall MAE: `0.0089`
- LOOCV overall MAE: `0.0219`

LOOCV by behavior dimension:

- `Q_aff`: `0.0164`
- `Initiative`: `0.0134`
- `Q_clarify`: `0.0182`
- `T_w`: `0.0270`
- `E`: `0.0444`
- `Directness`: `0.0417`

Interpretation:

- the bridge is strongest on:
  - `Q_aff`
  - `Initiative`
  - `Q_clarify`
  - disclosure dimensions
- it is weaker on:
  - `E`
  - `Directness`

So the current 4D relation space appears to explain follow-up style and initiative better than it explains response scope and directness.

## Dimension-by-dimension interpretation

### 1. `E` (reply expansion / scope)

Most visible structure:

- large positive `care`, `trust`, `trust_stability`
- large negative `care_trust`, `care_stability`, `stability_sq`, `fragility`

Reading:

- expansion is not simply "more closeness means longer reply"
- instead it behaves like a **bounded permission signal**
- some care and trust can open room for expansion
- but once the relationship looks too settled, too fused, or too stabilized, expansion is suppressed again

Most plausible interpretation:

- the fitted model treats `E` as something like:
  - "allowed room to elaborate"
  - not "the warmer the relationship, the longer the answer"

This is important because it is less naive than the earlier hand-designed projector.

### 2. `Q_clarify`

Most visible structure:

- strong positive `trust`
- strong positive `bond_care`
- strong positive `permission_core`
- strong negative `bond_trust`
- strong negative `trust_stability`
- negative `care_stability`

Reading:

- clarify-followup seems to require a form of **permission to continue the exchange**
- not merely warmth
- trust helps, but high trust combined with high stability suppresses clarification

Most plausible interpretation:

- the system seems to read clarify-followup as:
  - acceptable when the relationship invites continued interaction
  - less appropriate once the interaction is already settled and should not be reopened

This matches the project's empirical observation that continuation-phase over-questioning is risky.

### 3. `Directness`

Most visible structure:

- strong negative `bond`
- strong positive `trust`
- strong positive `bond_trust`
- strong positive `trust_stability`
- strong negative `care_trust`
- strong negative `bond_sq`, `trust_sq`, `stability_sq` after saturation terms are considered jointly

Reading:

- directness is the hardest dimension to summarize simply
- the fitted model seems to use directness as a **trust-conditioned precision signal**
- high trust can support directness
- but high bond without the right trust/stability pattern does not

Most plausible interpretation:

- the model does not equate closeness with bluntness
- it equates some forms of trusted, stable interaction with being able to speak more plainly

### 4. `T_w` (warmth)

Most visible structure:

- positive `bond`, `care`, `bond_care`, `care_trust`, `warm_core`
- negative `bond_trust`, `care_stability`

Reading:

- warmth is the most intuitively human-readable dimension
- it is driven by a core of:
  - care
  - bond
  - and some care-trust interaction
- but warmth is suppressed when the interaction becomes too stabilized or too trust-heavy in a way that would risk over-reading the relationship

Most plausible interpretation:

- warmth is modeled as:
  - "allowed softening"
  - not "always turn up warmth when the relationship improves"

### 5. `Q_aff`

Most visible structure:

- positive `trust`
- positive `bond`
- strong positive `bond_care`
- strong positive `care_trust`
- strong positive `permission_core`
- strong negative `trust_stability`

Reading:

- affective follow-up is not mainly a pure care signal
- it behaves more like a **permission-sensitive emotional check-in**

Most plausible interpretation:

- the fitted bridge treats emotional follow-up as appropriate when:
  - there is enough trust/bond to permit it
  - but not when the situation is already stabilized enough that extra affect would become intrusive

This aligns with the later empirical finding that vulnerability continuation turns are especially sensitive.

### 6. `Initiative`

Most visible structure:

- strong positive `trust`
- positive `bond_care`
- positive `permission_core`
- negative `trust_stability`
- negative `care_stability`
- negative `fragility`

Reading:

- initiative looks very similar to `Q_aff` and `Q_clarify` in structure
- this suggests the current 4D relation space is mostly using one latent idea:
  - **permission to continue / permission to move**

Most plausible interpretation:

- initiative is allowed when the interaction has enough permission signal
- but should be suppressed in already-stabilized states

This is one reason the fitted bridge appears more plausible than the old hand-written projector, which tended to make initiative rise too globally.

### 7. `Disclosure_Content` and `Disclosure_Style`

Most visible structure:

- moderate positive `stability`
- positive `care_trust`
- negative `trust_stability`
- negative `care_stability`
- mild positive `warm_core` and `permission_core`

Reading:

- disclosure remains a small, conservative dimension
- it is not the main driver of the fitted bridge

Most plausible interpretation:

- the current relation space treats disclosure as a weak side effect of safe interaction, not as a major control axis

This matches earlier reverse-analysis evidence that disclosure was not the main unexplained gap.

## Cross-dimension reading

A broader pattern emerges across `Q_clarify`, `Q_aff`, and `Initiative`:

- the fitted bridge repeatedly builds around something like:
  - **permission / receptivity / allowed continuation**

using:

- `trust`
- `bond_care`
- `permission_core`
- and suppression from `trust_stability` or `care_stability`

This is probably the most important human-readable insight in the current fitted model:

> The fitted bridge does not behave as if stronger relationship always means more warmth, more questions, and more initiative.  
> It behaves as if relationship state determines whether continued movement is permitted.

That is a much stronger and more plausible interpretation of the current 4D bridge than the early hand-designed projector.

## What looks human-intuitive

The following patterns look relatively intuitive:

- warmth is driven by care/bond rather than trust alone
- initiative and affective follow-up require something like permission
- stabilization suppresses over-movement
- disclosure remains secondary

## What looks model-specific or less intuitive

The following patterns should be treated cautiously:

- the exact signs and magnitudes on `Directness`
- strong cancellation between first-order and squared terms
- some of the trust/bond interaction behavior in `Q_clarify`

These may reflect:

- small-sample fitting
- current oracle labeling style
- or genuine quirks of the present model/controller setup

## Paper-usable interpretation

The safest high-level interpretation for the paper is:

1. The current 4D relation representation is not merely fitting naive "more closeness -> more warmth -> more expansion" behavior.
2. Instead, the fitted bridge suggests a more structured picture:
   - `bond/care` mostly govern warmth,
   - `trust` and interaction terms govern permission to continue,
   - `stability` suppresses over-expansion and over-pursuit.
3. This makes the 4D analytic bridge interpretable enough to support the paper's mechanism story, even though it should not yet be claimed as a universal theory of relationship dynamics.
