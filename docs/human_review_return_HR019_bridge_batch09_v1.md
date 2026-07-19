# HR-019 跨议题 actor 第二组回交报告 Batch 09

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv`  
状态：**已完成——10/10 条**

## 0. 批次边界

- 本批复核 HR-019 bridge actor 队列第 11–20 条。
- 推荐决定仅使用队列允许值：`include_with_scope`、`candidate_only`、`exclude_from_narrative`。
- “bridge”只表示同一 actor 的可观察行动把议题表达、行动场域或制度渠道连接起来，不表示影响力、领导地位、中心性、联盟或因果效果。
- 本批特别区分同一案件中的不同角色：Earthjustice 是代理律师组织；JELF 和 Center for Biological Diversity 是具名组织原告。共同参与同一诉讼不生成稳定联盟。
- 对石垣、宫古等先岛 actor，只记录其公开提出的地下水、交通、生活安全、地方决策与前线化风险；不把风险主张写成已经证明的污染、伤害或政策因果。
- 本报告决定 actor 是否可进入跨议题正文及其必要范围；每条 actor–issue edge 的最终时间范围仍须由 HR-019 edge-scope 队列逐条决定。
- 本报告不直接修改中央 registry、actor–issue 表、HR CSV、source log、图或报告正文。

## 1. 建议结论总表

| actor | 当前候选 | 辅助建议 | 建议的桥接机制／限制 |
|---|---|---|---|
| A009 Earthjustice | `case_or_institutional_bridge`，3 issues | `include_with_scope` | 严格限于冲绳儒艮案的代理律师／国际法律渠道；不是具名原告 |
| A010 石垣島に軍事基地をつくらせない市民連絡会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 持续反军事部署定位连接地下水调查和地方参与／决策诉求；风险陈述按组织主张归属 |
| A011 石垣市住民投票を求める会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 自卫队部署争议→住民投票条例请求、市议会与后续司法争议；是请求／运动主体，不是具名组织原告 |
| A012 宮古島いのちの水を守ろう！ | `mixed_candidate_bridge`，3 | `candidate_only` | 现有材料更像单次活动执行委员会；精确组织身份与持续性仍无独立第二来源 |
| A013 ミサイル基地いらない宮古島住民連絡会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 反军事部署定位连接地下水、危险物与交通／生活安全请求；不证明实际污染或伤害 |
| A017 沖縄対話プロジェクト | `mixed_candidate_bridge`，3 | `include_with_scope` | 以对话活动连接台湾有事、冲绳前线化预防与和平；三个标签主要属于同一预防性框架 |
| A018 ノーモア沖縄戦 命どぅ宝の会 | `positioning_bridge`，3 | `include_with_scope` | 持续反战定位连接台湾有事、冲绳／先岛前线化与和平动员；不得推出所有共同参与者关系 |
| A020 日本環境法律家連盟（JELF） | `mixed_candidate_bridge`，3 | `include_with_scope` | 严格区分案件角色：儒艮案具名原告；泡濑案仅为支持者／正式材料发布者 |
| A045 Center for Biological Diversity | `mixed_candidate_bridge`，3 | `include_with_scope` | 冲绳儒艮案具名组织原告，把生物多样性争议带入美国司法／国际倡议渠道 |
| A049 基地・軍隊を許さない行動する女たちの会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 以女性人权与军事性暴力／生活安全框架连接反基地和反军事行动；不能压缩成一般反军事 actor |

建议分布：`include_with_scope` 9 条，`candidate_only` 1 条，`exclude_from_narrative` 0 条。

## 2. A009 · Earthjustice

现有三个 issue：

- I004 `dugong`
- I011 `legal`
- I012 `international_advocacy`

### 证据判断

HR-014 已人工确认 Earthjustice 在 Okinawa Dugong v. Rumsfeld／Center for Biological Diversity v. Esper 案中的角色：

- Earthjustice 是代表原告的律师组织；
- 它不是该案具名组织原告；
- 案件将冲绳儒艮和边野古工程争议带入美国《国家历史保存法》审查；
- 2020 年第九巡回法院最终维持国防部合规判断，诉讼没有停止工程。

主要材料：

- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`，R8R005；
- Earthjustice 案件页；
- 美国第九巡回法院 2017、2020 年判决。

### 辅助建议

