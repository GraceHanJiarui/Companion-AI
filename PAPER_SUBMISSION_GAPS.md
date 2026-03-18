# Submission Gaps

This file records the main issues that still need to be resolved before the current draft can be treated as submission-ready.

## G1. Two-layer causal attribution is not yet isolated

Current paper claim at risk:

- improvement comes from the `two-layer` structure itself

Why the current evidence is insufficient:

- the strongest current result is `relation -> i7 direct`
- this shows that the `i7` deploy chart is effective
- but it does **not** by itself prove that the gain comes from the existence of a two-layer structure rather than from `i7` simply being a better prompt interface

What is currently missing:

- a baseline-to-`i7` control experiment without explicit relational state
- i.e. an experiment where the system gets an `i7`-style interface or equivalent execution chart without the full explicit relation-state machinery

Implementation status:

- the route has now been implemented as `baseline_relational_instruction_to_interface`
- what remains is to run and report the comparison against:
  - `baseline_relational_instruction`
  - `baseline_relational_instruction_to_interface_i7_sc_vA`
  - `explicit_rel_state_rel_to_interface_i7_sc_vA`

Current safest paper stance:

- the paper can claim that explicit relational control plus a deployable execution chart produces the strongest current result
- the paper should **not** yet claim that the gain has been causally isolated to "two-layer structure itself"

Required follow-up for a stronger submission:

1. add a `baseline -> i7` or comparable no-relational-state `i7` control
2. compare:
   - strong baseline
   - strong baseline + `i7`-style interface
   - explicit `relation -> i7`
3. only then argue more strongly about what part of the gain is due to structure vs interface wording

Important theory boundary:

- even if a richer one-layer manifold can in principle absorb a multi-chart decomposition, that does **not** make the present decomposition useless
- the paper's strongest current defense of the layered controller is practical rather than ontological:
  - modularity
  - diagnosability
  - deployability
  - bridge inspection

Current update after `v1` proxy:

- the missing route has now been run on `paper_cases_oracle_exec_v1.json`
- first-pass result:
  - baseline = `98.17`
  - baseline `-> i7` = `41.33`
  - explicit `relation -> i7` = `16.50`

Interpretation:

- `i7` interface quality clearly explains a large share of the gain
- but explicit relation-chart decomposition still appears to add additional value beyond interface-only control
- therefore the correct current paper stance is:
  - the gain is partly interface-driven and partly decomposition-driven
  - not purely one or the other

Current update after focused judge read:

- `baseline -> i7` beats baseline across `warm / vuln / cool`
- `explicit relation -> i7` usually beats `baseline -> i7`
- `explicit relation -> i7` is already close to `oracle_i7`

Implication:

- the paper can now defend a mixed-attribution claim with better confidence
- but a larger paper-facing judge package would still strengthen the argument

## G2. Judge protocol is not yet formalized enough for a hard paper claim

Current paper claim at risk:

- "final conclusions rely on manual judge"

Why this is not yet strong enough:

- current manual reading is meaningful but still relatively informal
- the draft does not yet fully specify:
  - fixed judge prompt
  - exact temperature
  - number of samples per case
  - whether judging is blind
  - number of judges
  - inter-rater agreement

Required minimum upgrades:

1. fixed judge prompt in appendix
2. fixed judge temperature, preferably `0` or `0.2`
3. fixed number of samples per case, e.g. `3-5`
4. at least `2-3` independent judges
5. simple agreement reporting
   - raw agreement percentage is enough as a minimum
6. explicit statement of whether judges are blind to mode identity

Safest current paper stance:

- judge is currently the best endpoint signal available
- but the current draft should describe it as a frozen manual-evaluation package rather than as a fully formalized human-evaluation protocol

## G3. Relational coherence is still only partially operationalized

Current risk:

- "relational coherence" sounds central, but the operational definition is still partly qualitative

What exists already:

- trajectory continuity
- user-request preservation
- overinterpretation
- continuation/probe control

What is still weak:

- no sharper quantitative operationalization of "abrupt shift"
- no threshold rule for when a trajectory break counts as a meaningful relational discontinuity

Safest current paper stance:

- keep coherence as a judge-centered evaluation construct
- do not pretend it is already a sharp quantitative metric

Possible strengthening path:

1. define an abrupt shift operationally as:
   - a judge-observed turn where relational stance changes in direction or magnitude beyond what the prior trajectory and current user signal support
2. tie it to:
   - unsupported warmth jump
   - unsupported distance increase
   - unsupported continuation reopening
3. report:
   - `has_abrupt_shift`
   - `abrupt_shift_turns`
   as secondary structured outputs

## G4. Geometry/native-latent line is weakly connected to the main empirical claim

Current risk:

- it is interesting but can look speculative
- it can be criticized as analyzing hand-defined charts talking to each other

Safest current paper stance:

- keep this line as a conservative late discussion or appendix result
- explicitly state that it is chart-structure analysis, not proof of internal ontology

Recommended paper treatment:

- do not let this line carry the main paper claim
- keep the main empirical story on:
  - strong baseline competitiveness
  - deploy-route freeze
  - bridge freeze
  - ontology/framing freeze

## Recommended pre-submission priority order

1. formalize judge protocol
2. add no-relational-state `i7`-style control ablation if feasible
3. sharpen wording around relational coherence and abrupt shift
4. keep geometry/native-latent line conservative and secondary
