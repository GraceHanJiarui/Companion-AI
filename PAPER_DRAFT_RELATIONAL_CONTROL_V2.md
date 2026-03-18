# Draft Paper V2: Relational Control Under Strong Baselines

## Title

**Relational Control Under Strong Baselines for Long-Horizon Companion Dialogue**

Alternative titles:

- **Deployable and Analytic Charts for Long-Horizon Companion Dialogue**
- **From Relational State to Executable Control in Long-Horizon Companion Dialogue**

## Abstract

Large language models can produce fluent companion-style dialogue, but maintaining a coherent sense of relationship over long-horizon interaction remains difficult when control relies only on prompt instructions. A natural systems hypothesis is to introduce explicit relational state as an intermediate control layer. However, whether such structured control actually improves language-level relational coherence, and what kind of control interface is actually executable for a general-purpose LLM, remains unclear. We study long-horizon companion dialogue through the lens of relational drift, abrupt relational shifts, and case-level coherence. We compare a strong prompt baseline, a single-layer relational-control formulation, and a two-layer formulation that maps relational state into explicit execution constraints before generation. In the present system, these layers do not play the same role: `4D relation` is the coarse relational-state chart used to record change over the interaction trajectory, while `i7` is the deploy chart used to turn the current relation state into a stable executable generation interface. We further introduce oracle and hybrid controls to separate state updating, relation-to-behavior mapping, interface construction, and final language realization. Our evidence supports four main claims. First, strong prompt baselines are genuinely competitive, so explicit control is not solving an easy benchmark. Second, direct deployable control through `relation -> i7` is the strongest current real controller, while a corrected `4D relation -> fitted 8D behavior -> i7` route remains valuable as an analytic bridge rather than the preferred deploy path. Third, a new structure-vs-interface ablation shows that the observed gain is mixed rather than single-cause: a large share comes from the executable `i7` interface itself, while explicit relation-chart decomposition still adds further trajectory-level stabilization beyond interface-only control. Fourth, within the deploy ontology line, the default `vA` ontology with `sc` framing is the best current real configuration, while `vC` is better treated as a vulnerability-sensitive alternative than as a new default ontology. Final conclusions are based on a multi-evidence evaluation package rather than length statistics alone: structured case-level judge labels, pairwise coherence comparisons, multi-judge agreement, and lightweight automatic diagnostics.

## 1. Introduction

Long-horizon companion dialogue is not just a sequence of locally helpful responses. It is also a process in which the system must maintain a stable, interpretable, and non-jumping sense of relationship over time. Prompt-only systems can often sound locally good while still exhibiting relational drift: they may become abruptly warmer, colder, more over-involved, or more distant than the interaction history supports.

A common engineering response is to introduce explicit intermediate state: track relationship variables, update them conservatively, and use them to shape downstream behavior. This idea is intuitively attractive, but intuition alone is insufficient. A structured control layer may be internally coherent yet fail to produce better language behavior, especially when realized through an unmodified general-purpose LLM. Strong prompt baselines may also already capture much of the visible gain.

This paper asks a focused question: **when relational control is made explicit, what kind of control interface is actually executable for long-horizon companion dialogue?** In particular, we study the contrast between:

- a **strong prompt baseline** that uses high-level relational instruction only;
- a **single-layer relational control** formulation that directly conditions generation on relational stance;
- a **chart-decomposed control** formulation that first represents relational stance and then projects it into explicit behavior-side constraints before generation.

Our results support a more nuanced conclusion than "explicit state helps" or "explicit state fails." Strong baselines are highly competitive. Single-layer control appears weaker than the current chart-decomposed controller. A well-designed decomposed interface shows clear promise in oracle form and retains part of that advantage in the real chain. Recent deployment fixes further show that oracle-space explanatory fit and deployable controller success must be distinguished, but are not necessarily disconnected: under a corrected fitted projector, `relation -> behavior -> i7` can remain close to oracle behavior while direct `relation -> i7` remains the stronger deploy route. A dedicated structure-vs-interface ablation further shows that the gain is mixed: executable interface quality explains a large share of the improvement, but explicit relation-chart decomposition still adds further trajectory-level stabilization beyond interface-only control. The remaining gap is therefore better understood as a control-route construction and structure-preservation problem than as a simple failure of explicit relational state. The right theoretical reading is a chart-decomposition claim, not a final ontological claim. In that reading, the coarse relation chart and the deploy chart are not competing alternatives: `4D relation` records trajectory-level change, while `i7` stabilizes turn-level execution.

