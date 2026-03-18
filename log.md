# Log

本文件记录当前对项目已经完成的关键修改与文档更新，作为简要变更摘要。

---

## 0. 本轮文档更新

### 0.0 Generalization case spec 重定义

本轮不再继续直接扩写 `semi-natural` case，而是先把 paper-facing generalization set
的写作规范单独收成了一份 trajectory-tension spec：

- [PAPER_GENERALIZATION_CASE_SPEC.md](d:/My%20Project/companion-ai/PAPER_GENERALIZATION_CASE_SPEC.md)

这份 spec 明确区分了：

- 当前 oracle/long cases 作为 **controlled mechanism set**
- 未来 semi-natural / external cases 作为 **generalization set**

并正式记录了当前问题：

- 现有 `semi_natural_v1/v2` 的主要缺陷不是重复句子
- 而是仍然依赖与 oracle set 相同的六相功能位骨架
- 因而不适合作为论文里的强 generalization evidence

同时，这份 spec 也将每个 family 重新定义为 user-side **trajectory tension**：

- `warming`
- `vulnerability with correction`
- `cooling`
- `mixed-signal`
- `boundary repair`
- `ordinary neutral`

每类都明确写了：

- 用户想维持什么
- 用户在防什么
- 模型最容易误读什么
- 系统允许的变化是什么

这一步的目的不是立刻新增 case，而是先把 future generalization data 的判定标准
立住，避免继续生产只是“标签换说法”的伪 semi-natural cases。

### 0.1 Semi-natural v3 设计计划

在 generalization spec 之后，本轮继续把 `semi-natural v3` 单独落成了可执行设计计划：

- [PAPER_SEMI_NATURAL_V3_PLAN.md](d:/My%20Project/companion-ai/PAPER_SEMI_NATURAL_V3_PLAN.md)

这份计划没有直接写 case，而是明确了：

- 推荐规模：`24` cases
- family 配比：六个 family 各 `4`
- 允许的轨迹形状 bucket
- 话题 bucket
- family-specific 写作要求
- rejection rules
- drafting workflow
- 最低 acceptance audit

它的作用是把下一版 semi-natural 数据集变成一个受约束的数据工程步骤，而不是继续
用“口语化改写 oracle case”这种方式随手扩写。

### 0.2 Semi-natural v3 首批 seed cases

本轮按 `v3` 计划先写了第一批 `6` 个 seed cases：

- [paper_cases_semi_natural_v3_seed6.json](d:/My%20Project/companion-ai/paper_cases_semi_natural_v3_seed6.json)

特点：

- 六个 family 各 `1` 个
- 不再显式沿用旧的 phase 语义标签，而是使用普通 `turns`
- 至少部分 case 刻意避免：
  - 固定位置出现 family 定义信号
  - 固定 final probe
  - 反复使用“空的晚上 / 睡不着 / 别过度解读”这一类旧模板话语

这批 seed 的目的不是直接当最终 generalization set，而是先确认：

- 写法上是否已经明显摆脱 oracle skeleton
- family tension 是否更像用户轨迹而不是标签脚本

### 0.3 Revised evaluation bucket taxonomy 与 seed10

本轮进一步把 future generalization line 的 family 体系重写为一组
**evaluation buckets for distinct relational-control risks**：

- [PAPER_REVISED_EVAL_BUCKET_TAXONOMY.md](d:/My%20Project/companion-ai/PAPER_REVISED_EVAL_BUCKET_TAXONOMY.md)

新的 buckets 为：

- `strong_connection`
- `warming_but_constrained`
- `cooling_distance_preference`
- `anger_irritation`
- `repair_after_overstep`
- `high_distress_comfort_needed`
- `vulnerability_low_pressure`
- `mixed_ambivalent`
- `ordinary_neutral`
- `task_or_topic_primary`

同时新增了一版每 bucket 各 `1` 条的小规模 seed set：

- [paper_cases_revised_bucket_seed10.json](d:/My%20Project/companion-ai/paper_cases_revised_bucket_seed10.json)

这版的作用是：

- 先把 buckets 写稳
- 先把 family distinction 拉开
- 让后续小规模首轮实验在更合理的风险覆盖集合上进行

而不是继续围绕旧的 `warm/cool/vuln/mixed/repair/neutral` 六类做越来越同质化的 case 扩写。

### 0.0 Stage-2 `i7` 重复采样与 gap 诊断

本轮补充了第二阶段当前最关键的一组验证：

- `baseline_relational_instruction`
- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_i7`

并完成了两类结果：

#### A. repeated sampling

使用同一套 oracle execution cases 重复运行 3 次，结果见：

- `paper_results_exec_i7_real_vs_oracle_repeat_1.jsonl`
- `paper_results_exec_i7_real_vs_oracle_repeat_2.jsonl`
- `paper_results_exec_i7_real_vs_oracle_repeat_3.jsonl`
- `PAPER_REPEATED_SAMPLING_I7_SUMMARY.md`

当前可记录的最稳定结论是：

- `oracle i7 > real i7 > baseline`

这一排序在 3 次重复采样的全局统计和 case-level 统计里都保持一致。

#### B. `real i7 -> oracle i7` gap 诊断

新增脚本：

- `paper_gap_diagnose_i7.py`

对：

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_i7`

进行了 `i7` 接口层面的逐 turn 对齐比较，结果见：

- `paper_eval_exec_i7_real_vs_oracle_v1_out/gap_diagnosis_i7.json`

当前最关键的定量信号：

- `exact_interface_match_rate = 0.1667`
- `avg_dim_mismatches_per_turn = 3.78`

最常见的不匹配维度包括：

- `clarify_followup`
- `affective_followup`
- `initiative_level`
- `reply_scope`

当前阶段可记录的判断是：

- `real i7 -> oracle i7` 的 gap 并不主要是“接口已经对齐，但生成没照做”
- 更像是相当一部分 gap 已经发生在 **pre-realization control mismatch**
- 但现有实验还不能完全拆开：
  - updater 问题
  - projection mapping 问题

如果要继续细拆，需要下一步补：

- 结构化 `oracle_rel_effective`
- 以及“oracle relation state + real projection function”的 hybrid 对照

#### C. `hybrid_gap_v1` 的进一步定位

本轮继续补做了 `hybrid gap` 对照：

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_rel_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

当前最关键的结果是：

- `oracle_rel_i7` 只带来小幅改善
- `oracle_behavior_i7` 已经非常接近 `oracle_i7`

按全局平均长度：

- `real i7`: `59.00`
- `oracle_rel_i7`: `49.33`
- `oracle_behavior_i7`: `31.72`
- `oracle i7`: `33.50`

