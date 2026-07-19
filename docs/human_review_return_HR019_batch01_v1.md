# HR-019 人工复核回交报告 Batch 01（分类规则 9 项）

日期：2026-07-19  
承办人：项目负责人  
辅助整理：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_review_v0.csv`  
状态：**已完成——9/9 规则决定及 2/2 实体范围判断完成**

## 0. 复核边界

- 本批只决定 `actor_class` 受控词、`review_status`／watchlist 分工和 R1 派生分析功能层。
- 本批不重新批准 actor 身份、issue edge、bridge、组织关系、政治立场或影响力。
- 现有来源与既往 HR 记录只用于理解分类对象，不因本批决定改变 evidence level 或关系状态。
- 所有最终决定必须由项目负责人明确作出；辅助建议不自动成为决定。
- 本报告不直接修改 HR CSV、中央 registry、schema 或图表，只生成供主线程合并的决定记录。

## 1. 决策顺序

| 小组 | 项目 | 原因 | 状态 |
|---|---|---|---|
| A | CLASS-02、CLASS-03、CLASS-01 | 先决定 `labor_union`／`labor_union_federation`，再处理混合词 `labor_or_education_union` | 已完成，3/3 |
| B | CLASS-04、CLASS-05、CLASS-06 | 分别处理媒体／倡议、女性／社区、女性／人权分类 | 已完成，3/3 |
| C | STATUS-X014、STATUS-X015、FAMILY-01 | 分开 review workflow、watchlist 和派生分析层 | 已完成，3/3 |

## 2. 小组 A：劳工词表

### HR019-CLASS-02 · `labor_union`

影响 actor：

- A093 全日本自治団体労働組合沖縄県本部；
- A114 全日本港湾労働組合沖縄地方本部。

现状：

- 两者 `legal_status_guess=labor_union`；
- A114 已经 HR-027 人工确认身份、持续性和组织边界；
- 当前 schema 建议词表没有独立的 `labor_union` actor class。

辅助建议：将 `labor_union` 加入受控词；它描述组织类型，不自动编码和平、反基地或其他政治立场。

负责人决定：**`approve_extension`——将 `labor_union` 加入 `actor_class` 受控词。**

负责人理由／限制：项目负责人认为组织类型应保持精简。`labor_union` 作为六个相关组织统一使用的组织类型；本决定不赋予任何议题、政治立场或关系。

### HR019-CLASS-03 · `labor_union_federation`

影响 actor：

- A091 日本労働組合総連合会沖縄県連合会（連合沖縄）；
- A092 沖縄県労働組合総連合。

现状：

- 两者 `legal_status_guess=labor_union_federation`；
- 该值可区分单一工会／地方本部与工会联合体；
- 两个 actor 的分类与议题边仍受外部 HR-010 约束，本批只决定术语是否允许。

辅助建议：将 `labor_union_federation` 加入受控词；不因联合体身份推定成员关系、代表范围或政治联盟。

负责人决定：**`map_to_existing`——不新增 `labor_union_federation` actor class，A091、A092 映射为 `labor_union`。**

负责人理由／限制：联合体结构继续保留在 `legal_status_guess=labor_union_federation` 或 notes，不在 `actor_class` 另增一类。

### HR019-CLASS-01 · `labor_or_education_union`

影响 actor：

- A089 沖縄県教職員組合；
- A090 沖縄県高等学校障害児学校教職員組合。

现状：

- 两者均为教职员工会，`legal_status_guess=labor_union`；
- `labor_or_education_union` 把组织类型（工会）与行业／议题领域（教育）合在同一字段；
- 如果 `labor_union` 获准，可将两者 actor class 归入 `labor_union`，把教育／和平教育保留在 issue 或 sector／notes 层。

辅助建议：不新增 `labor_or_education_union`；在 `labor_union` 获准的前提下映射为 `labor_union`。这不改变两者仍须 HR-010 完成分类和 edge 复核的状态。

负责人决定：**`map_to_existing`——不新增 `labor_or_education_union`，A089、A090 映射为 `labor_union`。**

负责人理由／限制：教育属于行业／议题属性，保留在 issue、sector 或 notes；不与组织类型混写。

## 3. 小组 B：媒体与女性组织词表

### HR019-CLASS-04 · `media_or_advocacy_actor`

影响 actor：A026 ピース・ニュース。

项目负责人要求先完成一次有界线上调查，再决定是否新增或映射该类型。调查结果如下：

- 组织自有说明明确写明，其先发行名为「ピース・ニュース」的 newsletter，随后团体本身也沿用该名称及简称 PN；因此名称来自刊物，但对象是团体，不只是刊物。
- 自有会则明确规定会名、会员、年会费、募款、官网、邮件新闻／机关报和 mailing list；自称以 fieldwork、学习会和反战和平行动为内容的“市民运动”。
- 2010 S003、2015 S004 和 2017 Greenpeace 联合声明均将其列为参与团体；这些只证明有界事件参加，不证明稳定联盟。
- 2019 明治学院大学国际和平研究所活动页以同一 `p-news@jca.apc.org` 邮箱列为联系入口；2020 冲绳集会材料将其列入执行委员会组成。
- 2026 年 note 活动公告继续使用同一邮箱，并以ピース・ニュース名义举办学习讨论活动，支持旧官网团体与当前账号的连续性。
- 未发现其为新闻企业、法人媒体或单纯出版物的证据；也未发现会改变上述同一性的近名冲突。英文世界同名刊物不应与本 actor 混同。

辅助建议：`map_to_existing`——A026 映射为现有 `citizen_group`，不新增 `media_or_advocacy_actor`。newsletter／机关报属于该团体的行动方式，放入 notes 或 action 字段；其日本国内来源、法律身份未解析和具体议题边分别保留在其他字段。

负责人决定：**`map_to_existing`——A026 映射为 `citizen_group`；不新增 `media_or_advocacy_actor`。**

负责人理由／限制：项目负责人要求先调查再判断，并于调查结果回交后确认该分类。newsletter／机关报只作行动方式；本项决定只处理 actor class，不得因身份闭合自动批准长期 anti-base 定位、地点边或稳定组织关系。

调查来源：

- ピース・ニュース自有说明与会则：`https://www.jca.apc.org/~p-news/about_PN.htm`
- 2010 S003、2015 S004 本地归档名单；
- Greenpeace Japan 2017-03-16 联合声明；
- 明治学院大学国际和平研究所 2019-07-14 活动页；
- 2020 沖縄のつどい材料；
- 2026 ピース・ニュース note 活动公告。