**A009=`include_with_scope`，保留 `case_or_institutional_bridge`。**

正文安全表述：

> Earthjustice 作为冲绳儒艮案原告方律师组织，把边野古／儒艮保护争议转入美国联邦司法和国防部合规审查，是严格案件范围内的法律—国际制度桥梁。

限制：

- 不称 Earthjustice 为原告；
- 不把律师代理关系写成与 JELF、CBD 或冲绳组织的稳定联盟；
- 不从诉讼参与推断案件胜诉、工程停止或政策影响；
- 三个 issue 是同一案件机制的不同面向，不作三个独立运动领域。

建议 notes 机制标签：`dugong_case_counsel_and_us_legal_channel_bridge`。

## 3. A010 · 石垣島に軍事基地をつくらせない市民連絡会

现有三个 issue：

- I002 `anti_military`
- I006 `groundwater`
- I009 `local_autonomy`

### 证据判断

HR-012 已确认该会的组织连续性：

- 2016 年作为更广泛的市民联合体成立，并可追溯至 2015 年前身活动；
- 公开行动持续围绕石垣岛自卫队部署、候选地和建设程序；
- 2018 年材料记录该会参与水源地／地下水调查并提出风险问题；
- 其地方自治连接来自要求居民说明、信息公开、地方参与和决策正当性的行动，而不是从“地方组织”身份自动推出。

主要材料：

- S157：组织成立和前身连续性；
- 冲绳时报 2018 年水源地调查报道；
- 既有石垣自卫队部署和地方程序材料。

### 辅助建议

**A010=`include_with_scope`。**

正文安全表述：

> 石垣島に軍事基地をつくらせない市民連絡会在持续反对军事部署的行动中，把候选地水源／地下水调查与居民说明、信息公开和地方决策参与连接起来。

限制：

- `groundwater` 只写组织开展调查和提出风险，不写成基地已经造成污染；
- `local_autonomy` 具体落在居民参与、说明责任和地方决策程序，不泛化为代表全体石垣市民；
- 不把同场组织、住民投票运动或共同声明参与者自动编码为联盟。

建议 notes 机制标签：`military_deployment_to_water_and_local_decision_bridge`。

## 4. A011 · 石垣市住民投票を求める会

现有三个 issue：

- I002 `anti_military`
- I009 `local_autonomy`
- I010 `referendum`

### 证据判断

HR-014 已人工确认：

- A011 是围绕陆上自卫队部署提出住民投票条例请求的请求／公民运动主体；
- 官方石垣市记录确认条例请求及市议会处理；
- 后续诉讼材料可以说明这一运动与司法争议的过程连接；
- 但在没有起诉状明确列名的情况下，A011 不是具名组织原告。

### 辅助建议

**A011=`include_with_scope`。**

正文安全表述：

> 石垣市住民投票を求める会把自卫队部署争议转译为住民投票条例请求，进入市长、市议会和后续司法争议，是“军事设施争议—地方自治—公投程序”的明确制度桥梁。

限制：

- 只写请求、议会处理和可核实的后续程序，不推断代表全市多数意见；
- 不称 A011 为具名组织原告；
- 不从投票请求推断部署、选举或政策结果。

建议 notes 机制标签：`deployment_dispute_to_referendum_procedure_bridge`。

## 5. A012 · 宮古島いのちの水を守ろう！

现有三个 issue：

- I002 `anti_military`
- I006 `groundwater`
- I007 `life_safety`

### 证据与身份缺口

现有 S020 可以支持 2016 年一场围绕宫古岛地下水和自卫队配备的活动，但其名称更像活动执行委员会／动员名义，尚不足以确认：

- 它是否为持续存在的独立组织；
- 名称是否稳定；
- 该 actor 与 A112 宮古島地下水研究会、A013 ミサイル基地いらない宮古島住民連絡会或其他名称相近团体的关系；
- 事件之后是否还有独立行动和组织连续性。

本批补查未找到与 A012 精确名称相匹配的独立第二来源。检索到的 `宮古島・命の水・自衛隊配備を考える会` 等近似名称不能仅凭议题和词语相似即合并。

### 辅助建议

**A012=`candidate_only`。**

候选安全表述：

> 2016 年宫古岛一场以“守护生命之水”为名的市民活动把地下水、生活安全和自卫队配备争议并置；现有资料尚不能确认该名称对应持续独立组织。

