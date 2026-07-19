# 人工复核任务书 v0

日期：2026-07-12（状态更新至 2026-07-20）

## 1. 目的

本文件用于指挥人工复核。人工复核的目标不是“帮 AI 润色”，而是判断每条 actor、source、edge 是否能进入一期数据底座，是否需要降级、补证或剔除。

原则：

- AI 只负责初筛和结构化，不能做最终审定。
- 敏感关系必须由人审，尤其是资助、委托、公共外交、军属服务、NED / USAID / 外务省 / 美国使领馆相关线索。
- 不确定就降级为 `needs_second_source` 或 `needs_local_retrieval`。

## 0. 当前状态（更新至 2026-07-20）

2026-07-20：负责人已经回交的 HR-016–033 线上决定均已合并。HR-027 的 A112–A115 保留；AP123 已修复为 P007 Camp Foster；HR-033 的 dyadic relation 与 aggregate observation 已分层；HR-029 已重生为 505 个候选／41 个空白决定。

合并后的重新核账确认仍有三组前置人工任务：HR-010 批 6 的 47 条 actor–issue 补证、LCR001–004 的 4 条生命周期个案，以及 HR-034 的 50 条 `review_status` 交叉表。它们完成并合并以后才最终重生 HR-029；HR-031 的 3 条解释强度仍最后处理。完整总账见：

- `docs/principal_online_human_tasks_v1.md`
- `docs/principal_human_review_remaining_v14.md`

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

2026-07-12 建立 HR-010 至 HR-015 编号段；截至 2026-07-13 已收到并回写 HR-010 至 HR-015。A087-A106 已按 E4 一手来源先合并“组织身份”；其分类、议题、地点、事件和关系不因身份合并而自动成立。下列任务原文保留为审核轨迹，实际状态以本节和各任务标题为准。

2026-07-13：HR-010 批5（A102-A106）已完成并合并。A102/A103 为全国法律/原告团 background-support，A104 为普天间诉讼 core-support，A105 为声明层 background-solidarity，A106 为本土声援层；F037-F041 仅编码成员、法律代理和事件/伙伴行动，均非资金边或稳定联盟。A106 的 `首都圏キャンペーン` 暂作可能 canonical variant，待定名。HR-010 剩余对象为 A087-A093、A095-A101；A094 已按范围修正撤出。

同日，用户已提供并落库 HR-011、HR-012、HR-013、HR-014、HR-015 结论。HR-013 只新增 A111，并按 HR-010 范围修正撤出 A094，故 registry 净数不变。当前状态为：

| 任务 | 状态 | 当前结论 |
|---|---|---|
| HR-010 | partial / pending | A102-A106 已完成；A094 已按范围修正撤出；A087-A093、A095-A101 的 47 条边级补证仍待复核。 |
| HR-011 | completed | 新增 A107 沖縄YWCA、A108 沖縄を再び戦場にさせない県民の会、A109 第4次嘉手納弁护团、A110 大阪行动；C015 defer，不入主 registry。 |
| HR-012 | completed | A052/A053 完成规范名与诉讼轮次 alias；C026/C027 分别为 `round_of` A052/A053；C028 为 A010 的 `predecessor_of`，不另建 actor。 |
| HR-013 | completed | C011 以 A111 入表；C010、C034 只作 background；C029-C033 rejected。`okinawajosei.org` 属おきなわ女性財団，不能作为 A111 官网；A111 不接 `沖女連` alias。 |
| HR-014 | completed | 六案与 27 条案件角色已按案件特定边界人审落库。 |
| HR-015 | completed | 49 条 evidence note 与 64 条 actor-event-venue 记录已人审；A077-A085 撤出主 registry，保留为 E2 事件参与线索。 |
| HR-027 | completed | A112 宮古島地下水研究会、A113 宜野湾ちゅら水会、A114 全港湾沖縄地方本部、A115 新婦人沖縄県本部按模块价值入表；不自动批准事件或关系。 |
| HR-034 | pending | 45 条 source-log 行、AI068 及 4 条表级字段政策待人工 crosswalk；不得把 legacy 状态自动改成 `human_checked`。 |