### 1.1 Contributions

The current draft supports the following contributions:

1. We formulate long-horizon companion dialogue as a problem of relational coherence and abrupt relational shift rather than only local helpfulness.
2. We compare strong prompt baselines, single-layer relational control, and a chart-decomposed controller under the same long-horizon setting.
3. We show that strong prompt baselines remain highly competitive, making this a nontrivial control problem rather than a weak-baseline artifact.
4. We develop an oracle and hybrid diagnostic framework that separates relation-state quality, relation-to-behavior projection, deploy interface construction, and final language realization.
5. We identify a current best deployable controller: direct `relation -> i7`, with `vA` ontology and `sc` framing as the strongest current real configuration.
6. We show that good oracle-space fit does not automatically imply deployed control success, but that the gap can shrink substantially after correcting the fitted projector implementation.
7. We retain `relation -> behavior(8D) -> i7` as a strong analytic bridge rather than a failed intermediate layer.
8. We explicitly distinguish what the current evidence does and does not establish: the paper currently isolates a strong deploy route and a viable analytic bridge, but does not yet fully isolate how much of the observed gain is due to chart decomposition itself versus the strength of the final deploy interface.
9. We clarify the theoretical status of the current decomposition: even if a richer one-layer alternative may exist in principle, the empirical value of the present `raw4 / behavior_8d / i7` stack lies in modularity, diagnosability, and deployability rather than in a claim of ontological finality. Concretely, `raw4` is retained as the current coarse relation-state chart for recording interaction-trajectory change, while `i7` is retained as the current deploy chart for stable execution.

### 1.2 Scope

This paper is intentionally scoped as a focused mechanism paper, not a full product paper. It does not attempt to solve:

- relation-state representation design in full generality;
- why strong baselines may already encode implicit relational control;
- the full product-level question of controllability versus zero-shot language quality;
- human-human relationship modeling in general;
- model-internal ontology discovery.

Those are promising follow-on directions, but including them here would make the paper unstable and difficult to defend.

## 1.3 Related Work

This paper sits at the intersection of four neighboring lines of work.

First, it relates to controllable dialogue generation and structured response control [CITATION: controllable dialogue / controllable generation]. Prior work has shown that dialogue behavior can be shaped through explicit attributes, planning variables, or intermediate control signals. Our work differs in two ways. We focus on long-horizon companion dialogue rather than short single-turn style control, and we evaluate explicit control under a strong prompt baseline rather than a weak prompt-only foil.

Second, it connects to persona consistency and long-term dialogue [CITATION: persona consistency / long-term dialogue]. Much prior work studies consistency as maintaining a stable persona, biography, or profile. Our emphasis is different: we focus on maintaining a coherent **interactional relationship process** over time, including avoiding abrupt warm/cold jumps, continuation inflation, and unsupported relationship movement.

Third, it is adjacent to social-signal and partner-state modeling [CITATION: partner state / social signal / user state]. There is a natural overlap with work that tracks user state, engagement, affect, or conversational stance. The current paper is narrower. We do not claim to model human relationships in full generality. Instead, we study whether an explicit relational controller can improve long-horizon companion dialogue when the execution path is made concrete enough for a general-purpose LLM to follow.

Fourth, it is adjacent to broader work on LLM controllability and structured intermediate representations [CITATION: controllability / intermediate representations]. However, the present paper does not attempt model-internal ontology discovery and does not treat that line as part of its main empirical contribution.

## 2. Problem Setting

We study long-term companion-style dialogue, where the same system interacts with the same user across multiple turns and is expected to maintain relational continuity.

### 2.1 Relational Coherence

We treat relational coherence as a dialogue-level property: a multi-turn interaction should feel like one ongoing relationship process rather than a sequence of isolated, stylistically reset responses.

### 2.2 Abrupt Relational Shift

We define an abrupt relational shift not as any large change, but as a change that exceeds what is supported by the interaction history and current user signal. This includes:

- direction: whether the system moves warmer or cooler appropriately;
- magnitude: whether the change overshoots what the context supports;
- timing: whether the shift occurs without sufficient buildup.

### 2.3 Slow-Variable Assumption

Our explicit relational-state design assumes that relationship is a slow variable:

