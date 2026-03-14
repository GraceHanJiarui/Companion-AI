# 论文执行计划：显式关系态与行为态投影

## 0. 总目标

当前论文线要回答的问题是：

**显式关系态 + 行为态投影，是否比 prompt-only control 更适合作为长期交互中的中间控制层；如果是，未微调 LLM 的 realization gap 在哪里。**

当前论文**不**以以下内容为主目标：

- boundary 方法创新
- anti-manipulation 安全框架
- disclosure control 最优设计
- tone evaluator / controller / actor 的训练优化

这些能力可以保留在系统中，但不作为当前论文主问题。

---

## 1. 阶段一：锁定实验定义（已完成）

### 目标

把论文问题、实验组、核心指标固定下来，不再继续发散。

### 已完成内容

- 论文主问题已收敛到“显式中间控制层”，而不是整个 companion 产品。
- 核心实验组已固定为：
  - `method`
  - `baseline_prompt_only`
  - `baseline_prompt_only_strong`
- 核心指标已固定为：
  - `state-to-response alignment`
  - `longitudinal consistency`
  - `behavior drift`
  - `realization gap`
- `boundary` 已降级为系统背景能力，不进入论文主结果。
- 暂不做：
  - tone evaluator 微调
  - actor 微调
  - controller 蒸馏
  - 多模型主实验

### 对应文件

- [PAPER_PROPOSAL_RELATION_STATE.md](/d:/My%20Project/companion-ai/PAPER_PROPOSAL_RELATION_STATE.md)

### 阶段成果

- 一份稳定的论文问题定义
- 一份不再混乱变动的研究方向说明

---

## 2. 阶段二：建立最小可复现实验管线（已完成）

### 目标

让 method 和 baseline 能在同一套 case 上批量运行，并统一导出结构化结果。

### 已完成内容

- `/chat` 已支持实验模式：
  - `method`
  - `baseline_prompt_only`
  - `baseline_prompt_only_strong`
- 已建立实验运行脚本：
  - [paper_run_experiment.py](/d:/My%20Project/companion-ai/paper_run_experiment.py)
- 已建立第一版 case 文件：
  - [paper_cases_v1.json](/d:/My%20Project/companion-ai/paper_cases_v1.json)
- 已统一输出字段：
  - `experiment_mode`
  - `case_id`
  - `session_id`
  - `turn_idx`
  - `user_text`
  - `assistant_text`
  - `boundary_keys`
  - `memory_previews`
  - `rel_effective`
  - `behavior_effective`
  - `_last_controller`
  - `trace_id`
  - `elapsed_s`
- 已修复实验链路中的关键运行问题：
  - `session_id` 过长导致 422
  - `turn_events.tone_eval` 列缺失导致 500

### 对应文件

- [paper_run_experiment.py](/d:/My%20Project/companion-ai/paper_run_experiment.py)
- [paper_cases_v1.json](/d:/My%20Project/companion-ai/paper_cases_v1.json)
- [app/api/chat.py](/d:/My%20Project/companion-ai/app/api/chat.py)
- [app/generation/actor_prompt.py](/d:/My%20Project/companion-ai/app/generation/actor_prompt.py)
- [app/memory/events.py](/d:/My%20Project/companion-ai/app/memory/events.py)

### 阶段成果

- 一套能跑 method 与 baseline 的实验主链路
- 一份统一格式的原始实验结果集

---

## 3. 阶段三：完成第一轮基础汇总（已完成）

### 目标

先得到最基础的组间行为差异全景图，确认实验平台不是空转。

### 已完成内容

- 已建立评测骨架脚本：
  - [paper_eval.py](/d:/My%20Project/companion-ai/paper_eval.py)
