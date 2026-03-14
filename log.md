# Log

本文件记录当前对项目已经完成的关键修改与文档更新，作为简要变更摘要。

---

## 0. 本轮文档更新

### 0.1 `ToDo.md` 优先级收口

已在 `ToDo.md` 开头新增“优先级总览”版块，用于把当前待办按执行顺序和依赖关系重新收口，而不是仅按主题分散记录。

#### 本轮新增内容

- 新增“优先级总览”版块
  - 明确第一优先级应先做最小端到端验证
  - 明确各大任务的推荐执行顺序
  - 明确各任务之间的前置依赖关系
- 新增 `0A. 先做最小端到端验证与运行闭环确认`
  - 将“运行验证”从阶段性备注上升为显式 P0 待办
  - 补齐问题、影响、相关文件、目标、建议方向、依赖关系
- 为关键待办补充页内锚点
  - 便于从优先级总览直接跳到详细描述位置

#### 涉及文件

- `ToDo.md`

#### 当前状态

- 文档已更新
- 尚未新增自动化验证脚本或代码实现改动

### 0.2 最小 E2E 验证结果同步

已将本轮真实运行验证结果同步回文档，确认项目已从“仅静态修复”推进到“主链路最小真实运行已打通”。

#### 本轮已验证通过

- Docker 中的 Postgres/pgvector 可启动并可连接
- FastAPI 服务可启动
- `/health/llm` 已通过真实 LLM 配置打通
- `POST /chat` 已成功返回 reply
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

#### 本轮观察到的关键信息

- 当前主链路 latency 已被真实运行结果确认偏高
  - `tone_delta` 约 10s
  - `controller` 约 13s
  - `memory_retrieve` 约 1.4s
  - `total_ms` 约 25s
- 这说明当前最优先的优化方向仍然是：
  - 降低 `/chat` 延迟
  - 轻量化 tone evaluator
  - 规则化 / 蒸馏 controller

#### 本轮尚未验证通过

- boundary belief 在明确边界输入下的真实落库
- `events` / `turn_events` 的显式数据库侧核查
- async belief extractor 的真实入队、认领、执行闭环
- summary memory 的真实生成与写入
- `actor_model / controller_model` 多模型配置路径验证

#### 涉及文件

- `ToDo.md`
- `log.md`

#### 当前状态

- 文档已同步
- 下一步建议使用新的 `session_id` 做 boundary 专项验证
- 当前不建议为此先清空数据库

### 0.3 boundary 专项验证的阶段性结果

boundary 专项验证现已完成，可确认 belief extractor 的同步规则抽取链路正常。

#### 最终有效验证结果

- 使用 UTF-8 文件 + `charset=utf-8` 方式发送请求后：
  - `/sessions/demo-boundary-2/events` 中 user content 已正确记录为：`别再问我压力大不大。`
  - `/debug/sessions/demo-boundary-2/beliefs` 中已写入 boundary belief
  - belief key 为：`no_unsolicited_emotion_questions`
  - `/debug/sessions/demo-boundary-2/state?slim=1` 中 rel_delta / controller / behavior 均正常返回
  - tone evaluator 的 `scene / signals` 已体现 boundary 语义

#### 当前判断

- belief extractor 的同步规则抽取链路工作正常
- 之前的空 belief 结果来自请求输入编码污染，而不是后端抽取失败
- 当前最突出的未解决问题仍是主链路 latency 过高

#### 下一步建议

- 保留 UTF-8 文件方式作为后续中文手工验证的默认做法
- 继续做最低成本活性确认
- 然后进入低风险 latency 优化

### 0.4 最低成本活性确认已通过

本轮补充完成了三项“只确认链路活性、不做重验收”的验证，结果均通过。

#### 已通过项

- `turn_events`
  - 已确认每轮对话快照可写入
- async belief extractor
  - 已确认 outbox 入队、认领、执行闭环可运行
- summary memory
  - 已确认 summary 生成与 `memories` 写入链路可运行

#### 当前判断

- 当前项目已从“部分链路仅静态修复”推进到“主链路及关键补充链路最小真实运行已打通”
- 后续主线不应再停留在“这些能力能不能跑”的层面
- 后续更值得投入的是：
  - 低风险 latency 优化
  - `tone evaluator` 轻量化
  - `controller` 收敛

#### 涉及文件

- `ToDo.md`
- `log.md`

### 0.5 第一批低风险 latency 优化

已开始推进第一批低风险延迟优化，目标是在不改动核心行为语义的前提下，先压缩主链路中的稳定冗余读取。

#### 本轮改动

