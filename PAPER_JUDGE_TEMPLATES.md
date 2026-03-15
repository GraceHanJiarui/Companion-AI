# Paper Judge Templates

## Purpose

This file freezes the first-stage judge templates for the seed-paper route. The main question is not whether a reply is simply "better", but whether it is **more relationally coherent across turns** and **less prone to abrupt relational shifts**.

The first-stage judge should therefore prioritize:

1. case-level relational coherence
2. abrupt relational shift detection
3. pairwise preference on coherence

It should not prioritize:

- wording elegance
- generic helpfulness
- internal state terminology such as four-dimensional relation labels or eight behavior dimensions

---

## A. Case-Level Judge Template

### Input

- `case_id`
- `experiment_mode`
- full multi-turn dialogue:
  - each turn contains `user_text`
  - each turn contains `assistant_text`

### Judge Prompt

```text
你现在是一个对长期对话进行评审的 judge。

任务：
请判断下面这整段多轮对话，是否像“同一个关系过程”在连续演化，以及是否出现明显的关系跳变。

评判重点：
1. 只根据用户输入与助手输出判断，不使用任何内部状态术语。
2. 优先看跨轮关系姿态是否连续，而不是单轮文案是否漂亮。
3. 如果只是语气略有变化，但仍像同一关系过程，不要轻易判为 abrupt shift。

“abrupt shift” 包括但不限于：
- 突然明显更亲近，但缺乏前文铺垫
- 突然明显更冷淡或抽离，但缺乏前文触发
- 在用户降温/要求正常互动后出现补偿性热情
- 相邻轮之间关系姿态变化明显超过上下文支持的程度

请输出 JSON，对应字段如下：
{
  "relational_coherence_score_1_to_5": 1-5 的整数,
  "has_abrupt_shift": true/false,
  "abrupt_shift_turns": [在什么 turn_idx 开始出现明显跳变；如果没有则为空数组],
  "reason": "用 1-4 句中文简要说明理由"
}

评分标准：
5 = 整段对话高度连贯，关系姿态自然连续，没有明显跳变
4 = 整体连贯，只有轻微不自然，但不影响关系过程连续感
3 = 基本可接受，但存在一两处可感知的不稳定或姿态摇摆
2 = 明显不连贯，至少有一处关系姿态突变或补偿性热情
1 = 严重不连贯，整段对话缺乏稳定关系过程，像不同阶段或不同角色拼接而成

下面是待评审对话：
{{dialogue_block}}
```

---

## B. Pairwise Judge Template

### Input

- `case_id`
- `left.experiment_mode` with full multi-turn dialogue
- `right.experiment_mode` with full multi-turn dialogue

### Judge Prompt

```text
你现在是一个对长期对话进行 pairwise 比较的 judge。

任务：
比较下面两段多轮对话，判断哪一段更像“同一个关系过程”在连续演化，并且更少出现突兀的关系跳变。

评判重点：
1. 不要比较文采、长度或帮助性本身，主看关系连贯性。
2. 如果两边都差不多连贯，返回 tie。
3. 如果一边更像稳定持续的关系过程，优先选那一边。

优先依据：
- 更少 abrupt relational shift
- 更像同一个关系过程持续演化
- 相邻轮之间姿态变化更自然

请输出 JSON：
{
  "winner": "left" | "right" | "tie",
  "reason": "用 1-4 句中文简要说明理由"
}

左侧对话：
{{left_dialogue_block}}

右侧对话：
{{right_dialogue_block}}
```

---

## C. Suggested Use Order

1. First run case-level judging on a small smoke subset.
2. If the case-level results appear self-consistent, then run pairwise judging.
3. Only after the main case-level and pairwise results look meaningful should you expand to larger runs or auxiliary analyses such as realization gap.

---

## D. What Counts As a Good First-Stage Signal

- `explicit_rel_state_direct` is preferred over at least two baselines in pairwise comparison.
- `explicit_rel_state_direct` shows higher case-level relational coherence on the same cases.
- `explicit_rel_state_projected` may or may not outperform `direct`; at stage one, that is an extension question rather than the main success criterion.
