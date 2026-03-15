# 论文执行计划：审稿式收敛版

## 0. 先说结论

当前这条论文线**还不能**按原计划直接推进到 judge 和结论阶段。

原因不是代码没跑通，而是研究设计还有两个根本问题：

1. **baseline 还不够公平**
2. **主评测还不够外部**

如果不先修这两个问题，后面即使跑出很多结果，也很难支撑一个有说服力的论文结论。

因此，这份执行计划不再把“先做 judge”当成下一步，而是先做：

1. 重新收窄 claim
2. 补一个真正强且公平的 baseline
3. 重新定义主评测
4. 再进入正式实验

---

## 1. 当前真正能 defend 的研究问题

当前最稳妥的研究问题不应该是：

- 显式关系态 + 行为态投影是否整体更优、更稳定

而应该收窄成：

**在长期 companion dialogue setting 下，显式关系态中间层是否能减少明显的关系跳变，并形成更连贯的 case-level relational coherence。**

这意味着：

- 我们先不急着证明最终自然语言在所有层面都更好
- 先证明显式中间层在“多轮关系连贯性”上有净收益
- realization gap 作为第二层结论，而不是主结论的前提

---

## 2. 当前版本里哪些部分已经完成（保留）

### 已完成

- 论文问题已经从“整个产品”收缩到“显式中间控制层”
- 实验主链路已经能跑：
  - `method`
  - `baseline_prompt_only`
  - `baseline_prompt_only_strong`
- 第一版 case 集已经建立：
  - [paper_cases_v1.json](/d:/My%20Project/companion-ai/paper_cases_v1.json)
- 实验脚本已经建立：
  - [paper_run_experiment.py](/d:/My%20Project/companion-ai/paper_run_experiment.py)
- 基础评测脚本已经建立：
  - [paper_eval.py](/d:/My%20Project/companion-ai/paper_eval.py)
- 第一轮 pilot run 已完成，已知：
  - method 更慢
  - method 更短、更克制
  - strong prompt baseline 没有自然追平 method
- tone delta normalization 已接入主链路

### 当前不推翻

这些工作都保留，因为它们解决的是：

- 工程可运行性
- 实验基础设施
- 噪声控制

问题不在这里，问题在研究设计。

---

## 3. 当前计划的主要缺陷

### 缺陷 A：baseline 不公平

当前三组里：

- `method` 拿到了显式状态、投影、controller 等结构化控制
- 两个 baseline 只是 prompt-only 版本

所以即使 `method` 胜出，也不能强力证明：

- 显式中间层本身更优

最多只能证明：

- 给系统更多结构化控制会带来不同输出

这不足以支撑强论文 claim。

### 缺陷 B：judge 仍有循环论证风险

如果 judge 主要围绕：

- 直接性
- 主动推进
- 追问
- 温暖度

这类和内部八维高度同构的量来打分，那么评测会变成：

- 系统按自己的本体论编码
- judge 再按近似同一套本体论验收

这会削弱说服力。

### 缺陷 C：claim 仍然偏大

当前很多写法还在暗示：

- 显式状态层更稳定、更可控、更优

但在 baseline 和评测都还没站稳前，这个 claim 太大。

---

## 4. 新的执行顺序

从现在开始，执行顺序改为下面这 6 步。

---

## 5. 阶段 A：重写研究 claim（下一步之前必须完成）

### 目标

把论文主张收成一个当前能 defend 的版本。

### 新的主张

第一版论文只主张：

**显式关系态中间层有助于减少长期对话中的明显关系跳变，并形成更连贯的 case-level relational coherence。**

### 暂不主张

- 八维行为投影已经被完整证明优于强 prompt
- 最终自然语言整体更优
- 零样本通用 LLM 已经能稳定执行数值行为态

### 这一步的产出

- 更新 [PAPER_PROPOSAL_RELATION_STATE.md](/d:/My%20Project/companion-ai/PAPER_PROPOSAL_RELATION_STATE.md)
- 让摘要、研究问题、假设都服从这个更小的 claim

### 在完成这一步之前，不做

- judge 设计
- 更多实验运行

---

## 6. 阶段 B：补一个真正公平的强 baseline

### 目标

新增一个比当前 `baseline_prompt_only_strong` 更有说服力的 baseline。

### 新 baseline

建议新增：

- `baseline_relational_instruction`

并明确把它视为**第一步可运行版本**，不是最终强 baseline 的终点。

### 它的定义

- 不使用显式关系态状态机
- 不使用 relation -> behavior projection
- 不使用你的内部四维/八维原词
- 但每轮给模型一段**自然语言的高层关系姿态说明**

### 这一步为什么先不直接照搬 DFA-RAG / Skeleton-to-Response / Prototype-to-Style