- 为 `core_self` 增加进程内 TTL 缓存
- 在 `/chat` 主链路中收口重复读取/整理：
  - `policy`
  - `boundary_keys`
  - `core_self preview`

#### 涉及文件

- `app/core/core_self.py`
- `app/api/chat.py`
- `ToDo.md`
- `log.md`

#### 当前状态

- 已完成代码改动
- 已通过 Python 编译检查
- 已完成一次最小真实 latency 复测
- 与前一轮基线相比，观测到实际下降：
  - `tone_delta` 约 `10.3s -> 8.9s`
  - `memory_retrieve` 约 `1.4s -> 1.3s`
  - `controller` 约 `13.7s -> 10.9s`
  - `total_ms` 约 `25.4s -> 21.3s`
- 当前判断：
  - 这批低风险收口改动有效
  - 但主瓶颈仍明确集中在 `tone evaluator` 与 `controller`
  - 下一步不继续深挖并行化，直接进入 `tone evaluator` 轻量化

### 0.6 `tone evaluator` 路线收敛

本轮已完成 `tone evaluator` 轻量化方向的设计收敛。

#### 已确认结论

- 不采用固定 rule-based evaluator 作为主路线
- 不优先采用蒸馏/微调小 LLM 保留 JSON 输出
- 当前主路线收敛为：小型文本模型回归
- 核心监督字段收敛为：
  - `delta_R`
  - `confidence`
- `scene / signals` 降为次级字段，后续再决定是否作为附属目标保留

#### 原因

- 固定规则和粗粒度分类可扩展性差
- 小 LLM 方案仍保留较高推理成本
- 非 LLM 多头回归对当前个人开发阶段的数据工程压力偏大

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.7 关系态定义边界收敛

本轮进一步收敛了 `core_self / belief / relation state` 三者的职责边界，并同步修正了关系态的设计解释。

#### 已确认结论

- `core_self` 与 `belief` 负责：
  - 人格底色
  - 长期边界
  - 硬约束
- `relation state` 不负责：
  - permission / acceptance / policy gating
- `relation state` 负责：
  - 描述这个 AI 与用户关系已经发展到什么状态
  - 驱动更像人与人关系发展的互动模式投影

#### 对四维关系态的当前立场

- 当前仍保留四维：
  - `bond`
  - `care`
  - `trust`
  - `stability`
- 但不再把它们解释为“用户是否授权某类行为”
- 而是解释为关系动态本身的连续状态
- 当前也不主张“人与人关系被且仅被这四维完全定义”
- 它们只是当前系统中用于驱动行为投影的最小核心连续变量

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.8 四维关系态与行为映射问题的进一步收敛

基于多轮反例压力测试，当前对关系态建模的判断进一步收敛。

#### 已确认结论

- 在当前产品边界下：
  - AI 与用户的底层关系结构固定为“助手 / 陪伴体”
  - 关系态模型负责建模这一固定结构内部的关系发展强度
  - 不负责模拟完整的人类关系结构类型
- `bond / care / trust / stability` 当前仍可作为最小核心关系态 basis
- 当前尚未发现必须新增第五维关系态的明确反例

#### 当前真正值得优先处理的问题

- 问题重点已从“关系态维度数量是否不足”转移到：
  - 关系态 -> 行为态 映射是否足够自然
- 当前特别值得怀疑的是：
  - `stability` 在行为投影中的作用偏弱
  - 它目前主要显著影响 `Disclosure_Content`
  - 但理论上还应影响主动推进节奏、情绪确认、关系记忆和互动连续性

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.9 保留疑点与训练时机判断

本轮补充记录了一个保留疑点，并明确了 `tone evaluator` 训练启动时机。

#### 保留疑点

- “独特牵引关系 / 不可替代性” 当前暂时被吸收到 `bond` 中
- 但该判断尚未被永久定死
- 后续若出现稳定反例，需要重新审视它是否应完全归入 `bond`

#### 关于 `tone evaluator` 训练时机的当前判断

- 现在就适合开始：
  - teacher 数据记录
  - 样本导出
  - 分布分析
- 最好在关系态 -> 行为态映射先收敛一版后再做：
  - 正式 baseline 训练
  - 模型替换评估

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.10 `tone evaluator` 训练准备已启动

本轮已正式开始 `tone evaluator` 的训练准备工作，目标是先建立稳定的 teacher 数据生产链路，而不是立即进入正式训练。

#### 本轮改动

- 为 `turn_events` 新增 `tone_eval` 字段
- 在 `/chat` 中把 `tone evaluator` 的 teacher 输入输出快照写入 `turn_events.tone_eval`
- 新增导出脚本：
  - `export_tone_dataset.py`