- per-turn `delta_R` should usually be small;
- many turns should naturally produce `delta_R = 0`;
- no strong relationship signal should mean no update by default.

This assumption is part of the paper's modeling hypothesis.

## 3. Method

### 3.1 Strong Prompt Baseline

Our strongest baseline, `baseline_relational_instruction`, does not maintain explicit relational state. Instead, it uses current context, lightweight heuristics, and limited memory cues to produce a natural-language instruction about the current relationship stance, then generates directly from that instruction.

This baseline is important because it is substantially stronger than a plain prompt-only system and often highly competitive in language-layer evaluation.

### 3.2 Single-Layer Relational Control

In the single-layer formulation, the system maintains explicit relational state and uses that state to condition generation directly through a natural-language relational summary.

Conceptually:

1. user input updates relational state;
2. relational state is summarized;
3. the summary conditions generation.

This formulation tests whether explicit relational stance alone is sufficient as a generation-time control interface.

### 3.3 Two-Layer Relational Control

In the two-layer formulation, relational state does not directly drive generation. Instead:

1. user input updates relational state;
2. relational state is projected into a behavior or execution interface;
3. generation is conditioned on both current relational stance and explicit execution constraints.

This second layer is intended to bridge the gap between high-level social position and low-level language behavior.

### 3.4 Execution Interfaces

We evaluated multiple execution-interface families during Stage 2. The current best-performing family is `i7`, which separates behavior-side control into executable fields rather than relying on a single prose summary.

The `i7` interface includes:

- `reply_scope`
- `clarify_followup`
- `affective_followup`
- `initiative_level`
- `warmth_level`
- `relational_push`
- `support_mode`

Prompt layout was later stabilized through:

- explicit layout separation between relational stance and expression constraints;
- phase-sensitive hard constraints, especially for ordinary continuation and final probe phases.

The paper's claim here should remain narrow. We do not claim that the present seven-field interface is minimal or necessary. The current interface-family evidence supports a weaker but still useful conclusion: among the deploy charts we actually tested, `i7` is the strongest current candidate. Earlier family comparisons suggest that too much merging degrades fidelity and naturalness, while simply adding another field does not automatically improve execution. A later focused supplement compared a merged-family variant (`i6`) and an add-one-field variant (`i8`) against `i7` on `warm / vuln / cool` oracle cases. That supplement did not support a stronger minimality claim: `i6` remained a competitive lower-variance alternative, `i8` failed to show a stable overall gain, and pairwise winner agreement remained modest. The value of the supplement is therefore boundary-setting rather than theorem-proving: it makes the best-tested-family claim more defensible without upgrading it into a necessity claim.

### 3.5 Oracle and Hybrid Controls

To separate mechanisms, we introduced oracle and hybrid modes:

- oracle relation plus oracle behavior control;
- oracle relation plus real behavior control;
- real relation plus oracle behavior control;
- oracle relation state values plus real projection mapping and real realization.

These variants allow us to ask where the remaining gap lives:

- in relation-state quality;
- in relation-to-behavior projection;
- in deploy-interface construction;
- or in final language realization.

## 4. Experimental Design

### 4.1 Research Questions

The paper centers on the following questions:

- **RQ1.** Is a chart-decomposed relational controller more promising than single-layer relational control for long-term companion dialogue?
- **RQ2.** Can a strong decomposed execution interface outperform a strong prompt baseline?
- **RQ3.** If the real-chain decomposed system does not reach oracle performance, where does the gap come from?
- **RQ4.** How should analytic charts and deployable charts be separated and bridged in a decomposed controller?

### 4.2 Case Sets

We used several case sets over the course of the study:

- short smoke cases for pipeline checks;
- long-range manually designed multi-phase cases;
- oracle long cases;
- oracle execution-interface cases.

The main expanded oracle execution family now includes:

- warming trajectories;
- vulnerability-with-correction trajectories;
- cooling trajectories;
- mixed-signal trajectories;
- ordinary-neutral trajectories;
- boundary-repair trajectories.

### 4.3 Evaluation Protocol

We use three main evaluation styles:

1. summary statistics:
   - average response length;
   - phase-level inflation;
   - continuation and probe over-expansion.
2. case-level judge:
   - relational coherence;
   - abrupt shift;
   - phase transition quality.
3. pairwise judge:
   - baseline vs explicit control;
   - single-layer vs chart-decomposed control;
   - real vs oracle;
   - direct vs projected route.