主 registry 保留 **122 条历史记录**，其中 A072 是合并到 A071 的重复组织 tombstone，当前为 **121 个有效 actor**，仍达到原方案 120–180 下限。当前中央表另有 **295 sources、248 条 actor–issue 历史边、135 条 actor–place 历史边、67 条 AEV**。来源归档状态为 273 archived、2 manual_archived、18 failed、2 non-URL；归档失败不否定来源内容。

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

### HR-010 新增 E4 主体的分类与入网复核 — partial / pending

状态（2026-07-13）：A102-A106 已完成；A094 已撤出；A087-A093、A095-A101 仍待审核。以下保留原任务要求。

对象：A087-A093、A095-A101（A094 已按 HR-013 范围修正撤出；A102-A106 已于批5完成；对应 `outputs/registry_expansion_v1/merge_manifest_v1.csv`）

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

### HR-011 五个 E3 首批候选的补源与入表决定 — completed

完成状态（2026-07-13）：C009、C012、C023、C036 分别以 A107-A110 入表；C015 `defer`，不建 actor，只有取得能闭合组织身份与行动归属的一手／当地材料后才重开。A105 → A107 仅为总组织到地域组织的 `organizational_affiliation`；A109 → A052 仅为案件特定 `legal_counsel`。所有声援、活动和组织关系均明确不是资金关系或稳定联盟；具名人员未进入 organization registry。

以下保留原任务要求。

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

### HR-012 组织沿革、别名与诉讼代际复核 — completed

完成状态（2026-07-13）：A052 规范名为 `嘉手納基地爆音差止訴訟原告団`，C026 是其 `round_of`；A053 规范名为 `普天間基地爆音訴訟団`，C027 是其 `round_of`。C028 `石垣島への自衛隊配備を止める住民の会` 于 2015-08-20 成立，记录为 2016 年 9 月形成的较广联盟 A010 的 `predecessor_of`。三项均不另建 actor，也不推定跨轮次成员完全相同或前身与后继完全同体。

以下保留原任务要求。

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

### HR-013 范围边界与一般公益组织复核 — completed

完成状态（2026-07-13）：C011 `沖縄県女性団体連絡協議会` 以 A111 入表，作为有直接基地相关女性动员证据的 core-support actor；C010 `ひめゆり平和祈念財団` 与 C034 `沖縄県サンゴ礁保全推進協議会` 只作 background actor，不生成反基地关系或政治立场；C029-C033 因只有一般公益功能而无一期直接连接，均 `out_of_scope`／`rejected`。C015 仍属 HR-011 defer，不因本轮 gate 重开而入表。

范围修正：A094 `沖縄県女性連合会` 作为一般妇人会撤出 registry；A111 的加入与 A094 的撤出相抵，registry 仍为 118。后续在线核查还确认 `okinawajosei.org` 属 `公益財団法人おきなわ女性財団`，不是 A111 的组织官网；因此不以该域名支持 A111 身份，也不把歧义简称 `沖女連` 接到 A111。A111 只保留来源可核的正式名及 `女団協` 等无歧义写法。

机器 gate 已由本次人工决定覆盖：`outputs/registry_expansion_gate_v1/` 只保留为检索和提案轨迹，不再代表待定入表建议。以下保留原任务要求。

对象：C010、C011、C029-C034

要查：

- 持续法人或组织身份是否成立，以及是否有与基地、先岛安全化、地下水、珊瑚/海洋开发、战争记忆转译等一期问题的直接连接。
- 区分一般和平教育、环境教育、资源循环、珊瑚保全功能与基地争议参与。
- 对多方协作平台 C034，不因行政协作或成员交叠推定政治立场。

交付物：

- `core_actor` / `background_actor` / `out_of_scope` 决定及理由。
- 能支撑模块解释的具体事件、文件或程序入口；没有直接连接则不新增关系边。

### HR-014 法律与行政程序事实、角色和结果复核 — completed

完成状态（2026-07-13）：六案全部 `human_checked`，27/27 条案件角色按 plaintiff、counsel、requester、supporter、non-party 等案件特定边界接受并写入正式角色表。A002/A019 保持 Dugong 案 non-party；A011 是石垣住民投票 requester 而非组织原告；泡濑两轮结果保持分开。完整说明见 `outputs/R08_legal_procedure_v0/hr014_merge_note.md`。

