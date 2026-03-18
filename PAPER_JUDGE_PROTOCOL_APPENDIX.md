# Appendix: Judge Protocol Specification

## Purpose

This appendix freezes the judge protocol used for paper-facing relational evaluation.
It is intended to make the main evaluation more reproducible and less dependent on
informal one-off reading.

This appendix does not claim to replace human judgment with a perfect metric.
Instead, it defines a stable judge procedure for a judge-centered construct:
relational coherence over multi-turn dialogue.

The paper-facing evaluation should be understood as a multi-evidence protocol:

1. structured case-level judge labels
2. pairwise preference judge
3. multi-judge agreement
4. lightweight automatic diagnostics

No single scalar is treated as sufficient on its own.

## A. Evaluation Units

Two judge units are used.

1. Case-level judging
   - input: one full multi-turn case from one mode
   - output: structured relational annotation plus overall coherence judgment

2. Pairwise judging
   - input: the same full multi-turn case from two modes
   - output: left / right / tie preference with reason

## B. Fixed Decoding Settings

Recommended frozen settings for paper-facing judge runs:

- temperature: `0.0`
- top_p: default
- max judge samples per case: `3`

If a lighter exploratory package is needed, use:

- temperature: `0.2`
- max judge samples per case: `3`

The paper should report which setting was used.

## C. Blindness

Judges should not be shown raw mode names such as:

- `baseline_relational_instruction`
- `explicit_rel_state_rel_to_interface_i7_sc_vA`
- `explicit_rel_state_projected_oracle_i7`

Instead, render anonymous labels:

- `System A`
- `System B`
- `System C`

If pairwise judging is used, randomize left/right order.

## D. Number of Judges

Minimum recommended setup:

- `2` independent judges

Stronger setup:

- `3` independent judges

Judges may be:

- human readers
- or LLM judges using fixed prompt wording with independent seeds / order randomization

The paper should state which one was used.

Recommended practical setup for the current project:

- `3` judge runs with the same frozen prompt
- temperature `0.0`
- either:
  - different seeds
  - or different left/right randomization and anonymized system labels

This is sufficient to report a paper-facing raw-agreement number even before a larger human study.

## E. Agreement Reporting

Minimum required reporting:

- raw agreement percentage

For pairwise judging:

- percentage of pairwise decisions with identical winner labels

For case-level judging:

- percentage agreement on:
  - `has_abrupt_shift`
  - `unsupported_warmth_increase`
  - `unsupported_distance_increase`
  - `unsupported_initiative_jump`
  - `continuation_reopen_after_cooling`
  - `final_probe_overshoot`
  - binned coherence score (`1-2`, `3`, `4-5`) or exact score

If stronger reporting is wanted later, Cohen's kappa or Krippendorff's alpha may
be added, but raw agreement is sufficient for the current paper.

Agreement can be computed with:

- [paper_judge_agreement.py](d:/My%20Project/companion-ai/paper_judge_agreement.py)

## F. Case-Level Judge Prompt

Use the following fixed prompt wording.

```text
You are evaluating a long-horizon dialogue case.

Your task is to judge whether this full multi-turn dialogue feels like one coherent
relationship process unfolding over time, rather than a sequence of locally plausible
but interactionally reset replies.

Evaluation priorities:
1. Judge only from user turns and assistant turns.
2. Prioritize cross-turn continuity over single-turn elegance.
3. Do not reward verbosity or generic helpfulness by default.
4. A mild tone change is not automatically an abrupt shift if it still fits the same
   ongoing interaction process.

An abrupt shift may include:
- unsupported warmth increase
- unsupported distance increase
- compensatory warmth after the user has cooled interaction down
- reopening continuation or final-probe behavior beyond what the trajectory supports

Return JSON with exactly these fields:
{
  "trajectory_continuity_1_to_5": 1-5 integer,
  "user_request_preservation_1_to_5": 1-5 integer,
  "overinterpretation_1_to_5": 1-5 integer,
  "continuation_probe_control_1_to_5": 1-5 integer,
  "unsupported_warmth_increase": true/false,
  "unsupported_distance_increase": true/false,
  "unsupported_initiative_jump": true/false,
  "continuation_reopen_after_cooling": true/false,
  "final_probe_overshoot": true/false,
  "trajectory_reset_present": true/false,
  "has_abrupt_shift": true/false,
  "abrupt_shift_turns": [turn indices or empty array],
  "overall_relational_coherence_1_to_5": 1-5 integer,
  "reason": "1-4 sentence explanation"
}

Scoring guidance:
5 = highly coherent; same relational process throughout; no meaningful break
4 = coherent overall; minor roughness but no meaningful break
3 = acceptable but noticeably unstable in one or two places
2 = clearly unstable; at least one obvious unsupported relational move
1 = fragmented; does not feel like one ongoing relationship trajectory

Dialogue:
{{dialogue_block}}
```

## G. Pairwise Judge Prompt

Use the following fixed prompt wording.

```text
You are comparing two long-horizon dialogue trajectories for relational coherence.

Your task is to decide which trajectory better preserves the same ongoing
relationship process across turns.

Evaluation priorities:
1. Do not reward verbosity, elegance, or generic helpfulness by default.
2. Prefer the trajectory with less abrupt relational shift.
3. Prefer the trajectory with less overinterpretation and less compensatory warmth.
4. Prefer the trajectory that keeps ordinary continuation and final-probe turns under control.
5. If both are close, return tie.

Return JSON with exactly these fields:
{
  "winner": "left" | "right" | "tie",
  "better_on_trajectory_continuity": "left" | "right" | "tie",
  "better_on_request_preservation": "left" | "right" | "tie",
  "better_on_shift_control": "left" | "right" | "tie",
  "reason": "1-4 sentence explanation"
}

Left dialogue:
{{left_dialogue_block}}

Right dialogue:
{{right_dialogue_block}}
```

## H. Operational Reading of Relational Coherence

The paper should treat relational coherence as a judge-centered construct, not as
a fully solved scalar metric.

The current operational reading is:

- high coherence means the dialogue still feels like one ongoing relationship process
- low coherence means the trajectory contains unsupported stance changes, trajectory resets,
  or continuation/probe behavior that no longer fits the prior interaction

To make the construct more reproducible, the paper should report not only the overall
coherence score, but also the structured label profile:

- unsupported warmth increase
- unsupported distance increase
- unsupported initiative jump
- continuation reopen after cooling
- final probe overshoot
- trajectory reset present

This is strong enough for a paper-facing evaluation protocol, but should not be
oversold as a complete quantitative theory of relationship.
