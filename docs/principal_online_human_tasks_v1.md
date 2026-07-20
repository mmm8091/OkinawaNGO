# 项目负责人当前线上人工任务单 v1

日期：2026-07-20  
对象：项目负责人  
范围：只列线上可完成、必须由人作判断的任务；不列当地检索和 AI 机械任务。

当前计数详表：`docs/principal_human_review_remaining_v19.md`。

## 1. 一句话状态

此前列出的 **183 个正式线上人工决定已于 2026-07-20 全部由负责人确认并完成受控合并**：

- HR-035 Batch 1：15项；
- HR-010 批6、LCR001–004、HR-034：101项；
- HR-029 schema／alias freeze：41项；
- HR-031 报告解释强度：3项；
- HR-035 Batch 2：23项。

当前已派发且决定栏为空的线上人工任务为 **0**。AI157、AI158 已作
`defer_second_source` 决定，属于后续在线补源线索，不是空白人工决定。另有 12 个当地／
新一手材料项：HR-017 九项、HR-018 两项和 HR-024/A073 一项；其中 HR-018 两项已有
`deferred_local_or_internal_record` 决定，等待新材料后闭合。以下旧批次说明保留为派工
审计轨迹，不再是待办清单。

## 2. 广泛研究的独立检查点

### OPI-00 · 项目重新进入决策单

状态：**已有暂停／未完成回交记录，仍未满足。**

入口：`lessons/0001-project-reentry-5-hour.html`
回交：`docs/principal_checkpoint_return_OPI00_v1.md`

这不阻断已批准的有界人工复核和机械维护，但继续阻断未经另行批准的广泛研究波次。

## 3. 历史派工范围（已闭合）

### 第一组 · HR-035 Batch 1：案件／公投／程序 actor–issue 事实边（15）

权威队列：

`outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv`

这 15 条已经由 HR-019 审过解释范围，但事实边仍为 `ai_seeded`。本轮只判断现有来源能否
支持确切 actor—issue 映射，不重做 bridge 或 scope。原告、律师、requester、supporter、
proponent 与争议 target 必须分开；AI106 与 AI178 是优先纠错项。

### 第二组 · HR-010 批 6：actor–issue 边级证据（47）

权威队列：

`outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`

对象为 A087–A093、A095–A101 的 47 条补证。逐条决定证据是否足以支持该组织—议题边及其范围，不从 registry `issue_tags` 自动生边。

边界：

- 法人宗旨不等于所有项目都已实际实施；
- 分支机构材料不能无条件外推到全县组织；
- 某次声明／行动只支持事件级角色，不自动支持长期组织定位；
- 接受 issue edge 不批准组织间联盟、资金或因果关系。

### 第三组 · LCR001–004：生命周期个案（4）

权威队列：

`outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv`

受控规则已经确认，但四个具体个案仍为空白。分别判断解散、改组、休止或持续性未确认。

边界：线上未见近期活动不等于解散；身份、谱系和活动连续性必须分开。

### 第四组 · HR-034：非法 `review_status` 交叉表（50）

权威队列：

`outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv`

构成：

- 中央 source log 逐行判断 45 项；
- actor–issue AI068 逐行判断 1 项；
- R4、R9、异质行动和 lifecycle 的表级字段政策 4 项。

边界：

- `verified`、`human_verified`、`accepted`、`qa_safe_online`、`watchlist_only` 不能按字符串自动映射为 `human_checked`；
- source 状态迁移不批准 actor、edge、金额或解释；
- AI067 已被 HR-019 拒绝；AI068 也不得借状态迁移重新进入默认冲绳关系图；
- 表级政策不等于把受影响的 10／29／49／4 行批量判成人工通过。

## 4. 后置任务（均已闭合）

### HR-029 · schema／alias 最终冻结（41）

当前重生快照：

`outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv`

状态：**已完成并合并。** 前置决定合并后已重生 505-candidate／41-item 快照，41 项决定均已
完成中央冻结；P004/P010 保持分离。

### HR-031 · 报告解释强度（3）

权威队列：

`outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv`

状态：**已完成并合并。** 三项均采用经负责人确认的限定解释；仍不批准新的事实、角色、
边、金额或因果。

## 5. 不在本轮线上任务里

- HR-017 local：9；
- HR-018 local：2，已有 defer 决定，等待 KOSC／AWWA 年报、Form 990 或等价新材料后闭合；
- HR-024 A073：1，`online_exhausted`／E0；
- HR-023、HR-028：机械任务，零人工决定；
- NR-04／NR-05：须先完成 OPI-00；
- 当地 T2-D／E／F／G：属于当地检索任务，不属于线上人工复核。

## 6. 历史执行节奏

每次只处理 **8–12 项、60–90 分钟**，不要把不同证据语义混成一个大批次。

实际顺序：

1. HR-035 Batch 1，先完成 15 条最重要的案件／公投／程序事实边；
2. HR-010 批 6，完成新组织—议题事实；
3. LCR001–004，单独处理生命周期；
4. HR-034，先逐行来源，再处理表级字段政策；
5. 主线程决定 HR-035 后续批次，并最终重生 HR-029；
6. 分批完成 HR-029 的 41 项；
7. 最后完成 HR-031 的 3 项。

所有决定都写回权威 CSV，并保留 reviewer、date、note 和限定范围；AI 不代填。
