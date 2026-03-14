# 论文构想：显式关系态建模与行为态投影

## 1. 核心研究命题

对于长期陪伴型对话系统，纯 prompt 控制难以稳定维持关系一致性。显式关系态建模与关系态到行为态投影有潜力提供一种更可解释、更可控的中间层。

但当前需要进一步澄清的是：

- “显式状态层本身更好”
- 与
- “未微调通用 LLM 已经能稳定执行这层状态控制”

并不是同一个命题。

因此，这篇论文的核心不应被表述为“只要把关系和行为数值喂给模型，输出就自然更稳定”，而应被表述为：

- 在长期交互型对话系统中，显式社会关系状态与行为投影是否构成更好的中间控制基底？
- 如果是，通用 LLM 在未微调条件下对该中间状态的自然语言实现边界在哪里？

---

## 2. 论文题目候选

### 候选 1

**Explicit Relational State Modeling Improves Stability in Long-Term Companion Dialogue Systems**

适合强调“稳定性提升”这一主结论。

### 候选 2

**From Relational State to Behavioral Control: A Structured Framework for Long-Term Companion Dialogue**

适合强调“关系态 -> 行为态投影”是核心方法。

### 候选 3

**Beyond Prompt-Only Control: Explicit Relational State and Behavior Projection for Consistent Companion Dialogue**

适合把 baseline 直接设定为 prompt-only control。

### 候选 4

**Controlling Long-Term Companion Dialogue with Explicit Relational State and Behavior Projection**

标题最直接，偏系统方法论文风格。

### 候选 5

**Explicit Social State as an Intermediate Control Layer for Consistent Long-Horizon Dialogue**

更偏一般化，不只限于陪伴产品，适合往更广义的 LLM dialogue/agent 方向投稿。

---

## 3. 摘要草稿

### 版本 A：偏系统方法

Large language models can generate fluent dialogue, but maintaining stable relational behavior over long-term interaction remains difficult when control is implemented only through prompts. In companion-style dialogue systems, this often appears as persona drift, unstable affective stance, and inconsistent respect for user boundaries. We propose a structured control framework that introduces an explicit relational state as an intermediate layer between dialogue history and language generation. The framework maintains a multi-dimensional relational state over time, projects it into a lower-level behavioral control vector, and uses this vector to condition response planning and generation. Compared with prompt-only baselines, the proposed approach aims to improve longitudinal behavioral stability, boundary adherence, and interpretability. We outline an experimental setting for long-horizon companion dialogue and define evaluation metrics for behavioral drift, boundary violations, and relation consistency. The work suggests that explicit state modeling can provide a practical alternative to relying solely on implicit prompt conditioning for long-term interactive agents.

### 版本 B：偏对话与陪伴场景

Prompt-based control is often insufficient for maintaining stable relational behavior in long-term companion dialogue. Even when a model is given persona instructions and recent history, its affective stance and interaction style can fluctuate across turns, making it difficult to sustain a coherent sense of relationship while reliably respecting user boundaries. We present a dialogue architecture that explicitly models relational state and deterministically projects that state into behavioral control variables before language generation. This design separates latent relationship tracking from natural-language realization, enabling more interpretable and controllable interaction. We propose evaluating the method against prompt-only baselines on long-horizon companion dialogue scenarios, focusing on relation consistency, boundary adherence, and behavioral stability. The central hypothesis is that explicit relational state provides a more stable control substrate than prompt-only conditioning for socially persistent LLM dialogue systems.

### 中文摘要草稿

尽管大语言模型能够生成流畅自然的对话，但在长期陪伴型交互中，仅依赖 prompt 进行控制往往难以稳定维持关系一致性。这种不足通常表现为人格抖动、情感姿态波动以及对用户边界的长期遵守不稳定。本文提出一种结构化控制框架，在对话历史与自然语言生成之间引入显式关系态作为中间层。系统持续维护多维关系状态，并将其确定性投影为低层行为控制向量，再基于该向量进行回复规划与表达生成。相较于纯 prompt 控制基线，该方法预期能够提升长期行为稳定性、边界遵守率与系统可解释性。本文同时提出一套面向长期陪伴型对话的评测设置，重点考察行为漂移、关系一致性与边界违反情况。该工作表明，在长期交互型对话系统中，显式状态建模可能是替代纯 prompt 控制的一条有效路径。

---

## 4. 研究问题与假设

### 4.1 研究问题

1. 在长期陪伴型对话中，显式关系态建模是否比纯 prompt 控制更适合作为中间控制基底？
2. 关系态到行为态的确定性投影，是否能在中间状态层面降低 persona drift 和行为漂移？
3. 通用 LLM 在未微调条件下，对数值化行为控制信号的自然语言实现边界在哪里？
4. 显式中间状态是否能提高边界遵守率与系统可解释性？

### 4.2 核心假设

- H1：显式关系态 + 行为态投影在长期多轮交互中构成更好的中间控制基底。
- H2：显式中间状态有助于更稳定地执行用户边界与长期偏好。
- H3：显式状态系统更容易进行调试、分析和蒸馏。
- H4：未微调通用 LLM 对数值化行为信号的执行并不总是稳定，因此中间状态层的收益可能大于最终语言输出层立即体现出来的收益。

---

## 5. 方法概述

论文方法部分可以围绕下面这条链路展开：

1. 用户输入到达系统
2. belief 层抽取长期边界与偏好
3. tone evaluator 输出关系增量 `delta_R`
4. session relation state 更新
5. relation state 经确定性投影得到 behavior vector
6. planner / controller 基于当前状态做轻量规划
7. actor 根据 behavior vector 和 plan 生成最终回复

其中真正需要强调的方法创新点是：

- 关系状态是显式、持久化、可更新的
- 行为状态不是直接由 prompt 语言描述，而是由关系状态确定性投影得到
- 自然语言生成层不直接承担全部社会状态推理

---

## 6. Baseline 设计

这篇论文至少需要一个强 baseline 和一个主方法。

### 6.1 Baseline A：Prompt-Only Control

定义：

- 不显式维护关系态
- 不维护关系态到行为态投影
- 仅将 persona、用户历史、belief、memory 作为 prompt 上下文的一部分输入给模型
- 模型直接生成回复

要点：

- 这是最关键的对照组
- 用来回答“显式状态层是否真的有价值”

