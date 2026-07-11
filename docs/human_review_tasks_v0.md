# 人工复核任务书 v0

日期：2026-07-12

## 1. 目的

本文件用于指挥人工复核。人工复核的目标不是“帮 AI 润色”，而是判断每条 actor、source、edge 是否能进入一期数据底座，是否需要降级、补证或剔除。

原则：

- AI 只负责初筛和结构化，不能做最终审定。
- 敏感关系必须由人审，尤其是资助、委托、公共外交、军属服务、NED / USAID / 外务省 / 美国使领馆相关线索。
- 不确定就降级为 `needs_second_source` 或 `needs_local_retrieval`。

## 0. 当前状态（2026-07-01）

HR-001 至 HR-009 已完成首轮人工复核。详细合并包见：

- `docs/human_review_merge_package_v0.md`
- `data/interim/human_review_log_v0.csv`

首轮结论摘要：

| 任务 | 状态 | 合并结论 |
|---|---|---|
| HR-001 | closed first-pass | A002 保留并确认为 SDCC / 任意団体 / IUCN 国家级 NGO 会员；新增 A076 Save the Dugong Foundation；不得把 A002 写成美国诉讼法律原告。 |
| HR-002 | closed first-pass | A008 保留为全国性国际协力 / 和平 NGO 网络；只写 2019 辺野古县民投票连带声明，不写成本地核心 actor。 |
| HR-003 | closed first-pass | A014 替换为 `住民投票を成功させるための実行委員会` E2；A015 保留为八重山 / 石垣侧声援线索 E2；A016 保留 E3。 |
| HR-004 | closed first-pass | A019 保留 E4，是辺野古现场核心 actor；legal_status 为任意団体；F013 降为 E2。 |
| HR-005 | closed first-pass | AWWA 名称修正为 American Welfare & Works Association；补全 X005/X006/X007/X016/X017 五成员网络。 |
| HR-006 | closed first-pass | X007 OESC 身份、EIN、2025 年 OESC -> USO Okinawa 捐赠可作为 E4 事实。 |
| HR-007 | closed first-pass | X013 只确认 NOFO / grant opportunity 存在；不得写 recipient 或已拨款。 |
| HR-008 | closed first-pass | X014 NED 与 X015 Peace Winds Japan 保持 watchlist_only；不得写 NED/USAID 资助冲绳 NGO。 |
| HR-009 | closed first-pass | A040 / A046 身份确认；A032-A046 只作为 2015 共同署名 / 国际声援节点，不写成稳定联盟。 |

首轮后仍需补的事项不属于 HR 未完成，而是后续补源 / 当地材料收集：

- A014/A015 仍需地方报纸、意见广告实物或议会资料交叉确认。
- A016 仍需成立年月、代表人、法律身份。
- A019 / A076 的 2003 年 dugong 诉讼 plaintiff 映射仍待核实。
- AWWA 网络仍需 charity recipient / Schedule I / 活动手册补证。
- X013 长期观察 Grants.gov / USASpending / 领馆公告是否出现 award 或 recipient。
- X014 NED 跨年度排除需要另查，本轮只覆盖 FY2024 亚洲清单。

2026-07-12 新增 HR-010 至 HR-015。A087-A106 已按 E4 一手来源只合并“组织身份”；其分类、议题、地点、事件和关系均未自动审定。法律程序角色、证据笔记和事件—场域映射也未合并进结论性关系表，须完成下列复核后再进入主数据。

## 2. 复核输入材料

主要输入：

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `data/metadata/coding_schema_v0.md`

必要时参考：

