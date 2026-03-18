# Paper Line Synthesis

## One-sentence paper claim

Explicit relational control for long-horizon companion dialogue is worthwhile, but only when analytic charts and deployable charts are separated: the best current real controller is direct `relation -> i7`, while `relation -> behavior(8D) -> i7` is better retained as an analytic bridge than as the main deploy route. The strongest current paper claim is therefore a chart-decomposition claim, not a proof that layered structure is ontologically privileged over every richer one-layer alternative. In the current decomposition, `4D relation` serves as a coarse relation-state chart for recording change over the interaction trajectory, while `i7` serves as the deploy chart for stable execution.

## What the paper is really about

This is not a paper claiming that we discovered the model's true internal relational ontology.

It is a paper about three linked questions:

1. Can explicit relational control beat a genuinely strong prompt baseline in long-horizon companion dialogue?
2. If explicit control helps, what kind of execution interface is actually deployable for a general-purpose LLM?
3. How should analytic layers and deployable layers be separated once we observe that oracle-side explanatory structure and real deploy success are not the same thing?

## The research line

### Stage 1. Establish the real problem

Early smoke and short-form runs showed that short cases were too weak to reveal relational drift.

The project therefore moved to long-horizon multi-phase cases and adopted a strong prompt baseline rather than a weak prompt-only foil.

Key takeaway:

- the benchmark is nontrivial because the strong baseline is already strong.

### Stage 2. Single-layer vs decomposed control

We compared:

- strong prompt baseline
- single-layer explicit relational control
- decomposed control with relation projected into explicit execution constraints

Key takeaway:

- single-layer control is weaker;
- the decomposed controller has real promise;
- but real-chain gains do not automatically appear at the language layer.

### Stage 3. Oracle and hybrid diagnostics

We then separated:

- relation-state quality
- relation-to-behavior projection
- deploy interface construction
- final language realization

Key takeaway:

- oracle decomposed routes are better than real ones;
- this means the idea is not empty;
- but the gap is not just "explicit state good / bad";
- it lives in how analytic structure is turned into an executable deploy chart.

### Stage 4. Freeze the deploy route

After expanding the oracle execution set and repeating the main comparisons, the deploy-side result stabilized:

- best deploy route: `relation -> i7 direct`
- strongest current real candidate: `explicit_rel_state_rel_to_interface_i7_sc_vA`

At the same time:

- corrected `relation -> fitted 8D behavior -> i7` stayed close to oracle behavior and oracle deploy routes
- so it was retained as an analytic bridge

Key takeaway:

- deployment and explanation should be separated;
- deploy chart and analytic chart are not the same object;
- `4D relation` and `i7` are not the same object either: the former records relational change, the latter executes the current state.

### Stage 5. Ontology and wording ablation

We compared:

- ontology variants `vA / vB / vC`
- framing variants `sa / sb / sc`

using both proxy summaries and collaborative manual reading.

Key takeaway:

- `vA` remains the best default ontology;
- `sc` is the best framing;
- `vC` is not a failed idea, but a vulnerability-sensitive alternative;
- projected routes remain more tool-like and explanatory, so they are not the preferred main deploy route.

## Frozen conclusions

The current paper can safely freeze the following conclusions:

1. Strong prompt baselines are genuinely competitive.
2. Single-layer relational control is weaker than the current decomposed controller, but the remaining causal-isolation question is not binary: current evidence now suggests that both matter, with a large share of the gain coming from the `i7` interface and an additional share coming from explicit relation-chart decomposition.
3. The current decomposed controller is not reducible to "just a better prompt."
4. The best current deployable controller is direct `relation -> i7`.
5. The strongest current real configuration is `direct sc_vA`.
6. `vA` is the default deploy ontology.
7. `vC` is a vulnerability-sensitive alternative, not the new default.
8. `relation -> behavior(8D) -> i7` should be retained as an analytic bridge.

The paper can also make one narrower interface-family claim:

- `i7` is the strongest deploy chart among the interface families we explicitly evaluated.
- a focused `i6 / i7 / i8` supplement strengthens that boundary-setting story:
  - `i6` remains a competitive merged / stronger-clamp alternative,
  - `i8` does not show a stable overall gain over `i7`,
  - and therefore the paper still stops at a best-tested-family claim.
- However, the paper should not claim that the present `i7` field decomposition is already minimal or necessary.
## What not to claim

The paper should not claim:

- that explicit state always beats strong prompt baselines;
- that `raw4` is the true latent relational ontology;
- that `behavior_8d` is the true intermediate layer the model internally uses;
- that manifold analyses here directly recover the model's real internal representation.

## Recommended paper structure

### 1. Introduction

- Long-horizon companion dialogue needs relational continuity, not just local helpfulness.
- Strong prompt baselines are already good.
- The real question is what kind of explicit control remains useful under that stronger baseline.

### 2. Problem setup

- relational coherence
- abrupt relational shift
- slow-variable relational-state assumption

### 3. System formulations

- strong prompt baseline
- single-layer control
- decomposed control
- oracle and hybrid controls

### 4. Experimental setup

- long-horizon oracle execution cases
- evaluation protocol
- manual judge and pairwise reading as final evidence

### 5. Main results

- strong baseline competitiveness
- single-layer vs decomposed control
- deploy freeze: `relation -> i7 direct`
- bridge freeze: `relation -> behavior(8D) -> i7`

### 6. Deploy ontology results

- ontology/framing ablation
- `vA` default, `sc` best framing
- `vC` as vulnerability-sensitive alternative

### 7. Analytic/deploy separation

- why deploy chart and analytic bridge should be distinguished
- why projected routes remain useful analytically but not as the preferred deploy route

### 8. Conservative geometric reading

- chart-role clarification only
- `behavior_8d` as the most native analytic chart
- `i7` as the deploy chart
- `raw4` as coarse chart
- no strong claim about model-internal ontology

### 9. Discussion

- what this work establishes
- what remains open
- why a later model-native response-manifold line should be treated as a separate follow-on research program

## Writing stance

The safest high-level writing stance is:

- this paper establishes a usable explicit control decomposition for long-horizon companion dialogue;
- it identifies the current best deploy route and the current best analytic bridge;
- and it closes by clarifying the role of the current charts without overclaiming that they are the model's true internal ontology.