限制：

- 不把一次活动名直接升级为持续 actor；
- 不与 A112、A013 或名称相近团体合并；
- 不进入正式 bridge 正文和 bridge 排名；
- 保留 event-only／identity-needs-second-source 状态，等待宫古地方资料补证。

建议 notes 机制标签：`water_and_deployment_event_identity_unresolved`。

## 6. A013 · ミサイル基地いらない宮古島住民連絡会

现有三个 issue：

- I002 `anti_military`
- I006 `groundwater`
- I007 `life_safety`

### 补查结果

本批补查改善了原有 `ai_seeded` 的连续性：

- 2018 年材料点名该会共同代表和每周持续行动，并记录其围绕地下水、软弱地盘、燃料和弹药设施提出的问题；
- 2023 年宫古岛市地域协调会议记录正式点名该会，并记载其向市方提出基地对策窗口、交通安全等请求；
- 2024 年市方会议记录继续出现该会；
- 2026 年地方报道仍记录该会相关行动。

主要补查来源：

- `https://www.jcp.or.jp/akahata/aik18/2018-12-25/2018122515_01_1.html`
- `https://www.city.miyakojima.lg.jp/soshiki/shityo/kikaku/hisyokouhou/files/00_kaigirokuR5.7.3.pdf`
- `https://miyakojima.cmskit.jp/soshiki/shityo/kikaku/hisyokouhou/oshirase/20241002gijiroku.pdf`
- `https://ryukyushimpo.jp/national/entry-5377153.html`

### 辅助建议

**A013=`include_with_scope`。**

正文安全表述：

> ミサイル基地いらない宮古島住民連絡会通过持续反对导弹／自卫队基地部署的行动，把地下水、危险物设施和交通安全等生活风险诉求带入公开抗议及市政协调渠道。

限制：

- 记录组织提出的风险类别和行政请求，不断言设施已经造成地下水污染、事故或健康损害；
- `anti_military` 可作为持续定位；`groundwater`、`life_safety` 应按具体年份和行动定界；
- 党报可支持被点名行动，不由此推断政党隶属；
- 与 A112、A012 或其他共同参加者的议题重合不构成组织关系。

建议 notes 机制标签：`anti_deployment_to_water_and_life_safety_request_bridge`。

## 7. A017 · 沖縄対話プロジェクト

现有三个 issue：

- I017 `frontline_prevention`
- I018 `Taiwan_contingency`
- I019 `peace`

### 证据判断

组织官网和规约可以确认：

- 项目具有明确组织目的、活动形式和名护市主事务所；
- 它通过对话会、讲座和交流讨论台湾有事、冲绳成为战场／前线的风险；
- 其核心机制是以对话和冲突预防推动和平讨论，而不是反对某一单项工程的环保或诉讼 actor。

来源：

- `https://okinawataiwa.net/`
- `https://okinawataiwa.net/index.php/about-us/about_terms/`

### 辅助建议

**A017=`include_with_scope`。**

正文安全表述：

> 沖縄対話プロジェクト通过持续对话活动，把台湾有事讨论、冲绳前线化预防与和平／冲突预防连接起来，是项目型的议题翻译 actor。

限制：

- 三个标签主要属于同一预防性对话框架，不能当成三个独立领域；
- 只写公开活动、参与场域和组织目的，不推断对政策、舆论或冲突风险的实际效果；
- 参与对话不表示参与者形成稳定联盟或接受项目全部立场。

建议 notes 机制标签：`dialogue_based_frontline_prevention_bridge`。

## 8. A018 · ノーモア沖縄戦 命どぅ宝の会

现有三个 issue：

- I017 `frontline_prevention`
- I018 `Taiwan_contingency`
- I019 `peace`

### 证据判断

组织官网和持续活动记录显示：

- 该会以防止冲绳再次成为战场为明确长期定位；
- 其声明、学习会和行动持续讨论台湾有事、先岛军事化和居民避难／生活风险；
- 官网活动更新延续至 2026 年，足以排除一次性事件名称的主要疑虑。

来源：

- `https://nomore-okinawasen.org/`

### 辅助建议

**A018=`include_with_scope`，保留 `positioning_bridge`。**

正文安全表述：

> ノーモア沖縄戦 命どぅ宝の会以“防止冲绳再次成为战场”为持续定位，把台湾有事、冲绳／先岛前线化与和平动员连接起来。