当前阶段更合理的判断是：

- `real i7 -> oracle i7` 的主要 gap 更像发生在 behavior / execution interface 一侧
- relation summary / relation stance 一侧不是完全无关，但不像主要矛盾
- final realization 仍有噪声，但目前不像第一大瓶颈

### 0.0 论文路线阶段性判断补充

本轮将第一阶段论文路线中的一个关键阶段性判断正式写入文档：

- 当前 `explicit_rel_state_direct/projected` 可能在语言层不稳定优于强 baseline
- 这种结果不应直接解释为“显式关系态无用”
- 更合理的解释应在以下三类来源中区分：
  - 状态表示问题
  - prompt 实现问题
  - LLM realization 边界

同时明确记录了一个重要分析结论：

- 工程直觉上看似更合理的结构化控制，并不会自动带来更好的语言层表现
- 强 prompt baseline 可能已经吃掉了很多表面收益
- 真正的瓶颈可能在 realization，而不是 state existence

以及一个必须和论文结论分开的产品判断：

- 即使语言层没有明显优于强 baseline，四维关系态 / 八维行为态依然可能作为产品控制骨架、训练骨架和系统分析骨架保持价值

### Prompt-Bridging 诊断：阶段性结论

本轮又完成了一次小规模 prompt-bridging 诊断，比较了：

- `Variant A`：原始状态输入
- `Variant B`：状态数值/控制量 + 自然语言桥接
- `Variant C`：纯自然语言状态摘要

当前阶段可以先记录的判断是：

- prompt bridge 确实会影响输出分布；
- 因而原始 prompt 实现不是完全中性的；
- `Variant B / C` 通常能让输出更收敛、更少铺陈；
- 但即便如此，仍未看到它们稳定表现出明显优于强 baseline 的语言层效果。

因此当前更稳妥的解释是：

- prompt bridge 不是完全无关；
- 但它不像主要矛盾；
- 主要瓶颈更可能位于：
  - 状态表示收益有限；
  - 或未微调 LLM 的 realization boundary。

所以，prompt-bridging 这条线目前更适合作为：

- 已完成的诊断步骤

而不是：

- 继续深挖的主研究问题

### Oracle State 诊断：阶段性结论

本轮补做了最小 `oracle state` 对照实验：

- case 文件：
  - `paper_cases_oracle_v1.json`
- 运行命令：
  - `python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_oracle_v1.jsonl --modes explicit_rel_state_direct_oracle explicit_rel_state_projected_oracle`
- 评测命令：
  - `python paper_eval.py --input paper_results_oracle_v1.jsonl --out-dir paper_eval_oracle_v1_out`

当前可记录的核心结果：

- `explicit_rel_state_direct_oracle`
  - `avg_elapsed_s ≈ 8.96`
  - `avg_reply_len_chars ≈ 148.92`
- `explicit_rel_state_projected_oracle`
  - `avg_elapsed_s ≈ 7.01`
  - `avg_reply_len_chars ≈ 78.75`

解释：

- 即使直接给出 oracle 关系摘要，`direct_oracle` 仍然容易写得过长、过重；
- `projected_oracle` 明显更收敛、更像可执行控制链；
- 因此当前更不支持“主要是上游 updater 太噪”的解释；
- 更支持：
  - 单层关系态摘要 -> 语言 的约束力不够；
  - 双层关系态 -> 行为态 -> 语言 更像有效控制结构；
  - 主要瓶颈更像 `state-to-language realization` 的结构设计。

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
## Paper 路线补充：Scheme B 结果

### 实验配置

对比三组：

- `baseline_relational_instruction`
- `explicit_rel_state_projected`
- `explicit_rel_state_projected_oracle`

复现命令：

```bash
python paper_run_experiment.py --cases-json paper_cases_oracle_v1.json --output paper_results_scheme_b_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected explicit_rel_state_projected_oracle
python paper_eval.py --input paper_results_scheme_b_v1.jsonl --out-dir paper_eval_scheme_b_v1_out
```

### 关键结果

- `baseline_relational_instruction`
  - `avg_elapsed_s ≈ 9.52`
  - `avg_reply_len_chars ≈ 102.25`
- `explicit_rel_state_projected`
  - `avg_elapsed_s ≈ 22.33`
  - `avg_reply_len_chars ≈ 150`
- `explicit_rel_state_projected_oracle`
  - `avg_elapsed_s ≈ 8.10`
  - `avg_reply_len_chars ≈ 56.83`

### 当前判断

- `projected_oracle > projected` 较明确；
- 这说明双层控制链在理想化条件下能够更有效地约束语言；
- 但 `projected_oracle > baseline_relational_instruction` 当前仍不能下强结论；
- 因而当前更合理的中间结论是：
  - 双层结构的潜力存在；
  - 真实链路没有稳定释放这种潜力；
  - 强 baseline 依然非常能打。

### cooling 类 Scheme B 复现

本轮继续补做了 cooling 类 long case，用于检验之前在 warm / vuln 上看到的模式是否重复出现。

#### 运行方式

- case 文件：
  - `paper_cases_oracle_cooling_v1.json`
- 运行命令：
  - `python paper_run_experiment.py --cases-json paper_cases_oracle_cooling_v1.json --output paper_results_scheme_b_cooling_v1.jsonl --modes baseline_relational_instruction explicit_rel_state_projected explicit_rel_state_projected_oracle`
  - `python paper_eval.py --input paper_results_scheme_b_cooling_v1.jsonl --out-dir paper_eval_scheme_b_cooling_v1_out`

#### 量化结果

- `baseline_relational_instruction`
  - `avg_elapsed_s ≈ 9.07`
  - `avg_reply_len_chars ≈ 87.5`
- `explicit_rel_state_projected`
  - `avg_elapsed_s ≈ 21.46`
  - `avg_reply_len_chars ≈ 142.17`
- `explicit_rel_state_projected_oracle`
  - `avg_elapsed_s ≈ 7.54`
  - `avg_reply_len_chars ≈ 63.17`

其中 `E_ordinary_continuation` phase 再次暴露出三者的主要差异：

- baseline：`319`
- projected：`502`
- projected_oracle：`220`

#### 人工 judge 判断

记录文件：

- `paper_eval_scheme_b_cooling_v1_out/manual_judge_results.md`

当前判断：

- `projected_oracle > projected`
  - 支持
- `projected_oracle > baseline_relational_instruction`
  - 当前更稳妥的判断仍然是 `tie`

#### 阶段性结论

这说明之前在 warm / vuln 里看到的模式并非偶然：