- 新增迁移：
  - `0006_add_tone_eval_to_turn_events.py`

#### 当前状态

- 已完成代码改动
- 已通过 Python 编译检查
- 尚待运行数据库迁移并做一次真实写入验证

#### 涉及文件

- `app/api/chat.py`
- `app/memory/events.py`
- `app/models/event.py`
- `export_tone_dataset.py`
- `migrations/versions/0006_add_tone_eval_to_turn_events.py`
- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.11 模块职责边界进一步收敛

本轮进一步收紧了 `tone evaluator / belief / controller / actor` 的职责边界。

#### 已确认结论

- `tone evaluator`
  - 不应依赖长期 `belief`
  - 应收敛为：
    - 读取本轮输入文本
    - 结合前一轮关系态快照
    - 估计 `delta_R`
- `belief`
  - 主要消费者应是 `controller`
- `actor`
  - 不应直接深度消费原始 `belief`
  - 是否直接读取 belief、读多少，暂列为开放问题

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.12 `tone evaluator` 样本 schema v1 收敛

本轮已将 `tone evaluator` 训练样本格式正式收敛为 v1，并同步到代码与文档。

#### 已确认结论

- 核心输入仅保留：
  - `user_text`
  - `prev_rel_effective`
- 核心监督目标固定为：
  - `delta_R.bond`
  - `delta_R.care`
  - `delta_R.trust`
  - `delta_R.stability`
  - `confidence`
- 当前固定的 target 向量顺序为：
  - `[delta_bond, delta_care, delta_trust, delta_stability, confidence]`

#### 本轮改动

- 收紧 `turn_events.tone_eval.input`
- 调整 `export_tone_dataset.py` 导出格式
- 增加 `training_input` 与 `target_vector`

#### 涉及文件

- `app/api/chat.py`
- `export_tone_dataset.py`
- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.13 `delta_R labeling policy v1` 定稿

本轮已将 `delta_R` 的 teacher 标注/生成约束正式收敛为 v1，并同步为后续批量数据生成的统一标准。

#### 已确认结论

- 每维 `delta_R` 限制在 `[-0.05, 0.05]`
- 总量限制采用：
  - `L1 <= 0.10`
- 死区规则：
  - 若某维 `|delta| < 0.015`，则该维归零
  - 若四维全部落入死区，则整轮 `delta_R = 0`
- 无明确关系信号时，默认优先输出 `delta_R = 0`
- 批量 teacher 生成脚本必须显式包含这些约束
- 生成后必须再做程序级清洗

#### 涉及文件

- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

### 0.14 批量 teacher 生成脚本已落地

本轮已实现 `tone evaluator` 的批量 teacher 生成脚本与清洗流程。

#### 本轮新增

- `generate_tone_teacher_labels.py`

#### 当前能力

- 读取基础输入样本 JSONL
- 调用 LLM 批量生成 raw teacher 输出
- 按 `delta_R labeling policy v1` 清洗为 `cleaned_target`
- 记录清洗痕迹：
  - 单维裁剪
  - `L1` 缩放
  - 死区归零
  - 是否最终全零

#### 涉及文件

