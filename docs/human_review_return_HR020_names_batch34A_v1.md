# HR-020 R5 名称、别名与名单切分复核回交报告 Batch 34A

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R05_coaction_v1/hr020_review_queue_v0.csv`  
本批范围：HR020-01 至 HR020-08，共 8 项  
状态：**负责人已确认——3 项 `accept`、5 项 `revise`**

## 0. 批次边界

- 本批只判断名单名称的同一性、别名、组织层级和切分。
- 2010／2020 名单本身只证明相应组织名称公开参加该次声明／请求，不证明稳定联盟、
  成员关系、资金关系、持续协调或共同组织。
- `source_name` 必须原样保留；规范名、英文别名和 actor key 是另外的字段。
- 独立查到组织存在不自动授权加入 registry；HR-020 只决定 R5 名单身份连接。
- 严格重复参与统计只合并同一 actor；母体与下属／现场团队只记录组织层级关系，
  不应为了提高重复数而强行合并。
- 本报告不修改 HR CSV、actor registry、alias 表、AEV、关系表、图或正文，留待主线程统一合并。

## 1. 辅助建议总表

| queue_id | 辅助建议 | 结论 |
|---|---|---|
| HR020-01 | `revise` | AOCHR 是 `沖縄国際人権法研究会`，不是 A054 `沖縄人権協会` |
| HR020-02 | `revise` | `Anti-war Network` 是爱知／名古屋的 `不戦へのネットワーク`，不是 A008 `NGO非戦ネット` |
| HR020-03 | `revise` | 对应 `基地のない平和で豊かな沖縄をめざす会・大阪`，不是已判定退役的 A072 |
| HR020-04 | `accept` | 罗马字逐词对应 A110 `辺野古に基地を絶対つくらせない大阪行動` |
| HR020-05 | `revise` | 对应 `Stop!辺野古埋め立てキャンペーン`，不是 A106 首都圏連絡会 |
| HR020-06 | `accept` | 缺失分隔符，应切为两个独立组织，保持 67 行 |
| HR020-07 | `accept` | 2010 日文名与 2020 英文名是同一二见以北十区组织 |
| HR020-08 | `revise` | 2020 英文名指现场调查队 `北限のジュゴン調査チーム・ザン`；与 2010 母体有关联但不是严格别名 |

建议分布：

- `accept`：3 项；
- `revise`：5 项；
- `reject`：0 项。

这里使用 `revise` 而不是简单 `reject`，是因为五项都已查到更准确的日文实体或组织层级；
修订后仍可保留来源所证明的事件参与，但不得连接到错误 actor。

## 2. HR020-01 · AOCHR 不是 A054 沖縄人権協会

### 调查结果

AOCHR 自有页面的发布账号、日文署名及独立组织介绍一致指向：

> 沖縄国際人権法研究会  
> All Okinawa Council for Human Rights (AOCHR)

其自有页面说明它以 AOCHR 名义参与联合国普遍定期审议、任意拘禁工作组等国际人权程序；
页面署名和 Blogger 账号均为 `沖縄国際人権法研究会`。恣意的拘禁网络的组织介绍进一步记载：

- 日文名为 `沖縄国際人権法研究会`；
- 英文名为 `All Okinawa Council for Human Rights/AOCHR`；
- 2016 年由研究者、记者和市民成立；
- 目的为从国际人权法角度检验冲绳问题并向国际社会报告。

这与 A054 `沖縄人権協会` 不同。项目既有调查把 A054 的历史追至 1961 年，并确认其 2019
年第 56 次总会；两者的日文名、成立年代、活动形式和公开身份均不同。

### 辅助建议

**`revise`。**

- P012 `source_name` 原样保留 `All Okinawa Council for Human Rights (AOCHR)`；
- canonical identity 修订为 `沖縄国際人権法研究会`；
- 不连接 A054；
- 在 HR-020 层保留为已识别的 event-only organization；
- 若以后按模块价值考虑纳入 registry，必须另开 registry gate，不在本批自动新增 actor；
- 2020 MMC 请求只证明该次公开参与，不把 AOCHR 的所有联合国活动转给其他共同署名者。

来源：

- https://allokinawahr.blogspot.com/
- https://naad.info/about_naad/
- https://hrn.or.jp/eng/news/2016/09/20/okinawa-hrc-statement/

## 3. HR020-02 · Anti-war Network 不是 A008 NGO非戦ネット

### 调查结果

A008 自己的英文页面使用的正式英文名是：

> NGO NO WAR NETWORK

而不是 `Anti-war Network`。更关键的是，2020 年另一份由日本国际志愿中心发布的英文声明
把 `Anti-War Network` 的代表明确写为 `Shigeaki IIJIMA`。爱知／名古屋组织
`不戦へのネットワーク` 的自有页面和行动记录则明确：

- 代表为饭岛滋明；
- 以爱知、名古屋为主要活动场域；
- 联系邮箱使用 `husen@jca.apc.org`；
- 英文外部材料持续使用 `Anti-War Network`；
- 2015 边野古英文署名表也出现 `anti-war-network`。

因此 2020 MMC 名单中的 `Anti-war Network` 与 A008 的正式英文名不符，却与
`不戦へのネットワーク` 的英文自称、代表和地域脉络闭合。项目 HR-002 也已经认定 S005
过去对 A008 的映射错误，不能借 HR-020 恢复。

### 辅助建议

**`revise`。**

- P044 `source_name` 原样保留 `Anti-war Network`；
- canonical identity 修订为 `不戦へのネットワーク`；
- 不连接 A008；
- 作为已识别 event-only organization 保留；
- 不因名称中的 Network 推定其成员团体或与其他签署者形成网络关系；
- A008 的 2019 边野古县民投票声明仍按既有人审保留，但不是本次 2020 参与的证据。

来源：

- A008 官方英文页：https://ngo-nowar.org/english/
- 不戦へのネットワーク：https://www.jca.apc.org/~husen/index.htm
- JVC 英文声明：https://www.ngo-jvc.com/en/blogs/2020/02/14/we-call-on-the-japanese-government-to-mediate-negotiation-efforts-in-relation-to-tensions-between-the-u-s-and-iran/
- 2015 边野古英文署名：https://www.foejapan.org/en/aid/151013.html

## 4. HR020-03 · 不是 A072，而是大阪组织的跨年名称

### 调查结果

HR-025 已经确认：

- A071 `沖縄平和市民連絡会` 是
  `沖縄から基地をなくし世界の平和を求める市民連絡会` 的简称；
- A072 是 A071 的重复键，应退役；
- S031 `沖縄平和運動センター` 不能支持 A071／A072。

2020 `The Association for Military Base Free Peaceful Okinawa` 位于名单的日本／菲律宾部分，
不是冲绳本地组织部分。跨来源材料则反复把近似英文用于大阪组织：

> 基地のない平和で豊かな沖縄をめざす会・大阪

证据包括：

- 2010 WWF 名单 P018 已列 `基地のない平和で豊かな沖縄をめざす会大阪`；
- 2010 生物多样性 NGO 声明列 `基地のない平和で豊かな沖縄をめざす会・大阪`；
- 2011 CODEPINK 材料把芳泽章子写作该大阪组织共同代表，英文为
  `the Osaka Association for military base free peaceful Okinawa`；
- 2015 FoE 英文名单使用 `the Osaka Association for military base free peaceful Okinawa`；
- 2024／2025 日本材料仍把芳泽章子列为该会共同代表并在大阪活动。

2020 英文漏掉 `Osaka`，但独特名称、名单分区、长期英文译名和 2010 同一名单样本共同支持
它是上述大阪组织，而不是冲绳的 A071／A072。

### 辅助建议

**`revise`。**

- P068 `source_name` 原样保留；
- canonical identity 修订为 `基地のない平和で豊かな沖縄をめざす会・大阪`；
- 与 2010 P018 建立 event-only identity bridge，计为 2010／2020 重复公开参与；
- 不连接 A071 或 A072；
- 不自动把该 event-only bridge 升为 registry actor；
- 2020 来源遗漏 Osaka 应写入 alias note，不静默改写原文。

来源：

- https://www.jelf-justice.org/jelf/wp-content/themes/jelf-justice/backnumber/prefecture-map/documents/COP10-NGOjoint-statement.pdf
- https://www.foejapan.org/en/aid/151013.html
- https://www.codepink.org/messages_from_japan_solidarity_across_the_seas
- https://kakushinkon.org/activity/meeting/6895.html

## 5. HR020-04 · 大阪行动罗马字名对应 A110

### 调查结果

2020 名称：

> Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo

是 `辺野古に基地を絶対つくらせない大阪行動` 的逐词罗马字。该完全相同的罗马字串还出现在
2015 FoE 边野古英文署名名单。A110 的自有博客持续使用日文正式名；独立 IWJ 行动记录已由
HR-011 用于确认该大阪行动 actor。

同一份 2020 名单还另列 P066 `STOP！Henoko Shinkichikensetsu Osaka Action`，因此不能把
两个大阪行动名称合并；P051 的罗马字唯一、精确对应 A110。

### 辅助建议

**`accept`。**

- P051 连接 A110；
- 把该罗马字串记录为 source-attested transliteration alias；
- 只新增 A110 在 2020 MMC 请求中的一次公开参与；
- 不与 P066 合并，不从共同请求推定 A110 与其他签署者有稳定联盟。

来源：

- A110 官方博客：https://blog.livedoor.jp/henoko_osaka/
- 2015 FoE 英文名单：https://www.foejapan.org/en/aid/151013.html
- 2020 MMC 请求：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/Letter-of-Request-to-MMC-re.-Okinawa-Dugong-July-10-2020.pdf

## 6. HR020-05 · Stop! Henoko 不是 A106 首都圏連絡会

### 调查结果

项目 A106 是：

> 辺野古の海を土砂で埋めるな！首都圏連絡会

其博客标题有时使用 `首都圏キャンペーン`，但博客自述和独立报道均确认组织名为
`首都圏連絡会`。

另一方面，另有一个公开活动主体：

> Stop!辺野古埋め立てキャンペーン

它有独立博客。2020-12 的行动公告明确把二者分开：

- 呼びかけ：`Stop!辺野古埋め立てキャンペーン`；
- 協力：`辺野古の海を土砂で埋めるな！首都圏連絡会`。

这是一条直接的非同一证据。2020 MMC P065 的英文
`Stop! Henoko Reclamation Campaign` 与前者逐词对应，不能因为两者都反对边野古填海就连接
A106。

### 辅助建议

**`revise`。**

- P065 canonical identity 修订为 `Stop!辺野古埋め立てキャンペーン`；
- 不连接 A106；
- 保留为已识别 event-only organization；
- `首都圏キャンペーン／首都圏連絡会` 的 canonical variant 仍留给 HR-029，不由本项解决；
- 两组织公开协作只是一条具名 action/cooperation 证据，不等于同一 actor 或稳定联盟。

来源：

- A106 博客：https://henokoumeruna2018.exblog.jp/
- 独立 Stop! 博客：https://stop-henoko-umetate.blogspot.com/
- 两者分列的 2020 公告：https://stop-henoko-umetate.blogspot.com/2020/12/blog-post_25.html
- A106 独立记录：https://www.jawan.jp/rept/rp2019-j129/4.html

## 7. HR020-06 · 2010 缺失分隔符应切为两个组织

### 调查结果

WWF 和日本野鸟会镜像都把以下字符串连写：

> 憲法ひろば・杉並福岡地区合同労働組合

但两页都声明共有 67 个团体；按逗号机械切分只有 66 项。外部材料独立确认两端均为真实组织：

- `憲法ひろば・杉並` 至少在 2007–2010 年有活动记录，2008 年一周年活动明确使用该名，
  2010 年其他声明也单独列名；
- `福岡地区合同労働組合` 是 1976 年成立的个人加盟型劳动组合，厚生劳动省劳动委员会命令、
  法人信息和自有活动页面均独立确认其名称。

没有材料显示存在一个跨杉并与福冈、名称恰为连写串的单一组织。两个独立组织加上来源自称总数
67，足以确认是网页漏掉分隔符。

### 辅助建议

**`accept`。**

- 保留 P060 `憲法ひろば・杉並`；
- 保留 P061 `福岡地区合同労働組合`；
- 2010 结构化名单保持 67 行；
- 在 provenance 记录 `source_missing_delimiter_human_confirmed`；
- 两组织均保持 event-only，不因本次切分自动加入 registry；
- `福岡地区合同労働組合` 的实体类型可记为 `labor_union`，与负责人已确认的精简组织类型一致。

来源：

- https://kunyon.com/shucho/080922.html
- https://sarutora.hatenablog.com/entry/20100327/p1
- https://www.mhlw.go.jp/churoi/meirei_db/mei/pdf/m02476.pdf
- https://blog.livedoor.jp/white0wolf-fukuokagoudou/

## 8. HR020-07 · 二见以北十区日英名是同一组织

### 调查结果

1999 年该组织自己的募款页面明确使用：

> ヘリ基地いらない二見以北十区の会

并说明它由名护市东海岸二见区以北各区的居民志愿者构成。之后的来源持续使用同一日文名。

英文材料形成连续交叉：

- OEJP 2016 材料使用
  `“No Heliport Base” Association of 10 Districts North of Futamai`；
- Mission Blue／NACSJ 英文材料使用同一英文形式；
- 2020 MMC P019 使用同一英文名；
- 2016 同一请求的日文版把该签署者写作 `ヘリ基地いらない二見以北十区の会`；
- 2021 NACSJ 正式陈情书继续以日文名列该组织及代表。

`Futamai` 是来源持续沿用的英文拼写，但日文地名为 `二見/Futami`。不应修正
`source_name`，可在规范化 alias note 中注明。

### 辅助建议

**`accept`。**

- 合并 2010 P010 与 2020 P019 为同一 event-only identity bridge；
- canonical name 使用 `ヘリ基地いらない二見以北十区の会`；
- 英文来源名原样保留，另记 `Futamai is source spelling for Futami/二見`；
- 进入 2010／2020 严格重复公开参与表；
- 不由跨年两次名单出现推定其十年间持续活动的每一年、完整成员或稳定联盟。

来源：

- https://www.jca.apc.org/HHK/Heliport/99/futami_campaign9911.html
- https://okinawaejp.blogspot.com/2016/12/launched-in-november-2016-okinawa.html
- https://www.nacsj.or.jp/official/wp-content/uploads/2019/10/MissionBlue_Henoko-ouraBay-hopespot-pressreleas-en.pdf
- https://www.nacsj.or.jp/archives/uploads/2021/03/20210305_ourabay-NaturalTreasure_chinjyo.pdf

## 9. HR020-08 · 见守会与 Team Zan 是母体／现场队关系

### 调查结果

2020 英文名：

> Protect Northernmost Dugong Team Zan

明确包含 `Team Zan`。日文公开材料对组织层级的表达并不完全统一，但核心关系清楚：

- 冲绳县地域环境中心把 `北限のジュゴンを見守る会` 列为 1999 年成立的任意团体，
  并说明东京事务局与在儒艮生息现场设立的 `調査チーム・ザン` 协作；
- NACSJ 2013 报告把 `北限のジュゴンを見守る会` 与
  `北限のジュゴン調査チーム・ザン` 并列；
- 2016 JELF 赞同团体名单也把两者分别列名；
- 其他 NACSJ 材料使用过合成形式 `北限のジュゴンを見守る会チーム・ザン`；
- 铃木雅子的公开署名同时标示她为见守会代表和 Team Zan 成员／代表。

因此它们不是互不相干的组织，但也不是可以无条件互换的严格别名。最安全的模型是：

`北限のジュゴンを見守る会`（母体／东京事务局）  
→ `北限のジュゴン調査チーム・ザン`（冲绳现场调查队）

2010 P013 只列母体名称；2020 P009 明确列 Team Zan。严格 actor 重复统计不应把母体和下属队
自动算作同一节点。

### 辅助建议

**`revise`。**

- 2010 P013 canonical identity 保持 `北限のジュゴンを見守る会`；
- 2020 P009 canonical identity 修订为 `北限のジュゴン調査チーム・ザン`；
- 两行不合并为严格 event-only identity bridge，不计入严格 2010／2020 重复 actor；
- 可另记 `organizational_unit_of / affiliated_field_team` 候选关系，但不得写成联盟或两个完全独立、
  无关系组织；
- 如未来 registry 需要母体／下属队建模，应另做 actor-level gate。

来源：

- https://kankyo-center.okinawa/environmental-organization-facility/%E5%8C%97%E9%99%90%E3%81%AE%E3%82%B8%E3%83%A5%E3%82%B4%E3%83%B3%E3%82%92%E8%A6%8B%E5%AE%88%E3%82%8B%E4%BC%9A
- https://what-we-do.nacsj.or.jp/2013/09/486/
- https://www.jelf-justice.org/jelf/wp-content/themes/jelf-justice/backnumber/aboutjelf/contents/documents/20160217henokoopinionlist.pdf
- https://congrant.com/project/takagifund/5103/reports/390

## 10. 本批对 R5 计数的预期影响

若负责人采用以上建议：

- A054、A008、A072、A106 均不获得错误的 2020 参与；
- A110 获得一条 2020 事件参与；
- 2010 名单保持 67 行；
- 二见以北十区新增一个严格 2010／2020 event-only 重复桥；
- 大阪 `基地のない平和で豊かな沖縄をめざす会・大阪` 新增一个严格 2010／2020
  event-only 重复桥；
- 见守会／Team Zan 只形成组织层级关系，不增加严格重复 actor；
- AOCHR、不戦へのネットワーク、Stop!辺野古埋め立てキャンペーン得到正确的 event-only 身份，
  但不自动进入 registry。

具体总数必须在主线程回填后由脚本重算；本报告不手工覆盖现有 R5 图表数字。

## 11. 建议负责人本批判断

建议一次确认：

- HR020-01 `revise`
- HR020-02 `revise`
- HR020-03 `revise`
- HR020-04 `accept`
- HR020-05 `revise`
- HR020-06 `accept`
- HR020-07 `accept`
- HR020-08 `revise`

## 12. 负责人确认

负责人于 2026-07-20 确认采用本报告全部建议：

- HR020-01、02、03、05、08 为 `revise`；
- HR020-04、06、07 为 `accept`；
- 错误的 A054、A008、A072、A106 映射不得进入 2020 参与层；
- A110 可连接 2020 事件，2010 名单保持 67 行；
- 二见以北十区建立严格 event-only 跨年桥；
- 见守会与 Team Zan 保留母体／现场调查队层级，不作为严格同一 actor；
- 本次确认不批准稳定联盟、成员关系、资金关系、长期连续性或 registry 新增。

HR-020 累计完成 **8/14**，剩余 HR020-09 至 HR020-14 共 6 项。
