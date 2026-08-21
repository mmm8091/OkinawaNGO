# USN-SERVICE-01 研究支持与决策建议 v1

状态：AI 证据核查完成；项目负责人于 2026-08-20 按本稿建议全部确认。研究日期：2026-08-19。

本文件服务于 `human_review_assignment_USN_service_ecology_v1.md` 的 13 项正式人工任务。下列内容原为**非约束性建议**；负责人已经全部确认，正式决定以 `outputs/us_presence_service_recon_v1/human_review_queue_v1.csv` 和 `human_review_return_USN_service_ecology_v1.md` 为准。本轮没有改中央 actor、relation、source、person、前端数据或 publication adapter。

## 一页拍板表

| 任务 | 对象 | 建议使用的允许决定 | 置信度 | 最关键边界 |
|---|---|---|---|---|
| SR-HR-001 | Marine Thrift Shop Okinawa | `add_background_service_actor` | 高 | 只批组织身份，不连带批准赠款或 AWWA 边 |
| SR-HR-002 | Marine Gift Shop | `add_with_status_note` | 中高 | 当前运作可核；联邦免税资格仍 unresolved |
| SR-HR-003 | Neighborhood Pantry – Camp Butler | `add_actor` | 中高 | MCIPAC 私人组织身份支持自治；法人／税号未知 |
| SR-HR-004 | NIOSC | `add_background_service_actor` | 高 | `positive contribution` 只是组织自述 |
| SR-HR-005A | Army Emergency Relief | `national_actor_with_local_presence` | 高 | Torii 只建同一全国 actor 的服务 presence |
| SR-HR-005B | Air & Space Forces Aid Society | `national_actor_with_local_presence` | 高 | Kadena 只建同一全国 actor 的服务 presence |
| SR-HR-006A | Helping Japan International | `defer_second_source` | 中 | 法律身份已较清楚，但 HJI—HelpOki—冲绳功能桥接未证 |
| SR-HR-006B | OAO Civilian Welfare Council | `defer_second_source` | 高 | 仍只有 roster，不能凭名称推定功能 |
| SR-HR-007 | ACGO 生命周期 | `retain_historical_status_unknown` | 高 | FY2018 是 last observed，不是 dissolution date |
| SR-HR-008 | KOSC→AWWA USD 2,580 | `defer_underlying_filing_or_crosswalk` | 高 | 金额位于 Schedule I 的个人援助表，组织受款语义异常 |
| SR-HR-009 | OESC→AWWA USD 8,479 | `accept_new_dated_flow` | 高 | 官方 XML 明列 AWWA EIN、金额和期间 |
| SR-HR-010 | MTS—AWWA | `accept_membership_and_separate_channel_role` | 高 | membership、渠道、年度金额必须三分 |
| SR-HR-011 | USO sponsor roster | `accept_dated_sponsor_snapshot` | 高 | 仅是 2026-08-19 层级快照；区域层和冲绳层分开 |
| SR-HR-012 | 解释门禁 | `revise_gate_with_explicit_rule` | 高 | 恢复四级并改称 LEG0–LEG3；目前无 LEG3 |
| SR-HR-013 / SR006 | NPO/ARU | `defer_identity` | 高 | MTS 直接受款端更像 Kubasaki HS，多跳链未解 |
| SR-HR-013 / SR007 | Tinsaku no Kai | `accept_crosswalk_with_canonical_name` | 高 | 规范为“沖縄小児在宅医療基金 てぃんさぐの会” |
| SR-HR-013 / SR009 | Far East Council | `accept_crosswalk_with_canonical_name` | 高 | 是美国侧 Scouting council，不是日本侧 recipient |
| SR-HR-013 / SR010 | Oki Hands Oki Hearts | `accept_crosswalk_with_canonical_name` | 高 | 身份可核；MTS 页面只支持候选 outreach support |

## 会改变原任务书建议的四项发现

