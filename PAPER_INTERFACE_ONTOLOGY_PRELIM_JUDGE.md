# Interface Ontology Preliminary Judge

This note is a lightweight human-readable companion to the ontology ablation runs.
It does **not** replace the full judge package. Its purpose is to:

- record the current shortlist;
- give concrete sample comparisons that are worth reading closely;
- state the preliminary reasons behind the current working conclusion.

## Current shortlist

Keep for focused judge:

- `explicit_rel_state_projected_i7_pfitpoly2_sa_vA`
- `explicit_rel_state_projected_i7_pfitpoly2_sc_vA`
- `explicit_rel_state_projected_i7_pfitpoly2_sa_vC`
- `explicit_rel_state_projected_i7_pfitpoly2_sc_vC`
- `explicit_rel_state_rel_to_interface_i7_sa_vA`
- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_rel_to_interface_i7_sa_vC`
- `explicit_rel_state_rel_to_interface_i7_sc_vC`
- `explicit_rel_state_projected_oracle_i7`

Deprioritize for now:

- all `vB`
- all `sb`

Reason:

- `vB` did not show a reliable upside in either main deploy proxy or bridge sanity;
- `sb` tends to induce more expansion and a more over-active interaction style.

## What the preliminary reading currently supports

1. The main deploy route is still `relation -> i7 direct`.
2. The current `i7` ontology (`vA`) remains the most stable ontology.
3. `vC` is still worth keeping as the only serious ontology alternative.
4. `sc` is the most promising framing variant, especially for bridge stability.
5. Length is no longer enough to decide between `vA` and `vC`; focused manual judge is required.

## Suggested joint reading cases

These are the best first cases to read collaboratively because they expose different failure modes.

### Case 1. `oracle_exec_warm_001`

Compare:

- `main_direct_sa_vA_vs_sa_vC`
- `main_direct_sc_vA_vs_sc_vC`

What to look for:

- whether `vC` becomes too explicit about permission / rules;
- whether `vA` feels more like one naturally continuing interaction;
- whether either side over-corrects after the user says "normal chat, not too serious".

Current preliminary read:

- `vA` feels more like a natural ongoing interaction;
- `vC` feels slightly more interface-like and explanatory in the middle turns.

### Case 2. `oracle_exec_vuln_001`

Compare:

- `main_direct_sa_vA_vs_sa_vC`
- `main_direct_sc_vA_vs_sc_vC`

What to look for:

- whether a more permission-oriented ontology avoids over-reading vulnerability;
- whether the answer becomes too cold or too explicitly regulated;
- whether continuation and final probe stay controlled.

Current preliminary read:

- `vC` is sometimes usefully more restrained;
- but `vA` still tends to preserve a more natural supportive trajectory.

### Case 3. `oracle_exec_cool_001`

Compare:

- `main_projected_sa_vA_vs_sa_vC`
- `main_projected_sc_vA_vs_sc_vC`

What to look for:

- whether cooling is respected without turning robotic;
- whether the system reopens intimacy or over-explains;
- whether `sc` helps reduce unnecessary reopening.

Current preliminary read:

- `sc` is helpful;
- `vA` still looks more stable than `vC` overall.

### Case 4. `oracle_exec_repair_002`

Compare:

- `main_direct_vs_projected_sa_vA`
- `main_direct_vs_projected_sc_vA`

What to look for:

- whether direct `relation -> i7` stays cleaner in boundary-repair situations;
- whether projected routes become too explanatory or too helpful;
- whether repair stays one coherent stance instead of becoming compensatory warmth.

Current preliminary read:

- direct route still looks more like the right deploy controller;
- projected route still has analytic value, but not the best deployment feel.

## Reading rule for collaborative judgement

When we jointly read these samples, do **not** ask:

- which answer is nicer,
- which answer is more helpful in the abstract,
- which answer is simply shorter.

Instead ask:

1. does this still feel like the same interactional trajectory?
2. does it preserve the user's requested level of closeness and seriousness?
3. does it over-read weak signals into warmth, follow-up, or relationship movement?
4. does continuation / final probe stay controlled?

## Files to use

The corresponding judge packs are:

- [interface_ontology_main_case_level_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_interface_ontology_main_judge_v1_out/interface_ontology_main_case_level_judge_inputs.json)
- [interface_ontology_main_pairwise_judge_inputs.json](d:/My%20Project/companion-ai/paper_eval_interface_ontology_main_judge_v1_out/interface_ontology_main_pairwise_judge_inputs.json)

These should be treated as the source of truth for exact turn text.

## Preliminary Win/Tie/Loss Summary

This section summarizes the current collaborative manual reading across:

- `oracle_exec_warm_001`
- `oracle_exec_vuln_001`
- `oracle_exec_cool_001`
- `oracle_exec_repair_002`

These are still preliminary manual reads rather than a full adjudicated table, but they are already strong enough to refine the project-level interpretation.

### A. Ontology comparison: `vA` vs `vC`

#### `warm_001`

- `main_direct_sa_vA_vs_sa_vC`: `vA` wins
- `main_direct_sc_vA_vs_sc_vC`: `vA` wins

Reason:

- `vA` better preserves companion-like presence and a thoughtful sense of being-with the user.
- `vC` is not incoherent by default, but often feels more rigid, more ordinary-LLM-like, and less relationally present.

#### `cool_001`

- `main_direct_sa_vA_vs_sa_vC`: `vA` wins
- `main_direct_sc_vA_vs_sc_vC`: `vA` wins

Reason:

- `vC` does not merely become more restrained in cooling situations; it can destabilize the interactional register.
- In this family, `vC` is more likely to produce abrupt shifts from distant/functional interaction into unexpectedly companion-like language.
- `vA` keeps the cooler trajectory more stable.

#### `vuln_001`

- `main_direct_sa_vA_vs_sa_vC`: `vC` wins
- `main_direct_sc_vA_vs_sc_vC`: roughly tie / slight `vC` edge

Reason:

- In vulnerability cases, `vC` can sound more tender and soft without automatically collapsing into over-reading.
- This is the strongest current evidence that `vC` is a real family-sensitive alternative rather than a uniformly worse ontology.

### Current ontology reading

- `vA` remains the best default deploy ontology across families.
- `vC` should not be treated as a failed alternative; it is better described as a vulnerability-sensitive ontology that can improve softness/tenderness in some cases.
- `vB` remains deprioritized for now because it has not shown comparable upside in either proxy or preliminary manual reading.

### B. Wording comparison: `sa` vs `sc`

#### Current read

- `sc` is more promising than `sa`.
- `sc` often preserves restraint while retaining more relationship presence than `sa`.
- `sa` is still a valid low-temperature baseline, but can become too dry.

Important correction:

- `sa_vA` should not be described as strongly tool-like.
- Its main weakness is lower temperature / weaker relationship presence, not projected-style explanatory tool behavior.
- In very cold settings, `sa_vA` can still be a reasonable reply style.

### C. Route comparison: `direct` vs `projected`

#### `warm_001`

- `projected` is more likely to drift into tool-like suggestions and ordinary-assistant behavior.

#### `cool_001`

- `main_direct_vs_projected_sa_vA`: direct wins
- `main_direct_vs_projected_sc_vA`: direct wins
- `main_direct_vs_projected_sa_vC`: direct wins
- `main_direct_vs_projected_sc_vC`: direct wins

Reason:

- The projected route is not merely longer; it is more likely to become explanatory, tool-like, or list-heavy.
- In cooling and repair-like situations this reads as less person-like and less naturally embedded in a continuing interaction trajectory.

#### `repair_002`

- `main_direct_vs_projected_sc_vA`: direct wins
- `main_direct_vs_projected_sa_vC`: direct wins
- `main_direct_vs_projected_sc_vC`: direct wins

Reason:

- Boundary-repair cases expose the projected route's core weakness very clearly:
  it often sounds like it is executing an interface or explaining how it will behave,
  rather than simply continuing the repaired interaction in a stable way.

### Current route reading

- `relation -> i7 direct` remains the strongest candidate for the main deploy route.
- `relation -> behavior(8D) -> i7` should still be retained, but primarily as the analytic bridge rather than the main deployment route.

### D. Real-vs-oracle gap

#### `repair_002`

- `main_direct_sa_vA_vs_oracle_i7`: oracle small win
- `main_direct_sc_vA_vs_oracle_i7`: tie / oracle slight edge

#### `vuln_001`

- `main_direct_sa_vA_vs_oracle_i7`: oracle small win
- `main_direct_sc_vA_vs_oracle_i7`: approximately tie

### Current real-vs-oracle reading

- `direct sc_vA` is currently the strongest real candidate.
- It is the closest current real route to `oracle_i7` in the collaborative reading so far.
- `direct sa_vA` remains a useful low-temperature baseline, but `sc_vA` better preserves companion-like presence without obvious instability.

## Working conclusion after collaborative reading

1. Main deploy route:
   - still `relation -> i7 direct`
2. Default deploy ontology:
   - still `vA`
3. Family-sensitive alternative:
   - keep `vC`, especially for vulnerability-like settings
4. Best current framing:
   - `sc`
5. Best current real candidate:
   - `explicit_rel_state_rel_to_interface_i7_sc_vA`
6. Analytic bridge:
   - keep `relation -> behavior(8D) -> i7`, but not as the main deploy route

## Minimal Focused Judge Table

This is the smallest paper-facing table we can currently defend from the collaborative reading.

| Question | Evidence summary | Current read |
|---|---|---|
| Default deploy route | `direct vs projected` across `warm / cool / repair`, plus prior frozen route judge | `direct` wins |
| Default deploy ontology | `vA vs vC` across `warm / cool / vuln` | `vA` is the best default ontology |
| Family-sensitive alternative | `vC` in `vuln_001` | `vC` remains worth keeping for vulnerability-like cases |
| Best framing | `sa vs sc` across manually read cases | `sc` is the strongest current framing |
| Best current real candidate | `direct sc_vA` vs `oracle_i7` in `vuln / repair` | `direct sc_vA` is closest current real route to oracle |
| Role of projected route | repeated `direct vs projected` manual reads | retain as analytic bridge, not main deploy route |

## Paper-facing frozen statement

At the current stage, the deploy ontology line can be frozen as:

- **main deploy route**: `relation -> i7 direct`
- **default deploy ontology**: `vA`
- **best current framing**: `sc`
- **best current real candidate**: `explicit_rel_state_rel_to_interface_i7_sc_vA`
- **family-sensitive alternative**: retain `vC` for vulnerability-like settings
- **analytic bridge**: retain `relation -> behavior(8D) -> i7`

This does not yet claim that `vA` is universally optimal across all interaction families. The stronger current claim is:

- `vA` is the best default chart;
- `vC` is the only ontology variant that shows real family-conditional upside;
- `projected` remains useful for explanation, but not for primary deployment.
