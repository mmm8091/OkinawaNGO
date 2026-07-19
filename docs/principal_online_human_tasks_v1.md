# 项目负责人当前线上人工任务单 v1

日期：2026-07-20  
对象：项目负责人  
范围：只列线上可完成、必须由人作判断的任务；不列当地检索和 AI 机械任务。

当前计数详表：`docs/principal_human_review_remaining_v14.md`。

## 1. 一句话状态

当前尚有 **145 个线上人工决定**：

- **101 个现在可以分批进行**：HR-010 批 6 的 47 项、LCR001–004 的 4 项、HR-034 的 50 项；
- **41 个要在上述决定合并并重生后进行**：HR-029 schema／alias freeze；
- **3 个最后进行**：HR-031 报告解释强度；
- 另有 **12 个当地／新一手材料项**，不在本线上任务单内。

HR-016 至 HR-033 中已有负责人回交的线上决定均已合并；HR-017 local 9、HR-018 local 2、HR-024 A073 1 继续保持空白。

## 2. 广泛研究的独立检查点

### OPI-00 · 项目重新进入决策单

状态：**已有暂停／未完成回交记录，仍未满足。**

入口：`lessons/0001-project-reentry-5-hour.html`
回交：`docs/principal_checkpoint_return_OPI00_v1.md`

这不阻断以下 101 项有界人工复核和已经批准的机械维护，但继续阻断 NR-04／NR-05 或其他大范围研究波次。

## 3. 现在可以做：101 项

### 第一组 · HR-010 批 6：actor–issue 边级证据（47）

权威队列：

`outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`

对象为 A087–A093、A095–A101 的 47 条补证。逐条决定证据是否足以支持该组织—议题边及其范围，不从 registry `issue_tags` 自动生边。

边界：

- 法人宗旨不等于所有项目都已实际实施；
- 分支机构材料不能无条件外推到全县组织；
- 某次声明／行动只支持事件级角色，不自动支持长期组织定位；
- 接受 issue edge 不批准组织间联盟、资金或因果关系。

### 第二组 · LCR001–004：生命周期个案（4）

权威队列：

`outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv`

受控规则已经确认，但四个具体个案仍为空白。分别判断解散、改组、休止或持续性未确认。

边界：线上未见近期活动不等于解散；身份、谱系和活动连续性必须分开。

### 第三组 · HR-034：非法 `review_status` 交叉表（50）

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

## 4. 上述 101 项完成后再做

### HR-029 · schema／alias 最终冻结（41）

当前重生快照：

`outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv`

状态：**暂不执行。** 当前包有 505 个统一候选和 41 个空白决定，但 HR-010、生命周期和 HR-034 会改变最终冻结输入。先合并这三组，再重生一次 HR-029。

### HR-031 · 报告解释强度（3）

权威队列：

`outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv`

状态：**最后做。** 它只决定报告／论文的解释强度，不批准新的事实、角色、边、金额或因果。

## 5. 不在本轮线上任务里

- HR-017 local：9；
- HR-018 local：2；
- HR-024 A073：1，`online_exhausted`／E0；
- HR-023、HR-028：机械任务，零人工决定；
- NR-04／NR-05：须先完成 OPI-00；
- 当地 T2-D／E／F：属于当地检索任务，不属于线上人工复核。

## 6. 推荐执行节奏

每次只处理 **8–12 项、60–90 分钟**，不要把不同证据语义混成一个大批次。

建议顺序：

1. HR-010 批 6，先完成组织—议题事实；
2. LCR001–004，单独处理生命周期；
3. HR-034，先逐行来源，再处理表级字段政策；
4. 主线程机械合并并最终重生 HR-029；
5. 分批完成 HR-029 的 41 项；
6. 最后完成 HR-031 的 3 项。

所有决定都写回权威 CSV，并保留 reviewer、date、note 和限定范围；AI 不代填。
