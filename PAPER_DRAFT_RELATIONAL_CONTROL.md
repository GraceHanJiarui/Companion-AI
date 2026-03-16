# Draft Paper: Two-Layer Relational Control for Long-Term Companion Dialogue

## Title

**Two-Layer Relational Control for Long-Term Companion Dialogue: Strong Baselines, Oracle Gaps, and Executable Interfaces**

Alternative titles:

- **Single-Layer vs Two-Layer Relational Control in Long-Term Companion Dialogue**
- **From Relational State to Executable Behavior Control in Long-Horizon Companion Dialogue**
- **Realization Gaps in Structured Relational Control for Long-Term Companion Dialogue**

---

## Abstract

Large language models can produce fluent companion-style dialogue, but maintaining a coherent sense of relationship over long-horizon interaction remains difficult when control relies only on prompt instructions. A natural systems hypothesis is to introduce explicit relational state as an intermediate control layer. However, whether such structured control actually improves language-level relational coherence, and what kind of control interface is most executable for a general-purpose LLM, remains unclear. In this paper, we study long-term companion dialogue through the lens of relational drift, abrupt relational shifts, and case-level coherence. We compare a strong prompt baseline, a single-layer relational-control formulation, and a two-layer formulation that maps relational state into explicit behavior constraints before generation. We further introduce oracle controls and hybrid diagnostics to separate state updating, relation-to-behavior mapping, and final language realization. Our current evidence suggests that strong prompt baselines are highly competitive, that single-layer relational control is weaker than two-layer control, and that the best two-layer interface can outperform the strong baseline in oracle form while still exhibiting a substantial real-chain gap. Repeated sampling supports a stable ordering of `oracle i7 > real i7 > baseline` for the current best execution interface. The remaining gap appears to arise primarily from behavior-side control mismatch rather than from high-level relational stance description alone.  

**Placeholder:** The final abstract should be updated after completing the remaining Stage-2 experiments: `mixed_signal` and the final frozen full-run judge.

---

## 1. Introduction

Long-term companion dialogue is not just a sequence of locally helpful responses. It is also a process in which the system must maintain a stable, interpretable, and non-jumping sense of relationship over time. Prompt-only systems can often sound locally good while still exhibiting relational drift: they may become abruptly warmer, colder, more over-involved, or more distant than the interaction history supports.

A common engineering response is to introduce explicit intermediate state: track relationship variables, update them conservatively, and use them to shape downstream behavior. This idea is intuitively attractive, but intuition alone is insufficient. A structured control layer may be internally coherent yet fail to produce better language behavior, especially when realized through an unmodified general-purpose LLM. Strong prompt baselines may also already capture much of the visible gain.

This paper asks a focused question: **when relational control is made explicit, what kind of control interface is actually executable for long-term companion dialogue?** In particular, we study the contrast between:

- a **strong prompt baseline** that uses high-level relational instruction only;
- a **single-layer relational control** formulation that directly conditions generation on relational stance;
- a **two-layer relational control** formulation that first represents relational stance and then projects it into explicit behavior-side constraints before generation.

Our results so far suggest a more nuanced conclusion than “explicit state helps” or “explicit state fails.” Strong baselines are highly competitive. Single-layer control appears weaker than two-layer control. A well-designed two-layer interface shows clear promise in oracle form and retains part of that advantage in the real chain. The remaining gap is not explained primarily by high-level relational stance wording, but appears to depend more heavily on behavior-side control mismatch.

### 1.1 Contributions

The current draft supports the following contributions:

1. We formulate long-horizon companion dialogue as a problem of **relational coherence** and **abrupt relational shift** rather than only local helpfulness.
2. We compare **single-layer** and **two-layer** relational control against a **strong prompt baseline**.
3. We show that **strong prompt baselines remain highly competitive**, making this a nontrivial control problem rather than a weak-baseline artifact.
4. We develop an **oracle and hybrid diagnostic framework** that separates:
   - relational stance,
   - behavior / execution interface,
   - final language realization.
5. We identify a current best two-layer interface (`i7`) whose repeated-sampling behavior supports a stable ordering:
   - `oracle i7 > real i7 > baseline`
6. We provide evidence that the remaining `real i7 -> oracle i7` gap is driven more by **behavior-side mismatch** than by relational-stance wording alone.
7. We localize the dominant current failure point more specifically to the deterministic **relation -> behavior projection mapping**, rather than updater quality alone.