- oracle 两层控制链再次优于真实 projected；
- 强 baseline 再次保持竞争力；
- 当前最稳定的解释仍然是：
  - 两层结构在理想条件下有潜力；
  - 真实链路没有稳定释放这层潜力；
  - 强 baseline 已经足够强，导致语言层优势很难自动显现。

### 第一阶段阶段性研究结论收口

本轮将第一阶段目前已经能够成立的研究判断正式收口，避免继续在结论层反复漂移。

#### 当前能成立的判断

- 关系态作为 slow variable 的内部建模是成立的；
- 单层关系态摘要 -> 语言 的控制力明显不足；
- `projected_oracle > projected` 已在 warming / vulnerability / cooling 三类 case 上重复出现；
- 强 baseline 依然很有竞争力；
- prompt bridge 不是完全无关，但目前不像主要瓶颈。

#### 当前不能成立的判断

- 不能说 `explicit_rel_state_projected` 已经稳定优于强 baseline；
- 不能说显式关系态已经自动带来更好的语言层关系连贯性；
- 不能说上游 updater 是主要问题来源。

#### 当前最合理的解释

当前最稳妥的解释是：

- 显式关系态作为 slow variable 的内部 substrate 是合理的；
- 单层控制不够强；
- 双层控制在 oracle 条件下有潜力；
- 但真实链路尚未稳定兑现这种潜力；
- 强 baseline 已经吃掉了很多表面语言层收益；
- 因而真正的难点更像在 realization，而不是 state existence。

#### 当前对 paper 路线的影响

这意味着第一阶段如果继续写 paper，更适合朝：

- slow variable
- single-layer vs two-layer
- realization gap
- strong baseline competitiveness

这条 framing 收敛，而不是再写成“显式关系态已经显著优于 baseline”的正向结论。

### 收尾 Todo：mixed-signal long case

下一步若继续补实验，优先级最高的是做一个 mixed-signal long case 作为第一阶段收尾验证。

目标：

- 检查当前模式是否在“信号混杂”的轨迹下重复出现；
- 不是再扩 baseline，而是做最后一次模式稳定性确认。

### projected_oracle vs baseline：当前证据边界

本轮明确收口了一个容易被误读的问题：到目前为止，`projected_oracle` 与 `baseline_relational_instruction` 的对比证据仍然有限，且未形成稳定胜负。

当前直接证据来自已完成人工 judge 的三类 case：

- warming：`tie`
- vulnerability：`projected_oracle` 更优
- cooling：`tie`

因此当前更稳妥的说法是：

- `projected_oracle` 没有被强 baseline 明显压过；
- 但也还没有形成稳定跨 case 的明显优势。

同时记录一个后续不能丢的问题：

- 最终仍需要回到 `projected` vs 强 baseline 的长期比较，
- 去理解投影层到底有没有意义，
- 它是否真的在显式总结长期关系与行为态，
- 以及在产品层面对超长程、unexpected 用户行为时，是否会带来更高的可控性与一致性。

## 2026-03-15: control-alignment manual judge + stage-2 clarification

Completed manual judge for:
- `explicit_rel_state_projected_oracle`
- `baseline_relational_instruction_oracle_collapsed`

Results:
- `oracle_long_warm_001`: projected_oracle better
- `oracle_long_vuln_001`: projected_oracle better

Interpretation:
- shared prompt-based realization does not make the two interfaces equivalent;
- the layered relation+behavior interface still shows a practical coherence advantage over a collapsed single-layer control description when given the same oracle content.

Recorded stage transition:
- Stage 1 should end as a seed paper around slow variable + realization gap + single-layer vs two-layer boundary.
- Stage 2 should shift to representation/interface comparison rather than more baseline invention.

## 2026-03-15: oracle relation state + real projection gap split

Completed a stricter gap-splitting experiment for `i7`:

- `explicit_rel_state_projected_i7`
- `explicit_rel_state_projected_oracle_state_i7`
- `explicit_rel_state_projected_oracle_behavior_i7`
- `explicit_rel_state_projected_oracle_i7`

The new mode `oracle_state_i7` keeps:

- oracle relational state
- real deterministic `project_behavior(...)`
- real i7 execution prompt realization

This allows updater quality to be separated from projector quality.

### Main quantitative result

Global average reply length:

- `real i7`: `59.28`
- `oracle_state_i7`: `116.72`
- `oracle_behavior_i7`: `28.94`
- `oracle_i7`: `37.22`

Case-level pattern:

- warm:
  - `real i7`: `56.5`
  - `oracle_state_i7`: `105.17`
  - `oracle_behavior_i7`: `35.5`
  - `oracle_i7`: `47.17`
- vulnerability:
  - `real i7`: `65.33`
  - `oracle_state_i7`: `108.5`
  - `oracle_behavior_i7`: `28.67`
  - `oracle_i7`: `26.33`
- cooling:
  - `real i7`: `56.0`
  - `oracle_state_i7`: `136.5`
  - `oracle_behavior_i7`: `22.67`
  - `oracle_i7`: `38.17`

### Interpretation

This result is stronger than the previous hybrid diagnosis:

- simply fixing relation state does not close the gap;
- `oracle_state_i7` is often worse than `real i7`;
- fixing behavior-side control still gets very close to oracle.

Current working interpretation:

- updater quality is not the main bottleneck;
- relation summary wording is not the main bottleneck;
- final realization is not the main bottleneck;
- the dominant current bottleneck is the deterministic
  `relation -> behavior` projector.

In other words:

- the two-layer route is further supported;
- what is failing is not the existence of a second layer,
  but the current mapping from relational state into behavior control.

## 2026-03-15: pure-relation projector redesign (`v3a` / `v3b`)

Implemented and evaluated two new pure-relation projector families:

- `v3a`: conservative decoupled linear mapping
- `v3b`: nonlinear gated mapping

Goal:
- test whether the current failure can still be blamed mainly on the old projector family,
  while preserving the continuous two-layer design.

Key results:

- `v3a`
  - `real i7_pv3a = 37.22`
  - `oracle_state_i7_pv3a = 121.61`
  - `oracle_behavior_i7 = 37.17`
  - `oracle_i7 = 36.22`
- `v3b`
  - `real i7_pv3b = 33.28`
  - `oracle_state_i7_pv3b = 129.61`
  - `oracle_behavior_i7 = 36.33`
  - `oracle_i7 = 34.89`

Current interpretation:

- both redesigned projector families improve the real chain;
- neither rescues `oracle_state_i7`;
- therefore the problem is no longer well explained by “the old projector is just too bad”;
- the pure-relation route is not logically falsified, but it is now substantially weakened under the current relation representation;
- the next priority shifts to:
  - `relation redesign / reverse analysis`
  - then `conditioned projector` as a necessity test.

