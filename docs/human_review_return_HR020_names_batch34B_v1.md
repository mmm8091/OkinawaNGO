# HR-020 R5 名称、别名与名单切分复核回交报告 Batch 34B

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源队列：`outputs/R05_coaction_v1/hr020_review_queue_v0.csv`  
本批范围：HR020-09 至 HR020-14，共 6 项  
状态：**负责人已确认——4 项 `accept`、2 项 `revise`**

## 0. 批次边界

- 本批只判断名单名称的同一性、别名、组织层级和切分。
- 2010／2020 名单只证明相应名称在特定声明／请求中公开出现，不证明稳定联盟、成员关系、
  资金关系、持续协调或共同组织。
- `source_name` 必须原样保留；规范名、英文别名和 actor key 是另外的字段。
- 独立查到组织存在不自动授权加入 registry；HR-020 只决定 R5 名单身份连接。
- 同一来源日英版本的同序号对照可以证明翻译对应，但错误或非正式英文译名不能替代组织自定英文名。
- 本报告不修改 HR CSV、actor registry、alias 表、AEV、关系表、图或正文，留待主线程统一合并。

## 1. 辅助建议总表

| queue_id | 辅助建议 | 结论 |
|---|---|---|
| HR020-09 | `accept` | `Pan-Seto Inland Sea Congress` 是環瀬戸内海会議自用英文名 |
| HR020-10 | `accept` | 2020 日英同序号确认同一组织；来源英文误用 `Conservation`，官方英文为 `Protection` |
| HR020-11 | `accept` | `Minshuku Yaponesia` 对应みん宿／民宿ヤポネシア；实体是家族经营小型宿泊设施，不自动视为 NGO |
| HR020-12 | `accept` | `Dugong no Sato` 是じゅごんの里的直接罗马字对应 |
| HR020-13 | `revise` | 2010 爱知组织与 2020 冲绳的命どぅ宝を継承する会不是同一组织 |
| HR020-14 | `revise` | “自然の権利”基金与 JELF 有紧密事务／人员协作，但有独立组织与财务边界，不是 A020 别名 |

建议分布：

- `accept`：4 项；
- `revise`：2 项；
- `reject`：0 项。

## 2. HR020-09 · 環瀬戸内海会議的日英对应

### 调查结果

環瀬戸内海会議现行自有网站在同一页并列：

> 環瀬戸内海会議  
> Pan-Seto Inland Sea Congress

旧网站和高木仁三郎市民科学基金的助成报告也使用同一英文名。名称不是对相似组织的推测性翻译，
而是该组织长期公开使用的日英对应。

### 辅助建议

**`accept`。**

- 合并 2010 P022 与 2020 P035 为同一 event-only identity bridge；
- canonical name 使用 `環瀬戸内海会議`；
- `Pan-Seto Inland Sea Congress` 记录为组织自用英文别名；
- 可计入严格 2010／2020 重复公开参与；
- 不因两次共同署名推定该组织与其他参与者存在稳定联盟。

来源：

- https://kanseto.net/
- https://www.jca.apc.org/~tukasa/pan-seto/pan-seto.htm
- https://www.takagifund.org/admin/img/sup/rpt_file10046.pdf

## 3. HR020-10 · 同一组织，但 2020 英文译名不是官方英文名

### 调查结果

海の生き物を守る会自有组织概要明确并列：

> 海の生き物を守る会  
> Association for Protection of Marine Communities (AMCo)

并记载该会于 2007 年 7 月 1 日成立。

2020 MMC 请求的日文版第 29 项是 `海の生き物を守る会`，英文版同一序号第 29 项是
`Association for Conservation of Marine Communities`。因此身份对应没有疑问，但英文版把
组织自定名称中的 `Protection` 写成了 `Conservation`。

这两层不能混在一起：

- 身份层：2010 和 2020 是同一组织；
- 名称层：2020 来源英文必须原样保存，但不应冻结为组织的正式英文名。

### 辅助建议

**`accept`。**

- 合并 2010 P032 与 2020 P029 为同一 event-only identity bridge；
- canonical name 使用 `海の生き物を守る会`；
- canonical English alias 使用
  `Association for Protection of Marine Communities (AMCo)`；
- 2020 `source_name` 原样保留
  `Association for Conservation of Marine Communities`，并标为
  `source_translation_variant`；
- 可计入严格 2010／2020 重复公开参与；
- 本项接受的是身份对应，不是接受错误英文为正式英文名。

来源：

- 组织概要：https://e-amco.com/aboutus
- 2020 日文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/d91ba4d8df8d1d9131fc0becc9b4e66c.pdf
- 2020 英文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/Letter-of-Request-to-MMC-re.-Okinawa-Dugong-July-10-2020.pdf

