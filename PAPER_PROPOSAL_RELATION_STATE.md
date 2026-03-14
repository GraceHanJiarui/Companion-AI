# 论文构想：显式关系态建模与行为态投影

## 1. 核心研究命题

对于长期陪伴型对话系统，纯 prompt 控制难以稳定维持关系一致性。显式关系态建模与关系态到行为态投影提供了一种更可解释、更可控的中间层，可提升长期行为稳定性与边界遵守。

这篇论文的核心不是“做了一个复杂的陪伴系统”，而是回答一个更一般的研究问题：

- 在长期交互型对话系统中，显式社会关系状态建模，是否比纯 prompt 控制更稳定、更可控、更可解释？

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

1. 在长期陪伴型对话中，显式关系态建模是否比纯 prompt 控制更稳定？
2. 关系态到行为态的确定性投影，是否能降低 persona drift 和行为漂移？
3. 显式中间状态是否能提高边界遵守率与系统可解释性？

### 4.2 核心假设

- H1：显式关系态 + 行为态投影在长期多轮交互中具有更低的行为漂移。
- H2：显式中间状态有助于更稳定地执行用户边界与长期偏好。
- H3：显式状态系统更容易进行调试、分析和蒸馏。

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