以下保留原任务要求。

对象：`data/interim/17_legal_policy_procedure_cases_v0.csv` 六个案件；`data/interim/18_legal_policy_actor_roles_v0.csv`（模块镜像为 `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`）的候选角色。

要查：

- 六个案件的案号、法院/行政机关、起止日期、程序类型、请求内容和结果摘要。
- A052、A053、A011、A055、A020 等主体与案件的原告、支援、提交意见或运动组织角色。
- Dugong 诉讼中 A076、JELF、Earthjustice、Turtle Island Restoration Network 等角色不得外推给 A002/A019。
- 环评、住民诉讼、噪音诉讼和住民投票程序须区分；第一轮与第二轮泡濑诉讼结果不得合并为单一胜负。

交付物：

- 每案 `human_checked` 的事实摘要及来源定位（页码/段落/条款）。
- 每个 actor-case role 的接受、修订或拒绝决定。
- 只有复核后的角色才可进入主关系数据；程序存在不等于组织实际使用该程序。

### HR-015 证据笔记与事件—场域映射复核 — completed

完成状态（2026-07-13）：49 条 evidence note 和 64 条 actor-event-venue 记录全部完成人审，没有 reject 行；`revise` 表示措辞、角色、证据或 locator 边界修订，不表示证据自动升级。A077-A085 因仅有 E2 一次性 MMC 署名线索撤出主 registry，九条事件记录继续保留为 `unverified_event_participant`。四条 pathway 仍是 `analytical_seed`，五条 locator 明确待精确定位。完整说明见 `outputs/phase1_foundation_v1/hr015_merge_note.md`。

以下保留原任务要求。

对象：`outputs/phase1_foundation_v1/evidence_notes_seed_v0.csv` 49 条；`outputs/phase1_foundation_v1/actor_event_venue_seed_v0.csv` 64 条。

要查：

- 逐条打开来源，核对 locator、原文事实、actor、event、venue、target 和 action_type。
- 区分抗议、诉讼、游说、公开声明、共同署名、服务供给和制度协作。
- 同场参与、共同声明和共同署名只能作为事件性关系，不得自动升级为稳定联盟。
- 资助、赞助、委托、公共外交或军属服务相关条目须按敏感关系规则复核。

交付物：

- 每行 `accept` / `revise` / `reject` 与 reviewer、date、note。
- 经接受的 evidence note 和 event-venue 行；被拒或需补源的独立清单。
- 复核完成前不得把这些 seed 用作报告中的确定性关系结论。

### HR-016 先岛框架语义与来源定位复核 — completed / merged

当前状态（2026-07-20）：12 项线上决定已完成并合并；R4 当前为 19 条人审／QA-safe 事实、24 条安全摘录和 14 个分层实体。以下保留 2026-07-13 原任务说明作为审计轨迹，不得重复执行；地方组织原始表达缺口转入当地任务。

复核包：

- `outputs/R04_sakishima_frame_corpus_v0/hr016_review_items_v0.csv`
- `outputs/R04_sakishima_frame_corpus_v0/HR016_human_review_packet.md`

人工重点：

- 宫古 6・11 集会执行委员会与 A012／其他地下水组织的 crosswalk。
- 具名议员、匿名居民、行政材料与持续组织角色不得互相替代。
- 每项 `accept` / `revise` / `reject` 后，说明是否改变正式事实表、三地比较图、entity–frame 图或 brief。
- 与那国仍以安全环境、自治、公投、台湾邻近和生活／健康安全为主；语料缺少直接环境—部署连接不等于当地不存在环境关切。

### HR-017 公投程序阶段与角色复核 — online merged / 9 local items open

