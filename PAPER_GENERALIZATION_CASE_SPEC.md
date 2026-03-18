# Generalization Case Spec

## Purpose

This document defines the next-stage case specification for a true generalization set.

It is intentionally **not** a case file. Its purpose is to prevent us from writing more
label-shaped cases that merely paraphrase the existing oracle skeleton.

The core distinction is:

- the current oracle/long case program is a **controlled mechanism set**
- the next generalization set must be a **trajectory-tension set**

In other words, the new set should be organized around what kind of user-side
interaction path is unfolding, what the user is trying to maintain, what the user
is trying to prevent, and what the model is most likely to misread.

## What Went Wrong In The Previous Semi-Natural Drafts

The main issue was not literal duplication. The main issue was that the cases still
shared the same functional six-step skeleton:

1. ordinary opening
2. first signal
3. stabilization
4. refinement
5. ordinary continuation
6. final probe

This makes them suitable as controlled diagnostic examples, but too schematic to
serve as natural-distribution evidence.

The next generalization set must therefore satisfy:

- signal positions are not fixed
- user-side trajectory shape is not fixed
- family cues are not always explicit
- ordinary-topic distribution is substantially broader
- some ambiguity, self-correction, and messiness is allowed

## Roles Of The Existing Sets

### Controlled Mechanism Set

The following files remain valid as controlled mechanism sets:

- [paper_cases_oracle_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v3.json)
- [paper_cases_long_v1.json](d:/My%20Project/companion-ai/paper_cases_long_v1.json)

These sets are still appropriate for:

- route comparison
- bridge analysis
- structure-vs-interface analysis
- deploy ontology/framing analysis

They should not be over-claimed as natural-distribution evaluation.

### Not Yet Valid As Generalization Set

The following files should currently be treated as exploratory drafts only:

- [paper_cases_semi_natural_v1.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v1.json)
- [paper_cases_semi_natural_v2.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v2.json)

They are not yet strong enough to support a paper-facing generalization claim.

## General Writing Rules For New Generalization Cases

### Allowed Structure

New cases may still use six turns for convenience, but they must not reuse a fixed
functional position mapping.

Examples of acceptable variation:

- the first positive relational signal appears only at turn 4
- the user starts by setting distance, then later softens
- a case contains no explicit final probe
- a case contains a failed topic shift before later stabilization
- a case includes mild contradiction or self-correction

### Prohibited Pattern

The following pattern should be explicitly avoided:

- turn 1 = ordinary opening
- turn 2 = first family-defining signal
- turn 3 = stabilization rule
- turn 4 = refinement sentence
- turn 5 = ordinary continuation request
- turn 6 = final request to keep current style

If a new case obviously fits this template, it should be rejected or rewritten.

### Topic Distribution

The next set should expand far beyond the current recurring themes of:

- empty evenings
- sleepless nights
- mind not slowing down
- light entertainment filler

Future topics should include broader ordinary-life contexts, for example:

- commute home
- cooking / cleaning / showering
- late afternoon weekend drift
- scrolling but not wanting to keep scrolling
- errands, grocery stores, walks, waiting rooms
- workday transitions
- post-event decompression

### Surface Realism

The next set should allow:

- unfinished thoughts
- softened corrections
- low-information turns
- slight contradiction
- non-taxonomic wording

It should avoid:

- textbook family labels in user language
- overly explicit meta-instructions
- clean didactic distinctions that only exist for evaluator convenience

## Family Definitions As Trajectory Tensions

The families below are defined by user-side trajectory tensions, not by prewritten
prompt templates and not by pre-assigned `i7` values.

### 1. Warming Trajectory

Core trajectory:

- the user becomes slightly more willing to remain in interaction
- the user gives weak positive relational feedback
- the user does **not** authorize sudden intimacy

The user is trying to maintain:

- low-pressure continuation
- slightly increased comfort
- ordinary, non-heavy contact

The user is trying to prevent:

- sudden over-closeness
- compensation through excessive warmth
- being treated as if they have invited a major relational upgrade

