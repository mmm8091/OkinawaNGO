# USN-ACCOUNTABILITY-02 人工复核回传 v1

日期：2026-08-21

拍板人：项目负责人

研究与证据辅助：Codex

来源任务：`docs/human_review_assignment_USN_accountability_v1.md`

正式回填：`outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv`

状态：**9 项全部完成负责人决定；仅回填 research-only 任务包，未作中央合并或前端发布。**

## 决定记录

| 任务 | 对象 | 负责人决定 |
|---|---|---|
| USHR001 | Earthjustice 案件资源 | `revise` |
| USHR002 | A070 身份、连续出现及人物 | `revise` |
| USHR003 | A070→No Heliport… 协调端点 | `revise` |
| USHR004 | 吉川秀樹双重职务 person bridge | `accept` |
| USHR005 | Network for Okinawa | `revise` |
| USHR006 | Protect；Henoko Anti-Base Project | `revise` |
| USHR007 | A033／A042 冲绳持续性 | `revise` |
| USHR008 | X013 Okinawa Youth Council NOFO | `accept` |
| USHR009 | X014 NED 负检索 | `revise` |

## 必须保留的决定边界

1. Earthjustice 的 USD 276,345.50 是权责发生制 FY2021 Form 990 中报告的案件级 court-award amount；财政部另有 USD 280,000 Judgment Fund 付款记录。两数不合并，不据此生成 OSD→Earthjustice 的简单资金边。
2. A070 的身份与人物角色按多个公开日期分别观察；目录日期不作为任职起始日，离散快照不补成无间断任期。
3. USAA005 撤销错误的 A019 端点，改指 `EO_R5_FUTAMI_TEN_DISTRICTS` 或保留 raw label；event-only 身份不进入 actor-to-actor 主图。
4. 吉川秀樹的双重职务只形成点时 person bridge，不生成 A001↔A002 的组织关系、联盟或资金边。
5. `Network for Okinawa` 与 A028/JUCON 是不同主体；独立 coalition 是否进入 registry 另过 actor gate。
6. `Protect Henoko and Takae! NGO Network` 与 `ZHAP / ZENKO Henoko Anti-base Project` 的标签规范不等于 actor admission，也不证明 membership、funding 或稳定联盟。
7. A033 的 2015、2019 材料是两个离散冲绳事件；A042 当前日本清洁航运项目不能补作冲绳连续性。
8. Okinawa Youth Council 材料只是 NOFO／机会，不是 award；完整机会号为 `Naha-PAS-FY24-02-M001`，仍不建立 directed funding edge。
9. NED 负检索只约束指定公开列表、检索词和日期；匿名披露制度使“未找到具名冲绳对象”不能写成“没有 NED 资助”或“没有 Japan 项目”。

## 后续受控整合动作

- 先修正 USAA005 endpoint，再考虑关系写回；所有 event-only／provisional endpoint 保持 off-graph。
- USAR001 调整期间、resource type 与 amount semantics；财政部付款机制另建来源线索，不覆盖 990 金额。
- 人物表统一采用 `role_observed_at` 表示页面／目录观察日，只有来源明确的任期起点才写 `role_start`。
- 归档与 source proposal 动作按 `human_review_research_USN_accountability_v1.md` 执行，新增来源仍标 `relation_or_claim_approved=no`。
- 四份 USN 正式任务和五项 architecture checkpoint 现已全部返回；该条件完成只允许进入受控集成设计，不自动授权中央 merge 或 publication adapter。

## 写回边界

本回传只确认 USN accountability research package 的人工决定。中央 actor、relation、source、person、publication adapter 和 frontend 均保持不变；下一步另行设计、验证受控集成并提交预期 diff，再由负责人授权实际写入。
