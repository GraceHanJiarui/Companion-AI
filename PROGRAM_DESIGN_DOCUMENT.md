# Program Design Document

## 1. 项目目的

这个项目是一个面向长期陪伴型角色系统的后端架构。目标不只是“生成一条自然的回复”，而是让系统在长期互动中逐步形成连续性：

- 记住重要互动
- 根据关系变化调整行为
- 长期尊重用户边界
- 在保持生命感表达的同时，避免滑向操控和情感勒索

因此，这个系统不是一个“超长 prompt 聊天机器人”，而是一个带状态、带记忆、带行为控制的多模块对话系统。

## 2. 设计目标

### 功能目标

- 通过 `POST /chat` 支持多轮对话
- 持久化完整对话历史
- 提取并保存长期有效的 belief / boundary
- 检索语义相关的长期记忆
- 在每轮对话后更新内部关系状态
- 在生成自然语言前先做一层行为规划
- 提供可观测、可调试的内部状态查看接口

### 非功能目标

- 可控性
- 可解释性
- 可调试性
- 模块化
- 为未来蒸馏和微调保留结构空间

## 3. 高层架构

当前系统的运行结构大致如下：

1. API 接收用户消息
2. 将事件写入数据库
3. 抽取 belief / boundary
4. 估计关系增量 `ΔR`
5. 更新有效关系状态
6. 由关系态投影出行为态
7. 执行 memory retrieval
8. Controller 生成结构化 plan
9. Actor 生成最终自然语言回复
10. 写入 debug 信息和 turn snapshot

核心实现文件包括：

- `app/main.py`
- `app/api/chat.py`
- `app/beliefs/policy.py`
- `app/relational/projector.py`
- `app/memory/memories.py`
- `app/controller/controller_client.py`
- `app/generation/actor_prompt.py`

## 4. 主链路设计

### 4.1 Event Logging

实现位置：

- `app/api/chat.py`
- `app/memory/events.py`
- `app/models/event.py`

当前行为：

- 用户消息写入 `events`
- Assistant 回复也写入 `events`
- 在事件日志层面采用 append-only 模式

这样设计的原因：

- 可以完整回放任意 session
- 下游模块都能基于统一的原始事件流工作
- 方便后续做分析、记忆构建和排障

### 4.2 Belief Extraction

实现位置：

- `app/beliefs/extract.py`
- `app/beliefs/extract_llm.py`
- `app/beliefs/store.py`
- `app/beliefs/apply.py`
- `app/models/belief.py`

当前设计：

- `/chat` 主链路中启用的是同步规则抽取
- 项目中已经存在结构化的 LLM belief extractor
- belief 会带 evidence 信息和状态字段落库
- 重复 belief 会被去重
- 相同 key 的新 belief 会 supersede 旧 belief

这样设计的原因：

- 用户边界和偏好不应该只在当前轮生效
- 系统需要稳定的长期行为约束，而不是每轮临时塞进 prompt
- 将 belief 抽取从 Actor 中拆出来，更容易维护和调试

### 4.3 Relationship State Update

实现位置：

- `app/inference/tone_evaluator.py`
- `app/beliefs/policy.py`
- `app/models/session_state.py`

状态结构：

- `rel_trait`
- `rel_state_boost`
- `rel_effective`

四个关系维度：

- `bond`
- `care`
- `trust`
- `stability`

当前更新逻辑：

- tone evaluator 使用 LLM 输出结构化 `delta_R`
- `apply_tone_delta()` 先对短期 boost 做衰减
- 再根据当前轮增量和置信度更新 boost
- 最后重新计算有效关系态并缓存进 policy

当前演进方向说明：

- 当前实现仍是通用 LLM evaluator
- 但后续主路线不再是 rule-based evaluator，也不优先是小 LLM JSON 生成
- 当前更明确的替换方向是：
  - 用小型文本模型做连续 `delta_R` 回归
  - 核心监督字段优先保留：
    - `delta_R`
    - `confidence`
    - `scene / signals` 降为次级 debug 字段，后续再决定是否保留为附属预测目标

当前对 `tone evaluator` 职责边界的进一步收敛：

- `tone evaluator` 不应依赖长期 `belief`
- 它的核心职责应收敛为：
  - 读取本轮输入文本
  - 结合前一轮关系态快照
  - 估计关系态增量 `delta_R`
