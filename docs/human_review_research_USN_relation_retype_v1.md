# USN-HR-01 现有 43 条关系分层归位研究支持与决策建议 v1

状态：AI 语义核查完成，项目负责人已于 2026-08-21 按建议全部拍板。研究日期：2026-08-21。

本文件服务于 `human_review_assignment_USN_relation_retype_v1.md` 的 6 项分组决定。下列内容原为**非约束性建议**，现已由项目负责人确认；正式决定以 `outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv` 和 `docs/human_review_return_USN_relation_retype_v1.md` 为准。

本任务只决定既有 F001–F043 应进入哪一层及哪一 `proposed_record_family`。它不重审事实，不改变原 `review_status`、`claim_status`、金额、端点身份、时间或图资格，也不新增任何关系。

## 一页拍板表

| 规则 | 目标 | 行数 | 建议 | 关键结论 |
|---|---|---:|---|---|
| USN-RT-R01 | USN02 `money_flows` | 8 | `accept` | 八行均为资金／赞助／grant／汇总财务观察；commission 不在本组，金额门保持原样 |
| USN-RT-R02 | USN04 `service_recipient` | 4 | `accept` | 实物、设备取得协助与共同交付归服务—受益方层；recipient 解析和估值另过门 |
| USN-RT-R03 | USN05 `affiliation_control` | 9 | `revise` | 九行仍全进 USN05；F017、F043 的 record family 改为 `regional_branch`，其余七行为 `umbrella_membership` |
| USN-RT-R04 | USN06 `action_institution` | 20 | `accept` | 服务点、案件角色、行政委托、事件／项目参与与协调均保留 scope node；不生成共同参与者两两边 |
| USN-RT-R05 | LEAD `research_lead` | 1 | `accept` | F012 仍为 `opportunity_not_award`，不得进入资金流 |
| USN-RT-R06 | EXCLUDE `history_only` | 1 | `accept` | 同意 F008 的 proposed destination；它继续是 rejected duplicate，不是恢复该行 |

建议汇总为 `accept 5 / revise 1`。这里 R06 的 `accept` 表示“同意归入 EXCLUDE”，不是接受 F008 为有效关系。

## R01 — USN02 money_flows

建议：`accept`，无 edge 例外。

| edge | 归位 | 必守边界 |
|---|---|---|
| F001 | `direct_resource_transfer` | 原事实仍为 `ai_seeded`；notes 中 JPY 1,000,000 不自动写入 amount |
| F002 | `sponsorship_resource_flow` | 宽口径长期 sponsor 观察与较新 USD 16,000 具额捐赠分开 |
| F021 | `direct_resource_transfer` | 保留已核 USD 3,250、日期与直接慈善捐赠语义 |
| F025 | `direct_resource_transfer` | KOSC→AWWA contribution 可归资金层；USD 102,000 是复合汇总，不挂到本边 |
| F026 | `grant_resource_flow` | AWWA→USO Kinser grant 关系可保留，金额继续未知 |
| F027 | `aggregate_multi_recipient_observation` | 约40年／约 JPY 8亿只作多 recipient 汇总，不拆到年度或机构 |
| F034 | `sponsorship_resource_flow` | MBC tier 未拆 cash/in-kind 且无金额，继续保留原 research-lead 边界 |
| F035 | `sponsorship_resource_flow` | Matson 的 target 是 USO Indo-Pacific；不得改写为 USO Okinawa 定向资助 |

F031、F032、F033 三条 commission 均保留在 USN06，没有进入 USN02，也不得因这次归位生成付款金额。

建议 `principal_note_or_exceptions`：

> 逐行核对 F001、F002、F021、F025、F026、F027、F034、F035，同意 USN02 及各 proposed_record_family，无例外。仅批准语义归位：F001/F002 不从 notes 补金额；F021 保留 USD 3,250；F025 不得挂接 USD 102,000；F027 保留约 JPY 8 亿／约40年的多 recipient 汇总，不能分配到具体 recipient 或年度；F034/F035 的 sponsor tier 不换算金额，F035 不写成冲绳定向资助。所有原 review/claim、端点与图资格不变；commission 不在本组。

## R02 — USN04 service_recipient

建议：`accept`，无 edge 例外。

| edge | 归位 | 必守边界 |
|---|---|---|
| F028 | `in_kind_transfer` | JPY 2,000,000 只作有来源的实物估值，不是现金付款 |
| F029 | `in_kind_transfer` | 法人 recipient 已确认；具体下属设施与金额仍未确认 |
| F030 | `acquisition_assistance` | 不补事件日期、数量、金额或 AWWA 份额 |
| F036 | `joint_in_kind_transfer` | NOSCO 只是四个贡献方之一；recipient 正式名称未解析，不能把三台设备或全部价值归给 NOSCO |

四个 target 的身份状态并不相同：设施与 operator 分离、法人已核但下属设施未明、历史—现名 crosswalk、描述性 recipient 未解析。它们继续经 USN08 解决，不能为了画图自动新增 registry actor。

建议 `principal_note_or_exceptions`：

> 逐行核对 F028、F029、F030、F036，同意 USN04 及各 proposed_record_family，无例外。F028 的 JPY 2,000,000 仅作为实物价值保留，不是现金或付款；F029 不补具体下属设施或金额；F030 不补事件日、数量、金额或 AWWA 份额；F036 保留四方共同交付和未解析 recipient，不把三台设备或全部价值归给 NOSCO，也不生成联盟边。recipient 解析继续走 USN08，原 review/claim 与 graph eligibility 不变。

## R03 — USN05 affiliation_control