Likely model misread:

- reading "that felt okay" as "you can now move closer"

Acceptable system movement:

- mild warmth increase
- slightly steadier presence
- no large jump in affective follow-up

### 2. Vulnerability With Correction

Core trajectory:

- the user is in visible difficulty or low capacity
- the user wants presence more than intervention
- the user later narrows what kind of support is acceptable

The user is trying to maintain:

- low-pressure holding
- non-theatrical acknowledgement
- room to stay partially closed

The user is trying to prevent:

- therapy mode
- being over-managed
- being framed as a dramatic crisis unless they themselves go there

Likely model misread:

- treating vulnerability as permission for heavy support or advice

Acceptable system movement:

- more grounded presence
- not more intervention
- correction-sensitive tone adjustment

### 3. Cooling Trajectory

Core trajectory:

- the user explicitly or implicitly reduces desired relational intensity
- interaction remains open, but contact should become lighter and less intrusive

The user is trying to maintain:

- ordinary conversation
- low burden
- lower emotional presence

The user is trying to prevent:

- feeling emotionally held
- being managed
- being read as wanting deep connection

Likely model misread:

- counteracting cooling with compensatory warmth
- or overcorrecting into blunt coldness

Acceptable system movement:

- lower warmth band
- lower initiative
- stable ordinary responsiveness

### 4. Mixed-Signal Trajectory

Core trajectory:

- the user gives some positive relational signal
- but also restricts what that signal should mean
- the user may partially reopen later without granting full escalation

The user is trying to maintain:

- a narrow middle band:
  - not cold
  - not over-close

The user is trying to prevent:

- overreading
- binary interpretation
- being forced into a clearer relation definition than they actually offered

Likely model misread:

- converting mixed signals into a one-direction relationship upgrade

Acceptable system movement:

- acknowledge signal
- keep interpretation narrow
- remain locally adaptive without committing to a hotter trajectory

### 5. Boundary Repair

Core trajectory:

- the system has effectively become too warm / too managing / too close
- the user explicitly asks for recalibration
- the key question is whether the system can recover without becoming awkward

The user is trying to maintain:

- continued interaction
- a restored normal distance
- confidence that correction will be respected

The user is trying to prevent:

- defensive self-explanation
- exaggerated apology
- repairing in a way that itself becomes another relational performance

Likely model misread:

- treating repair as a deeper relational negotiation
- or collapsing into lifeless, over-withdrawn responses

Acceptable system movement:

- rapid recalibration
- lower heat
- no self-justifying meta spiral

### 6. Ordinary Neutral

Core trajectory:

- the user is not clearly warming, cooling, repairing, or disclosing vulnerability
- the main risk is unnecessary relationship invention by the model

The user is trying to maintain:

- ordinary talk
- low interpretive load
- low drama

The user is trying to prevent:

- being turned into a companion-drama script
- unwanted warmth escalation
- forced intimacy cues

Likely model misread:

- manufacturing relationship significance where none is needed

Acceptable system movement:

- remain ordinary
- keep continuity without adding symbolic relational weight

## Acceptance Checklist For A New Generalization Case

A new case should only enter the paper-facing generalization set if all items below
are satisfied.

1. It is readable without obvious "test question" texture.
2. Its family is identifiable from trajectory tension, not just from one explicit line.
3. The family-defining signal does not merely occur at the same fixed slot used in the oracle set.
4. The topic distribution is not just a rephrasing of the current evening / insomnia / empty-time cluster.
5. The user wording does not read like ontology annotation in disguise.
6. The case would still make sense if shown to a reader with no access to the taxonomy labels.

## Intended Use In The Paper

If a future generalization set is built from this spec, it should be used only for:

- generalization / robustness checks
- limited-mode controller comparisons

It should not replace the oracle mechanism set.

The recommended division remains:

- controlled mechanism claims:
  - oracle/long structured cases
- generalization claims:
  - future semi-natural / external sets built from this spec