- `data/actor_registry_seed_v0.csv`
- `data/external_ngo_funding_seed_v0.csv`
- `docs/phase1_external_ngo_funding_adjustment_v0.md`
- 当前方案 md：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案.md`

## 3. 复核交付物

每轮人工复核后至少交付：

1. 已复核表格：在原表基础上补 `human_reviewer`、`review_date`、`review_note`，或另交 review log。
2. 问题清单：哪些 actor / edge 需要二次来源，哪些需要当地补查，哪些应剔除。
3. 口径修改建议：是否需要新增 actor_class、issue_tags、evidence_level 判定说明。
4. 可进入沟通稿的结论：只写 E3/E4，E2 只能写“线索”。

## 4. 复核判定字段

建议人工复核时补充以下字段：

| 字段 | 说明 |
|---|---|
| human_reviewer | 复核人 |
| review_date | 复核日期 |
| review_status | human_checked / human_revised / needs_second_source / needs_local_retrieval / rejected |
| review_note | 简短说明 |
| evidence_level_final | 人工确认后的 E0-E4 |
| publishable_claim | yes / cautious / no |

## 5. 证据等级复核口径

| 等级 | 可写法 | 人工判断重点 |
|---|---|---|
| E4 | “证据显示”“公开记录确认” | 是否有官方/组织/财报/award/contract/正式报告 |
| E3 | “公开资料显示”“基本确认” | 是否确认关系存在，但金额、年份或链条不全 |
| E2 | “存在相关线索”“仍需核查” | 是否只有新闻、活动页、社媒、二手资料 |
| E1 | 不进结论 | 是否无法复核或政治性指控为主 |
| E0 | 剔除 | 是否误配、同名误认、与冲绳无关 |

## 6. 第一批人工复核任务（原始任务定义，首轮已完成）

### HR-001 Save the Dugong Campaign Center

对象：A002

要查：

- 日文正式名是否为 `ジュゴン保護キャンペーンセンター` 或其他写法。
- 是否有独立官网、组织说明、法律身份或代表信息。
- 与 Earthjustice / OEJP / Henoko dugong litigation 的关系是否只是共同倡议，还是更稳定组织关系。

材料：

- `S007` APJJF 文章
- `S009` Earthjustice 页面
- `S004` NACSJ 2015 声明

交付物：

- 确认 canonical_name。
- 给出 legal_status_guess。
- 给出 evidence_level_final。
- 若找不到正式资料，标 `needs_second_source`。

### HR-002 NGO非戦ネット

对象：A008

要查：

- 组织结构：网络、任意团体、实委会还是项目名。
- 成员名单或参与声明。
- 是否与冲绳议题有直接关系，还是全国和平网络支援。

材料：

- `S005` Peace Boat 页面
- 组织官网 / Web Archive / 声明页

交付物：

- actor_class 判定。
- issue_tags 修正。
- 是否进入核心 actor 或只作为背景 actor。

### HR-003 与那国早期反部署组织

对象：A014、A015、A016

要查：

- `与那国改革会議`
- `与那国自衛隊配備反対意見広告実行委員会`
- `与那国島の明るい未来を願うイソバの会`

重点：

- 是否有地方新闻、议会记录、活动传单、住民投票资料支持。
- 不能只依赖党派媒体。
- 如果只有赤旗或单一报道，维持 E2。

材料：

- `S010` QAB 住民投票报道
- `S011` 琉球新报报道
- `S015` 赤旗报道

交付物：

- 每个组织是否保留。
- 是否需要当地补查。
- 与那国专题中可写到什么程度。

### HR-004 ヘリ基地反対協議会

对象：A019

要查：

- 直接官网或组织声明。
- 成立时间、活动地点、是否为边野古现场核心组织。
- 与边野古现场行动、共同声明、县民投票或国际倡议是否有公开关系。

材料：

- `S008`
- 组织官网 / Web Archive
- 地方新闻

交付物：

- 组织时间线简表。
- 可作为核心 actor 的依据。
- 缺口说明。

### HR-005 AWWA 正式名称与网络

对象：X004、X005、X006、X007

要查：

- AWWA 的正式名称到底是 American Women's Welfare Association 还是 American Welfare & Works Association，或是否历史上有改名。
- AWWA 与 NOSCO / KOSC / OESC 的成员或协调关系。
- 是否有 charity recipients / grant recipients。

材料：

- `X004` DVIDS
- NOSCO / KOSC / OESC 官网
- base newspaper / event booklet

交付物：

- actor alias 表建议。
- AWWA network edge 是否保留。
- 哪些内容需要当地补查。

### HR-006 OESC 线索复核

对象：X007

要查：

- OESC 是否有独立官网或公开社媒。
- Stripes 报道中的 501(c)(3)、USO donation、local/military community support 是否可由组织资料确认。

材料：

- Okinawa Stripes 报道
- OESC 官网 / 社媒 / 活动材料

交付物：

- evidence_level_final。
- 是否从 E2 升为 E3/E4。
- 不能确认时保持 `needs_second_source`。

### HR-007 美国领馆 Okinawa Youth Council

对象：X013、F012

要查：

- Grants.gov 或美国使领馆页面是否有 award notice。
- 实际 recipient organization 是谁。
- 执行机构是否为冲绳本地组织、学校、外部承包机构或美国机构。

材料：

- Grants.gov 页面
- U.S. Embassy / Consulate NOFO PDF
- 领馆活动新闻 / 社媒 / local news

交付物：

- recipient 是否确认。
- 若只是 grant opportunity，必须保留 `no_public_evidence`。
- 不得写成“美国领馆资助了某冲绳 NGO”，除非找到 award / recipient。

### HR-008 NED / USAID watchlist

对象：X014、X015

要查：

- NED FY2024 Asia grant listing 中是否有日本 / 冲绳 / 琉球 / Okinawa 直接 recipient。
- Peace Winds Japan 是否与冲绳基地、先岛、灾害治理或安全网络有一期相关连接。
- USAID 资助是否只作为“方法样本”，而不是冲绳关系。

材料：

- NED grant listing
- USAspending
- Peace Winds Japan 项目页

交付物：

- 是否进入 actor registry 主表。
- 是否仅保留 watchlist。
- 可写入沟通稿的保守措辞。

### HR-009 2015 国际署名组织身份确认

对象：A040、A046，必要时包括 A032-A045

要查：

- Pro Public 是哪个国家 / 哪个组织，是否与 NACSJ 英文署名一致。
- Pro Natura / FoE Switzerland 的正式组织名称。
- 其他海外组织是否只作为 2015 署名 seed，而不进入核心网络解释。

材料：

- `S004` NACSJ 2015 声明
- 各组织官网

交付物：

- 正式英文名。
- origin_type。
- 是否需要 actor_alias。

### HR-010 新增 E4 主体的分类与入网复核

对象：A087-A106（对应 `outputs/registry_expansion_v1/merge_manifest_v1.csv`）

已完成的安全合并：

- 仅凭 E4 一手来源确认组织名称和主体存在。
- `review_status` 暂为 `ai_seeded`；主表中的分类、地点和议题为候选值，不是人工审定结论。
- 未因新增主体自动生成 actor-issue、actor-place、actor-event 或 actor-relation 边。

要查：

- canonical name、日英中别名、法律身份和组织持续性。
- `actor_class`、`actor_type`、`origin_type`、`primary_places`、`issue_tags` 是否准确。
- 是否满足一期范围；如只具一般公益属性而无本项目议题连接，应降为背景主体或剔除。
- 只有在来源明确记载参与方式时，才新增议题、地点、事件或关系边。

交付物：

- 每个主体的 `human_reviewer`、`review_date`、`review_status`、`review_note`。
- 接受、修订、背景保留或剔除决定。
- 经审核的新增边清单；共同署名或同场参与不得写成稳定联盟。

### HR-011 五个 E3 首批候选的补源与入表决定

对象：C009、C012、C015、C023、C036

重点对象：沖縄YWCA、沖縄を再び戦場にさせない県民の会、宮古島・命の水・自衛隊配備について考える会、第4次嘉手納基地爆音差止訴訟弁護団、辺野古に基地を絶対つくらせない大阪行動。

要查：

- 为每个候选补至少一条独立来源，优先组织官网、法人记录、诉状/判决或地方报刊。
- 确认组织持续性、正式名称、代表/事务局及与一期议题的直接连接。
- C023 不得仅凭律师事务所博客推定完整律师团成员或诉讼代理范围。
- C036 属本土声援层，须明确它进入 registry 后在 R11 中的分析用途，避免改变冲绳本地主体的构成口径。

交付物：

- `add` / `background_only` / `needs_local_retrieval` / `reject` 决定。
- `evidence_level_final` 与新增来源编号。
- 若加入，按 HR-010 相同标准审定字段和边。

### HR-012 组织沿革、别名与诉讼代际复核

对象：C026、C027、C028；对照 A052、A053、A010

要查：

- 第4次嘉手納基地爆音差止訴訟原告団是否为 A052 的时代名称、继承组织或应独立建 actor。
- 普天間基地第2次爆音訴訟原告団与 A053 的代际和覆盖范围。
- 石垣島への自衛隊配備を止める住民の会与 A010 的前身、改名、并存或人员重叠关系。
- 优先查诉状、判决、原告团会报、组织章程、地方新闻和可核日期，不以名称相似直接合并。

交付物：

- `alias_of` / `predecessor_of` / `successor_of` / `separate_actor` 判定。
- 如拆分，给出新 actor ID 和有效时间；如合并，给出 alias 与依据。
- 不能确认时保留候选，不写跨期稳定关系。

### HR-013 范围边界与一般公益组织复核

对象：C010、C011、C029-C034

要查：

- 持续法人或组织身份是否成立，以及是否有与基地、先岛安全化、地下水、珊瑚/海洋开发、战争记忆转译等一期问题的直接连接。
- 区分一般和平教育、环境教育、资源循环、珊瑚保全功能与基地争议参与。
- 对多方协作平台 C034，不因行政协作或成员交叠推定政治立场。

交付物：

- `core_actor` / `background_actor` / `out_of_scope` 决定及理由。
- 能支撑模块解释的具体事件、文件或程序入口；没有直接连接则不新增关系边。

### HR-014 法律与行政程序事实、角色和结果复核

对象：`data/interim/17_legal_policy_procedure_cases_v0.csv` 六个案件；`outputs/R08_legal_procedure_v0/actor_procedure_roles_v0.csv` 的候选角色。

要查：

- 六个案件的案号、法院/行政机关、起止日期、程序类型、请求内容和结果摘要。
- A052、A053、A011、A055、A020 等主体与案件的原告、支援、提交意见或运动组织角色。
- Dugong 诉讼中 A076、JELF、Earthjustice、Turtle Island Restoration Network 等角色不得外推给 A002/A019。
- 环评、住民诉讼、噪音诉讼和住民投票程序须区分；第一轮与第二轮泡濑诉讼结果不得合并为单一胜负。

交付物：

- 每案 `human_checked` 的事实摘要及来源定位（页码/段落/条款）。
- 每个 actor-case role 的接受、修订或拒绝决定。
- 只有复核后的角色才可进入主关系数据；程序存在不等于组织实际使用该程序。

### HR-015 证据笔记与事件—场域映射复核

对象：`outputs/phase1_foundation_v1/evidence_note_seeds_v1.csv` 49 条；`outputs/phase1_foundation_v1/actor_event_venue_seeds_v1.csv` 64 条。

要查：

- 逐条打开来源，核对 locator、原文事实、actor、event、venue、target 和 action_type。
- 区分抗议、诉讼、游说、公开声明、共同署名、服务供给和制度协作。
- 同场参与、共同声明和共同署名只能作为事件性关系，不得自动升级为稳定联盟。
- 资助、赞助、委托、公共外交或军属服务相关条目须按敏感关系规则复核。

交付物：

- 每行 `accept` / `revise` / `reject` 与 reviewer、date、note。
- 经接受的 evidence note 和 event-venue 行；被拒或需补源的独立清单。
- 复核完成前不得把这些 seed 用作报告中的确定性关系结论。

## 7. 人工复核节奏

建议每轮 60-90 分钟，先处理 8-12 个高风险条目。

优先级：

1. E2 但可能进入结论的条目。
2. 资助 / 赞助 / 公共外交 / 军属服务关系。
3. 与那国 / 先岛专题核心组织。
4. 组织名、别名、法律身份不稳定的条目。

## 8. 不合格复核示例

以下不算合格人工复核：

- 只说“看起来重要”。
- 只把 AI 输出重读一遍。
- 没有打开来源。
- 没有说明为什么升/降 evidence_level。
- 把“出现于署名名单”写成“稳定联盟成员”。
- 把“grant opportunity”写成“已获资助”。