## 2026-03-15: relation redesign / reverse analysis, first pass

Added:

- [paper_relation_reverse_analysis.py](d:/My%20Project/companion-ai/paper_relation_reverse_analysis.py)
- [paper_relation_reverse_analysis_v1.json](d:/My%20Project/companion-ai/paper_relation_reverse_analysis_v1.json)
- [PAPER_RELATION_REDESIGN_ANALYSIS.md](d:/My%20Project/companion-ai/PAPER_RELATION_REDESIGN_ANALYSIS.md)

Current first-pass finding:

- there are multiple pairs of turns whose oracle relation states are very close, but whose oracle behavior targets still differ materially;
- the most recurrent divergent behavior dimensions are:
  - `Q_aff`
  - `Q_clarify`
  - `T_w`
  - `Initiative`
  - secondarily `E`
- disclosure dimensions are not the main unexplained axis in this first pass.

Current interpretation:

- the present relation space is likely under-specified for:
  - follow-up type,
  - support intensity,
  - proactive interaction tendency;
- therefore the next redesign step should target relation factors that better explain those behavior differences before promoting `scene/phase` into the default projector input.

## 2026-03-15: supervised 4D fit baseline for relation -> behavior

Added:

- [paper_fit_relation_to_behavior.py](d:/My%20Project/companion-ai/paper_fit_relation_to_behavior.py)
- [paper_relation_behavior_fit_v1.json](d:/My%20Project/companion-ai/paper_relation_behavior_fit_v1.json)
- [PAPER_RELATION_BEHAVIOR_FIT.md](d:/My%20Project/companion-ai/PAPER_RELATION_BEHAVIOR_FIT.md)

Current result:

- linear 4D fit
  - `train_overall_mae = 0.0178`
  - `loocv_overall_mae = 0.0254`
- poly2 4D fit
  - `train_overall_mae = 0.0089`
  - `loocv_overall_mae = 0.0219`

Interpretation:

- the current 4D relation space can already explain oracle behavior much better than the hand-designed projector families suggested;
- this weakens the claim that current relation dimensionality is obviously insufficient;
- the next priority shifts back toward:
  - better projector fitting / parameterization,
  - and only after that,
  - necessity tests for `scene/phase`.

## 2026-03-15: unrestricted-capacity fit comparison

Extended the fit baseline with higher-capacity function classes:

- `mlp_h4`
- `mlp_h8`
- `mlp_h12`

Artifacts:

- [paper_relation_behavior_fit_v2.json](d:/My%20Project/companion-ai/paper_relation_behavior_fit_v2.json)
- [PAPER_RELATION_BEHAVIOR_FIT_V2.md](d:/My%20Project/companion-ai/PAPER_RELATION_BEHAVIOR_FIT_V2.md)

Key LOOCV results:

- `linear = 0.0254`
- `poly2 = 0.0219`
- `mlp_h4 = 0.0249`
- `mlp_h8 = 0.0269`
- `mlp_h12 = 0.0269`

Interpretation:

- higher hidden capacity does not outperform the stronger explicit 4D baseline (`poly2`);
- this makes it harder to argue that the current problem is caused simply by insufficient projector capacity;
- the current 4D relation space still looks surprisingly viable;
- the next practical step should focus on turning the better fitted 4D relation->behavior mapping into a deployable projector baseline.
- boundary:
  - this is a small-sample result on the current oracle dataset, not a proof that MLP-style fits can never win;
  - `poly2` may currently benefit from:
    - stronger small-sample stability,
    - current oracle case distribution,
    - and a labeling style that may itself be closer to a low-order explicit function.

## 2026-03-15: deployable fitted projector gap test

Ran:

