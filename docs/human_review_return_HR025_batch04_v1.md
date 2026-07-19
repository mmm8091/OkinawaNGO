# HR-025 关键地点语义回交报告 Batch 04

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——11/11 项决定**

## 0. 批次边界

- 本批只复核 11 条 actor–place 候选边，优先处理嘉手纳／宜野湾、边野古—大浦湾和先岛关键地点。
- 复核对象是地点键是否成立，以及应在 `headquarters`、`site_presence`、`event_site`、`advocacy_target`、`institutional_venue`、`unclear` 中使用哪一种语义。
- 接受地点边不批准组织间联盟、议题立场、行动效果、因果关系、事件完整事实或长期代表性。
- 本报告不直接修改中央 actor–place 表、place registry、source log、archive manifest 或 HR CSV。

## 1. 建议结论总表

| 项目 | 当前候选 | 辅助建议 | 核心理由 |
|---|---|---|---|
| AP088 | A052→P018 Ginowan `unclear` | `reject_edge`／`retire_candidate` | S026 只证明嘉手纳基地周边居民诉讼，没有宜野湾地点依据；A052→P005 Kadena 的 AP087 已另行存在 |
| AP106 | A065→P012 Ishigaki `site_presence` | `reject_edge`／`retire_candidate` | S036 把 A065 与八重山大地会列为两个共同交涉团体，不能据此推定 A065 有“石垣节点” |
| AP107 | A065→P013 Miyako `site_presence` | `revise`→`event_site` | 找到 2016 年宫古岛活动中 A065 共同代表登台的直接报道；只支持有界事件，不支持常设节点 |
| AP108 | A065→P011 Yonaguni `site_presence` | `accept_with_revision` | 2016、2023 材料反复确认 A065 共同代表猪股哲为与那国居民并以该身份公开活动；不等于总部／正式分支 |
| AP114 | A069→P002 Henoko `site_presence` | `revise`→`advocacy_target` | 独立材料充分证明其以边野古环境影响评价、海上工程和保护诉求为行动对象；现有材料不足以把组织据点写在边野古 |
| AP115 | A069→P003 Oura Bay `site_presence` | `revise`→`advocacy_target` | 多份意见书明确以边野古—大浦湾沿岸生态与工程为诉求对象；不把共同声明推成常设现场节点 |
| AP122 | A075→P002 Henoko `site_presence` | `accept_with_revision` | S047 是冲绳防卫局官方边野古环境影响评价页面，支持该机构在项目实施／管理上的地点连接；不是办公室位置 |
| AP130 | A112→P013 Miyako `site_presence` | `revise`→`headquarters` | A112 官方页面列出“宮古島地下水研究会事務局”及宫古岛市地址，证据比一般在场更精确 |
| AP131 | A113→P018 Ginowan `site_presence` | `accept` | 市议会记录和多年度报道持续确认该宜野湾居民团体在市内采样、请愿和行政请求 |
| AP132 | A113→P004 Futenma `advocacy_target` | `accept` | 证据把普天间基地及其周边 PFAS、基地进入／信息交换请求置于行动对象；不证明基地内设点 |
| AP134 | A114→P012 Ishigaki `event_site` | `accept` | 两份官方记录确认 2024 年石垣港罢工／行动发生地点；不批准争议中的合法性或效果判断 |

建议汇总：

- `accept`：AP131、AP132、AP134；
- `accept_with_revision`：AP108、AP122；
- `revise`：AP107、AP114、AP115、AP130；
- `reject_edge/retire_candidate`：AP088、AP106。

## 2. AP088 · 嘉手纳爆音原告团—宜野湾

原候选称 Ginowan 是 “Adjacent affected area”，来源为 S026。

核查结果：

- S026 报道对象是第三次嘉手纳爆音诉讼，正文只称“嘉手纳基地周边居民”；
- 来源没有提到宜野湾，也没有证明原告团办公室、成员范围或行动地点在宜野湾；
- “基地受影响范围可能跨行政区”不能替代具体来源中的地点事实；
- 同一 actor 已有 AP087 A052→P005 Kadena，候选语义是 `advocacy_target`，因此无需把 AP088 错误重键到 P005 造成重复。

### 辅助建议

**AP088=`reject_edge`／`retire_candidate`。**

限制：这表示 S026 不支持 Ginowan 地点边，不表示原告中绝无宜野湾居民，也不对原告地理构成作反向事实判断。

## 3. AP106–AP108 · 南西诸岛 Peace Net 三岛节点

### 3.1 现有 S036 实际证明什么

S036 是 2017 年政府交涉报道。它列出：

- 宮古島市民会議；
- 南西諸島ピースネット；
- 八重山大地会；
- てぃだぬふぁ島の子の平和な未来をつくる会。

这证明 A065 存在并参加该次政府交涉，但四个名称是并列的行动团体，不能把其他地方团体的所在地反向转写为 A065 自身的石垣／宫古节点。

### 3.2 AP106 · Ishigaki

在线补查没有找到 A065 在石垣设点、设分支、由石垣成员公开代表或在石垣举办具体活动的独立材料。S036 中八重山大地会的出现，反而要求把两个 actor 分开。

