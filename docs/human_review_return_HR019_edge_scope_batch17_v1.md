# HR-019 actor–issue edge 范围第七组回交报告 Batch 17

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**负责人已确认——10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 61–70 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 历史组织可以具有明确的 `organizational_positioning`，但必须同时标注可证活动期；历史定位不等于当前仍在活动。
- “后续公开记录中消失／未找到后续活动”不等于正式解散。只有明确解散、休止、改组或后继记录时才写相应生命周期状态。
- 临时组织若承担签名、条例直接请求、公投推动等多阶段正式程序，按 `institutional_or_case_role`，而不是把每一阶段拆成独立事件。
- 分会与国际母体、全国网络与成员团体、临时前身与后继组织均保持 actor 单元分离。
- 本报告不直接修改中央 edge 表、registry、生命周期表、source log、HR CSV 或图。

## 0A. 本轮调查与反向核查

| actor | 本轮核查材料 | 调查所得 |
|---|---|---|
| A064 No Bases Network | [2007 年 No Bases Bulletin](https://focusweb.org/no-bases-bulletin-no-3-january-2007/)、[TNI 建网回顾](https://www.tni.org/en/publication/foreign-military-bases-and-the-global-campaign-to-close-them)、[ISQ 网络形成研究](https://academic.oup.com/isq/article-pdf/53/3/571/5072601/53-3-571.pdf)、[2019 年学术回顾](https://www.journals.uchicago.edu/doi/full/10.1086/701042)、HR025 Batch 06 | 2007 年厄瓜多尔会议正式形成跨国反外国军事基地网络，并制定网站、研究、全球行动日和跨地区联络计划；冲绳代表／议题进入网络传播。但后续研究明确以该网络后来“消失”来回顾其作用，未见正式解散日或当前组织结构。 |
| A065 琉球弧（南西諸島）ピースネット | [组织自有网站](https://peacenet-nansei-islands.jimdofree.com/)、[2016 年宫古活动报道](https://iwj.co.jp/wj/open/archives/304004)、S036、HR019 bridge Batch 10、HR025 Batch 04 | 2016–2018 可证阶段持续反对南西诸岛自卫队／导弹部署，并把部署与岛屿前线化、台湾／区域冲突和居民生活风险连接；2019 年以后连续性仍未闭合。 |
| A067 辺野古土砂搬出反対全国連絡協議会 | [组织官网](https://dosyazenkyo.com/)、[2023 年会报](https://dosyazenkyo.com/news/No24.pdf)、[2024 年会报](https://www.dosyazenkyo.com/news/No27.pdf)、S040、HR019 bridge Batch 10 | 2015 年成立后持续至 2024–2026 可见材料；组织直接反对为边野古填海从各地搬出土砂，并长期处理外来物种、珊瑚／儒艮海域、生物多样性和土砂条例问题。中央 canonical name 的“搬入／全国協議会”需改为“搬出／全国連絡協議会”。 |
| A068 名護市民投票推進協議会 | [名护市官方时间线](https://www.city.nago.okinawa.jp/kurashi/2018071900226/)、[名护市公投资料页](https://www.city.nago.okinawa.jp/kurashi/2018071901216/)、[1997 公投推进协议会成员回顾](https://ryukyushimpo.jp/news/entry-825165.html)、HR019 bridge Batch 10 | 可靠名称是 `ヘリポート基地建設の是非を問う名護市民投票推進協議会`。它在 1997 年围绕海上直升机基地建设组织条例直接请求、签名和市民投票，之后发展性解散／改组并进入 A019 谱系；当前 registry 名 `名護市民投票の会` 未获来源支持。 |
| A069 沖縄ジュゴン環境アセスメント監視団 | [CiNii 组织出版记录](https://ci.nii.ac.jp/ncid/BB01359003)、[2012 年意见书材料](https://www.nacsj.or.jp/archives/files/katsudo/henoko/pdf/20121225henoko-ikensyosoufusyo.pdf)、S047、HR019 bridge Batch 10、HR025 Batch 04 | 2003–2012 至少可证：组织专门监督边野古替代设施环境评估，编印意见／资料集、提交意见、进入评估审查并处理儒艮、海草藻场和沿岸生态。S047 只能证明官方 EIA 程序，不能单独证明 A069。 |
| A070 VFP-ROCK | [VFP 2016 冲绳声明](https://www.veteransforpeace.org/files/9815/9967/2216/2016_Position_Statements_Complete_9.9.20.pdf)、[VFP 冲绳成员专题](https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism)、[VFP chapter 名录](https://www.veteransforpeace.org/files/2816/9832/3977/23.10.26.ChapterListingforWebsite.pdf)、[2016 地方报道](https://english.ryukyushimpo.jp/2016/06/14/25229/)、S048 | 可确认冲绳分会／国际 chapter 身份及跨期和平活动；2016 年分会自身声明直接反对驻军暴力并主张移除冲绳美军基地。应统一为 `Veterans For Peace Ryukyu/Okinawa Chapter Kokusai (VFP-ROCK)`，不把美国母体全部立场转给分会。 |

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI152 | A064—anti_base | `organizational_positioning` | 2007 年形成时的明确反外国军事基地宗旨；不写成当前仍活跃 |
| AI153 | A064—international_advocacy | `organizational_positioning` | 2007 年跨国会议、网络和全球行动计划；冲绳是倡议对象／参与来源，不是已证正式分支 |
| AI154 | A065—anti_military | `organizational_positioning` | 限于 2016–2018 可证的琉球弧／先岛反军事化网络定位 |
| AI160 | A067—anti_base | `organizational_positioning` | 2015 年以来持续反对边野古填海土砂搬出及新基地建设 |
| AI162 | A067—biodiversity | `organizational_positioning` | 持续处理外来种、搬出地自然环境与边野古海域生物多样性风险 |
| AI164 | A068—anti_base | `institutional_or_case_role` | 限于 1997 年海上直升机基地市民投票的直接请求／签名／公投程序；先修复 actor 名称和谱系 |
| AI166 | A069—dugong | `organizational_positioning` | 2003–2012 项目型 EIA 监督中的核心物种／调查定位 |
| AI167 | A069—biodiversity | `organizational_positioning` | 同期环境评估、藻场及沿岸生态监督；不外推 2013 年后连续性 |
| AI169 | A070—peace | `organizational_positioning` | Ryukyu/Okinawa chapter 的退伍军人和平行动定位 |
| AI170 | A070—anti_base | `organizational_positioning` | 分会自身材料支持冲绳反基地立场；不转移美国母体全部行动 |

建议分布：

- `organizational_positioning`：9 条；
- `institutional_or_case_role`：1 条；
- `event_specific`：0 条；
- `remain_unclear`：0 条。

## 2. AI152／AI153 · A064 No Bases Network—anti_base／international_advocacy

### 组织与生命周期判断

S033 只是 2006 年背景性学术资料，不能承担 2007 年网络成立和连续性证明。补查材料可以确认：

- 2007 年 3 月在 Quito／Manta 召开的国际会议正式形成 `International Network for the Abolition of Foreign Military Bases`；
- 网络宗旨直接是反对／撤除外国军事基地；
- 会议规划了网站、共同研究、全球行动日及向各地反基地运动扩展联络；
- 冲绳的新基地建设和军事同盟重组进入其问题清单；
- 冲绳／日本代表参加网络形成和会议传播，网络发言也公开声援冲绳反基地斗争。

因此 A064 不是仅由一次会议标题误生成的 actor，两条 issue 都属于成立宗旨。

但 2019 年学术回顾已经用该网络后来的“disappearance”讨论其影响；本轮没有找到正式解散公告、当前组织名录或持续官网。安全做法是把 A064 当作 2007 年前后可证的历史跨国网络，而不是当前活跃国际组织。

### 辅助建议

**AI152=`organizational_positioning`。**  
**AI153=`organizational_positioning`。**

AI152 安全范围：

> A064 于 2007 年形成时，以撤除外国军事基地、反对基地扩张和军事化为明确网络宗旨。

AI153 安全范围：

> A064 通过国际会议、共同研究与全球行动计划，把不同地区反基地运动带入跨国倡议渠道，其中包括冲绳议题和冲绳／日本参与者。

限制：

- 时间写为“2007 年形成及其后可证活动期”，不写成 2026 年当前网络；
- 学术文献中的“disappearance”可支持 `continuity_unverified`／“后续公开记录中消失”，但不能改写为有正式日期的 `dissolved`；
- 冲绳是倡议对象并有代表参与，不是已证制度化 `Okinawa node`；
- 共同会议和国际声援不生成 A064 与冲绳组织的稳定联盟；
- 不把网络倡议归因为基地关闭或政策变化。

建议 review notes：

- AI152：`historical_2007_network_foundational_anti_foreign_base_positioning;later_public_continuity_unverified_not_formally_dissolved`；
- AI153：`historical_transnational_conference_research_and_global_action_advocacy;Okinawa_target_and_participation_not_formal_branch`。

## 3. AI154 · A065 琉球弧（南西諸島）ピースネット—anti_military

S036 可证明该网络参加一次政府交涉，但单独不足以证明长期定位。组织自有网站及 2016–2018 活动记录补足：

- 公开反对在与那国、宫古、石垣、奄美和冲绳岛推进自卫队／导弹部署；
- 通过跨岛信息交流和代表讲演讨论军事要塞化；
- 把部署与岛屿前线化、台湾／区域冲突、避难和居民生活风险连接；
- A065 的三个 issue `anti_military`、`frontline_prevention`、`Taiwan_contingency` 是同一反前线化框架，不是三个独立行动领域。

HR019 bridge Batch 10 已把可证活动期限定为 2016–2018；生命周期表也只记录 `last_observed_activity_only`，没有解散或休止证据。

### 辅助建议

**AI154=`organizational_positioning`，限于 2016–2018 可证阶段。**

安全范围：

> A065 在 2016–2018 可证活动中持续反对琉球弧／南西诸岛的自卫队和导弹部署，并以岛屿前线化及居民生活风险解释该立场。

限制：

- 不外推 2019–2026 仍持续活动；
- 不把“未找到后续材料”写成解散或休止；
- 不推断 A065 代表所有相关岛屿居民；
- S036 中并列交涉的地方团体保持独立，不自动成为成员或分支；
- 不把组织风险主张写成战争必然发生或岛屿必然成为攻击目标。

建议 review notes：`2016_2018_observed_cross_island_anti_JSDF_and_missile_deployment_positioning;continuity_after_2018_unverified`。

## 4. AI160／AI162 · A067 辺野古土砂搬出反対全国連絡協議会—anti_base／biodiversity

### 身份修复

中央 registry 当前名称：

`辺野古土砂搬入反対全国協議会（辺野古土砂全協）`

组织正式自称：

`辺野古土砂搬出反対全国連絡協議会`

这不是纯粹字形问题：“搬出”强调奄美／西日本等土砂来源地的行动结构，“全国連絡協議会”是正式组织名。后续合并须同步修正 canonical name。

### 两条 edge 的连续性

官网、规约和 2016–2024 会报显示：

- 2015 年由多个土砂搬出地团体发足；
- 持续反对以各地土砂填埋边野古、建设新基地；
- 反复向防卫省、环境省及地方议会提出请求／意见；
- 将土砂搬出与来源地环境破坏、外来生物进入冲绳、珊瑚／儒艮海域和固有生态系统风险连接；
- 2023–2024 仍直接参与国家生物多样性战略和冲绳土砂条例相关倡议。

这两条都是成立后持续组织定位，不是一份声明的附带标签。

### 辅助建议

**AI160=`organizational_positioning`。**  
**AI162=`organizational_positioning`。**

AI160 安全范围：

> A067 持续反对从各地搬出土砂用于边野古新基地填海，并组织跨县联络、请求和宣传。

AI162 安全范围：

> A067 持续把土砂搬出／运输与来源地自然环境、外来物种及边野古海域生物多样性风险连接。

限制：

- 风险按组织材料和公开请求记录，不断言所有预测破坏均已发生；
- 官网成员／构成团体关系不等于成员彼此形成一般性稳定联盟；
- 全国网络活动不能全部归给任何单一成员；
- 两条 issue 经常来自同一土砂行动链，分析时避免重复计数；
- canonical name 修复不自动批准 F018 或其他 actor–actor 关系。

建议 review notes：

- AI160：`sustained_2015_onward_opposition_to_Henoko_fill_soil_export_and_new_base_construction;canonical_name_repair_required`；
- AI162：`sustained_soil_source_environment_invasive_species_and_Henoko_marine_biodiversity_frame;risks_not_proven_outcomes`。

## 5. AI164 · A068 名護市民投票推進協議会—anti_base

### 为什么不是当前组织定位

1997 年的程序事实充分：

- `ヘリポート基地建設の是非を問う名護市民投票推進協議会` 于 1997 年 6 月形成；
- 组织条例制定直接请求和签名；
- 推动名护市就海上直升机基地建设举行市民投票；
- 推进协议会本身采取反对基地建设立场；
- 在投票前后发生发展性解散／改组，后续组织进入 A019 谱系。

但中央 registry 的 `名護市民投票の会` 不是可靠史料中的正式名称，且不能把 A068 写成从 1997 年持续至今的反基地团体。

AI164 不是一次普通抗议的 `event_specific`，因为它覆盖直接请求、签名、议会条例与公投推动等多阶段制度过程；最合适的是有边界的程序角色。

### 辅助建议

**AI164=`institutional_or_case_role`。**

安全范围：

> `anti_base` 表示正式名称待修复的 A068 在 1997 年名护海上直升机基地市民投票过程中，以反对基地建设立场承担条例直接请求、签名和公投推动角色。

限制：

- 合并前先将 canonical name 修复为 `名護市民投票推進協議会`／资料所示全称；
- 活动期限定为 1997 年，不能写成当前组织；
- A068→A019 是前身／发展性改组候选关系，不把两者直接合并；
- 公投反对票多数不等于组织造成投票结果；
- 不从程序角色推断基地工程、政府政策或后续选举效果；
- AI163 `referendum` 与 AI164 `anti_base` 描述同一程序链，不算两次组织行动。

建议 review notes：`bounded_1997_Nago_heliport_referendum_direct_request_signature_and_campaign_role;identity_genealogy_repair_before_activation`。

## 6. AI166／AI167 · A069 沖縄ジュゴン環境アセスメント監視団—dugong／biodiversity

S047 是冲绳防卫局官方 EIA 索引，只证明项目和行政程序存在，不能单独证明 A069。独立材料显示：

- A069 于 2003 年组成，目的就是监督边野古替代设施环境影响评价；
- 2007 年以组织名义编印 701 页方法书意见／资料集；
- 2007–2012 持续提交意见、陈情、参加审查相关活动并整理专家／市民意见；
- 议题直接包括儒艮、海草藻场、海域调查方法和边野古—大浦湾沿岸生态；
- 当前没有足够证据把组织连续性外推到 2013 年以后。

尽管这些行动发生在一个特定 EIA 项目中，`dugong` 和 `biodiversity` 是组织名称、成立目的和多年工作中的实体议题，而不是只在某次听证中承担的外部角色。因此 edge scope 以有时间界限的组织定位更准确；其 EIA 程序渠道另由法律／程序观察记录。

### 辅助建议

**AI166=`organizational_positioning`。**  
**AI167=`organizational_positioning`。**

AI166 安全范围：

> A069 在 2003–2012 可证阶段持续以边野古环境评估中的儒艮调查、栖息地和评价方法为核心工作。

AI167 安全范围：

> A069 同期持续处理海草藻场、沿岸生态、调查范围及环境评估完整性等生物多样性问题。

限制：

- 不外推 2013 年后仍活动，也不因无后续材料写成已解散；
- 组织意见不等于行政机关或法院采纳其全部评估判断；
- `dugong` 与 `biodiversity` 属同一 EIA 生态链，不作为两个独立运动领域加权；
- S047 继续只作官方项目／程序侧来源，须由具名 A069 材料补强；
- 与其他组织共同提交意见不生成稳定联盟。

建议 review notes：

- AI166：`2003_2012_group_mission_and_recurrent_Henoko_EIA_dugong_monitoring;post_2012_continuity_unverified`；
- AI167：`2003_2012_recurrent_seagrass_coastal_ecology_and_EIA_biodiversity_monitoring;same_project_chain`。

## 7. AI169／AI170 · A070 VFP-ROCK—peace／anti_base

### 分会身份修复

公开材料支持的精确名称包括：

- `Veterans For Peace Ryukyu/Okinawa Chapter Kokusai`
- `VFP-ROCK`
- `Veterans for Peace, Ryukyu/Okinawa (VFP ROC)`
- `Chapter 1003 - Ryukyu Okinawa`

`Veterans for Peace Okinawa` 应只作简略 alias。VFP 官方 chapter 名录、2016 声明、2021 分会协调者专题和后续决议共同支持冲绳分会身份。

### 两条 edge 的直接性

- `peace`：分会由退伍军人和平行动者组成，持续以反战争、反军事化、退伍军人证言和冲绳和平活动为公开功能；
- `anti_base`：2016 年 VFP ROC 自身声明及地方报道直接把驻军暴力与冲绳美军基地结构连接，并提出移除基地；后续材料继续反对冲绳军事扩张。

这超过母体的一次决议或一份共同声明，可以支持分会层面的持续定位。

### 辅助建议

**AI169=`organizational_positioning`。**  
**AI170=`organizational_positioning`。**

AI169 安全范围：

> A070 作为 VFP 的 Ryukyu/Okinawa 国际 chapter，持续以退伍军人和平行动、反战争和反军事化倡议为组织定位。

AI170 安全范围：

> A070 的分会自身声明与公开活动支持其反对冲绳美军基地暴力、基地继续存在及军事扩张的定位。

限制：

- 不把 VFP 美国母体的全部决议、成员或行动自动转给 A070；
- 分会／母体 affiliation 不等于 A070 与其他签署者形成稳定联盟；
- 不从退伍军人身份推断代表全部美国退伍军人或在冲绳美军人员；
- 声明／抗议不证明政策变化或基地撤除效果；
- 两条 edge 常属于同一和平—反基地行动链，分析时避免重复计数。

建议 review notes：

- AI169：`Ryukyu_Okinawa_chapter_sustained_veterans_peace_antiwar_and_demilitarization_positioning;parent_chapter_boundary`；
- AI170：`chapter_attributed_Okinawa_US_base_removal_and_anti_military_expansion_positioning;not_parentwide_or_outcome_claim`。

## 8. 如负责人确认，本批后续动作

1. AI152／AI153 作为 2007 年前后历史组织定位保留；A064 生命周期只记后续连续性未证／公开记录中消失，不写正式解散。
2. AI154 限定 2016–2018 可证活动期，不外推当前持续性。
3. AI160／AI162 同步修正 A067 canonical name 为 `辺野古土砂搬出反対全国連絡協議会`；名称修复不批准 actor–actor 关系。
4. AI164 作为 1997 名护公投程序角色；先修复 A068 名称、生命周期及 A068→A019 谱系，再进入可发布层。
5. AI166／AI167 限于 2003–2012；S047 只作官方 EIA 背景，补入具名 A069 来源。
6. AI169／AI170 使用 VFP-ROCK 精确 chapter 名和别名；保持母体／分会边界。
7. 同一行动链中的多 issue 不重复计为独立行动，也不生成稳定联盟。
8. 所有新增 URL 先进入 source proposal；来源入表不自动批准 actor、关系、因果或政策效果。
9. 本报告本身不修改中央 edge 表、registry、生命周期表、source log、HR CSV 或图，留待 HR019 全批完成后统一合并。

## 9. 负责人确认记录

负责人于 2026-07-20 确认本批全部辅助建议：

- AI152 A064 No Bases Network—`anti_base`：`organizational_positioning`，历史时间边界；
- AI153 A064—`international_advocacy`：`organizational_positioning`，历史时间边界；
- AI154 A065 琉球弧（南西諸島）ピースネット—`anti_military`：`organizational_positioning`，限 2016–2018；
- AI160 A067 辺野古土砂搬出反対全国連絡協議会—`anti_base`：`organizational_positioning`；
- AI162 A067—`biodiversity`：`organizational_positioning`；
- AI164 A068 名護市民投票推進協議会—`anti_base`：`institutional_or_case_role`，限 1997 公投程序且先修复身份／谱系；
- AI166 A069 沖縄ジュゴン環境アセスメント監視団—`dugong`：`organizational_positioning`，限 2003–2012；
- AI167 A069—`biodiversity`：`organizational_positioning`，限 2003–2012；
- AI169 A070 VFP-ROCK—`peace`：`organizational_positioning`；
- AI170 A070—`anti_base`：`organizational_positioning`。

负责人同时确认：

- A064 作为历史网络记录成立期组织定位，但不写成当前活跃或有正式日期的解散组织；
- A065 与 A069 分别保持 2016–2018、2003–2012 的可证时间边界；
- A067 合并时修正 canonical name，名称修复不批准任何 actor–actor 关系；
- A068 先修复正式名称、生命周期和 A068→A019 谱系，再激活 1997 公投程序 edge；
- A070 使用 VFP-ROCK 精确 chapter 名，并保持美国母体／冲绳分会边界。

本报告作为 10 条人工决定的回交记录；中央 edge 表、registry、生命周期表、HR CSV、source log 与图表仍留待主线程统一合并。