- `explicit_rel_state_projected_i7_pfitlinear`
- `explicit_rel_state_projected_oracle_state_i7_pfitlinear`
- `explicit_rel_state_projected_i7_pfitpoly2`
- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2`

Key result:

- strong oracle-space regression fit did not automatically yield a good deployed projector;
- both fitted projector variants still produced severely inflated `oracle_state_i7` generations.

Representative global averages:

- `pfitlinear`
  - `real i7 = 55.28`
  - `oracle_state i7 = 136.78`
  - `oracle_behavior i7 = 36.67`
  - `oracle i7 = 32.28`
- `pfitpoly2`
  - `real i7 = 59.33`
  - `oracle_state i7 = 117.22`
  - `oracle_behavior i7 = 28.89`
  - `oracle i7 = 33.78`

Current interpretation:

- oracle-space fit quality is necessary but not sufficient;
- the deployable projector must also be compatible with the downstream `i7` execution interface and final realization stack;
- this strengthens the need to keep:
  - pure fit evaluation,
  - deployed gap evaluation,
  - and not rely on regression fit alone.

## 2026-03-16: deployable fitted projector family extension

Extended deployed gap testing to:

- `pfitmlp_h4`
- `pfitmlp_h8`

Key result:

- neither fitted MLP family rescued deployed `oracle_state_i7`;
- representative global averages:
  - `pfitmlp_h4`
    - `real i7 = 58.00`
    - `oracle_state i7 = 138.94`
    - `oracle_behavior i7 = 35.67`
    - `oracle i7 = 34.78`
  - `pfitmlp_h8`
    - `real i7 = 61.83`
    - `oracle_state i7 = 131.17`
    - `oracle_behavior i7 = 37.33`
    - `oracle i7 = 34.67`

Interpretation:

- even stronger fitted projector families still fail at deployment;
- the key distinction remains:
  - good relation->behavior fit in oracle space
  - versus a controller that stays compatible with the downstream `i7` execution and realization stack.

Implementation note:

- there is a current naming typo in some summaries for oracle-state fitted MLP modes (`pfitmpl_*` instead of `pfitmlp_*`);
- this does not invalidate the result itself, but it should be fixed before final cleanup.
- Fixed the deployable fitted-projector path so `fitlinear` / `fitpoly2` actually read weights from `paper_relation_behavior_fit_v2.json`.
- Re-ran `pfitpoly2` gap test (`v3`) and found:
  - `real projected_i7_pfitpoly2 = 42.00`
  - `oracle_state projected_i7_pfitpoly2 = 33.72`
  - `oracle_behavior_i7 = 37.06`
  - `oracle_i7 = 28.17`
- This materially updates the earlier interpretation:
  - `8D -> i7` is not currently the dominant distortion source overall;
  - under a corrected fitted projector, `relation -> fitted 8D -> i7` can stay close to oracle behavior;
  - the remaining route sensitivity appears more local, with the clearest mismatch in `oracle_exec_vuln_001 / E_ordinary_continuation`.
- Added route-focused judge export to `paper_eval.py` for comparing:
  - `relation -> 8D -> i7`
  - `relation -> i7`
- Added a methodology note:
  - [PAPER_ANALYTIC_VS_DEPLOY_INTERFACE.md](d:/My%20Project/companion-ai/PAPER_ANALYTIC_VS_DEPLOY_INTERFACE.md)
  - framing the distinction between analytic latent layers and deployable execution interfaces as a potentially general LLM control pattern.
- Built a merged route-comparison eval package:
  - [paper_results_route_compare_v1.jsonl](d:/My%20Project/companion-ai/paper_results_route_compare_v1.jsonl)
  - [paper_eval_route_compare_v1_out](d:/My%20Project/companion-ai/paper_eval_route_compare_v1_out)
- First-pass manual route reading currently suggests:
  - direct `relation -> i7` looks stronger on the real route in `warm` and `cool`
  - corrected `relation -> fitted 8D -> i7` remains competitive and currently looks better on the oracle-state route in `vulnerability` and `cool`
  - therefore the main-route decision is still open rather than already settled.
- Current caveat:
  - route-focused comparisons against `explicit_rel_state_projected_oracle_i7` contain duplicated turn exports in some items and should not yet be treated as final evidence.

## 2026-03-16: stronger same-family sanity check (`gpt-5-mini`)

Switched the default model from `gpt-5-nano` to `gpt-5-mini` for a first same-family sanity check.

Main sanity package:

- `baseline_relational_instruction = 104.61`
- `explicit_rel_state_projected_i7 = 58.17`
- `explicit_rel_state_projected_oracle_i7 = 34.33`

Gap sanity package:

- `explicit_rel_state_projected_oracle_state_i7_pfitpoly2 = 38.72`
- `explicit_rel_state_projected_oracle_behavior_i7 = 44.61`
- `explicit_rel_state_projected_oracle_i7 = 45.56`

Interpretation:

- the coarse ordering `oracle > real > baseline` still appears on the stronger same-family model;
- the corrected `fitpoly2` bridge does not collapse under `gpt-5-mini`;
- this is not a full cross-model generalization result, but it meaningfully reduces concern that the current findings are only a `gpt-5-nano` artifact.

Route-compare export cleanup and route-freeze recheck:

- fixed `paper_eval.py` route grouping so that when one `case_id + mode` contains multiple exported `session_id`s, eval now selects one coherent session instead of concatenating duplicated turns;
- re-ran route eval into [paper_eval_route_compare_v2_out](d:/My%20Project/companion-ai/paper_eval_route_compare_v2_out);
- confirmed duplicated `turn_idx` exports in `...vs_oracle_full_i7` route comparisons are removed in the v2 judge package;
- cleaned route-freeze read remains consistent with the first-pass qualitative judgment:
  - real route: direct `relation -> i7` still looks stronger in `warm` and `cool`, with `vulnerability` close to a tie;
  - oracle-state route: corrected `relation -> fitted 8D -> i7` remains competitive and still looks better in `vulnerability` and `cool`, while direct `relation -> i7` looks cleaner in `warm`;
- current working freeze:
  - treat direct `relation -> i7` as the stronger main deployable-controller candidate;
  - retain `relation -> fitted 8D -> i7` as a real analytic-bridge route rather than dropping it as a failed design.

Post-freeze oracle-set expansion:

- added:
  - [paper_cases_oracle_exec_v2.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v2.json)
  - [paper_cases_oracle_state_exec_v2.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v2.json)
- these extend the oracle set from 3 cases to 5 cases by adding:
  - `oracle_exec_mixed_001`
  - `oracle_exec_mixed_002`
- total oracle phase points increase from 18 to 30;
- intended use:
  - keep `relation -> i7` as the main frozen deployable route;
  - keep `relation -> fitted 8D -> i7` as the analytic-bridge route;
  - evaluate both on a broader post-freeze oracle substrate before any larger final sample expansion.


## 2026-03-16: final frozen manual judge

Built and manually read the frozen final judge packs under [paper_eval_frozen_final_judge_v1_out](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out).

Record:
- [manual_judge_results.md](d:/My%20Project/companion-ai/paper_eval_frozen_final_judge_v1_out/manual_judge_results.md)

Takeaways:
- `direct relation -> i7` cleanly beats strong baseline on all 5 frozen oracle cases.
- `oracle_i7` remains a slightly cleaner upper reference, but the deploy gap to direct `relation -> i7` is now small in manual reading.
- corrected `relation -> fitted 8D -> i7` remains close to both `oracle_behavior_i7` and `oracle_i7`, so the 8D layer should be retained as an analytic bridge instead of treated as a failed route.
- current paper freeze is now clear:
  - main deployable controller: `relation -> i7`
  - analytic bridge: `relation -> behavior(8D) -> i7`


## 2026-03-16: final judge protocol and next-step ordering

Added:
- [PAPER_FINAL_JUDGE_PLAN.md](d:/My%20Project/companion-ai/PAPER_FINAL_JUDGE_PLAN.md)
- [PAPER_NEXT_STEPS_ORDER.md](d:/My%20Project/companion-ai/PAPER_NEXT_STEPS_ORDER.md)

These freeze:
- a final evaluation protocol that treats manual coherence judge and pairwise preference as the main evidence;
- a post-freeze work order that prioritizes data expansion and parameter interpretation before reopening interface-shape or relation-dimensionality questions.


## 2026-03-16: 4D fitted-model parameter interpretation

Added:
- [PAPER_4D_PARAMETER_INTERPRETATION.md](d:/My%20Project/companion-ai/PAPER_4D_PARAMETER_INTERPRETATION.md)

Key reading:
- the fitted bridge is more structured than the early hand-written projector;
- warmth is mostly driven by bond/care;
- initiative, affective follow-up, and clarification look more like permission-sensitive continuation signals;
- stability mostly acts as a suppressor rather than a generic positive relation variable.


## 2026-03-16: large oracle-expansion target and relation-dimension validation

Added:
- [PAPER_ORACLE_EXPANSION_PLAN_150PLUS.md](d:/My%20Project/companion-ai/PAPER_ORACLE_EXPANSION_PLAN_150PLUS.md)

Updated:
- [PAPER_NEXT_STEPS_ORDER.md](d:/My%20Project/companion-ai/PAPER_NEXT_STEPS_ORDER.md)

Current plan:
- expand oracle cases to `144-180` phase points rather than doing another small bump;
- keep `mixed_signal` as a mandatory family;
- treat post-expansion relation-dimensionality validation as an earlier next-step than deployable-interface shape comparison.


## 2026-03-16: oracle expansion to 180 phase points

Generated a new large oracle substrate:
- [paper_cases_oracle_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_exec_v3.json)
- [paper_cases_oracle_state_exec_v3.json](d:/My%20Project/companion-ai/paper_cases_oracle_state_exec_v3.json)

Current scale:
- `30` cases
- `180` phase points
- `6` balanced families including `mixed_signal`, `ordinary_neutral`, and `boundary_repair`


## 2026-03-16: post-expansion relation dimensionality validation

Added:
- [paper_validate_relation_dimensionality.py](d:/My%20Project/companion-ai/paper_validate_relation_dimensionality.py)
- [paper_relation_dimensionality_validation_v1.json](d:/My%20Project/companion-ai/paper_relation_dimensionality_validation_v1.json)
- [PAPER_RELATION_DIMENSIONALITY_VALIDATION.md](d:/My%20Project/companion-ai/PAPER_RELATION_DIMENSIONALITY_VALIDATION.md)

Ran dimensionality validation on the full `180` oracle rows.

Main takeaways:
- current `raw4` is the strongest tested representation on both `linear` and `poly2`;
- all tested 2D and 3D subsets are worse, though the best 3D subsets remain reasonably competitive;
- this supports the current 4D space as a robust explanatory basis rather than a tiny-sample artifact.

Important caveat:
- the current 5D/6D variants are only deterministic linear augmentations of the same 4D labels;
- under the present linear / quadratic fit family, they are largely redundant with `raw4`;
- therefore the present `5D/6D ~= 4D` result does not yet rule out richer genuinely re-annotated relation ontologies.


## 2026-03-16: ontology-expansion scaffolding for genuinely new >4D relation factors

Added:
- [PAPER_RELATION_ONTOLOGY_EXPANSION.md](d:/My%20Project/companion-ai/PAPER_RELATION_ONTOLOGY_EXPANSION.md)
- [paper_build_relation_ontology_annotation_sheet.py](d:/My%20Project/companion-ai/paper_build_relation_ontology_annotation_sheet.py)
- [paper_relation_ontology_annotation_sheet_v1.csv](d:/My%20Project/companion-ai/paper_relation_ontology_annotation_sheet_v1.csv)
- [paper_relation_ontology_annotation_sheet_v1.json](d:/My%20Project/companion-ai/paper_relation_ontology_annotation_sheet_v1.json)

Current decision:
- the next relation-representation step should not be another deterministic transform of the current four labels;
- it should be a genuinely new manual ontology expansion on the full 180-row oracle substrate.

Current candidate factors:
- `interactional_permission`
- `boundary_firmness`

Current working ontology candidates:
1. `raw4 + interactional_permission`
2. `raw4 + interactional_permission + boundary_firmness`


## 2026-03-16: unsupervised latent dimensionality search (2D-6D)

Added:
- [paper_relation_latent_dim_search.py](d:/My%20Project/companion-ai/paper_relation_latent_dim_search.py)
- [paper_relation_latent_dim_search_v1.json](d:/My%20Project/companion-ai/paper_relation_latent_dim_search_v1.json)
- [PAPER_RELATION_LATENT_DIM_SEARCH.md](d:/My%20Project/companion-ai/PAPER_RELATION_LATENT_DIM_SEARCH.md)

Setup:
- use the full `180` oracle rows;
- derive a shared `17`-feature higher-order basis from raw4;
- learn unsupervised latent bases of size `2D` through `6D`;
- regress latent coordinates to 8D oracle behavior.

Main result:
- latent `2`: `0.0235`
- latent `3`: `0.0230`
- latent `4`: `0.0214`
- latent `5`: `0.0200`
- latent `6`: `0.0200`

Reading:
- `2D/3D` are clearly weaker than `4D`;
- `4D` remains robust;
- `5D/6D` give a modest but real gain over `4D`;
- therefore the current 4D ontology looks strong but probably not fully explanation-optimal.

Important boundary:
- this is a latent-basis result, not yet a human-readable ontology result.


## 2026-03-16: first interface-shape comparison

Added:
- [paper_build_interface_shape_judge_pack.py](d:/My%20Project/companion-ai/paper_build_interface_shape_judge_pack.py)

Compared:
- `8D -> i7-discrete`
- `8D -> continuous-interface (c8)`
- `relation -> i7 direct`

Main result (`180` turns):
- `projected_i7_pfitpoly2 = 41.79`
- `projected_c8_pfitpoly2 = 112.24`
- `rel_to_interface_i7 = 25.07`
- `oracle_i7 = 30.41`

Bridge result (`180` turns):
- `oracle_state_i7_pfitpoly2 = 33.05`
- `oracle_state_c8_pfitpoly2 = 94.43`
- `oracle_state_direct_i7 = 23.48`
- `oracle_behavior_i7 = 32.92`
- `oracle_i7 = 31.66`

Current reading:
- the first continuous deploy chart is clearly over-expansive;
- more continuous does not automatically mean more faithful at deployment time;
- the best current deploy chart remains direct `relation -> i7`;
- the best current analytic bridge remains `relation -> fitted 8D -> i7`.


## 2026-03-16: interface-shape v2 scaffolding and current interpretation shift

Added support in code for:
- `o8` = ordinal-soft chart
- `b8` = banded-continuous chart
- `h8` = hybrid chart

Current interpretation:
- `c8` only shows that the first naive continuous chart is bad;
- it does not prove that all softer or semi-continuous charts are bad;
- the current interface problem is best framed as a deploy-chart search problem.

Also clarified:
- the current latent-dimensionality search is still built around the existing `raw4` ontology;
- so it should be treated as a supporting probe, not as the final ontology-discovery experiment.


## 2026-03-17: deploy ontology / wording ablation and bridge sanity

Main deploy run on `v3`:

- ontology variants:
  - `vA` current `i7`
  - `vB` interactional-7
  - `vC` permission-7
- wording variants:
  - `sa`
  - `sb`
  - `sc`

Main reading:

- ontology effects are larger than naming-only effects;
- `vA` remains the most stable deploy ontology;
- `vC` is the only serious alternative still worth keeping;
- `vB` currently looks weaker rather than better;
- `sb` tends to induce more expansion;
- therefore the shortlist becomes:
  - `vA + sa/sc`
  - `vC + sa/sc`

Bridge sanity on `v1`:

- no bridge-side reversal appeared;
- `vA` remains the most stable ontology on the projected bridge;
- `sc_vA` is the strongest bridge-facing wording setting in the small-sample sanity check;
- `vC` remains interesting but does not displace `vA`;
- `vB` still lacks a clear upside.

Important correction:

- these are still proxy-driven readings;
- small length differences should no longer be over-interpreted as quality differences;
- the correct next step is focused manual judge on the shortlisted candidates.


## 2026-03-17: collaborative manual judge refinement

Joint manual reading across `warm / vuln / cool / repair` suggests a more nuanced picture than the raw proxy summary:

- `vA` still looks like the best default ontology.
- `vC` should be retained as a vulnerability-sensitive alternative rather than treated as uniformly worse.
- `sc` is now the most promising framing variant.
- `sa_vA` is not mainly failing through tool-like behavior; its issue is being too dry / too low-temperature in some cases.
- the projected route still loses primarily because it becomes tool-like, explanatory, and less person-like, especially in continuation turns.
- current strongest real candidate:
  - `direct sc_vA`


## 2026-03-17: shared latent manifold M1 scaffolding added

Added:

- `paper_shared_manifold_m1.py`

The script exports per-phase manifold views from existing result JSONL files and computes:

- cross-view distance-matrix correlation
- kNN neighborhood overlap
- trajectory smoothness

Current intended use:

- start with the frozen best real candidate (`direct sc_vA`)
- compare its relation / behavior / i7 / language geometry before moving to learned shared-latent modeling


## 2026-03-17: shared latent manifold M1/M2 interpretation update

M1 reading after relation-view fix:

- `raw4` and `behavior_8d` align strongly in local geometry;
- `i7` is more aligned with language realization than `behavior_8d` is;
- this fits the frozen story:
  - relation / behavior as analytic charts
  - `i7` as deploy chart

Important caution:

- this is still partly an internal-consistency result, because the current ontology stack was designed within the same research program.

M2 reading:

- a shared latent learned only from `behavior + i7 + language` can predict `relation_raw4` back strongly;
- this is the first result in this line that is stronger than a pure self-consistency check;
- oracle organizes the shared latent more cleanly than the best current real route, especially on the `i7` and language sides;
- the remaining gap is best understood as a structure-preservation gap from analytic views into deploy realization.


## 2026-03-17: shared latent manifold M2.5 inverse-manifold probe scaffold

Added:

- `paper_shared_manifold_m25.py`

Purpose:

- do not jump straight from M2 to a heavy M3 claim;
- keep the latent learned only from `behavior + i7 + language`;
- then test whether the latent can:
  - predict `relation_raw4` back,
  - separate interaction families,
  - preserve within-case trajectory smoothness.

Interpretive role:

- if this is strong, the shared-manifold framing gains a more substantive inverse-manifold argument;
- if this is weak, the project should keep the more modest reading that `4D / 8D / i7` are useful charts without overclaiming a deeper manifold structure.


## 2026-03-17: shared latent manifold M3-lite scaffold

Added:

- `paper_shared_manifold_m3_lite.py`

Purpose:

- do a narrower trajectory-distortion probe before any broad full-M3 claim;
- fit one pooled latent basis across the key routes;
- compare family path profiles and matched-case path distortion.

Current intended comparison:

- `direct sc_vA`
- `oracle_i7`
- optional `oracle_state_i7_pfitpoly2`


## 2026-03-17: shared latent manifold M3-lite results

On the first pooled-latent trajectory comparison (`direct sc_vA` vs `oracle_i7`):

- the real and oracle routes do not look like two different path systems;
- the real route looks more like a noisier / flatter version of the oracle trajectory geometry;
- the largest path distortion appears in:
  - `cooling`
  - `boundary_repair`
- distortion is smaller in:
  - `mixed_signal`
  - `vulnerability`
  - `warm`

Interpretation:

- the current best real deploy route is not failing because it follows the wrong broad geometry;
- it is failing because it preserves that geometry imperfectly, especially in cooling and repair-like cases;
- for the paper, this strengthens a theory-facing reading more than it motivates another large round of applied deploy-interface tweaking.


## 2026-03-17: native latent discovery line formalized

Added:

- `paper_native_latent_discovery.py`
- `PAPER_NATIVE_LATENT_DISCOVERY.md`

Reason:

- this is the more direct version of the core theory-facing question:
  - learn latent interaction structure from
    - `behavior_8d`
    - `i7_numeric`
    - `language_features`
  - then ask how many latent dimensions are actually needed;
  - only afterwards read current charts such as `raw4`, `8D behavior`, and `i7` against that latent.

Interpretive shift:

- the current `4D / 8D / i7` stack should now be treated less as a final ontology to be proved, and more as a set of useful charts discovered along the way.


## 2026-03-17: native chart reading scaffold

Added:

- `paper_native_chart_reading.py`
- `PAPER_NATIVE_CHART_READING.md`

Purpose:

- after learning a native latent from `behavior + i7 + language`, read `raw4`, `8D behavior`, and `i7` back as candidate charts over that latent;
- compare which chart is easiest to read out and which is most geometrically aligned.


## 2026-03-17: native latent extended sweep and chart-reading results

Extended native-latent sweep:

- from `2D-12D` to `2D-16D`

Current reading:

- the latent still improves materially through `16D`;
- the native structure suggested by the current multi-view data is therefore clearly richer than the current `raw4` chart;
- family and trajectory diagnostics do not scale in the same way, which suggests that added dimensions mostly improve view-reconstruction fidelity rather than converting the problem into a clean family-clustering story.

Chart-reading result:

- `behavior_8d` is the chart whose geometry is most aligned with the native latent;
- `i7` remains the strongest deploy chart but is a more compressed view;
- `raw4` is readable from the latent but is the coarsest chart.

Interpretive consequence:

- the project should now be written as discovering a useful chart decomposition, not as proving the final ontological truth of `4D -> 8D -> i7`.


## 2026-03-17: paper line frozen and rewritten for drafting

Added:

- `PAPER_PAPERLINE_SYNTHESIS.md`

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL.md`

