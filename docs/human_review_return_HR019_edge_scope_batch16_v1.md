# HR-019 actor–issue edge 范围第六组回交报告 Batch 16

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**负责人已确认——10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 51–60 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 本批特别区分：
  - 组织的长期议题定位；
  - 受政府／国际合作机构委托的制度角色；
  - 与该组织并不相符或定义过宽的 issue 标签；
  - 同一运动中冲绳本体与关东 block 的不同组织单元。
- `human_rights` 不自动推出 `life_safety`；后者须直接涉及日常安全、事故、噪音、撤离、风险或成为攻击目标等内容。
- 环境组织刊物收录作者文章不等于每一篇文章都是组织决议；长期定位须由多期材料、组织自有声明、总会／活动记录或可交叉的具名行动共同支持。
- “全县 umbrella”“关东声援”“共同请求”均不生成稳定联盟边，也不表示代表全部居民。
- 本报告不直接修改中央 edge 表、source log、HR CSV、taxonomy 或图。

## 0A. 本轮调查与反向核查

| actor | 本轮核查材料 | 调查所得 |
|---|---|---|
| X010 沖縄NGOセンター | [ONC NGO相談員页](https://www.oki-ngo.org/project/ngo-support)、[ONC 开发教育页](https://www.oki-ngo.org/project/development-education)、S095、S096、S099–S101、HR-018-01–07 | ONC 的外务省 NGO 相談員与 JICA 开发教育是可验证的委托／指定角色，但准确落在 `international_cooperation` 与行政协作；当前 I013 定义偏向使领馆、交流、奖学金、青年领导力及联盟传播，不能仅因“面向公众的国际合作教育”就称为 `public_diplomacy`。 |
| A048 沖縄一坪反戦地主会 | S038、HR019 bridge Batch 08、HR025 Batch 05、此前 AI116 审核 | S038 实际是东京的 A063 `沖縄・一坪反戦地主会関東ブロック` 网站。它可支持关东 block，不能直接替冲绳本体 A048 证明 `local_autonomy`。本轮没有找到能够闭合 A048 组织身份与自治主张的直接材料。 |
| A054 沖縄人権協会 | [2019 年第 56 回总会报道](https://www.okinawatimes.co.jp/articles/-/507715)、S033、HR025 Batch 07 | 可确认 1961–2019 的协会历史、2019 年总会和一般人权／反战定位；没有直接材料把 A054 连接到 I007 所定义的日常安全、事故、撤离、噪音或目标化风险。2020–2026 连续性也未闭合。 |
| A055 泡瀬干潟を守る連絡会 | [冲绳县地域环境中心组织页](https://kankyo-center.okinawa/environmental-organization-facility/%E6%B3%A1%E7%80%AC%E5%B9%B2%E6%BD%9F%E3%82%92%E5%AE%88%E3%82%8B%E9%80%A3%E7%B5%A1%E4%BC%9A)、[NACS-J 2016 保护奖记录](https://award.nacsj.or.jp/result/result2016)、[湿地 Green Wave 2024](https://www.ramnet-j.org/gw/group2024/gr24-370.html)、S030 | 2001 年成立后持续进行潮间带调查、自然观察／导览、宣传、行政请求和拉姆萨尔湿地登记倡议。S030 只是一宗诉讼结果新闻，单独不足以证明长期生物多样性定位，但补查材料可以。 |
| A056 沖縄環境ネットワーク | [官方通信档案（创刊准备号至 104 号）](https://oki-kan.net/tsushin/)、[日本自然保护协会共同请求](https://www.nacsj.or.jp/statement/50880/)、HR025 Batch 07 | 官方档案跨约 24 年，反复出现边野古／大浦湾环境评估、基地污染、高江、宫古自卫队部署及先岛军事设施环境问题；2020 年还有网络自身针对边野古设计变更申请的意见。支持有环境边界的持续基地批评，但不能把每篇署名文章自动写成全组织决议。 |
| A059 島ぐるみ会議 | S029、[国会记录中的国连倡议说明](https://www.shugiin.go.jp/internet/itdb_kaigirokua.nsf/html/kaigirokua/000518920150522012.htm)、[国立国会图书馆团体典据](https://id.ndl.go.jp/auth/ndlna/001186459)、HR019 bridge Batch 10、HR025 Batch 05 | 正式名称为 `沖縄「建白書」を実現し未来を拓く島ぐるみ会議`。其跨阶段活动直接连接《建白书》、边野古新基地反对、地方尊严／自决表达和全县动员；但市町村“岛ぐるみ会議”不能全部并入 A059。 |
| A060 高江のヘリパッドいらない住民の会 | S028、[2016 年向环境省请求](https://ryukyushimpo.jp/news/entry-259228.html)、HR025 Batch 05 | 至少从 2007 年起持续反对高江直升机坪；2016 年具名请求又明确要求优先返还北部训练场、制定生物多样性行动计划并调查动植物、自然环境和噪音对生态系统的影响。反直升机坪与やんばる生物多样性均有直接组织材料。 |
| A063 一坪反戦地主会関東ブロック | [组织首页](https://www.jca.apc.org/HHK/index.html)、[活动档案](https://www.jca.apc.org/HHK/Meetings/index.html)、[关东 block 总会报告](https://www.jca.apc.org/HHK/Tsushin/164/164-sokai1.html)、S038 | 网站明确自称 `沖縄・一坪反戦地主会関東ブロック`，以首都圈为组织基础，长期开展反军用地强制使用、边野古新基地反对及面向冲绳反基地运动的声援。它是日本本土／关东 actor，不是 A048 的同一 registry 单元。 |

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI063 | X010—public_diplomacy | `remain_unclear` | ONC 的正式角色属于国际合作／开发教育和行政协作；当前 I013 定义不宜被“相邻性”扩张，AI062 已承载准确的 I015 角色 |
| AI118 | A048—local_autonomy | `remain_unclear` | S038 属 A063 关东 block，不能移作 A048 直接证据；等待具名 A048 的自治／土地权材料 |
| AI134 | A054—life_safety | `remain_unclear` | 一般人权与反战材料不等于 I007；建议从可发布层停用 |
| AI135 | A055—biodiversity | `organizational_positioning` | 2001–2024 持续的潮间带调查、导览、保护和拉姆萨尔倡议 |
| AI138 | A056—anti_base | `organizational_positioning` | 长期从环境评估、污染、生物多样性等角度批评具体基地建设／军事设施 |
| AI143 | A059—anti_base | `organizational_positioning` | 《建白书》与边野古新基地反对是全县组织的持续主轴 |
| AI145 | A059—local_autonomy | `organizational_positioning` | 限于地方尊严、自决权及“冲绳事务由冲绳决定”的组织框架 |
| AI146 | A060—anti_base | `organizational_positioning` | 2007–2016 可见期内持续反对高江直升机坪建设 |
| AI147 | A060—biodiversity | `organizational_positioning` | 具名请求直接涉及やんばる动植物、生态调查和生物多样性保护 |
| AI150 | A063—anti_base | `organizational_positioning` | 关东／首都圈层面的长期反基地与冲绳声援；不是冲绳本地组织 |

建议分布：

- `organizational_positioning`：7 条；
- `institutional_or_case_role`：0 条；
- `event_specific`：0 条；
- `remain_unclear`：3 条。

## 2. AI063 · X010 沖縄NGOセンター—public_diplomacy

### 可确认的制度事实

直接材料支持：

- ONC 受外务省委托担任 NGO 相談員，提供 ODA、国际志愿、NGO 运营及国际合作咨询／出张服务；
- ONC 承担 JICA 冲绳的开发教育、教师研修及教育成果回流工作；
- FY2024 法定事业报告和 FY2025／2026 外务省名单支持相关角色的连续性；
- HR-018-01–07 正在逐项审核委托、指定角色、期间及金额语义。

这些事实足以支持 AI062 `X010—I015 international_cooperation` 的 `institutional_or_case_role`，也可支持行政协作层的候选关系。

### 为什么仍不能直接保留 AI063

I013 当前定义是：

> U.S. consulate, exchange, scholarship, youth leadership, alliance-related outreach

ONC 材料所示的是国际合作 NGO 支援、ODA 咨询和开发教育。两者可能在广义“政府对外／公众传播”概念上相邻，但当前项目 taxonomy 没有把所有外务省／JICA 国内公众教育都定义为 `public_diplomacy`。

若仅因委托方是外务省或 JICA 就保留 I013，会产生三个问题：

1. 将国际合作／开发教育误写为外交倡议；
2. 与 AI062 重复计算同一制度角色；
3. 把 `public_diplomacy` 从当前受控定义扩张成几乎所有政府关联国际交流。

### 辅助建议

**AI063=`remain_unclear`，并建议从当前可发布／制图层停用。**

安全处理：

> ONC 的外务省 NGO 相談員与 JICA 开发教育角色继续由 AI062 `international_cooperation` 和 HR-018 行政协作关系承载；不单列为 `public_diplomacy`。

重新激活路径：

- 若负责人以后决定扩写 I013 定义，须先改 taxonomy，再将 AI063 修订为 `institutional_or_case_role`；
- 或找到 ONC 直接承担对外国家形象、外交传播、使领馆交流、奖学金／青年领导力或联盟相关 outreach 的具名项目；
- HR-018 即使确认委托关系，也不会自动批准 I013 议题标签。

建议 review notes：`formal_MOFA_JICA_roles_support_I015_and_admin_collaboration_not_current_I013_definition;deactivate_duplicate_until_taxonomy_revision_or_direct_public_diplomacy_evidence`。

## 3. AI118 · A048 沖縄一坪反戦地主会—local_autonomy

### 组织单元错配

中央表当前把 S038 同时用于：

- A048 `沖縄一坪反戦地主会`；
- A063 `一坪反戦地主会関東ブロック`。

但 S038 的网站标题、地址、活动档案和自我介绍均指向：

> `沖縄・一坪反戦地主会関東ブロック`

网站中确有土地权、法治、地方自治破坏和冲绳基地问题材料，但这些材料至少首先属于 A063 的发布／整理体系，不能不经身份核对就转给 A048。

HR019 bridge Batch 08 已确认 A048 只保留为 `candidate_only`；HR025 Batch 05 也已明确 A048 与 A063 是不同 actor 层。此前 AI116 `A048—legal` 同样因该错配保持 `remain_unclear`。

### 辅助建议

**AI118=`remain_unclear`。**

当前可说：

> 一坪反战地主运动一般具有土地权、反基地与地方决定权含义，但现有 registry source 没有把该 `local_autonomy` 主张可靠归属到 A048 这一组织单元。

限制：

- 不把 A063 的组织网站转作 A048 的直接组织证据；
- 不因名称相近或运动谱系相关就合并两者；
- 不从反对军用地续租自动推出受控的 `local_autonomy` edge；
- 待补具名 A048 的声明、机关刊物、土地收用程序材料或独立组织史后重审。

建议 review notes：`S038_is_A063_Kanto_block_site_not_direct_A048_evidence;local_autonomy_attribution_requires_actor_unit_repair_and_direct_A048_source`。

## 4. AI134 · A054 沖縄人権協会—life_safety

2019 年报道可以确认：

- A054 举行第 56 回定期总会；
- 选出新理事长；
- 报道标题与组织发言支持一般人权保护及反战延续。

HR025 Batch 07 已把 A054 的可验证活动期保守限定在 1961–2019，并指出现有材料不能证明 2020–2026 活动连续性；S033 只是 2006 年学术二手资料，不能承担当前组织状态。

更关键的是，I007 定义为：

> Daily safety, evacuation, risk, noise, accident, targetization concerns

“人权组织”“保护人权”或“反战”都不能单独证明 A054 曾持续处理这些生活安全内容。本轮也没有找到 A054 具名的事故、噪音、撤离、基地周边日常风险或成为攻击目标的材料。

### 辅助建议

**AI134=`remain_unclear`，并建议从当前可发布／制图层停用。**

限制：

- 不用 `human_rights` 替代 `life_safety`；
- 不用一般冲绳基地安全背景替代 A054 具名主张；
- 2019 总会材料可保留用于身份／人权／反战核查，但不能支持 AI134；
- 若以后找到具名生活安全行动，只按材料所示时期和对象恢复。

建议 review notes：`general_human_rights_and_antiwar_material_does_not_support_I007_daily_safety_definition;deactivate_until_direct_A054_risk_noise_accident_or_evacuation_evidence`。

## 5. AI135 · A055 泡瀬干潟を守る連絡会—biodiversity

S030 记录的是第二次泡濑干潟填海诉讼的那霸地院判决。它可以参与证明法律／案件背景，但单独不能把 A055 的长期生物多样性工作讲完整。

补查材料形成跨时期链：

- 冲绳县地域环境中心记载该会 2001 年成立，并开展泡濑干潟生物调查、自然观察／导览、宣传和行政请求；
- 日本自然保护协会的保护奖记录确认其长期保全工作；
- 2024 年湿地 Green Wave 仍具名该会，目标包括泡濑干潟的拉姆萨尔条约湿地登记；
- 这些行动围绕潮间带、鸟类／海洋生物、生境和湿地保全，直接落入 I005。

### 辅助建议

**AI135=`organizational_positioning`。**

安全范围：

> `biodiversity` 表示 A055 自 2001 年起持续围绕泡濑干潟开展生物调查、观察教育、湿地保护与拉姆萨尔登记倡议。

限制：

- 不把保护倡议写成拉姆萨尔登记已经实现；
- 不从组织调查直接确认填海导致的全部生态因果；
- 诉讼角色仍按 R8 人审结果：A055 是 case-specific supporter，不是组织原告或律师；
- S030 应由组织页、NACS-J 和 2024 记录补强，不再单独承担长期定位。

建议 review notes：`sustained_Awase_tidal_flat_biodiversity_surveys_guides_conservation_and_Ramsar_advocacy_2001_2024;no_registration_or_ecological_causality_claim`。

## 6. AI138 · A056 沖縄環境ネットワーク—anti_base

S033 是 2006 年学术二手资料，不能证明 A056 当前结构或直接的反基地定位。组织官方通信档案则提供了更强的跨期材料：

- 通信从创刊准备号延续至 104 号，100 号回顾约 24 年网络活动；
- 多期专题处理边野古／大浦湾环境评估、土砂投入、设计变更、儒艮影响及基地污染；
- 也处理高江、宫古自卫队部署、先岛军事设施与环境问题；
- 2020 年材料含网络自身对边野古设计变更申请的意见；
- 2024／2025 年仍有总会与基地环境议题记录。

这不只是一次共同署名，可以支持持续定位；但组织刊物中有不同作者／团体供稿，不能把所有文章都改写为 A056 的正式共同立场。

### 辅助建议

**AI138=`organizational_positioning`。**

安全范围：

> A056 长期从环境评估、基地污染、生物多样性与军事设施环境负荷角度，批评边野古、高江及先岛等具体基地建设／部署。

限制：

- `anti_base` 只按环境议题中的具体工程／设施反对或批评编码，不写成对所有基地议题的统一政治代表；
- 区分组织自有意见、总会活动和通信中的署名作者文章；
- 不把刊载文章自动生成作者／团体与 A056 的稳定联盟；
- S033 应退出主要支持位，改用官方通信及组织自有声明。

建议 review notes：`recurrent_environmental_assessment_pollution_and_biodiversity_critique_of_specific_base_projects;distinguish_network_statements_from_contributed_articles`。

## 7. AI143／AI145 · A059 島ぐるみ会議—anti_base／local_autonomy

### 名称与组织层级

A059 的 canonical name 应补全为：

> `沖縄「建白書」を実現し未来を拓く島ぐるみ会議`

`島ぐるみ会議` 可保留为 alias。公开材料同时存在名护、宜野湾、うるま等市町村级“岛ぐるみ”组织；它们不能只因名称相似就自动成为 A059 分会、成员或同一 actor。

### 两条议题的连续证据

S029 与补查材料显示，全县 A059：

- 以实现《建白书》要求为成立和行动主轴；
- 持续反对边野古新基地建设并组织现场／全县／本土及国际倡议；
- 在联合国倡议中提出自决权、土地权、环境权及表达自由等内容；
- 将基地强加与地方尊严、自治／自决和“冲绳的事情由冲绳决定”连接。

因此两条 edge 都超过一次活动，但它们高度相关，分析时不能当成两个互相独立的行动。

### 辅助建议

**AI143=`organizational_positioning`。**  
**AI145=`organizational_positioning`。**

AI143 安全范围：

> `anti_base` 表示全县 A059 持续以《建白书》要求和边野古新基地反对为组织主轴。

AI145 安全范围：

> `local_autonomy` 表示 A059 持续把基地强加问题表达为地方尊严、自决权、土地权和冲绳地方决定权问题。

共同限制：

- 不写成 A059 代表全体冲绳居民；
- 不与 `オール沖縄会議` 混同；
- 不把市町村岛ぐるみ组织的全部行动直接归给 A059；
- 联合国／访美活动只证明公开倡议渠道，不证明政策影响；
- 与其他组织共同活动不生成稳定联盟。

建议 review notes：

- AI143：`formal_A059_umbrella_sustained_Kenpakusho_and_Henoko_new_base_opposition;municipal_shimagurumi_not_auto_merged`；
- AI145：`sustained_local_dignity_self_determination_land_rights_and_Okinawa_decision_frame;not_all_resident_representation`。

## 8. AI146／AI147 · A060 高江のヘリパッドいらない住民の会—anti_base／biodiversity

S028 直接记录 2016 年高江直升机坪施工中的具名居民会抗议。县议会记录与补查材料又显示：

- 该会至少自 2007 年起围绕高江直升机坪持续行动；
- 组织名称存在 `高江のヘリパッドいらない住民の会`／`「ヘリパッドいらない」住民の会` 等格式差异，但现阶段可作为同一名称变体处理；
- 2016 年与另一现场组织向环境省具名请求，要求优先完成北部训练场返还；
- 请求直接包括生物多样性行动计划、动植物／自然环境调查、国立公园范围及噪音对生态系统影响。

这分别直接支持反直升机坪和やんばる生物多样性两条持续定位。

### 辅助建议

**AI146=`organizational_positioning`。**  
**AI147=`organizational_positioning`。**

AI146 安全范围：

> A060 在 2007–2016 可验证时期持续反对高江直升机坪建设，并要求优先处理北部训练场返还。

AI147 安全范围：

> A060 将高江直升机坪／北部训练场争议与やんばる动植物、生物多样性、自然环境调查及生态噪音影响连接。

限制：

- 当前材料支持的是至少 2007–2016 的可见连续性，不自动写成 2026 年仍活跃；
- 环境损害和噪音影响按组织请求／关切记录，不作为已完成科学因果鉴定；
- 不从组织名推断代表全部高江居民；
- 与现场行动联络会的共同请求不生成稳定联盟或组织合并；
- 两条 issue 常属于同一行动链，分析时避免重复计数。

建议 review notes：

- AI146：`sustained_Takae_helipad_opposition_2007_2016_observed_period;no_current_status_or_all_resident_claim`；
- AI147：`direct_Yanbaru_biodiversity_species_environmental_survey_and_ecosystem_noise_requests;group_claims_not_proven_damage`。

## 9. AI150 · A063 一坪反戦地主会関東ブロック—anti_base

S038 与组织网站明确显示：

- 正式名称应规范为 `沖縄・一坪反戦地主会関東ブロック`；
- 组织基础在东京／首都圈，成员包括居住首都圈的冲绳出身者和认同者；
- 长期支持反战地主、参加军用地公开审理、反对强制使用；
- 多期记录边野古新基地反对、首都圈集会、宣传和对冲绳行动的声援。

这足以支持持续反基地定位，也同时证明中央 registry 应把它与 A048 冲绳本体严格分开。

### 辅助建议

**AI150=`organizational_positioning`。**

安全范围：

> A063 是以东京／关东为活动基础的反战地主声援组织，长期开展反军用地强制使用、边野古新基地反对和面向冲绳反基地运动的首都圈行动。

限制：

- `origin_type` 继续是 `japan_domestic`，不得把它画成冲绳本地组织；
- “声援”不证明 A063 与 A048 或其他冲绳组织存在稳定联盟、隶属或持续协调；
- 不能把 A063 网站内容转作 A048 的直接证据；
- 公开审理、集会和边野古行动可共同支持定位，但不得把多种行动拆成未证的多条组织关系；
- canonical name 后续补 `沖縄・`，但本报告不直接改 registry。

建议 review notes：`long_running_Kanto_Tokyo_anti_base_land_use_and_Henoko_solidarity_positioning;mainland_actor_not_A048_or_Okinawa_local_alliance`。

## 10. 如负责人确认，本批后续动作

1. AI063 从可发布／制图层停用；ONC 的正式角色继续由 AI062 `international_cooperation` 和 HR-018 行政协作层承载。只有 taxonomy 明示扩写或补到直接公共外交项目时才重开。
2. AI118 保持 unclear，删除 S038 作为 A048 直接支持的错误用法；A048 与 A063 不合并。
3. AI134 从可发布／制图层停用；一般人权／反战材料不补足 `life_safety`。
4. AI135 用组织页、NACS-J 和 2024 湿地活动补强，S030 只保留为诉讼背景。
5. AI138 用 A056 官方通信与组织自有意见替换 S033 的主要支持地位，并在 notes 中区分组织声明与署名供稿。
6. AI143／AI145 使用 A059 正式全称；地方“岛ぐるみ”组织不自动并入全县 A059。
7. AI146／AI147 保留 2007–2016 可见期，不推断当前活动、全部居民代表性或已证环境损害。
8. AI150 使用 A063 正式名称与东京／关东活动边界；其材料不得转给 A048。
9. 所有新增 URL 先进入 source proposal；来源进入日志不自动批准 actor、关系、联盟、因果或政策效果。
10. 本报告本身不修改中央表、source log、HR CSV、taxonomy 或图，留待 HR019 全批完成后统一合并。

## 11. 负责人确认记录

负责人于 2026-07-20 确认本批全部辅助建议：

- AI063 X010 沖縄NGOセンター—`public_diplomacy`：`remain_unclear`，停用当前 I013 edge；准确制度角色由 I015／HR-018 承载；
- AI118 A048 沖縄一坪反戦地主会—`local_autonomy`：`remain_unclear`；
- AI134 A054 沖縄人権協会—`life_safety`：`remain_unclear`，从当前可发布／制图层停用；
- AI135 A055 泡瀬干潟を守る連絡会—`biodiversity`：`organizational_positioning`；
- AI138 A056 沖縄環境ネットワーク—`anti_base`：`organizational_positioning`；
- AI143 A059 沖縄「建白書」を実現し未来を拓く島ぐるみ会議—`anti_base`：`organizational_positioning`；
- AI145 A059—`local_autonomy`：`organizational_positioning`；
- AI146 A060 高江のヘリパッドいらない住民の会—`anti_base`：`organizational_positioning`；
- AI147 A060—`biodiversity`：`organizational_positioning`；
- AI150 A063 沖縄・一坪反戦地主会関東ブロック—`anti_base`：`organizational_positioning`。

负责人同时确认：

- ONC 的外务省／JICA正式制度角色不自动扩写为当前定义下的 `public_diplomacy`；
- S038 不得从 A063 关东 block 转作 A048 冲绳本体的直接证据；
- 一般 `human_rights`／反战材料不能替代 `life_safety`；
- A056 官方通信须区分组织自有意见与署名供稿；
- A059 与市町村岛ぐるみ组织、A063 与 A048 均保持组织单元分离。

本报告作为 10 条人工决定的回交记录；中央 edge 表、HR CSV、source log、taxonomy 与图表仍留待主线程统一合并。