1. **RF001 不能按普通组织拨款接受。** KOSC 申报的 USD 2,580 位于 Schedule I Part III “Grants and Other Assistance to Domestic Individuals”；AWWA 名称被填进援助类型栏，没有 recipient EIN 或地址。名称 crosswalk 很可能正确，但 dyadic organization flow 的申报语义未成立。
2. **解释门禁应恢复为四级。** 权威 `us_presence_network_architecture_v1.md` 已定义 L0–L3；任务书将“地方反应”和“可重复效果”挤进同一个 L2。为避免和前端的 L0/L1/L2 层级重名，本建议使用 `LEG0–LEG3`。
3. **“没有受益方材料”已过时，但仍无效果证据。** 已找到少量地方参加者、地方机构和地方媒体承载的反应材料，可做 LEG2 research-only 候选；没有调查、基线、比较、重复测量或可归因的态度／行为／制度效果，因此 LEG3 仍为零。
4. **SR006 的直接受款链被扁平化。** MTS 原页更像“`Kubasaki High School / Month of the Military Child Benefit`”，后接 `NPO/ARU/Halfway House for Teenage Girls` 下游标签。不能直接生成 MTS→ARU 边。

另有一项 source QA：S097 的 source-log 备注声称页面含 AK Kogyo、Domino’s，但 S097 归档 HTML 和 2026-08-19 当前页都只列 Matson、UMGC、AIG、MBC、AEC、Billabong。前两者不得进入本次 sponsor snapshot；S097 备注待受控修正。

## 分项证据与建议回填文字

### SR-HR-001 — Marine Thrift Shop Okinawa

建议：`add_background_service_actor`。