- 已生成输出：
  - [paper_eval_out/turn_level_metrics.json](/d:/My%20Project/companion-ai/paper_eval_out/turn_level_metrics.json)
  - [paper_eval_out/case_mode_summary.json](/d:/My%20Project/companion-ai/paper_eval_out/case_mode_summary.json)
  - [paper_eval_out/global_summary.json](/d:/My%20Project/companion-ai/paper_eval_out/global_summary.json)
  - [paper_eval_out/judge_examples.json](/d:/My%20Project/companion-ai/paper_eval_out/judge_examples.json)
- 已得到第一轮初步现象：
  - `method` 明显更慢
  - `method` 回答更短、更克制
  - `baseline_prompt_only_strong` 没有自然追平 `method`
  - 当前实验结果仍不足以证明论文核心假设

### 对应文件

- [paper_eval.py](/d:/My%20Project/companion-ai/paper_eval.py)
- [paper_results_v1.jsonl](/d:/My%20Project/companion-ai/paper_results_v1.jsonl)
- [paper_eval_out/global_summary.json](/d:/My%20Project/companion-ai/paper_eval_out/global_summary.json)

### 阶段成果

- 一版“实验平台已跑通”的内部结果
- 一版初始现象总结，已回写到 proposal

---

## 3.5 阶段三点五：tone delta normalization（当前应优先执行）

### 目标

在正式做核心 judge 评测前，先把 `tone evaluator -> apply_tone_delta` 之间的关系增量清洗成一个更稳定的 teacher policy，减少上游噪声污染。

### 为什么必须插入这一步

如果 `delta_R` 本身抖动很大，那么后续所有核心评测都会混在一起：

- 是显式状态层没价值？
- 还是上游 `delta_R` 噪声太大？
- 还是 state 到语言的 realization gap 太大？

因此，在阶段四与阶段五之前，先做一层确定性 normalization 更合理。

### 当前采用的初始标准

- 单维 clamp：`[-0.05, 0.05]`
- 总量约束：`L1 <= 0.10`
- 死区阈值：`|delta| < 0.015 -> 0`
- 默认策略：无强关系信号时优先全零
- 允许“高置信地判断这一轮不该更新”

### 强关系信号优先包括

- 明确边界表达
- 明确脆弱表达
- 明确关系确认 / 关系试探
- 明确离开 / 暂停
- 明确感谢、信任、失望、疏离
- 明确冲突、纠偏、关系修复

### 对普通场景的默认策略

以下场景优先全零：

- 纯技术请求
- 普通信问答
- 无明显关系信号的短句
- 模糊噪声输入

### 代码落地要求

1. 在 `tone evaluator -> apply_tone_delta` 之间增加独立 normalization policy。
2. 记录：
   - `raw_delta_R`
   - `normalized_delta_R`
   - `normalization_reason`
3. 用 normalized delta 而不是 raw delta 更新关系态。
4. 实现不能依赖论文分支特定代码，后续能无缝回到 `main`。

### 完成标准

- 主链路已经用 normalized delta 更新 `rel_state_boost`
- debug/turn 记录中能看到 raw vs normalized 差异
- 运行几组 case 后，关系态抖动明显下降

### 在这一步完成之前，不做

- 正式 alignment judge
- 正式 longitudinal judge
- tone evaluator 微调

### 阶段成果

- 一层独立的 `tone delta normalization policy`
- 一版更稳定、可审查的 `delta_R` teacher policy

---

## 4. 阶段四：核心评测一，做 state-to-response alignment

### 目标

验证当前中间状态是否真的解释最终回复。

### 评测口径（更新后）

这一阶段**不直接拿内部“四维八维原词”当 judge 主模板**，避免循环论证。

评测分成两层：

#### A. 外显行为语言层评测（主评测）

Judge 只看外部可观察行为倾向，例如：

- 直接性
- 主动推进程度
- 是否追问
- 温暖度
- 是否显得关系连贯
- 是否突然过度亲近 / 突然抽离

这层不直接暴露 `bond/care/trust/stability` 这些内部术语。

#### B. 内部状态释义层评测（辅助评测）

把内部 state 先翻译成自然语言倾向描述，再交给 judge，例如：