## 4. HR020-11 · ヤポネシア是同一宿泊实体，不自动编码为 NGO

### 调查结果

官方页面使用名称 `みん宿ヤポネシア`，并自述为冲绳县糸满市的“家族经营的小型宿”，主题为
“和平、自然、儿童”。2010 来源使用该自写形式；2020 日文版写作较常见的
`民宿ヤポネシア`，英文版同序号写作 `Minshuku Yaponesia`。

名称、地点和日英名单序号共同确认三种写法指向同一经营／活动实体。它确实参与过公共声明和行动，
但公开身份首先是宿泊设施，不应仅因参加声明就改写为 NGO。

### 辅助建议

**`accept`。**

- 合并 2010 P042 与 2020 P016 为同一 event-only identity bridge；
- canonical name 保持其自用形式 `みん宿ヤポネシア`；
- `民宿ヤポネシア` 与 `Minshuku Yaponesia` 记录为来源别名；
- 可计入严格 2010／2020 重复公开参与；
- entity note 记录为 `family-run small lodging / civic activity venue`；
- 不自动纳入 NGO registry，也不从其公共参与反推所有住宿经营活动具有政治属性。

来源：

- https://www.yaponesia.com/
- 2020 日文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/d91ba4d8df8d1d9131fc0becc9b4e66c.pdf
- 2020 英文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/Letter-of-Request-to-MMC-re.-Okinawa-Dugong-July-10-2020.pdf

## 5. HR020-12 · じゅごんの里的日英对应

### 调查结果

じゅごんの里的现行自有网站持续使用该名称，并说明该项目／经营体 2000 年成立，通过自然体验、
修学旅行和大浦湾介绍推进“不依赖基地的地域振兴”。2020 日文版第 3 项是 `じゅごんの里`，
英文版同序号为 `Dugong no Sato`。

英文名是日文名的直接罗马字，且同序号日英版本排除了误配的可能。

### 辅助建议

**`accept`。**

- 合并 2010 P066 与 2020 P003 为同一 event-only identity bridge；
- canonical name 使用 `じゅごんの里`；
- `Dugong no Sato` 记录为来源英文／罗马字别名；
- 可计入严格 2010／2020 重复公开参与；
- 本项不额外判定其法人资格，也不把活动目标外推为与所有共同署名者的稳定关系。

来源：

- https://www.dugongnosato.jp/
- 2020 日文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/d91ba4d8df8d1d9131fc0becc9b4e66c.pdf
- 2020 英文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/Letter-of-Request-to-MMC-re.-Okinawa-Dugong-July-10-2020.pdf

## 6. HR020-13 · 两个“命どぅ宝”组织不能跨年合并

### 调查结果

2020 MMC 请求的日文版第 20 项直接把英文
`Nuchi du Takara o keisyosurukai` 对应为：

> 命どぅ宝を継承する会

QAB 报道记载该会于 2013 年为实现和平的冲绳而成立；2013 年琉球新报报道也以该会为命どぅ宝
研讨会主办者。它是冲绳本地的战时记忆／和平传承团体。

2010 P055 则是另一个组织：

> 沖縄について考え連帯する「命どぅ宝」の会  
> 略称：「命どぅ宝」あいち

名古屋市市民活动推进中心的正式登记信息显示，该任意团体 1996 年成立，所在地在爱知县，活动范围
主要为名古屋市，宗旨包括学习冲绳历史文化并与冲绳县民交流。

两者的全名、成立时间、所在地和活动主体均不同。共享“命どぅ宝”表达不足以构成身份同一。
它们也都不同于 2022 年成立的 A018 `ノーモア沖縄戦 命どぅ宝の会`。

### 辅助建议

**`revise`。**

- 2010 P055 canonical identity 修订／规范为
  `沖縄について考え連帯する「命どぅ宝」の会（「命どぅ宝」あいち）`；
- 2020 P020 canonical identity 使用 `命どぅ宝を継承する会`；
- 不建立 2010／2020 identity bridge，不计为严格重复 actor；
- 两者均先保留为已识别 event-only organization；
- 不连接 A018；
- 如未来任何一者需进 registry，应另开 registry gate。

来源：

- 2020 日文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/d91ba4d8df8d1d9131fc0becc9b4e66c.pdf
- 2020 英文名单：https://www.jelf-justice.org/jelf/wp-content/uploads/2020/07/Letter-of-Request-to-MMC-re.-Okinawa-Dugong-July-10-2020.pdf
- 爱知组织正式登记：https://www.n-vnpo.city.nagoya.jp/groupsearch/grouplist/135/
- 冲绳组织成立报道：https://www.qab.co.jp/news/2014042553325.html
- 2013 研讨会报道：https://ryukyushimpo.jp/news/prentry-214730.html