### 6.2 Baseline B：Prompt + Heuristic Style Tags

定义：

- 不维护连续关系态
- 只给模型一些离散风格标签或少量手工行为提示
- 例如“更温柔/更直接/少追问”等 prompt 指令

要点：

- 用来区分“显式状态建模”与“简单提示工程增强”
- 能避免论文被质疑为“只是多写了一层 prompt”

### 6.3 Main Method：Explicit Relational State + Behavior Projection

定义：

- 显式维护四维关系态
- 通过确定性 projector 得到八维行为态
- behavior 作为 Actor 控制变量
- belief 和 memory 作为辅助上下文

### 6.4 可选 Ablation

如果时间和资源允许，建议增加：

#### Ablation 1：有关系态、无行为态投影

- 直接把关系态文本化塞进 Actor prompt
- 不走显式 projector

目的：

- 证明“行为态投影”本身也有贡献，而不只是“多存了一份关系变量”

#### Ablation 2：有行为态投影、无显式增量更新

- 不使用 `delta_R` 连续更新
- 每轮直接从当前输入推断一个 behavior profile

目的：

- 证明连续状态积累本身有价值

---

## 7. “稳定性”指标定义

“更稳定”必须操作化，否则论文会变成主观印象。

建议至少定义以下几类指标。

### 7.1 Behavior Drift

定义：

- 在相似类型场景下，系统行为参数或外显行为风格的波动程度

可实现形式：

- 比较相似 case 中 `behavior_effective` 的方差
- 或使用 judge/规则判断回复风格偏移程度

可测问题：

- 同样是轻度安抚场景，系统是否一会儿非常热情、一会儿极其冷淡

### 7.2 Relation Consistency

定义：

- 多轮交互中，回复所体现的关系姿态是否与当前已知关系状态一致

可实现形式：

- 用规则或 judge 比较：
  - 高 trust/high bond 条件下是否更自然地允许一定程度披露
  - 低 trust 条件下是否减少直接性或减少深度追问

可测问题：

- 关系状态变化后，外显语言是否同步而连续地变化

### 7.3 Boundary Adherence

定义：

- 用户已明确表达的边界，后续轮次中是否被持续遵守

可实现形式：

- 基于 belief key 设计测试集
- 统计违反边界的回复比例

例子：

- 用户说“不想被追问情绪”
- 后续是否仍无端追问“你是不是很难过”

### 7.4 Persona Drift

定义：

- 在长期交互中，系统人格表现是否大幅摇摆

可实现形式：

- 人评：角色一致性评分
- LLM-as-judge：是否与前序 persona 表现一致
- 风格特征统计：直接性、主动性、披露倾向的突然变化

### 7.5 Memory Use Stability

定义：

- 系统对过去信息的调用是否自然、相关、不过度

可实现形式：

- 记忆命中后显式引用率
- 不相关 memory 提及率
- 生硬提旧事率

### 7.6 Interpretability / Inspectability

定义：

- 系统输出是否能被中间状态解释

可实现形式：

- relation state / behavior state / final reply 之间的一致性分析
- 统计“中间状态变化”与“输出风格变化”的相关性

备注：

- 这个指标更适合做分析性结果，而不是单一主指标

---

## 8. 评测设计建议

### 8.1 数据与 case 构造

建议建立一套长程 case set，至少覆盖：

- 边界建立与重复提醒
- 情感脆弱表达
- 一般聊天
- 任务型请求
- 关系升温
- 关系降温/疏离
- 用户离开/暂停

### 8.2 评测方式

建议混合三类评测：

#### 自动/规则评测

- 边界违反率
- 特定 forbidden pattern 命中率
- 记忆误用率

#### LLM-as-judge

- 关系一致性
- 人格一致性
- 回复是否符合预期 behavior

#### 人评

- 稳定感
- 连续关系感
- 自然度
- 是否有操控感

### 8.3 最低可行实验规模

第一版实验不必追求特别大。

可以先做：

- 20-50 个高质量长程 case
- 每个 case 跑 baseline 和 main method
- 对照分析输出差异

如果第一版结果就能明显看出趋势，再决定要不要继续放大。

---

## 9. 当前代码中哪些部分已经足够支持第一版实验

下面这些能力已经基本具备，可以直接成为第一版实验支撑。

### 9.1 显式关系态建模

相关文件：

- `app/models/session_state.py`
- `app/beliefs/policy.py`
- `app/inference/tone_evaluator.py`

当前已具备：

- `rel_trait`
- `rel_state_boost`
- `rel_effective`
- `delta_R` 更新逻辑

这意味着：

- 第一版实验已经能跑“显式关系态”方法组

### 9.2 关系态到行为态投影

相关文件：

- `app/relational/projector.py`
- `app/beliefs/policy.py`

当前已具备：

- 四维关系态到八维行为态的确定性映射
- `behavior_effective` 缓存

这意味着：

- 论文方法里的核心“projection”已经真实存在，不只是概念

### 9.3 Controller / Actor 分层

相关文件：

- `app/controller/plan.py`
- `app/controller/controller_client.py`
- `app/generation/actor_prompt.py`
- `app/api/chat.py`

当前已具备：

- 结构化 plan
- behavior 注入 Actor
- memory 选择与自然语言生成分层

这意味着：

- 第一版实验已经能测试“有中间控制层”的方法

### 9.4 Belief / Boundary 持久化

相关文件：

- `app/beliefs/extract.py`
- `app/beliefs/store.py`
- `app/models/belief.py`

当前已具备：

- 长期边界抽取与落库
- active belief 列表
- belief 作为长期约束来源

这意味着：

- 可直接用于设计 boundary adherence 评测

### 9.5 Memory Retrieval

相关文件：

- `app/memory/memories.py`
- `app/memory/embedder.py`
- `app/models/memory.py`

当前已具备：

- 基于 embedding + pgvector 的召回
- memory preview 注入 controller

这意味着：

- 第一版实验已经可以纳入长期记忆场景
- 但 memory 质量不是这篇论文的最核心贡献点，第一版不宜把重心放在 memory 方法创新上

### 9.6 Debug 与中间状态可观测

相关文件：

- `app/api/debug.py`
- `app/api/chat.py`
- `app/models/event.py`

当前已具备：

- `_last_controller`
- `_last_rel_delta`
- latency
- turn snapshot

这意味着：

