# Prompt Bridging Experiment

## 1. 目的

这份文档定义第一步诊断实验：

- **状态显式化输入 + 当前这版 prompt 实现**
- 为什么没有稳定表现出优于强 baseline 的语言层效果

第一步实验不直接回答全部问题，只先回答：

- **这更像是 prompt bridge 的问题，还是更底层的表示 / realization 问题。**

---

## 2. 固定实验对象

第一步只建议在少量 case 上做，例如：

- `long_warm_001`
- `long_vuln_001`

每个 case 只比较：

- `explicit_rel_state_direct`
- `explicit_rel_state_projected`

其内部状态更新机制保持不变。

不变的部分：

- `delta_R` 规范化
- relation state 更新
- projected 里的 behavior projection

唯一改变的是：

- **状态如何被翻译成给生成模型的输入 prompt**

---

## 3. 三种 prompt 变体

## Variant A: 原版状态输入

### 用途

作为当前实现基线。

### direct

- 使用当前 `explicit_rel_state_direct` 的状态释义方式

### projected

- 使用当前 `explicit_rel_state_projected` 的 behavior 输入方式

### 预期作用

这是当前实际表现，不做额外桥接强化。

---

## Variant B: 数值/状态 + 自然语言桥接

### 目的

测试：

- 是否只是因为当前状态喂法太抽象、太硬，导致模型没有把状态稳定兑现成语言。

### direct 建议模板

```text
你现在是一个长期陪伴型对话系统的表达层。

请基于下面的“关系状态说明”来回应用户。

要求：
1. 关系变化必须渐进，不要突然拉近或突然疏离。
2. 用户给出的信号如果只是轻微升温或轻微降温，你的语言也只能做小幅调整。
3. 如果用户没有继续强化关系信号，应维持当前关系轨迹，而不是自行继续升温。
4. 先回应用户当前内容，再体现关系姿态。

【当前关系状态（数值）】
bond={bond}
care={care}
trust={trust}
stability={stability}

【当前关系状态（自然语言解释）】
{rel_state_explanation}

【用户输入】
{user_text}
```

### projected 建议模板

```text
你现在是一个长期陪伴型对话系统的表达层。

请基于下面的“关系状态”和“行为控制说明”来回应用户。

要求：
1. 先回应用户当前内容，再体现姿态。
2. 行为风格只能渐进变化，不能过冲。
3. 如果当前行为说明是克制，就不要写成补偿性热情。

【关系状态】
{rel_state_explanation}

【行为控制（数值）】
E={E}
Q_clarify={Q_clarify}
Directness={Directness}
T_w={T_w}
Q_aff={Q_aff}
Initiative={Initiative}
Disclosure_Content={Disclosure_Content}
Disclosure_Style={Disclosure_Style}

【行为控制（自然语言解释）】
{behavior_explanation}

【用户输入】
{user_text}
```

---

## Variant C: 纯自然语言状态摘要

### 目的

测试：

- 不直接暴露数值，只给自然语言状态摘要，是否更适合未微调 LLM。

### direct 建议模板

```text
你现在是一个长期陪伴型对话系统的表达层。

请基于下面的“当前关系姿态”来回应用户。

要求：
1. 关系变化必须渐进。
2. 如果当前关系仍偏谨慎或偏克制，就不要突然热情。
3. 如果用户刚给出轻微信任或感谢，也只能小幅升温。
4. 先回应内容，再体现关系姿态。

【当前关系姿态】
{relational_summary_only}

【用户输入】
{user_text}
```

### projected 建议模板

```text
你现在是一个长期陪伴型对话系统的表达层。

请基于下面的“当前关系姿态”和“当前行为倾向”来回应用户。

要求：
1. 语言风格必须和这些说明一致。
2. 变化必须渐进。
3. 不要额外放大温暖度、亲近感或主动推进。

【当前关系姿态】
{relational_summary_only}

【当前行为倾向】
{behavior_summary_only}

【用户输入】
{user_text}
```

---

## 4. 怎么看结果

### 如果 Variant B / C 明显优于 Variant A

更像是：

- **prompt 实现问题**

即：

- 状态本身可能没错
- 但原版喂法太硬、太抽象、桥接不够

### 如果三者都差不多

更像是：

- 状态表示问题
- 或 realization 边界问题

### 如果 direct 在桥接后明显改善，而 projected 没改善

更像是：

- 八维行为层可能增加了 realization 难度

### 如果 projected 在桥接后反而改善最多

更像是：

- 行为层并非无用，问题只是当前 prompt 实现没把它翻好

---

## 5. 第一轮建议

第一轮不要跑很多 case。

建议：

- `2` 个 long cases
- `2` 个方法组：
  - `explicit_rel_state_direct`
  - `explicit_rel_state_projected`
- `3` 个 prompt 变体：
  - Variant A
  - Variant B
  - Variant C

这样就足够先判断：

- 问题更像 prompt bridge
- 还是更像表示 / realization 边界

---

## 5. 当前阶段性结论（已完成）

基于当前的小规模 prompt-bridging 诊断实验，可以先写下一个阶段性判断：

- 改变显式状态的呈现方式，确实会影响输出分布；
- 因此，原始 `Variant A` 并不是一个完全中性的实现；
- `Variant B / C` 通常会让输出更短、更收敛、更少铺陈；
- 但即便进行了 bridge 改写，当前仍然没有看到它们稳定表现出明显优于强 baseline 的语言层效果。

因此，更稳妥的解释不是：

- “显式关系态无用”

而是：

- prompt bridge 不是完全无关；
- 但它目前看起来也不像主要瓶颈；
- 它更像一个次要因素或降噪因素；
- 主要问题更可能位于：
  - 状态表示本身的任务收益有限；
  - 或未微调 LLM 的 realization boundary。

也就是说，这一步实验的作用已经足够清楚：

- 它排除了“只是 prompt 写得太差”这一简单解释；
- 但没有提供继续深挖 prompt bridge 本身的充分理由。

所以这条 bridge 线接下来的定位应当是：

- **已完成的诊断步骤**
- 而不是新的主研究方向