- “当前系统倾向于较低主动推进、中等温暖度、较克制的直接性”

Judge 再判断输出是否与这些倾向一致。

### 要做的事

1. 修改 [paper_eval.py](/d:/My%20Project/companion-ai/paper_eval.py)
2. 导出 `alignment_judge_inputs.json`
3. 每条样本包含：
   - `case_id`
   - `experiment_mode`
   - `turn_idx`
   - `user_text`
   - `assistant_text`
   - `rel_effective`
   - `behavior_effective`
   - `state_summary_text`（内部状态的自然语言释义）
4. 设计 judge 模板，先对以下 4 个外显维度打分：
   - `Directness`
   - `Initiative`
   - `Q_clarify`
   - `T_w`
5. 输出：
   - 总体 alignment，1-5
   - 4 个维度分数
   - `major_mismatch`
   - `reason`

### 样本规模

- 先抽 5 个 case × 3 组 × 3 turn
- 约 45 个 turn 样本

### 期待输出

- `method` 的 alignment 分数整体高于两个 baseline
- baseline strong 可能接近，但不稳定
- 出现一批“state 合理，但回复不对齐”的 method 样本

### 不同输出意味着什么

- 如果 `method` 明显更高：
  - 论文核心命题开始站住
- 如果 `method` 和 baseline 接近：
  - 显式状态层价值需要怀疑
- 如果 `method` 的 state 合理但 alignment 低：
  - 这正是 realization gap 的证据
- 如果 judge 本身不稳定：
  - 先改 judge 模板，不进入下一步

### 在这一步完成之前，不做

- tone evaluator 微调
- actor 微调
- 多模型主实验

### 阶段成果

- `alignment_judge_inputs.json`
- 一份 alignment 评分表
- 一批高分 / 低分典型例子

---

## 5. 阶段五：核心评测二，做 longitudinal consistency

### 目标

验证一个 case 的多轮关系演化是否连贯。

### 要做的事

1. 修改 [paper_eval.py](/d:/My Project/companion-ai/paper_eval.py)
2. 导出 `longitudinal_judge_inputs.json`
3. 按 `case_id + experiment_mode` 打包整段对话
4. judge 输入包括：
   - 全部 turns
   - 每轮 relation / behavior state
   - 每轮 `state_summary_text`
5. judge 输出包括：
   - `longitudinal_consistency_score`，1-5
   - `has_abrupt_shift`
   - `shift_turns`
   - `reason`

### 样本规模

- 理想：20 case × 3 组 = 60 条 case-level 样本
- 若太慢，先测 10 个代表性 case

### 期待输出

- `method` 在关系升温、关系降温、脆弱表达场景下更连贯
- baseline 更容易出现风格跳变或关系突变

### 不同输出意味着什么

- 如果 `method` 分数明显更高：
  - 论文价值明显增强
- 如果 `baseline_prompt_only_strong` 追平 `method`：
  - prompt-only 上限比预期高，需要重审 claim
- 如果 `method` 反而更跳：
  - 显式状态链路可能仍被 noisy delta 扰动

### 在这一步完成之前，不做

- 微调
- 第二模型复现

### 阶段成果

- `longitudinal_judge_inputs.json`
- 一份 case-level consistency 结果
- 一批 abrupt shift 典型例子

---

## 6. 阶段六：测 behavior drift

### 目标

把“漂移”从感觉变成结构化统计。

### 要做的事

1. 在 [paper_eval.py](/d:/My Project/companion-ai/paper_eval.py) 中新增 `behavior_drift_method.json`
2. 第一版先只对 `method` 组计算真实 drift
3. 先选 4 个维度：
   - `Directness`
   - `Initiative`
   - `Q_clarify`
   - `T_w`
4. 计算：
   - 同 case 相邻 turn 的 L1 drift
   - 同类 case 间的均值和方差

### 期待输出

- `method` 在相似场景下行为变化较平滑
- 能识别少量异常跳变样本