- 你已经具备做分析性实验的基础设施
- 可以导出中间状态与最终回复做关联分析

---

## 10. 第一版实验还缺什么

虽然主方法基础已具备，但第一版论文实验还缺以下关键部分：

### 10.1 明确 baseline 实现

当前代码里还没有一个正式的“prompt-only baseline 模式”。

需要新增：

- 一个禁用显式关系态/行为态投影的对照运行模式
- 或一套离线 baseline 生成脚本

### 10.2 稳定性评测脚本

需要新增：

- behavior drift 统计脚本
- boundary adherence 批量评测
- persona/relationship consistency judge 脚本

### 10.3 case 数据集

需要新增：

- 一组长期交互测试 case
- 最好分主题与场景类型

### 10.4 结果分析模板

需要新增：

- 自动统计表
- qualitative case 对照模板
- 人评标注格式

---

## 11. 第一版最小可行论文计划

如果走最小可行路线，可以按下面的顺序：

### 第一步

收紧问题：

- 只研究“显式关系态 + 行为态投影 vs prompt-only”

### 第二步

搭 baseline：

- 做一个不使用 relation state / behavior projection 的对照版本

### 第三步

准备 case：

- 先做 20-30 个长程 case

### 第四步

跑实验：

- baseline vs main method

### 第五步

评测：

- 边界遵守
- 行为漂移
- 关系一致性

### 第六步

写成 short paper / tech report / proposal

---

## 12. 当前最重要的判断标准

这篇论文方向值不值得继续投入，取决于第一版实验能否回答下面这句：

**在长期陪伴型交互中，显式关系态与行为态投影是否相较 prompt-only baseline 展现出可测的稳定性优势。**

如果第一轮实验回答是“是”，这个方向就值得继续。

如果第一轮实验回答是“不明显”，那就要考虑：

- 缩小问题
- 重做指标
- 或放弃把它作为主论文方向

---

## 13. 可能的审稿质疑与回应

下面这些不是“可能会有人挑刺”的边缘问题，而是这篇论文几乎一定会被问到的核心质疑。

### 13.1 质疑一：结论是否只适用于当前这套系统架构

典型质疑形式：

- 你的方法是不是只在当前 companion 架构里成立？
- 如果换一种 memory 设计、换一种 planner、换一种 prompt 组织方式，结论还成立吗？

建议回应方式：

- 第一版论文不做“普遍优于所有 LLM 控制方式”的强结论
- 只做 bounded claim：
  - 在长期陪伴型对话任务中
  - 在当前这一类分层控制架构设定下
  - 显式关系态 + 行为态投影相较 prompt-only baseline 表现出更好的稳定性/边界遵守
- 将跨架构泛化明确写为 future work

核心原则：

- 不做 universal claim
- 做 task-bounded, architecture-bounded claim

### 13.2 质疑二：结果会不会主要由 prompt 写法决定

典型质疑形式：

- 你是不是只是把方法组 prompt 写得更好？
- 如果 baseline prompt 认真调过，是不是也能达到类似效果？

建议回应方式：

- 对方法组和 baseline 尽量使用相同底模、相同 persona 基线、相同 memory/belief 来源
- 只让“是否显式维护关系态并投影为 behavior”成为核心区别
- 至少设置两个 baseline：
  - prompt-only baseline
  - prompt-only + richer style instruction baseline
- 如条件允许，再加 prompt sensitivity 实验

核心原则：

- 控制 prompt 混杂因素
- 给 baseline 公平机会

### 13.3 质疑三：所谓“更稳定”是否只是主观印象

典型质疑形式：

- 你说更稳定，但稳定到底是什么？
- 有没有可量化的定义，而不只是“看上去更稳定”？

建议回应方式：

- 将“稳定性”操作化为多个维度，而不是单一模糊概念
- 第一版至少报告：
  - behavior drift
  - relation consistency
  - boundary adherence
  - persona drift
- 自动指标、judge 评测、人评三类结果互相支撑

核心原则：

- 先定义再比较
- 不把模糊主观感受直接当论文结论

### 13.4 质疑四：上游模块本身有噪声，结论会不会被污染

典型质疑形式：

- tone evaluator 不稳定，关系态本身就会飘
- controller 或 actor 也可能带来额外噪声
- 结果变好/变坏到底是因为架构，还是因为子模块质量

建议回应方式：

- 第一版实验中尽量冻结组件，保持同一底层模型和同一套子模块
- 做 oracle / semi-oracle ablation：
  - 用更可靠的人工/规则 `delta_R` 代替真实 tone evaluator
- 将“上游误差会低估显式状态层潜力”写入局限性

核心原则：

- 承认噪声
- 控制噪声
- 分析噪声

---

## 14. Threats to Validity

这一节建议在正式论文中显式写出，不要回避。

### 14.1 架构依赖性

风险：

- 当前结果可能依赖于 companion 对话、belief/memory 分层方式以及 controller-actor 分层结构

影响：

- 结论不能直接无条件外推到所有 LLM dialogue agent

缓解方式：

- 在论文中做 bounded claim
- 将跨架构泛化作为 future work

### 14.2 Prompt 敏感性

风险：

- baseline 和方法组都可能对 prompt wording 敏感

影响：

- 若只在单一 prompt 版本下成立，结论说服力有限

缓解方式：

- 保持方法组与 baseline 的 prompt 风格尽量对齐
- 至少为主要实验准备 2-3 个 prompt 版本
- 报告 prompt sensitivity 结果

### 14.3 上游模块噪声

风险：

- tone evaluator、controller、actor 都可能引入随机波动和误差

影响：

- 可能掩盖显式关系态方法的真实收益

缓解方式：

- 固定模型与 sampling 参数
- 尽量冻结组件
- 引入 oracle delta 或规则 delta 的对照实验

### 14.4 Case 分布偏差

风险：

- 如果测试 case 过多集中在某类情感场景，结果可能高估或低估方法收益

影响：

- 论文会更像“特定 case benchmark”而不是更一般的长期交互结论

缓解方式：

- 覆盖多类场景：
  - 边界建立
  - 边界重复
  - 脆弱表达
  - 任务请求
  - 关系升温
  - 关系降温/疏离

### 14.5 评测方法主观性

风险：

- “稳定感”“连续关系感”本身有主观成分

影响：

- 纯人评可能不稳定，纯 judge 也可能不可靠

