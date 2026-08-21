# USN-ACCOUNTABILITY-02 研究支持与决策建议 v1

状态：AI 证据核查完成；项目负责人于 2026-08-21 按本稿建议全部确认。研究日期：2026-08-20。

本文件服务于 `human_review_assignment_USN_accountability_v1.md` 的 9 项正式人工任务。下列内容原为**非约束性建议**；负责人已经全部确认，正式决定以 `outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv` 和 `human_review_return_USN_accountability_v1.md` 为准。本轮不修改中央 actor、relation、source、person、前端数据或 publication adapter。

## 一页拍板表

| 任务 | 对象 | 建议使用的允许决定 | 置信度 | 最关键修改／边界 |
|---|---|---|---|---|
| USHR001 | Earthjustice 案件资源 | `revise` | 高 | 990 的 USD 276,345.50 是权责发生制申报的案件明细；财政部另有 USD 280,000 付款记录，两数不得合并 |
| USHR002 | A070 身份、连续出现及人物 | `revise` | 高 | 身份与多期出现可升格；观察日不得写成任期起点，姓名变体需显式归一 |
| USHR003 | A070→“No Heliport…” | `revise` | 高 | 原 A019 端点错配；应改为二見以北十区会 event-only 身份或保留 raw label |
| USHR004 | 吉川秀樹双重职务 | `accept` | 高 | 同一简介足以确认 person bridge；2021-02-08 只作观察日 |
| USHR005 | Network for Okinawa | `revise` | 高 | 同页一手材料明确把它与 A028/JUCON 分开；保留独立 coalition 端点 |
| USHR006 | Protect；Henoko Anti-Base Project | `revise` | 中高 | 两个端点均可规范，但未过 actor admission，主图仍 off-graph |
| USHR007 | A033／A042 冲绳持续性 | `revise` | 高 | A033 新增 2019 有期事件证据；A042 仍只到 2015；均无持续项目结论 |
| USHR008 | X013 Youth Council NOFO | `accept` | 高 | opportunity-only 边界可接受；完整机会号作机械修正，仍无 named award／recipient |
| USHR009 | X014 NED 负检索 | `revise` | 高 | 只记录指定公开列表的字面检索；匿名披露使“未找到”不能等于“没有资助” |

## 会改变原任务书建议的关键发现

1. **USAA005 的 A019 端点应撤回。** VFP 会报用了简称 `No Heliport Base Association`；既有 S006 在同一名单中把 `No Heliport Base Association of 10 Districts North of Futamai` 与 A019 的英文名 `The Conference Opposing Heliport Construction` 分列。前者已经是经 HR-020 确认的 event-only 身份 `EO_R5_FUTAMI_TEN_DISTRICTS`。
2. **Network for Okinawa 不是 A028/JUCON。** CBD 2010 联署页给 Network 单列 member list，再把 `Japan-U.S. Citizens for Okinawa` 放入 additional supporters；CBD 同年公告还称 Network 与东京的 JUCON 共同赞助广告。应否定同一实体 crosswalk，而不是继续因名称相近而 defer。
3. **两个未解析英文端点已有较强交叉材料。** `Protect Henoko/Takae` 可规范为 `Protect Henoko and Takae! NGO Network`，且不是 A060；`Henoko Anti-Base Project` 高置信对应 `ZHAP / ZENKO Henoko Anti-base Project`。这解决标签，不自动通过 actor admission。
4. **A033 不再只有 2015 单点。** FoE Japan 官方页面显示 Friends of the Earth U.S. 是 2019 Henoko petition 的共同组织者／提交者。它支持第二个事件观察，却仍不足以证明 2015—2019 或 2019—现在的连续项目。
5. **Earthjustice 990 金额与联邦付款记录必须分开。** Part VIII 将 `COURT AWARDS` 列为 program-service revenue，Schedule O 再列出 Okinawa Dugong 的 USD 276,345.50，且申报采用 accrual accounting。财政部 Judgment Fund 另有 2021-03-05 的 USD 280,000 付款记录，责任机构为国防部长办公室、DOJ 为提交机构、Earthjustice 被列为 counsel；两数相差 USD 3,654.50，现有材料不能解释差额或证明两者是同一笔净额／总额。
6. **NED 负检索必须带披露制度边界。** FY2024 Asia、FY2025 年报 grant appendix 与截至 2026-07-15 的 active listing 均未定位冲绳关键词，但前两份存在 Japan-related regional projects；NED 又明确说明部分公开列表会隐去伙伴身份。因此只能说指定公开版本未定位冲绳具名 direct recipient／project。