### 4.4 What Counts as Evidence

This paper does not treat response length as a standalone objective. Lower length is interpreted only as a coarse diagnostic proxy when it aligns with:

- lower over-expansion;
- less compensatory warmth;
- fewer unnecessary follow-ups;
- cleaner adherence to relationship continuity.

Final conclusions rely on:

- manual judge;
- pairwise comparison;
- repeated sampling;
- hybrid diagnostics.

At the same time, the current draft should be read honestly: the judge package is already central to the paper's conclusions, but the full submission-standard protocol still needs stronger formalization in the final version, including fixed prompt wording, fixed decoding settings, and multi-judge agreement reporting. The frozen appendix-ready protocol is provided in `PAPER_JUDGE_PROTOCOL_APPENDIX.md`. A semi-formal operationalization layer and automatic secondary diagnostics are summarized in `PAPER_RELATIONAL_COHERENCE_OPERATIONALIZATION.md`.

### 4.5 Judge Protocol

The final paper should be read through judge-based relational evaluation rather than proxy statistics alone. The fixed case-level and pairwise prompts, together with decoding and agreement-reporting requirements, are frozen in `PAPER_JUDGE_PROTOCOL_APPENDIX.md`.

We use two judge formats.

First, a **case-level coherence judge** evaluates complete multi-turn trajectories. The main dimensions are:

- `trajectory_continuity`
- `user-request-preservation`
- `overinterpretation`
- `continuation_probe_control`

These dimensions are used to support an overall coherence judgment rather than to replace it. In addition, the case-level judge emits structured failure labels:

- unsupported warmth increase
- unsupported distance increase
- unsupported initiative jump
- continuation reopen after cooling
- final probe overshoot
- trajectory reset present

This makes the evaluation less dependent on one global impression score. The key question is whether the dialogue still feels like one ongoing relational process rather than a sequence of locally plausible but interactionally reset replies.

Second, a **pairwise preference judge** compares two routes on the same case. The pairwise rule is:

- prefer the trajectory that better preserves the same relationship process;
- do not reward verbosity or generic helpfulness by default;
- prioritize less abrupt shift, less overinterpretation, less compensatory warmth, and cleaner continuation/final-probe behavior.

This matters for two reasons.

First, many bad failures in this project appear as:

- continuation inflation
- over-explanation
- compensatory warmth
- unnecessary follow-up

so length was a useful exploration-time proxy.

Second, a shorter answer can still be:

- too cold
- too generic
- discontinuous with prior turns

and a slightly longer answer can still be:

- coherent
- well-calibrated
- relationally stable

Therefore, the final argument of the paper should lead with a multi-evidence package:

- case-level coherence
- structured failure labels
- pairwise results
- agreement
- automatic diagnostics

and use raw length only as supporting evidence.

For submission, the evaluation section should additionally specify:

- fixed judge prompt wording in the appendix;
- fixed decoding temperature (preferably `0` or `0.2`);
- fixed sample count per case;
- whether judging is blind to mode identity;
- number of judges;
- and a simple agreement statistic.

### 4.6 Semi-Formal Coherence Operationalization

The paper's main endpoint remains judge-centered relational coherence, but this should be supplemented by a semi-formal diagnostic layer rather than left as a purely soft notion.

The current project now distinguishes four heuristic instability components:

- `Δ warmth per turn`
- `unexpected polarity flip`
- `unsupported initiative jump`
- `response length spike`

These are not treated as replacements for coherence judge. Instead, they operationalize the kinds of trajectory failures the paper is already concerned with:

- unsupported warmth increase
- unsupported distance increase
- continuation inflation
- abrupt reopening after cooling or boundary cues

The current lightweight automatic proxy package is documented in `PAPER_RELATIONAL_COHERENCE_OPERATIONALIZATION.md` and implemented in `paper_relational_proxy_metrics.py`.

## 5. Experiments and Results

### 5.1 Long-Range Cases vs Short Smoke

Short smoke cases were useful for pipeline checks but too short to support serious claims about relational coherence. This motivated the shift to multi-phase long-range cases.

**Conclusion:** long cases are necessary for this problem.

### 5.2 Prompt-Bridging Diagnosis

We tested whether weak performance of explicit-state methods was mainly caused by poor prompt presentation.

**Conclusion:** prompt presentation matters, but prompt bridge alone is not the main bottleneck.

### 5.3 Single-Layer vs Two-Layer Oracle Comparison

