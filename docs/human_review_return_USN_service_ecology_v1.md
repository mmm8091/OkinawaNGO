# USN-SERVICE-01 人工复核回传 v1

日期：2026-08-20

拍板人：项目负责人

研究与证据辅助：Codex

来源任务：`docs/human_review_assignment_USN_service_ecology_v1.md`

正式回填：`outputs/us_presence_service_recon_v1/human_review_queue_v1.csv`

状态：**13 项全部完成负责人决定；仅回填 research-only 任务包，未作中央合并或前端发布。**

## 决定记录

| 任务 | 对象 | 负责人决定 |
|---|---|---|
| SR-HR-001 | Marine Thrift Shop Okinawa | `add_background_service_actor` |
| SR-HR-002 | Marine Gift Shop | `add_with_status_note` |
| SR-HR-003 | Neighborhood Pantry – Camp Butler | `add_actor` |
| SR-HR-004 | NIOSC | `add_background_service_actor` |
| SR-HR-005 | AER；AFAS | 两者均为 `national_actor_with_local_presence` |
| SR-HR-006 | Helping Japan International；OAO Civilian Welfare Council | 两者均为 `defer_second_source` |
| SR-HR-007 | ACGO | `retain_historical_status_unknown` |
| SR-HR-008 | KOSC→AWWA，USD 2,580 | `defer_underlying_filing_or_crosswalk` |
| SR-HR-009 | OESC→AWWA，USD 8,479 | `accept_new_dated_flow` |
| SR-HR-010 | Marine Thrift Shop—AWWA | `accept_membership_and_separate_channel_role` |
| SR-HR-011 | USO sponsor roster | `accept_dated_sponsor_snapshot` |
| SR-HR-012 | legitimation gate | `revise_gate_with_explicit_rule`，采用 LEG0–LEG3 |
| SR-HR-013 / SR006 | NPO/ARU | `defer_identity` |
| SR-HR-013 / SR007 | Tinsaku no Kai | `accept_crosswalk_with_canonical_name` |
| SR-HR-013 / SR009 | Far East Council | `accept_crosswalk_with_canonical_name` |
| SR-HR-013 / SR010 | Oki Hands Oki Hearts | `accept_crosswalk_with_canonical_name` |

复合项 SR-HR-013 在单一 `principal_decision` 字段中使用 `object_id=decision` 的分号分隔格式，以保留四个对象各自的允许决定；完整边界已经写入同一行 `principal_note`。

## 必须保留的决定边界

1. 新增或识别服务 actor 不赋予亲基地／反基地立场，也不自动批准 funding、recipient 或结构关系。
2. KOSC 的 USD 2,580 仅保留为待核异常 filing 观察；不得生成精确组织间 flow，也不得覆盖 F025/F007。
3. OESC→AWWA 的 USD 8,479 是 2024-07-01—2025-06-30 的单一有期申报事实；不外推下游用途、其他年度或政治影响。
4. MTS—AWWA 的 membership、grant-selection/distribution channel 与年度金额分别编码；AWWA 不是 MTS 已证唯一渠道。
5. USO roster 只表示 2026-08-19 的层级快照；区域层与冲绳层分开，tier 不换算金额或治理关系。
6. LEG0–LEG3 与 E0–E4 正交。现有 LC 行不得直接写成效果结论；LEG2 只收有界反应，LEG3 仍无证据。
7. recipient identity 的批准与具体受赠事实、金额或 partnership 语义分别审批。

## 新来源与归档处置

逐项 URL、locator、反证和建议引用见 `docs/human_review_research_USN_service_ecology_v1.md`。本次回填没有直接修改中央 source log 或归档 manifest。后续受控整合时：

- 将 OESC→AWWA 的 IRS 官方 XML 建为正式 source proposal；KOSC 异常行只保留 research-only 检索动作；
- 将新 actor／recipient identity 来源和 LEG2 候选以 `relation_or_claim_approved=no` 提案，不因本次身份决定自动批准关系或解释主张；
- 为 USO roster 新建带日期的 capture，不覆盖 S097 旧 bytes；受控修正 S097 中关于 AK Kogyo、Domino’s 的过宽备注；
- 在 LEG schema 另行实施四级改名和逐行 QA，不以本决定自动升级任何 LC 行。

## 写回边界

本回传只确认 USN service research package 的人工决定。四份正式任务和架构 checkpoint 现已完成；中央 actor、relation、source、person、publication adapter 和 frontend 仍保持不变。下一步先另行设计、验证受控集成，再由负责人授权实际写入。
