# ToDo

本文件用于记录这个项目当前已识别出的优化方向、问题背景、相关代码位置、目标状态和建议修改路径。

设计原则：

- 让一个没有当前对话上下文、只看代码和本文件的工程师或 LLM，也能理解项目接下来该往哪里改
- 每条 ToDo 尽量包含：问题、影响、相关文件、目标、建议方案、优先级
- 该文件不是泛泛 roadmap，而是尽量可执行的工程待办

---

## 优先级总览

这个版块用于回答三个问题：

- 现在最该先做什么
- 哪些事项必须建立在前面的事项已验证/已收口之后
- 哪些事项属于中长期，不应过早展开

### 第一优先级：先验证现有链路，建立可运行基线

1. [先做最小端到端验证与运行闭环确认](#todo-e2e-validation)
   - 这是当前所有后续优化的前置条件
   - 在真实运行验证前，不应对“是否真的修好”“真正瓶颈在哪”下结论
2. [降低 `/chat` 端到端延迟](#todo-latency)
   - 必须先有端到端可运行基线，才能做 latency 对比
3. [将 Tone Evaluator 轻量化或替换](#todo-tone-evaluator)
   - 依赖前面的运行基线和分段耗时，避免盲改
4. [将 Controller 蒸馏或规则化](#todo-controller)
   - 依赖 controller 输入/输出在真实链路中已验证稳定
5. [优化 Actor Prompt，逐步将规则内化](#todo-actor-prompt)
   - 依赖已有可运行 actor 链路和回归工具

### 第二优先级：在主链路稳定后提升质量与可训练性

6. [继续完善 Debug / Observability，而不是在优化中削弱它](#todo-observability)
   - 应与性能优化并行推进，但落位在“有运行基线”之后
7. [记忆系统升级方案：向更成熟的长期记忆体验推进](#todo-memory-upgrade)
   - 必须晚于现有 retrieval / summary / debug 链路跑通
8. [质量提升与更成熟模型架构方向](#todo-mature-architecture)
   - 建立在 controller / actor / memory 基础能力已经稳定之上

### 当前推荐执行顺序

1. 先跑通最小端到端验证、健康检查、debug 查看、最小批量回归
2. 再验证第一轮已修复链路：
   - async belief extractor
   - summary memory
   - `actor_model / controller_model` 配置路径
3. 再做低风险主链路收口：
   - 缓存 `core_self`
   - 减少重复状态读取
   - 并行化只读且互不依赖的步骤
   - 将 summary / richer belief extraction 移出同步路径
4. 再减少主链路中的 LLM 调用：
   - 先 `tone evaluator`
   - 后 `controller`
5. 再做 actor prompt 精简、batch probe、训练数据导出、LoRA 准备
6. 最后再推进记忆系统升级、consolidation / rewrite、更成熟的 planner / actor 架构

### 明确的前置依赖

- 没有端到端运行验证前，不应推进性能结论和大规模架构调整
- 没有稳定 debug 基线前，不应贸然重写 `tone evaluator` 或 `controller`
- 没有稳定的 controller 输出、memory 输出和导出链路前，不应推进蒸馏/微调
- memory 的 rerank / gating 应先于 consolidation / rewrite
- Actor 微调准备应晚于回归工具和数据导出链路稳定

---

## 0. 当前产品状态判断

当前系统的架构方向是清晰的：

- 有完整的事件日志层
- 有 belief / boundary 长期约束层
- 有 session 级关系状态与行为态缓存
- 有长期记忆召回
- 有 controller / actor 分层
- 有 debug API 和批量探测脚本

但当前更接近“研究型原型”，距离“可实时使用的产品”还差一轮系统级优化，主要问题集中在：

- 主链路过长
- LLM 调用次数过多
- 多个步骤串行执行
- 可异步的工作仍在同步路径上
- 某些状态读取/缓存策略仍偏 MVP

---

<a id="todo-e2e-validation"></a>
## 0A. 先做最小端到端验证与运行闭环确认

### 0A.1 问题

当前项目已经完成了一轮“坏链路修复”和文档收口，但仍有多个关键链路停留在“代码看起来已接通，尚未真实运行验证”的状态。若不先做最小端到端验证，后续的性能优化、规则替换和训练准备都会建立在不稳定地基上。

当前最需要验证的不是“所有高级能力都完美可用”，而是以下最小闭环是否真实成立：

1. Docker 中的 Postgres/pgvector 可启动并可连接
2. Alembic 可完成 schema 迁移
3. FastAPI 服务可启动
4. `/health/llm` 可通过真实 LLM 配置打通
5. `POST /chat` 能跑通主链路并返回 reply
6. `/debug` 能看到 relation / behavior / controller / rel_delta
7. `beliefs`、`events`、`turn_events` 能按预期落库
8. 第一轮已修复链路能在真实运行中验证：
   - async belief extractor
   - summary memory
   - `actor_model / controller_model` 配置路径

### 0A.2 影响

- 若这一层不先验证，后续 latency 优化无法判断收益是否真实
- 若 LLM、数据库、迁移、debug 任一基础环节未通，后续 ToDo 的优先级判断会失真
- 若没有最小回归闭环，后续对 controller / actor / memory 的改动容易引入隐性回归

### 0A.3 相关文件

- `docker-compose.yml`
- `.env`
- `README.md`
- `app/main.py`
- `app/api/chat.py`
- `app/api/debug.py`
- `app/api/health.py`
- `app/outbox/worker.py`
- `app/memory/memories.py`
- `test/batch_style_tests.py`

### 0A.4 目标状态

- 建立一套可重复执行的最小端到端验证流程
- 明确区分：
  - 已静态修复但未运行验证
  - 已通过最小真实运行验证
  - 已通过批量回归验证
- 为后续性能、架构、训练相关改动提供稳定基线

### 0A.5 建议修改方向

- 把“最小 E2E 验证”视为当前最高优先级任务，而不是杂项
- 先验证主链路，再验证异步链路，不要一上来追求全覆盖
- 验证顺序建议固定为：
  1. Docker DB
  2. Alembic migration
  3. FastAPI startup
  4. `/health/llm`
  5. `/chat`
  6. `/debug`
  7. `test/batch_style_tests.py`
- 对第一轮已修复链路分别记录验证状态：
  - outbox belief extractor
  - summary memory
  - actor/controller model config
- 在 `log.md` 中单独记录“已验证到哪一步”，不要只写“看起来已修好”

### 0A.5.1 当前验证进展（2026-03-13）

本轮已经完成一轮最小真实运行验证，确认以下链路已经打通：

- Docker 中的 Postgres/pgvector 可启动并可连接
- FastAPI 服务可启动
- `/health/llm` 已通过真实 LLM 配置打通
- `POST /chat` 已能返回 reply
- `/debug/sessions/{session_id}/state?slim=1` 已能返回：
  - relation state
  - behavior projection
  - `_last_controller`
  - `_last_rel_delta`
  - latency breakdown
- `/debug/sessions/{session_id}/context?slim=1` 已能返回：
  - active core self
  - policy_view
  - beliefs / memories 视图

本轮验证还暴露出以下信息：

- 当前主链路已确认存在显著 latency 问题
  - `tone_delta` 约 10s
  - `controller` 约 13s
  - `memory_retrieve` 约 1.4s
  - 总时延约 25s
- 这进一步验证了 [降低 `/chat` 端到端延迟](#todo-latency)、[将 Tone Evaluator 轻量化或替换](#todo-tone-evaluator)、[将 Controller 蒸馏或规则化](#todo-controller) 的优先级判断是正确的

本轮尚未确认通过的点：

- `actor_model / controller_model` 多模型配置路径验证

### 0A.5.2 下一步建议

- 无需先清空数据库
  - 当前验证更适合通过新 session 隔离，而不是破坏已有验证样本
- 若通过 PowerShell 直接发送中文请求时出现编码污染，应先修正测试输入编码
  - 当前已确认可通过 UTF-8 文件 + `charset=utf-8` 的方式稳定发送中文请求
- 本轮最低成本活性确认现已完成，下一步继续做：
   - `actor_model / controller_model` 多模型配置验证
   - 低风险 latency 优化
   - `tone evaluator` 轻量化
   - `controller` 收敛

### 0A.5.3 boundary 专项验证结果（2026-03-13）

本轮 boundary 输入专项验证已经通过，验证结果基于修正后的 UTF-8 请求发送方式。

已验证通过的点：

- `/sessions/{session_id}/events` 中 user content 已正确记录中文输入
- `/debug/sessions/{session_id}/beliefs` 中已成功写入 boundary belief：
  - `kind=boundary`
  - `key=no_unsolicited_emotion_questions`
- `/debug/sessions/{session_id}/state?slim=1` 中 relation / behavior / rel_delta / controller 均正常
- tone evaluator 的 `scene / signals` 已能反映 boundary 语义：
  - `no_emotion_probing`
  - `emotional_boundary_set`
  - `boundary_respected`

当前可得出的结论：

- boundary belief 的同步规则抽取链路正常
- 之前 `beliefs` 为空的原因是请求输入编码污染，不是 extractor 本身失效
- 当前最主要的未解决问题已再次收敛为主链路延迟过高

建议的后续顺序：

1. 验证 `actor_model / controller_model` 多模型配置路径
2. 开始进入低风险 latency 优化
3. 进入 `tone evaluator` 轻量化
4. 进入 `controller` 收敛

### 0A.5.4 最低成本活性确认结果（2026-03-13）

本轮用于“确认链路是真活的，而不是伪接通”的三项补充验收已完成，并已通过：

- `turn_events`
  - 已确认每轮对话快照可正常写入
- async belief extractor
  - 已确认 outbox 入队、认领、执行闭环可运行
- summary memory
  - 已确认 summary 生成与 `memories` 写入链路可运行

当前可据此做出的工程判断：

- 当前主链路相关基础能力已不是“是否能跑通”的问题
- 后续主线应转向：
  - 延迟优化
  - `tone evaluator` 轻量化
  - `controller` 收敛
  - actor / memory 质量提升

### 0A.6 与后续任务的依赖关系

- 是 [降低 `/chat` 端到端延迟](#todo-latency) 的前置条件
- 是 [将 Tone Evaluator 轻量化或替换](#todo-tone-evaluator) 的前置条件
- 是 [将 Controller 蒸馏或规则化](#todo-controller) 的前置条件
- 是 [优化 Actor Prompt，逐步将规则内化](#todo-actor-prompt) 的前置条件
- 是 [记忆系统升级方案：向更成熟的长期记忆体验推进](#todo-memory-upgrade) 的前置条件

### 0A.7 优先级

`P0`

---

<a id="todo-latency"></a>
## 1. 降低 `/chat` 端到端延迟

### 1.1 问题

当前 `POST /chat` 主链路包含多个远程调用和数据库写入，端到端 latency 预期较高。根据代码结构，主要步骤包括：

1. event logging
2. belief extraction / belief loading
3. tone evaluator
4. memory embedding + retrieval
5. controller
6. actor
7. turn snapshot
8. optional summary

其中最可能主导延迟的是：

- tone evaluator LLM 调用
- controller LLM 调用
- actor LLM 调用
- embedding 调用

### 1.2 影响

- 当前系统难以达到实时陪伴产品体验
- 用户等待时间过长
- 迭代 prompt / controller / actor 时调试成本高

### 1.3 相关文件

- `app/api/chat.py`
- `app/core/llm_client.py`
- `app/inference/tone_evaluator.py`
- `app/controller/controller_client.py`
- `app/memory/embedder.py`
- `app/memory/memories.py`

### 1.4 目标状态

- 先将端到端时延显著降到可接受范围
- 中期目标是把主链路压缩到更接近实时的体验

### 1.5 建议修改方向

- 将能并行的步骤从串行改为并行
- 将能异步补全的工作移出主链路
- 优先减少结构化 LLM 子模块的调用次数
- 在 debug 中继续保留精确分段耗时，方便优化前后对比

### 1.5.1 建议优先落地的低风险延迟优化

- 缓存 `core_self`
  - 当前读取成本虽小，但属于稳定低频数据，适合进程内缓存
- 减少重复状态读取
  - 例如主链路中 `boundary_keys`、`policy` 的重复整理可以收口
- 避免在热路径中保留临时调试输出
- 对只读且互不依赖的步骤做并行化评估
  - 尤其是 `core_self` 获取、部分状态整理、部分 retrieval 前后处理

#### 当前进展（2026-03-13）

本轮已完成第一批低风险延迟优化代码改动：

- 已为 `core_self` 增加进程内 TTL 缓存
- 已在 `/chat` 主链路中收口重复的：
  - `policy` 读取
  - `boundary_keys` 整理
  - `core_self preview` 截取

当前状态说明：

- 这批改动属于低风险收口，不改变既有行为语义
- 已通过 Python 编译检查
- 已完成一次最小真实 latency 复测，对比结果显示存在实际收益：
  - `tone_delta`: 约 `10.3s -> 8.9s`
  - `memory_retrieve`: 约 `1.4s -> 1.3s`
  - `controller`: 约 `13.7s -> 10.9s`
  - `total_ms`: 约 `25.4s -> 21.3s`
- 这说明第一批低风险收口是有效的，但主瓶颈仍然明确集中在：
  - `tone evaluator`
  - `controller`

#### 当前结论（2026-03-13）

- 第一批低风险延迟优化可以视为已完成
- 后续不再继续在这一轮深挖并行化
- 下一阶段主线直接进入 [将 Tone Evaluator 轻量化或替换](#todo-tone-evaluator)

### 1.5.2 不建议优先做的延迟优化

- 不建议一上来切换向量数据库
- 不建议一上来引入额外 rerank 模型
- 不建议一上来重写整个 controller / actor 架构

原因：

- 当前最大收益仍来自“先修链路、减少 LLM 调用、并行化与异步化”

### 1.6 优先级

`P0`

---

<a id="todo-tone-evaluator"></a>
## 2. 将 Tone Evaluator 轻量化或替换

### 2.1 问题

当前每轮都调用 `ToneEvaluatorClient` 推断关系增量 `delta_R`：

- 逻辑位置：`app/api/chat.py`
- 实现位置：`app/inference/tone_evaluator.py`

这个模块的任务边界较窄，输出是结构化 JSON，且只服务于关系状态更新。长期来看，继续使用通用大模型会造成不必要的延迟和成本。

### 2.2 影响

- 增加主链路一次完整 LLM 调用
- 推高总体时延和调用成本
- 对产品化部署不友好

### 2.3 相关文件

- `app/api/chat.py`
- `app/inference/tone_evaluator.py`
- `app/beliefs/policy.py`

### 2.4 目标状态

- tone evaluator 不再依赖一次昂贵的通用 LLM 调用
- 保持输出结构兼容现有 `apply_tone_delta()` 流程

### 2.5 建议修改方向

- 不再将 rule-based evaluator 作为主路线
  - 原因是固定规则与粗粒度场景分类可扩展性差，且与当前项目对连续、多维内部状态的方向不一致
- 当前优先路线改为：小型文本模型回归
  - 输入：`user_text`、`active_boundary_keys`、轻量 `prev` 状态
  - 核心监督字段只保留：
    - `delta_R`
    - `confidence`
- `scene / signals` 降为次级字段
  - 可先不进入核心监督目标
  - 后续可作为 debug 派生字段或多任务附属目标再补
- 训练数据优先来自现有运行时 teacher 输出
  - 先把当前大模型 evaluator 的输出作为 teacher label
  - 先做数据导出和评测方案，再进入模型训练与替换
- 当前阶段不优先采用：
  - 蒸馏/微调小 LLM 保留 JSON 输出
  - 非 LLM 多头回归
  - 原因分别是：
    - 前者仍保留较高推理成本
    - 后者对个人开发阶段的数据工程压力偏大

### 2.5.1 当前收敛结论（2026-03-13）

当前已确认的 `tone evaluator` 路线为：

- 主路线：小型文本模型回归
- 核心目标：预测连续 `delta_R` 四维 + `confidence`
- 次级字段：`scene / signals` 暂不进入核心监督
- 当前下一步：先做训练数据方案与导出链路设计，再做 baseline 训练

### 2.5.2 关系态定义边界收敛（2026-03-13）

在进入 `tone evaluator` 训练方案之前，当前已确认一个更上游的设计边界：

- `core_self` 与 `belief` 负责：
  - 人格底色
  - 长期边界
  - 不可越过的硬约束
- `relation state` 不负责：
  - 用户是否“授权”模型出现某种行为
  - interaction permission / policy gating
- `relation state` 负责描述的是：
  - 在 `core_self` 与 `belief` 之外
  - 这个 AI 与用户之间的关系已经发展到什么状态
  - 以及这种关系状态如何自然投影为更像“人与人互动”的交流模式

这意味着：

- 关系态不是 permission system
- 若 `core_self / belief` 没有明确禁止，模型应允许自然出现：
  - 被纠偏
  - 深入追问
  - 任务指挥感
  - 关系推进
- 这些不是外部许可逻辑，而是“生命感 / 互动感 / 关系发展感”的核心组成部分

### 2.5.2A 模块职责边界的进一步收敛（2026-03-14）

在继续推进 `tone evaluator` 训练方案前，当前又进一步收敛了模块职责边界：

- `tone evaluator`
  - 不应依赖长期 `belief`
  - 核心职责是：
    - 根据本轮输入文本
    - 估计关系态增量 `delta_R`
  - 它不是长期边界执行层，也不是策略规划层
- `belief`
  - 主要消费者应是 `controller`
  - 用于影响本轮决策、边界遵守、memory use 和策略选择
- `actor`
  - 不应直接深度消费原始 `belief`
  - “actor 是否直接读取 belief、读多少” 当前暂时保留为开放问题
  - 后续再单独讨论

当前收敛后的工程判断：

- `tone evaluator` 的训练目标应进一步纯化
- teacher 样本的核心输入应围绕：
  - `user_text`
  - `prev` 关系态快照
- 不应把长期 `belief` 直接并入 `tone evaluator` 的核心监督输入

### 2.5.3 关于 `delta_R` 四维是否暂时固定的当前结论

当前结论不是“人与人关系被且仅被四维定义”，而是：

- 当前系统用于驱动行为投影的最小核心连续关系变量，暂时仍保留为四维：
  - `bond`
  - `care`
  - `trust`
  - `stability`
- 保留原因是：
  - 现有工程结构已经围绕它们建立
  - 它们足够小、连续、可解释
  - 在没有明确证据前，不宜过早扩维
- 但需要明确：
  - 这四维不是对“关系本体”的最终哲学定义
  - 而是当前系统中“足以驱动行为投影”的最小核心关系状态表示

#### 基于反例压力测试的进一步收敛（2026-03-13）

经过多轮反例压力测试，当前对四维关系态的判断进一步收敛为：

- 在当前产品前提下：
  - AI 与用户的底层关系结构固定为“助手 / 陪伴体”
  - 关系变化发生在这一结构内部，而不是切换成其他社会角色类型
- 因此当前关系态模型的任务是：
  - 模拟关系发展强度
  - 而不是建模完整的人类关系结构类型

当前已测试的几个候选反例包括：

- “深度默契搭子” vs “温柔照顾者”
  - 当前四维可区分
- “平等朋友” vs “照顾者关系”
  - 主要差异属于关系结构类型，不属于当前产品边界
- “通用温柔支持” vs “独特牵引关系”
  - 当前可先视为 `bond` 的高阶语义

当前阶段结论：

- 在当前产品约束下，`bond / care / trust / stability` 很可能已经是一组足够小且足够完整的关系态 basis
- 当前尚未发现必须新增第五维关系态的反例
- 当前更值得怀疑的问题已经从“关系态维度数量”转移到“关系态 -> 行为态”的映射质量

保留疑点：

- “独特牵引关系 / 不可替代性” 当前暂时可被解释为 `bond` 的高阶语义
- 但这一点尚未被永久性定死
- 后续若出现：
  - 四维取值接近
  - 但“独特牵引感”明显不同
  - 且这种差异不能被当前映射层解释
  - 则需要重新审视它是否应继续完全吸收在 `bond` 中

### 2.5.4 四维关系态的当前推荐定义

- `bond`
  - 连接感、共同体感、彼此牵引感
- `care`
  - 主动在意对方状态、愿意为对方分配心理资源的强度
- `trust`
  - 关系中承受真实碰撞、被指出、被深入、被直接回应的能力
  - 不是“用户授权”
- `stability`
  - 关系连续性的稳固感、安全感、是否处于易断裂/易退缩状态

### 2.5.5 当前不建议采取的方向

- 不建议把 `relation state` 重解释成 permission / acceptance system
- 不建议在当前阶段为了覆盖更多现象而立刻扩维
- 不建议让 `tone evaluator` 学习“用户是否允许模型这样做”
  - 这类硬约束应优先落在 `core_self / belief`

### 2.5.6 当前最值得继续检验的地方

当前最值得继续检验的不是“是否需要第五维”，而是：

- 四维关系态 -> 八维行为态 的映射是否足够自然
- `stability` 是否被充分使用

当前已识别出的重点怀疑点：

- `stability` 在当前映射中作用偏弱
- 当前它主要显著影响：
  - `Disclosure_Content`
- 但理论上它还可能影响：
  - `Initiative`
  - 情绪确认方式
  - 关系记忆调用节奏
  - 互动推进节奏

因此下一阶段更合理的主线不是扩维，而是：

- 先继续保留四维关系态
- 审视并改进关系态 -> 行为态映射

### 2.5.7 关于 `tone evaluator` 训练启动时机的当前判断

当前建议不是立刻冻结目标并开始正式训练，而是区分“现在就能做的部分”和“应在映射收敛后再做的部分”。

现在就适合开始：

- `tone evaluator` teacher 数据记录与导出
- 样本字段设计
- 训练/验证集切分方案
- 基础分布分析

最好在关系态 -> 行为态映射先收敛一版后再做：

- 正式 baseline 训练
- 线上替换决策
- 以行为投影效果为目标的误差评估

原因：

- `tone evaluator` 预测的是 `delta_R`
- 但 `delta_R` 是否“好”，最终要看它投影到行为态后是否符合设计目标
- 若映射层很快要调整，过早训练会让监督目标和评估标准一起漂移

#### 当前进展（2026-03-13）

本轮已正式启动 `tone evaluator` 的训练准备工作，并已完成第一步：

- 已将 teacher 输入输出快照持久化到 `turn_events.tone_eval`
- 已新增初版导出脚本：
  - `export_tone_dataset.py`

当前这一步的目标不是开始正式训练，而是先建立稳定的数据生产链路。

### 2.5.8 `delta_R labeling policy v1`（2026-03-14）

在正式批量导出 teacher 数据前，当前已确认需要先统一 `delta_R` 的标注/生成标准，以降低 teacher 抖动。

#### 核心目标

- 先保证 `delta_R` 的方向稳定性与小步更新性质
- 明确什么情况下应输出非零更新
- 明确什么情况下宁可输出 `0`，也不输出似是而非的小波动

#### v1 约束

1. 单维范围限制
- 每一维 `delta_R.{bond, care, trust, stability}` 必须限制在：
  - `[-0.05, 0.05]`

2. 总量限制
- 四维总变化量采用 `L1` 约束：
  - `|bond| + |care| + |trust| + |stability| <= 0.10`

3. 死区 / 零更新规则
- 若某一维 `|delta| < 0.015`，则该维直接置 `0`
- 若四维全部落入死区，则整轮 `delta_R = 0`

4. 非零更新触发条件
- 只有在存在明确关系信号时，才优先考虑非零更新，例如：
  - 明确边界表达
  - 明确脆弱表达
  - 明确关系确认/关系试探
  - 明确离开/暂停
  - 明确感谢、信任、依赖、失望、疏离
  - 明确冲突、被纠偏、关系修复
- 对以下场景，默认优先输出 `delta_R = 0`：
  - 纯技术请求
  - 普通信息问答
  - 无明显关系信号的短句
  - 模糊噪声输入

5. confidence 规则
- `confidence` 也应接受规范化约束
- 若无明确关系信号，默认不应给高置信的非零更新
- 若最终判定 `delta_R = 0`，允许输出：
  - “高置信地判断本轮不该更新”

#### 当前工程要求

- 批量 teacher 生成脚本必须显式包含上述约束
- 生成后还必须进行程序级清洗：
  - clamp 单维范围
  - 执行 `L1` 截断
  - 执行死区归零
- 应同时保留：
  - raw teacher output
  - cleaned target
  - 是否触发过裁剪/归零

#### 当前样本 schema v1（已确认）

当前已确认的 `tone evaluator` 样本 schema v1 为：

- `input`
  - `user_text`
  - `prev_rel_effective`
- `target`
  - `delta_R.bond`
  - `delta_R.care`
  - `delta_R.trust`
  - `delta_R.stability`
  - `confidence`
- `meta`
  - `turn_event_id`
  - `session_id`
  - `created_at`
  - `trace_id`
  - `teacher_model`
  - `source`

当前训练时推荐的模型输入模板为：

```text
User: {user_text}
PrevRelEffective: bond={bond} care={care} trust={trust} stability={stability}
```

当前固定的 target 向量顺序为：

```text
[delta_bond, delta_care, delta_trust, delta_stability, confidence]
```

### 2.6 优先级

`P0`

---

<a id="todo-controller"></a>
## 3. 将 Controller 蒸馏或规则化

### 3.1 问题

当前 controller 是一次单独的结构化 LLM 调用：

- 调用位置：`app/api/chat.py`
- 实现位置：`app/controller/controller_client.py`

controller 的任务是生成 `Plan`，但它的输入本身已经包含：

- `behavior_effective`
- `active_boundary_keys`
- memory previews
- core self preview

说明 controller 的工作并不是完全开放生成，而是一个强结构化决策问题，长期适合蒸馏或规则化。

补充状态说明：

- 原型期用于占位的 `hard_constraints` 已决定废弃，不再作为 plan 结构的一部分维护
- 当前 plan 中真正高价值的输出主要是：
  - `behavior`
  - `selected_memories`
  - `intent`（但当前分类方式仍值得重审）

### 3.2 影响

- 主链路多出一次高成本 LLM 调用
- 增加失败面和 latency
- 产品上线后的成本不可忽视

### 3.3 相关文件

- `app/api/chat.py`
- `app/controller/controller_client.py`
- `app/controller/plan.py`
- `app/controller/prompts.py`

### 3.4 目标状态

- 常见场景下 controller 不依赖通用大模型
- 保持 `Plan` 结构兼容 Actor 输入
- controller 输出收敛成少量真正有决策价值的字段，而不是保留原型期占位字段

### 3.5 建议修改方向

- 先做 rule-based fallback 增强版，而不是只有当前的简化 fallback
- 按用户输入场景和 `behavior_effective` 构建规则 planner
- 逐步收敛 `Plan` schema，避免保留低价值占位字段
- 中期可蒸馏成小模型
- 最终保留“规则 / 小模型 / LLM fallback”三级降级链路

### 3.5A 与 belief 的当前职责边界

当前进一步确认：

- `belief` 的主要消费者应是 `controller`
- `controller` 是长期约束进入主链路决策的主要入口
- `actor` 是否直接读取 belief 暂时保留为开放问题，不在当前阶段定死

### 3.5.1 关于 `intent` 的当前问题

当前 `intent` 存在的主要问题不是“这个概念绝对错误”，而是：

- 分类粒度偏粗
  - `chat / ask_help / task / venting / other` 很难真实决定策略分叉
- 对系统决策的实际影响不够清晰
  - 当前它没有明显稳定地主导 memory use、回答结构或披露策略
- 与 `scene` / `signals` 这类上下文标签的边界不够清楚

换句话说，当前 `intent` 的问题更像是：

- 分类方式偏弱
- 使用方式偏弱

而不是简单“有没有 intent”。

### 3.5.2 `intent` 的后续路线候选

推荐保留以下三条路线，后续根据实验结果做选择：

#### 路线 A：保留 intent，但重做分类

适用前提：

- 仍然希望 controller 输出一个离散的高层模式标签

推荐方向：

- 不再使用过粗的聊天类型分类
- 改为更能决定策略分流的模式，例如：
  - `task_resolution`
  - `emotion_support`
  - `boundary_repair`
  - `relationship_checkin`
  - `light_companionship`
  - `mixed_support`

优点：

- 更贴近真实策略差异
- 便于统计分析和蒸馏

风险：

- 需要重新定义标注和评估标准

#### 路线 B：弱化 intent，改成更轻的 response mode

适用前提：

- 不需要一个太抽象的高层标签
- 更需要对回复结构做控制

推荐方向：

- 用更轻、更贴近输出形态的字段替代当前 intent，例如：
  - `direct_answer`
  - `supportive_answer`
  - `clarify_first`
  - `reflective_answer`

优点：

- 更容易直接影响 Actor 表达
- 比当前 intent 更实用

风险：

- 可能丢掉部分高层任务语义

#### 路线 C：彻底去掉 intent

适用前提：

- behavior + memory selection + boundary/policy 已足够决定生成策略

优点：

- schema 更简
- controller 更聚焦

风险：

- 失去一个潜在的离散分析维度
- 后续蒸馏时少了一个显式监督目标

### 3.5.3 推荐的 controller 收敛方向

当前最推荐的收敛方向不是继续扩张 schema，而是压缩成少量高价值输出。

推荐的 controller 最小核心输出应围绕：

- `behavior`
- `selected_memories`
- 一个经过重做的轻量模式字段
  - 可以是更好的 `intent`
  - 也可以是更轻的 `response_mode`
- `notes`

不再建议恢复或扩张：

- `hard_constraints`
- 其他纯占位性质字段

### 3.5.4 Controller 微调 / 蒸馏的设计路线

如果后续要把 controller 从通用 LLM 迁移到规则系统、小模型或蒸馏模型，建议按以下方式设计。

#### 蒸馏目标

让 controller 学会：

- 从用户输入、当前关系/行为态、边界、候选 memories 中
- 输出一个小而稳定的结构化 plan

#### 推荐的监督字段

优先监督：

- `behavior`
- `selected_memories`
- 轻量模式字段（如果最终保留）

次级监督：

- `notes` 可选，不应成为核心训练目标

不推荐作为长期训练目标：

- 原型期占位字段
- 纯 debug 字段

#### 数据来源

优先来源：

- 真实运行时的 `_last_controller` 与 turn snapshot
- 批量 probe 产物
- 人工筛选后的高质量 controller 样本

需要前置条件：

- `_last_controller` 中应保存足够完整的 plan 信息
- selected memories 应有稳定格式
- relation / behavior 状态最好能结构化导出，而不是只存在 JSON blob 中

#### 推荐实施路径

阶段 1：
- 用规则 planner 做 baseline
- 明确 schema 收敛后的目标字段

阶段 2：
- 记录一段时间线上 controller 的输入与输出
- 做人工抽样检查，筛掉低质量 plan

阶段 3：
- 训练小模型或做 few-shot distilled planner

阶段 4：
- 在线保留：
  - rule planner
  - distilled planner
  - LLM fallback

#### 替代方案

方案 1：
- 直接删掉 controller，全部交给 Actor

为什么不推荐：

- 会失去结构化控制层
- 行为调试和未来微调会更困难

方案 2：
- 长期保留通用 LLM controller

为什么不推荐作为最终方案：

- 成本和时延都偏高
- 对产品化不友好

### 3.6 优先级

`P0`

---

<a id="todo-actor-prompt"></a>
## 4. 优化 Actor Prompt，逐步将规则内化

### 4.1 问题

当前 Actor prompt 很长，规则密集，包含：

- 人格基线
- 行为变量说明
- disclosure 规则
- anti-manipulation 规则
- anti-obligation 规则

实现位置：

- `app/generation/actor_prompt.py`

这会带来：

- token 成本高
- latency 高
- 行为一致性仍依赖 prompt 质量

### 4.2 影响

- actor 调用最重，且最难直接删掉
- prompt 过长会降低稳定性和响应速度

### 4.3 相关文件

- `app/generation/actor_prompt.py`
- `app/core/llm_client.py`
- `actor_batch_probe.py`
- `test/batch_style_tests.py`

### 4.4 目标状态

- 在不丢掉核心行为约束的前提下缩短 actor prompt
- 为未来 LoRA 微调准备训练数据与验证手段

### 4.5 建议修改方向

- 先做 prompt ablation
  - 找出哪些 prompt 段真正决定输出差异
  - 删除重复、弱影响、表述重叠的规则文本
- 优先保留：
  - 关键人格基线
  - disclosure gating
  - anti-manipulation / anti-obligation 规则
  - 行为变量到写法的映射
- 继续使用 `actor_batch_probe.py` 和 `test/batch_style_tests.py` 作为回归工具
- 中期整理 actor 训练数据，推进 LoRA 微调

### 4.6 优先级

`P0`

---

## 4B. Actor 微调路线：将表达规则逐步内化到模型

### 4B.1 目标

Actor 是当前系统中最适合做微调的部分，因为它承担的是：

- 最终自然语言表达
- 行为变量到文本风格的映射
- disclosure 规则落地
- anti-manipulation / anti-obligation 约束落地

微调目标不是让模型“会聊天”这么简单，而是让它更稳定地完成下面这些事：

- 在给定行为参数时输出一致的风格差异
- 在不同关系状态下保持表达自然
- 遵守边界和 disclosure 规则
- 降低对超长 Actor prompt 的依赖
- 缩短延迟，降低 token 成本

### 4B.2 为什么优先微调 Actor，而不是先微调别的模块

#### 原因 1：Actor 是最重、最靠近用户的一层

- 主链路里 Actor 调用最难删掉
- 用户最终感知几乎都落在这一层

#### 原因 2：Actor prompt 当前承载了大量规则

这些规则非常适合逐步内化进模型权重，而不是长期留在 prompt 文本里。

#### 原因 3：Actor 微调对架构侵入相对较小

- 不需要先推翻当前 controller / policy / memory 架构
- 可以先保持输入结构不变，逐步替换输出模型

### 4B.3 推荐的微调阶段划分

推荐按 5 个阶段推进，而不是一开始就直接训练。

#### 阶段 1：定义训练目标和输入结构

先明确 Actor 到底要学什么。

推荐输入结构：

- `user_text`
- `core_self_preview` 或精简版人格基线
- `behavior`
  - 8 维行为变量
- `selected_memories_preview`
  - 少量 memory preview
- 可选：
  - 轻量模式字段（如果 controller 最终保留）

推荐输出结构：

- `assistant_reply`

暂时不建议让 Actor 训练时直接吃一整坨系统 prompt 文本，而是应逐步收敛为更结构化、更稳定的输入格式。

#### 阶段 2：批量生成候选数据

目标：

- 快速得到足够大的“可筛选候选集”

推荐来源：

##### 来源 A：现有真实运行数据

来自：

- `events`
- `turn_events`
- `_last_controller`
- `session_state`

优点：

- 更贴近真实使用
- 包含真实系统状态和行为参数

风险：

- 现有数据质量不一定稳定
- 有些历史样本可能带着 prompt 缺陷

##### 来源 B：离线 probe 批量生成

来自：

- `actor_batch_probe.py`
- `behavior_profiles.py`
- 人工整理的 prompt case 集

优点：

- 可控
- 容易做参数覆盖
- 适合刻意补齐边界场景

风险：

- 可能过于人工化
- 与真实分布有偏差

##### 来源 C：人工高质量改写集

做法：

- 对 probe 输出或真实输出做人工改写
- 保留合格样本，修正不自然/不安全/不符合风格的部分

优点：

- 质量最高

风险：

- 人工成本高

推荐策略：

- 以 A + B 生成大池子
- 用 C 做高质量核心训练集

### 4B.4 候选数据生成的具体实践步骤

#### 步骤 1：建立 case 维度覆盖表

建议覆盖以下 case 类别：

- 技术帮助
- 任务型请求
- 轻聊天
- 情绪脆弱
- 边界表达
- 边界重复确认
- 关系确认
- 离开 / 暂停
- 低 Disclosure 场景
- 高 Disclosure 场景

#### 步骤 2：建立 behavior profile 网格

不要只依赖少量手写 behavior profile。

建议覆盖：

- 低 / 中 / 高 `T_w`
- 低 / 中 / 高 `Directness`
- 低 / 中 / 高 `Q_aff`
- 低 / 中 / 高 `Disclosure_Content`

注意：

- 不需要暴力枚举全部组合
- 应优先挑“真实会出现且差异明显”的组合

#### 步骤 3：批量生成候选输出

使用：

- `actor_batch_probe.py`
- 或新增更正式的数据生成脚本

输出建议至少包含：

- case_id
- user_text
- core_self version
- behavior json
- selected_memories_preview
- raw actor reply
- 生成模型信息
- 生成时间

#### 步骤 4：写入中间数据表或统一 JSONL

建议统一用结构化中间格式，而不是只存 Excel。

推荐中间字段：

- `input`
- `raw_output`
- `edited_output`
- `quality_label`
- `safety_label`
- `use_for_training`
- `notes`

### 4B.5 数据清洗与筛选流程

这一步比“生成更多数据”更重要。

#### 必须过滤掉的样本

- 违反边界
- 过度工具化
- 明显机械化
- 披露规则错误
- 没有解义务成分的高披露样本
- 明显情绪勒索 / 操控倾向
- 和行为参数不匹配的样本

#### 推荐的自动初筛规则

可基于：

- `test/batch_style_tests.py` 中已有规则
- 新增正则 / 关键词检查
- 行为参数和文本特征的粗对齐检查

例如：

- `Disclosure_Content < 0.6` 不应出现明显自体情绪披露
- 出现自体情绪披露时应有足够的解义务成分
- 技术型 case 不应莫名带入离开/关系表达

#### 推荐的人工复核重点

人工不需要全量审，但要重点看：

- 高 disclosure 样本
- 高 Q_aff 样本
- 关系确认类样本
- 边界类样本
- 模型表现不稳定的 case

#### 推荐的数据分层

- `gold`
  - 高质量、人工确认、优先用于训练
- `silver`
  - 自动规则通过，但未人工深审
- `reject`
  - 不用于训练

### 4B.6 训练数据组织方式

推荐导出为 JSONL，每条样本至少包含：

```json
{
  "messages": [
    {"role": "system", "content": "...精简版 Actor 指令或结构化说明..."},
    {"role": "user", "content": "...结构化输入..."},
    {"role": "assistant", "content": "...目标回复..."}
  ],
  "meta": {
    "case_type": "...",
    "behavior": {...},
    "memory_count": 1,
    "quality": "gold"
  }
}
```

替代方案：

- 指令微调格式
- 纯 prompt-completion 格式

当前推荐 JSONL / chat format 的原因：

- 与现有接口思维一致
- 容易和后续模型 API 对齐
- 兼容大多数指令微调流程

### 4B.7 模型训练路线选择

#### 路线 A：LoRA / PEFT 微调

当前最推荐。

优点：

- 成本低
- 训练快
- 适合先验证“规则能不能内化”
- 不需要全量训练大模型

适用场景：

- 先做第一阶段 Actor 稳定性提升

#### 路线 B：全量监督微调

当前不优先推荐。

原因：

- 成本高
- 资源要求高
- 对你当前阶段过重

#### 路线 C：先做 DPO / 偏好优化

可作为后续阶段考虑，但不建议作为第一步。

原因：

- 你现在最缺的是“稳定的正样本分布”，不是偏好对比优化
- 先把基础表达能力训稳更重要

### 4B.8 推荐的训练实施顺序

#### 训练前置任务

1. 修通 actor dataset 导出链路
2. 明确精简版 Actor 输入格式
3. 建立数据质量标签体系
4. 准备 gold/silver 数据集

#### 第一轮训练

目标：

- 学会 behavior -> text 的基本映射
- 保持安全边界
- 降低 prompt 依赖

输入应尽量保持简洁：

- `core_self_preview`
- `behavior`
- `selected_memories_preview`
- `user_text`

不要一上来把超长原始 Actor prompt 全塞进训练输入。

#### 第一轮训练后的评测

必须做三类评测：

##### 1. 自动规则评测

- disclosure gating
- 解义务表达
- 边界遵守
- 技术场景不过度关系化

##### 2. 行为一致性评测

- 相同 case 下改行为参数，输出是否真的变化
- 高 `T_w` 是否比低 `T_w` 更温暖
- 高 `Directness` 是否更直率
- 高 `Disclosure_Content` 是否更容易自然披露

##### 3. 人工主观评测

重点看：

- 自然度
- 稳定性
- 非操控性
- 记忆使用是否自然

### 4B.9 推荐的测试与回归体系

现有可利用工具：

- `actor_batch_probe.py`
- `test/batch_style_tests.py`
- `export_actor_dataset.py`

建议新增：

- `test/actor_regression_cases.json`
  - 固定评测集
- `test/actor_eval.py`
  - 对比 base actor 与 fine-tuned actor

建议至少对比：

- base prompt-only actor
- LoRA actor + 短 prompt
- LoRA actor + 极短 prompt

目标是回答：

- 微调后能不能减少 prompt 长度
- 微调后是否更稳定
- 微调后是否出现新的安全问题

### 4B.10 预计时间

以下是较现实的粗略时间估计。

#### 阶段 1：数据生成和格式打通

- 1 到 3 天

前提：

- 当前导出脚本可用
- probe 脚本可批量运行

#### 阶段 2：规则清洗 + 人工筛样

- 3 到 7 天

视人工复核强度而定。

#### 阶段 3：第一轮 LoRA 训练

- 0.5 到 2 天

取决于：

- 使用的底模
- 显存资源
- 数据规模

#### 阶段 4：评测与二次修订

- 2 到 5 天

#### 整体第一轮闭环

- 大约 1 到 2 周

如果只做极简 MVP 验证版，最快可压到：

- 3 到 5 天

但那通常只够验证方向，不够得到稳定可用的 Actor 微调版本。

### 4B.11 已知风险和可能失败点

- 如果数据生成时行为参数覆盖不足，模型只会学到平均化风格
- 如果 gold 样本太少，模型可能学不到关键规则
- 如果 silver 样本质量太差，训练反而会污染 Actor
- 如果训练输入仍然过于依赖长 prompt，微调收益会被掩盖
- 如果没有固定评测集，训练后很难判断是“更好”还是“只是更像训练集”
- 如果 controller 输出本身不稳定，Actor 训练效果也会被拖累

### 4B.12 当前推荐的实际起步方案

如果马上开始做，推荐按下面顺序推进：

1. 先修并稳定 `export_actor_dataset.py`
2. 用 `actor_batch_probe.py` 扩充 case 与 behavior profile
3. 建立 gold / silver / reject 清洗流程
4. 做第一版 LoRA 微调
5. 用固定 regression case 对比 base 与微调版
6. 再决定是否继续压缩 Actor prompt

### 4B.13 优先级

`P1`

---

## 5. 将可异步工作移出主链路

### 5.1 问题

当前系统虽然已有 outbox 机制，但主链路中仍存在适合异步化的工作，尤其是：

- richer belief extraction
- summary memory consolidation
- 某些非必要 debug 派生信息

### 5.2 影响

- 不必要地增加主链路时延
- 同步路径过长
- 用户等待所有衍生工作完成后才能收到回复

### 5.3 相关文件

- `app/api/chat.py`
- `app/outbox/enqueue.py`
- `app/outbox/worker.py`
- `app/models/outbox_job.py`
- `app/beliefs/extract_llm.py`
- `app/memory/memories.py`

### 5.4 目标状态

- 同步路径只保留“本轮回复必须依赖”的步骤
- 衍生性、补全性、分析性任务放入 outbox 异步执行

### 5.5 建议修改方向

- 明确划分同步必要路径：
  - 用户事件写入
  - 最小 boundary enforcement
  - 最小关系状态更新
  - 最终回复生成
- 将以下任务移到异步：
  - LLM belief extractor
  - summary memory 写入
  - 更重的 debug 扩展信息
- 对异步任务补充幂等和重试策略

### 5.6 优先级

`P0`

---

## 6. 对主链路中可并行步骤做并发优化

### 6.1 问题

当前 `app/api/chat.py` 的多个步骤按顺序串行执行，但部分步骤之间不存在强依赖。

潜在可并行项包括：

- core self 读取
- belief 读取后的部分轻量预处理
- memory embedding / retrieval
- 某些不影响回复生成的 debug 写入

### 6.2 影响

- 多个轻中等耗时步骤线性叠加
- 端到端 latency 偏大

### 6.3 相关文件

- `app/api/chat.py`
- `app/core/core_self.py`
- `app/memory/memories.py`
- `app/beliefs/policy.py`

### 6.4 目标状态

- 主链路中没有依赖关系的步骤尽量并发执行

### 6.5 建议修改方向

- 审查 `chat.py` 中每个步骤的数据依赖
- 使用异步并发收集不互相依赖的结果
- 并行前先确保数据库 session 的使用方式安全
- 先从只读步骤开始并发化，不要先碰复杂写入逻辑

### 6.6 优先级

`P1`

---

## 7. 缓存稳定不变或低频变化的数据

### 7.1 问题

当前某些内容在每轮请求中重复读取，但变化频率很低，例如：

- core self
- 某些 prompt 模板
- 某些 session 的轻量 policy snapshot

### 7.2 影响

- 增加不必要的数据库访问
- 造成主链路额外开销

### 7.3 相关文件

- `app/core/core_self.py`
- `app/api/chat.py`
- `app/generation/actor_prompt.py`

### 7.4 目标状态

- 低频变化数据使用合理缓存
- 保持和数据库的一致性策略清晰

### 7.5 建议修改方向

- `core_self` 可做进程内缓存
- 如需版本更新，按 active version 或更新时间戳刷新缓存
- prompt 中固定段落可以预组装或缓存模板

### 7.6 优先级

`P1`

---

## 8. 重构 Belief 读取策略，避免简单 `limit=50`

### 8.1 问题

当前主链路使用：

- `list_active_beliefs(..., limit=50)`

这是一个工程上限，但不是成熟的 belief 检索策略。当前策略的问题：

- 没有区分 hard / soft belief
- 没有 recency 衰减
- 没有 relevance 排序
- 没有基于 strength 或 key 的优先级

### 8.2 影响

- belief 数量增长后，主链路的行为约束质量会下降
- 重要 belief 和次要 belief 混在一起处理
- 当前上限只是防爆，不是语义合理的选择

### 8.3 相关文件

- `app/api/chat.py`
- `app/beliefs/store.py`
- `app/beliefs/policy.py`
- `app/models/belief.py`

### 8.4 目标状态

- belief 检索分层处理，而不是固定读取前 N 条

### 8.5 建议修改方向

- 将 belief 分成：
  - hard constraints
  - soft preferences
  - decayed / archived beliefs
- hard constraints 应该全量生效，但数量必须受控
- soft beliefs 应该按得分排序后参与当前轮
- 评分可以综合：
  - kind
  - strength
  - recency
  - 是否最近被重复确认
  - 与当前用户输入的相关性

### 8.6 优先级

`P1`

---

## 9. 明确 `session_state.policy_json` 的边界，逐步从实验态过渡到稳定态

### 9.1 问题

当前 `policy_json` 同时承担：

- 关系态缓存
- 行为态缓存
- ack 状态
- controller debug
- latency debug
- extractor/apply debug

这种设计在早期实验阶段是合理的，但长期可能变得混杂。

### 9.2 影响

- `policy_json` 结构可能持续膨胀
- 状态字段和调试字段混在一起
- 对长期维护和迁移不够友好
- 对后续训练数据抽取、统计分析、行为分布检查不友好
- 当需要直接读取四维关系态和八维行为态作为模型输入或分析条件时，JSON 结构不够顺手

### 9.3 相关文件

- `app/models/session_state.py`
- `app/beliefs/policy.py`
- `app/api/debug.py`

### 9.4 目标状态

- 保留当前实验灵活性
- 同时为后续结构收敛预留路径
- 让关系态和行为态可以更直接地被查询、导出、分析和用于训练数据构造

### 9.5 建议修改方向

- 短期继续使用 JSON，但明确“业务状态字段”和“调试字段”的命名边界
- 中期优先把高频核心字段外提成明确结构，建议优先级如下：
  - 第一优先级：四维关系态
    - `rel_trait`
    - `rel_state_boost`
    - `rel_effective`
  - 第二优先级：八维行为态
    - `behavior_effective`
  - 第三优先级：少量高频策略字段
    - 例如 ack 相关元状态
- 对 debug blob 做裁剪，避免写入过多冗余数据
- 不要求一次性去掉 `policy_json`
  - 更现实的做法是保留一个瘦身后的 JSON，用于实验中尚未稳定的辅助字段
  - 同时把长期稳定、训练/分析高频使用的字段逐步外提

### 9.5.1 额外说明：为什么要外提关系态和行为态

- 后续若要做 relation / behavior 相关微调、蒸馏、样本筛选或分布分析，结构化字段会明显优于 JSON blob
- 常见后续需求包括：
  - 筛选 `trust_effective` 高于某阈值的样本
  - 比较 `Disclosure_Content` 在不同阶段的分布
  - 导出 `(user_text, relation_state, behavior_state, reply)` 训练样本
- 这些需求如果完全依赖 `policy_json`，可做但不利于长期维护

### 9.6 优先级

`P2`

---

## 10. 修复并收口 Outbox 异步 belief extractor 链路

### 10.1 问题

异步 belief extractor 链路已经完成第一轮代码修复，但还没有完成真实运行验证和失败场景收口。

已观察到的风险：

- `app/api/chat.py` 中的 `enqueue_job(...)` 调用方式与 `app/outbox/enqueue.py` 现有签名不一致
- worker 端期待的 job kind 和 payload 结构与主链路未完全对齐

### 10.2 影响

- belief extractor async 可能根本没有实际工作
- outbox 形同存在但不可用

### 10.3 相关文件

- `app/api/chat.py`
- `app/outbox/enqueue.py`
- `app/outbox/worker.py`
- `app/beliefs/extract_llm.py`
- `app/beliefs/apply.py`

### 10.4 目标状态

- 主链路和 worker 对 job kind / payload 结构完全一致
- 异步 extractor 任务能稳定入队、处理、回写结果

### 10.5 建议修改方向

- 统一 `kind` 命名
- 统一 payload 字段结构
- 补充最小端到端测试
- 在 debug 接口中明确暴露最近一次 outbox extractor / apply 状态

### 10.6 优先级

`P1`

### 10.7 当前状态

- 已修复主链路入队调用与 worker 的 `kind` 对齐问题
- 已补齐主链路传入的关键 payload：
  - `session_id`
  - `user_text`
  - `evidence_event_id`
  - `active_beliefs_text`
  - `policy_json`

后续仍需继续做：

- 端到端实际运行验证
- 失败场景与重试策略验证
- debug API 中对 async extractor 结果的可见性增强

---

## 10B. 收口 `beliefs/policy.py` 的职责，但避免过度拆文件

### 10B.1 问题

当前 `app/beliefs/policy.py` 同时承担：

- 默认 policy 定义
- policy schema 兜底和归一化
- session state 读写
- ack 逻辑
- tone delta 应用
- 关系态重算
- 行为态重算
- debug 字段裁剪
- slim snapshot 构建

这说明它已经是一个“状态中枢文件”，继续扩张会降低可读性和可维护性。

但另一方面，如果为了单一职责把它拆得过细，也会导致：

- 文件数量暴涨
- 跳转成本升高
- 维护时需要同时打开过多小文件

### 10B.2 影响

- 当前文件职责偏多，阅读和修改门槛上升
- 若过度拆分，又会出现“逻辑过散”的反效果

### 10B.3 相关文件

- `app/beliefs/policy.py`
- `app/models/session_state.py`
- `app/relational/projector.py`
- `app/api/debug.py`

### 10B.4 目标状态

- 保留 `policy.py` 作为“session 状态中枢”的核心入口
- 但把明显不同职责的代码做中度拆分，而不是碎片化拆分

### 10B.5 建议修改方向

- 不建议拆成很多很小的文件
- 更合理的是控制在 2 到 4 个职责清晰的文件内，例如：

#### 方案建议

- 保留 `policy.py`
  - 作为外部主入口
  - 对外暴露最常用的状态读写与更新函数
- 额外拆出一个“状态 schema / store”文件
  - 负责默认值、normalize、load/save、state 获取
- 额外拆出一个“关系更新 / 行为刷新”文件
  - 负责 `apply_tone_delta()`、effective 计算、behavior 刷新
- 如后续确实继续膨胀，再考虑把 ack/debug 相关逻辑拆出

### 10B.6 不建议的方向

- 不建议把每个小函数都拆成单独文件
- 不建议为了“单一职责”把状态逻辑切得过碎
- 不建议把对外主入口打散，否则主链路会变得更难读

### 10B.7 优先级

`P2`

---

## 11. 修复并收口 Summary Memory 链路

### 11.1 问题

summary memory 路径已经完成第一轮主链路契约修复，但还没有完成真实写入验证和异步化收口。

### 11.2 影响

- summary memory 可能没有真正写入
- 长期记忆沉淀能力不稳定

### 11.3 相关文件

- `app/api/chat.py`
- `app/memory/memories.py`

### 11.4 目标状态

- summary 写入流程参数一致
- 调用契约清晰
- 可选择同步或异步执行

### 11.5 建议修改方向

- 对齐：
  - `should_create_summary_now(...)`
  - `build_summary_for_last_n_turns(...)`
  - `write_memory_summary(...)`
- 明确返回值和参数结构
- 最终建议把 summary 写入移到异步链路

### 11.6 优先级

`P1`

### 11.7 当前状态

- 已修复主链路与 `memories.py` 之间的基础调用契约
  - 参数名已对齐
  - `build_summary_for_last_n_turns()` 的返回值已正确解包
  - `write_memory_summary()` 已按 async 方式调用

后续仍需继续做：

- 补充端到端验证
- 评估是否彻底迁移到异步路径
- 定义更可靠的 summary 触发策略与质量标准

---

## 12. 将 `actor_model` / `controller_model` 真正接入主链路

### 12.1 问题

配置层已经提供：

- `controller_model`
- `actor_model`

当前状态是：

- Actor 已接入 `actor_model -> llm_model` fallback
- Controller 继续按 `controller_model -> llm_model` 路径工作

剩余问题主要是：

- 缺少多模型配置下的真实运行验证
- tone evaluator 仍没有独立模型配置

### 12.2 影响

- 配置和实际行为不一致
- 不利于独立调试 controller / actor 模型
- 不利于后续做不同模型替换和评估

### 12.3 相关文件

- `app/core/config.py`
- `app/api/chat.py`

### 12.4 目标状态

- controller、actor、tone evaluator 各自支持独立模型配置

### 12.5 建议修改方向

- 在主链路中明确：
  - controller 优先用 `controller_model`
  - actor 优先用 `actor_model`
  - tone evaluator 优先用 `tone_model`（如果后续增加配置）
- 配置为空时再 fallback 到 `llm_model`

### 12.6 优先级

`P2`

### 12.7 当前状态

- Actor 已接入 `actor_model` 配置优先级
- controller 仍继续按 `controller_model -> llm_model` 运行

后续仍需继续做：

- 为 tone evaluator 增加独立模型配置
- 增加多模型运行日志，便于后续 A/B 对比

---

## 13. 强化批量评估与训练数据准备能力

### 13.1 问题

当前已有：

- `test/batch_style_tests.py`
- `actor_batch_probe.py`

但它们更像实验脚本，尚未形成清晰的数据生产与回归评测流程。

### 13.2 影响

- prompt 调整后难以系统性比较
- 为 LoRA / 蒸馏准备数据时缺少标准流程

### 13.3 相关文件

- `test/batch_style_tests.py`
- `actor_batch_probe.py`
- `behavior_profiles.py`
- `excel_to_actor_jsonl.py`
- `export_actor_dataset.py`

### 13.4 目标状态

- 建立一套稳定的批量探测、样本筛选、导出训练集流程

### 13.5 建议修改方向

- 明确行为 profile 设计与命名规范
- 固化测试 case 分类：
  - 技术帮助
  - 情绪脆弱
  - 边界表达
  - 离开 / 暂停
  - 关系确认
- 将 probe 输出统一成后续可直接筛选、打标、导出的格式
- 为关键规则增加自动评估指标

### 13.5.1 `tone evaluator` 训练准备的当前落点

当前已开始补齐 `tone evaluator` 训练数据链路，落点包括：

- 在 `turn_events` 中为每轮持久化：
  - teacher 输入快照
    - `user_text`
    - `active_boundary_keys`
    - `prev`
  - teacher 监督目标
    - `delta_R`
    - `confidence`
  - 基础元信息
    - `trace_id`
    - `teacher_model`
- 提供 `export_tone_dataset.py` 导出 JSONL/样本能力

当前仍待继续做：

- 跑一次迁移并验证 `tone_eval` 字段写入
- 生成第一批真实样本
- 做字段分布检查
- 再进入正式 baseline 训练前的映射收敛

### 13.5.2 批量 teacher 生成与清洗流程（已实现 v1）

当前已新增批量 teacher 生成脚本：

- `generate_tone_teacher_labels.py`

其职责是：

1. 读取基础输入样本（来自 `export_tone_dataset.py` 导出的 JSONL）
2. 调用 LLM 生成 raw teacher 标注
3. 按 `delta_R labeling policy v1` 进行程序级清洗
4. 输出：
   - `input`
   - `raw_teacher`
   - `cleaned_target`
   - `cleaning`
   - `meta`

当前 v1 清洗流程包括：

- 单维 clamp 到 `[-0.05, 0.05]`
- `L1 <= 0.10` 总量截断
- 死区归零：
  - 若某维 `|delta| < 0.015`，则该维归零
- 记录清洗痕迹：
  - 是否触发单维裁剪
  - 是否触发 `L1` 缩放
  - 哪些维度进入死区
  - 是否最终全零

### 13.6 优先级

`P1`

### 13.7 补充建议：让训练数据导出链路更可信

- `_last_controller` 中应保留完整 plan 信息，而不是只有摘要
- 导出脚本应同时兼容：
  - 完整 plan
  - 摘要字段 fallback
- 训练数据导出应显式记录：
  - `intent` 或后续替代字段
  - `behavior`
  - `selected_memories`
  - 生成时可用的关系态/行为态

否则后续蒸馏和微调会缺乏稳定监督信号

---

<a id="todo-observability"></a>
## 14. 继续完善 Debug / Observability，而不是在优化中削弱它

### 14.1 问题

在做性能优化时，容易把 debug 信息视为“可删负担”，但这个项目是多模块状态系统，缺乏可观测性会严重影响迭代质量。

### 14.2 影响

- 难以定位回复异常的具体原因
- 无法对比优化前后的实际行为变化

### 14.3 相关文件

- `app/api/debug.py`
- `app/api/chat.py`
- `app/beliefs/policy.py`

### 14.4 目标状态

- 在不破坏主链路性能的前提下，保留关键调试视图

### 14.5 建议修改方向

- 保留最小但关键的 debug 维度：
  - trace id
  - 分段耗时
  - last controller
  - last rel delta
  - behavior snapshot
- 重型 debug 信息可异步化或按需查询
- 所有优化都应能通过 debug API 观察前后差异

### 14.6 优先级

`P1`

---

<a id="todo-memory-upgrade"></a>
## 14B. 记忆系统升级方案：向更成熟的长期记忆体验推进

### 14B.1 设计目标

当前项目已经具备基础记忆能力：

- 原始事件日志：`events`
- 结构化长期约束：`beliefs`
- session 动态状态：`session_state`
- 摘要式长期记忆：`memories`

但如果目标是把记忆体验推进到更成熟、更接近高质量产品的水平，仅靠“embedding + top-k memory summary”还不够。需要补齐以下能力：

- 更清晰的记忆分层
- 更聪明的记忆写入策略
- 更丰富的召回排序
- 对“是否显式提起某段记忆”的表达控制
- 更稳定的记忆 consolidation / rewrite
- 更适合训练、评估和统计分析的结构设计

本节定义的是推荐的目标记忆架构，而不是局限于当前代码已有能力。

### 14B.2 为什么要升级

当前记忆实现的优点：

- 方向正确，已经把 `events / beliefs / session_state / memories` 分层
- 使用 embedding + pgvector 做 retrieval，工程复杂度低
- 没有把完整历史粗暴硬塞进生成上下文

当前记忆实现的主要不足：

- 写入策略仍偏粗
- retrieval 排序单一，几乎只看向量相似度
- episodic memory 和长期偏好/画像的边界仍可继续清晰化
- summary consolidation 路径还未完全收口
- 检索到记忆后，缺少“该不该提起、怎么提起”的专门控制层

### 14B.3 推荐的目标记忆分层

推荐将“记忆”理解为 5 个逻辑层，而不是只有一张 `memories` 表。

#### A. Raw Event Memory

当前对应：

- `events`

作用：

- 保存原始事实
- 为 replay、debug、summary、未来抽取提供底稿

是否保留：

- 必须保留

替代方案：

- 可以换成事件流系统或对象存储归档
- 但不建议在当前阶段替换 Postgres 事件表

为什么保留当前方案：

- 当前规模下，Postgres append-only 足够
- 与 beliefs、session_state、memory 共享事务边界，工程上最简单

#### B. Hard Memory / Constraint Memory

当前对应：

- `beliefs` 中的 boundary / high-priority preference

作用：

- 保存必须持续生效的长期约束
- 例如禁止某类追问、禁止某类话题推进、明确偏好

目标状态：

- 这类记忆不应该依赖普通 memory retrieval 才生效
- 应该被视为最高优先级长期状态

替代方案：

- 继续放在 `beliefs`
- 或拆成单独 `session_constraints` 表

为什么优先继续用 `beliefs`：

- 当前已经有基本 schema 和写入逻辑
- 比新建单独约束系统改动更小

#### C. Stable Profile Memory

当前状态：

- 项目中部分信息可能被 belief 化，但没有明确独立层

推荐新增的逻辑定义：

- 保存用户长期稳定画像信息
- 例如沟通风格偏好、长期稳定喜好、长期互动节奏

这类信息与 episodic memory 不同：

- 它不是“一次经历”
- 而是“稳定特征”

实现方案候选：

方案 1：
- 继续扩展 `beliefs`
- 用 `kind=preference/style/relationship` 承载

方案 2：
- 新建 `profile_memory` 表

建议选择：

- 先用 `beliefs` 扩展，短期不单开表

原因：

- 当前 belief 已经是结构化长期信息容器
- 过早拆新表会增加复杂度
- 等 profile 类型明确稳定后再决定是否独立拆表

#### D. Episodic Memory

当前对应：

- `memories`

作用：

- 保存“发生过的共同经历”的紧凑摘要
- 在当前 query 下按相关性召回

这是当前记忆系统最核心的 retrieval 层。

继续保留原因：

- 它和 stable profile / hard constraint 的信息类型不同
- 适合 embedding 检索

#### E. Working Memory / Recent Context Memory

当前对应：

- `session_state`
- 最近几轮 `events`

作用：

- 保存本轮生成最需要的短期状态
- 包括当前关系态、行为态、最近对话语境

目标状态：

- 不要让 working memory 和 long-term episodic memory 混在同一机制里
- 短期状态优先从 `session_state` 和最近事件窗口获取

替代方案：

- 也可以额外维护一层 recent summary buffer

建议当前阶段：

- 先继续依赖 `session_state + recent events`

### 14B.4 推荐的记忆写入策略

当前问题：

- 不是所有重要信息都被正确写入
- 也不是所有被写入的东西都值得长期保留

推荐把写入分成三条独立路径：

#### 路径 1：Constraint / Belief 写入

触发条件：

- 用户明确表达边界
- 用户明确表达稳定偏好
- 用户反复确认某个沟通风格偏好

当前落点：

- `beliefs`

要求：

- 强调规范化 key
- 支持 supersede / revoke
- 支持强弱和最近确认信息

#### 路径 2：Episodic Memory 写入

触发条件：

- 一段对话形成了“值得记住的共同经历”
- 包括情绪重要时刻、关系确认时刻、关键任务协作过程

推荐写入时机：

- 不要每轮都写
- 使用窗口化 consolidation
- 优先异步写入

推荐规则：

- 低信息量、纯噪声、短句不写
- 单纯边界表达优先 belief 化，不写 episodic memory
- 纯任务步骤如果没有长期价值，可不写
- 高情绪强度、高关系意义、高复现价值的片段优先写

#### 路径 3：Profile Memory 更新

触发条件：

- 用户表达长期稳定而非一次性的偏好或风格

推荐策略：

- 优先更新已有 profile belief，而不是反复新建
- 强调“覆盖/收敛”而不是“堆积”

### 14B.5 推荐的 episodic memory 结构

当前 `memories` 表字段较少：

- `text`
- `embedding`
- `salience`
- `from_event_id`
- `to_event_id`

推荐中期扩展字段或等价信息：

- `memory_type`
  - 例如 `episodic_summary / emotional_moment / task_history / relationship_moment`
- `importance`
  - 与当前 `salience` 类似，但定义更清晰
- `source_count`
  - 该记忆由多少事件或多少 turn 汇总而来
- `last_accessed_at`
  - 用于后续分析和检索排序
- `access_count`
  - 用于评估哪些 memory 真正在被使用
- `superseded_by`
  - 用于 consolidation 后替换旧记忆

替代方案：

- 不扩表，只把这些元数据塞进 JSON

为什么不推荐全放 JSON：

- 后续检索排序和分析会更麻烦
- 这些字段是长期稳定的 memory 元信息，适合结构化

### 14B.6 推荐的召回策略

当前召回：

- 单 session 范围内
- embedding cosine top-k

这是合理 baseline，但不够成熟。

推荐改成“混合排序”：

最终得分可综合以下因子：

- `semantic_score`
  - 向量相似度
- `recency_score`
  - 记忆越近，默认权重越高
- `importance_score`
  - 高 salience / high-importance 记忆应被优先考虑
- `type_priority_score`
  - 不同 memory type 在不同场景下优先级不同
- `access_score`
  - 被验证过有价值的记忆可以适度提高

推荐排序形式：

- 先做候选召回：vector top-k
- 再做 rerank：混合加权排序

替代方案候选：

方案 1：继续纯 cosine top-k
- 简单
- 但长期效果有限

方案 2：向量召回 + 规则重排
- 当前最推荐

方案 3：向量召回 + cross-encoder rerank
- 效果可能更好
- 但主链路变更重，不适合当前优先级

为什么推荐“向量召回 + 规则重排”：

- 性价比最高
- 与当前代码兼容
- 不引入额外大模型延迟

### 14B.7 推荐的“是否显式调用记忆”控制层

当前问题：

- 即使检索到了相关 memory，也不代表本轮就应该在回复中显式带出

成熟系统的关键不只是“检索得准”，还包括：

- 这轮该不该提
- 提哪一段
- 用什么方式提才自然

推荐新增一层逻辑：

#### Memory Use Gating

由 controller 或 controller 前置规则决定：

- 当前场景是否适合引用过去记忆
- 本轮最多注入几条
- 哪些记忆只作为隐式参考，不允许显式提起

推荐规则示例：

- 纯技术排障：
  - 默认只允许 task-related memory
- 用户脆弱表达：
  - 允许引入与安抚、被理解相关的 episodic memory
- 用户明确谈关系：
  - 允许 relationship memory
- 用户未开启相关话题：
  - 不要为了“显得记得”而生硬提起旧事

替代方案：

- 完全让 Actor 自己决定是否提记忆

为什么不推荐：

- Actor 会倾向于不稳定使用记忆
- 容易出现“明明检索到但不该提的时候乱提”

### 14B.8 推荐的 consolidation / rewrite 机制

当前问题：

- 记忆不能只是不断追加，否则会越来越碎

推荐新增机制：

- 周期性将多个低层 episodic memory 合并成更稳定的 summary
- 当新记忆能够更准确概括旧记忆时，将旧记忆标记为 superseded
- 对高重复主题做抽象提升，而不是简单堆积文本

推荐两级 consolidation：

#### Level 1：窗口摘要

当前已基本具备雏形：

- 最近 N 个 user turns -> 一条 episodic summary

#### Level 2：主题收敛

新推荐：

- 多条相似 episodic summary -> 一条更高层长期记忆

例如：

- 多次提到“用户不喜欢被追问情绪”
  - 应最终主要体现在 belief/profile 层，而不是堆很多 episodic summary

替代方案：

- 不做 rewrite，只持续追加

为什么不推荐：

- 长期 retrieval 会越来越噪
- 记忆体验会变差

### 14B.9 存储与工具方案的选择说明

#### Embedding 生成方案

候选：

- 远程 embedding API
- 本地 embedding 模型
- 独立 embedding 服务

当前推荐：

- 短期继续远程 embedding API

原因：

- 当前系统已接入
- 工程改动最小
- 适合先把写入/召回逻辑打磨成熟

何时考虑替换：

- 如果 embedding 调用成为明显成本或 latency 瓶颈
- 如果需要更高可控性或离线批量构建

#### 向量存储方案

候选：

- Postgres + pgvector
- 独立向量数据库（Pinecone / Weaviate / Milvus / Qdrant 等）
- 混合方案

当前推荐：

- 短中期继续使用 Postgres + pgvector

原因：

- 当前 memory 规模和复杂度尚未迫使拆分基础设施
- 与主业务数据同库存储，最容易保持一致性
- 工程复杂度低

何时考虑迁移：

- memory 规模明显扩大
- 召回与重排链路显著复杂化
- 需要更强检索性能或跨服务部署

### 14B.10 已知风险和可能做不到的地方

- 若没有足够好的写入判定，新增更多 memory 类型只会增加复杂度，不会提升体验
- 如果 controller 不负责 memory use gating，Actor 可能会不自然地调用记忆
- 如果 summary / consolidation 做得不好，系统会积累大量低质量 memory
- 如果没有批量评估工具，很难判断“记忆体验变好了”还是“只是更爱乱提旧事了”
- 主题收敛和记忆重写比基础向量检索更难，需要更多迭代和回归评测
- 若主链路 latency 已经过高，不应在短期引入 cross-encoder rerank 或额外重型模型

### 14B.11 推荐的实施优先级与前置依赖

下面按“先修现有能力，再提升质量，再增加复杂度”的顺序执行。

#### 阶段 1：先修通并稳定现有记忆链路

目标：

- 让现有 retrieval 和 summary 能稳定工作

优先任务：

1. 修复 `summary memory` 调用链路
2. 保证 `retrieve_memories()` 输出结构稳定
3. 为 memory retrieval 增加更明确的 debug 信息
4. 为 memory 写入和召回增加最小端到端测试

前置依赖：

- 无

相关文件：

- `app/api/chat.py`
- `app/memory/memories.py`
- `app/api/debug.py`

#### 阶段 2：先把 retrieval 做成“可用”，不要急着复杂化

目标：

- 在不引入额外大模型的前提下，让记忆召回更合理

优先任务：

5. 为 `memories` 增加更清晰的元字段
6. 在 `retrieve_memories()` 中加入基于 recency / importance / type 的规则重排
7. 给 controller 传入更明确的 memory type / score 信息，而不只是 preview 文本
8. 增加“本轮最多使用几条 memory”的 gating 规则

前置依赖：

- 阶段 1 稳定

相关文件：

- `app/models/memory.py`
- `app/memory/memories.py`
- `app/controller/controller_client.py`
- `app/controller/plan.py`

#### 阶段 3：完善写入策略，避免垃圾记忆增长

目标：

- 提升“值得记住什么”的判断质量

优先任务：

9. 明确 episodic memory 写入规则
10. 区分 task / emotional / relationship / generic episodic memory
11. 强化 belief / profile / episodic 三类写入边界
12. 把 summary memory 写入移到异步路径

前置依赖：

- 阶段 2 完成基础 retrieval metadata
- outbox 能稳定工作

相关文件：

- `app/memory/memories.py`
- `app/outbox/*`
- `app/beliefs/*`

#### 阶段 4：加入 consolidation / rewrite

目标：

- 防止记忆不断碎片化堆积

优先任务：

13. 新增低层 episodic memory 合并逻辑
14. 为 memory 增加 supersede / archive 机制
15. 建立“多个相似记忆收敛成更高层记忆”的任务流

前置依赖：

- 阶段 3 已能稳定写入不同类型记忆

相关文件：

- `app/memory/memories.py`
- `app/models/memory.py`
- `app/outbox/*`

#### 阶段 5：把记忆系统接入训练和评测体系

目标：

- 让记忆能力可以系统迭代，而不是靠主观体验

优先任务：

16. 建立 memory-related regression cases
17. 记录 memory retrieval 命中、最终使用与是否显式提起
18. 支持导出 `(user_text, selected_memories, behavior_state, reply)` 样本
19. 为未来蒸馏 controller / 微调 actor 准备记忆相关训练数据

前置依赖：

- 前 4 个阶段至少基本可用

相关文件：

- `test/batch_style_tests.py`
- `actor_batch_probe.py`
- `export_actor_dataset.py`
- `app/api/debug.py`

### 14B.12 本节的推荐结论

在当前项目阶段，推荐的总体策略是：

1. 保持 `events / beliefs / session_state / memories` 的分层方向不变
2. 短期继续使用远程 embedding + Postgres/pgvector
3. 优先把 retrieval 从“纯 cosine top-k”升级为“向量召回 + 规则重排”
4. 优先把 memory 写入策略和 consolidation 做清楚，而不是先换工具
5. 明确增加 memory use gating，避免记忆调用生硬
6. 等 retrieval / write / rewrite 稳定后，再考虑更复杂的模型化 rerank 或独立向量基础设施

### 14B.13 优先级

`P1`

---

<a id="todo-mature-architecture"></a>
## 14C. 质量提升与更成熟模型架构方向

### 14C.1 目标

在不破坏当前分层架构的前提下，吸收更成熟 LLM 产品中常见的系统方向，提高：

- 记忆调用自然度
- 控制层稳定性
- 表达层一致性
- 训练与蒸馏可行性

### 14C.2 推荐方向

#### A. 把 retrieval 和 memory use 分开

不要把“检索到什么”直接等同于“回复里显式用什么”。

推荐做法：

- retrieval 负责找候选
- rerank 负责排序
- controller / rule gating 负责决定最终是否显式调用

#### B. 把 controller 视为可蒸馏 planner，而不是永久依赖的大模型

推荐长期形态：

- rule planner
- distilled planner
- LLM fallback

#### C. 把 Actor 视为最终表达层，并逐步把规则内化到模型

推荐长期形态：

- prompt 负责剩余高层边界
- 低层表达规律尽量迁移到 LoRA / 微调权重中

#### D. 把关系态与行为态视为训练和分析的一等公民

推荐方向：

- 逐步结构化四维关系态与八维行为态
- 为后续分布分析、样本筛选、蒸馏监督提供稳定字段

#### E. 增加 feature logging，为后续蒸馏做准备

建议记录：

- slim policy snapshot
- selected memories
- controller 输出
- actor 输出
- turn-level behavior snapshot

这样未来才能做：

- controller 蒸馏
- actor 微调
- memory use 质量分析

### 14C.3 替代方向及为什么当前不选

#### 方向 1：取消 controller，全部交给 Actor

不推荐原因：

- 会显著降低可控性
- 不利于蒸馏与调试

#### 方向 2：继续长期依赖通用大模型做所有子模块

不推荐原因：

- 成本高
- 延迟高
- 产品化不友好

#### 方向 3：大规模引入独立基础设施

例如：

- 独立向量数据库
- cross-encoder rerank
- 更多在线模型链路

当前不优先原因：

- 还没把现有结构的收益榨干
- 系统复杂度会上升过快

### 14C.4 优先级

`P1`

---

## 15. 建议的优化顺序

下面是建议执行顺序，按“收益 / 风险 / 依赖”综合排序。

### 阶段 A：先收口现有实现（第一轮代码修复已完成，待运行验证）

1. outbox async belief extractor 链路
   - 已完成第一轮代码修复
   - 已完成最小真实入队、认领、执行验证
2. summary memory 链路
   - 已完成第一轮代码修复
   - 已完成最小真实 summary 生成与 `memories` 写入验证
3. `actor_model / controller_model`
   - Actor 已接通 `actor_model -> llm_model` fallback
   - Controller 继续按 `controller_model -> llm_model` 路径工作
   - 待做多模型配置下的真实运行验证
4. 最小主链路 E2E 验证
   - 已完成第一轮真实运行验证
   - 已确认：`/health/llm`、`/chat`、`/debug state/context`、boundary belief、events/turn_events、async belief extractor、summary memory 基本打通
   - 待继续验证：多模型配置路径

### 阶段 B：先压同步链路长度

4. 将 summary 和 richer belief extraction 移出同步路径
5. 缓存 core self
   - 第一轮进程内缓存已完成
   - 后续可继续视需要补充失效策略或更细粒度缓存
6. 减少重复状态读取
   - 第一轮主链路收口已完成
   - 后续仍可继续检查是否还能减少多余 `_load_policy` / 整理逻辑
7. 审查并并行化主链路中的可并行步骤

### 阶段 C：砍主链路中的 LLM 调用

8. 轻量化 tone evaluator
9. 规则化 / 蒸馏 controller

### 阶段 D：提升生成稳定性并准备训练

10. 精简 actor prompt
11. 强化 batch probe / regression / dataset 导出
12. 推进 actor LoRA 微调

### 阶段 E：中长期结构收敛

13. 重构 belief 检索策略
14. 收敛 `policy_json` 结构边界
15. 按 14B 方案升级记忆系统
16. 按 14C 方案推进更成熟的 planner / actor / 训练架构

---

## 16. 后续维护要求

当后续讨论出新的优化项时，更新本文件时应遵守：

- 新增条目必须写清楚“问题 -> 影响 -> 相关代码 -> 目标 -> 建议方向”
- 如果某项已经完成，应将其状态标记为已完成，并说明改动落在哪些文件
- 如果某项方案被推翻，应保留简短变更记录，而不是直接删除