### HR019-CLASS-05 · `womens_or_community_organization`

影响 actor：A111 沖縄県女性団体連絡協議会、A115 新日本婦人の会沖縄県本部。

辅助建议：将两个女性组织相关混合词收敛为一个简洁受控词 `womens_organization`；具体法律／层级结构留在 `legal_status_guess` 与 notes。

负责人决定：**同意合并为 `womens_organization`。**

负责人理由／限制：项目负责人基本同意以更少的组织类型处理；社区、和平、人权等属于议题／功能信息，不继续塞入 actor class。

### HR019-CLASS-06 · `womens_or_human_rights_ngo`

影响 actor：A105 日本YWCA、A107 沖縄YWCA。

辅助建议：与 CLASS-05 同一收敛规则。

负责人决定：**同意合并为 `womens_organization`。**

负责人理由／限制：YWCA 的 NGO／公益法人／地域组织差异继续由 legal status、组织层级与 notes 表达；本分类决定不转移全国／地域组织的行动或关系。

## 4. 小组 C：watchlist 与派生分析层

### HR019-STATUS-X014 · NED

既有人工记录：

- HR-008 已由项目负责人 `human_checked`；
- FY2024 NED 亚洲官方 grant listing 未见日本／冲绳／琉球 direct recipient；
- 该负面核查只覆盖 FY2024，不能作跨年度排除。

