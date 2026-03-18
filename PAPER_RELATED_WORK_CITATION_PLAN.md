# Related Work Citation Plan

This file maps the current citation placeholders in
`PAPER_DRAFT_RELATIONAL_CONTROL_V2.md` to concrete literature buckets.

It is a planning file, not a final bibliography.

## Bucket 1. Controllable Dialogue / Controlled Generation

Placeholder in draft:

- `[CITATION: controllable dialogue / controllable generation]`

What this bucket should cover:

- explicit control attributes for dialogue generation
- planning variables or controllable generation interfaces
- structured guidance for response style or behavior

What the citation should do in the paper:

- establish that explicit intermediate control in dialogue is a real prior line
- distinguish our work by:
  - using long-horizon companion dialogue
  - evaluating under a strong prompt baseline

Candidate papers:

- Keskar et al., "CTRL: A Conditional Transformer Language Model for Controllable Generation"
- Dathathri et al., "Plug and Play Language Models: A Simple Approach to Controlled Text Generation"
- representative controllable dialogue papers to add after final bibliography pass

## Bucket 2. Persona Consistency / Long-Term Dialogue

Placeholder in draft:

- `[CITATION: persona consistency / long-term dialogue]`

What this bucket should cover:

- maintaining stable persona across turns
- long-term consistency in multi-turn dialogue
- memory/persona-grounded conversation

What the citation should do in the paper:

- establish that dialogue consistency has prior work
- distinguish our work by:
  - focusing on relational trajectory rather than only persona/profile consistency

Candidate papers:

- Xu et al., "Long Time No See! Open-Domain Conversation with Long-Term Persona Memory"
- Maharana et al., "Evaluating Very Long-Term Conversational Memory of LLM Agents"
- Lee et al., "REALTALK: A 21-Day Real-World Dataset for Long-Term Conversation"

## Bucket 3. Partner State / Social Signal / User State

Placeholder in draft:

- `[CITATION: partner state / social signal / user state]`

What this bucket should cover:

- dialogue systems that model user state, affect, engagement, or social stance
- systems that explicitly estimate partner-side conversational variables

What the citation should do in the paper:

- position the relation-state layer near user-state / partner-state modeling
- clarify that this paper is narrower and does not claim full human relationship modeling

Candidate papers:

- dialogue user-state / affect / engagement modeling papers to finalize in bibliography pass
- long-term personalized dialogue memory-management papers such as:
  - Tan et al., "In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents"
  - Zhao et al., "Inside Out: Evolving User-Centric Core Memory Trees for Long-Term Personalized Dialogue Systems"

## Bucket 4. Controllability / Intermediate Representation / Geometry

Placeholder in draft:

- `[CITATION: controllability / intermediate representations / representation geometry]`

What this bucket should cover:

- structured intermediate representations in LLM control
- representation geometry / latent-space reading
- work adjacent to the late chart-structure analysis

What the citation should do in the paper:

- justify why it is reasonable to discuss analytic charts and deploy charts separately
- make clear that our late geometric analysis is conservative and not a claim of internal ontology discovery

Candidate papers:

- work on hidden-representation geometry in transformers
- work on representation of structured variables in language models
- Schur et al., "Concept Bottleneck Models Without Predefined Concepts"
- candidate neighboring references already discussed in project notes:
  - "The Geometry of Hidden Representations of Large Transformer Models"
  - "Language Models Represent Space and Time"

## Writing rule

When filling the final bibliography:

- use these citations only to locate the paper in neighboring literatures;
- do not overclaim novelty against broad prior areas;
- keep the paper's novelty claim focused on:
  - strong-baseline relational control,
  - deploy-chart vs analytic-chart separation,
  - and the frozen empirical result line.
