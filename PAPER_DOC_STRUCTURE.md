# Paper Document Structure

## Purpose

This file reorganizes the current paper-related markdown files into:

1. primary documents to keep active
2. secondary documents that can be merged or downgraded
3. archival notes that should not drive the main paper anymore

The goal is to reduce document sprawl without losing experimental history.

## Current file inventory

Main paper-related files currently present:

- `PAPER_DRAFT_RELATIONAL_CONTROL.md`
- `PAPER_EXECUTION_PLAN.md`
- `PAPER_EXPERIMENT_REGISTRY.md`
- `PAPER_JUDGE_TEMPLATES.md`
- `PAPER_LONG_RANGE_CASE_DESIGN.md`
- `PAPER_MINI_SCOPE_GO_NO_GO.md`
- `PAPER_PROJECTOR_ANALYSIS.md`
- `PAPER_PROJECTOR_ROUTE_CLARIFICATION.md`
- `PAPER_PROMPT_BRIDGING_EXPERIMENT.md`
- `PAPER_PROPOSAL_RELATION_STATE.md`
- `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`
- `PAPER_STAGE2_I7_STATUS.md`
- `PAPER_TWO_STAGE_STRATEGY.md`

## Recommended target structure

### Keep as primary active documents

These should remain the main working set:

1. `PAPER_DRAFT_RELATIONAL_CONTROL.md`
   - primary paper draft
   - should absorb stable findings and finalized framing

2. `PAPER_EXPERIMENT_REGISTRY.md`
   - canonical experiment log and reproduction index
   - should remain the source of truth for:
     - experiment purpose
     - commands
     - output files
     - main conclusions

3. `PAPER_EXECUTION_PLAN.md`
   - active next-step execution plan
   - should contain only current and future work, not old exploratory debate

4. `PAPER_PROPOSAL_RELATION_STATE.md`
   - high-level research framing and scope definition
   - should remain as the concise conceptual anchor

### Keep as focused technical supplements

These are still useful, but should no longer behave like parallel main documents:

5. `PAPER_PROJECTOR_ANALYSIS.md`
   - focused technical note for projector-gap diagnosis
   - keep as a dedicated analysis memo

6. `PAPER_JUDGE_TEMPLATES.md`
   - useful reusable evaluation specification
   - keep as a reference file

## Recommended merge / downgrade candidates

### Merge into `PAPER_EXPERIMENT_REGISTRY.md`

These are experiment-specific notes whose content largely belongs in the registry:

1. `PAPER_PROMPT_BRIDGING_EXPERIMENT.md`
   - status: mostly experiment-specific
   - recommendation: merge stable conclusions into the registry, then downgrade this file to archival reference

2. `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`
   - status: very specific result memo
   - recommendation: merge stable result summary into the registry and draft, then archive

3. `PAPER_STAGE2_I7_STATUS.md`
   - status: transient status snapshot
   - recommendation: merge its surviving conclusions into the registry / draft, then archive

### Merge into `PAPER_PROPOSAL_RELATION_STATE.md` or `PAPER_EXECUTION_PLAN.md`

4. `PAPER_PROJECTOR_ROUTE_CLARIFICATION.md`
   - status: important conceptual clarification
   - recommendation: merge into proposal and execution plan once encoding is normalized
   - until then, keep as addendum

5. `PAPER_LONG_RANGE_CASE_DESIGN.md`
   - status: design memo
   - recommendation:
     - keep only if case design is still evolving
     - otherwise compress key principles into proposal or execution plan and archive this file

6. `PAPER_TWO_STAGE_STRATEGY.md`
   - status: historically useful
   - recommendation:
     - its core outcome has already been absorbed by the current paper direction
     - downgrade to archival background

7. `PAPER_MINI_SCOPE_GO_NO_GO.md`
   - status: early-stage steering memo
   - recommendation:
     - much of its role has been superseded by the current execution plan
     - archive after preserving any still-live go/no-go criteria in `PAPER_EXECUTION_PLAN.md`

## Recommended archival set

These should be treated as historical process documents rather than active paper drivers:

- `PAPER_MINI_SCOPE_GO_NO_GO.md`
- `PAPER_TWO_STAGE_STRATEGY.md`
- `PAPER_STAGE2_I7_STATUS.md`
- `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`
- `PAPER_PROMPT_BRIDGING_EXPERIMENT.md`

Archival does not mean delete immediately.
It means:

- stop editing them as active sources of truth
- keep them for traceability
- rely on registry / proposal / draft instead

## Suggested minimal active set

If we want the cleanest workable paper-doc set, the active set should be reduced to:

- `PAPER_DRAFT_RELATIONAL_CONTROL.md`
- `PAPER_PROPOSAL_RELATION_STATE.md`
- `PAPER_EXECUTION_PLAN.md`
- `PAPER_EXPERIMENT_REGISTRY.md`
- `PAPER_PROJECTOR_ANALYSIS.md`
- `PAPER_JUDGE_TEMPLATES.md`

Everything else should either:

- be merged gradually into one of the files above, or
- be marked archival and left untouched

## Practical merge order

Recommended merge order:

1. merge stable experimental conclusions from:
   - `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`
   - `PAPER_STAGE2_I7_STATUS.md`
   - `PAPER_PROMPT_BRIDGING_EXPERIMENT.md`
   into `PAPER_EXPERIMENT_REGISTRY.md`

2. merge stable conceptual clarifications from:
   - `PAPER_PROJECTOR_ROUTE_CLARIFICATION.md`
   - `PAPER_LONG_RANGE_CASE_DESIGN.md`
   into `PAPER_PROPOSAL_RELATION_STATE.md` and `PAPER_EXECUTION_PLAN.md`

3. keep `PAPER_DRAFT_RELATIONAL_CONTROL.md` as the only writing-oriented document
   - it should not duplicate raw experiment logs

## Immediate recommendation

Do not try to merge everything at once.

Instead:

1. freeze the archival documents
2. continue editing only the active set
3. merge one cluster at a time when encoding and formatting are safe

At the current stage, the highest-value merges are:

- stage-2 status -> experiment registry
- repeated sampling summary -> experiment registry
- projector route clarification -> proposal / execution plan