原因不是这些方法没价值，而是：

1. 它们与本文任务不完全同构
2. 如果整套照搬，会引入过多额外变量
3. 会让比较不再聚焦于“显式关系态中间层是否有净收益”

因此，这些工作更适合作为：

- semantic routing
- prototype retrieval
- retrieval-guided control

的设计灵感，而不是主 baseline 的整套替身。

### 阶段 B 的更合理终点

阶段 B 更合理的终点不是只停在启发式 `baseline_relational_instruction`，而是：

#### `baseline_relational_instruction_retrieval`

即：

- 建一组“关系信号原型库”
- 原型库包含：
  - `signal_description`
  - `relational_stance_instruction`
  - 少量示例
- 当前输入做语义检索
- 取最相近原型生成高层关系姿态说明

这个 retrieval-style baseline 才是后续真正更强、更公平的 strong baseline。

### 阶段 B 的建议顺序

1. 先让启发式 `baseline_relational_instruction` 跑通
2. 用 smoke set 看它是否比 `baseline_prompt_only_strong` 明显更强
3. 再把它升级成 `baseline_relational_instruction_retrieval`
4. 之后才进入正式主实验

例如：

- 当前应保持距离、不要主动推进、语气简短克制
- 当前适合温和回应，但不宜突然亲近
- 当前应避免关系降温中的过度补偿

### 为什么它重要

它能更公平地回答：

- 是显式状态层有价值
- 还是你只是给 method 更多结构化先验

### 这一步的产出

- 新实验组设计说明
- baseline 输入格式定义
- 后续代码落地方案

### 在完成这一步之前，不做

- 主结果表
- judge 主评测

---

## 7. 阶段 C：重写主评测

### 目标

把主评测从“接近内部八维的 judge”改成更外部、更 case-level 的评测。

### 新的主评测指标

主结果优先看：

1. `case-level relational coherence`
2. `abrupt shift rate`
3. `longitudinal consistency`

### 这些指标问什么

- 整段对话是否像同一个关系过程？
- 是否出现突兀亲近 / 突兀疏离 / 突兀补偿？
- 系统是否保持了可理解的关系演化轨迹？

### alignment 的新地位

`state-to-response alignment` 不删除，但降级为：

- 辅助分析指标
- 用来解释中间状态和输出之间的 realization gap

而不是主结果。

### 这一步的产出

- judge 评测问题定义
- 主结果表结构
- 辅助分析表结构

### 在完成这一步之前，不做

- 大规模 judge 跑分

---

## 8. 阶段 D：小规模验证新 baseline 和新 judge

### 目标

先验证新的 baseline 和 judge 本身是否成立，而不是马上全量跑实验。

### 样本规模

只用：

- 6 个 case
- 每类挑 1 个代表样本
- 跑：
  - `method`
  - `baseline_prompt_only`
  - `baseline_prompt_only_strong`
  - `baseline_relational_instruction`

### 要看什么

1. 新 baseline 是否比旧 strong baseline 更强、更公平
2. judge 是否能稳定区分：
   - 连贯
   - 跳变
   - 过度补偿
   - 忽冷忽热

### 可能结果与含义

#### 结果 1：新 baseline 仍明显弱于 method
- 说明结构化中间层确实可能有研究价值

#### 结果 2：新 baseline 接近或追平 method
- 说明论文 claim 需要继续收缩
- 可能真正的贡献不在“状态层”，而在“关系指令组织方式”

#### 结果 3：judge 本身判断不稳定
- 说明当前评测问题写得不好
- 先改评测，不扩实验

### 这一步的产出

- 一份小规模 smoke 结果
- 一份 baseline/judge 可用性结论

### 在完成这一步之前，不做

- 20 case 全量主实验
- tone evaluator 微调

---

## 9. 阶段 E：正式第一轮主实验

### 前提

只有阶段 D 证明：

- baseline 更公平了
- judge 问题可用

才进入这一步。

### 正式实验组

1. `method`
2. `baseline_prompt_only`
3. `baseline_prompt_only_strong`
4. `baseline_relational_instruction`

### 主指标

1. `case-level relational coherence`
2. `abrupt shift rate`
3. `longitudinal consistency`

### 辅助指标

1. `state-to-response alignment`
2. `behavior drift`
3. `realization gap`

### 样本规模

- 全量 20 case
- 4 组

### 这一步的产出

- 第一轮真正可进入论文的结果表
- 一批典型正例 / 反例

---

## 10. 阶段 F：go / no-go 决策

### 继续做的条件

满足以下至少两条：

- `method` 在 case-level coherence 上明显更好
- `method` 的 abrupt shift 更少
- `method` 在 longitudinal consistency 上明显更好
- 新 baseline 仍无法稳定追平 method