Oracle comparisons showed that:

- `projected_oracle > direct_oracle`
- `projected_oracle > oracle-collapsed-single-layer`

This matters because it means the projected oracle route is not reducible to a collapsed single-layer prompt in this setting. However, the current evidence is still weaker than a true causal isolation of "chart decomposition itself," because the strongest current deploy result also depends on the strength of the `i7` interface family. A stronger causal claim requires a no-relational-state `i7`-style control ablation; in the current project this is instantiated as a `baseline_relational_instruction_to_interface` route, which should be compared directly against both `baseline_relational_instruction` and `explicit_rel_state_rel_to_interface_i7`.

**Table 0 placeholder:** oracle single-layer vs decomposed-control comparison plus no-relational-state `i7` control ablation.
Suggested columns:

- setting
- single-layer score / summary
- two-layer score / summary
- baseline-to-`i7` score / summary
- judge outcome
- interpretation

### 5.4 Strong Baseline Competitiveness

A recurring result is that `baseline_relational_instruction` is highly competitive. In several long-range cases, full oracle projected control was tied with or only modestly better than the strong baseline.

**Conclusion:** strong baselines are genuinely strong; the paper is not succeeding due to trivial baseline weakness.

**Table 0b placeholder:** strong baseline vs oracle projected comparison.
Suggested columns:

- case family
- strong baseline
- oracle projected
- pairwise result
- notes

### 5.5 Structure vs Interface Control Ablation

To separate "decomposition gain" from "interface gain," we added a no-relational-state control route:

- `baseline_relational_instruction`
- `baseline_relational_instruction_to_interface_i7_sc_vA`
- `explicit_rel_state_rel_to_interface_i7_sc_vA`

The purpose of this comparison is simple. If `baseline -> i7` already matches `explicit relation -> i7`, then the main gain should be attributed primarily to the `i7` interface itself. If `explicit relation -> i7` remains clearly stronger, then explicit relation-chart decomposition is still adding value beyond interface choice.

The first proxy result is already informative. On the `v1` structure-vs-interface package:

- `baseline_relational_instruction` = `98.17` average characters
- `baseline_relational_instruction_to_interface_i7_sc_vA` = `41.33`
- `explicit_rel_state_rel_to_interface_i7_sc_vA` = `16.50`

This establishes two points.

First, the `i7` interface itself contributes a large share of the observed gain. Simply converting the baseline-side relational instruction into an `i7`-style deploy chart removes a large amount of over-expansion.

Second, explicit relation-chart decomposition still appears to add further value beyond interface-only `i7`. The explicit `relation -> i7` route remains substantially more controlled than `baseline -> i7`.

The paper should therefore avoid both extreme readings:

- not "all gain comes from chart decomposition itself"
- not "only the final `i7` prompt interface matters"

The safer reading is that the current improvement is compositional:

- part of the gain comes from the deploy-interface family (`i7`)
- part comes from explicit relation-chart decomposition on top of that interface

The focused multi-judge package on `warm / vuln / cool` now supports the same reading more concretely. Across `3` independent judge runs, `baseline -> i7` beats the strong baseline in `9/9` pairwise comparisons, `explicit relation -> i7` beats the strong baseline in `8/9`, and `explicit relation -> i7` beats `baseline -> i7` in `6/9`. Pairwise winner agreement is `0.7778`. This is not strong enough to justify a claim that chart decomposition dominates interface choice by itself, but it is strong enough to support the paper's mixed-attribution reading: executable interface quality explains a large share of the gain, while explicit relation-chart decomposition adds a further moderate stabilization effect.

This is the strongest current reading of the ablation:

- the gain is not purely "chart decomposition itself";
- the gain is not purely "better final prompt interface" either;
- instead, executable interface quality and explicit relation-chart decomposition both contribute, with the interface accounting for a large share of the improvement and the explicit relation chart adding further trajectory-level stabilization.

### 5.6 Execution Interface Family Screening

Stage-2 interface screening initially compared multiple interface families. After explicit prompt separation and phase-sensitive hard constraints were added, the most promising interfaces became `i6` and `i7`, with `i7` emerging as the strongest overall candidate.

