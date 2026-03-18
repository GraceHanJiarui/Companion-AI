# Draft Paper: Two-Layer Relational Control for Long-Term Companion Dialogue

## Title

**Two-Layer Relational Control for Long-Term Companion Dialogue: Strong Baselines, Oracle Gaps, and Executable Interfaces**

Alternative titles:

- **Single-Layer vs Two-Layer Relational Control in Long-Term Companion Dialogue**
- **From Relational State to Executable Behavior Control in Long-Horizon Companion Dialogue**
- **Realization Gaps in Structured Relational Control for Long-Term Companion Dialogue**

---

## Abstract

Large language models can produce fluent companion-style dialogue, but maintaining a coherent sense of relationship over long-horizon interaction remains difficult when control relies only on prompt instructions. A natural systems hypothesis is to introduce explicit relational state as an intermediate control layer. However, whether such structured control actually improves language-level relational coherence, and what kind of control interface is actually executable for a general-purpose LLM, remains unclear. In this paper, we study long-term companion dialogue through the lens of relational drift, abrupt relational shifts, and case-level coherence. We compare a strong prompt baseline, a single-layer relational-control formulation, and a two-layer formulation that maps relational state into explicit behavior constraints before generation. We further introduce oracle controls and hybrid diagnostics to separate state updating, relation-to-behavior mapping, interface construction, and final language realization. Our evidence supports four main claims. First, strong prompt baselines are genuinely competitive, so explicit control is not solving an easy benchmark. Second, direct deployable control through `relation -> i7` is the strongest current real controller, while a corrected `4D relation -> fitted 8D behavior -> i7` route remains valuable as an analytic bridge rather than the preferred deploy path. Third, within the deploy ontology line, the default `vA` ontology with `sc` framing is the best current real configuration, while `vC` is better treated as a vulnerability-sensitive alternative than as a new default ontology. Fourth, later manifold-style analyses are best read conservatively as chart-structure analyses over hand-defined views, not as direct recovery of the model's true internal ontology. Final conclusions are based on manual judge and pairwise coherence comparisons rather than length statistics alone.

---

## 1. Introduction

Long-term companion dialogue is not just a sequence of locally helpful responses. It is also a process in which the system must maintain a stable, interpretable, and non-jumping sense of relationship over time. Prompt-only systems can often sound locally good while still exhibiting relational drift: they may become abruptly warmer, colder, more over-involved, or more distant than the interaction history supports.

A common engineering response is to introduce explicit intermediate state: track relationship variables, update them conservatively, and use them to shape downstream behavior. This idea is intuitively attractive, but intuition alone is insufficient. A structured control layer may be internally coherent yet fail to produce better language behavior, especially when realized through an unmodified general-purpose LLM. Strong prompt baselines may also already capture much of the visible gain.

This paper asks a focused question: **when relational control is made explicit, what kind of control interface is actually executable for long-term companion dialogue?** In particular, we study the contrast between:

- a **strong prompt baseline** that uses high-level relational instruction only;
- a **single-layer relational control** formulation that directly conditions generation on relational stance;
- a **two-layer relational control** formulation that first represents relational stance and then projects it into explicit behavior-side constraints before generation.

Our results suggest a more nuanced conclusion than “explicit state helps” or “explicit state fails.” Strong baselines are highly competitive. Single-layer control appears weaker than two-layer control. A well-designed two-layer interface shows clear promise in oracle form and retains part of that advantage in the real chain. Recent deployment fixes further show that oracle-space explanatory fit and deployable controller success must be distinguished, but are not necessarily disconnected: under a corrected fitted projector, `relation -> behavior -> i7` can remain close to oracle behavior while direct `relation -> i7` remains the stronger deploy route. The remaining gap is therefore better understood as a control-route construction and structure-preservation problem than as a simple failure of explicit relational state.

### 1.1 Contributions

The current draft supports the following contributions:

