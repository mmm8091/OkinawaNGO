# 当地材料收集任务书 v0

日期：2026-06-17

## 1. 目的

本文件用于记录后续可能需要当地协作者或有数据库权限的人协助收集的材料。重点不是让当地人“复核证据”，而是收集线上难以取得的原始材料、馆内数据库结果、地方报道、组织年报、活动手册和纸质资料。

目标不是做访谈研究，也不是现在立刻派任务，而是先把需要当地协助收集的材料方向攒起来。第一次沟通稿只概括这些方向；下周再整理更具体的当地查资料任务表，届时再决定是否正式派给当地协作者。

本文件是当地材料收集方向的唯一权威入口。`data/interim/local_retrieval_queue_v0.csv` 仅作为早期结构化草稿保留，暂不继续维护；后续如进入云表格协作，再从本任务书重新生成任务表。

## 2. 未来正式派任务时的交付物

未来正式派给当地协作者时，每个任务至少交付：

1. 资料截图或 PDF / 照片，文件名含日期和来源。
2. 资料出处说明：机构、数据库、报纸名、日期、页码或 URL。
3. 200-500 字中文摘要：确认了什么、不能确认什么。
4. 对应 actor_id / edge_id / source_id。
5. 材料类型判断：官方资料 / 报刊资料 / 组织资料 / 活动材料 / 其他。
6. 是否可写入报告正文：yes / cautious / no。

## 3. 文件命名建议

`YYYYMMDD_taskid_source_shorttitle.ext`

例：

- `20260618_L002_RyukyuShimpo_YonaguniReferendum.pdf`
- `20260618_L003_KOSC_CharityRecipients_photo1.jpg`
- `20260618_L007_ONC_AnnualReport_2024.pdf`

## 4. 材料收集方向

### LR-001 冲绳本地 NPO 报告与财务资料

优先级：P1

相关对象：

- A003 ジュゴンネットワーク沖縄
- A012 宮古島いのちの水を守ろう！
- A017 沖縄対話プロジェクト
- X010 沖縄NGOセンター

要查：

- 事業報告書
- 財務諸表
- 设立、解散、改名记录
- 役员、活动目的、资金来源
- 与外务省 / JICA / 县 / 市町村 / 基金会 / 企业赞助的关系

可能地点：

- 冲绳县 NPO Plaza
- 内阁府 NPO 法人 portal
- 冲绳县相关窗口
- 组织官网或办公室公开资料

交付物：

- 每个组织一条补查摘要。
- 若有财务或委托关系，记录来源页码和金额。
- 若没有找到，说明检索路径。

材料价值：

- 用于确认组织法律身份、活动范围、资金来源和行政协作关系。
- 不要求当地协作者做解释，只需尽量收集原始材料和来源说明。

### LR-002 与那国早期反部署组织

优先级：P1

相关对象：

- A014 与那国改革会議
- A015 与那国自衛隊配備反対意見広告実行委員会
- A016 与那国島の明るい未来を願うイソバの会

要查：

- 地方新闻原文。
- 町议会记录。
- 住民投票资料。
- 意见广告、传单、公开请求书。
- 组织是否真实存在、持续多久、代表人物是谁。

可能地点：

- 冲绳县立图书馆数据库。
- 琉球新报 / 沖縄タイムス馆内数据库。
- 与那国町资料。
- 当地保存材料。

交付物：

- 每个组织是否确认存在。
- 至少一条非党派来源，若能找到。
- 若只能找到党派媒体，说明仍为 E2。
- 与那国专题可用的 3-5 条事实句。

### LR-003 军属配偶俱乐部慈善网络

优先级：P1

相关对象：

- X004 AWWA
- X005 NOSCO
- X006 KOSC
- X007 OESC

要查：

- annual charity recipients
- grant recipients
- thrift shop 收益去向
- bazaar / gala / event program
- 与冲绳本地福利机构的捐赠关系
- 是否只服务美军军属，还是也服务 Okinawan charities

可能地点：

- 各俱乐部官网。
- Facebook / Instagram 公共页面。
- base newspaper / Okinawa Stripes。
- 活动手册或当地联系人。

交付物：

- 组织正式名与别名。
- recipient 名单，按年份整理。
- 每条 donation / grant edge 的证据等级。
- 可用于报告的保守表述。

判定要求：

- 年报 / 活动手册 / 组织官网明确 recipient：E4。
- DVIDS / Stripes 报道：E2-E3，视细节而定。
- 口头转述：只作 E1，不进结论。

### LR-004 USO Okinawa 赞助与服务网络

优先级：P1