- [组织官网](https://marinethriftshopokinawa.org/)公开 mission、Camp Foster 地址、board、grants 和 outreach。
- [MCIPAC 私人组织名录](https://www.okinawa.usmc-mccs.org/more/private-organizations)将 Marine Thrift Shop 单列为 `ACTIVE`；同页说明这类 PO 是经书面授权、由个人在联邦官方身份之外控制的 non-federal entity，并非 MCCS 组成部分。
- IRS EO BMF（[官方 CSV](https://www.irs.gov/pub/irs-soi/eo_xx.csv)，2026-08-11 数据快照）命中 EIN `38-3924106`，`SUBSECTION=03`、`STATUS=01`、tax period `202412`。旧自动撤销历史行不能否定当前重新进入 BMF 的状态。

建议字段：canonical name=`Marine Thrift Shop Okinawa`；actor class=`base_community_service_actor`；origin=`us_origin`；legal status=`us_501c3_nonprofit`。

建议 `principal_note`：

> 新增 Marine Thrift Shop Okinawa 为基地社区服务背景 actor（base_community_service_actor；us_origin）。组织官网、现行 MCIPAC 私人组织名录及 IRS EO BMF（EIN 38-3924106，501(c)(3)，tax period 202412）共同支持身份与持续性。本决定不批准任何赠款、收款或 AWWA 关系边，也不赋予亲／反基地立场。

### SR-HR-002 — Marine Gift Shop

建议：`add_with_status_note`，把“当前运作”和“税务资格”拆开。

- MCIPAC roster 将 Marine Gift Shop 单列为 `ACTIVE`。
- [FY2025 IRS-derived filing](https://projects.propublica.org/nonprofits/organizations/980016061)有 EIN `98-0016061`、officers、库存销售和经营数据；IRS 2025 XML index 对应 object `202522959349301772`。
- 该申报自报 501(c)(4)，但 EIN 未出现在 2026-08-11 EO BMF；当前自动撤销 bulk 也未命中。缺失不能解释成普通自动撤销，最稳妥编码是联邦免税资格未解决。
- [占位官网](https://marinegiftshop.org/)不足以补足法律状态。历史材料曾把 MGS 与 MOSCO 相连，但当前 roster 分列、MGS 有独立 EIN/990，不能据此合并或创建现行控制边。

建议 `principal_note`：

> 以 add_with_status_note 新增 Marine Gift Shop，并与 MOSCO、AWWA、Marine Thrift Shop 保持不同 actor。现行 MCIPAC 名录和 FY2025 Form 990 支持持续运作；但申报仅自报 501(c)(4)，EIN 98-0016061 未见于 IRS 2026-08-11 EO BMF，故当前联邦免税资格编码为 unresolved。历史章程镜像不足以证明现行隶属，不新增结构边。

### SR-HR-003 — Neighborhood Pantry – Camp Butler

建议：`add_actor`。

- MCIPAC roster 将其作为独立 `ACTIVE` private organization 行；这比单纯项目名提供了更强的自治证据。
- [2024-08-14 MCIPAC 报道](https://www.mcipac.marines.mil/Media-Room/News/Article/3871746/camp-kinser-opens-a-new-neighborhood-pantry/)给出具名 assistant director、Foster/Kinser 两点和连续服务量。
- [项目页](https://marinethriftshopokinawa.org/neighborhood-pantry-camp-butler/)由 MTS 承载，但报道把 MTS 写成捐赠来源之一，把 CARES 写成协调框架，把 CLR-37 DRC office 写成 Kinser 场地；都不是已证 parent/host。
- actor 不等同法人。独立法人、EIN 和财务未知，应写入 legal-status 缺口，而不是把它降成 MTS program。

建议字段：actor class=`base_community_service_actor`；origin=`us_origin`；institutional status=`MCIPAC-authorized private organization; separate legal/tax status unknown`。

建议 `principal_note`：

> 将 Neighborhood Pantry – Camp Butler 新增为独立服务 actor。现行 MCIPAC 名录将其单列为 ACTIVE private organization，官方报道另有具名负责人、Foster/Kinser 两处持续服务。Marine Thrift Shop 是捐赠／网页支持方，CARES 是资源协调框架，CLR-37 DRC office 是 Kinser 场地；现有证据不支持把任何一方写成承载或母组织。独立法人及税务状态仍未知。

### SR-HR-004 — NIOSC

建议：`add_background_service_actor`。

- [NIOSC About](https://www.niosc.org/about-us)说明跨军种、SOFA、GS 配偶会员和公益功能；2025/26 活动页支持当前持续性。
- MCIPAC roster 将 `North Island Okinawa Spouses Club` 单列为 `ACTIVE`。
- IRS EO BMF 命中 EIN `98-0231743`、501(c)(3)、status 01；BMF 仍用旧法律名称 `North Island Officers Spouses Club`。当前名与旧法律名应作 rename/alias，而不是两个 actor。

建议字段：canonical name=`North Island Okinawa Spouses Club`；alias=`North Island Officers Spouses Club`；actor class=`base_spouse_club`；origin=`us_origin`；legal status=`us_501c3_nonprofit`。

建议 `principal_note`：

> 新增 North Island Okinawa Spouses Club（NIOSC）为基地配偶俱乐部背景 actor（base_spouse_club；us_origin）。组织官网、现行 MCIPAC 名录与 IRS EO BMF 共同支持身份和当前活动；BMF 旧名 North Island Officers Spouses Club 只作法律名／历史别名。官网关于 positive contribution 的表述仅作组织自述，不编码为地方接受或社会效果。

### SR-HR-005 — AER 与 AFAS

两者分别建议：`national_actor_with_local_presence`。全国组织共用一个 actor ID；Torii/Kadena 只建 service-presence 或 actor-place 记录，不新造冲绳法人 actor。

- [Army Emergency Relief 官网](https://www.armyemergencyrelief.org/about/)说明全国组织和 Arlington 总部；[Torii Station listing](https://installations.militaryonesource.mil/military-installation/torii-station/base-essentials/emergency-assistance)确认当地 office 及贷款／补助。
- AFAS 已于 2025-12-15 使用当前名 [Air & Space Forces Aid Society](https://afas.org/newname/)；[Kadena listing](https://installations.militaryonesource.mil/military-installation/kadena-ab/base-essentials/emergency-assistance)确认当地服务点与贷款／补助。

建议 `principal_note`：

> AER：将 Army Emergency Relief 编为 national actor with local presence；Torii Station 仅建 service-presence/actor-place 记录并复用全国 AER actor ID，不另建地方法人。
>
> AFAS：将 Air & Space Forces Aid Society 编为 national actor with local presence；Kadena 服务点仅建 service-presence/actor-place 记录并复用全国 AFAS actor ID，不另建地方法人。

### SR-HR-006 — Helping Japan International / OAO CWC

Helping Japan International 建议：`defer_second_source`。

- MCIPAC roster 单列 `ACTIVE / IRS`。
- IRS EO BMF 命中 EIN `83-4249039`、501(c)(3)、status 01、tax period `202512`，所以法律身份不再只有 roster 一条线索。
- [HelpOki 官网](https://www.helpoki.org/)公开冲绳救助功能，但页面没有把 HelpOki 与 Helping Japan International 法定名/EIN 明确桥接；roster 又覆盖 Okinawa、Fuji、Iwakuni，不能将 HelpOki 功能自动灌给 HJI。

建议 `principal_note`：

> 选择 defer_second_source。现行 MCIPAC 名录与 IRS EO BMF（EIN 83-4249039，501(c)(3)，tax period 202512）已支持 Helping Japan International 的法律身份，但尚缺一手材料把该法定名与 HelpOki 官网、具体冲绳地点及服务功能明确桥接；不凭名称推定服务关系。

Okinawa Area Office Civilian Welfare Council 建议：`defer_second_source`。

> 当前仅能确认 Okinawa Area Office Civilian Welfare Council 是 MCIPAC 名录中的 ACTIVE/Fiscal private-organization 条目；尚无第二条一手身份、逐行地点、治理或功能来源，不凭 Welfare/Council 名称推定服务关系。

### SR-HR-007 — ACGO 生命周期

建议：`retain_historical_status_unknown`。

- [公开 filing series](https://projects.propublica.org/nonprofits/organizations/261170858)最后观察到 FY2018。
- 当前 MCIPAC roster 和 EO BMF 未见 ACGO，但 absence 不能给出 dissolution 或 end date。
- IRS 自动撤销表保留历史行，也会保留其后恢复资格的组织；同一机制不能单独证明组织解散。尚无一手 dissolution、withdrawal、rename 或 successor 材料。

建议 `principal_note`：

> 保留 Army Community Group of Okinawa 为 historical actor，current status unknown；FY2018 仅作 last-observed filing bound。当前 MCIPAC 名录与 EO BMF 未见、以及 IRS 历史自动撤销行，均不等于组织解散或给出终止日；不设 end date，不认 successor，等待章程、会议记录或官方解散／更名材料。

### SR-HR-008 — KOSC→AWWA USD 2,580

建议：`defer_underlying_filing_or_crosswalk`。

- [KOSC FY ending 2025-05 full filing](https://projects.propublica.org/nonprofits/organizations/980214323/202630129349300153/full)的 Part IV line 21（国内组织／政府 grants）为 No，line 22（国内个人 assistance）为 Yes。
- [Schedule I](https://projects.propublica.org/nonprofits/full_text/202630129349300153/IRS990ScheduleI)的组织 recipient 表没有这条；`American Womens Welfare Association` 和 USD 2,580 出现在 Part III 国内个人援助表的“援助类型”栏，缺 recipient EIN、地址和组织 recipient 结构。
- 中央 alias 已把 `American Women's Welfare Association` 记为 X004 former name，所以名称 crosswalk 可能成立；但现有 F025/F007 不能修复新 filing 的金额语义。
- 同表还有 period 与标签不协调的 `Fall 2025 Scholarships`，进一步支持暂缓。不得覆盖历史 F025。

建议 `principal_note`：

> 底层申报已核：2024-06-01—2025-05-31 Form 990 的 Schedule I Part III（国内个人援助）列有“American Womens Welfare Association”2,580 美元，但 Part IV line 21=No、line 22=Yes，且该行无受款组织 EIN/地址。名称很可能对应 X004，但申报结构与组织拨款边不一致；本轮暂缓新增 dyadic flow，等待 KOSC/AWWA 年度明细或收款凭证。F025 与 F007 原边均不变。

### SR-HR-009 — OESC→AWWA USD 8,479

建议：`accept_new_dated_flow`。

IRS 官方 2025 bulk XML 已精确核实：ZIP [2025_TEOS_XML_11D](https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_11D.zip)，member `202513109349302911_public.xml`，节点 `Return/ReturnData/IRS990ScheduleI/RecipientTable`：

- filer=`OKINAWA ENLISTED SPOUSES CLUB`，EIN `98-0346507`；
- period=`2024-07-01`—`2025-06-30`，filed `2025-10-27`；
- recipient=`AMERICAN WELFARE AND WORKS ASSOCIATION`，EIN `98-0227149`；
- `CashGrantAmt=8479`，用途原文限定在冲绳美军社区相关免税组织的 grants。

建议 `principal_note`：

> 接受为新的有期组织 grant flow：X007 OESC→X004 AWWA，USD 8,479，amount_semantics=exact_reported，期间 2024-07-01—2025-06-30，申报日 2025-10-27。IRS Schedule I RecipientTable 明确给出 AWWA 名称、EIN 98-0227149 及现金拨款额；用途按原表保留。该边不推断下游用途、政治影响或其他年度关系。

### SR-HR-010 — MTS 与 AWWA

建议：`accept_membership_and_separate_channel_role`，前提是 SR-HR-001 批准 SA010 actor。

- [MTS Grants](https://marinethriftshopokinawa.org/grants/)明确区分：MTS 自有 board/申请流程；MTS 是 AWWA member 并向 AWWA grants 作 contribution；AWWA 申请流程另行运行。
- [MTS Outreach](https://marinethriftshopokinawa.org/outreach/)把 AWWA American Grants 与 Japanese Grants 分列。
- [2024 DVIDS 报道](https://www.dvidshub.net/news/printable/465683)说明 AWWA 通常参与 recipient 选择，而该次 Lions transfer 是绕过 AWWA 的例外。因此 AWWA 不是 MTS 唯一或恒定渠道。

建议拆成：

1. membership：MTS `member_of` AWWA；
2. channel：MTS 作为 contributing member，经 AWWA 作部分 grant selection/distribution；
3. 每年 amount：另建 flow，不写进 affiliation。

建议 `principal_note`：

> 在 SA010 actor 获准的前提下，接受两层拆分：结构层记 X004 AWWA→SA010 Marine Thrift Shop 的 network_membership；渠道层另记 SA010→X004 的 contributing_member_to_grant_selection/distribution_channel（以 2024 报道及当前官网为观察边界）。官网明确 AWWA 申请流程与 MTS 自有流程分开，2024 Lions 捐赠亦明确绕过 AWWA，故不得合并为泛化“合作关系”、控制关系或稳定唯一渠道；任何年度金额另建 flow。

### SR-HR-011 — USO sponsor roster

建议：`accept_dated_sponsor_snapshot`，`observed_at=2026-08-19`。

[USO Okinawa 当前 sponsor 页](https://okinawa.uso.org/sponsors)与 S097 2026-07-11 归档的可见名单一致：

| 层级与 target | 页面名称 | crosswalk / 去重建议 |
|---|---|---|
| USO Indo-Pacific Mission Partner | Matson | 复用 F035，只补本次观察，不复制；不是 Okinawa-local allocation |
| USO Indo-Pacific Mission Partner | University of Maryland Global Campus | 新 provisional institution endpoint；名称清楚 |
| USO Indo-Pacific Community Partner | AIG Auto Insurance | 详情页称 AIG Japan；具体法人仍 provisional |
| USO Okinawa Platinum | MBC | 复用 F034 / Mediatti Broadband Communications，不复制 |
| USO Okinawa Silver | American Engineering Corporation | 复用 X003/F002；2025 USD 16,000 flow 另存 |
| USO Okinawa Bronze | Billabong | 先写 `BILLABONG STORE Okinawa Rycom` provisional endpoint，不上升全球品牌／母公司 |

空的 Community/Gold 层不造边；tier 不换算金额、起始日、治理、隶属或政治立场。

建议 `principal_note`：

> 接受 2026-08-19 定点快照。区域层：Matson、UMGC=USO Indo-Pacific Mission Partner；AIG Japan/AIG Auto Insurance=USO Indo-Pacific Community Partner。冲绳层：Mediatti Broadband Communications/MBC=Platinum，X003 AEC=Silver，BILLABONG STORE Okinawa Rycom=Bronze。空层不生成边。所有行仅表示该日官网层级；金额、起始日、治理／隶属和政治立场均未证。F034/F035/F002 只作既有关系的本次再观察，不重复造边；AEC 2025 具额流另存。

### SR-HR-012 — 解释门禁

建议：`revise_gate_with_explicit_rule`。

权威 [USN architecture](us_presence_network_architecture_v1.md) 定义 L0–L3；[既有 actor-relation architecture](actor_relation_architecture_v1.md) 又将 L0/L1/L2 用于前端层。建议研究字段改称：

| 研究层级 | 门槛 | 允许表述 |
|---|---|---|
| LEG0 | 可核服务、资源流、recipient 或项目事实 | 只写发生了什么，不编码 legitimation |
| LEG1 | 行动方明示 goodwill、trust、bond、bridge 等目标／叙事 | 正当化意图或公开叙事，不写效果 |
| LEG2 | 受益者、地方机构或独立媒体的接受、转述、抵制或重释 | 只写有界公共反应；记录 `response_target`、`source_position` |
| LEG3 | 重复、基线／比较或明确研究设计下的态度、行为、制度效果 | 在竞争解释下讨论 effect |

当前 `legitimation_claim_observations_v1.csv` 机械上是 9 条 L1（LC001–008、012）和 3 条 L0（LC009–011），不是六条 narrative。逐行 QA 还发现：

- LC004 来源可拆出参加者体验的 LEG2 候选，但整行不能升级；
- LC006 是美军—陆自 `alliance/inter-service narrative`，不是冲绳民间反应；
- LC007 更接近 LEG0；若保留 LEG1，只能写弱 self-claim；
- LC012 是 sponsor durability，不是地方合法化；
- LC001 将 DVIDS 写成 E4，与 v0 codebook 将 DVIDS／地方新闻通常列为 E2 不一致。E0–E4 与 LEG0–LEG3 必须正交。

新找到的 LEG2 候选包括：

- [USO Futenma English Discussion](https://okinawa.uso.org/stories/41)中的参加者体验；
- [DVIDS 2020 Henoko 报道](https://www.dvidshub.net/news/400768/continuity-key-friendship)中的单一地方居民引语；
- [Japan Marines 2022 Halloween 报道](https://www.japan.marines.mil/-News/Article/Article/3202581/)中的幼儿园负责人反应；
- [宫古新报 2026-02-14](https://miyakoshinpo.com/2026/02/14/%E5%9C%A8%E6%B2%96%E7%B1%B3%E8%BB%8D%E5%A9%A6%E4%BA%BA%E7%A6%8F%E7%A5%89%E5%8D%94%E4%BC%9A%E3%81%8C%E5%B8%82%E9%95%B7%E8%A1%A8%E6%95%AC-%E6%96%BD%E8%A8%AD%E8%A6%96%E5%AF%9F%E3%81%A7%E7%A6%8F%E7%A5%89/)中的市长礼节性感谢。

它们是单次、被选择或礼节性材料，不能外推为冲绳公众意见，也都不是 LEG3。

建议 `principal_note`：

> 恢复 USN 架构的四级并改称 LEG0–LEG3：LEG0=可核服务或转移事实；LEG1=行动方明示的 goodwill/trust/bond/bridge 等意图或公开叙事；LEG2=受益者、地方机构或独立媒体的接受、转述、抵制或重释，须记录反应对象及来源位置；LEG3=有重复、基线／比较或明确研究设计的态度、行为或制度效果。当前 LC 表机械上为 9 条 LEG1、3 条 LEG0；不得将任何现有整行直接批准为效果结论。LC004 及新增检索可拆出若干 LEG2 research-only 候选，但仍无 LEG3。E0–E4 来源等级与 LEG 主张层级分开。

### SR-HR-013 — recipient crosswalk

#### SR006 / NPO/ARU

建议：`defer_identity`。

[MTS Grants](https://marinethriftshopokinawa.org/grants/)重复写作 `Kubasaki High School- US / Month of the Military Child Benefit NPO/ARU/Halfway House for Teenage Girls`。按页面的 recipient/purpose 结构，直接端更像 Kubasaki High School，ARU 是下游标签。`一般社団法人ある`（[gBizINFO](https://info.gbiz.go.jp/hojin/ichiran?hojinBango=2360005006351)、[官网](https://aru-okinawa.jp/%E3%81%82%E3%82%8B%E3%80%82%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/)）只是功能相近候选：法律类型、项目名和直接收款链都未吻合。

> SR006 选择 defer_identity。MTS 原页的直接 grant recipient 更可能是 Kubasaki High School-US，NPO/ARU/Halfway House for Teenage Girls 是 Month of the Military Child Benefit 的下游受益标签。一般社団法人ある是功能相近的身份候选，但法律类型、项目名称及直接收款链均未吻合；不得建立 MTS→一般社団法人ある直接边。后续须由 Kubasaki、MTS 或该组织的受赠确认材料解决。

#### SR007 / Tinsaku no Kai

建议：`accept_crosswalk_with_canonical_name`。

[组织官网](https://tynsag.jpn.org/about/)给出正式名 `沖縄小児在宅医療基金 てぃんさぐの会`、任意团体、1993 年设立，并说明医疗设备免费出借；[活动页](https://tynsag.jpn.org/activity/)列出具体器材；[冲绳县医师会资料](https://archive.okinawa.med.or.jp/html/kouho/kaiho/2019/pdf/05/105.pdf)独立确认名称与功能。MTS 的 `Tinsaku` 是来源拼写，不是另一个组织。

> SR007 选择 accept_crosswalk_with_canonical_name，canonical name=沖縄小児在宅医療基金 てぃんさぐの会，legal status=任意団体；保留 MTS 原拼写 Tinsaku no Kai 为来源别名。官网与冲绳县医师会资料均确认其医疗设备免费出借功能，与 MTS 的 Medical Equipment 用途高度吻合。不得与一般社团法人 Kukuru 或同名政治临时团体合并；身份批准不等于具体 grant／金额批准。

#### SR009 / Far East Council

建议：`accept_crosswalk_with_canonical_name`。

[Scouting America 官方页](https://www.scouting.org/international/resources/22-333/)使用当前名 `Far East Council, Scouting America`；[Far East Council 官网](https://www.fareastcouncil.org/far-east-council-home/about-the-far-east-council)列 Okinawa 服务区。HR-018 已确认历史名 crosswalk，故应复用 `R_BSA_FAR_EAST`，不造重复 actor。MTS 原页将其列在 `US` 侧，`Counsil` 是拼写错误。

> SR009 选择 accept_crosswalk_with_canonical_name，canonical name=Far East Council, Scouting America；Far East Counsil 为来源拼写错误，历史别名为 Boy Scouts of America Far East Council。该组织是服务亚太地区美国侨民／军属社区的美国侧 scouting council，不是日本侧组织。复用 HR-018 已批准的 R_BSA_FAR_EAST crosswalk；MTS 2023 equipment replacement 仍是无单项金额的独立候选事实。

#### SR010 / Oki Hands Oki Hearts

建议：`accept_crosswalk_with_canonical_name`。

- [国税庁法人番号页](https://www.houjin-bangou.nta.go.jp/henkorireki-johoto.html?selHouzinNo=3360005006276)确认正式名 `一般社団法人Ｏｋｉ Ｈａｎｄｓ Ｏｋｉ Ｈｅａｒｔｓ`、法人号 `3360005006276`。
- [袋中园／青云寮页面](https://taichuen.or.jp/wpmain/?p=885)用完整法人名称记录其捐赠；发布日期和正文受赠日必须分别保存。
- MTS [Outreach](https://marinethriftshopokinawa.org/outreach/)把 OHOH 列为 2025 Okinawan initiative，只支持候选 outreach support/funding，不支持当前 CSV 的 `outreach partnership`，也没有金额或接受记录。

> SR010 选择 accept_crosswalk_with_canonical_name，canonical name=一般社団法人Ｏｋｉ Ｈａｎｄｓ Ｏｋｉ Ｈｅａｒｔｓ，法人号=3360005006276，aliases=Oki Hands Oki Hearts; OHOH。法人番号与受赠机构官网足以确认当前法人身份；MTS 2025 页面仅支持候选 outreach support/funding，不应写成 partnership，且身份批准不等于金额或资金边批准。

## 拍板后的回填与来源动作

负责人已确认上述建议；下一步按以下顺序做受控回填：

1. 只填写 `human_review_queue_v1.csv` 的 `principal_decision` / `principal_note`，并生成单独 human-return 文档；不直接合并中央表。
2. 将 IRS 官方 XML 的 OESC→AWWA 记录作为正式 source proposal；KOSC 异常行保留 research-only 检索动作。
3. 为新增身份来源和 LEG2 候选建立 `relation_or_claim_approved=no` 的 source proposals，并保留访问日期／locator；动态网页采用新增 dated capture，不覆盖旧归档 bytes。
4. 受控修正 S097 过宽 notes；不把 AK Kogyo、Domino’s 写入本次 roster。
5. 对 LEG 表另开 schema/row 修订，不以 SR-HR-012 的拍板自动升级任何现有 LC 行。
6. 完成专用验证后暂停，再进入第 2 份正式任务“问责侧复核”。