辅助建议：`watchlist_only` 不再作为 `review_status`，另设 `watchlist=yes` 或 `scope_status=watchlist_only`；X014 的 `review_status` 记为 `human_checked`。保留现有谨慎证据说明，不改写成 NED 与冲绳 NGO 的关系。

负责人决定：**批准字段拆分：`review_status=human_checked`，另设 `watchlist=yes` 或等价 `scope_status=watchlist_only`。**

负责人理由／限制：项目负责人确认“已经人工复核”与“当前只作观察”是两个维度；要求除规则决定外，继续调查 X014 是否存在可核的跨年度／冲绳实质连接，再判断其观察边界。

#### 2026-07-19 有界实体关系补查

公开证据结果：

- NED 当前申请规则说明，其资助对象是境外非政府组织；不资助在美国或“其他成熟民主国家”实施的民主项目，但可资助设在这些国家、面向合资格国家或地区开展工作的组织。这使“直接资助一个在冲绳实施的国内民主项目”与其公开规则不吻合，但不能据此证明历史上绝无任何间接、跨境或未公开联系。
- NED 当前 active-grant 页面明确说明，出于 duty of care，部分合作方名称不会公开；因此公开名单中没有命中不能作为完整的负面证明。
- 对当前 active-grant listing 及既有 FY2024 记录补查，仍未找到以 Okinawa、Ryukyu 或冲绳组织为明确受资助对象／项目地点的公开记录。可见的 Japan 项目属于亚洲区域民主支持或日本对外政策／议员参与语境，不等于冲绳受资助关系。
- 未找到能把 X014 与本项目任一冲绳 actor、冲绳地点、基地争议或先岛安全议题相连的受奖、合同、机构报告或项目记录。

证据边界：

- 可以写：**截至本轮公开资料补查，未确认 NED—冲绳组织的直接 recipient／project 关系。**
- 不可以写：NED 从未资助冲绳组织；也不可以把亚洲区域项目、项目机会或未具名条目猜测为冲绳关系。

辅助范围建议（待负责人决定）：

- 保持 `scope_status=watchlist_only`，X014 只作外部资助制度观察节点，不进入默认冲绳组织网络。
- HR-025 的 AP048 不应继续保留为 `unclear` 的冲绳地点边；建议判为 `reject_edge`／`retire_candidate`，理由是“无公开证据支持 Okinawa place relation”，而不是选择某一种 place semantic。
- 除非以后出现明确 recipient、award、contract 或项目报告，否则不建立 actor-place、actor-issue、funding/support 或 inter-actor edge。

负责人实体范围追加决定：**确认上述建议。X014 保持 `scope_status=watchlist_only`；HR-025 AP048 应判为 `reject_edge`／`retire_candidate`。**

负责人理由／限制：截至本轮公开资料补查，没有证据支持 NED—冲绳 recipient、项目或地点关系。该决定是当前公开证据下的范围判断，不是跨年度“从未存在关系”的事实断言；出现明确 award、recipient、contract 或项目报告时可重新提交人审。

补查来源：

- NED 申请资格规则：`https://www.ned.org/apply-for-grant/en/`
- NED active-grant 页面及其当前 listing：`https://www.ned.org/active-grant-listing/`

### HR019-STATUS-X015 · Peace Winds Japan

既有人工记录：

- HR-008 已由项目负责人 `human_checked`；
- E4 资料只支持其 2018 年西日本水灾／北海道地震中的 USAID 灾害救援方法样本；
- 未确认冲绳基地、先岛或安全网络连接。

辅助建议：与 X014 使用同一字段规则；`watchlist_only` 移至独立 scope/watchlist 字段，`review_status=human_checked`。不得把非冲绳的 USAID 方法样本写成冲绳关系。