## 分项证据与建议回填文字

### USHR001 — Earthjustice 案件资源

建议：`revise`。

- [Earthjustice FY2021 Form 990](https://earthjustice.org/wp-content/uploads/earthjustice-form990-fy21.pdf)覆盖 2020-07-01—2021-06-30。Part VIII（物理 PDF p.12/62，表内 p.9）把 `COURT AWARDS` 的 USD 3,747,441 列为 related/exempt-function program-service revenue。
- Schedule O（PDF 1-based p.55；原提案以 0-based index 54 定位，表内 p.2）在十大法院判给律师费／成本明细中列 `1272 OKINAWA DUGONG`、USD 276,345.50。
- Part XII（物理 PDF p.15/62，表内 p.12）勾选 `Accrual`。因此这两处合读支持“Earthjustice 在该申报期报告／确认的案件级 court-awards revenue 明细”，不支持把它写成该期现金到账。
- [财政部 Judgment Fund 2021-03-01—03-15 半月报](https://fiscal.treasury.gov/system/files/files/judgment-fund/payment-report-03-01-21-thru-03-15-21.xlsx)把同案原告组和 Earthjustice counsel 列在一起，并在 CBD 所在行记录 USD 280,000 attorney fees；责任机构为 `Office of the Secretary of Defense - Agencies`，提交机构为 DOJ，法源为 16 USC 470w-4。[财政部 filtered API](https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/payments/jfics/jfics_congress_report?filter=control_nbr:eq:202102348)进一步给出 control no. `202102348`、payment ID `022572021` 与 `payment_sent_date=2021-03-05`。
- USD 280,000 不等于 990 的 USD 276,345.50，且财政部行结构没有证明 USD 280,000 全额直接支付给 Earthjustice。它可以另存为付款机制线索，不能替代或合并 USAR001，也不能据此生成 OSD→Earthjustice 的简单资金边。
- 本轮对公开案卷的有界检索仍未取得 fee order／settlement 正文；Dkt. 237—246 需定向调取。这是材料缺口，不是不存在判费命令的证明。

建议把 USAR001 改为：`year_or_period=FY2021_2020-07-01/2021-06-30 (IRS form year 2020)`；`resource_type=court_awards_program_service_revenue_case_line`；`amount_semantics=case-level court-award amount reported by Earthjustice in its accrual-basis FY2021 return`。`provider_actor_id` 继续留空，不生成 directed money edge。

建议 `principal_note`：

> 建议 revise：接受 Earthjustice FY2021（2020-07-01—2021-06-30；IRS form year 2020）Form 990 所报告的案件级金额 USD 276,345.50；Schedule O 将 `1272 OKINAWA DUGONG` 列于 court-awarded attorney fees & costs，Part VIII 将组织当期 Court Awards 汇总列作 program-service revenue，且申报采用 accrual accounting。因此把语义改为“Earthjustice 在该申报期报告／确认的案件级 court-award amount”，不称该期现金 receipt，也不写成 donation、grant、项目预算或案件支出。财政部 Judgment Fund 另记录 2021-03-05 支付 USD 280,000：责任机构为 Office of the Secretary of Defense，DOJ 提交，Earthjustice 为 counsel；该金额落在 CBD 所在原告行并覆盖同案原告组，与 990 金额相差 USD 3,654.50，故两笔记录不合并，也不据此直接编码 OSD→Earthjustice。fee order／settlement 正文仍待 Dkt. 237—246 定向调取。

### USHR002 — A070 VFP-ROCK 身份、重复出现与人物

建议：`revise`。

- [VFP 2018 章节目录](https://www.veteransforpeace.org/files/8915/2183/7236/18.03.22.ChapterContacts.pdf)已列 chapter 1003 `Ryukyu Okinawa`，并写 `Charles 'Doug' Lummis`、`Peter Doktor`；这为后续姓名变体提供直接桥接。
- [2020 章节目录](https://www.veteransforpeace.org/files/1415/8938/5791/20.05.13.ChapterContact.pdf)列 `Charles Douglas Lummis`、`Pete Doktor` 为 chapter contacts，邮箱与 2018 目录一致。
- [2021 VFP 活动页](https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism)列 Pete Shimazaki Doktor 为 chapter 1003 co-founder、Doug Lummis 为 VFP-ROCK coordinator；这是 2021-02-08 的公开简介观察。
- [2023 春季会报](https://www.veteransforpeace.org/files/8616/8433/7175/VFPNews_2023.Spring-FULL_SMALL_FIN.pdf)print p.23 再次列 chapter 1003 及 Doug Lummis 的活动报告。
- [2025-01-31 目录](https://www.veteransforpeace.org/files/8017/3834/1504/25.01.31.ChapterContactListing.pdf)、[2026-02-09 目录](https://www.veteransforpeace.org/files/5617/7066/3944/26.02.09.ChapterContactListing.pdf)和 [2026-04-16 目录](https://www.veteransforpeace.org/files/4817/7635/3140/26.04.06.ChapterContactsforWebsite.nonames3.pdf)仍列 chapter 1003；2 月版本具名 Pete Doktor，4 月公开版本隐去姓名但保留相同邮箱。它们加强当前身份与重复出现，但不把间隔期补成每日连续活动或任期。

建议归一：`Charles Douglas Lummis`／`Charles 'Doug' Lummis`／`Doug Lummis` 为同一人物；`Peter Doktor`／`Pete Doktor`／`Pete Shimazaki Doktor` 为同一人物。USAPN006–007 的 `role_start` 应留空、只保留 `role_observed_at=2020-05-13`；2021 角色同理只作观察点。

建议 `principal_note`：

> 建议 revise：确认 A070 是 VFP chapter 1003 Ryukyu/Okinawa，并接受 2018、2020、2021、2023、2025、2026 官方材料中的重复出现。2018/2020 目录的同一邮箱支持 Charles Douglas/“Doug” Lummis 与 Peter/Pete Doktor 的姓名归一，2021 简介再支持 Pete Shimazaki Doktor 变体。所有人物职务均只按来源观察日记录；清空把观察日误写成任期起点的 `role_start`，不推断间隔期每日连续活动、完整任期或 chapter 对全国 VFP 的控制关系。

### USHR003 — A070 与 No Heliport Base Association 的协调

建议：`revise`，撤回 A019 端点。

- VFP 2023 春季会报 print p.23 支持 chapter 1003 自报“continues to work with”一个具名 coalition；这可作为 2023 春季的有界 coordination observation。
- [2022 OEJP 请求书](https://international.dsausa.org/files/sites/13/2022/11/OEJP-Okinawa-Letter.pdf)在同一参与名单中写全称 `No Heliport Base Association of 10 Districts North of Futamai`，并与 A070、Protect network、ZHAP 同群出现。
- 已归档 S006 的 2020 原始名单把上述十区会与 `The Conference Opposing Heliport Construction`（A019）分列。中央 `data/interim/25_coaction_event_participation_v0.csv` 已将十区会的人审 event-only identity 冻结为 `EO_R5_FUTAMI_TEN_DISTRICTS`。

因此 USAA005 的 target 首选改为 `EVENT_ONLY:EO_R5_FUTAMI_TEN_DISTRICTS`；若负责人要求来源间直接互认才准 crosswalk，则先保留 VFP raw label。event-only 身份未经过 actor admission，不进入 actor-to-actor 主图。

建议 `principal_note`：

> 建议 revise：接受 VFP 2023 春季会报中 A070 自报与具名 coalition 持续工作的有界协调事实，但撤销 A019 端点。VFP 的简称经 2022 OEJP 同群名单可展开为 `No Heliport Base Association of 10 Districts North of Futamai`；S006 又把该十区会与 A019 的英文名分列。目标改为既有 event-only 身份 `EO_R5_FUTAMI_TEN_DISTRICTS`，或在更严格门槛下保留 raw label。只按 2023 春季观察，不确认 membership、funding、稳定联盟或持续区间，主 actor graph 继续 off-graph。

### USHR004 — 吉川秀樹人物桥

建议：`accept`，但按点时语义读取日期。

- [VFP 2021-02-08 活动页](https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism)在同一 `YOSHIKAWA Hideki` 讲者简介中同时列 A002/SDCC `International Director` 与 A001/OEJP `Director`。
- 同一名称、同一简介、同一观察页足以确认 person bridge；未见同名冲突。
- 2021-02-08 是页面观察日，活动时间是冲绳时间 2021-02-15；两者都不是职务任期起点。若后续 schema 把 `role_start` 当真实任期字段，整合时应清空并只保留 `role_observed_at`。

建议 `principal_note`：

> 建议 accept：VFP 2021-02-08 官方活动页在同一吉川秀樹简介中同时列明 A002/SDCC International Director 与 A001/OEJP Director，可确认同一人物的两个同日公开职务并形成 person bridge。2021-02-08 仅作网页观察日，2021-02-15 仅作活动日；均不补任期起止，也不生成 A001↔A002 的组织关系、联盟或资金边。

### USHR005 — Network for Okinawa

建议：`revise`，明确否定 A028/JUCON 同一实体 crosswalk。

- [CBD 2010-04-23 联署页](https://www.biologicaldiversity.org/species/mammals/Okinawa_dugong/sign-on_letter.html)为 `Network for Okinawa` 单列 member groups，其中含 CBD；随后在 additional supporters 中另列 `Japan-U.S. Citizens for Okinawa`。
- [CBD 2010-05-14 公告](https://www.biologicaldiversity.org/news/press_releases/2010/okinawa-dugong-05-14-2010.html)称 Network 在华盛顿行动，并称 Network 与“Tokyo-based Japan-U.S. Citizens for Okinawa Network”共同赞助广告，再次把两者作为不同主体。
- 这足以回答“是否 A028”：否。仍在线的历史页面不能反推 Network 在 2026 年仍活跃。

USAA004 可保留为 A045→独立 coalition `Network for Okinawa` 的 2010 历史 member／works-with 观察；coalition 是否进入 registry 另过 actor gate。

建议 `principal_note`：

> 建议 revise：拒绝将 Network for Okinawa 交叉到 A028/JUCON。CBD 2010 联署页为 Network 单列成员名单，随后把 Japan-U.S. Citizens for Okinawa 另列为 additional supporter；同年 CBD 公告又把 Network 与东京的 JUCON 写成共同赞助广告的两个主体。USAA004 的目标改为独立 coalition Network for Okinawa，并只保留 2010 历史 member/works-with 观察；不据遗留页面推断 2026 活跃、稳定联盟或 A028 成员关系，是否建节点另过 actor gate。

### USHR006 — Protect Henoko/Takae；Henoko Anti-Base Project

建议：`revise`，规范两个标签但不直接建 registry actor 边。

- `Protect Henoko/Takae` 可规范为 `Protect Henoko and Takae! NGO Network`。 [FoE Japan 2019 页面](https://www.foejapan.org/en/aid/190412.html)把它列为 organizer；[2021 联合声明 PDF](https://www.foejapan.org/en/aid/210621_en_2.pdf)给出全称和东京联系方式；S006 已有同一全称的 event-only 参与记录。它不是在地住民组织 A060。
- `Henoko Anti-Base Project` 高置信对应 `ZHAP / ZENKO Henoko Anti-base Project`。[ZENKO 项目页](https://zenko-peace.com/zhap/1st)给出英文全称、ZHAP 缩写与联系方式；[现行英文页](https://zenko-peace.com/en/zhap)说明项目在 2020 年 5 月启动。2022 OEJP 名单也直接写 `ZHAP (ZENKO Henoko Anti-base Project)`。
- VFP 会报省略了 `ZENKO`／`ZHAP`，因此第二个 crosswalk 可标 `high_confidence/probable`，而不是假装来源内有法定名直接互认。

建议 `principal_note`：

> 建议 revise：将 `Protect Henoko/Takae` 规范为 `Protect Henoko and Takae! NGO Network`（既有 S006 event-only 身份，明确不是 A060）；将 `Henoko Anti-Base Project` 高置信规范为 `ZHAP / ZENKO Henoko Anti-base Project`。依据为组织／主办方页面的全称、联系方式及 2022 OEJP 同群名单。只接受 VFP 在 2023 春季自报的 coalition coordination；Protect 仍是 event-only、ZHAP 尚非 registry actor，故 actor-to-actor 主图继续 off-graph，待 actor admission。不得推 membership、funding、稳定联盟或冲绳本地法人属性。

### USHR007 — A033／A042 的冲绳持续性

建议：`revise`，拆开两者。

- A033/Friends of the Earth U.S. 不应再写成“只找到 2015”。[FoE Japan 2019-04-12 页面](https://www.foejapan.org/en/aid/190412.html)把 FoE U.S.、FoE Japan、Protect network 列为 Henoko petition organizers；[2019-06-24 后续页](https://www.foejapan.org/en/aid/190624.html)称三方提交 19,406 个联署。这是第二个冲绳议题事件观察。
- 这些材料支持 2015 与 2019 两个离散事件，不证明 A033 在间隔期或 2019 以后有持续 Okinawa program，也不自动生成其与 FoE Japan／Protect 的稳定联盟。
- 对 A042/Pacific Environment 的 `pacificenvironment.org` 有界检索仍未定位 2015 以后冲绳／Henoko／dugong 的组织材料。A042 保持 2015 NACSJ statement 的 event-level participant；负检索只描述所搜公开域名。
- [Pacific Environment 当前 Japan 页面](https://www.pacificenvironment.org/about-us/where-we-work/asia/japan/)与 [2025 项目启动页](https://www.pacificenvironment.org/pacific-environment-launches-clean-shipping-advocacy-in-japan/)显示其现有日本工作是清洁航运、港口脱碳和横滨等港口合作。它反驳“当前没有任何 Japan 工作”，但不构成冲绳、边野古或儒艮项目连续性。

建议 `principal_note`：

> 建议 revise 并拆分：A033 除 2015 NACSJ 声明外，FoE Japan 官方页面还支持其作为 2019 Henoko petition 共同组织者／提交者的第二个有期事件观察；这仍不证明连续项目、完整合作关系或当前活动。A042 在本轮官方域名有界检索中仍只保留 2015 冲绳事件参与；其 2025 年起日本清洁航运／港口脱碳项目不属于冲绳连续性。两者均不得因共同署名或单次共同组织而编码为稳定联盟。

### USHR008 — X013 Okinawa Youth Council NOFO

建议：`accept` opportunity-only 边界；完整机会号作机械修正。

- 已归档 S056 原 PDF 首页给出的完整 Funding Opportunity Number 是 `Naha-PAS-FY24-02-M001`，不是当前 USAR002 的缩写 `NAHA-PAS-02`；申请截止日为 2024-04-15。
- NOFO 写 `Total Amount Available: $10,000`、`Number of awards anticipated: One award`，并称 award amounts *may* range from USD 5,000 to 10,000。三者分别是总额度、预计数量与可能区间，不是已发生的 award。
- PDF p.2 另写 `subject to availability of funding`；p.8 明确只有 Grants Officer 签署的 award agreement 才是授权文件，NOFO 本身不构成 award commitment。Grants.gov 使用基号 `NAHA-PAS-FY24-02`，`-M001` 是该 PDF 的完整修订号。
- 截至 2026-08-20，按标题、基号、完整号及 USAspending／官方使领馆页面的有界检索仍未定位 named award 或 recipient。USAspending 的 DOS、AL 19.040、USD 0—15,000、2024-01-01—2025-12-31 导出中，Naha/`19JA51` 的 7 条记录均不能与该项目的标题、金额和活动说明同时匹配；其 `funding_opportunity_number` 又均为 `NOT APPLICABLE`，所以零匹配不能证明未授奖。第三方机会聚合页只复述 NOFO，不能补成 award。

USAR002 建议把 `associated_case_or_program` 修正为完整机会号，把 `resource_type` 写成 `notice_of_funding_opportunity`，并分别保存 total available／anticipated award count／possible award range；继续不建 directed funding edge。

建议 `principal_note`：

> 建议 accept opportunity-only 边界：S056 只证明 2024-04-15 截止的开放竞争、总可用额度 USD 10,000、预计一个 award 及可能的 USD 5,000—10,000 区间；p.8 明确 NOFO 不构成 award commitment。按标题、两种机会号及联邦支出记录的有界检索未定位具名 recipient，但 USAspending 机会号字段多为 `NOT APPLICABLE`，负检索不证明未授奖。X013 继续作为 program/opportunity node，USAR002 不建 directed funding edge；展示号机械修正为 `Naha-PAS-FY24-02-M001`，另存 Grants.gov 基号 alias。

### USHR009 — X014 NED 负检索

建议：`revise`，保留 watchlist，但收窄负面命题。

- [NED FY2024 grants page](https://www.ned.org/2024-grant-listings/)说明公开清单经过安全／duty-of-care 处理，部分伙伴身份会被隐去。
- [FY2024 Asia PDF](https://www.ned.org/wp-content/uploads/2025/04/Asia-Grant-Listing-FY24.pdf)覆盖 FY2024 获批且截至 2025-01-15 active 的项目。字面检索没有 `Okinawa`／`Ryukyu`，但其 Asia Regional 部分有一项 USD 249,321 的匿名项目，目标涉及把 democracy support 纳入 Japan foreign policy。它不能映射到冲绳 actor，也说明“没有 Japan grant”会过度表述。
- [NED 2025 Annual Report](https://www.ned.org/wp-content/uploads/2026/02/2025-Annual-Report.pdf) Appendix B 的同组冲绳关键词也为零；PDF p.116／报告内页 112 却有 6 个月、USD 98,000 的 Japan-related Asia Regional 项目，仍未指向冲绳。
- [截至 2026-07-15 的 Active Grant Listing PDF](https://www.ned.org/wp-content/uploads/2026/07/July-2026-Active-Grant-Listings_Final.pdf)共 102 页；`Okinawa / Okinawan / Ryukyu / Ryukyuan / Henoko / Naha / Sakishima / Yonaguni / Miyako / Ishigaki` 以及 `Japan / Japanese` 字面检索均未定位结果。[NED active-grant 页面](https://www.ned.org/active-grant-listing/)同时说明公开列表可能不披露伙伴身份。结果只约束所查版本和显式文本；FY2023 以前也未做等价的逐页全文审计。

建议 `principal_note`：

> 建议 revise：X014 保持 funder watchlist，不生成 NED→冲绳 actor 资金边。可记录“NED FY2024 Asia 正式列表、2025 Annual Report grant listings 及截至 2026-07-15 的 Active Grant Listing 中，指定冲绳关键词均零命中，未发现公开的 named Okinawa direct recipient／project”；不得写成“没有 NED 资助”或“没有 Japan 项目”。FY2024 与 FY2025 材料均含 Japan-related regional programming，NED 又明确说明部分伙伴身份因 duty of care 不公开，且 FY2023 以前未完成等价全文审计，因此负检索只能描述指定公开版本、检索词和日期。

## 建议的来源与归档动作

负责人决定已经完成；中央 source log 或 archive manifest 仍未改。后续受控集成设计应包括：

1. P0：归档 Earthjustice 990、财政部 Judgment Fund 半月报 XLSX／filtered API JSON、VFP 2018/2020/2021/2023 关键材料、CBD 2010 联署页／公告、2022 OEJP 请求书；保留 PDF 页码、printed-page 与观察日期三类 locator。另建 PACER Dkt. 237—246 定向调取任务，不用 CourtListener 的空正文替代 fee order。
2. P0：USAA005 先做 endpoint correction，再谈关系写回；不得让错误 A019 边进入主图。
3. P1：归档 FoE Japan 2019 两页、Protect 2021 PDF、ZENKO/ZHAP 自有页和 VFP 2025／2026-02-09／2026-04-16 目录；所有 source proposal 仍标 `relation_or_claim_approved=no`。
4. P1：S056/S082 不重复建源；在 source metadata 补完整 opportunity number 与 Grants.gov 基号 alias。USAspending 查询 JSON/CSV、过滤条件、检索时点及 hash 可作 `manual_archived` 检索快照。
5. P0：新增 NED 2025 Annual Report、2026-07 active-list PDF 与披露说明页；每次负检索记录 listing 版本、覆盖期、关键词、逐词计数与披露限制。
6. 人物表在整合前统一时间语义：`role_start` 只存来源明确的任期起点，页面／目录日期存 `role_observed_at`；姓名 alias 与 person identity 分字段。

## 拍板后才可做的动作

- 只回填 9 行 `principal_decision` 与 `principal_note`；`revise` 的具体字段修改留到受控整合层。
- 四份 USN 正式任务和五项 architecture checkpoint 已全部返回；下一步先做受控集成设计，仍不自动执行中央 merge、publication adapter 或前端写入。
- 关系层继续区分 case role、event participation、point-in-time coordination、membership 与 funding；本任务没有批准稳定联盟或因果主张。
