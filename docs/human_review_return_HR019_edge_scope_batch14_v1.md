# HR-019 actor–issue edge 范围第四组回交报告 Batch 14

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**负责人已确认——10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 31–40 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 本批 A112–A115 的 actor 身份、连续性、分类和 registry issue tags 已由 HR-027 人工确认；本次只判断 10 条 edge 的时间／角色范围。
- 同一组织的多个 issue edge 可能来自同一行动链，不得把标签数量当作互相独立的组织桥接或行动次数。
- 科学风险、污染来源、健康因果、罢工合法性、程序成败和政策效果均不由本批推定。
- 本报告不直接修改中央 edge 表、source log、HR CSV 或图。

## 0A. 本轮调查与反向核查

| actor | 本轮核查材料 | 调查所得 |
|---|---|---|
| A112 宮古島地下水研究会 | [组织官网](https://miyakojima-tikasui.com/)、[2024 年度总会／事业计划](https://miyakojima-tikasui.com/report_activity/2024_06_29.pdf)、S269–S271 | 官网将地下水称为宫古岛“命之水”，长期发布研究、学习会、监测、条例修改及市政要请；2024 事业计划继续列地下水流域协议会、保全条例修改、井泉调查、农药检测和医师会协作。支持持续组织功能，不证明其风险判断或污染归因正确。 |
| A113 宜野湾ちゅら水会 | [宜野湾市请愿状态](https://www.city.ginowan.lg.jp/shisei/gikai/5/14043.html)、[2022 市议会意见书](https://www.city.ginowan.lg.jp/material/files/group/61/ikensyo1.pdf)、[2025 公害调停申请报道](https://www.okinawatimes.co.jp/articles/-/1700743)、[2026 调停驳回报道](https://www.otv.co.jp/okitive/news/post/00015363/index.html) | 2022 PFAS 血液检查请愿截至 2026-03-27 仍为审查中；2025-10 与另外两团体申请公害调停，2026-02 因防卫设施适用除外而被程序性驳回。`legal` 应作为具名正式程序角色，不能写成一般法律组织定位，也不能写成实体问题败诉。 |
| A114 全港湾沖縄地方本部 | [2024 石垣港罢工报道](https://www.otv.co.jp/okitive/news/post/00010155/index.html)、[2024 Keen Sword 25 抗议](https://www.okinawatimes.co.jp/articles/-/1461249)、[2025 沖縄地本和平行进报告](https://www.zenkowan.org/wp-content/uploads/2025/06/%E6%B2%96%E7%B8%84%E5%9C%B0%E6%96%B9%E3%80%80%E6%96%B0%E9%87%8C%E8%89%AF%E5%B9%B3.pdf)、[2026 沖縄地本和平行进报告](https://www.zenkowan.org/wp-content/uploads/2026/06/%E6%B2%96%E7%B8%84%E5%9C%B0%E6%96%B9-%E5%AE%AE%E5%9F%8E-%E5%A4%A7%E7%BF%94.pdf)、S286–S289 | 分支级证据从 2015 反安保／边野古集会，延伸到 2024 石垣港罢工、Keen Sword 港湾抗议及 2025–2026 连续和平行进。可支持有时间边界的持续定位和组织行动 repertoire；不得判定罢工合法性／效果，也不能把全国工会材料自动转给沖縄地本。 |
| A115 新婦人沖縄県本部 | [2008 冲绳县行政记录](https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/014/905/h20gyouseikiroku.pdf)、[2018 边野古县民投票署名](https://www.jcp.or.jp/akahata/aik18/2018-06-18/2018061801_03_1.html)、[2024 中央＋县本部联合要请](https://www.shinfujin.gr.jp/16399/)、[2026 冲绳最前线化请愿名单](https://nomore-okinawasen.org/55871/)、S280–S283 | `women` 是会员制女性组织的核心身份；县本部可核的基地相关行动横跨 2008、2015、2018、2024、2026，已经超过单次事件。但全国中央本部 2014 声明 S254 不能作为县本部自身行动证据，联合要请须保留“中央＋县本部”口径。 |

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI223 | A112—groundwater | `organizational_positioning` | 组织名称、设立目的、研究、监测、条例倡议和持续事业计划直接支持 |
| AI225 | A112—life_safety | `organizational_positioning` | 持续把地下水作为饮用水源和“命之水”保护；不证明健康损害 |
| AI226 | A112—environment | `organizational_positioning` | 地下水保全、井泉调查、污染预防及珊瑚礁关切属于持续环境功能 |
| AI231 | A113—legal | `institutional_or_case_role` | 限于2022请愿及2025–2026公害调停等正式程序；不是一般法律组织 |
| AI232 | A114—anti_base | `organizational_positioning` | 2015–2026分支级行动反复连接边野古、基地负担和“基地ない沖縄” |
| AI233 | A114—anti_military | `organizational_positioning` | 严格限定为民用港军事利用、军舰寄港及日美演习反对 |
| AI234 | A114—peace | `organizational_positioning` | 2015行动及2024–2026连续和平行进支持持续和平活动 |
| AI236 | A114—mobilization | `organizational_positioning` | 集会、罢工、港湾抗议和年度行进构成重复组织 repertoire |
| AI237 | A115—women | `organizational_positioning` | 女性会员组织及县本部—支部—班结构的核心组织属性 |
| AI240 | A115—anti_base | `organizational_positioning` | 县本部多期具名行动支持；不得由全国中央声明或共同署名单独承担 |

建议分布：

- `organizational_positioning`：9 条；
- `institutional_or_case_role`：1 条；
- `event_specific`：0 条；
- `remain_unclear`：0 条。

## 2. AI223 · A112 宮古島地下水研究会—groundwater

组织名称、2018 设立材料、官网研究／活动目录、2023 宫古岛市正式回答及 2024 年事业计划共同支持：

- 地下水研究与信息传播；
- 井、泉及硝酸性氮等监测；
- 地下水保全条例、流域协议会和学术部会倡议；
- 向市政府提出意见、请愿及取得正式回应。

### 辅助建议

**AI223=`organizational_positioning`。**

安全范围：

> `groundwater` 是 A112 自 2018 年设立以来的核心组织议题和持续工作对象。

限制：

- 不把组织提出的污染风险写成已证事实；
- 市政府回答只证明行政往来，不证明市方接受组织解释；
- 具体领导、项目与行动仍按年份记录。

建议 review notes：`core_groundwater_research_monitoring_and_policy_advocacy_since_2018;no_scientific_causality_inference`。

## 3. AI225 · A112—life_safety

官网持续把地下水描述为宫古岛唯一饮用水源及“命之水”；其行动包括水源保护、断水／污染预防、高度净水设施请愿及面向居民和学生的学习活动。`life_safety` 因此不是单次请愿附带标签。

### 辅助建议

**AI225=`organizational_positioning`。**

安全范围：

> `life_safety` 表示 A112 持续从饮用水源、供水连续性和风险预防角度讨论地下水保护。

限制：

- 不推断已有特定居民健康损害；
- 不把“健康影响担忧”强化为医学因果；
- 与 AI223、AI226 属同一地下水工作链，分析时不得算作三次独立桥接。

建议 review notes：`sustained_drinking_water_source_and_preventive_life_safety_frame;overlaps_groundwater_environment`。

## 4. AI226 · A112—environment

A112 的设立与持续计划包括地下水污染预防、井泉调查、农药检测、保全条例修改、森林／水循环及珊瑚礁环境关切。这些内容跨年度存在，超过单一行动。

### 辅助建议

**AI226=`organizational_positioning`。**

安全范围：

> `environment` 表示 A112 围绕地下水保全及其生态环境条件开展持续研究和公共政策倡议。

限制：

- 不由一般环境 edge 自动生成反军事定位；
- 自卫队设施排水仅可写为该会提出的风险类别；
- 不推断污染来源或政策效果。

建议 review notes：`sustained_groundwater_conservation_environmental_function;SDF_risk_is_group_position_not_proven_contamination`。

## 5. AI231 · A113 宜野湾ちゅら水会—legal

### 正式程序链

1. 2022 年向宜野湾市议会提出 PFAS 血液浓度检查等请愿；市议会官网截至 2026-03-27 仍标记为“审查中”。
2. 2025-10-27，A113 与另外两个团体向沖縄県公害審査会提出公害调停申请。
3. 2026-02，申请因公害纷争处理法排除“防卫设施”事项而被驳回。

该链是明确的程序角色，不是 A113 作为律师、诉讼代理或一般法律研究组织的长期身份。程序驳回也不是对 PFAS 污染来源、健康影响或政策主张实体内容作出否定判断。

### 辅助建议

**AI231=`institutional_or_case_role`。**

安全范围：

> `legal` 表示 A113 作为请愿人／公害调停申请团体进入具名行政与准司法程序。

限制：

- 2022 请愿写作“审查中”，不得写已通过或已拒绝；
- 2025 调停申请与 2026 程序驳回必须同时记录；
- 不写成实体争议败诉；
- 三团体共同申请不生成稳定联盟。

建议 review notes：`named_petitioner_and_pollution_mediation_applicant;2022_petition_pending_as_of_2026-03-27;2025_application_procedurally_rejected_2026-02_not_merits_ruling`。

### 来源修复

当前 AI231 的 S273/S274 只能支持 2022 请愿／意见书，不能支持 relation basis 中的 pollution mediation。合并前须提出并归档：

- 2025-10-27 调停申请来源；
- 2026-02 驳回及其程序理由来源。

## 6. AI232 · A114 全日本港湾労働組合沖縄地方本部—anti_base

分支级材料显示：

- 2015 年沖縄地本组织反安保法案／边野古新基地集会；
- 2025 年沖縄地本报告称在普天间基地路线诉说过重基地负担；
- 2026 年沖縄地本报告明确记录“基地ない沖縄”目标。

因此它已经超过孤立事件，但时间范围应写作目前可证的 2015–2026，而不是工会成立以来永久不变。

### 辅助建议

**AI232=`organizational_positioning`。**

安全范围：

> `anti_base` 表示 A114 在可核分支级行动中持续反对边野古新基地、过重基地负担并参加“基地ない沖縄”行动。

限制：

- 不泛化为反对全部军事设施或全部工会成员完全一致；
- 2025／2026个人署名报告是分支活动报告，不单独证明全员立场；
- 行进共同参与不生成联盟。

建议 review notes：`recurrent_branch_level_anti_Henoko_and_base_burden_positioning_2015_2026;not_every_member_or_every_base`。

## 7. AI233 · A114—anti_military

本 edge 的直接支撑不是抽象反军事思想，而是港湾劳动场域：

- 2024-03 反对美海军军舰使用石垣民港并实际实施罢工；
- 2024-10 反对 Keen Sword 25 使用沖縄民用港，提出“不让港口军事利用”；
- 工会将上述行动与港湾劳动者职场安全相连接。

### 辅助建议

**AI233=`organizational_positioning`，但必须窄化为港湾／职场军事利用。**

安全范围：

> `anti_military` 表示 A114 重复反对军舰、日美演习及其他军事活动使用民用港，并以劳动者职域安全说明其角色。

限制：

- 不写成一般性反对所有自卫队／美军存在；
- 不裁判罢工合法性；
- 不推断港湾抗议阻止了军舰寄港或改变政策。

建议 review notes：`recurrent_opposition_to_military_use_of_civilian_ports_and_exercises;workplace_safety_frame;no_legality_or_effect_finding`。

## 8. AI234 · A114—peace

除 2015 年行动外，全港湾官网已有 2024、2025、2026 连续沖縄和平行进记录；2025 沖縄地本报告把它称为每年活动，并将基地负担与和平教育相连。

### 辅助建议

**AI234=`organizational_positioning`。**

安全范围：

> `peace` 表示 A114 持续参加并组织性承接沖縄和平行进、基地负担学习及反战和平传播。

限制：

- 不由参加和平行进推断与全部参会组织形成联盟；
- 不把个人参加感想当作全体成员政策表决；
- 与 AI232、AI233、AI236 高度重叠，网络指标中需去重复权。

建议 review notes：`recurrent_branch_peace_march_and_peace_learning_activity;do_not_infer_alliance_or_member_unanimity`。

## 9. AI236 · A114—mobilization

A114 可核 repertoire 包括：

- 2015 集会；
- 2024 罢工；
- 2024 港湾抗议；
- 2024–2026 和平行进。

这不是单次事件标签，而是重复出现的工会组织行动方式。`mobilization` 在此描述组织 repertoire／能力，不代表每次动员成功或具有同等政治意义。

### 辅助建议

**AI236=`organizational_positioning`。**

安全范围：

> `mobilization` 表示 A114 在多个时期使用集会、罢工、港湾抗议和行进等组织行动方式。

限制：

- 不由工会身份自动推定实际动员规模；
- 人数须保留主办方／媒体口径；
- 不推断行动效果、合法性或政治影响；
- 同一行动同时支撑多个 issue 时只计一个 event／action unit。

建议 review notes：`recurrent_union_mobilization_repertoire_rally_strike_port_protest_march;no_effect_or_legality_inference`。

## 10. AI237 · A115 新日本婦人の会沖縄県本部—women

A115 是全国女性会员组织的沖縄県本部，县本部—市町村支部—班的组织结构及长期女性、生活、人权与和平活动支持 `women` 为核心组织属性，不是单次事件。

### 辅助建议

**AI237=`organizational_positioning`。**

安全范围：

> `women` 表示 A115 作为女性会员制组织的县级本部，开展女性生活、权利和公共议题活动。

限制：

- 全国中央本部行动不自动转嫁给县本部；
- 裸称“新婦人”不能无条件解析为 A115；
- 不因报道来源或议员同席推断政党隶属；
- 县本部与 A111 等女性组织的共同活动不生成稳定联盟。

建议 review notes：`core_prefectural_womens_membership_organization_function;preserve_national_prefectural_unit_boundary`。

## 11. AI240 · A115—anti_base

县本部自身或明确包含县本部的材料包括：

- 2008 年县本部就美海兵队员性暴力向县政府要请；
- 2015 年县本部成员参与边野古新基地反对行动；
- 2018 年县本部启动边野古县民投票条例署名；
- 2024 年中央＋县本部联合声明把性暴力、人权与基地负担相连接；
- 2026 年县本部作为具名赞同团体参加反对沖縄最前线化请愿。

这些材料支持有明确年份范围的持续定位。2026 赞同记录只能证明该次请愿赞同，不能单独证明联盟；本 edge 由多期县本部行动共同支撑。

### 辅助建议

**AI240=`organizational_positioning`。**

安全范围：

> `anti_base` 表示 A115 在多期县本部具名行动中反对边野古新基地、基地负担及基地相关人权侵害。

限制：

- 不把全国组织所有反基地声明转给县本部；
- 2024 行动写成“中央＋沖縄県本部联合”，不能改成县本部单独；
- 共同署名／共同活动不生成联盟；
- 不推断政策或选举效果。

建议 review notes：`recurrent_prefectural_headquarters_anti_Henoko_base_burden_and_base_related_rights_actions_2008_2026;national_actions_not_transferred`。

### 来源修复

- 当前 AI240 引用的 S254 是全国中央本部 2014 声明，不能直接承担 A115 县本部 edge，应移除或仅作中央背景。
- 保留 S281（中央＋县本部联合）和 S283（县本部2018行动）。
- 补入可明确指向县本部的 2008、2015及2026材料；联合／赞同关系保留各自边界。

## 12. 跨 edge 去重复与数据修复

若负责人确认：

1. A112 的 AI223、AI225、AI226 是同一地下水机制的三个观察维度；桥接分析不得按三条独立行动累计。
2. AI231 标为程序角色，并补 2025 申请与 2026 驳回来源；不得把驳回写成实体败诉。
3. A114 的 AI232、AI233、AI234、AI236 大量共享 2015／2024／2025–2026 行动：
   - actor–issue 图可保留四个维度；
   - event、mobilization 或 bridge 强度计算须按 action unit 去重复；
   - 所有罢工效果／合法性判断保持关闭。
4. AI240 移除全国中央声明 S254 作为县本部直接证据，改用县本部或明确联合材料。
5. 本轮新检索来源先进入 source proposal／归档队列，不在本报告内直接写入中央 source log。

本报告本身不修改中央表、source log、HR CSV 或图。

## 13. 负责人决定

负责人于 2026-07-20 确认本报告全部 10 条建议：

- `organizational_positioning`：AI223、AI225、AI226、AI232、AI233、AI234、AI236、AI237、AI240；
- `institutional_or_case_role`：AI231。

同时确认第 12 节的跨 edge 去重复和来源修复要求。中央 edge 表、source log、HR CSV 和图留待后续受控合并。