负责人决定：**批准与 X014 相同的字段拆分：`review_status=human_checked`，另设 `watchlist=yes` 或等价 `scope_status=watchlist_only`。**

负责人理由／限制：项目负责人要求继续调查 Peace Winds Japan 是否存在可核的冲绳／先岛／基地／安全或当地灾害治理连接；调查结果不得自动生成关系边。

#### 2026-07-19 有界实体关系补查

公开证据结果：

- Peace Winds Japan 的 FY2024 官方年报在“加强社区防灾能力”项下明确写明：该年度把地方社区联系网络扩展至北海道利尻岛和**冲绳先岛诸岛**，对象／方式包括居民、自主防灾组织、地方政府职员、医疗人员与 NPO 人员参加的学习会、技能学习和演练。这是此前 HR-008 未发现的直接先岛联系。
- 同一官方年报记载其灾害医疗支援船 `Power of Change` 于 2023 年 7 月投入使用，可作临时医疗、人员和物资运输；这只说明船舶功能。
- 2024 年 1 月由内阁官房、消防厅、冲绳县及先岛五市町村制作的国民保护共同图上训练资料，把该船列为近海区域运输的候选船，表述为“正在协调／尝试协调”。材料同时明确这是训练假定，不针对特定事态；因预计先岛约 12 万人避难时船运能力不足，仍需继续寻找候选船。
- 官方组织概况只列广岛总部、东京／佐贺分支和海外据点，未列冲绳分支。因此现有证据支持的是**项目／网络接触与政策演练中的候选资源角色**，不支持冲绳总部、分支或常驻据点。
- 2018 年 USAID 资金仍只对应西日本水灾和北海道地震救援。没有来源把这笔资金与先岛防灾网络或国民保护训练相连。

证据边界：

- 可以写：**PWJ 自报 FY2024 将社区防灾联系网络扩展到先岛；冲绳官方训练资料将其医疗支援船列为正在协调的候选船。**
- 不可以写：PWJ 已签约承担先岛撤离、已经实际部署、获得冲绳项目资金、与政府形成稳定合作关系，或在基地／自卫队部署争议中采取赞成或反对立场。
- 训练材料中的自卫队、海保和多种民间船舶并列出现，只说明同一演练方案中的候选运输资源；不得据此生成 PWJ 与这些机构的组织关系边。

辅助范围建议（待负责人决定）：

- 将 X015 从 `scope_status=watchlist_only` 改为一个有限纳入状态，例如 `scope_status=in_scope_limited`；角色限定为**日本国内外部防灾 NGO，经社区防灾与国民保护／居民避难规划进入先岛场域**。
- 议题只建议进入后续 edge 人工复核的候选队列：`life_safety` 可由现有词表承载；不得自动编码 anti-base、pro-base、anti-military、militarization 或政治立场。
- HR-025 的 AP049 已被新证据实质改变：原文“冲绳连接未确认”应撤回。若保留地点边，应以 `Sakishima` 为证据尺度，语义优先考虑 `institutional_venue` 或更精确的“有界项目／防灾网络场域”，不能写成 headquarters。是否需要新增／选择 place node 和最终 semantic，应在 HR-025 单独决定。
- 国民保护训练观察可进入后续 event/procedure 候选队列，角色严格写成 `candidate_vessel_under_coordination`；不得直接写入已执行服务、合同、稳定行政合作或组织联盟。

负责人实体范围追加决定：**确认上述建议。X015 改为有限纳入状态 `scope_status=in_scope_limited`；角色限定为通过社区防灾与居民避难规划进入先岛场域的外部防灾 NGO。**

负责人理由／限制：允许将 `life_safety`、Sakishima 地点连接和 `candidate_vessel_under_coordination` 分别送入后续 edge／place／event-procedure 人工复核，但本决定本身不批准这些边。不得编码反基地、拥基地、反军事等政治立场；不得把 2018 USAID 资金连接到先岛活动，也不得推定合同、实际部署、稳定政府合作或组织联盟。