**辅助建议：AP106=`reject_edge`／`retire_candidate`。**

限制：这是“当前候选没有组织层地点证据”，不是“历史上从未在石垣活动”。以后如取得直接活动／成员代表材料，可新建有来源的边。

### 3.3 AP107 · Miyako

补查找到 2016-09-29 宫古岛公开活动：

- 主办方是 `てぃだぬふぁ島の子の平和な未来をつくる会`；
- A065 共同代表猪股哲以 A065 身份参加现场 talk event；
- 这证明 A065 在宫古有一次明确的组织身份事件，但不证明 A065 有宫古节点、办公室或持续组织能力。

来源：

- IWJ：`https://iwj.co.jp/wj/open/archives/335214`

**辅助建议：AP107=`revise`，从 `site_presence` 改为 `event_site`。**

回填前应把 IWJ 页面进入 source proposal／metadata／archive；地点说明限定为“2016-09-29 宫古岛公开活动的组织身份出席”。

### 3.4 AP108 · Yonaguni

补查形成两期独立可见材料：

- 2016 年 IWJ 把猪股哲写为 A065 共同代表、与那国岛居民，并由他报告与那国部署后的情况；
- 2023 年《冲绳时报》可见 locator 再次写明 A065 共同代表猪股哲居住于与那国町，并就当地／南西诸岛安全化公开发言。

来源：

- IWJ：`https://iwj.co.jp/wj/open/archives/304004`
- 冲绳时报：`https://www.okinawatimes.co.jp/articles/-/1162100`

**辅助建议：AP108=`accept_with_revision`，保留 `site_presence`。**

精确关系文本建议：

> A065 通过居住于与那国、并在 2016 与 2023 年以共同代表身份持续公开活动的代表形成可观察的与那国在场。

不得写成：

- A065 总部位于与那国；
- 与那国存在正式分支或法定节点；
- A065 代表与那国居民总体；
- A065 与其他岛屿团体形成稳定联盟。

## 4. AP114/AP115 · 冲绳儒艮环境影响评价监视团—边野古／大浦湾

当前两条边仅引 S047。S047 是冲绳防卫局的官方环境影响评价文档页面，可以证明项目及行政程序，但页面本身不能单独证明 A069 的组织活动。

补查材料证明：

- A069 长期以普天间替代设施的环境影响评价、边野古海上工程和边野古—大浦湾生态保护为明确行动对象；
- 2012 年对评估报告的意见、2014 年 Ramsar 共同声明、2015 年对边野古—大浦湾海域施工的抗议／中止要求均明确列名 A069；
- QAB 与琉球新报报道也记录 A069 向县方提出边野古工程、现场视察及环境程序请求；
- 这些材料最稳妥地支持“倡议／争议对象”，但共同声明、观察和行政请求不能自动证明组织在两个地点设有持续据点。

来源：

- 日本自然保护协会 2012 意见：`https://www.nacsj.or.jp/statement/50949/`
- 日本自然保护协会 2014 边野古—大浦湾共同声明：`https://www.nacsj.or.jp/statement/50847/`
- QAB 2014 报道目录：`https://www.qab.co.jp/news/2014/05`
- 琉球新报 2015：`https://ryukyushimpo.jp/news/prentry-241609.html`
- 2015 抗议／要求书：`https://img03.ti-da.net/usr/o/k/i/okinawabd/2015-02-12%E6%B2%96%E7%B8%84%E9%98%B2%E8%A1%9B%E5%B1%80-%E6%8A%97%E8%AD%B0%E5%8F%8A%E3%81%B3%E8%A6%81%E6%B1%82%EF%BC%88ver.2%EF%BC%89.pdf`

### 辅助建议

- **AP114=`revise`→`advocacy_target`；**
- **AP115=`revise`→`advocacy_target`。**

两条边可继续引用 S047 作为争议项目／程序的官方侧材料，但必须至少补入一条列名 A069 的独立材料。不要据共同署名生成 actor–actor alliance edge；不要把保护诉求写成工程变化或生态效果。

## 5. AP122 · 冲绳防卫局—边野古

S047 是 A075 自身的官方页面，列出普天间飞行场替代设施建设事业的环境影响评价材料。它足以支持 A075 对边野古项目的行政／实施连接。

六种受控语义中：

- 不是 `headquarters`：冲绳防卫局办公室位置并非边野古；
- 不是 `advocacy_target`：A075 是项目行政／实施主体，不是以外部倡议指向该地；
- `institutional_venue` 更适合办公室、行政渠道或制度节点；
- `site_presence` 是当前词表中最接近“持续项目实施／管理活动在场”的语义。

### 辅助建议

**AP122=`accept_with_revision`，保留 `site_presence`。**

关系文本改为：

> 冲绳防卫局作为普天间替代设施建设事业的行政／实施机构，与边野古项目现场形成持续项目活动连接。

限制：不写成“总部在边野古”，不以官方 EIA 页面证明环境评价充分、工程合法、争议已解决或政策效果。