1. We formulate long-horizon companion dialogue as a problem of **relational coherence** and **abrupt relational shift** rather than only local helpfulness.
2. We compare **single-layer** and **two-layer** relational control against a **strong prompt baseline**.
3. We show that **strong prompt baselines remain highly competitive**, making this a nontrivial control problem rather than a weak-baseline artifact.
4. We develop an **oracle and hybrid diagnostic framework** that separates:
   - relational stance,
   - behavior / execution interface,
   - final language realization.
5. We identify a current best deployable controller:
   - direct `relation -> i7`,
   - with `vA` ontology and `sc` framing as the strongest current real configuration.
6. We show that good oracle-space fit does not automatically imply deployed control success, but that the gap can shrink substantially after correcting the fitted projector implementation.
7. We motivate a broader distinction between:
   - analytic charts used for explanation and oracle fit,
   - and deployable execution charts used for reliable language control.
8. We show, in frozen final comparisons, that:
   - direct `relation -> i7` is the best current deployable controller,
   - while `relation -> behavior(8D) -> i7` remains a strong analytic bridge rather than a failed intermediate layer.
9. We provide a conservative late-stage geometric analysis showing that the current hand-defined charts (`raw4`, `8D behavior`, `i7`) play different roles over a richer shared structure, while explicitly avoiding the stronger claim that we have recovered the model's true internal ontology.

### 1.2 Scope

This paper is intentionally scoped as a **focused mechanism paper**, not a full product paper. It does **not** attempt to solve:

- all questions of relational-state representation design;
- why strong baselines may already encode implicit relational control;
- the full product-level question of controllability vs zero-shot language quality;
- human-human relationship modeling in general.

Those are important follow-on directions, but including them here would make the paper unstable and difficult to defend.

At the current stage, the paper should also avoid expanding itself into:

- a full `scene/phase` necessity paper;
- a full relation-dimensionality search paper;
- a full analysis of why the strongest prompt baseline is already so competitive;
- a generalized LLM decision-interpretation methodology paper.

Those are all promising follow-on directions, but they should remain either:

- future work,
- appendix-level discussion,
- or separate papers.

---

## 2. Problem Setting

We study **long-term companion-style dialogue**, where the same system interacts with the same user across multiple turns and is expected to maintain relational continuity.

### 2.1 Relational Coherence

We treat relational coherence as a dialogue-level property: a multi-turn interaction should feel like one ongoing relationship process rather than a sequence of isolated, stylistically reset responses.

### 2.2 Abrupt Relational Shift

We define an abrupt relational shift not as any large change, but as a change that exceeds what is supported by the interaction history and current user signal. This includes three components:

- **direction**: whether the system moves warmer or cooler appropriately;
- **magnitude**: whether the change overshoots what the context supports;
- **timing**: whether the shift occurs without sufficient buildup.

### 2.3 Slow-Variable Assumption

Our explicit relational-state design assumes that relationship is a **slow variable**:

- per-turn `delta_R` should usually be small;
- many turns should naturally produce `delta_R = 0`;
- no strong relationship signal should mean no update by default.

This assumption is not merely a design preference; it is part of the paper’s modeling hypothesis.

---

## 3. Method

### 3.1 Baseline: High-Level Relational Instruction

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
2. relational state is projected into a **behavior / execution interface**;
3. generation is conditioned on both:
   - current relational stance,
   - explicit execution constraints.

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

Prompt layout was further stabilized through two important design changes:

- **B. explicit layout separation**
  - `Current relationship stance`
  - `Current expression constraints`
- **C. phase-sensitive hard constraints**
  - especially for:
    - `E_ordinary_continuation`
    - `F_final_probe`

These changes were critical: before them, interface comparisons were heavily polluted by continuation-phase over-expansion.

### 3.5 Oracle and Hybrid Controls

To separate mechanisms, we introduced oracle and hybrid modes:

- `projected_oracle`
  - oracle relation summary + oracle behavior control
- `oracle_rel`
  - oracle relation summary + real behavior control
- `oracle_behavior`
  - real relation summary + oracle behavior control
- `oracle_state + real projection`
  - oracle relation state values + real projection mapping + real realization