### 应该止损或改题的条件

出现任一条就要严肃考虑调整方向：

- `baseline_relational_instruction` 已接近或追平 `method`
- 主 judge 难以稳定工作
- 所有差异主要来自 prompt phrasing，而不是状态结构
- method 的内部状态层本身仍然很不稳

### 这一步的产出

- 一份内部 go / no-go 报告

---

## 11. tone evaluator 微调什么时候开始

### 结论

仍然不是现在。

### 只有在下面条件满足后才考虑

1. 新 baseline 和新主评测已经跑通
2. method 在主指标上表现出一定趋势
3. 你能明确看到：
   - 架构方向本身有价值
   - 但 `delta_R` 噪声仍在拖后腿

### 否则不做

如果这些还没成立，现在做 tone evaluator 微调只会：

- 提前混入训练变量
- 让你更难判断论文核心问题

---

## 12. 当前最合理的下一步

不是继续做 judge 脚本，也不是继续跑更多实验。

**下一步应该是：**

1. 更新 [PAPER_PROPOSAL_RELATION_STATE.md](/d:/My%20Project/companion-ai/PAPER_PROPOSAL_RELATION_STATE.md)，把 claim、baseline、指标全部收紧到这版
2. 设计 `baseline_relational_instruction` 的输入格式
3. 再决定 judge 该怎么写

---

## 13. 当前状态

### 已完成

- 实验基础设施
- 第一轮 pilot
- tone delta normalization

### 当前不再按旧顺序推进

- 不直接进入旧版阶段四 judge

### 当前真正要做

- 修正研究设计
- 补公平 baseline
- 重写主评测

---

## 14. 第二阶段实验组冻结版

第二阶段不再继续扩 baseline 家族，也不再把实验组无限细分。当前冻结为下面 5 组。

### G0. Strong Baseline

- `baseline_relational_instruction`

作用：
- 作为外部强基线；
- 代表“单层高层关系指导”的强 prompt 控制路线。

### G1. Single-Layer Relational Control

- `explicit_rel_state_direct`

作用：
- 代表显式关系态单层控制；
- 用来回答“单层显式关系控制本身是否优于强 baseline”。

### G2. Two-Layer Relational-Behavior Control

- `explicit_rel_state_projected`

作用：
- 代表真实链路下的双层控制；
- 用来回答“真实 two-layer 是否优于 single-layer，以及是否优于强 baseline”。

### G3. Single-Layer Oracle Control

- `explicit_rel_state_direct_oracle`

作用：
- 用 oracle 关系摘要替代真实 updater；
- 用来隔离“single-layer 结构本身”的上限。

### G4. Two-Layer Oracle Control

- `explicit_rel_state_projected_oracle`

作用：
- 用 oracle 关系/行为摘要替代真实 updater；
- 用来隔离“two-layer 结构本身”的上限。

## 15. 第二阶段默认主比较

第二阶段默认主比较也冻结为下面 4 组对照，不再随意新增。

1. `G1 vs G0`
- `explicit_rel_state_direct` vs `baseline_relational_instruction`
- 回答：单层显式关系控制是否优于强 baseline。

2. `G2 vs G1`
- `explicit_rel_state_projected` vs `explicit_rel_state_direct`
- 回答：真实链路下，two-layer 是否优于 single-layer。

3. `G4 vs G3`
- `explicit_rel_state_projected_oracle` vs `explicit_rel_state_direct_oracle`
- 回答：理想控制信号下，two-layer 结构上限是否优于 single-layer。

4. `G4 vs G0`
- `explicit_rel_state_projected_oracle` vs `baseline_relational_instruction`
- 回答：two-layer 的理想上限与强 baseline 的距离。

## 16. 对照但不进入默认主结果表的辅助组

下面这些保留为诊断或补充，不作为第二阶段默认主结果组：

- `baseline_prompt_only`
- `baseline_prompt_only_strong`
- `baseline_relational_instruction_oracle_collapsed`
- `explicit_rel_state_direct_vA/vB/vC`
- `explicit_rel_state_projected_vA/vB/vC`

它们的用途分别是：
- prompt-only 家族：保留作早期 baseline 和附录；
- oracle-collapsed：用于控制信息对齐诊断；
- vA/vB/vC：用于 prompt-bridge 诊断。

## 17. 第二阶段冻结原则

在 mixed-signal 收尾和第二阶段正式启动之后，除非出现明确证据表明当前分组无法回答核心问题，否则：

- 不再新增新的 baseline 名称；
- 不再新增新的 prompt 变体主组；
- 不再把诊断组提升为主结果组；
- 不再把产品链路中的其他模块混入第二阶段主问题。
