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