These variants allow us to ask where the remaining gap lives:

- in relation-state quality,
- in relation-to-behavior projection,
- or in final language realization.

---

## 4. Experimental Design

### 4.1 Research Questions

The current paper centers on the following questions:

**RQ1.** Is two-layer relational control more promising than single-layer relational control for long-term companion dialogue?

**RQ2.** Can a strong two-layer execution interface outperform a strong prompt baseline?

**RQ3.** If the real-chain two-layer system does not reach oracle performance, where does the gap come from?

**RQ4.** How should analytic latent layers and deployable execution interfaces be separated and bridged in a two-layer controller?

### 4.2 Datasets / Case Sets

We used several case sets over the course of the study:

- short smoke cases
- long-range manually designed multi-phase cases
- oracle long cases
- oracle execution-interface cases

The main Stage-2 case family currently includes:

- warming trajectories
- vulnerability-with-correction trajectories
- cooling trajectories
- **placeholder:** mixed-signal trajectories to be finalized in the final frozen run

### 4.3 Evaluation Protocol

We use three main evaluation styles:

1. **summary statistics**
   - average response length
   - phase-level inflation
   - continuation/probe over-expansion
2. **case-level judge inputs**
   - relational coherence
   - abrupt shift
   - phase transition quality
3. **pairwise judge**
   - baseline vs two-layer
   - single-layer vs two-layer
   - oracle vs real

### 4.4 What Counts as Evidence

This paper does not treat response length as a standalone objective. Instead, lower length is interpreted only as a **coarse diagnostic proxy** when it aligns with:

- lower over-expansion,
- less compensatory warmth,
- fewer unnecessary follow-ups,
- cleaner adherence to relationship continuity.

Final conclusions rely on:

- manual judge,
- pairwise comparison,
- repeated sampling,
- and hybrid diagnostics taken together.

At the current point, projector evaluation must distinguish:

- oracle-space fit quality;
- deployable controller quality inside the `i7` execution stack.

---

## 5. Experiments and Current Findings

### 5.1 Long-Range Cases vs Short Smoke

Short smoke cases were useful for pipeline checks but too short to support serious claims about relational coherence. This motivated the shift to multi-phase long-range cases.

**Current conclusion:** long cases are necessary for this problem.

### 5.2 Prompt-Bridging Diagnosis

We tested whether weak performance of explicit-state methods was mainly caused by poor prompt presentation (`vA/vB/vC`).

**Current conclusion:** prompt presentation matters, but prompt bridge alone is not the main bottleneck.

### 5.3 Single-Layer vs Two-Layer Oracle Comparison

Oracle comparisons showed that:

- `projected_oracle > direct_oracle`
- `projected_oracle > oracle-collapsed-single-layer`

This matters because it means two-layer control is not merely “another good prompt.” The layered control structure itself appears to add useful constraint.

### 5.4 Strong Baseline Competitiveness

A recurring result is that `baseline_relational_instruction` is highly competitive. In several long-range cases, full oracle projected control was tied with or only modestly better than the strong baseline.

**Current conclusion:** strong baselines are genuinely strong; the paper is not succeeding due to trivial baseline weakness.

### 5.5 Execution Interface Family

Stage-2 interface screening initially compared `i4/i6/i7/i8`. After adding:

- strict prompt separation (B),
- phase-sensitive hard constraints (C),

the most promising interfaces became:

- `i6`
- `i7`

Further judge-based comparison showed that:

- both `i6` and `i7` can beat the strong baseline in oracle form;
- `i7` is currently the best overall candidate.

### 5.6 Final Frozen Main Comparison