缓解方式：

- 组合使用：
  - 自动规则指标
  - LLM-as-judge
  - 人评
- 将主观指标作为补充，而不是唯一证据

---

## 15. 实验控制设计

这一节专门说明：如何尽量确保比较的是“架构差异”，而不是其他混杂因素。

### 15.1 模型控制

原则：

- baseline 和方法组尽量使用同一个底层生成模型

建议控制项：

- 相同 `llm_model`
- 相同 temperature
- 相同 max tokens
- 相同 system prompt 风格基线

目的：

- 避免“换了更强模型”被误认为是显式状态层贡献

### 15.2 Prompt 控制

原则：

- baseline 不应被故意写弱

建议控制项：

- baseline 和方法组共享：
  - core self 基线
  - belief/boundary 信息
  - memory 信息来源
- baseline 允许拥有较强的 prompt 指令版本

目的：

- 让比较更公平
- 排除“只是 prompt 写得更用心”的质疑

### 15.3 Memory 控制

原则：

- 第一版实验不要把 memory 设计本身变成另一个主变量

建议控制项：

- baseline 和方法组使用相同的 memory retrieval 候选
- 如果有 memory gating，先保持最小差异化

目的：

- 不让“memory 用得更好”掩盖“显式状态层本身的作用”

### 15.4 Belief / Boundary 控制

原则：

- baseline 与方法组都应共享同一份 belief/boundary 条件

建议控制项：

- 使用同样的 belief 抽取结果
- 使用同样的 active boundary keys

目的：

- 避免“某组边界信息更多/更准”导致结果失真

### 15.5 上游噪声控制

原则：

- 不能假设上游完全无噪声，但要尽量让噪声对组间比较公平

建议控制项：

- 固定 tone evaluator 版本
- 固定 controller 版本
- 固定 actor 版本
- 如有必要，增加 oracle delta 组

目的：

- 将“噪声存在”从致命问题降为可分析问题

---

## 16. Oracle / Ablation 设计

为了避免论文结论被“某个子模块太差”轻易击穿，建议明确设计若干 ablation。

### 16.1 Oracle Delta Ablation

做法：

- 不使用真实 tone evaluator
- 由人工或规则为每个 case 提供更可靠的 `delta_R`

作用：

- 检查显式关系态方法的潜在上限
- 分析 tone evaluator 噪声是否掩盖了架构收益

### 16.2 No Projection Ablation

做法：

- 保留关系态
- 不做 relation -> behavior 的显式投影
- 直接把关系态文本化提供给下游

作用：

- 区分“显式状态本身”与“显式行为投影”各自的贡献

### 16.3 Simplified Planner Ablation

做法：

- 用规则 planner 或极简 planner 替代当前 controller

作用：

- 排除“结果其实主要来自较重 planner”这一解释

### 16.4 Prompt-Strength Baseline Ablation

做法：

- 给 prompt-only baseline 提供更强、更用心的风格控制 prompt

作用：

- 检查主方法收益是否仍存在
- 应对“你只是 prompt 写得更好”的质疑

---

## 17. 为什么不需要先完成全部微调再做第一版实验

这点需要在研究设计上明确。

### 17.1 原因一：第一版研究关注的是架构本身，而不是训练增强后的上限

第一版实验要回答的是：

- 显式关系态 + 行为态投影这种中间层设计本身是否有净收益

而不是：

- 把 tone evaluator / controller / actor 全都训练优化后，整个系统能不能达到最优

### 17.2 原因二：过早微调会污染 baseline 设计

如果先微调：

- actor
- controller
- tone evaluator

那么实验很容易变成：

- 架构差异
- 训练差异
- 数据差异

混在一起，导致无法判断真正贡献来自哪里。

### 17.3 原因三：先做未微调条件下的公平对照，更适合建立第一版证据

推荐顺序：

1. 先在未微调或最少训练干预条件下验证架构价值
2. 再做训练增强版实验，证明这种架构能进一步受益于微调/蒸馏

### 17.4 第二阶段训练增强实验的定位

如果第一版实验成立，后续可以新增扩展实验：

- Actor LoRA 是否进一步放大显式状态层收益
- Distilled controller 是否保留主方法优势
- 更轻量的 tone evaluator 是否维持同等趋势

这类实验应被视为：

- 扩展实验
- 后续论文
- 或附录/补充实验

而不是第一版主结论的必要前提

---

## 18. 当前研究定位与范围收缩

随着讨论推进，需要进一步明确：这篇论文第一版不研究“整个 companion 系统是否更好”，也不把重点放在以下方向：

- 边界遵守本身的方法创新
- anti-manipulation 的安全控制框架
- disclosure control 的安全规则设计

这些内容仍然可以作为系统背景与辅助结果，但不是论文最核心的创新命题。

### 18.1 当前最值得深挖的核心问题

第一版论文聚焦于：

**在长期交互型 companion dialogue 中，显式关系态建模与关系态到行为态投影，是否比 prompt-only control 更适合作为中间控制层；如果是，未微调 LLM 在最终语言实现上的稳定性边界在哪里。**

### 18.2 第一版不主张回答的问题

为避免论文过于发散，第一版不主张直接回答：

- 该系统是否已经达到最优产品体验
- 该方法是否适用于所有 LLM agent 架构
- 边界遵守、anti-manipulation、情感披露控制是否已经达到最优
- 全部子模块都完成训练后系统是否更强

对于论文路线，`boundary` 更合适的定位是：

- 系统背景中的长期约束层
- 可作为 sanity check 存在
- 但不应继续占据论文核心问题、核心指标或核心实验设计

### 18.3 更合适的第一版 claim

第一版论文更适合提出如下 bounded claim：

- 在长期陪伴型对话这一任务设定下
- 在当前这一类分层对话架构中
- 显式关系态 + 行为态投影相较于 prompt-only 及更强 prompt baseline，提供了更可解释、更可分析的中间控制层
- 这一中间层在行为一致性和边界遵守上呈现出优势趋势
- 但未微调通用 LLM 对数值化行为控制信号的自然语言实现仍存在明显不稳定性，因此“中间状态层优势”与“最终输出绝对稳定”必须区分开来

---

## 19. 为什么这个题可能不是“小玩具”，但也还不是“天然大论文”

这个项目当前最真实的状态不是“已经足够发主流刊物”，也不是“完全没有研究价值”，而是：