当前状态（2026-07-20）：9 项线上决定已合并，中央正式层为 29 stages／29 roles；另有 4 个阶段＋5 个角色共 9 项因缺当地一手材料继续空白。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R09_referendum_process_v0/hr017_review_queue_v0.csv`
- `outputs/R09_referendum_process_v0/HR017_review_packet_v0.md`

人工重点：

- A068 与官方事件名「名護市民投票推進協議会」的 alias／改名／拆分判断。
- A014／A015 的事件角色、持续性与当地材料；意见广告或反对运动不得写成投票正式发起／实施。
- 石垣两条诉讼链、个人原告／组织支援／律师／法院的角色分离，以及最高裁处分的中性措辞。
- `accept` / `revise` / `reject` 后同步检查正式阶段／角色表、空心／星号图层和 brief。

### HR-018 行政协作、金额与服务关系复核 — online merged / 2 local items open

当前状态（2026-07-20）：线上关系与来源前置决定均已合并，只剩 2 项当地／内部材料决定。当前目的性样本为 35 relations／28 amount observations／43 function observations，并与 S002 616-row 来源总体分层；以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R10_administrative_collaboration_v0/HR018_relation_review_v0.csv`
- `outputs/R10_administrative_collaboration_v0/HR018_source_prerequisites_v0.csv`
- `outputs/R10_administrative_collaboration_v0/HR018_review_guide_v0.md`

人工重点：

- 区分 actual contract、named recipient flow、project cost、aggregate、NOFO、sponsor tier、membership 与 service presence。
- 14 条 project-cost observation 一律不得当作 actor payment 或图中金额线宽；JPY／USD 不跨币种求和。
- ONC 的行政／公共服务功能不得泛化为运动资金关系；USO／AWWA／OESC／NOSCO 的服务对象不得替代政治立场证据。
- 每项 `accept` / `revise` / `reject` 后再决定是否执行 `main_merge_proposal_v1.csv`；不得让 AI 自行把敏感关系升级为人审结论。

### HR-019 R1/R2 分类词、桥梁机制与议题边范围复核 — completed / merged

当前状态（2026-07-20）：HR-019 已完成并合并。历史层为 122 actor rows／248 edge rows；当前图使用 121 个有效 actor 和 238 条有效 edge（65 人审／173 候选，103 connected／18 isolated）。以下保留原任务说明作为审计轨迹；HR-010 批 6 的 47 条边级补证仍是独立前置任务。

复核包：

- `outputs/R01_R02_actor_issue_v1/HR019/HR019_review_v0.csv`（9 个规则／受控词决定）
- `outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv`（30 个 bridge actor）
- `outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`（65 条 edge scope）
- `outputs/R01_R02_actor_issue_v1/HR019/HR019_review_guide_v0.md`

人工重点：

- 决定 6 个 schema 外 `actor_class` 术语是扩充受控词还是映射既有宽类；不得把组织法律身份、行动形态和政治立场压成同一字段。
- 对跨议题 actor 区分长期组织定位、案件／制度角色和事件性参加；共同署名或多议题出现不构成稳定联盟或长期经纪地位。
- 对 65 条范围不清 edge 只审 `organizational_positioning`／`institutional_or_case_role`／`event_specific`／`remain_unclear`，不得把 actor–issue edge 改写为 actor–actor 关系。
- 17 个 edge-isolated actor 应先补边级证据；扩样 gate 已由 HR-013 人工决定覆盖，不能为越过 120 下限而恢复已拒或仅背景对象。

### HR-020 R5 名称、别名与名单切分复核 — completed / merged

当前状态（2026-07-20）：14 项决定已完成并合并。169 条事件参与观察现分为 64 registry rows、22 human-reviewed event-only identities 和 83 other event-only names，alias pending 为 0；严格重复身份为 15 registry＋6 human-reviewed event-only。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R05_coaction_v1/HR020_review_packet_v0.md`
- `outputs/R05_coaction_v1/hr020_review_queue_v0.csv`
- `data/interim/25_coaction_event_participation_v0.csv`
- `outputs/R05_coaction_v1/repeat_participation_bridges_v0.csv`

人工重点：

- 核实日英／罗马字别名、跨事件同一主体和组织／项目层级，不凭名称相似或共同署名自动合并。
- 2010 来源自称 67 团体，但原字符串缺一处分隔符；HR020-06 决定应为 66 个 source-literal 名称还是拆为 67 个可辨组织。
- 接受 alias 只改变 entity crosswalk、事件重叠和重复参与计数；不把 event-only name 自动升为 registry actor，也不生成联盟、成员或资金边。
- 人审完成后须重跑参与表、二部边、重复桥梁、重叠表、两图和 brief，并保留原始 `source_name`。

### HR-021 R6/R7/R11 下游纳入与 analytical seed 复核 — completed / merged

当前状态（2026-07-20）：8 项决定已完成并合并；共用正式层为 80 条 observation，4 条 analytical seed 继续独立，R11 为 53 条进入观察。六个 SVG/HTML 已按当前模块表重绘。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R06_R07_R11_pathways_v1/HR021_review_items_v0.csv`
- `outputs/R06_R07_R11_pathways_v1/HR021_review_packet.md`