## 7. HR020-14 · “自然の権利”基金不是 JELF 别名

### 调查结果

2010 NACS-J 声明在同一赞同名单中相邻但分别列出：

- `日本環境法律家連盟（JELF）`
- `「自然の権利」基金`

这已经是强烈的“同一事件中被当作两个参与主体”证据。名单下方的 JUCON 联系方式写作
`「自然の権利」基金/JELF気付`，只能证明共同事务联系，不能推翻名单的双列结构。

基金自己的组织材料进一步显示它具有独立组织边界：

- 有自己的代表、理事、监事、事务局长和会员；
- 有自己的章程、入会费、年会费和捐款账户；
- 有独立活动报告《「自然の権利」基金通信》；
- 有自己的预算、决算、资产、诉讼援助金和ジュゴン专项收支；
- 2016 年 2 月 1 日独立法人化为 `一般社団法人自然の権利基金`。

JELF 和基金确实存在紧密关联：

- 部分理事／事务局人员重叠；
- 地址和事务联系曾共用；
- JELF 旧年度报告描述过一种功能分工：JELF 提供诉讼信息与弁護団支持，基金提供资金。

因此最准确的结构不是“完全无关”，也不是“基金是 A020 的别名／一个可折叠项目”，而是两个具有
独立边界、长期协作且人员／事务部分重叠的组织。

### 辅助建议

**`revise`。**

- 2010 P017 保留为独立 event-only organization：
  `「自然の権利」基金`；
- 不连接 A020 JELF，不把它计作 A020 在同一事件中的第二个名称；
- 2010 事件中 JELF 与基金各保留一条参与记录；
- 可另记一条谨慎的组织关系候选：
  `administrative_and_litigation-support collaboration / overlapping personnel`；
- 不使用 `alias_of`、`organizational_unit_of` 或 `project_of`；
- 2016 年后的法人名 `一般社団法人自然の権利基金` 可作为连续性／法人成立注记，
  但本项不自动把该组织加入 registry；
- 关系描述不得扩张为稳定政治联盟或把基金资助自动写成对本名单其他组织的资助。

来源：

- 2010 NACS-J 声明及双列名单：https://www.nacsj.or.jp/statement/51026/
- 基金组织页：https://www.f-rn.org/whats/organization.html
- 基金通信第 74 号、财务与法人化报告：https://f-rn.org/backnumber/documents/kikintuushin74.pdf
- JELF 旧年度活动报告：https://www.jelf-justice.org/jelf/wp-content/themes/jelf-justice/backnumber/aboutjelf/jelfact07.htm
- 法政大学大原社会问题研究所资料目录：https://oisr-org.ws.hosei.ac.jp/wp/wp-content/uploads/0007_20240828.pdf

## 8. 本批对 R5 的预期影响

若负责人采用以上建议：

- 新增四个严格 2010／2020 event-only identity bridge：
  - 環瀬戸内海会議；
  - 海の生き物を守る会；
  - みん宿ヤポネシア；
  - じゅごんの里；
- `命どぅ宝` 候选桥被拆除为爱知组织与冲绳组织，不增加严格重复 actor；
- “自然の権利”基金作为独立事件参与者保留，不折叠进 A020；
- 不新增 registry actor；
- 不批准联盟、成员、资助、持续协调或共同组织关系。

具体 R5 数字必须在主线程回填后由脚本重算；本报告不手工覆盖既有图表数字。

## 9. 建议负责人本批判断

建议一次确认：

- HR020-09 `accept`
- HR020-10 `accept`
- HR020-11 `accept`
- HR020-12 `accept`
- HR020-13 `revise`
- HR020-14 `revise`

## 10. 负责人确认

负责人于 2026-07-20 确认采用本报告全部建议：

- HR020-09、10、11、12 为 `accept`；
- HR020-13、14 为 `revise`；
- 四组 2010／2020 event-only 身份桥可建立，但不自动进入 registry；
- 两个“命どぅ宝”组织保持分离；
- “自然の権利”基金与 A020 JELF 保持实体分离，仅可记录谨慎的事务／诉讼支持协作和人员重叠；
- 本次确认不批准稳定联盟、成员关系、对其他共同署名者的资助关系或长期连续活动推断。

HR-020 已完成 **14/14**。全部人工复核剩余量从 86 降至 **80**；可立即在线处理的
非依赖项从 35 降至 **29**，下一批转入 HR-016。