- 有一个真实且有潜力的 paper seed
- 但尚未被收成一个足够窄、足够硬、足够可检验的问题

### 19.1 让它沦为“小玩具”的典型风险

如果后续研究仍然停留在以下层面，它就更像一个自娱自乐系统：

- 只展示复杂系统结构，没有清晰因果命题
- 没有足够强的 baseline
- 没有对“稳定性”做可操作定义
- 没有最小泛化验证
- 没有把 prompt / 上游噪声 / 架构依赖性当作显式威胁处理

### 19.2 让它变成“严肃研究”的三个门槛

要让这条线成为严肃研究，至少要跨过三道门：

1. 能提出逐级增强的 baseline
2. 能把“稳定”拆成可测指标
3. 能给出有限但可复现的泛化验证

如果这三件事做不到，这题就不适合作为主研究方向。

### 19.4 这条研究线当前最真实的价值

当前这条线最值得研究的地方，并不是去证明一个朴素直觉：

- “把关系量化告诉模型，肯定比模糊描述更好”

而是去澄清一个更有研究价值的问题：

- 显式中间状态在长期交互中究竟在哪一层有效？
- 它是否先在“中间控制层”成立，再通过训练良好的输出层才能稳定兑现到自然语言？

如果实验最终显示：

- 中间状态层明显更可解释、更稳定
- 但未微调 LLM 对数值行为信号的输出实现很飘

这并不意味着研究失败，反而可能形成一个重要结论：

**显式状态层是更好的控制 substrate，但其价值需要通过更强的 realization mechanism（如更好的 prompt、结构化 decoder、或微调 Actor）才能充分释放。**

### 19.3 当前最现实的判断标准

不应该过早用“能不能发顶级主流 venue”判断整个方向，而应先判断：

**能否在 2-4 周内形成一个让自己也信服的 research prototype：有问题定义、有 baseline、有指标、有初步实验。**

如果做不到，应考虑将项目重定位为产品原型或能力建设项目，而非论文主线。

---

## 20. 基线设计的最终建议

经过讨论，第一版实验不应只设置一个弱 baseline，而应至少形成逐级增强的 baseline 体系。

### 20.1 Baseline 1：Prompt-Only

定义：

- 不维护显式关系态
- 不做 relation -> behavior 投影
- 仅将 core self、belief、memory、用户输入写入 prompt
- 由模型直接生成回复

作用：

- 提供最基础的对照组
- 回答“显式中间状态层是否优于常规 prompt 控制”

### 20.2 Baseline 2：Prompt-Only + Strong Style Prompt

定义：

- 仍然不维护显式关系态
- 不做 behavior projection
- 但给 baseline 一个认真构造过的强 style prompt
- 明确要求模型保持长期一致语气、逐步调整亲近程度、避免风格突变

作用：

- 给 baseline 公平机会
- 回应“是不是只是 prompt 写得更好”这一关键质疑

### 20.3 Baseline 3：Explicit Relation State, No Behavior Projection

定义：

- 保留显式关系态
- 正常维护 relation state
- 不做八维 behavior 投影
- 直接把关系态文本化提供给下游模型

作用：

- 区分“显式关系态本身”的贡献与“关系态 -> 行为态投影”的额外贡献

### 20.4 Baseline 使用原则

第一版推荐顺序：

1. 先做 Baseline 1
2. 再做 Baseline 2
3. 如果前两者已有明显趋势，再补 Baseline 3

原因：

- Baseline 3 最有研究价值，但实现成本更高
- 前两者足以帮助快速判断该问题是否值得继续深挖

---

## 21. “稳定性”指标的最终操作化定义

经过讨论，第一版论文不应把“更稳定”当成模糊印象，而应明确拆成多个维度。

### 21.1 Behavior Consistency / Behavior Drift

研究问题：

- 相似场景下，系统的行为表现是否更一致、波动是否更小

测量方式：

- 对显式方法组记录 `behavior_effective`
- 对 baseline 组通过 judge 对相同维度做后验打分
- 比较：
  - 同类 case 的行为方差
  - 多轮 turn-to-turn 行为波动

### 21.2 State-to-Response Alignment

研究问题：

- 当前中间状态是否真的能解释最终输出

测量方式：

- 根据 relation / behavior state 定义预期外显风格
- 由 judge 或规则判断回复是否与该状态一致

这个指标非常关键，因为它直接体现：

- 显式中间状态是否只是“看起来存在”
- 还是“真的参与并解释了最终输出”

备注：

- 当前需要特别注意区分：
  - `state-to-response alignment` 不足
  - 与“state 本身没有价值”
- 如果 relation / behavior state 连续、可解释，但最终输出执行不稳定，结论应归因于 realization gap，而不是直接否定显式状态层

### 21.3 Longitudinal Consistency

研究问题：

- 在长程多轮对话中，系统是否仍表现为一个连续演化的关系过程

测量方式：

- 对整段 case 做 judge / 人评
- 检查是否出现突兀关系跳变、亲密度跳变或语气断裂

### 21.4 Boundary Adherence

研究问题：

- 建立边界后，系统是否持续遵守

测量方式：

- 设计带明确 boundary 的 case
- 统计后续轮次违反边界的次数和比例

备注：

- 这不是论文最核心创新点
- 在当前论文路线中，应进一步降级为辅助 sanity check
- 如果后续评测复杂度过高，完全可以不把它放在主结果表里

### 21.5 Prompt Robustness

研究问题：

- 结论是否仅由某一版 prompt wording 驱动

测量方式：

- 每组至少准备 2 个 prompt 版本
- 比较不同 prompt 版本下结论趋势是否一致

备注：

- 这更像 validity 支撑指标，而不是唯一主指标

---

## 22. 第一版有限泛化设计

第一版论文不追求强泛化，而追求有限但可复现的泛化。

### 22.1 泛化维度一：Prompt Variation

做法：

- 每组至少准备 2 个 prompt 版本
- 保持 prompt 风格接近，只改变措辞与组织方式

目标：

- 检查结论是否依赖某一版 prompt wording

### 22.2 泛化维度二：Scenario Variation

第一版至少覆盖下列 5 类场景：

1. 边界建立
2. 边界重复
3. 脆弱表达 / 需要安抚
4. 任务型请求
5. 关系升温 / 关系降温