人工重点：

- `dependent_on_hr018` 项在对应 HR-018 `accept`／`revise` 前不得填写；之后只选 `include_after_hr018`／`revise_scope_after_hr018`／`exclude`。
- 行政协作不得外推资金方向、政府认同或基地政治立场；服务、慈善与 sponsor tier 不得推断亲／反基地立场或金额。
- analytical seed 只有取得独立事实性有向边证据才能升级；否则保持 seed，不能在路径图中画成因果或稳定关系。

### HR-022 跨模块来源元数据与支持范围复核 — completed / merged

当前状态（2026-07-20）：49 项来源元数据／支持边界决定已完成并合并。来源进入索引仍不批准 actor、关系、金额、角色或解释。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/phase1_source_integration_v1/HR022_source_metadata_review_v0.csv`
- `outputs/phase1_source_integration_v1/HR022_review_guide_v0.md`

人工重点：

- 打开 URL 或本地归档，核对 title、source_type、year/period、evidence_level 和可支持范围。
- `archived` 只表示保存成功，不表示元数据、actor relation、金额、角色或解释已获认可。
- R9 `usable_with_limit`、R4 locator/speaker 和 R10 type/year 推定必须保留原边界；来源入表不能自动升级模块结论。
- 对失败 URL 可记录权威替代副本与定位，但不得删除失败日志或把无法访问写成证据不存在。

### HR-023 覆盖审计

未建立人工决定任务。六维 coverage audit 是对既有字段的机械聚合，不含新的关系、角色或解释判断；因此保留编号说明，不伪造空白人审项。

### HR-024 既有 actor 的议题边补证复核 — online merged / A073 local item open

当前状态（2026-07-20）：HR-024 的线上决定已合并；A073 维持 `online_exhausted`／E0，作为 1 项当地材料决定继续开放。A087–A093、A095–A101 的 47 条补证仍归 HR-010 批 6。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`
- `outputs/edge_activation_v1/HR024_edge_activation_review_v0.csv`
- `outputs/edge_activation_v1/post_hr013_edge_activation_candidates_v1.csv`
- `outputs/edge_activation_v1/post_hr013_source_evidence_crosswalk_v1.csv`
- `outputs/edge_activation_v1/HR_review_guide_v0.md`

人工重点：

- 分开确认“组织身份存在”与“组织和一期议题有直接连接”；不得从 registry 的 `issue_tags` 反推边。
- 逐条选择 `accept`／`revise`／`reject`，并核对 source locator、scope、事件性／持续性和 actor 身份。
- 共同署名、同场参与或案件中的个人角色不得升级为组织的稳定联盟、常设定位或跨案件角色。
- A073 在线检索已耗尽且组织身份仍不闭合；不能仅凭旧名单或名称相似激活。

### HR-025 actor—place 语义与 AP123 键冲突复核 — completed / merged

当前状态（2026-07-20）：41 项决定已完成并合并；中央表保留 135 条历史地点边，其中 130 条有效（53 人审／77 候选）、5 条 retired，AP123 已固定为 P007 Camp Foster。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R03_spatial_dossier_v1/HR025_actor_place_semantics_review_v0.csv`
- `outputs/R03_spatial_dossier_v1/R03_spatial_dossier_brief_v1.md`
- `data/interim/32_actor_place_semantic_candidates_v1.csv`

人工重点：

- AP123 的现有 `place_id=P006` 指向 Camp Schwab，但边文本与证据指向 Camp Foster；必须由 HR-025 决定修订为 P007、改写证据范围或拒绝，任何 schema／脚本不得机械覆盖。
- `target` 表示行动、倡议或争议所指向的地点，不等于组织驻地；`site_presence`、`headquarters` 与广义 `institutional_scope` 必须分开。
- 边野古 44 条候选中 41 条为 target、3 条为 presence；该差异是解释重点，不得把 44 写成“44 个在地组织”。

### HR-026 三届县知事选—市民组织接口复核 — completed / merged

当前状态（2026-07-20）：19 项决定已完成并合并；18 条确认公开行动发生，1 条只确认活动预告。该层仍不批准票数、胜负或政策因果。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/R09_election_civic_interface_v1/HR026_election_civic_role_review_v0.csv`
- `outputs/R09_election_civic_interface_v1/R09_election_civic_interface_brief_v1.md`
- `data/interim/33_r09_election_civic_events_v1.csv`