相关对象：

- X001 USO Okinawa
- X002 Phoenix Corporation / Phoenix Park Hotel
- X003 American Engineering Corporation

要查：

- USO Okinawa 具体中心位置。
- sponsor 名单年份。
- donation amount / in-kind support。
- 本地企业赞助是否持续。
- 服务对象是否仅限美军人员 / 军属。

可能地点：

- USO Okinawa 官网。
- USO Pacific 新闻。
- local sponsor 公司页面。
- 基地社区新闻。

交付物：

- sponsor-edge 表：source -> USO Okinawa。
- site-presence 表：USO -> base / camp。
- 服务对象说明。
- 不能确认金额的 sponsor 标 E3。

### LR-005 美国领馆 / 公共外交项目 recipient

优先级：P2

相关对象：

- X012 TOMODACHI Initiative
- X013 U.S. Consulate General Naha Okinawa Youth Council Program

要查：

- award notice。
- recipient organization。
- implementing partner。
- 活动报告。
- 参与学校、NPO、地方机构。
- 项目目标是否涉及 U.S.-Japan Alliance、Indo-Pacific、leadership、youth exchange。

可能地点：

- Grants.gov。
- U.S. Embassy Tokyo / Consulate Naha 页面。
- 领馆社媒归档。
- TOMODACHI / USJC 官网。
- 地方新闻。

交付物：

- 是否存在实际 recipient。
- recipient actor 是否进入 actor registry。
- 若只有 NOFO / grant opportunity，标 `no_public_evidence`。
- 不得写成已资助事实，除非找到 award / recipient。

### LR-006 外务省 / JICA / ONC 关系链

优先级：P2

相关对象：

- X010 沖縄NGOセンター
- X011 JICA沖縄

要查：

- 外务省 NGO 相談員是否为委托 / 补助 / 项目合作。
- 年度金额、合同、项目报告。
- ONC 事業報告書中关于外务省 / JICA 的记载。
- ONC 与冲绳本地 NGO、国际合作、多文化共生、教育项目的网络。

可能地点：

- 外务省页面。
- JICA Okinawa。
- ONC 年报 / 财报 / 活动报告。
- NPO 法人报告。

交付物：

- ONC - 外务省 / JICA edge 是否为 E4 或 E3。
- 若有金额，记录金额、年度和来源页码。
- 可写入报告的 2-3 句事实。

### LR-007 报刊数据库补查：先岛与边野古核心组织

优先级：P2

相关对象：

- A010 石垣島に軍事基地をつくらせない市民連絡会
- A011 石垣市住民投票を求める会
- A012 宮古島いのちの水を守ろう！
- A013 ミサイル基地いらない宮古島住民連絡会
- A019 ヘリ基地反対協議会

要查：

- 首次出现时间。
- 代表人物。
- 主要行动。
- 与住民投票、诉讼、声明、行政请求的关系。
- 是否有名称变化。

可能地点：

- 冲绳县立图书馆馆内数据库。
- 沖縄タイムス 1997 年以后。
- 琉球新報 1998 年 1 月以后。

交付物：

- 每个组织 3-5 条关键时间线。
- 可引用的新闻日期、标题、报纸名。
- 若只找到二手网页，说明缺口。

### LR-008 失效网站与 Web Archive

优先级：P3

相关对象：

- A002 Save the Dugong Campaign Center
- A008 NGO非戦ネット
- A019 ヘリ基地反対協議会
- 其他官网失效组织

要查：

- 组织官网旧页面。
- 声明页。
- 活动记录。
- 组织简介和联系信息。

可能地点：

- Internet Archive。
- 本地保存 PDF。
- 旧新闻链接。

交付物：

- archived_url。
- capture_date。
- 页面标题。
- 可提取字段。
- 是否足以将 evidence_level 提升到 E3。

## 5. 暂定材料收集优先顺序

如果后续正式启用当地协作者，第一批建议优先做：

1. LR-002 与那国早期反部署组织。
2. LR-003 军属配偶俱乐部慈善网络。
3. LR-006 外务省 / JICA / ONC 关系链。

原因：

- 这些最依赖本地资料。
- 这些最容易影响 proposal 的新方向。
- 这些也是第一次沟通稿里最适合概括为“后续可能需要当地协作收集材料”的部分。

## 6. 不合格交付示例

以下不算有效材料收集：

- 只发链接，没有摘要。
- 只说“查不到”，但不说明查了哪些库 / 关键词。
- 没有日期、标题、页码或来源。
- 只给口头判断，没有可复核材料。
- 把社媒转述当成财务证据。