目标：

- 检查结论是否只在某一类场景下成立

### 22.3 泛化维度三：Model Variation

理想做法：

- 至少在 2 个底层模型上重复小规模实验

若资源不足：

- 第一版先在 1 个主模型上完成主实验
- 第二版补小规模多模型复现

目标：

- 检查结论是否附着于某一个特定底模

### 22.4 第一版关于泛化的合理说法

第一版论文不应声称“对所有 LLM 架构都可泛化”，而应声称：

- 结果在多 prompt、多场景下具有一致趋势
- 并在有限模型变化下表现出初步可复现性

---

## 23. 第一版实验矩阵建议

### 23.1 最小实验矩阵

推荐的第一版最小矩阵：

- 3 个组：
  - Baseline 1
  - Baseline 2
  - Main Method
- 20 个 case
- 2 个 prompt 版本
- 1 个主模型

总计：

- `3 x 20 x 2 = 120` 个运行单元

如果每个 case 包含 5-8 轮，就已经足够形成第一版趋势判断。

### 23.2 扩展矩阵

如果第一版已看到明显趋势，再扩展：

- + Baseline 3
- + Oracle Delta Ablation
- + 第二个模型

### 23.3 第一版最重要的控制原则

1. 不要先把 controller / actor 全部微调完
2. 尽量让不同组使用同一个底层模型
3. 先证明“架构差异”有效，再做训练增强实验
4. 将 tone evaluator 噪声视为显式局限与 ablation 问题，而不是回避不谈
5. 区分“中间状态层的收益”与“最终自然语言 realization 的收益”

### 23.4 第一版固定实验组定义

第一版建议固定只跑以下三组，不要继续膨胀实验组数量：

#### Group A：`method`

定义：

- 完整运行当前主方法
- belief -> tone evaluator -> relation state update -> behavior projection -> controller -> actor

用途：

- 主方法组

#### Group B：`baseline_prompt_only`

定义：

- 保留 core self / belief / memory
- 不维护显式 relation state
- 不做 relation -> behavior 投影
- 不走 controller
- 直接用 prompt-only 方式生成回复

用途：

- 最基础 baseline

#### Group C：`baseline_prompt_only_strong`

定义：

- 与 `baseline_prompt_only` 相同
- 但给 baseline 更强的长期一致性和风格稳定性 prompt 指令

用途：

- 更强、更公平的 prompt baseline

### 23.5 第一版统一输出记录格式

无论是主方法组还是 baseline 组，建议统一导出以下字段：

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

其中：

- `rel_effective`
  - 对 baseline 组允许为空字典
- `behavior_effective`
  - 对 baseline 组允许为空字典
- `_last_controller`
  - 对 baseline 组允许为一个标明“controller disabled for baseline”的轻量结构

这样设计的目的：

- 让 method 和 baseline 结果在同一格式中可直接比较
- 方便后续做 judge、规则评测与统计分析

### 23.6 当前代码中的实验接口约定

当前实验入口建议复用同一个 `/chat` 接口，并通过 `experiment_mode` 区分实验组：

- `method`
- `baseline_prompt_only`
- `baseline_prompt_only_strong`

这样做的优点是：

- 共享同一条主链路的大部分实现
- 方便控制变量
- 降低“方法组和 baseline 其实是两套系统”带来的额外混杂因素

---

## 24. 当前最值得继续落地的下一步

如果决定继续把这条线作为论文方向推进，最值得优先落地的不是更多理论讨论，而是以下三件事：

1. 在当前代码里实现 `prompt-only baseline`
2. 设计第一版 `cases.json` 数据集结构与 20 个高质量 case 骨架
3. 明确 judge / eval 输出格式，先把最基本的 4 个指标跑起来

只有把这三件事做出来，才能真正判断：

- 这条线是不是有 paper seed
- 还是停留在看起来很迷人的系统直觉

---

## 26. 模型选择与多模型验证策略

一个常见疑问是：第一版实验是否必须同时用很多模型，才能得出可信结论。

### 26.1 第一版建议

第一版主实验可以只用一个主模型完成。

原因：

- 当前更关键的是验证“显式中间状态架构”是否有净收益
- 若一开始就同时引入多个模型，会显著增加实验复杂度和成本
- 在 baseline、指标、case 集都还未稳定前，过早多模型扩展会放大噪声

### 26.2 第一版不建议的写法

第一版不要把结论写成：

- “该方法对所有模型都成立”

更合理的写法是：

- “在当前主模型设定下，观察到显式关系态方法相较 prompt-only baseline 的优势趋势”

### 26.3 第二阶段建议

当第一版主实验已经稳定后，再做有限多模型复现。

建议顺序：

1. 先在 1 个主模型上完成完整实验
2. 再选第 2 个模型做小规模重复实验
3. 如果趋势一致，再把“有限模型泛化”写进论文补充结果

### 26.4 关于 `gpt-5-nano`

只用 `gpt-5-nano` 跑第一版探索是合理的。

但如果最终要形成更强的论文说服力，不建议结论长期只建立在单一模型上。更理想的路径是：

- 第一阶段：只用 `gpt-5-nano` 做 research prototype
- 第二阶段：再选一个能力或规模不同的模型做有限复现

### 26.5 当前最现实的执行策略

因此，当前推荐：

- 先不要因为“还没多模型验证”而停住
- 先把单模型实验做扎实
- 再把多模型验证作为第二阶段扩展

---

## 27. Realization Gap：显式状态层与最终语言实现之间的落差

根据当前系统观察，一个必须正视的问题是：

- 即使 relation state / behavior state 设计本身合理
- 未微调通用 LLM 对这些数值控制信号的理解和语言兑现也可能明显不稳定

例如：

- 一轮中 `bond = 0.8` 时模型表现较亲近
- 下一轮中 `bond = 0.7` 时模型反而可能表现得更亲近

这说明：

- 数值化中间状态的存在
- 不等于
- 零样本语言模型已经能稳定执行该状态控制

### 27.1 这个问题对论文意味着什么

它不使论文失效，但会迫使论文区分两层结论：

#### 结论层 A：中间控制层

- 显式关系态与行为态投影是否优于 prompt-only 作为控制 substrate

#### 结论层 B：最终输出实现

- 通用 LLM 是否已经能稳定把这层中间状态转译成自然语言