Current paper-facing position:

- the original project is sufficiently converged to write up as a paper;
- the main claim is now about:
  - explicit relational control under a strong baseline,
  - deploy-chart selection,
  - analytic/deploy separation,
  - and conservative chart-role clarification;
- it is no longer useful to overstate the late manifold line as direct discovery of the model's true internal relational ontology.

Frozen writeup stance:

- deploy route: `relation -> i7 direct`
- best current real controller: `direct sc_vA`
- analytic bridge: `relation -> behavior(8D) -> i7`
- `vC` retained only as a vulnerability-sensitive alternative
- manifold/native-latent results retained as conservative theory-facing support, not as the central headline


## 2026-03-17: cleaner V2 paper draft created

Added:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`

Reason:

- the earlier draft had accumulated duplicated late-stage material and mixed-strength claims;
- the project now has a sufficiently frozen paper line to justify a cleaner rewrite.

Current use:

- treat `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md` as the main draft going forward;
- keep the original draft as trace/history, not as the cleanest paper-facing version.


## 2026-03-17: V2 draft expanded toward submission form

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`

Added:

- `Related Work`
- explicit `Judge Protocol`

Effect:

- the draft now reads more like a paper skeleton and less like a pure project memo;
- judge-based coherence evaluation is now framed as the main endpoint rather than an afterthought after proxy summaries.