- 它不是：
  - 长期边界执行层
  - controller 式策略规划层

因此在后续小型文本模型回归路线下，当前更推荐的核心输入为：

- `user_text`
- `prev.rel_effective`
- 可选的轻量上下文快照

而不把长期 `belief` 作为核心监督输入的一部分

当前已补充的 `delta_R` 标注约束：

- 在正式批量导出 teacher 数据前，先统一 `delta_R labeling policy v1`
- 当前约束包括：
  - 单维范围：每维 `delta_R` 限制在 `[-0.05, 0.05]`
  - 总量限制：`L1 <= 0.10`
  - 死区规则：若某维 `|delta| < 0.015`，直接归零
  - 若四维全部落入死区，则整轮 `delta_R = 0`
  - 无明确关系信号时，默认优先给 `delta_R = 0`

这样做的原因：

- 关系态应作为慢变量，小步更新
- 若 teacher 本身抖动过大，后续小模型只会学习噪声
- 因此批量 teacher 生成和导出前必须先统一标注尺度

关系态职责边界的当前收敛结论：

- `core_self` 与 `belief` 负责：
  - 人格底色
  - 长期边界
  - 硬约束
- `relation state` 不负责 permission / acceptance / policy gating
- `relation state` 描述的是：
  - 在 `core_self` 与 `belief` 之外
  - 这个 AI 与用户的关系已经发展到什么状态
  - 以及这种关系如何自然投影成更接近人与人关系发展的互动模式

这意味着：

- 若 `core_self / belief` 没有明确禁止，模型允许自然出现更像真实关系发展的行为变化
- 包括但不限于：
  - 被纠偏
  - 深入追问
  - 任务指挥感
  - 关系推进
- 这些不应被建模为“用户是否授权”，而应被视为关系动态本身的一部分

当前四维关系态的推荐定义也据此收敛为：

- `bond`
  - 连接感、共同体感、彼此牵引感
- `care`
  - 主动在意对方状态、愿意为对方分配心理资源的强度
- `trust`
  - 关系中承受真实碰撞、被指出、被深入、被直接回应的能力
  - 不是许可概念
- `stability`
  - 关系连续性的稳固感、安全感、是否处于易断裂/易退缩状态

关于四维是否最终固定的当前立场：

- 当前并不声称人与人关系“被且仅被”这四维完全定义
- 但在现阶段，这四维仍作为系统用于驱动行为投影的最小核心连续关系变量
- 在没有明确证据前，不建议过早扩维

基于近期反例压力测试，当前结论进一步收敛为：

- 在本项目当前产品前提下，AI 与用户的底层关系结构固定为“助手 / 陪伴体”
- 因此关系态模型的目标不是模拟完整的人类社会关系体系
- 而是在这一固定关系结构内部，建模关系发展强度与互动变化

这意味着：

- 许多在一般社会学意义上可能需要额外维度的差异
  - 例如平等朋友、恋人、导师/学生等结构类型差异
  - 并不是当前产品边界内必须建模的对象
- 在这一前提下，`bond / care / trust / stability` 当前很可能已经构成一组足够小且足够完整的关系态 basis
- 当前尚未发现必须新增第五维关系态的明确反例

当前保留疑点：

- “独特牵引关系 / 不可替代性” 当前暂时可视为 `bond` 的高阶语义
- 但这一判断仍保留开放性
- 若后续出现无法被现有四维与映射层解释的稳定反例，需要重新审视它是否应继续完全吸收在 `bond` 中

当前更值得怀疑的地方不在维度数量，而在映射层：

- 当前系统的主要风险更可能出现在“关系态 -> 行为态”的映射过于僵硬或使用不足
- 尤其是 `stability` 的作用目前偏弱
- 当前它主要显著影响 `Disclosure_Content`
- 但理论上它还应当更广泛影响：
  - 主动推进节奏
  - 情绪确认方式
  - 关系记忆调用节奏
  - 互动连续性与收放方式

因此在 `tone evaluator` 小型模型化推进上，当前更合理的阶段顺序是：

1. 先完成 teacher 数据记录与导出
2. 先收敛一版关系态 -> 行为态映射
3. 再进行正式 baseline 训练与替换评估