### 1.2 Scope

This paper is intentionally scoped as a **focused mechanism paper**, not a full product paper. It does **not** attempt to solve:

- all questions of relational-state representation design;
- why strong baselines may already encode implicit relational control;
- the full product-level question of controllability vs zero-shot language quality;
- human-human relationship modeling in general.

Those are important follow-on directions, but including them here would make the paper unstable and difficult to defend.

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

This paper does not treat response length as a standalone objective. Instead, lower length is interpreted only as a **coarse proxy** when it aligns with:

- lower over-expansion,
- less compensatory warmth,
- fewer unnecessary follow-ups,
- cleaner adherence to relationship continuity.

Final conclusions rely on:

- manual judge,
- pairwise comparison,
- repeated sampling,
- and hybrid diagnostics taken together.

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

### 5.6 Real i7 vs Oracle i7 vs Strong Baseline

Using the current best interface, repeated runs and manual judge support the ordering:

- `oracle i7 > real i7 > baseline`

This is one of the strongest current results in the paper.

### 5.7 Hybrid Gap Diagnosis

Hybrid experiments currently suggest:

- `oracle_rel_i7` only modestly improves over `real i7`
- `oracle_behavior_i7` is close to `oracle i7`

**Current conclusion:** the main remaining gap is more likely on the behavior / execution-interface side than on the relational-stance wording side.

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

The resulting global average lengths were:

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

In other words, the two-layer route is not being undermined. Instead, the evidence suggests that the second layer is important, but the current projector is translating relational state into the wrong behavior profile.

---

## 6. Discussion

### 6.1 What the Paper Currently Supports

At the current stage, the evidence supports the following claims:

1. Strong prompt baselines are highly competitive in long-term companion dialogue.
2. Single-layer relational control is weaker than two-layer relational control.
3. Two-layer control is not reducible to “just a better single-layer prompt.”
4. A well-designed execution interface matters.
5. The current best interface (`i7`) shows a stable oracle-to-real-to-baseline ordering:
   - `oracle i7 > real i7 > baseline`
6. The current deterministic `relation -> behavior` projector appears to be the dominant remaining bottleneck.

### 6.2 What the Paper Does Not Yet Claim

This paper does **not** yet claim:

- that explicit relational state always yields better language behavior than strong baselines;
- that relation-state representation design has been solved;
- that realization gaps are fully understood;
- that the current system is already product-optimal.

### 6.3 Why This Is Still a Strong Result

The interesting result is not simply that “explicit state works.” Rather, the more valuable finding is:

- structured control that appears intuitively reasonable does **not** automatically translate into better language-level behavior;
- two-layer control has real potential, but that potential must be realized through an executable behavior interface;
- strong baselines can already absorb much of the visible gain, which makes the remaining mechanism analysis essential.

This is a stronger and more defensible story than a naive “structured state beats baseline” narrative.

---

## 7. Limitations

### 7.1 Case Scale

Current experiments rely on carefully designed long-range cases rather than large naturally collected datasets.

### 7.2 Judge Scale

Much of the current evidence relies on:

- manual judge,
- limited pairwise comparison,
- repeated sampling,

rather than a fully scaled final judge pass.

### 7.3 Mixed-Signal Coverage

The mixed-signal case family is not yet fully integrated into the frozen final results.

### 7.4 Mechanism Diagnosis Still In Progress

The final decomposition of:

- updater,
- projection mapping,
- final realization

is not yet fully complete.

---

## 8. Conclusion

This paper studies explicit relational control for long-term companion dialogue under a stronger and more realistic setup than a simple prompt-vs-state comparison. We find that strong prompt baselines are difficult to beat, that single-layer relational control is insufficient, and that two-layer control with an executable interface is substantially more promising. The best current interface (`i7`) shows stable superiority over the strong baseline in oracle form and partial retention of that advantage in the real chain. Current evidence further suggests that the main remaining bottleneck lies more on the behavior / execution-interface side than on relational stance wording alone.

If the remaining Stage-2 experiments continue to support this pattern, the final paper should argue that:

- two-layer relational control is a viable and meaningful direction for long-horizon companion dialogue;
- the critical issue is not merely whether to use structured relational state, but how to turn it into a behavior-side interface that a general-purpose LLM can actually execute.

> **Placeholder:** The final wording of the conclusion must be updated after:
> - `oracle relation state + real projection`
> - `mixed_signal`
> - final frozen full-run judge

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
