# 项目负责人人工复核剩余任务盘点 v16

日期：2026-07-20

口径：在 v15 基础上扣除负责人已确认的 HR-035 Batch 1 共 15 项；不把尚未正式派发的
actor–issue 候选自动算成必须完成的人审。

## 当前正式未闭合：157 项

| 类别 | 数量 | 说明 |
|---|---:|---|
| 现在可做的线上决定 | 101 | HR-010 batch 6：47；LCR001–004：4；HR-034：50 |
| 有依赖、后做的线上决定 | 44 | HR-029：41；HR-031：3 |
| 当地／新一手材料决定 | 12 | HR-017：9；HR-018：2；HR-024 A073：1 |
| **合计** | **157** | 155 个空白决定＋HR-018 两个已 defer、等待新材料的项目 |

## HR-035 Batch 1 已闭合

负责人于 2026-07-20 确认：

- `accept`：6；
- `revise`：8；
- `reject`：1（AI178）；
- `defer_second_source`／`defer_local`：0。

确认文件：

- `outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv`
- `docs/human_review_return_HR035_batch01_v1.md`

本轮确认关闭 HR-035 的 15 个人工决定，但中央 actor–issue 表和下游派生包仍待主线程受控合并。

## 仍可立即进行的 101 项

### 1. HR-010 batch 6：47 项

对象为 A087–A093、A095–A101 的 actor–issue 边级补证。组织身份已经存在，但确切议题连接
尚未完成事实复核。该批直接影响 17 个此前孤立 actor 的议题连接。

权威表：

`outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`

### 2. LCR001–004：4 项

四个生命周期个案，分别处理已解散、未活动、连续性不明或发展性改组的状态语义。必须把
生命周期状态与普通 `review_status` 分栏，不用相近名称自动合并组织。

权威表：

`outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv`

### 3. HR-034：50 项

45 条 source-log legacy status、AI068，以及 4 条表级字段政策。该任务是状态语义 crosswalk，
不是把旧状态批量改成 `human_checked`。

权威表：

`outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv`

## 有依赖、后做的 44 项

### HR-029：41 项

schema／alias 最终冻结。必须等 HR-010 batch 6、LCR001–004、HR-034 合并后重新生成，当前
505-candidate 包不是最终 freeze。

### HR-031：3 项

报告解释强度：基地问题“转译”、地点差异强度、边野古“连续国际化”措辞。应在事实和字段
冻结以后最后决定。

## 本轮不做的当地／新材料 12 项

- HR-017 公投程序：9；
- HR-018 行政协作：2；
- HR-024 A073：1。

这些项目需要当地报刊、馆藏、内部记录或新的独立一手材料；不因线上未找到而自动拒绝。

## 尚未正式派发的 actor–issue 债务

HR-035 审计还识别出：

- 58 条旧人工接受边尚缺 v1 `claim_status/reviewed_fields/confirmed_scope` 字段冻结；
- 在 HR-019 已审解释范围、但事实仍待审的边中，除已完成的 Batch 1 外，还有 42 条线上项和
  2 条当地材料项。

这些事实债务继续在前端标为未冻结，但当前不计入 157 个正式未闭合决定。是否继续建立
HR-035 Batch 2，应由负责人完成当前 101 项前置任务后另行决定。

## 推荐顺序

1. HR-010 batch 6（47）；
2. LCR001–004（4）；
3. HR-034（50）；
4. 决定是否正式派发 HR-035 Batch 2／legacy 字段冻结；
5. 重新生成并处理 HR-029（41）；
6. 最后处理 HR-031（3）。