人工重点：

- 逐项确认 actor 身份、选举年份、行动类型、对象与证据 locator；全国组织的行为不得转嫁给冲绳县本部，反之亦然。
- endorsement、出马请求、政策问卷、主权者教育和议题行动不能互换；候选人、政党和临时选举协调体不自动进入 NGO registry。
- 本任务不批准票数、投票率、胜负或政策效果的因果解释。

### HR-027 registry 价值门槛 v2 — completed / merged

当前状态（2026-07-20）：4 项决定均为 add，并以 A112–A115 合并；17 个事件描述留在候选队列，未新增组织间关系。八重山大地会因持续性缺口继续 defer。以下保留原任务说明作为审计轨迹。

复核包：

- `outputs/registry_value_gate_v2/HR027_registry_value_review_v0.csv`
- `outputs/registry_value_gate_v2/registry_value_gate_brief_v2.md`
- `data/interim/34_registry_value_candidates_v2.csv`

候选：

1. 宮古島地下水研究会；
2. 宜野湾ちゅら水会；
3. 全日本港湾労働組合沖縄地方本部；
4. 新日本婦人の会沖縄県本部。

八重山大地会仅保留为 defer 线索。人工应分别判断持续组织身份、一期直接连接、全国／地方层级与新增解释价值；接受后才由主线程顺序分配 A 编号并更新下游数据。

### HR-028 R5/R7 异质行动包

未建立人工决定任务。该包只把 148 条既有正式观察重组为 39 个去重行动单元和 6 案／17 阶段展示，不新增 actor、事实角色、关系、联盟或因果判断；因此保留编号说明，不伪造空白人审项。

### HR-029 schema 与 alias 冻结复核 — pending / after HR-010, lifecycle and HR-034

状态（2026-07-20）：post-merge 包形成 505 个统一候选，其中 41 条需要人工决定。HR-019／024／025／032／033 已合并，AP123 已解决；当前仍须等待 HR-010 批 6、LCR001–004 与 HR-034 后最终重生，当前包不是最终 freeze。

复核包：

- `outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv`
- `outputs/schema_alias_freeze_v1/schema_alias_freeze_brief_v1.md`
- `data/interim/36_schema_alias_freeze_candidates_v1.csv`

人工重点：

- 不合并全国组织与冲绳地方组织、前身与后继、诉讼轮次与持续原告团、律师团与原告团。
- AP123 不在 HR-029 作机械修订，唯一决定权归 HR-025。
- 规范词表旨在消除同义写法，不得抹去研究上有意义的组织层级、案件代际和历史有效期。

### HR-030 下一波来源元数据与归档复核 — completed / merged

状态（2026-07-20）：22 个 URL 的 metadata／archive 决定已经由负责人完成并合并。当前 archive manifest 为 273 archived、2 manual_archived、18 failed、2 non-URL；失败仍可能来自 SSL、403 或动态页面，不等于来源内容被否定。来源建索引不等于 HR-026／027 的候选事实获得批准。

复核包：

- `outputs/next_wave_source_integration_v1/HR030_source_metadata_archive_review_v0.csv`
- `outputs/next_wave_source_integration_v1/README.md`
- `outputs/next_wave_source_integration_v1/proposal_to_source_crosswalk_v1.csv`

人工重点：

- 核对 title、机构／发布者、年份、source type、evidence level、locator 与可支持范围。
- 失败 URL 应记录权威替代副本或人工归档，不把抓取失败写成证据不存在。
- 不在本任务中批准 actor 纳入、选举角色、污染／健康因果、劳工效果、关系或资金流。

### HR-031 报告解释强度复核 — pending