After freezing the deploy route and expanding the oracle case set from `18` to `30` phase points, we compared:

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7`
- `explicit_rel_state_projected_oracle_i7`

The frozen global summaries show:

- `baseline_relational_instruction = 106.30`
- `explicit_rel_state_rel_to_interface_i7 = 34.07`
- `explicit_rel_state_projected_oracle_i7 = 37.67`

More importantly, final manual judge on the frozen package shows:

- direct `relation -> i7` beats the strong baseline on all five oracle cases;
- oracle `i7` also beats the strong baseline on all five oracle cases;
- oracle `i7` vs direct `relation -> i7` is mostly `tie` or only a slight oracle edge.

The current paper should therefore freeze:

- **main deployable controller:** `relation -> i7`

The significance of this result is not that the strong baseline is weak. It is that the frozen controller line remains cleaner in relational continuity even against a strong prompt-only system.

### 5.7 Hybrid Gap Diagnosis

Hybrid experiments currently suggest:

- `oracle_rel_i7` only modestly improves over `real i7`
- `oracle_behavior_i7` is close to `oracle i7`

**Current conclusion at this stage:** behavior-side control is the crucial layer, but later corrected deployment experiments show that the gap cannot be reduced to a simple “behavior side is broken” story. The more precise issue is how analytic behavior representations are bridged into deployable interfaces.

### 5.8 Oracle Relation State + Real Projection

We ran a stricter gap-splitting experiment using:

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_state_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

The purpose of this experiment is to distinguish:

- updater-side failure,
- projection-mapping failure,
- final realization failure.

The key logic is that `oracle_state_i7` uses:

- oracle relational state,
- real deterministic `project_behavior(...)`,
- real `i7` execution prompt realization.

The earlier global average lengths were:

- `real i7`: `59.28`
- `oracle_state_i7`: `116.72`
- `oracle_behavior_i7`: `28.94`
- `oracle_i7`: `37.22`

This result is highly diagnostic:

- simply fixing relation state does **not** close the gap;
- `oracle_state_i7` is often substantially worse than `real i7`;
- `oracle_behavior_i7` remains close to `oracle_i7`.

The current interpretation is therefore stronger than our earlier hybrid reading:

- the main remaining problem is not best described as updater failure;
- it is also not mainly a relation-summary wording problem;
- it is more likely located in the deterministic
  **relation-to-behavior projection mapping** itself.

At the time, this appeared to imply a major projector failure. However, later corrected fitted-projector experiments revised this interpretation: a substantial part of the earlier failure was implementation- and route-construction-dependent rather than evidence that the analytic bridge itself was fundamentally invalid.

### 5.9 Pure-Relation Projector Redesign (`v3a` / `v3b`)

To test whether the failure above can still be attributed mainly to a poor projector family, we implemented two new pure-relation projector variants while keeping the two-layer architecture and continuous `relation -> behavior` mapping:

- `v3a`: a conservative decoupled linear projector
- `v3b`: a nonlinear gated projector

The evaluation again compared:

- `real i7`
- `oracle_state i7`
- `oracle_behavior i7`
- `oracle i7`

For `v3a`, the global average lengths were:

- `real i7_pv3a`: `37.22`
- `oracle_state i7_pv3a`: `121.61`
- `oracle_behavior i7`: `37.17`
- `oracle i7`: `36.22`

For `v3b`, the global average lengths were:

- `real i7_pv3b`: `33.28`
- `oracle_state i7_pv3b`: `129.61`
- `oracle_behavior i7`: `36.33`
- `oracle i7`: `34.89`

These results are informative in a specific way. Both projector redesigns improve the real chain, but neither moves `oracle_state_i7` meaningfully closer to `oracle_behavior_i7`. This weakens the explanation that the main problem is simply that the old projector was poorly designed. The pure-relation hypothesis is therefore not logically falsified, but it is substantially weakened under the current relation representation.

The immediate implication is that oracle-space fit and deployed-controller quality must be evaluated separately.

### 5.10 Corrected Fitted Bridge and Interface-Gap Recheck

After correcting the fitted-projector deployment path, the `fitpoly2` bridge behaved very differently from the earlier polluted runs. On the repaired comparison:

- `real projected_i7_pfitpoly2 = 42.00`
- `oracle_state projected_i7_pfitpoly2 = 33.72`
- `oracle_behavior_i7 = 37.06`
- `oracle_i7 = 28.17`

This result substantially revises the earlier pessimistic interpretation. It shows that:

- `relation -> fitted 8D behavior -> i7` can in fact remain close to oracle-side behavior;
- `8D -> i7` is not a broad catastrophic distortion layer;
- the analytic bridge is viable when the fitted deployment path is implemented correctly.

An explicit `8D -> i7` mismatch analysis further found:

- small average per-dimension behavior deltas;
- only rare interface-field mismatches;
- residual sensitivity concentrated in a small number of delicate vulnerability-style turns.

Thus, the corrected reading is not that analytic behavior layers are unusable for deployment, but that deployable success depends on a faithful bridge between analytic and execution layers.

### 5.11 Final Bridge Sanity

Using the expanded oracle set, we then compared:

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

The frozen global summaries show:

- `oracle_state_i7_pfitpoly2 = 44.77`
- `oracle_behavior_i7 = 49.83`
- `oracle_i7 = 45.13`

Manual judge further shows that:

- `oracle_state_i7_pfitpoly2` vs `oracle_behavior_i7` is effectively `tie` across all five cases;
- `oracle_state_i7_pfitpoly2` vs `oracle_i7` is also mostly `tie`, with only a small oracle edge on vulnerability-style cases.

This supports a second frozen decision:

- **analytic bridge:** retain `relation -> behavior(8D) -> i7`

The 8D layer should therefore remain in the paper, but now as an analytic and explanatory bridge rather than as the paper’s main deploy controller.

---

### 5.12 Post-Expansion Relation Dimensionality Validation

After expanding the oracle substrate to `30` cases and `180` phase points, we tested whether the current 4D relation representation remained competitive against simpler alternatives.

The compared representations included:

- all 2D subsets of the current four relation axes;
- all 3D subsets of the current four relation axes;
- the current raw 4D basis;
- modest 5D/6D augmented bases built from the same four primitives.

The result is consistent across both `linear` and `poly2`:

- the current `raw4` basis is the best-performing tested representation;
- all tested 2D and 3D subsets are worse;
- the best 3D subsets remain reasonably competitive, but they do not match the full 4D basis.

The most important LOOCV numbers are:

- `linear`
  - `raw4 = 0.0216`
  - best 3D (`bond+care+trust`) = `0.0220`
- `poly2`
  - `raw4 = 0.0158`
  - best 3D (`care+trust+stability`) = `0.0169`

This does not prove that the current four dimensions are the final or uniquely correct ontology. However, it does support a more modest and important claim:

- the current 4D relation space is not trivially over-specified;
- dropping one of the four axes incurs a real explanatory cost on the expanded oracle substrate.

An important boundary is that the present 5D/6D augmented variants are still deterministic transforms of the same 4D labels. Under the current linear / quadratic fit family, they are largely redundant with the raw 4D basis. Therefore, the current `5D/6D ~= 4D` result should not be over-read as proof that richer relation ontologies are unnecessary. What it supports more directly is that the present raw 4D basis is a robust explanatory baseline.

## 6. Discussion

### 6.1 What the Paper Currently Supports

At the current stage, the evidence supports the following claims:

1. Strong prompt baselines are highly competitive in long-term companion dialogue.
2. Single-layer relational control is weaker than two-layer relational control.
3. Two-layer control is not reducible to “just a better single-layer prompt.”
4. A well-designed execution interface matters.
5. The current best deployable controller is a direct `relation -> i7` route.
6. A corrected `relation -> fitted 8D behavior -> i7` bridge remains close to oracle-side behavior and full oracle execution.
7. On the expanded oracle substrate, the current 4D relation space remains stronger than all tested 2D and 3D subsets.
8. The most useful distinction is therefore not “state works” vs “state fails,” but:
   - analytic latent layer
   - versus deployable execution interface
   - and the quality of the bridge between them.

### 6.2 What the Paper Does Not Yet Claim

This paper does **not** claim:

- that explicit relational state always yields better language behavior than strong baselines;
- that relation-state representation design has been solved;
- that the current 4D relation ontology is uniquely correct or final;
- that the final best deployable interface has been universally identified across all model families;
- that the current system is already product-optimal.

### 6.3 Why This Is Still a Strong Result

The interesting result is not simply that “explicit state works.” Rather, the more valuable finding is:

- structured control that appears intuitively reasonable does **not** automatically translate into better language-level behavior;
- two-layer control has real potential, but that potential must be realized through an executable behavior interface;
- strong baselines can already absorb much of the visible gain, which makes the remaining mechanism analysis essential;
- yet a frozen explicit controller can still stably beat that strong baseline;
- and an analytic bridge can survive as a near-oracle explanatory layer without having to be the main deploy route.

This is a stronger and more defensible story than a naive “structured state beats baseline” narrative.

---

## 7. Limitations

### 7.1 Case Scale

Current experiments rely on carefully designed long-range cases rather than large naturally collected datasets.

### 7.2 Judge Scale

Although the frozen final package now includes manual case-level and pairwise judge, the evaluation scale is still modest. A larger final judge pass would further strengthen the empirical story.

### 7.3 Proxy Metrics

Much of the exploratory process used average response length as a rough diagnostic signal for over-expansion. This was useful for fast iteration, but length alone is not a trustworthy endpoint metric. The final paper should therefore foreground manual coherence judge and pairwise preference results over raw length summaries.

### 7.4 Cross-Model Generalization

The main result has received a same-family sanity check on a stronger OpenAI model, but broader cross-family generalization remains incomplete.

---

## 8. Conclusion

This paper studies explicit relational control for long-term companion dialogue under a stronger and more realistic setup than a simple prompt-vs-state comparison. We find that strong prompt baselines are difficult to beat, that single-layer relational control is insufficient, and that two-layer control with an executable interface is substantially more promising. After freezing the system on an expanded oracle case set, the best deployable controller in the current study is a direct `relation -> i7` route, which consistently beats the strong baseline in manual coherence judgment and remains close to the oracle deploy route. At the same time, a corrected `4D relation -> fitted 8D behavior -> i7` bridge remains close to oracle-side behavior and full oracle execution, which justifies retaining the 8D layer as an analytic bridge rather than discarding it.

The final conclusion of the current draft is therefore:

- two-layer relational control is a viable and meaningful direction for long-horizon companion dialogue;
- deployable control and analytic explanation should be separated rather than conflated;
- the current 4D relation space remains a robust explanatory basis under expanded oracle evaluation, even though richer ontologies remain open;
- in the present system, the strongest configuration uses:
  - a **deploy route**: `relation -> i7`
  - an **analytic bridge**: `relation -> behavior(8D) -> i7`

This yields a stronger overall claim than either a pure prompt baseline story or a pure latent-state story: an explicit control framework can simultaneously support a deployable controller and a near-oracle analytic bridge, provided that the bridge between analytic and execution layers is constructed carefully.

### 8.1 Interface Shape Comparison

We ran a first direct comparison of deployable interface shapes on the expanded `180`-turn oracle substrate. The compared charts were:

- `8D -> i7-discrete`
- `8D -> continuous-interface`
- `relation -> i7 direct`

The result was unambiguous at the diagnostic level. The continuous deploy chart (`c8`) was systematically over-expansive:

- main route:
  - `projected_i7_pfitpoly2 = 41.79`
  - `projected_c8_pfitpoly2 = 112.24`
  - `rel_to_interface_i7 = 25.07`
  - `oracle_i7 = 30.41`
- oracle-state route:
  - `oracle_state_i7_pfitpoly2 = 33.05`
  - `oracle_state_c8_pfitpoly2 = 94.43`
  - `oracle_state_direct_i7 = 23.48`
  - `oracle_behavior_i7 = 32.92`
  - `oracle_i7 = 31.66`

The current paper-facing reading is therefore:

- a more continuous deploy chart is not automatically more faithful;
- under the present prompt-realization setup, the first continuous interface is substantially less stable than the discrete execution interface;
- the strongest current deploy chart remains direct `relation -> i7`;
- the strongest current analytic bridge remains `relation -> fitted 8D behavior -> i7`.

This comparison supports a broader methodological distinction:

- the analytic layer and the deploy layer should not be conflated;
- interface design should be treated as a separate chart-selection problem rather than assumed to be solved by making the deploy layer numerically closer to the analytic layer.

### 8.2 Deploy Ontology Freeze

We next compared deploy ontologies and framing variants on top of the current `i7` deploy chart. The ontology variants were:

- `vA`: the current `i7` ontology
- `vB`: an interactional-7 ontology
- `vC`: a permission-oriented 7-axis ontology

The framing variants were:

- `sa`
- `sb`
- `sc`

Proxy-level runs suggested that ontology differences matter more than wording-only differences, and that the current `vA` ontology remains the strongest default chart. A small-sample bridge sanity check did not produce a bridge-side reversal. Collaborative manual reading over representative `warm`, `vulnerability`, `cooling`, and `repair` cases refined this picture further:

- the best default deploy route remains direct `relation -> i7`;
- the best default deploy ontology remains `vA`;
- the strongest current framing is `sc`;
- the strongest current real candidate is `direct sc_vA`;
- `vC` should be retained as a vulnerability-sensitive ontology rather than treated as a uniformly worse alternative;
- the projected route remains valuable as an analytic bridge, but not as the preferred main deployment route.

The most important interpretive correction from the collaborative reading is that a more restrained ontology is not automatically a better relational controller. In particular, `vC` can become too regulation-like or can weaken companion-like relationship presence in some families, even while sounding softer and more natural in vulnerability-heavy cases. Conversely, `sc_vA` often preserves restraint without collapsing into low-temperature detachment.

### 8.3 Shared-Latent Manifold Evidence

We then moved from layerwise comparison to a more geometric question: whether `relation`, `behavior`, `i7`, and language-side realization behave like different charts on a shared latent interaction manifold.

The first-pass M1 geometry analysis supports three narrower but useful claims:

- the current `raw4` relation chart and the analytic `8D` behavior chart share substantial local structure;
- the deploy chart (`i7`) is geometrically closer to language realization than the analytic behavior chart is;
- the deploy chart is smoother than language realization but less smooth than the relation chart, which is consistent with its role as a stabilized execution chart rather than a final output space.

These M1 results should be interpreted carefully. They do **not** independently prove that the current ontology is externally correct, because the current behavior ontology was itself designed within the same research program. They are better read as geometry-level consistency checks that help clarify the role of each chart:

- `raw4` behaves like an upstream analytic chart;
- `8D behavior` behaves like a richer analytic chart;
- `i7` behaves like the deploy / realization-side chart.

We then ran a stronger M2 shared-latent reconstruction test. In M2, the latent was learned only from:

- `behavior`
- `i7`
- language-side features

and `relation_raw4` was predicted back from that shared latent afterwards rather than used to construct it.

This matters because it partially breaks the most obvious self-confirming path. The shared latent was not built from the hand-labeled relation coordinates themselves; instead, relation had to reappear as a predictable view of the common latent.

The main M2 findings are:

- a low-dimensional shared latent can jointly reconstruct `behavior`, `i7`, and language features with high accuracy;
- the same latent can also predict `relation_raw4` strongly, which suggests that the hand-labeled relation view is not disconnected from the multi-view interaction structure;
- the oracle deploy route organizes the shared latent more cleanly than the current best real route, especially on the `i7` and language sides.

The paper-facing reading is therefore not that the current ontology has been fully externally validated. The stronger justified claim is more modest:

- the current relation, behavior, deploy, and language views are not merely arbitrary disconnected layers;
- they are consistent with a shared interaction structure;
- the remaining real-vs-oracle gap appears to lie more in how faithfully that shared structure reaches deploy realization than in the mere existence of relation-side geometry.

We then ran a narrow `M3-lite` pooled-latent trajectory comparison on the two most important routes:

- the best current real route: `direct sc_vA`
- the current oracle deploy route: `oracle_i7`

Unlike M1 and M2, the point of `M3-lite` was not only whether the views can be jointly reconstructed, but whether the **same case trajectories** occupy roughly similar path geometry in a shared latent space. The result is best read as a trajectory-distortion result rather than a final manifold theorem.

The main findings are:

- the real and oracle routes do not behave like two unrelated path geometries;
- instead, the real route looks more like a noisier and somewhat flattened version of the oracle path geometry;
- the largest path distortion is concentrated in:
  - `cooling`
  - `boundary_repair`
- path distortion is smaller in:
  - `mixed_signal`
  - `vulnerability`
  - `warm`

This matters because it refines the current gap diagnosis. The remaining gap is not best described as:

- the real controller following a fundamentally different interaction logic,

but rather as:

- the real controller preserving the same broad trajectory family while compressing or distorting it, especially in `cooling` and `boundary_repair` cases.

This reading is also compatible with the collaborative manual judge:

- the best real controller often sounds stable and usable;
- however, in cooling and repair-like situations it can become too dry, too controlled, or too explicitly interface-shaped relative to the oracle route.

Taken together, M1, M2, M2.5, and M3-lite support a restrained but now substantially stronger interpretation:

- `4D relation`, `8D behavior`, and `i7` should not be treated as the final ontological truth of companion dialogue control;
- they are better understood as useful charts or views over a shared interaction structure;
- among those charts, `i7` is currently the most effective deploy chart;
- `behavior(8D)` remains useful as an analytic bridge;
- the main remaining problem is structure-preservation into realization, not a total failure of relation-side geometry.

Finally, we directly asked the more native question: if we learn a latent interaction structure only from

- `behavior_8d`
- `i7_numeric`
- `language_features`

then how many latent dimensions are actually needed, and how should the current charts be understood relative to that latent?

The native-latent discovery result materially changes the theoretical reading of the project:

- the latent does **not** appear to saturate at `4D`, `6D`, or even `12D`;
- in the present sweep, reconstruction quality continues to improve through at least `16D`;
- by contrast, family-level and trajectory-level diagnostics improve little beyond the earlier medium-dimensional regime.

The strongest paper-facing reading is therefore:

- the shared interaction structure suggested by the current multi-view data is not a small low-dimensional ontology of the same scale as the current `raw4` chart;
- rather, `raw4`, `8D behavior`, and `i7` are better understood as different compressed charts over a richer native latent.

Native chart reading sharpens this further. When we learn the latent from `behavior + i7 + language` and then read the existing charts back from that latent:

- all three charts remain readable from the latent;
- but they differ in how well their geometry matches the native latent.

In the present experiments:

- `behavior_8d` is the chart whose geometry is most aligned with the native latent;
- `i7` is more compressed, but remains the most deployable chart;
- `raw4` is the coarsest relation chart.

This yields the most stable current theoretical positioning of the entire project:

- the present work should not be read as proving that `4D -> 8D -> i7` is the final ontological decomposition of companion dialogue control;
- it is better read as discovering a practically useful chart decomposition:
  - `raw4` as a coarse relation chart
  - `8D behavior` as the most native analytic chart among the current hand-defined views
  - `i7` as the strongest deploy chart
- and as showing that these charts are connected by a richer shared interaction structure rather than exhausting it.

---

## References Placeholder

This draft intentionally leaves the reference section open. The final paper should ground itself in at least the following neighboring literatures:

- controllable dialogue generation
- persona consistency / long-term dialogue
- partner state / social signal modeling
- LLM controllability and structured intermediate representation

> **Placeholder:** Final citation list to be added after the experimental narrative is frozen.

---

## Appendix Placeholder

Possible appendix contents:

- full case templates
- judge rubrics
- interface-family definitions (`i4/i6/i7/i8`)
- hybrid mode definitions
- repeated sampling details
- implementation notes for phase-sensitive hard constraints