补查来源：

- Peace Winds Japan FY2024 官方年报，第 18 页：`https://en.peace-winds.org/wp-content/themes/pwj2024/assets/pdf/PWJ_AR2024en.pdf`
- Peace Winds Japan 官方组织概况：`https://en.peace-winds.org/about/outline`
- 令和 5 年度冲绳县国民保护共同图上训练资料（2024-01-30），第 26–28 页：`https://www.town.yonaguni.okinawa.jp/docs/2024081400014/file_contents/02_.pdf`
- 2018 USAID 方法样本边界：`https://en.peace-winds.org/1790/`

### HR019-FAMILY-01 · 十个派生分析功能层

原方案：

1. 冲绳本地公民行动；
2. 劳工／教育组织；
3. 女性／人权／社区；
4. 法律／制度程序；
5. 日本国内 NGO／声援；
6. 跨国 NGO／国际倡议；
7. 基地社区服务／慈善；
8. 国际合作／公共外交；
9. 资助／赞助／公共机构；
10. 媒体／倡议观察节点。

#### 规则与实际 actor 补查

- `analysis_family_v1` 是由 `actor_class` 单值机械映射的派生展示层，不是来源支持的政治立场，也不覆盖 registry 的具体 `actor_class`。
- 原“冲绳本地公民行动”实际包含 7 个 `origin_type=japan_domestic` actor；本轮 A026 映射为 `citizen_group` 后又会进入该层。由于图的横轴已经单独显示来源层，family 名继续使用“冲绳本地”会把议题指向／行动功能与组织来源混在一起。
- A026 不再使用 `media_or_advocacy_actor` 后，第 10 层“媒体／倡议观察节点”没有 actor，应删除而不是保留空类。
- 六个工会已统一为 `labor_union`；“教育”是 A089/A090 的行业／议题属性，不应继续出现在 family 名。
- 四个女性组织已统一为 `womens_organization`；人权和社区工作继续由 issue／功能信息表示，不应在 family 名中推定所有该类 actor 都具有同样议题定位。
- `domestic_japan_ngo` 中既有环保 NGO，也有外交倡议组织；“声援”不是所有 actor 的共同属性。
- `international_ngo` 包含环境、法律和 X015 防灾救援组织；“国际倡议”不是所有 actor 的共同功能。X015 的补查进一步证明应使用更中性的“国际连接”。
- “资助／赞助／公共机构”包含企业 sponsor 与公共机构 partner；它们是主网络外围的资源／制度接口，不应作为一种 NGO 类型理解。X014 依负责人决定从默认网络排除。

辅助建议：**不原样批准十层；批准以下九个修订后的派生分析层。**

| 修订 family | 对应范围 | 本轮决定后的机械计数 | 解释限制 |
|---|---|---:|---|
| 公民行动／议题网络 | citizen group/network、executive committee、local NPO／civic actor；含 A026 | 54 | 来源地域由 `origin_type` 横轴表达；不等于全为冲绳本地组织 |
| 劳工组织 | 统一后的 `labor_union` | 6 | 不推定教育、和平或反基地立场 |
| 女性组织 | `womens_organization` | 4 | 人权／社区属于另层信息 |
| 法律行动／法律支持 | lawyers network／litigation team | 5 | 区分律师、原告团和程序角色 |
| 日本国内 NGO | `domestic_japan_ngo` | 11 | 不推定全部属于声援组织 |
| 跨国 NGO／国际连接 | international NGO／international advocacy actor；含有限纳入的 X015 | 23 | 不推定全部从事倡议或持同一政治立场 |
| 基地社区服务／慈善 | 军属俱乐部、社区服务和慈善网络 | 9 | 按观察到的服务功能编码，不推定拥基地／反基地 |
| 国际合作／公共外交 | 国际合作 NGO、exchange actor、public-diplomacy program | 4 | 组织、网络和项目仍由具体 actor class 区分 |
| 外部资源／公共机构接口 | 企业 sponsor、公共机构 partner；默认不含 X014 | 5 | 不是 NGO 类型；资金或合作关系必须另有关系级证据 |