状态（2026-07-13）：机械 claim audit 在 78 条报告主张中识别出 3 个必须由研究负责人决定的解释强度问题；32 组数字全部匹配，事实表和来源可支持相关观察，但不能替代研究判断。所有决定栏为空。

复核包：

- `outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv`
- `outputs/report_claim_audit_v1/report_claim_audit_summary_v1.md`
- `data/interim/38_report_claim_evidence_audit_v1.csv`

人工重点：

- “基地问题的转译”可否作为一期中心解释，还是只称多议题并置／框架化。
- 地点差异可表述到何种强度，是否需要进一步用同口径材料控制资料可见度偏差。
- 边野古国际化是否可称“连续转换”；若保留，必须明确为分析性重建，不表达因果、指挥、资金或稳定联盟。

### HR-032 S002 高价值 partner alias／复合体 crosswalk 复核 — completed / merged

状态（2026-07-20）：8/8 identity／composite crosswalk 已由负责人完成并合并。R10 的 616 条来源行、machine display labels、standalone actor、办事机构、复合体与成员 crosswalk 继续分层；成员展开没有变成付款、资金边或稳定组织关系。

复核包：

- `outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv`
- `outputs/R10_official_collaboration_universe_v1/HR032_review_guide_v1.md`
- `outputs/R10_official_collaboration_universe_v1/official_collaboration_source_universe_v1.csv`

人工重点：

- 确认「沖縄県社会福祉協議会」的法律前缀省略是否仅作报告级 alias；这会改变第二图的高频 source-label 计数，但不使其进入一期 registry。
- 核对「沖縄県平和祈念財団」「おきなわ女性財団／男女共同参画センター」「沖縄平和協力センター A088」「沖縄県ユネスコ協会」及「レインボーハートokinawa」的同名连续性、法律类别与组织层级；不得与ひめゆり财团、A111 女団協或已移出 registry 的 A094 混同。
- JOCA 冲绳事务所、世界若者ウチナーンチュ连合会与各共同企业体必须区分 standalone actor、项目复合体和成员 crosswalk；即使接受成员说明，也不得拆分项目事业费或生成稳定关系。
- 当前两张 616-row source-universe 图不等待 HR-032；只有 canonical alias、JV 成员展开、registry crosswalk 或 actor-level 中心性解释受该任务控制。任何新行政关系／金额解释仍由 HR-018 或其后继任务决定。

### HR-034 legacy `review_status` 交叉复核 — pending

状态（2026-07-20）：中央表和派生模块仍混有 `verified`、`human_verified`、`watchlist_only`、`qa_safe_online`、`accepted` 及 lifecycle 工作流状态。已建立 50 个空白人工任务，不作自动字符串迁移。

复核包：

- `outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv`
- `outputs/review_status_crosswalk_v1/downstream_mechanical_impacts_v1.csv`
- `outputs/review_status_crosswalk_v1/README.md`

人工重点：

- 45 条 source-log 行逐条判断合法状态；source 状态不批准 actor、edge、资金或解释。
- AI067 已被 HR-019 拒绝；当前需处理的是 AI068，且不得把它重新纳入默认冲绳关系图。
- R4、R9、异质行动和 lifecycle 四项只决定字段语义与迁移规则，不能把所影响的行批量推定为人审通过。
- lifecycle 工作流状态应与 `review_status` 分栏；不改写仍为空白的 LCR001–004 个案决定。

## 7. 人工复核节奏

建议每轮 60-90 分钟，先处理 8-12 个高风险条目。

优先级：

1. HR-010 批 6 的 47 条 actor–issue 边级证据。
2. LCR001–004 的 4 条生命周期个案。
3. HR-034 的 50 条 legacy status crosswalk／表级政策。
4. 合并上述决定后最终重生并分批执行 HR-029 的 41 项 schema／alias freeze。
5. 最后处理 HR-031 的 3 条解释强度；当地 12 项等待一手材料。

## 8. 不合格复核示例

以下不算合格人工复核：

- 只说“看起来重要”。
- 只把 AI 输出重读一遍。
- 没有打开来源。
- 没有说明为什么升/降 evidence_level。
- 把“出现于署名名单”写成“稳定联盟成员”。
- 把“grant opportunity”写成“已获资助”。