## 6. AP130 · 宫古岛地下水研究会—宫古

现有候选为 `site_presence`，但 A112 官方页面提供了更精确的地点证据：

- 页面列出 `宮古島地下水研究会事務局`；
- 地址为 `沖縄県宮古島市平良字西里675-3`；
- S271 又从宫古岛市接收／答复侧确认该组织是当地行政交涉对象。

因此这里不是只凭组织名称推断地点，而是有公开事务局地址。

### 辅助建议

**AP130=`revise`，从 `site_presence` 改为 `headquarters`。**

精确表述宜用“公开事务局／办公室位于宫古岛市”；如果项目对 `headquarters` 要求法定总部证据，则字段标签仍用 `headquarters`，notes 明确它是公开事务局地址而非已核法人登记地址。

不得据地下水研究／请求材料写成已证明自卫队设施造成污染，或把 A112 与其他宫古地下水团体合并。

## 7. AP131/AP132 · 宜野湾 Chura Water Group—宜野湾／普天间

### AP131 · Ginowan

证据形成多年度、跨来源的当地活动链：

- 2021 年向宜野湾市长提出 PFAS 信息公开和健康对策请求；
- 2022 年居民筹资的学校土壤采样及市议会请愿审查；
- 2023 年向宜野湾市基地涉外部门提出市民参加市长—普天间司令官意见交换的请求；
- 宜野湾市议会材料确认组织名称、共同代表和工作经历。

**辅助建议：AP131=`accept`，`site_presence`。**

它表示可观察的宜野湾居民团体及持续市内行动，不必升级为 `headquarters`，因为当前材料未提供正式办公室／事务局地址。

### AP132 · Futenma

材料把以下事项直接放在普天间基地及周边：

- 普天间第二小学等基地邻接地点的采样；
- 对基地内／周边 PFAS 信息和调查的请求；
- 要求参与宜野湾市长与普天间飞行场司令官的意见交换。

**辅助建议：AP132=`accept`，`advocacy_target`。**

限制：

- 不把基地周边采样写成组织进入基地；
- 不把“可能／被指出的来源”强化为已证实污染因果；
- 请求参与不等于已被接纳或与市／美军建立伙伴关系。

## 8. AP134 · 全港湾冲绳地方本部—石垣

S287 与 S288 是两份独立官方记录：

- 石垣市议会决议记载该工会在石垣／那霸港行动计划及其公开安全理由；
- 国会记录确认 2024-03-11 至 13 日冲绳地方本部在石垣港实施罢工。

两份材料足以确认石垣是有界行动场域。

### 辅助建议

**AP134=`accept`，`event_site`。**

限制：

- 只确认事件发生地点与公开归因；
- 不据一次事件推断石垣常设分支、长期组织能力或地方总体代表性；
- 不在本地点边裁断罢工是否合法、造成多大影响或是否改变军事使用政策；
- HR027E010 的完整 AEV 事件记录仍须独立人审，地点语义接受不自动批准该事件表全部字段。

## 9. 如负责人确认，本批主线程动作

1. HR-025 回填 AP088、AP106=`reject_edge/retire_candidate`。
2. AP107 改为 `event_site`；将 IWJ 2016 宫古活动页面送入 source proposal／metadata／archive。
3. AP108 保留 `site_presence`，改写为“与那国居民共同代表的重复公开组织活动”；补入 IWJ 与冲绳时报 locator。
4. AP114、AP115 改为 `advocacy_target`，补入至少一条列名 A069 的独立来源；S047 只作官方项目／程序侧材料。
5. AP122 保留 `site_presence`，将 relation basis 改为项目实施／管理连接。
6. AP130 改为 `headquarters`，notes 写“公开事务局地址，不等于已核法人登记总部”。
7. AP131=`site_presence`、AP132=`advocacy_target`、AP134=`event_site`。
8. 不从本批生成任何 actor–actor alliance edge、资助边、因果结论或项目效果判断。
9. 合并后重跑 R03 空间 dossier、严格 place–issue 层、place-key validation、报告 claim audit 与 HR-029 输入。

本报告本身未修改中央 CSV、place registry、source log、archive manifest 或 HR 队列。

## 10. 负责人决定

负责人于 2026-07-19 确认全部 11 项辅助建议：

- AP088、AP106：`reject_edge`／`retire_candidate`；
- AP107：`revise`→`event_site`；
- AP108：`accept_with_revision`，保留 `site_presence` 及“与那国居民共同代表的重复公开组织活动”限制；
- AP114、AP115：`revise`→`advocacy_target`；
- AP122：`accept_with_revision`，保留 `site_presence` 及项目实施／管理连接限制；
- AP130：`revise`→`headquarters`，明确为公开事务局地址而非已核法人登记总部；
- AP131：`accept`→`site_presence`；
- AP132：`accept`→`advocacy_target`；
- AP134：`accept`→`event_site`。

负责人同时确认本报告列出的全部解释边界与主线程动作。上述决定不批准组织间联盟、资助关系、行动效果、污染因果、罢工合法性或事件表中的其他未审字段。