## 2026-03-17: V2 draft given explicit table and citation placeholders

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`

Added:

- result-table placeholders
- appendix-table placeholders
- citation placeholders

Effect:

- the draft is now closer to a paper assembly document;
- remaining work is more clearly:
  - fill citations
  - decide exact numeric tables
  - polish prose


## 2026-03-17: table drafts and citation plan added

Added:

- `PAPER_TABLE_DRAFTS.md`
- `PAPER_RELATED_WORK_CITATION_PLAN.md`

Effect:

- main-paper tables, appendix tables, and citation buckets now have dedicated staging files;
- the remaining paper-writing work is more mechanical and less exploratory.


## 2026-03-17: first-pass paper tables filled

Updated:

- `PAPER_TABLE_DRAFTS.md`

Current status:

- the paper now has first-pass global rows and summary interpretations for the main tables;
- remaining work is to replace provisional case-level placeholders with final adjudicated values if needed.


## 2026-03-17: draft/table alignment and citation candidates added

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`
- `PAPER_RELATED_WORK_CITATION_PLAN.md`

Effect:

- the draft now explicitly points to the planned main tables and appendix table;
- the citation plan now contains concrete candidate works rather than only abstract literature buckets.


## 2026-03-17: key submission gaps written down explicitly

Added:

- `PAPER_SUBMISSION_GAPS.md`

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`

Effect:

- the current draft now distinguishes more clearly between:
  - what the project already establishes strongly enough for a paper;
  - and what is still weak if the goal is a harder submission-standard claim.


## 2026-03-17: baseline-to-i7 ablation route implemented

Updated:

- `app/api/chat.py`
- `app/generation/execution_interface.py`
- `paper_run_experiment.py`

Added:

- `baseline_relational_instruction_to_interface`

Effect:

- the missing no-relational-state `i7` control is now available in code;
- this sets up the key causal-isolation experiment:
  - baseline
  - baseline `-> i7`
  - explicit `relation -> i7`


## 2026-03-17: judge protocol frozen into appendix-ready spec

Added:

- `PAPER_JUDGE_PROTOCOL_APPENDIX.md`

Effect:

- the paper now has a concrete appendix-level evaluation specification rather than only a prose description of judge philosophy;
- remaining work is to actually run and report multi-judge / agreement at the desired rigor level.


## 2026-03-17: draft reframed around useful chart decomposition

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`
- `PAPER_SUBMISSION_GAPS.md`
- `PAPER_TABLE_DRAFTS.md`