### 不同输出意味着什么

- 如果 drift 普遍很小：
  - 中间状态层至少在内部较稳
- 如果 drift 很大：
  - 显式状态层本身就不稳，论文风险上升
- 如果 drift 小但 alignment 低：
  - 说明 realization gap 很强

### 在这一步完成之前，不做

- baseline 组复杂行为后验估计
- tone evaluator 微调

### 阶段成果

- `behavior_drift_method.json`
- 一份 method 内部状态稳定性分析

---

## 7. 阶段七：识别 realization gap

### 目标

区分问题到底出在状态层还是状态到语言的实现层。

### 要做的事

1. 结合以下结果筛样本：
   - alignment
   - longitudinal consistency
   - behavior drift
2. 标记满足以下条件的样本：
   - state 连续
   - drift 小
   - 但 alignment 低或 consistency 差
3. 导出 `realization_gap_cases.json`

### 期待输出

- 一批典型样本，显示：
  - 中间状态层看起来合理
  - 但 LLM 最终没有稳定执行

### 不同输出意味着什么

- 如果这种样本很多：
  - 论文可转向“显式状态层有价值，但 realization 需要训练增强”
- 如果这种样本很少：
  - 当前零样本实现可能比预期更好

### 在这一步完成之前，不做

- tone evaluator 微调
- actor 微调

### 阶段成果

- `realization_gap_cases.json`
- 一段可直接进入论文结果部分的分析

---

## 8. 阶段八：第一轮 go / no-go 决策

### 目标

判断这条论文线值不值得继续投入。

### Go 条件

满足下面至少 2 条，就继续：

- `method` 在 alignment 上明显更好
- `method` 在 longitudinal consistency 上明显更好
- `method` 内部 behavior drift 较稳
- 出现了有研究价值的 realization gap 现象

### No-go 条件

出现下面任一条，要认真考虑止损或改题：

- `method` 和强 baseline 没有稳定差异
- judge 评分混乱，无法形成可信结论
- 中间状态层本身就不稳
- 结果高度依赖极少数个例

### 阶段成果

- 一份 2-4 页内部实验报告
- 一页明确的 go / no-go 结论

---

## 9. 什么时候可以开始 tone evaluator 微调

### 结论

**只有在阶段八之后考虑。**

### 可以开始的前提

必须满足：

1. 核心评测已经跑起来
2. 已确认：
   - 架构方向有希望
   - noisy `delta_R` 明显拖后腿
3. 已能区分：
   - 架构收益
   - 与 tone evaluator 噪声带来的损失

### 不满足前提时，不开始

如果还没完成阶段四到阶段七，就不进入 tone evaluator 微调。

### 进入微调阶段时的合理目标

不是“觉得应该训练就训练”，而是：

- 已知上游 `delta_R` 噪声是关键瓶颈
- 需要验证降噪后是否能放大中间状态层收益

---

## 10. 各阶段成果总览

### 阶段一到三结束时（已完成）

- 一份稳定的 proposal
- 一套能跑的实验管线
- 一份初始现象总结

### 阶段三点五结束时

- 一层独立的 tone delta normalization policy
- 一套可审查的 raw / normalized delta 记录

### 阶段四到五结束时

- alignment 评估结果
- longitudinal consistency 评估结果
- 典型正反例

### 阶段六到七结束时

- behavior drift 分析
- realization gap 样本集
- 一版真正有研究味道的结果解释

### 阶段八结束时

- 明确知道这条线是继续做论文，还是重定位为系统 / 产品探索

---

## 11. 当前执行状态

### 已完成

- 阶段一
- 阶段二
- 阶段三

### 当前应优先执行

- 阶段三点五：`tone delta normalization`

### 阶段三点五之后紧接着做

- 阶段四：`state-to-response alignment`
- 阶段五：`longitudinal consistency`

### 当前不做

- tone evaluator 微调
- actor 微调
- controller 蒸馏
- 多模型主实验