原因是：

- `tone evaluator` 预测的是 `delta_R`
- 但 `delta_R` 的优劣最终要通过行为投影来判断
- 若映射层尚未稳定，过早训练会让监督目标与评估标准一同漂移

这样设计的原因：

- 关系变化应该是小步累积，而不是每轮重新生成一个全新人格
- 把有效状态缓存下来，便于调试和给 controller 提供稳定输入
- 将 trait 和短期状态分开，可以显著降低 persona 抖动

### 4.4 Relation-to-Behavior Projection

实现位置：

- `app/relational/projector.py`

当前行为维度：

- `E`
- `Q_clarify`
- `Directness`
- `T_w`
- `Q_aff`
- `Initiative`
- `Disclosure_Content`
- `Disclosure_Style`

当前设计：

- 行为态由有效关系态确定性投影得到
- `scene` 标签和 active boundary 会对投影结果做轻微偏置
- 行为结果会缓存到 `policy_json`

当前阶段的进一步理解：

- 行为态当前主要承担“关系如何外显”的作用
- 当前已确认四维关系态本身在产品边界下基本够用
- 因此下一阶段更应优先审视：
  - 投影公式是否过于刚性
  - `stability` 是否被低估
  - 是否把某些本应由投影层表达的现象误判成“关系态缺维”

这样设计的原因：

- 在内部关系态和外部语言行为之间建立一层稳定桥梁
- 避免把所有风格控制都压给 Actor 自己临场理解
- 保留较强的可解释性，便于以后蒸馏或替换模型

## 5. Memory Architecture

### 5.1 事件历史与长期记忆分离

系统明确区分：

- 原始事件历史 `events`
- 摘要式 episodic memory `memories`

这样设计的原因：

- 全量历史适合回放、审计和构建衍生模块
- 长期记忆适合做紧凑语义召回
- 这两类数据的用途和检索方式不同，不应混在一起

### 5.2 Embedding 与 Memory Retrieval

实现位置：

- `app/memory/embedder.py`
- `app/memory/memories.py`
- `app/models/memory.py`

当前实现：

- embedding 模型：`text-embedding-3-small`
- 向量维度：1536
- 检索方式：pgvector 余弦距离 top-k
- 下游只传 memory preview，而不是把完整 memory 全部塞给 controller

为什么选 pgvector：

- 当前 memory 规模还适合放在主库中检索
- 运维复杂度低
- 关系数据和向量数据可以留在同一数据库
- 比单独引入一套向量数据库更适合当前阶段

### 5.3 Summary Memory

相关逻辑位于：

- `app/memory/memories.py`

设计意图：

- 定期对最近一段对话窗口做摘要
- 将摘要写入 `memories`
- 用事件范围字段避免重复总结同一段历史

当前状态说明：

- 这条 summary 路径已经完成第一轮主链路接线修复
- 当前更准确的状态是“代码契约已初步对齐，待做真实端到端写入验证”

## 6. Controller / Actor 分层

### 6.1 Controller

实现位置：

- `app/controller/prompts.py`
- `app/controller/plan.py`
- `app/controller/controller_client.py`

职责：

- 输出结构化 plan，而不是直接回复用户
- 以当前行为态为基线做本轮规划
- 选择需要注入的 memory
- 作为长期 `belief` 进入主链路决策的主要入口

当前 Plan 主要包括：

- `intent`
- `behavior`
- `selected_memories`
- `notes`

这样设计的原因：

- 结构化 planning 比自由文本中间推理更容易检查
- Controller 后续更容易蒸馏成规则或小模型
- Actor 收到的是更干净、更聚焦的控制信号

### 6.2 Actor

实现位置：

- `app/generation/actor_prompt.py`
- `app/core/llm_client.py`

职责：

- 将 plan 落成自然语言
- 保持在行为态和披露规则之内
- 不暴露内部系统机制
- 避免操控式表达

当前关于 `belief` 的进一步立场：

- `actor` 不应直接深度消费原始 `belief`
- “actor 是否直接读取 belief、读多少” 当前保留为开放问题
- 后续若需要，也更倾向于由 `controller` 提供本轮约束摘要，而不是让 `actor` 自行解释全量 belief

当前 Actor prompt 中包含：