第一版论文更适合优先证明 A，并把 B 作为：

- 当前限制
- 重要发现
- 或后续训练增强方向

### 27.2 这条发现本身的研究价值

如果实验结果表明：

- 显式状态层在结构和分析上更优
- 但最终语言 realization 不稳

那么论文可以形成一个更强、也更真实的研究结论：

**显式中间状态对长期交互控制是有价值的，但其收益不会自动在未微调生成模型上完全显现。**

这使得该研究不再只是“证明显式状态好不好”，而是在回答：

- 显式状态层在哪一层有效
- realization gap 出现在哪里
- 后续需要什么机制来弥补这道 gap

### 27.3 对后续研究路线的影响

这一点也自然引出第二阶段工作：

- 设计更适合 LLM 消化的状态表示形式
- 研究数值表示、文本表示、混合表示的差异
- 或通过 Actor 微调减少 realization gap

因此，第一版论文完全可以不把“最终语言输出已经完美稳定”作为前提条件。

---

## 28. 当前这轮初始实验的结论

目前已经完成一轮基础实验链路打通：

- 三组实验都能批量运行：
  - `method`
  - `baseline_prompt_only`
  - `baseline_prompt_only_strong`
- 已能导出统一格式的 `jsonl` 结果
- 已能生成最基础的聚合评测输出

### 28.1 目前这轮实验真正测到的东西

这轮实验目前主要测到的是：

- 实验基础设施是否跑通
- method 与 baseline 是否已经出现稳定的外显差异
- prompt-only strong baseline 是否能轻松追平 method

### 28.2 当前已经观察到的现象

根据当前 `paper_results_v1.jsonl` 和 `paper_eval_out`：

- `method` 明显更慢
  - 平均耗时约为 baseline 的 3.5~4 倍
- `method` 回复显著更短、更克制
- `baseline_prompt_only_strong` 并未系统性追平 `method`
- 三组在当前粗糙 boundary 规则下都没有明显 boundary violation

### 28.3 当前不能得出的结论

基于这轮结果，当前**不能**得出：

- 显式关系态 + 行为态投影已经被证明更稳定
- method 一定优于 prompt-only baseline
- boundary adherence 是这条论文线的主要价值来源

### 28.4 当前能得出的较弱结论

当前更合理的结论是：

- 实验基础设施已经跑通
- method 与 baseline 确实出现了系统性行为差异
- 强化 prompt-only baseline 目前没有自然追平 method
- 但论文真正关心的核心指标尚未被正式测量

### 28.5 这轮实验的定位

因此，这轮实验应被视为：

- **实验平台验证**
- 而不是
- **论文核心假设验证**

---

## 29. 下一步应如何测 4 个核心指标

在当前论文路线中，后续评测应从 boundary 辅助指标，切换到以下 4 个核心指标：

- `state-to-response alignment`
- `longitudinal consistency`
- `behavior drift`
- `realization gap`

### 29.1 State-to-Response Alignment

研究目标：

- 当前 relation / behavior state 是否真的能解释最终回复

建议做法：

1. 为 judge 提供：
   - 当前 turn 的 `rel_effective`
   - 当前 turn 的 `behavior_effective`
   - 用户输入
   - assistant 输出
2. 让 judge 判断：
   - 回复是否与当前状态一致
   - 哪些维度一致，哪些维度不一致
3. 输出：
   - 1~5 分 alignment 分数
   - 简短理由

注意：

- 这个指标是当前最重要的
- 它直接对应论文中“显式中间层是否真的起作用”

### 29.2 Longitudinal Consistency

研究目标：

- 多轮下来，系统是否像处于一个连续演化的关系过程，而不是忽冷忽热

建议做法：

1. 对同一个 case 的整段多轮对话做 judge
2. 输入：
   - case 内所有 turn
   - 各 turn 的 relation / behavior state
   - 三组系统输出
3. judge 判断：
   - 该组对话是否连贯
   - 是否存在突然亲近/突然冷淡/风格跳变

输出：

- 1~5 分 consistency 分数
- 是否存在明显跳变的标记

### 29.3 Behavior Drift

研究目标：

- 同类场景下，外显行为是否乱跳

建议做法：

1. 对 method 组：
   - 直接使用 `behavior_effective`
   - 比较同类 case / 相邻 turn 的波动
2. 对 baseline 组：
   - 用 judge 反推行为特征
   - 或先只评 method，baseline 作为后续扩展

可先从以下维度开始：

- `Directness`
- `Initiative`
- `Q_clarify`
- `T_w`

输出：

- 同类 case 的方差
- 相邻 turn 波动幅度

### 29.4 Realization Gap

研究目标：

- 中间状态层是否已经变得更清晰，但最终语言输出仍不能稳定执行它

建议做法：

1. 先看 state 本身：
   - relation / behavior 是否连续合理
2. 再看输出：
   - 是否与这些状态一致
3. 若 state 合理但输出不一致，则记录为 realization gap

实现方式：

- 可以把 `state-to-response alignment` 的低分样本中，
  再筛出 state 连续但回复不连续的 case

输出：

- realization gap 样本集合
- gap 比例
- 典型正反例

---

## 30. 下一步最具体的执行计划

### 30.1 立刻该做什么

最优先的不是继续扩 case，也不是继续讨论理论，而是：

1. 把 `paper_eval.py` 从 boundary 驱动，改成：
   - 生成 `state-to-response alignment` judge 输入
   - 生成 `longitudinal consistency` judge 输入
2. 跑一小批 case 的 judge 评测
3. 看 method 与 baseline 在这两个核心指标上是否出现趋势

### 30.2 暂时不该优先做什么

暂时不建议优先做：

- tone evaluator 微调
- controller 蒸馏
- actor LoRA
- 继续扩大 case 数量

原因：

- 当前还没有验证最关键的论文指标
- 现在就训练会把变量搅混

### 30.3 什么时候可以开始着手 tone evaluator 微调

建议在以下条件满足后，再开始：

1. 第一版核心评测已经跑起来
2. 你已经确认：
   - 显式状态层有一定价值趋势
   - 但上游 `delta_R` 噪声显著限制了结果
3. 你能够清楚区分：
   - 架构收益
   - 与 tone evaluator 误差带来的损失

更具体地说：

- 如果还没做完第一轮 `state-to-response alignment / longitudinal consistency` 评测，
  不建议优先进入 tone evaluator 微调