计数说明：基于当前 122 actor registry 模拟本轮分类决定，并按负责人决定将 X014 排除于默认网络，故九层合计 121；这是样本构成，不是冲绳组织总体比例。中央表尚未据此改动。

负责人决定：**`approve_with_revision`——不原样批准十层，批准上述九个修订后的 `analysis_family_v1` 派生层。**

负责人理由／限制：派生层应保持少而清楚，并与 actor class、来源地域和议题标签分工。删除 A026 改类后形成的空层；去掉教育、人权、声援、国际倡议等不能覆盖整层 actor 的推定性词语。九层只用于 R1 组织生态图和报告展示，不覆盖 registry 原 actor class，不生成政治立场、组织关系或资金关系。

## 5. 决定摘要

| 决定组 | 负责人决定 | 影响范围 |
|---|---|---|
| CLASS-02 | 新增受控词 `labor_union` | 六个工会／工会联合体统一使用 |
| CLASS-03 | `labor_union_federation` → `labor_union` | 联合体结构留在 legal status／notes |
| CLASS-01 | `labor_or_education_union` → `labor_union` | 教育留在 sector／issue／notes |
| CLASS-04 | A026 → `citizen_group` | newsletter 是行动方式，不新增媒体类 |
| CLASS-05/06 | 两个女性相关混合词 → `womens_organization` | 法律身份、层级、人权／社区议题另存 |
| STATUS-X014/X015 | `review_status=human_checked` 与独立 scope/watchlist 字段分开 | review workflow 不再承载研究范围 |
| X014 实体范围 | 保持 `scope_status=watchlist_only` | 默认网络排除；AP048 应 reject／retire |
| X015 实体范围 | 改为 `scope_status=in_scope_limited` | 仅限先岛社区防灾／居民避难规划接口 |
| FAMILY-01 | 十层修订为九层 | 只作派生分析与展示 |

本批未批准任何 actor–issue、actor–place、actor–event、funding/support 或 inter-actor edge。X015 新发现的先岛连接只是把对应事实送入后续专门人审的依据。

## 6. 交主线程执行清单

1. 将本报告的 9 项规则决定回填到 `HR019_review_v0.csv`；保留项目负责人、日期与边界说明。
2. 在 schema／registry 主线中新增 `labor_union`、`womens_organization`，并按摘要执行六个工会、四个女性组织和 A026 的映射；不得顺带批准 issue edge。
3. 将 `watchlist_only` 从 `review_status` 中拆出为独立 scope/watchlist 维度；X014、X015 均保持 `review_status=human_checked`。
4. X014 保留在 registry 的外部观察层，但从默认 R1/R2 网络和默认 actor-place 图排除；将 HR-025 AP048 路由为 `reject_edge`／`retire_candidate`。
5. X015 设为 `in_scope_limited`。把 FY2024 先岛社区防灾联系、AP049 新地点语义和 `candidate_vessel_under_coordination` 分别送入 source、HR-025 和 event/procedure 候选队列；本报告不得直接激活这些边。
6. 将 `CLASS_FAMILY` 修订为本报告批准的九层，删除“媒体／倡议观察节点”，并在图注说明默认九层为 121 个纳入 actor，另有 X014 一个 watchlist 节点。
7. 主线程完成中央映射后，重新生成 R01/R02 分类审计、生态图、cross-issue 表、报告 claim audit 和受影响的 HR-029 freeze 候选；旧图不得静默继续使用。
8. 所有补查 URL 先按正常 source proposal／metadata／archive 流程进入主线；来源纳入不批准 actor、edge、资金、合同、联盟或政治立场。

中央 CSV、schema、图和既有 HR 队列均未由本报告直接修改。