- core self / 人格基线
- 行为变量解释
- disclosure gating 规则
- 明确的 anti-obligation / anti-manipulation 约束

这样设计的原因：

- Actor 是直接面向用户的表达层
- 将表达和 policy 推理拆开后，更容易做风格调试和后续 LoRA 微调
- 这部分 prompt 也是未来最适合“规则内化”的部分

## 7. Core Self

实现位置：

- `app/core/core_self.py`
- `app/models/core_self.py`

当前设计：

- core self 存在数据库中，支持版本化
- 服务启动时如果为空会自动 seed 一份默认人格
- Actor prompt 会注入当前 active 的 core self

与关系态边界的配合方式：

- `core_self` 定义的是“这个存在本来是谁”
- 它不随短期互动频繁波动
- 它与 `belief` 一起决定：
  - 哪些行为是这个存在本来就不会做的
  - 哪些边界是长期不能越过的
- 在这些边界之外，`relation state` 才负责描述与用户关系的演化

这样设计的原因：

- 人格稳定性需要一个持久化基线
- 版本化更适合长期演进
- 把 core self 和短期关系状态分开，可以避免“身份基线”和“当前情绪波动”混在一起

## 8. 数据持久化模型

### `events`

作用：

- 作为会话的 canonical append-only 日志

### `beliefs`

作用：

- 保存长期有效的边界、偏好、相处风格等约束

### `session_state`

作用：

- 保存 session 级 policy 缓存以及关系/行为状态

### `memories`

作用：

- 保存摘要式长期记忆

### `core_self_versions`

作用：

- 保存可版本化的人格基线

### `turn_events`

作用：

- 保存每轮快照，用于行为分析和调试

### `outbox_jobs`

作用：

- 保存后台异步任务

## 9. Debug 与可观测性

实现位置：

- `app/api/debug.py`
- `app/api/sessions.py`

当前可查看内容包括：

- 当前关系态和行为态
- 当前 active beliefs
- core self 概览
- 可选的 memory retrieval 结果
- 完整事件流

当前系统还会记录：

- trace id
- latency breakdown
- 最近一次 controller 输出摘要
- 最近一次关系增量
- 可选的 extractor / apply 调试信息

为 `tone evaluator` 训练准备新增的记录方向：

- 当前已开始把每轮 teacher 输入输出快照持久化到 `turn_events`
- 目标是支持后续导出：
  - `user_text`
  - `prev_rel_effective`
  - teacher `delta_R`
  - teacher `confidence`
  - `trace_id / teacher_model` 等元信息

这样做的原因：

- 当前 `session_state.policy_json` 中的 `_last_rel_delta` 是覆盖式 debug 信息
- 不适合作为长期训练样本来源
- `turn_events` 更适合作为逐轮持久化样本载体

这样设计的原因：

- 多阶段 LLM 系统的问题通常不是“模型坏了”这么简单
- 需要能区分是 memory、policy、controller、actor 还是状态更新出了问题
- 没有显式中间状态，就很难排查“为什么这轮说成这样”

## 10. Outbox Pattern

实现位置：

- `app/outbox/enqueue.py`
- `app/outbox/worker.py`
- `app/models/outbox_job.py`

当前设计：

- 任务会写入 `outbox_jobs`
- worker 定期轮询 pending job
- 通过 `FOR UPDATE SKIP LOCKED` 认领任务
- 根据处理结果更新任务状态

这样设计的原因：

- 一些 LLM 任务不应该阻塞主对话链路
- 基于数据库的任务队列对当前项目足够简单实用
- 适合低到中等吞吐量的后台任务

当前状态说明：

- 异步 belief extraction 的代码接线已经完成第一轮修复
- 当前更准确的状态是“代码链路已接通，待做真实运行验证”

## 11. 测试与分析脚本

### `test/batch_style_tests.py`

作用：

- 通过真实 API 批量跑 case，检查风格和约束是否生效

当前检查项包括：

- disclosure gating
- 自体情绪披露后的“解义务”表达
- leave context 泄漏

### `actor_batch_probe.py`

作用：

- 在不同 behavior profile 下离线探测 Actor 的输出
- 为后续分析、数据整理或训练集构建做准备

为什么这些工具重要：