建议：`revise`，但九行的目标表仍全部是 USN05。

USN05 的受控 `affiliation_type` 区分 `umbrella_membership`、`regional_branch`、`operator`、`fiscal_sponsorship` 和 `governance_control`。当前 crosswalk 将旧 `organizational_affiliation` 原样带入 record family；对本组两条全国／地域结构，建议收紧为 `regional_branch`：

| edge | 建议 record family | 状态与边界 |
|---|---|---|
| F006、F007、F022、F023 | `umbrella_membership` | AWWA→NOSCO/KOSC/OESC/MOSCO；membership 不等于 control 或资金 |
| F024 | `umbrella_membership` | 只保留 ACGO 在 2012/2015 的历史成员观察；不推定当前连续性或退出日 |
| F037、F038 | `umbrella_membership` | 全国爆音原告团连络会→嘉手纳／普天间原告团；协调网络不是治理机构 |
| F017 | **改为 `regional_branch`** | A063 关东 block→A048 本体的迁移语义；原事实仍为 `ai_seeded`，不得翻转端点、合并 actor 或自动确认正式控制 |
| F043 | **改为 `regional_branch`** | 日本 YWCA→沖縄YWCA 全国—地域结构；不推定法律人格相同、治理控制或行动继承 |

九行均不达到 `governance_control` 门槛；`control_dimension` 应留空或 `not_applicable`。若未来合并器要求 parent→branch 的统一箭头方向，应另做方向字段复核，不能由本次归位自动翻转 F017。

建议 `principal_note_or_exceptions`：

> 接受9行全部归入 USN05 affiliation_control，但将 F017、F043 的 proposed_record_family 从泛型 organizational_affiliation 修订为 regional_branch；其余 F006、F007、F022、F023、F024、F037、F038 保持 umbrella_membership。全部9行只表示有方向和端点角色的结构关系，不编码 governance_control；control_dimension 留空或 not_applicable。F024 保留历史成员及2012/2015观察边界，不推定当前连续性或退出日期；F017 原事实状态保持 ai_seeded，且本次不翻转端点；F043 不推定 A105/A107 法律人格相同、治理控制或母组织行动自动转移。任何 membership、regional branch 或共同协调均不推出资金、政治联盟、共同立场或影响。

## R04 — USN06 action_institution

建议：`accept`，无 destination 例外。

- F003、F004、F005、F009、F010：只保留 actor→base/place 的 `service_site_presence`；地点不是组织 recipient。
- F011：ONC 与 JICA 的节庆合作围绕 festival/event node 表达，不保留为一般组织合作边。
- F013：只是共同出现线索，继续 `needs_second_source`；必须挂事件 node，不生成 A047–A019 联盟边。
- F014、F015、F018：协调观察需落实具体 action/event/program scope；缺 scope 时继续 off-graph。
- F016：共同政策活动是 program/event role，不是稳定 partnership。
- F019：只同意归 USN06；原 `not_supported + needs_second_source` 与疑似 A074 端点错配不被修复或确认。
- F020：公投法律支持只作具体程序／案件角色，原补证门槛不变。
- F031、F032、F033：只记录公共委托／制度角色；project cost 不得写成 contract payment，不把不同年度汇总成一笔付款。
- F039、F042：只限具体噪音诉讼律师角色，不推定资金或稳定联盟。
- F040、F041：只限具体活动角色，不生成一般联盟边。

建议 `principal_note_or_exceptions`：

> 同意20行归入 USN06；无 destination 例外。全部继承原 review、claim 与 graph 状态，归位不构成事实复核。F003、F004、F005、F009、F010只保留 actor→base/place 的 service_site_presence；F011、F013、F014、F015、F016、F018、F020、F040、F041须围绕具体 event/program/case scope 表达，不得保留或生成共同活动主体之间的联盟边，缺少 scope node 时继续 off-graph。F019继续保持 needs_second_source/not_supported，归位不确认其疑似 A074 端点错配。F031、F032、F033只记录公共委托／制度角色，不携带或推算付款，project cost 不得写成 contract payment。F039、F042只限具体案件律师角色，不推定资金或稳定联盟。

## R05 — LEAD

建议：`accept`。

> 同意 F012 仅进入 LEAD/research_lead，保留 opportunity_not_award、needs_local_retrieval、unknown_recipient 与 off-graph 状态。NOFO、总可用额度或预计 award 数量均不构成已授资金；没有官方具名 award 与 recipient 记录前不得生成 money flow。

本组与第2份 USHR008 的拍板一致：NOFO 可作为项目／机会线索，但不构成 award commitment 或具名资金关系。

## R06 — EXCLUDE

建议：`accept` proposed destination。

> 同意 F008 仅保留为 history_only/rejected_duplicate。F022 继续作为唯一的 X004–X007 membership 记录；不得复活 F008、不得形成第二条关系，也不得由 membership 推定资金、控制或政治联盟。

## 拍板后的受控动作

负责人已按本稿确认；当前受控动作状态为：

1. 六行规则表已回填：R01/R02/R04/R05/R06=`accept`，R03=`revise`，并写入 notes、reviewer 和日期。
2. 独立正式回传与 post-return validator 已生成；未运行会清空决定的 pre-human builder。
3. 四份正式任务和五项 principal architecture checkpoint 现已全部回传；43行 crosswalk 仍不展开，下一步先提交受控集成设计、预期 diff 与幂等测试方案。
4. 后续展开时，只有 F017、F043 的 `proposed_record_family` 发生映射修订；其余 41 行保留原 proposal。所有 43 行的原事实、review/claim、金额、端点、时间和图资格原样继承。