This screening is informative in a specific way. `i6` effectively serves as a merged-interface comparison because it collapses clarify-followup and affective-followup into one combined follow-up field; in practice it was repeatedly read as more rigid or over-merged. `i8` serves as an add-one-field comparison because it extends `i7` with an extra directness field; in practice it did not produce a stable overall improvement over `i7`. A later focused supplement retained the same qualitative reading: `i6` stayed competitive as a stronger-clamp alternative, while `i8` still failed to produce a stable net gain. These family-level comparisons support a best-tested deploy-chart claim, not a final minimality claim.

### 5.7 Frozen Main Deploy Comparison

After freezing the deploy route and expanding the oracle execution set, we compared:

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7`
- `explicit_rel_state_projected_oracle_i7`

The frozen summaries and final manual judge support:

- direct `relation -> i7` beats the strong baseline on all main oracle cases;
- oracle `i7` also beats the strong baseline;
- oracle `i7` vs direct `relation -> i7` is mostly tie or only a slight oracle edge.

The frozen-final multi-judge results now make this substantially more precise. Across `3` judge runs and `5` frozen case families, direct `relation -> i7` beats the strong baseline in `15/15` pairwise comparisons, and `oracle_i7` also beats the strong baseline in `15/15`. Pairwise winner agreement is `0.9111`, which is strong enough to treat the frozen-final pairwise result as the paper's main judge-backed empirical claim. At the same time, `oracle_i7` beats direct `relation -> i7` in `13/15` comparisons, so the best current real deploy route is clearly strong but not yet oracle-level. The remaining gap should therefore be described as modest and consistent rather than large.

The paper should therefore freeze:

- **main deployable controller:** `relation -> i7`

The significance of this result is not that the strong baseline is weak. It is that a frozen explicit controller line remains cleaner in relational continuity even against a strong prompt-only system.

See **Table 1** for the intended frozen main comparison.
Suggested rows:

- `warm`
- `vulnerability`
- `cooling`
- `mixed_signal`
- `boundary_repair`

Suggested columns:

- strong baseline coherence
- direct `relation -> i7` coherence
- oracle `i7` coherence
- direct vs baseline
- oracle vs baseline
- oracle vs direct
- notes

### 5.7 Hybrid Gap Diagnosis

Hybrid experiments suggest:

- oracle relation alone only modestly improves the real deploy route;
- oracle behavior remains close to oracle deploy output.

**Conclusion:** the gap is not mainly updater failure or relation-summary wording alone. The more precise issue is how analytic behavior representations are bridged into deployable interfaces.

### 5.8 Corrected Fitted Bridge

After correcting the fitted-projector deployment path, `relation -> fitted 8D behavior -> i7` behaved very differently from earlier polluted runs. The corrected bridge remained close to oracle-side behavior and close to full oracle execution.

This substantially revises the earlier pessimistic interpretation. It shows that:

- `relation -> fitted 8D behavior -> i7` can remain close to oracle-side behavior;
- `8D -> i7` is not a catastrophic distortion layer;
- the analytic bridge is viable when the fitted deployment path is implemented correctly.

**Appendix table placeholder:** corrected bridge recheck.
Suggested columns:

- route
- global summary
- bridge-vs-oracle pairwise
- interpretation

### 5.9 Final Bridge Sanity

Using the expanded oracle set, we then compared:

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

Manual judge shows that:

- `oracle_state_i7_pfitpoly2` vs `oracle_behavior_i7` is effectively tie across all five main cases;
- `oracle_state_i7_pfitpoly2` vs `oracle_i7` is also mostly tie, with only a small oracle edge on vulnerability-style cases.

This supports a second frozen decision:

- **analytic bridge:** retain `relation -> behavior(8D) -> i7`

The 8D layer should therefore remain in the paper, but as an analytic and explanatory bridge rather than as the paper's main deploy controller.

See **Table 2** for the intended bridge sanity presentation.
Suggested rows:

- `warm`
- `vulnerability`
- `cooling`
- `mixed_signal`
- `boundary_repair`

Suggested columns:

- oracle-state bridge coherence
- oracle-behavior coherence
- oracle full coherence
- state vs behavior
- state vs oracle
- behavior vs oracle
- notes

### 5.10 Deploy Ontology and Framing Freeze

We compared deploy ontology variants and framing variants on top of the frozen `i7` deploy chart.

The ontology variants were:

- `vA`: the current `i7` ontology
- `vB`: an interactional-7 ontology
- `vC`: a permission-oriented 7-axis ontology

The framing variants were:

- `sa`
- `sb`
- `sc`

Proxy-level runs suggested that ontology differences matter more than wording-only differences, and that the current `vA` ontology remains the strongest default chart. Collaborative manual reading over representative `warm`, `vulnerability`, `cooling`, and `repair` cases refined this picture further:

- the best default deploy route remains direct `relation -> i7`;
- the best default deploy ontology remains `vA`;
- the strongest current framing is `sc`;
- the strongest current real candidate is `direct sc_vA`;
- `vC` should be retained as a vulnerability-sensitive ontology rather than treated as a uniformly worse alternative;

This ontology/framing line should still be described more cautiously than the frozen main result. Its current status is a frozen collaborative reading backed by the focused ontology package and earlier comparative analysis, not yet a full multi-judge-agreement result at the same evidential level as frozen-final. The practical paper-facing claim should therefore remain local: within the current deploy-chart family, `vA` is the safest default ontology, `sc` is the strongest current framing, and `vC` is best retained as a vulnerability-sensitive alternative rather than as a global replacement.
- the projected route remains valuable as an analytic bridge, but not as the preferred main deployment route.

The most important interpretive correction from collaborative reading is that a more restrained ontology is not automatically a better relational controller. In particular, `vC` can become too regulation-like or can weaken companion-like relationship presence in some families, even while sounding softer and more natural in vulnerability-heavy cases. Conversely, `sc_vA` often preserves restraint without collapsing into low-temperature detachment.

See **Table 3** for the intended deploy ontology / framing summary.
Suggested rows:

- `warm`
- `vulnerability`
- `cooling`
- `repair`

Suggested columns:

- `vA+sa`
- `vA+sc`
- `vC+sa`
- `vC+sc`
- winner / tie
- notes

## 6. Discussion

### 6.1 What the Paper Currently Supports

At the current stage, the evidence supports the following claims:

1. Strong prompt baselines are highly competitive in long-term companion dialogue.
2. Single-layer relational control is weaker than the current chart-decomposed controller.
3. The current chart-decomposed controller is not reducible to "just a better single-layer prompt."
4. A well-designed execution interface matters.
5. The current best deployable controller is a direct `relation -> i7` route.
6. A corrected `relation -> fitted 8D behavior -> i7` bridge remains close to oracle-side behavior and full oracle execution.
7. Within the deploy ontology line, `vA` is the best default ontology, `sc` is the best framing, and `vC` is best treated as a vulnerability-sensitive alternative rather than a new default.
8. The most useful distinction is therefore not simply "state works" vs "state fails," but:
   - analytic chart
   - versus deployable execution chart
   - and the quality of the bridge between them.
9. The current stack should be read as a useful chart decomposition rather than as proof that layered structure is ontologically privileged over all possible one-layer alternatives.

### 6.2 What the Paper Does Not Claim

This paper does **not** claim:

- that explicit relational state always yields better language behavior than strong baselines;
- that relation-state representation design has been solved;
- that the current 4D relation ontology is uniquely correct or final;
- that the current hand-defined charts recover the model's true internal relational ontology;
- that the current experiments have fully isolated the causal contribution of chart decomposition apart from deploy-interface quality;
- that the present `i7` field decomposition has already been shown to be minimal or necessary;
- that the final best deployable interface has been universally identified across all model families;
- that the current system is already product-optimal.

### 6.3 Why This Is Still a Strong Result

The interesting result is not simply that structured state helps. The more valuable finding is:

- structured control that appears intuitively reasonable does **not** automatically translate into better language-level behavior;
- chart-decomposed control has real potential, but that potential must be realized through an executable behavior interface;
- strong baselines can already absorb much of the visible gain, which makes the remaining mechanism analysis essential;
- yet a frozen explicit controller can still stably beat that strong baseline;
- and an analytic bridge can survive as a near-oracle explanatory layer without having to be the main deploy route.

This is a stronger and more defensible story than a naive "structured state beats baseline" narrative.

## 7. Limitations

### 7.1 Case Scale

Current experiments rely on carefully designed long-range cases rather than large naturally collected datasets.

### 7.2 Judge Scale

Although the frozen final package now includes manual case-level and pairwise judge, the evaluation scale is still modest. A larger final judge pass would further strengthen the empirical story.

### 7.3 Proxy Metrics

Much of the exploratory process used average response length as a rough diagnostic signal for over-expansion. This was useful for fast iteration, but length alone is not a trustworthy endpoint metric. The final paper should therefore foreground manual coherence judge and pairwise preference results over raw length summaries.

### 7.4 Evaluation Formalization

The current project already relies heavily on case-level and pairwise judge, but the submission-standard evaluation protocol still requires stronger formalization. In particular, the final version should specify:

- exact judge prompt wording;
- fixed decoding temperature;
- number of samples per case;
- judge blindness;
- number of judges;
- and inter-judge agreement.

### 7.5 Operational Definition Boundary

The current notion of relational coherence is meaningful and practically useful, but it is still only partially operationalized. The present paper should therefore treat it as a judge-centered construct rather than pretend that it is already a sharp quantitative metric with a fully fixed threshold for abrupt shift.

### 7.6 Interface Minimality Boundary

Current interface-family comparisons justify treating `i7` as the strongest deploy chart among the families we tested. They do not yet justify a stronger statement that the current seven-field decomposition is minimal or necessary. In the present evidence, `i6` only supplies a merged-family comparison and `i8` only supplies an add-one-field comparison; a true per-field drop or merge ablation remains future work.

### 7.7 Cross-Model Generalization

The main result has received a same-family sanity check on a stronger OpenAI model, but broader cross-family generalization remains incomplete.

## 8. Conclusion

This paper studies explicit relational control for long-term companion dialogue under a stronger and more realistic setup than a simple prompt-vs-state comparison. We find that strong prompt baselines are difficult to beat, that single-layer relational control is insufficient, and that a chart-decomposed controller with an executable interface is substantially more promising. After freezing the system on an expanded oracle case set, the best deployable controller in the current study is a direct `relation -> i7` route, which consistently beats the strong baseline in manual coherence judgment and remains close to the oracle deploy route. A dedicated structure-vs-interface ablation also clarifies that this advantage is mixed rather than single-cause: the `i7` deploy interface itself explains a large share of the gain, while explicit relation-chart decomposition still contributes additional trajectory-level stabilization beyond interface-only `i7`. At the same time, a corrected `4D relation -> fitted 8D behavior -> i7` bridge remains close to oracle-side behavior and full oracle execution, which justifies retaining the 8D layer as an analytic bridge rather than discarding it.

The strongest frozen-final evidence is now pairwise and multi-judge rather than proxy-based. Direct `relation -> i7` beats the strong baseline in `15/15` pairwise comparisons, and `oracle_i7` does the same, while `oracle_i7` keeps only a modest but consistent edge over the best current real route (`13/15`). This sharpens the paper's central claim: the deploy route is no longer just plausible in principle, but already clearly better than the strong baseline while still leaving meaningful but limited headroom to oracle execution.

The final conclusion of the current draft is therefore:

- chart-decomposed relational control is a viable and meaningful direction for long-horizon companion dialogue, but its gain should be read as mixed attribution rather than as purely structural gain;
- deployable control and analytic explanation should be separated rather than conflated;
- in the present system, the strongest configuration uses:
  - a **deploy route**: `relation -> i7`
  - an **analytic bridge**: `relation -> behavior(8D) -> i7`
- within the deploy ontology line:
  - `vA` is the default ontology,
  - `sc` is the best framing,
  - `vC` is best retained as a vulnerability-sensitive alternative.

This yields a stronger overall claim than either a pure prompt baseline story or a pure latent-state story: an explicit control framework can simultaneously support a deployable controller and a near-oracle analytic bridge, provided that the bridge between analytic and execution layers is constructed carefully. In the current evidence, the deploy-side gain should be read as the combination of executable interface quality and explicit relation-chart decomposition rather than as a pure layered-structure effect.

The strongest defensible interpretation is therefore not "we proved the final layered ontology," but "we identified a useful layered chart decomposition whose deploy and analytic roles can be separated, tested, and improved."

## References Placeholder

The final paper should ground itself in at least the following neighboring literatures:

- controllable dialogue generation
- persona consistency and long-term dialogue
- partner state and social signal modeling
- LLM controllability and structured intermediate representation

Suggested citation placeholders to resolve before submission:

- [CITATION: controllable dialogue / controllable generation]
- [CITATION: persona consistency / long-term dialogue]
- [CITATION: partner state / social signal / user state]
- [CITATION: controllability / intermediate representations]

## Appendix Placeholder

Possible appendix contents:

- full prompt templates
- ontology/framing tables
- detailed judge rubric
- additional oracle and bridge tables
