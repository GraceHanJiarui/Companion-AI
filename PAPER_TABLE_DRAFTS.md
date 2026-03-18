# Paper Table Drafts

This file collects the current paper-facing table skeletons so they can be filled
without rewriting the main draft structure.

## Table 0. Structure vs Interface Control Ablation

| Setting | Relational state source | Execution interface | Judge-facing role | Status |
| --- | --- | --- | --- | --- |
| `baseline_relational_instruction` | none / prose-only relational instruction | none | strong baseline | frozen |
| `baseline_relational_instruction_to_interface_i7_sc_vA` | baseline heuristic instruction labels | `i7` | tests interface-only gain without explicit relation chart | `v1` proxy complete |
| `explicit_rel_state_rel_to_interface_i7_sc_vA` | explicit relation chart | `i7` | tests explicit relation chart + deploy chart decomposition | frozen winner |

Interface-family reading:

- `i7` is the strongest deploy chart among the interface families we explicitly tested.
- `i6` acts as a merged-family comparison and looks over-merged / more rigid.
- `i8` acts as an add-one-field comparison and does not show a stable overall gain over `i7`.
- This supports a best-tested deploy-chart claim, not a minimality / necessity claim.

Focused supplement reading (`warm / vuln / cool`; `3` judge runs; pairwise winner agreement `0.5556`):

| Pairwise comparison | Result | Conservative reading |
| --- | --- | --- |
| `oracle_i6` vs `oracle_i7` | mixed, with `i6` winning more often overall (`6/9` vs `3/9`) but low agreement | `i6` remains a competitive lower-variance / stronger-clamp alternative; this is not stable enough to overturn `i7` as the best-tested default |
| `oracle_i7` vs `oracle_i8` | near tie (`5/9` for `i7`, `4/9` for `i8`) with low agreement | adding one extra field does not produce a stable overall gain |

Interpretation boundary:

- useful as a reviewer-facing supplement on merge/add-one questions
- not strong enough to support a claim that `i7` is minimal
- not strong enough to replace the paper's main frozen-final evidence

Current `v1` proxy summary:

| Setting | Avg reply length | Current reading |
| --- | --- | --- |
| `baseline_relational_instruction` | `98.17` | strong baseline but strongly over-expanded |
| `baseline_relational_instruction_to_interface_i7_sc_vA` | `41.33` | large gain attributable to `i7` interface alone |
| `explicit_rel_state_rel_to_interface_i7_sc_vA` | `16.50` | additional gain beyond interface-only route |
| `explicit_rel_state_projected_oracle_i7` | `25.50` | oracle-side deploy reference |

Focused multi-judge reading (`warm / vuln / cool`; `3` judge runs; pairwise winner agreement `0.7778`):

| Pairwise comparison | Result | Interpretation |
| --- | --- | --- |
| baseline vs baseline `-> i7` | `9/9` pairwise wins for `baseline -> i7` | `i7` interface itself removes a large amount of over-expansion and continuation inflation |
| baseline `-> i7` vs explicit `relation -> i7` | `6/9` pairwise wins for explicit `relation -> i7`, `3/9` for `baseline -> i7` | explicit relation chart adds moderate trajectory-level stabilization beyond interface-only control |
| baseline vs explicit `relation -> i7` | `8/9` pairwise wins for explicit `relation -> i7` | combined interface + decomposition gain is real |
| explicit `relation -> i7` vs oracle `i7` | near tie: `5/9` wins for explicit `relation -> i7`, `4/9` for oracle | current real deploy controller is already close to oracle on trajectory structure |

Intended use:

- isolate whether the main gain comes from `i7` as an interface or from explicit relation-chart decomposition plus `i7`
- current `v1` proxy already shows that both matter:
  - `i7` itself explains a large share of the gain
  - explicit relation chart still adds further control beyond interface-only `i7`
- focused multi-judge now supports the same mixed reading

## Table 1. Frozen Main Comparison

| Case family | Strong baseline coherence | Direct `relation -> i7` coherence | Oracle `i7` coherence | Direct vs Baseline | Oracle vs Baseline | Oracle vs Direct | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| warm | TBD | TBD | TBD | `3/3` judge wins for direct `relation -> i7` | `3/3` judge wins for oracle `i7` | tie / slight oracle edge | direct route remains cleaner in relational continuity |
| vulnerability | TBD | TBD | TBD | `3/3` judge wins for direct `relation -> i7` | `3/3` judge wins for oracle `i7` | slight oracle edge most likely | oracle edge tends to show most on vulnerability-style cases |
| cooling | TBD | TBD | TBD | `3/3` judge wins for direct `relation -> i7` | `3/3` judge wins for oracle `i7` | tie / slight oracle edge | direct route remains preferred deploy chart |
| mixed_signal | TBD | TBD | TBD | `3/3` judge wins for direct `relation -> i7` | `3/3` judge wins for oracle `i7` | tie / slight oracle edge | mixed-signal family remains supportive of frozen deploy result |
| boundary_repair | TBD | TBD | TBD | `3/3` judge wins for direct `relation -> i7` | `3/3` judge wins for oracle `i7` | tie / slight oracle edge | direct route remains less tool-like than projected alternatives |

Global summary row:

| Global summary | `94.18` avg chars | `31.18` avg chars | `37.45` avg chars | `15/15` pairwise wins for direct vs baseline | `15/15` pairwise wins for oracle vs baseline | `13/15` pairwise wins for oracle vs direct | source: `paper_eval_frozen_main_v3_out/global_summary.json` + frozen-final multi-judge (`avg_winner_agreement = 0.9111`) |

Intended use:

- main paper result table
- judge-first evidence for the frozen deploy route

