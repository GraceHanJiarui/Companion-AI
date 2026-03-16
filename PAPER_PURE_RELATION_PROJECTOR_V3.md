# Pure Relation Projector v3

## Purpose

This note defines the first two serious `pure relation projector` candidates for the
next experiment round.

The design constraint is explicit:

- keep the two-layer architecture;
- keep a continuous `relation -> behavior` mapping;
- do **not** treat `scene` / `phase` as the default answer;
- test whether the current failure comes from a bad projector, rather than from
  the pure-relation hypothesis itself.

---

## Background

The latest gap experiments suggest:

- `oracle_behavior_i7 ~= oracle_i7`
- `oracle_state_i7 << oracle_behavior_i7`
- projector profile tuning (`balanced / conservative / sparse`) did not fix the issue

This points to a failure in the current deterministic projector, but it does **not**
yet prove that pure relation projection is impossible.

The next step is therefore to replace the current projector with better
continuous candidates before escalating to conditioned projector lines.

---

## Candidate A: `v3a`

### Design idea

`v3a` is a conservative, decoupled linear projector.

Its principles are:

- warmth should not imply pursuit;
- high stability should strongly suppress pursuit and expansion;
- disclosure should remain low and exceptional;
- clarification should remain weak in pure relation mapping.

### Main formulas

Latents:

- `warm_core = 0.55*care + 0.30*bond + 0.15*trust`
- `permission_core = 0.45*trust + 0.35*bond + 0.20*care`
- `fragility = 1 - stability`

Behavior:

- `E = 0.02 + 0.14*warm_core + 0.08*trust + 0.05*bond - 0.12*stability`
- `Q_clarify = 0.01 + 0.10*trust - 0.06*care - 0.04*bond + 0.02*fragility`
- `Directness = 0.10 + 0.55*trust - 0.08*care + 0.05*stability`
- `T_w = 0.06 + 0.42*care + 0.18*bond - 0.03*fragility`
- `Q_aff = 0.11*care + 0.05*bond - 0.10*stability`
- `Initiative = 0.10*permission_core - 0.12*stability`
- `Disclosure_Content = 0.06*bond*trust + 0.02*care - 0.04*stability + 0.02*fragility`
- `Disclosure_Style = min(0.02 + 0.40*Disclosure_Content, Disclosure_Content)`

### Hypothesis

`v3a` should reduce the systematic over-shoot seen in the old projector while
remaining faithful to the pure relation hypothesis.

---

## Candidate B: `v3b`

### Design idea

`v3b` is a nonlinear gated projector.

Its principles are:

- relation may influence behavior through multiplicative gates rather than broad additive bias;
- pursuit-like channels should activate only when multiple relational signals align;
- conservative caps should prevent runaway behavior even if relation values rise.

### Main formulas

Latents:

- `warm_gate = 0.50*care + 0.30*bond + 0.20*trust`
- `pursuit_gate = 0.55*trust*bond + 0.15*care - 0.30*stability`
- `support_gate = 0.45*care + 0.25*trust + 0.10*bond - 0.15*stability`

Behavior:

- `E = min(0.35, 0.02 + 0.18*warm_gate*trust + 0.06*bond - 0.08*stability + 0.03*fragility)`
- `Q_clarify = min(0.20, 0.01 + 0.16*trust*(1-care) + 0.03*fragility)`
- `Directness = 0.10 + 0.50*trust + 0.06*stability - 0.06*care`
- `T_w = 0.05 + 0.38*care + 0.20*bond - 0.02*fragility`
- `Q_aff = min(0.15, 0.22*care*bond + 0.04*care*trust - 0.08*stability)`
- `Initiative = min(0.16, 0.14*pursuit_gate + 0.03*trust - 0.08*stability)`
- `Disclosure_Content = min(0.12, 0.12*trust*bond + 0.02*care - 0.06*stability)`
- `Disclosure_Style = min(0.02 + 0.55*Disclosure_Content + 0.04*bond, Disclosure_Content)`

### Hypothesis

`v3b` tests whether the problem is not just over-aggressive coefficients but the
lack of nonlinear gating in the current projector family.

---

## What `v3a` vs `v3b` is meant to test

These two candidates are intentionally different.

- `v3a` tests whether a cleaner conservative linear mapping is enough.
- `v3b` tests whether pure relation projection needs nonlinear gating to remain plausible.

This keeps the research question focused:

- Is `behavior = f(relation)` still viable if `f` is redesigned more carefully?

---

## Recommended first comparison

Run:

- `explicit_rel_state_projected_i7_pv3a`
- `explicit_rel_state_projected_oracle_state_i7_pv3a`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

and:

- `explicit_rel_state_projected_i7_pv3b`
- `explicit_rel_state_projected_oracle_state_i7_pv3b`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

on:

- `paper_cases_oracle_state_exec_v1.json`

Key criterion:

- whether `oracle_state_i7_pv3a` or `oracle_state_i7_pv3b`
  moves substantially closer to
  `oracle_behavior_i7` / `oracle_i7`

If neither does, then the pure-relation route becomes much harder to defend
without relation redesign.