限制：

- 三个 issue 是同一反战／前线化预防框架的不同面向；
- 对先岛的讨论按组织公开主张归属，不代替与那国、石垣或宫古当地 actor 的地方自治判断；
- 共同声明、集会或学习会参与不生成稳定联盟；
- 不推断其行动改变部署、避难政策或安全环境。

建议 notes 机制标签：`anti_war_frontline_prevention_positioning_bridge`。

## 9. A020 · 日本環境法律家連盟（JELF）

现有三个 issue：

- I004 `dugong`
- I005 `biodiversity`
- I011 `legal`

### 证据判断

HR-014 已确认 JELF 在不同案件中的角色不能互相转移：

1. **冲绳儒艮案**
   - JELF 是美国第九巡回法院官方判决列出的具名组织原告／上诉人；
   - 在该案中不是律师。
2. **泡濑居民诉讼**
   - JELF 发布原告／律师团正式声明和材料；
   - 现有证据只支持 supporter／formal-material host；
   - 不能写成该案原告或律师。

主要材料：

- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`，R8R003、R8R026；
- `https://www.jelf-justice.org/base_issue/post-1430/`
- 美国第九巡回法院官方判决。

### 辅助建议

**A020=`include_with_scope`。**

正文安全表述：

> JELF 通过环境法网络把儒艮／生物多样性争议带入诉讼和正式法律材料传播；其具体制度角色必须逐案区分——在冲绳儒艮案是具名原告，在泡濑案仅有支持／材料发布证据。

限制：

- 不把 `legal` 身份自动泛化为所有冲绳环境案件的律师、原告或协调者；
- 不因与其他原告共同起诉推断稳定联盟；
- 儒艮与生物多样性是同一环境法律机制的相邻标签，不按两个独立领域加权；
- 保留各案结果和未获救济范围。

建议 notes 机制标签：`environmental_law_bridge_with_case_specific_roles`。

## 10. A045 · Center for Biological Diversity

现有三个 issue：

- I005 `biodiversity`
- I011 `legal`
- I012 `international_advocacy`

### 证据判断

美国第九巡回法院 2017、2020 年官方判决确认：

- Center for Biological Diversity 是冲绳儒艮案具名组织原告／上诉人；
- 诉讼针对美国国防部对边野古工程影响冲绳儒艮的审查与合规判断；
- 2020 年终局结果维持国防部合规判断，没有停止工程。

主要材料：

- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`，R8R001；
- `https://cdn.ca9.uscourts.gov/datastore/opinions/2017/08/21/15-15695.pdf`
- `https://cdn.ca9.uscourts.gov/datastore/opinions/2020/05/06/18-16836.pdf`

### 辅助建议

**A045=`include_with_scope`。**

正文安全表述：

> Center for Biological Diversity 作为冲绳儒艮案具名组织原告，把边野古／儒艮生物多样性争议带入美国联邦司法和跨国倡议场域，是严格案件范围的国际法律桥梁。

限制：

- A045 是原告，不是律师；
- 不从具名原告身份推断其与其他原告形成稳定联盟；
- 不把共同署名或案件参与扩大成对冲绳全部基地议题的持续代表；
- 不从诉讼推出工程停止或政策成功。

建议 notes 机制标签：`biodiversity_plaintiff_to_us_legal_channel_bridge`。

## 11. A049 · 基地・軍隊を許さない行動する女たちの会

现有三个 issue：

- I001 `anti_base`
- I002 `anti_military`
- I007 `life_safety`

### 补查结果

既有学术来源记录该会在 1995 年美军性暴力事件后形成。组织关联空间 `すぺーす結` 的官网和声明档案又显示：

- 组织持续以女性立场讨论基地／军队与性暴力；
- 它把个案抗议放入军事结构、女性人权与日常安全框架；
- 官网仍提供组织活动、声明和联络信息，支持持续性而非一次性事件 actor。

补查来源：

- `https://space-yui.com/`
- `https://space-yui.com/?cat=3`

### 辅助建议

**A049=`include_with_scope`。**

正文安全表述：

> 基地・軍隊を許さない行動する女たちの会从女性人权、军事性暴力和日常生活安全出发连接反基地与反军事行动，是性别化生活安全框架的跨议题 actor。

限制：