- 这个系统的质量不只取决于“单条回复像不像人”
- 更重要的是长期行为是否稳定、规则是否真正落地
- 后续做 LoRA 或蒸馏之前，必须先有批量评估能力

### `export_tone_dataset.py`

作用：

- 从 `turn_events.tone_eval` 中导出 `tone evaluator` 训练样本
- 为后续小型文本模型回归提供初版 JSONL 数据集

当前确认的样本 schema v1：

- `input`
  - `user_text`
  - `prev_rel_effective`
- `target`
  - `delta_R`
  - `confidence`
- `meta`
  - `turn_event_id`
  - `session_id`
  - `created_at`
  - `trace_id`
  - `teacher_model`
  - `source`

当前推荐的训练输入模板：

```text
User: {user_text}
PrevRelEffective: bond={bond} care={care} trust={trust} stability={stability}
```

当前数据导出与清洗要求：

- 导出时应同时保留：
  - raw teacher output
  - cleaned target
  - 是否触发裁剪/归零
  - 后处理必须至少执行：
    - 单维 clamp
    - `L1` 总量截断
    - 死区归零

### `generate_tone_teacher_labels.py`

作用：

- 批量调用 LLM 生成 `tone evaluator` 的 teacher 标注
- 将 raw teacher 输出进一步清洗为适合训练的 `cleaned_target`

当前 v1 输入输出格式：

- 输入：
  - 基础 JSONL 样本
  - 其中包含：
    - `input`
    - `meta`
- 输出：
  - `input`
  - `raw_teacher`
  - `cleaned_target`
  - `cleaning`
  - `meta`

当前 v1 清洗流程：

- 单维 clamp 到 `[-0.05, 0.05]`
- `L1 <= 0.10` 总量截断
- 死区归零（`|delta| < 0.015 -> 0`）
- 记录清洗痕迹，供后续人工审查与数据筛选

## 12. 技术选型说明

### FastAPI

选择原因：

- 适合编排多阶段异步 pipeline
- 请求模型和响应模型组织清晰
- debug 接口开发成本低

### PostgreSQL

选择原因：

- 能稳定承载事件日志和 belief 这种事务型数据
- 支持 JSON 和常规关系查询
- 可以和 pgvector 集成
- 也可以顺带承载 outbox queue

### pgvector

选择原因：

- 当前 memory retrieval 规模适合放在数据库内解决
- 不需要过早引入额外的向量数据库系统

### SQLAlchemy + Alembic

选择原因：

- 当前 schema 仍在演化
- 长期状态系统必须有迁移管理能力

### 结构化 LLM 调用

选择原因：

- Controller、tone evaluator、belief extractor 这类中间模块更适合产出机器可读结果
- 比从自由文本里硬解析更稳定、更容易 debug

## 13. 当前代码中的已知缺口

以下内容是“当前实现状态说明”，不是设计目标：

- 异步 belief extraction 链路已完成第一轮代码修复，但仍缺少真实端到端运行验证
- summary memory 主链路与 `memories.py` 的调用契约已完成第一轮修复，但仍缺少真实写入验证
- Actor 已接入 `actor_model -> llm_model` fallback，后续仍需要做多模型配置下的真实运行验证
- 部分实验脚本带有本地环境假设，复用前需要手动核对

## 14. Roadmap 对齐性

当前架构与以下未来方向是兼容的：

- 对 Actor 做 LoRA 微调，把 prompt 规则内化进模型
- 将 Controller 蒸馏成规则系统或更小的模型
- 将 tone evaluator 换成轻量模型
  - 当前更推荐的小型化方向是小型文本模型回归，而不是固定规则系统
- 显著降低端到端 latency

这也是为什么系统被拆成显式模块，而不是做成一个“大一统 prompt 链”。

## 15. 维护建议

后续迭代时，建议尽量保持以下边界不被打散：

- event logging 仍然作为 canonical append-only 数据层
- belief 仍然保持持久化和可检查
- relation state 仍然保持显式，而不是藏进 prompt
- behavior projection 仍然保持可解释
- controller 和 actor 仍然保持分离
- 只要状态结构有变化，debug view 也要同步更新

如果这些边界被打散，系统可能依然能“说话”，但会很快失去可调试性、可评估性和长期演化能力。
