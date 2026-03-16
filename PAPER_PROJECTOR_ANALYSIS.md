# Projector Analysis: `project_behavior(...)` vs Oracle Behavior

## Goal

This note analyzes the current deterministic projector:

- [projector.py](d:/My%20Project/companion-ai/app/relational/projector.py)

against the oracle behavior targets defined in:

- [paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json)

The purpose is to understand why:

- `explicit_rel_state_projected_oracle_state_i7`

performed substantially worse than both:

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`

and to propose a more realistic Stage-2 projector redesign.

---

## 1. Diagnostic Context

The key Stage-2 gap-splitting result is:

- `real i7`: `59.28`
- `oracle_state_i7`: `116.72`
- `oracle_behavior_i7`: `28.94`
- `oracle_i7`: `37.22`

Interpretation:

- supplying oracle relation state alone does **not** help;
- supplying oracle behavior control helps a lot;
- therefore the dominant current bottleneck is the deterministic
  `relation -> behavior` projector.

---

## 2. Current Projector Structure

The current projector uses four relational variables:

- `bond`
- `care`
- `trust`
- `stability`

to deterministically generate eight behavior variables:

- `E`
- `Q_clarify`
- `Directness`
- `T_w`
- `Q_aff`
- `Initiative`
- `Disclosure_Content`
- `Disclosure_Style`

The current formulas are mostly:

- linear,
- positively biased,
- and only weakly constrained by context.

In particular, the projector currently treats moderate increases in:

- `bond`
- `care`
- `trust`

as justification for broad simultaneous increases in:

- response expansion,
- follow-up tendency,
- affective pursuit,
- initiative,
- disclosure.

This appears to be too aggressive for the long-horizon companion cases used in this paper.

---

## 3. Empirical Bias Against Oracle Targets

Using the oracle relational states in
[paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json),
the current projector systematically overshoots the oracle behavior targets.

Average `predicted - oracle` across all phases:

- `E`: `+0.2372`
- `Q_clarify`: `+0.3078`
- `Directness`: `+0.0499`
- `T_w`: `+0.0334`
- `Q_aff`: `+0.2417`
- `Initiative`: `+0.2601`
- `Disclosure_Content`: `+0.3064`
- `Disclosure_Style`: `+0.2579`

### 3.1 Main pattern

The projector is not merely a little too warm. It is systematically too:

- expansive,
- inquisitive,
- affectively probing,
- proactive,
- disclosive.

The strongest overestimation is concentrated in:

- `Q_clarify`
- `Disclosure_Content`
- `Initiative`
- `Disclosure_Style`
- `Q_aff`
- `E`

By contrast:

- `Directness`
- `T_w`

are only mildly biased.

This means the current projector’s central failure is not “tone” in the narrow sense. It is the generation of an overly active interaction policy.

---

## 4. Why the Current Projector Over-Shoots

### 4.1 High positive floors

Several dimensions have nontrivial minimum baselines:

- `E = 0.15 + ...`
- `Q_clarify = 0.10 + ...`
- `Q_aff = 0.05 + ...`
- `Initiative = 0.10 + ...`
- `Disclosure_Content = 0.10 + ...`
- `Disclosure_Style = 0.10 + ...`

These floors are too high for a setting where:

- the relationship is modeled as a slow variable,
- many turns should remain conservative,
- continuation and probe phases should stay brief.

### 4.2 “Invest” is used too broadly

The latent variable:

- `invest = 0.35*bond + 0.35*care + 0.30*trust`

is currently reused to drive several behavior channels at once. This makes the projector act as if modest relational warmth implies:

- more expansion,
- more pursuit,
- more initiative,
- and more disclosure.

But the oracle behavior targets show that these dimensions should often stay low simultaneously, even when the relationship is not cold.

### 4.3 Stability is underused as a suppressor

`stability` currently affects:

- `Disclosure_Content`

but does not strongly suppress:

- `E`
- `Q_aff`
- `Initiative`
- `Q_clarify`

In the current experimental framing, this is a mismatch. High stability often means:

- do not escalate,
- do not expand,
- do not reopen relational negotiation.

### 4.4 `Q_clarify` is too relationally driven

The current projector makes `Q_clarify` mostly a function of:

- `trust`
- `invest`

This is too strong. In practice, clarify-followup should be driven much more by:

- task / information structure,
- whether user input is incomplete,
- whether clarification is actually required.

The oracle targets confirm that many companion turns should keep `Q_clarify` near zero, even when trust is not especially low.

### 4.5 Disclosure is massively over-permitted

Current formulas produce relatively high:

- `Disclosure_Content`
- `Disclosure_Style`

even for cases that the oracle targets clearly intend to keep minimal and non-self-expansive.

This is especially problematic because disclosure pressure tends to co-occur with:

- over-explanation,
- meta-talk,
- continuation inflation.

---

## 5. What the Oracle Behavior Targets Actually Imply

The oracle behavior targets across warm / vulnerability / cooling all point to a different design philosophy:

### 5.1 Most turns should be low-action by default

Default companion behavior should be:

- brief,
- low-followup,
- low-initiative,
- low-disclosure,
- gentle but not actively escalating.

### 5.2 Warmth is not the same as pursuit

The oracle targets allow cases where:

- `T_w` is moderate,

while:

- `Q_aff` is near zero,
- `Initiative` is near zero,
- `Disclosure_*` is near zero.

So warmth must not automatically imply relational push.

### 5.3 Clarification and affective follow-up should be conservative

Both:

- `Q_clarify`
- `Q_aff`

should usually remain near zero unless there is a very specific reason to raise them.

### 5.4 Disclosure should be exceptional, not default

The oracle targets treat disclosure as a rare controlled move, not a smooth byproduct of bond/care.

---

## 6. Proposed Projector Redesign

The redesign goal is not to make the projector more expressive. It is to make it:

- more conservative,
- more phase-compatible,
- more aligned with the oracle behavior philosophy,
- and more suitable for the `i7` execution interface.

### 6.1 Design Principles

1. Lower almost all positive floors.
2. Use `stability` as a stronger suppressor of:
   - expansion,
   - pursuit,
   - initiative,
   - disclosure.
3. Decouple warmth from pursuit.
4. Make `Q_clarify` depend much less on relation state alone.
5. Treat disclosure as opt-in / exceptional.

---

## 7. Proposed `project_behavior_v2` Logic

Below is a concrete Stage-2 redesign proposal.

### Shared latent quantities

```text
warm_core = 0.60 * care + 0.40 * bond
trust_core = trust
stability_core = stability
relational_push_permission = 0.50 * bond + 0.30 * care + 0.20 * trust
```

### 7.1 Expansion `E`

Current problem:
- much too high by default

Proposed:

```text
E = clamp01(0.03 + 0.20 * warm_core + 0.08 * trust_core - 0.10 * stability_core)
```

Scene adjustments:

- `task_focus` / `tech_help`: `+0.06`
- `user_vulnerable`: `-0.02`
- `leave_or_pause`: `-0.04`

Rationale:

- expansion should be low unless something explicitly licenses it
- high stability should suppress rambling continuation

### 7.2 Clarification `Q_clarify`

Current problem:
- too strongly driven by trust

Proposed:

```text
Q_clarify = clamp01(0.01 + 0.10 * trust_core)
```

Scene adjustments:

- `task_focus` / `tech_help`: `+0.18`
- otherwise cap at `0.12`

Rationale:

- relation alone should rarely create clarification demand

### 7.3 Directness `Directness`

Current projector is only mildly biased here, so this dimension needs the least change.

Proposed:

```text
Directness = clamp01(0.08 + 0.65 * trust_core - 0.05 * care)
```

Rationale:

- directness should come mostly from trust, not from generalized investment

### 7.4 Warmth `T_w`

Current projector is only slightly biased here, but should still be made less aggressive.

Proposed:

```text
T_w = clamp01(0.06 + 0.45 * care + 0.20 * bond - 0.04 * (1 - stability_core))
```

Rationale:

- keep warmth moderate
- do not let it rise automatically with trust or initiative

### 7.5 Affective follow-up `Q_aff`

Current problem:
- too high almost everywhere

Proposed:

```text
Q_aff = clamp01(0.00 + 0.16 * care + 0.08 * bond - 0.10 * stability_core)
```

Boundary / scene constraints:

- if cooling / pause / distancing / anti-care signal: force to `0`
- if vulnerability scene: cap at `0.10`

Rationale:

- affective pursuit should be rare and small

### 7.6 Initiative `Initiative`

Current problem:
- too high by default

Proposed:

```text
Initiative = clamp01(0.00 + 0.14 * relational_push_permission - 0.10 * stability_core)
```

Scene adjustments:

- `task_focus`: `+0.06`
- `leave_or_pause`: `-0.06`
- `user_vulnerable`: `-0.04`

Rationale:

- initiative should be mostly off unless explicitly supported

### 7.7 Disclosure content `Disclosure_Content`

Current problem:
- massively overestimated

Proposed:

```text
Disclosure_Content = clamp01(0.00 + 0.08 * warm_core + 0.08 * (1 - stability_core))
```

Scene adjustments:

- `relationship_addressing`: `+0.04`
- `leave_or_pause`: `+0.04`
- otherwise cap at `0.08`

Rationale:

- disclosure should be rare and scene-triggered, not a default relational byproduct

### 7.8 Disclosure style `Disclosure_Style`

Proposed:

```text
Disclosure_Style = clamp01(min(0.04 + 0.50 * Disclosure_Content, Disclosure_Content))
```

Rationale:

- style must not exceed content openness
- disclosure style should remain lower than current projector defaults

---

## 8. Expected Effects of the Redesign

If the redesign is correct, we should expect:

1. `oracle_state_i7` to move much closer to `oracle_behavior_i7`
2. lower inflation in:
   - `Q_clarify`
   - `Q_aff`
   - `Initiative`
   - `Disclosure_*`
3. `real i7` to move closer to `oracle i7`
4. less continuation over-expansion even before prompt-level hard constraints

---

## 9. Recommended Next Experiment

After implementing projector v2, rerun:

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_state_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

on:

- [paper_cases_oracle_state_exec_v1.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v1.json)

and compare:

- whether `oracle_state_i7` still underperforms `real i7`
- whether the gap to `oracle_behavior_i7` shrinks
- whether manual judge also reflects improved coherence

---

## 10. Current Bottom Line

The current evidence does **not** argue against two-layer control.

Instead, it argues for a more specific conclusion:

- the second layer is important;
- but the current deterministic projector is the wrong translator.

The immediate Stage-2 target is therefore:

- **not** to abandon projection,
- but to redesign projection so that it behaves more like the oracle behavior policy already implied by the experiments.