- 不能把其桥接机制缩减为一般的反基地／反军事立场；
- 当前队列未列 I022 `women`、I023 `human_rights`，本批不自动新增 edge；应在后续 edge-scope／缺边审查中另行提出并由负责人判断；
- 声明、共同抗议和场地使用不生成稳定联盟；
- 不从组织立场推断全部美军相关犯罪、制度因果或政策效果。

建议 notes 机制标签：`gendered_military_violence_and_life_safety_bridge`。

## 12. 本批共同解释规则

若负责人确认，本批正文按四类机制处理：

1. **严格案件／法律角色**
   - A009：冲绳儒艮案原告方律师；
   - A020：儒艮案原告，泡濑案支持／材料发布者；
   - A045：儒艮案原告。
2. **地方程序与生活风险转译**
   - A010：部署争议—地下水调查—地方参与；
   - A011：部署争议—地方自治—住民投票程序；
   - A013：部署争议—地下水／危险物／交通安全—市政请求。
3. **和平／前线化预防定位**
   - A017：对话活动型；
   - A018：持续反战定位型。
4. **性别化生活安全**
   - A049：女性人权／军事性暴力—生活安全—反基地／反军事。

A012 保留 candidate layer，等待精确身份和持续性第二来源。

## 13. 如负责人确认，本批主线程动作

1. 在 HR019 bridge queue 回填 9 条 `include_with_scope`、A012 一条 `candidate_only`。
2. 将本报告的机制标签和限制写入 `review_notes`，不得只保留无范围的 include。
3. 对 A009、A020、A045 固定角色词：
   - Earthjustice=`counsel`；
   - JELF=`plaintiff`（儒艮案）、`supporter/formal-material host`（泡濑案）；
   - CBD=`plaintiff`。
4. 对 A011 固定 `requester/campaign body`，不得写成具名组织原告。
5. A010、A013 的地下水和生活安全内容按“组织调查／提出的风险与请求”写，不升级为已证明后果。
6. A012 不与 A112、A013 或近似名称组织合并，进入 local retrieval／identity repair 队列。
7. A017、A018 的三个标签不计为三个独立桥接领域。
8. A049 的 I022 `women`、I023 `human_rights` 作为后续缺边候选另审，本批不自动加入中央表。
9. 新增官网、官方会议记录和报道先进入 source proposal；source inclusion 不自动批准任何 edge、组织关系或因果解释。
10. HR019 全部 bridge 与 edge-scope 完成后再统一生成正文和图；不得按当前 issue_count 直接排名。

本报告本身未修改中央表、HR CSV、source log 或图表。

## 14. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议：

- A009 Earthjustice：`include_with_scope`；
- A010 石垣島に軍事基地をつくらせない市民連絡会：`include_with_scope`；
- A011 石垣市住民投票を求める会：`include_with_scope`；
- A012 宮古島いのちの水を守ろう！：`candidate_only`；
- A013 ミサイル基地いらない宮古島住民連絡会：`include_with_scope`；
- A017 沖縄対話プロジェクト：`include_with_scope`；
- A018 ノーモア沖縄戦 命どぅ宝の会：`include_with_scope`；
- A020 日本環境法律家連盟（JELF）：`include_with_scope`；
- A045 Center for Biological Diversity：`include_with_scope`；
- A049 基地・軍隊を許さない行動する女たちの会：`include_with_scope`。

负责人同时确认：

- A009 只作为冲绳儒艮案原告方律师组织；A020、A045 为该案具名组织原告，不得互换角色；
- A020 在泡濑案只按支持者／正式材料发布者使用；
- A011 是住民投票请求／运动主体，不写成具名组织原告；
- A010、A013 的地下水和生活安全内容只写组织开展的调查、提出的风险和行政请求，不升级为已证明污染、伤害或政策因果；
- A012 保持 `candidate_only`，不与 A112、A013 或近似名称团体合并；
- A017、A018 的三个标签是同一“台湾有事—前线化预防—和平”框架的分层表达；
- A049 按女性人权／军事性暴力—生活安全桥梁解释；I022 `women`、I023 `human_rights` 仅作为后续缺边候选，本批不自动新增；
- 同案、共同声明、共同活动和相同议题均不生成稳定联盟。

本报告作为 10 条人工决定的回交记录；中央表、HR CSV、source log 与图表仍留待主线程统一合并。
