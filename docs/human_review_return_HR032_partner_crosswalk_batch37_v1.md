# HR-032 partner alias／复合体 crosswalk 人工复核回交报告 Batch 37

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R10_official_collaboration_universe_v1/HR032_partner_alias_crosswalk_review_v1.csv`  
本批范围：HR-032 全部 8 项  
状态：**负责人已确认——2 项 accept_display_alias_only、1 项 accept_member_crosswalk_only、5 项 revise**

## 0. 本批判断边界

- 本批判断来源名称能否归到同一法人、既有 actor、办事机构或项目共同体成员。
- 本批不自动新增 actor，不批准行政关系边，不批准资金／支付关系，也不把共同企业体项目费拆给成员。
- S002 的 `事业费` 保持整项事业口径；只有另有合同记录时才能单列合同金额。
- 复合主体的原始 source cell 永久保留，成员展开只能进入独立 crosswalk 层。
- 当前两张 616-row source-universe 图继续按来源行和机器显示标签统计，不等待本批。
- 本报告不回填 HR CSV，不修改中央 registry、relation table、source log 或图，留待主线程统一合并。

## 1. 辅助建议总表

| item | 辅助建议 | 建议冻结／crosswalk | 关键限制 |
|---|---|---|---|
| HR032-01 | `accept_display_alias_only` | 两种写法统一显示为 `社会福祉法人沖縄県社会福祉協議会` | 只是法人前缀省略；不自动进 registry |
| HR032-02 | `revise` | 两行归同一 `公益財団法人沖縄県平和祈念財団`；保留原始 kind，另记 row496 类别冲突 | 不与ひめゆり财团混同；241,109 千円不是付款 |
| HR032-03 | `revise` | rows197/205/206 归女性财团；row207 保留管理运营共同体，并记录财团是成员 | 不与 A111 或已移出的 A094 混同 |
| HR032-04 | `accept_display_alias_only` | 三行 crosswalk 到 A088；冻结日文名、英文名和 OPAC | actor crosswalk 不等于自动批准三条关系 |
| HR032-05 | `accept_member_crosswalk_only` | JOCA 冲绳是母法人办事机构；三个 JV 名称分别保留，JOCA 只作成员 | 办事机构不是独立法人；项目费不得拆分 |
| HR032-06 | `revise` | rows433/571 归同一 WYUA；row434 保留 Team OKIYUA，并记录 WYUA 是成员 | 同时包含 alias 与 member 两种处理，不能整项只作名称合并 |
| HR032-07 | `revise` | 四行归同一持续组织 `沖縄県ユネスコ協会`；暂按任意团体处理 | row545 的 NPO法人类别疑为来源编码错误，保留 raw 值并标注冲突 |
| HR032-08 | `revise` | 四行归同一 NPO 法人；row466 仅保留为来源表事实，角色待项目级证据 | 不写成施工监理承包、付款或已解释的跨部门桥梁 |

建议分布：

- `accept_display_alias_only`：2 项；
- `accept_member_crosswalk_only`：1 项；
- `revise`：5 项；
- `keep_separate`：0 项；
- `defer`：0 项。

## 2. 逐项调查与建议

### 2.1 HR032-01 · 沖縄県社会福祉協議会

辅助建议：**`accept_display_alias_only`**。

S002 中的：

- `社会福祉法人沖縄県社会福祉協議会`；
- `沖縄県社会福祉協議会`

是同一法人的正式全称与省略法人前缀写法。机构官网使用正式名 `社会福祉法人 沖縄県社会福祉協議会`；WAM 法人公开系统可进一步确认该法人及法人编号 `4360005000294`。

建议：

- `approved_display_name=社会福祉法人沖縄県社会福祉協議会`；
- 两种来源写法允许在报告级别合并；
- 保留 literal source label；
- `registry_crosswalk_decision=display_alias_only_no_registry_entry`。

合并后，高频 partner-label 统计可以从分开的 20＋4 行改为同一显示实体的 24 行，但不能因此自动创建 actor 或行政关系。

来源：

- https://www.okishakyo.or.jp/html/about/
- https://www.wam.go.jp/wamnet/zaihyoukaiji/pub/PUB0201000E00.do?_FORMID=PUB0219000&vo_headVO_corporationId=1647119476

### 2.2 HR032-02 · 沖縄県平和祈念財団

辅助建议：**`revise`**。

S002 两行使用完全相同的法人名称：

- row 9：平和祈念资料馆相关业务，partner kind 2；
- row 496：平和祈念公园指定管理，partner kind 3，事业费 241,109 千円。

gBizINFO 确认 `公益財団法人沖縄県平和祈念財団` 是单一法人，法人编号 `4360005001441`，所在地为糸满市摩文仁 444。冲绳县的指定管理资料也把该财团列作相关设施管理者。因此，没有证据支持把两行解释成两个同名主体。

kind 2／3 应按“同一法人、来源表类别冲突”处理：

- 公益财团法人的法律类别与 kind 2 相符；
- row496 的 kind 3 不应据此制造第二主体；
- 保留 row496 原始 kind 值，同时加 `source_partner_kind_conflict` 说明；
- 不静默改写 S002 原表。

它必须与运营姬百合和平祈念资料馆的另一法人区分：

`公益財団法人沖縄県女師・一高女ひめゆり平和祈念財団`

后者有时简称 `公益財団法人ひめゆり平和祈念財団`，不是本项财团。

建议：

- `approved_display_name=公益財団法人沖縄県平和祈念財団`；
- rows9/496 归同一法人；
- `registry_crosswalk_decision=same_legal_entity_no_registry_entry`；
- row496 的 241,109 千円继续只写“来源表事业费”，不能写成向财团支付金额。

来源：

- https://info.gbiz.go.jp/hojin/ichiran?hojinBango=4360005001441
- https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/023/476/r60401shiteikanriitiran.pdf
- https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/031/750/1126_otugou.pdf
- https://www.himeyuri.or.jp/establish/basic_info/

### 2.3 HR032-03 · おきなわ女性財団与男女共同参画中心管理运营共同体

辅助建议：**`revise`**。

rows197/205/206 的相手方是：

`公益財団法人おきなわ女性財団`

row207 则写为：

`公益財団法人おきなわ女性財団（沖縄県男女共同参画センター管理運営団体）`

女性财团官网说明，该财团长期承担男女共同参画中心相关业务；但其沿革同时明确，2009 年起曾与 ACO 冲绳组成管理运营团体。冲绳县最新指定管理选择结果也把 `沖縄県男女共同参画センター管理運営団体` 明确列为共同体，并列出当期成员：

- `株式会社かりゆしエンターテイメント`；
- `公益財団法人おきなわ女性財団`。

因此，row207 的括号不是可以直接删掉的职能说明。它指向设施管理复合主体，女性财团是其中成员。

建议分层：

- rows197/205/206 → `公益財団法人おきなわ女性財団`；
- row207 → 保留 `沖縄県男女共同参画センター管理運営団体` 这一 composite；
- 另建 `公益財団法人おきなわ女性財団 member_of_composite 管理運営団体` crosswalk；
- 不把 row207 的事业费拆给女性财团或其他成员；
- 不把财团、设施和管理共同体互相替代。

还应明确：

- 它不是 A111 `沖縄県女性団体連絡協議会`；
- 它不是已经移出一期 registry 的 A094 `一般社団法人沖縄県女性連合会`；
- S002 出现该财团不构成恢复 A094 的理由。

来源：

- https://www.okinawajosei.org/about.php
- https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/005/128/01senteikekka_r06.pdf
- https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/015/322/zaienn.pdf

### 2.4 HR032-04 · 沖縄平和協力センター／A088／OPAC

辅助建议：**`accept_display_alias_only`**。

S002 rows10/11/501 均使用正式名：

`特定非営利活動法人沖縄平和協力センター`

该名称与中央 registry 的 A088 完全一致。JICA 官方页面给出英文名称 `Okinawa Peace Assistance Center` 和缩写 `OPAC`；gBizINFO 确认法人编号 `2360005001229`。

建议冻结：

- 日文 canonical：`特定非営利活動法人沖縄平和協力センター`；
- English：`Okinawa Peace Assistance Center`；
- abbreviation：`OPAC`；
- rows10/11/501 → A088。

`registry_crosswalk_decision=A088_same_legal_entity`

这里接受的是身份 crosswalk。三项行政项目能否全部进入 actor-level relation layer，仍须继承 HR-018 的关系决定；不能由 HR-032 自动建边。

来源：

- https://www.jica.go.jp/domestic/okinawa/activities/kaihatsu/festival/2022/organization_02/08.html
- https://info.gbiz.go.jp/hojin/ichiran?hojinBango=2360005001229
- https://www.peace-museum.okinawa.jp/umui%28bosyuu%29/index.html

### 2.5 HR032-05 · JOCA 冲绳事务所与三个共同企业体

辅助建议：**`accept_member_crosswalk_only`**。

S002 的相关层级为：

- row432：`令和６年度おきなわ国際協力人材育成事業共同企業体`；
- row435：`公益社団法人青年海外協力協会沖縄事務所` 单独出现；
- row436：`令和６年度ウチナージュニアスタディー事業に係る共同企業体`；
- row438：`令和６年度長野県への生徒派遣交流事業共同企業体`。

JICA 官方资料确认，JOCA 冲绳是 `公益社団法人青年海外協力協会` 的冲绳办事机构，不是另一个法人。三个共同企业体则是各自项目期复合主体，不能因为共享 JOCA 成员而互相合并。

建议冻结：

- 母法人 canonical：`公益社団法人青年海外協力協会`；
- 办事机构 display：`公益社団法人青年海外協力協会沖縄事務所（JOCA沖縄）`；
- row435 作为母法人冲绳办事机构的单独 source appearance；
- rows432/436/438 保留三个不同 JV 名称；
- 各 JV 另建 JOCA 冲绳的 `member_of_composite` crosswalk。

HR-018 Batch 20 已确认：共同体成员串只支持成员说明，不能把整项事业费或合同额分配给 JOCA。

来源：

- https://www.jica.go.jp/domestic/okinawa/activities/kaihatsu/festival/2021/organization_02/02.html
- https://www.mofa.go.jp/mofaj/gaiko/oda/sanka/demae/page22_000635.html

### 2.6 HR032-06 · 世界若者ウチナーンチュ連合会与 Team OKIYUA

辅助建议：**`revise`**。

WYUA 官网确认正式日文名称：

`一般社団法人世界若者ウチナーンチュ連合会`

英文名为：

`World Youth Uchinanchu Association`

该团体 2011 年作为任意团体起步，2015-07-17 法人化。因而：

- row433 的全称；
- row571 省略 `一般社団法人` 的名称

可以归到同一现存法人。

但 row434 的合同相手方是项目共同体 `Team OKIYUA`，同一 source cell 明列：

- `株式会社沖縄映像センター`；
- `一般社団法人世界若者ウチナーンチュ連合会`。

建议：

- rows433/571 → `一般社団法人世界若者ウチナーンチュ連合会`；
- row434 → 保留 `Team OKIYUA` composite；
- WYUA 只以 `member_of_composite` 连接 Team OKIYUA；
- 不把 Team OKIYUA 直接改名为 WYUA；
- 不把 Team OKIYUA 合同额或事业费拆给 WYUA。

由于本项同时包含 display alias 合并和 member crosswalk，单一 `accept_display_alias_only` 或 `accept_member_crosswalk_only` 都不完整，故建议 `revise`。

来源：

- https://wyua.okinawa/organization/
- https://www.jica.go.jp/overseas/peru/activities/nikkei/__icsFiles/afieldfile/2025/10/14/39.%20%E6%B2%96%E7%B8%84_%E3%82%A6%E3%83%81%E3%83%8A%E3%83%BC%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E6%B4%BB%E7%94%A8%E3%81%97%E3%81%9F%E6%8C%81%E7%B6%9A%E5%8F%AF%E8%83%BD%E3%81%AA%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3%E3%83%BC%E9%81%8B%E5%96%B6.pdf

### 2.7 HR032-07 · 沖縄県ユネスコ協会

辅助建议：**`revise`**。

S002 四行使用完全相同的名称，且项目与冲绳县官网所列该协会持续活动吻合：

- row529：平和の鐘／平和学习；
- row545：ユネスコ子どもの集い；
- row548：书きそんじハガキ campaign；
- row551：SDGs passport symposium。

冲绳县官网称该协会成立于 1959 年，并介绍上述核心活动；日本ユネスコ協会連盟也把它列为地区协会。现有材料足以支持“四行为同一持续组织”。

法律类别却有冲突：

- rows529/548/551：kind 8，法人格を持たない任意団体；
- row545：kind 1，NPO法人。

本轮未在官方 NPO 法人门户或 gBizINFO 找到该协会的法人记录，冲绳县自身的协会介绍也没有称其为 NPO 法人。因此，现阶段较可信的处理是任意团体，row545 很可能是来源表类别误码。

建议：

- `approved_display_name=沖縄県ユネスコ協会`；
- 四行归同一持续组织；
- `legal_status=unincorporated_voluntary_association`；
- 保留 row545 的 raw kind 1；
- 增加 `source_kind_conflict_probable_miscoding`；
- 在取得法人登记反证前，不写成 `特定非営利活動法人`。

机制仍须分开：

- rows529/545/548 是 C6 后援；
- row551 是 C4 补助；
- row551 的 28 千円仍是来源表事业费，不能仅凭本批改写为支付额。

来源：

- https://www.pref.okinawa.jp/kyoiku/shogaigakushu/1009501/1009543/1009545.html
- https://www.unesco.or.jp/aboutus/list/

### 2.8 HR032-08 · レインボーハートokinawa与 row466 异常

辅助建议：**`revise`**。

内阁府 NPO 法人门户确认正式法人名：

`特定非営利活動法人レインボーハートokinawa`

法人于 2021-02-10 获认证，所在地为那霸市。组织官网也确认其持续从事 LGBTQ／性别多样性教育、研修和咨询。S002 中空格、换行和 `NPO法人`／`特定非営利活動法人` 差异可以归一化，四行可 crosswalk 到同一法人：

- row204：性多样性理解促进启发业务；
- row466：首里城公园龙潭周边公共厕所新建工程监理业务；
- row499：县立学校事务职员 LGBTQ 研修；
- row591：在线 rainbow 讲座。

row466 不能简单作为抽取错误删除。本轮已对 S002 PDF p.64 做视觉核验，名称和项目确实同处官方原表；FY2023 的同类官方表也连续列出该法人和另一个无障碍组织参与相同厕所项目。

同时，row466 仍缺项目级外部材料解释该法人到底承担：

- 性别中立厕所设计咨询；
- 使用者／当事人意见提供；
- 一般监理；
- 还是其他协作角色。

该组织确有公共厕所与跨性别使用压力方面的公开倡议，宫古岛市教育资料也记录其向学校提出把无障碍厕所同时作为 all-gender toilet 使用的建议。这使咨询参与“具有可能性”，但不能替代本项目的职责证据。

建议：

- 四行身份归同一法人；
- rows204/499/591 可按官方表所写职能分别使用；
- row466 保留为 `official_source_row_fact`；
- row466 角色暂记 `unexplained_other_or_advisory_candidate`；
- 在取得项目级资料前，不写成施工监理承包商、工程实施者、收款者，或已经解释清楚的跨部门行政桥梁；
- C10 和零事业费都不能写成合同付款。

来源：

- https://www.npo-homepage.go.jp/npoportal/list?fiscal_year_end_first=&fiscal_year_end_second=&fiscal_year_start_first=&fiscal_year_start_second=&ket=LGBT&order=asc&page=1&sort=open_updated_at
- https://rainbowheartokinawa.com/
- https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/004/917/2r6hp.pdf
- https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/004/917/r5hppdf.pdf
- https://www.city.miyakojima.lg.jp/soshiki/kyouiku/kouhoushi/2021/files/01/55_3.pdf
- https://rainbowheartprojectokinawa.com/

## 3. 合并时的结构化处理建议

负责人若确认本批，主线程可按以下顺序合并：

1. 保留 8 项所涉所有 literal source labels 和 composite source cells；
2. 新增 report-level canonical display／alias crosswalk；
3. 将 HR032-04 的三行映射到既有 A088；
4. 将 HR032-03/05/06 的成员关系写入独立 `member_of_composite` 层；
5. 对 HR032-02/07 添加来源类别冲突标志，不静默改 raw kind；
6. 对 HR032-08 row466 添加职责未释明标志；
7. 不从本批生成 actor-resource relation、payment、funding、alliance 或 actor-level centrality；
8. 合并后再重生 HR-029 schema／alias freeze，避免用旧 crosswalk 候选做最终冻结。

## 4. 负责人确认

负责人于 2026-07-20 确认本批全部 8 项建议：

- `accept_display_alias_only`：HR032-01、HR032-04；
- `accept_member_crosswalk_only`：HR032-05；
- `revise`：HR032-02、HR032-03、HR032-06、HR032-07、HR032-08；
- `keep_separate`／`defer`：0 项。

同时确认：

- canonical name 与法人前缀按本报告冻结；
- 女性财团、JOCA、WYUA 所涉共同体永久保留 composite source cell，成员只进入独立 crosswalk；
- A088 可接受三行身份 crosswalk，但不由本批自动批准关系边；
- 沖縄県ユネスコ協会暂按任意团体处理，row545 的 kind 1 保留为来源类别冲突；
- レインボーハートokinawa row466 只保留为官方来源表事实，取得项目级证据前不解释为施工监理承包、付款或已闭合的跨部门桥梁；
- 本批不新增 actor、payment、funding、alliance 或 actor-level centrality。

HR-032 全部 8 项人工决定完成。中央 HR CSV、registry、relation table、source log 与图仍留待主线程统一合并／重生。