## Table 2. Bridge Sanity

| Case family | Oracle-state bridge coherence | Oracle-behavior coherence | Oracle full coherence | State vs Behavior | State vs Oracle | Behavior vs Oracle | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| warm | TBD | TBD | TBD | tie (frozen bridge judge summary) | tie / slight oracle edge | tie / slight oracle edge | corrected bridge remains near oracle |
| vulnerability | TBD | TBD | TBD | tie (frozen bridge judge summary) | tie / slight oracle edge | tie / slight oracle edge | oracle edge is most likely here |
| cooling | TBD | TBD | TBD | tie (frozen bridge judge summary) | tie / slight oracle edge | tie / slight oracle edge | bridge remains analytically viable |
| mixed_signal | TBD | TBD | TBD | tie (frozen bridge judge summary) | tie / slight oracle edge | tie / slight oracle edge | no evidence of bridge collapse |
| boundary_repair | TBD | TBD | TBD | tie (frozen bridge judge summary) | tie / slight oracle edge | tie / slight oracle edge | supports keeping 8D bridge |

Global summary row:

| Global summary | `36.91` avg chars | `39.21` avg chars | `36.30` avg chars | effectively tie | mostly tie / small oracle edge | mostly tie / small oracle edge | source: `paper_eval_frozen_bridge_v3_out/global_summary.json` + frozen bridge judge summary |

Intended use:

- main paper bridge table
- justify keeping `relation -> behavior(8D) -> i7` as analytic bridge

## Table 3. Deploy Ontology / Framing Freeze

| Case family | `vA+sa` | `vA+sc` | `vC+sa` | `vC+sc` | Winner / Tie | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| warm | present, warmer, more companion-like | strongest among `sc` pair | more rigid / ordinary-LLM-like | more restrained but less relationally present | `vA` wins | `vA` better preserves companion-like presence |
| vulnerability | somewhat dry | stronger than `sa_vA` | soft / tender | tie or slight edge over `vA+sc` | `vC` family-sensitive edge | strongest evidence for `vC` as vulnerability-sensitive alternative |
| cooling | stable low-temperature baseline | stable with slightly better presence | can destabilize register | more restrained but weaker relationship presence | `vA` wins | `vC` can jump interactional register in cooling |
| repair | direct route preferred | strongest current real candidate | more regulation-like | too interface-shaped at times | `vA+sc` wins | repair exposes projected/tool-like failure modes clearly |

Global summary row:

| Global summary | `21.69` avg chars | `23.51` avg chars | `22.31` avg chars | `22.61` avg chars | default winner = `vA+sc`; keep `vC` as vulnerability-sensitive alternative | source: `paper_eval_interface_ontology_main_v1_out/global_summary.json` + preliminary collaborative judge |

Intended use:

- main paper ontology/framing result
- communicate that `vA` is default, `sc` is best framing, and `vC` is family-sensitive

## Table 4. Aggregate Pairwise Summary

| Comparison | Wins | Ties | Losses | Notes |
| --- | --- | --- | --- | --- |
| Direct `i7` vs Baseline | `15` | `0` | `0` | frozen-final multi-judge summary |
| Oracle `i7` vs Baseline | `15` | `0` | `0` | frozen-final multi-judge summary |
| Oracle `i7` vs Direct `i7` | `13` oracle wins | `0` | `2` oracle losses | modest but consistent oracle edge in frozen-final multi-judge summary |
| Oracle-state bridge vs Oracle-behavior | prelim: ~0 decisive wins | prelim: majority ties | prelim: ~0 decisive losses | frozen bridge summary says effectively tie |
| Oracle-state bridge vs Oracle full | prelim: small oracle edge | prelim: majority ties | prelim: small oracle edge | vulnerability-style cases show the clearest oracle edge |
| Oracle-behavior vs Oracle full | prelim: small oracle edge | prelim: many ties | prelim: small oracle edge | bridge remains near-oracle rather than collapsing |

Intended use:

- compact result table or appendix table
- fast summary of pairwise judge outcomes

## Table 5. Secondary Diagnostics

| Route / Mode | Mean reply length | Variance / spread | Known failure tendency | Notes |
| --- | --- | --- | --- | --- |
| Strong baseline | `94.18` avg chars | TBD | continuation inflation / over-expansion | strong baseline remains competitive despite this tendency |
| Direct `relation -> i7` | `31.18` avg chars | TBD | can become too dry in some cooling / repair cases | best current deploy route |
| Oracle `i7` | `37.45` avg chars | TBD | slight oracle edge on vulnerability-style subtlety | strongest deploy-side upper bound in current paper |
| Corrected bridge (`oracle_state_i7_pfitpoly2`) | `36.91` avg chars | TBD | bridge not ideal as deploy route, but no broad collapse | keep as analytic bridge, not primary deploy controller |

Intended use:

- secondary table only
- do not let this table carry the main claim

## Appendix Table B. Semi-Formal Coherence Diagnostics

| Metric | Type | Current role | Interpretation |
| --- | --- | --- | --- |
| `length_spike` | automatic heuristic | secondary | continuation / probe over-expansion |
| `warmth_jump` | automatic heuristic | secondary | abrupt local warmth change |
| `unexpected_polarity_flip` | automatic heuristic | secondary | unsupported move between warmth-leaning and distance-leaning stance |
| `unsupported_initiative_jump` | automatic heuristic | secondary | rising initiative after cooling / boundary cue |
| `abrupt_shift_proxy` | aggregate heuristic | secondary | heuristic flag for possible trajectory break |

Intended use:

- appendix only
- supports operationalization of abrupt shift without replacing judge-centered coherence


- appendix or late discussion support
- should not be presented as the primary empirical table