- `generate_tone_teacher_labels.py`
- `ToDo.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
- `log.md`

---

## 1. 文档新增与整理

### 已新增

- `README.md`
  - 调整为更偏开源项目主页风格的简洁说明
- `PROGRAM_DESIGN_DOCUMENT.md`
  - 以中文版形式整理项目设计文档
- `ToDo.md`
  - 记录当前识别出的优化方向、架构问题、实现建议和优先级
- `log.md`
  - 记录已完成修改的简要总结

### 已补充到 `ToDo.md` 的内容

- 主链路性能优化方向
- memory 系统升级方案
- `session_state.policy_json` 的结构收敛建议
- `beliefs/policy.py` 的中度拆分建议
- controller 的收敛方向
- `intent` 的问题与可能路线
- controller 微调 / 蒸馏路线
- 更成熟的 planner / actor / 训练架构方向

---

## 2. Controller 相关修改

### 已删除 `hard_constraints`

原型期占位的 `hard_constraints` 已从代码中移除，不再作为 `Plan` 的一部分保留。

### 涉及文件

- `app/controller/plan.py`
- `app/controller/controller_client.py`
- `app/controller/prompts.py`
- `app/generation/actor_prompt.py`
- `app/api/chat.py`
- `actor_batch_probe.py`
- `export_actor_dataset.py`

### 当前状态

- `Plan` 结构已收缩为：
  - `intent`
  - `behavior`
  - `selected_memories`
  - `notes`
- Actor prompt 不再读取 `hard_constraints`
- 离线 probe 与训练导出脚本已同步清理相关字段

---

## 3. 坏链路修复

### 3.1 异步 belief extractor 链路

已修复主链路与 outbox worker 的对接问题。

#### 修改点

- `app/api/chat.py`
  - 修正 `enqueue_job(...)` 调用方式
  - 对齐 `kind="belief_extractor_llm"`
  - 补充传入：
    - `session_id`
    - `user_text`
    - `evidence_event_id`
    - `active_beliefs_text`
    - `policy_json`

#### 相关文件

- `app/api/chat.py`
- `app/outbox/enqueue.py`
- `app/outbox/worker.py`

#### 当前状态

- 代码链路已接通
- 尚未做真实运行验证

### 3.2 Summary memory 链路

已修复主链路和 `memories.py` 之间的基础调用契约。

#### 修改点

- `app/api/chat.py`
  - `should_create_summary_now(...)` 参数名改为与实现一致
  - `build_summary_for_last_n_turns(...)` 的 tuple 返回值正确解包
  - `write_memory_summary(...)` 改为正确 `await`

#### 相关文件

- `app/api/chat.py`
- `app/memory/memories.py`

#### 当前状态

- 代码调用已对齐
- 尚未做端到端验证

### 3.3 训练数据导出链路

已修复 `export_actor_dataset.py` 对 controller 数据结构的错误假设。

#### 修改点

- `_last_controller` 现在会保存完整 `plan`
- `export_actor_dataset.py` 改为兼容：
  - `controller["plan"]`
  - 摘要字段 fallback
- 事件配对角色从 `"ai"` 修正为 `"assistant"`

#### 相关文件

- `app/api/chat.py`
- `export_actor_dataset.py`

#### 当前状态

- 导出链路的静态结构问题已修复
- 尚未做实际导出验证

### 3.4 Actor 模型配置接线

已让 Actor 优先使用 `actor_model` 配置。

#### 修改点

- `app/api/chat.py`
  - `LLMClient` 改为：
    - `actor_model -> llm_model` fallback

#### 当前状态

- 配置接线已正确

---

## 4. Memory 模块清理

### 已处理

- 去掉 `app/memory/memories.py` 中的临时 `print(...)` 调试输出

### 相关文件

- `app/memory/memories.py`

---

## 5. 当前已完成的验证

已执行：

- 对以下文件进行 Python 编译检查，结果通过
  - `app/controller/plan.py`
  - `app/controller/controller_client.py`
  - `app/controller/prompts.py`
  - `app/generation/actor_prompt.py`
  - `app/api/chat.py`
  - `actor_batch_probe.py`
  - `export_actor_dataset.py`
  - `app/memory/memories.py`
- 最小真实运行验证已通过：
  - Docker DB 启动
  - FastAPI 启动
  - `/health/llm`
  - `/chat`
  - `/debug/sessions/{session_id}/state?slim=1`
  - `/debug/sessions/{session_id}/context?slim=1`
  - boundary belief 专项验证
  - `events` / `turn_events` 显式核查
  - async belief extractor 最小闭环验证
  - summary memory 最小写入验证

未执行：

- actor dataset 实际导出验证
- `actor_model / controller_model` 多模型配置验证

---

## 6. 当前整体状态总结

截至目前，已经完成的工作主要是两类：

### A. 文档化与架构梳理

- 梳理了主链路和四个关键支撑模块
- 把架构优化方向沉淀进 `ToDo.md`
- 把项目设计文档整理为可长期维护版本

### B. 关键坏链路修复与原型字段清理

- 删掉了已经弃用的 `hard_constraints`
- 修通了几条静态上明显有问题的链路
- 为后续做性能优化、controller 收敛、memory 升级和训练数据整理打了基础

---

## 7. 后续建议

当前最值得继续推进的方向：

1. 进入 `tone evaluator` 轻量化
2. 继续按 `ToDo.md` 推进：
   - 降延迟
   - 提升记忆质量
   - 收敛 controller
   - 为微调 / 蒸馏准备数据

---

## 8. 文档同步状态

本轮已额外同步更新：

- `ToDo.md`
  - 将“阶段 A”改为更准确的状态描述
  - 明确标记为“第一轮代码修复已完成，待运行验证”
- `PROGRAM_DESIGN_DOCUMENT.md`
  - 移除已废弃的 `hard_constraints` 现状描述
  - 更新 summary memory、outbox belief extractor、`actor_model` 接线的当前实现状态

当前建议将以下三份文档一起作为后续新对话的上下文摘要：

- `ToDo.md`
- `log.md`
- `PROGRAM_DESIGN_DOCUMENT.md`