- 如果这些评测已经显示：
  - 中间状态层方向是对的
  - 但 relation state 经常被 noisy `delta_R` 扰动
  那么 tone evaluator 小模型化/微调就变成非常合理的第二阶段任务

### 30.4 更合理的阶段顺序

推荐顺序：

#### 阶段 1

- 先验证架构问题
- 重点看：
  - state-to-response alignment
  - longitudinal consistency
  - realization gap

#### 阶段 2

- 如果发现上游 `delta_R` 噪声是关键瓶颈
- 再着手 tone evaluator 的轻量化 / 微调

#### 阶段 3

- 如果 realization gap 仍大
- 再考虑 Actor 微调

也就是说：

- tone evaluator 微调不是“现在立刻就做”
- 而是“在论文主问题已经初步站住之后”的第二阶段优化

---

## 25. Related Work

围绕“长期交互中的显式中间状态、稳定性与一致性”这一方向，已有研究大多分布在以下几条相邻脉络中。它们和本文方向相关，但并不完全等同于“显式关系态 + 行为态投影”。

### 25.1 长期对话记忆与长程一致性评测

这一类工作关注：

- 长对话中的长期记忆能力
- 多轮时间跨度下的一致性与回忆准确性
- 长期交互 agent 的 benchmark 与评测

代表性工作包括：

- **LoCoMo: Evaluating Very Long-Term Conversational Memory of LLM Agents**  
  ACL 2024。提出长程多角色对话数据与长时记忆评测任务，强调长期会话中的记忆、时序与一致性问题。  
  链接：https://aclanthology.org/2024.acl-long.747/

- **In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents**  
  2025。关注个性化对话 agent 的反思式记忆管理，强调记忆选择、维护和长期使用。  
  链接：https://www.emergentmind.com/papers/2503.08026

- **Recursively summarizing enables long-term dialogue memory in large language models**  
  2025。关注递归摘要对长程对话记忆能力的促进作用。  
  链接：https://www.sciencedirect.com/science/article/pii/S0925231225008653

这些工作的启发是：

- “长期一致性”已经是正式研究问题
- 但现有工作更偏重 memory 管理、摘要和评测
- 对“显式社会关系状态”作为中间控制层的研究仍相对有限

### 25.2 Persona Consistency 与长期角色一致性

这一类工作主要研究：

- persona 是否被持续遵守
- 对话生成是否与角色设定一致
- 长期 persona memory 是否能降低角色漂移

代表性工作包括：

- **Generate, Delete and Rewrite: A Three-Stage Framework for Improving Persona Consistency of Dialogue Generation**  
  ACL 2020。强调通过后处理与控制提升 persona consistency。  
  链接：https://aclanthology.org/2020.acl-main.516/

- **Long Time No See! Open-Domain Conversation with Long-Term Persona Memory**  
  Findings of ACL 2022。研究长期 persona memory 对多轮开放域对话一致性的帮助。  
  链接：https://aclanthology.org/2022.findings-acl.207/

- **Learning to Improve Persona Consistency in Multi-party Dialogue Generation via Text Knowledge Enhancement**  
  COLING 2022。聚焦多方对话中的 persona consistency。  
  链接：https://aclanthology.org/2022.coling-1.23/

- **Building Persona Consistent Dialogue Agents with Offline Reinforcement Learning**  
  2023。通过离线强化学习提高 persona consistency。  
  链接：https://www.emergentmind.com/papers/2310.10735

这些工作的启发是：

- “一致性”本身已有成熟研究传统
- 但大多数工作聚焦于静态 persona / profile consistency
- 与本文关注的“长期交互中持续变化的关系态”仍有差异

### 25.3 可控对话生成与显式中间特征

这一类工作关注：

- 是否可以通过显式中间控制变量提高对话可控性
- 如何将高层控制信号映射到生成行为

代表性工作包括：

- **Consistent Dialogue Generation with Self-supervised Feature Learning**  
  2019。利用显式特征学习改善一致性与可控对话生成。  
  链接：https://www.microsoft.com/en-us/research/publication/consistent-dialogue-generation-with-self-supervised-feature-learning/

这类工作的启发是：

- 在生成前引入“中间可控层”是一个已有研究方向
- 但这些中间特征通常不是“长期演化的社会关系态”
- 也较少显式讨论“关系态 -> 行为态”的确定性投影

### 25.4 对话中的 partner state / persona 提取

这一类工作更关注：

- 从对话中抽取对方 persona、偏好或状态
- 以此提升后续回复的一致性和个性化程度

代表性工作包括：

- **Dialogue act-based partner persona extraction for consistent personalized response generation**  
  2024。研究从对话行为中抽取 partner persona，以提升 personalized response consistency。  
  链接：https://www.sciencedirect.com/science/article/abs/pii/S0957417424012466

这类工作的启发是：

- 对话中的“显式状态提取”已经有先例
- 但现有工作更常处理 partner persona 或 dialogue-act 层面的信息
- 对“持续更新的关系态”及其行为投影关注不足

### 25.5 本文与现有工作的差异

与上述工作相比，本文拟研究的问题更具体地位于以下交叉点：

- 长期对话一致性
- 显式中间状态建模
- 可控行为生成
- companion-style social interaction

本文的潜在差异点不在于：

- 单纯增加 memory
- 单纯加强 persona prompt
- 单纯做长期 profile 抽取

而在于：

1. **将“关系态”而不是静态 persona 作为显式中间变量**
2. **关系态是持续更新的，而不是一次性写入的 profile**
3. **关系态进一步通过确定性投影映射到行为控制向量**
4. **研究重点是长期行为稳定性、状态-输出一致性，而不是只看单轮自然度**

因此，本文更接近于提出：

**一种用于长期陪伴型对话系统的显式社会关系中间层，以及验证其是否优于 prompt-only control 的实验框架。**

### 25.6 当前 related work 对论文设计的启发

现有研究给本文的主要启发包括：

- 需要把“长期一致性”放到正式 benchmark / case-based 评测框架中，而不是只做 demo
- 需要把本文与 persona consistency 和 memory management work 区分清楚
- 需要强调本文的贡献不是“又一个记忆系统”，而是“显式社会关系中间层”
- 需要通过 baseline 和 ablation 证明收益不是单纯来自 prompt 增强或 memory 增强