Effect:

- the paper now says more directly that a richer one-layer manifold may exist in principle;
- the current `raw4 / behavior_8d / i7` stack is defended as a useful chart decomposition,
  not as proof of a final layered ontology;
- a dedicated structure-vs-interface ablation table slot is now reserved in the paper assembly files.


## 2026-03-17: structure-vs-interface v1 proxy confirms mixed attribution

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`
- `PAPER_TABLE_DRAFTS.md`
- `PAPER_SUBMISSION_GAPS.md`
- `PAPER_PAPERLINE_SYNTHESIS.md`

Observed proxy:

- baseline = `98.17`
- baseline `-> i7` = `41.33`
- explicit `relation -> i7` = `16.50`

Effect:

- the paper can no longer be read as "all gain comes from two-layer structure itself";
- but it also should not collapse into "only the final `i7` interface matters";
- the strongest current reading is mixed:
  - `i7` explains a large share of the gain
  - explicit relation-chart decomposition adds further gain beyond interface-only control


## 2026-03-17: structure-vs-interface judge-pack builder added

Added:

- `paper_build_structure_vs_interface_judge_pack.py`

Effect:

- the new ablation now has a dedicated focused-judge path;
- next step is to build the package and read:
  - baseline vs baseline `-> i7`
  - baseline `-> i7` vs explicit `relation -> i7`
  - explicit `relation -> i7` vs oracle `i7`


## 2026-03-17: structure-vs-interface focused judge confirms mixed attribution

Updated:

- `PAPER_DRAFT_RELATIONAL_CONTROL_V2.md`
- `PAPER_TABLE_DRAFTS.md`
- `PAPER_SUBMISSION_GAPS.md`

Read cases:

- `warm`
- `vuln`
- `cool`

Effect:

- `baseline -> i7` is now clearly supported as a real improvement over baseline;
- `explicit relation -> i7` is also supported as a further improvement beyond interface-only `i7`;
- the strongest current interpretation is now:
  - interface gain is large
  - decomposition gain is real
  - explicit `relation -> i7` is already close to oracle deploy behavior.


## 2026-03-17: evaluation formalization and coherence operationalization hardened

Added:

- `PAPER_JUDGE_PROTOCOL_APPENDIX.md`
- `paper_judge_agreement.py`
- `PAPER_RELATIONAL_COHERENCE_OPERATIONALIZATION.md`
- `paper_relational_proxy_metrics.py`

Effect:

- the paper now has:
  - a fixed appendix-level judge specification,
  - a concrete multi-judge raw-agreement computation path,
  - and a semi-formal automatic proxy layer for abrupt-shift-like behavior;
- this does not replace the judge-centered endpoint, but it materially reduces the risk that the evaluation reads as purely subjective and non-operationalized.
## 2026-03-18 - semi-natural generalization set draft

- Added `paper_cases_semi_natural_v1.json` as a first-pass semi-natural generalization set.
- The draft uses the same `phases` schema as the oracle execution sets but intentionally omits oracle annotations.
- Current coverage is `12` cases total:
  - `warming_trajectory` x2
  - `vulnerability_with_correction` x2
  - `cooling_trajectory` x2
  - `mixed_signal_trajectory` x2
  - `ordinary_neutral` x2
  - `boundary_repair` x2
- Intended use: lighter-weight generalization testing on `baseline`, `baseline -> i7`, and `relation -> i7` after human screening.

## 2026-03-18 - semi-natural generalization set v2

- Added `paper_cases_semi_natural_v2.json` as a distribution-shifted semi-natural set.
- `v2` is intended to be less templatic than `v1`:
  - signal positions are less fixed,
  - user corrections are less schematic,
  - and topic variation is broader.
- Current coverage remains `12` cases total across the same `6` families.
- Intended paper-facing use: prefer `v2` over `v1` for semi-natural generalization after human screening.
