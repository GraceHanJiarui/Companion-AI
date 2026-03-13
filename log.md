# Log

本文件记录当前对项目已经完成的关键修改与文档更新，作为简要变更摘要。

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

未执行：

- 实际 API 端到端运行验证
- outbox 异步任务真实入队/执行验证
- summary memory 真实写入验证
- actor dataset 实际导出验证

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

1. 跑最小端到端验证
2. 继续梳理 `debug.py` 和 `outbox` 的运行闭环
3. 继续按 `ToDo.md` 推进：
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
