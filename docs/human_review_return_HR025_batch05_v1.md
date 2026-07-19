# HR-025 地点语义与重复实体修复回交报告 Batch 05

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——11/11 条地点边＋1/1 项实体合并**

## 0. 批次边界

- 本批复核 HR-025 的 11 条 actor–place 候选边。
- 核查 AP117/AP118 时发现 A071 与 A072 是同一组织的简称／全称，不先处理实体重复就不能安全决定两条地点边，因此增加 1 项有官方材料支持的实体合并决定。
- 本批只决定地点语义、地点边保留／退役，以及上述重复实体修复；不批准联盟、资助、政治效果、法律结论或行动因果。
- 本报告不直接修改中央 registry、actor–place、actor–issue、event、source log、archive manifest 或 HR CSV。

## 1. 建议结论总表

| 项目 | 当前候选 | 辅助建议 | 核心理由 |
|---|---|---|---|
| AP029 | X001 USO Okinawa→Camp Schwab `site_presence` | `accept` | USO Okinawa 官方页面确认 Camp Schwab Bldg. 3000 的常设中心、联系方式和服务 |
| AP081 | A048→Okinawa Prefecture `site_presence` | `accept_with_revision` | 冲绳军用地共有与当地收用程序支持冲绳在场；S038 是关东板块网站，不能写成 A048 的冲绳办公室或把两者合并 |
| AP092 | A055→Awase `site_presence` | `accept` | 当地环境机构名录及长期调查、导览、保全请求证明泡濑持续活动在场 |
| AP097 | A059→Okinawa Prefecture `site_presence` | `accept_with_revision` | 确认全县性“冲绳建白书…”组织；同时把含混简称规范为正式全称＋简称 |
| AP099 | A060→Takae `site_presence` | `accept` | 当地居民会、代表和高江反直升机坪行动有新闻与县议会记录交叉支持 |
| AP116 | A070→Okinawa Prefecture `site_presence` | `accept_with_revision` | 官方 VFP 和地方报道确认 VFP-ROCK 是在冲绳组成并活动的 chapter；需改成精确名称 |
| AP117 | A071→Okinawa Prefecture `site_presence` | `accept_with_revision` | A071 是长名称的简称；合并 A072 后保留一条全县持续活动边并更新来源 |
| AP118 | A072→Okinawa Prefecture `site_presence` | `retire_duplicate_edge` | A072 与 A071 为同一组织，不能保留两条重复 actor／地点边 |
| AP125 | A111→Okinawa Prefecture `site_presence` | `accept` | HR-013 已确认全县性女性网络及跨时期县级公开动员；不下沉为具体市町据点 |
| AP133 | A114→Naha `headquarters` | `accept` | 劳委会法律材料明确把冲绳地方本部列为那霸市当事人，历史命令书另有那霸地址 |
| AP135 | A115→Okinawa Prefecture `site_presence` | `accept` | 省级本部身份及跨年度县内请求／签名行动成立；P001 记录的是县域在场，不充当那霸办公室地址 |

附带实体建议：

> 保留 A071，将 canonical name 改为正式全称 `沖縄から基地をなくし世界の平和を求める市民連絡会`，alias 记录 `沖縄平和市民連絡会`；A072 标为 `merged_duplicate_of=A071` 并退役。

## 2. AP029 · USO Okinawa—Camp Schwab

原记录只用内部 X001 locator，备注要求核实具体 USO 中心。

在线核查找到 USO Okinawa 官方材料：

- `USO Camp Schwab` 独立地点页；
- 地址为 Camp Schwab Building 3000；
- 有独立电话、邮箱、营业时间、中心经理及服务说明；
- USO Okinawa 总地点页也把 Camp Schwab 与 Hansen、Kadena、Foster、Kinser 等中心分别列出。

来源：

- `https://okinawa.uso.org/usocampschwab`
- `https://okinawa.uso.org/`

### 辅助建议

**AP029=`accept`，`site_presence`。**

关系文本：

> USO Okinawa 在 Camp Schwab Building 3000 运营公开列名的服务中心。

限制：服务组织在基地内设点不代表反基地或支持基地扩张立场，也不自动生成其与军方单位、配偶会或其他服务组织的伙伴／资助关系。

## 3. AP081 · 一坪反战地主会—Okinawa Prefecture

### 3.1 来源边界

S038 的站点主体明确是 `沖縄・一坪反戦地主会 関東ブロック`，地点在东京。它不能证明：

- A048 在冲绳的办公室地址；
- A048 与关东板块是同一个 registry actor；
- 关东板块的全部活动可转给 A048。

但该站保存的历史法律／公开审理材料又明确区分并记录：

- `一坪反戦地主会`；
- 该会围绕嘉手纳、普天间等冲绳军用地共有权与拒绝提供军用地形成；
- 1997 年冲绳县收用委员会公开审理中有该会代表、共有地主及冲绳地点程序记录；
- 冲绳县历史材料也把 `一坪反戦地主会` 作为当地请求／程序 actor 记录。

### 3.2 辅助建议

**AP081=`accept_with_revision`，保留 `site_presence`。**

精确说明：

> A048 的冲绳地点连接来自其所共有的冲绳军用地及在冲绳发生的收用／返还行动，不是由关东板块办公地点反向定位。

同时：

- 把 S038 从 E4 下调为 E3 organization-related archive／历史背景材料；
- 补入冲绳县公开审理／历史行政记录；
- registry notes 明确 A048 与 `沖縄・一坪反戦地主会 関東ブロック` 是需分别编码的相关组织层级，不得静默合并。

本决定不批准所有共有地主的身份、当前会员规模或组织持续性细节。

## 4. AP092 · 泡濑干潟保护联络会—Awase

S030 只是一条诉讼判决新闻，单独看不能充分证明组织的持续地点在场。补查材料提供了更完整的组织层证据：

- 冲绳县地域环境中心名录列出正式名称、任意团体性质、冲绳市地址、2001 年成立及调查、干潟导览、宣传和对国／县／市请求等活动；
- 日本自然保护协会记录其长期进行泡濑干潟及藻场调查、诉讼、保全请求和自然观察活动；
- Ramsar Network 2024 仍记录其泡濑干潟观察会和保全行动。

来源：

- `https://kankyo-center.okinawa/environmental-organization-facility/%E6%B3%A1%E7%80%AC%E5%B9%B2%E6%BD%9F%E3%82%92%E5%AE%88%E3%82%8B%E9%80%A3%E7%B5%A1%E4%BC%9A`
- `https://award.nacsj.or.jp/result/result2016`
- `https://www.ramnet-j.org/gw/group2024/gr24-370.html`

### 辅助建议

**AP092=`accept`，`site_presence`。**

这里的 `site_presence` 指持续调查、导览和保全行动在泡濑干潟发生，不等于办公室位于 P019 干潟现场。诉讼／请求的结果和埋立面积变化因果不在本地点边中编码。

## 5. AP097 · “岛举会议”—Okinawa Prefecture

当前 canonical name `島ぐるみ会議` 过于含混，因为公开材料同时存在：

- 全县组织 `沖縄「建白書」を実現し未来を拓く島ぐるみ会議`；
- うるま市、宜野湾、东村、浦添等不同地方的市町村岛举会议。

独立身份材料：

- 国立国会图书馆团体典据记录正式名称和 2014 年成立；
- 2014 年结成大会材料确认全县组织；
- 后续材料又把市町村岛举会议作为不同地方组织列出。

来源：

- `https://id.ndl.go.jp/auth/ndlna/001186459`
- `https://www.jcp.or.jp/akahata/aik14/2014-07-28/2014072801_01_1.html`

### 辅助建议

**AP097=`accept_with_revision`，保留 `site_presence`。**

同步规范 A059：

- canonical name：`沖縄「建白書」を実現し未来を拓く島ぐるみ会議`；
- alias：`島ぐるみ会議`；
- P001 `site_presence` 只指该全县组织的公开活动范围；
- 不把所有市町村岛举会议自动编码成 A059 的正式分支、成员或同一 actor；
- 地方组织以后按确切全称和直接来源分别处理。

## 6. AP099 · 高江不需要直升机坪居民会—Takae

S028 直接记录：

- 东村高江；
- `ヘリパッドいらない住民の会` 的具名参与者；
- 围绕北部训练场直升机坪工程的当地公开行动。

冲绳县议会委员会记录还在 2010–2012 年间反复列出：

- `「ヘリパッドいらない」住民の会`；
- 具名代表；
- 高江直升机坪相关请求。

这形成地方居民组织、地点和重复活动的交叉支持。

### 辅助建议

**AP099=`accept`，`site_presence`。**

名称差异 `高江のヘリパッドいらない住民の会`／`「ヘリパッドいらない」住民の会` 作为格式／短称记录，不据此拆成多个 actor。组织连续性细节仍可保留 local-retrieval 注记；本边不推断当地居民总体立场或行动效果。

## 7. AP116 · Veterans for Peace Okinawa—Okinawa Prefecture

当前 A070 名称过于概括。独立材料支持的精确组织名是：

> `Veterans For Peace Ryukyu/Okinawa Chapter Kokusai (VFP-ROCK)`  
> 日文：`平和を求める元軍人の会・琉球沖縄国際支部`

证据链：

- VFP 官方 2021 页面把它写为 VFP-ROCK chapter，并列出 Okinawa 成员／协调者；
- VFP 官方决议记录从 2016 到 2025 持续列名该 chapter；
- 2016 年冲绳时报报道其于当年 1 月末成立并参加 VFP 总会；
- 2023 年地方报道记录其在冲绳县厅举行记者会。

来源：

- `https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism`
- `https://www.veteransforpeace.org/who-we-are/2025-online-business-meeting/resolution-2025-1-us-military-expansion-and-environmental-destruction-okinawa`
- `https://www.okinawatimes.co.jp/articles/-/57351`

### 辅助建议

**AP116=`accept_with_revision`，保留 `site_presence`。**

同步修改 A070 canonical name 为上述精确 chapter 名，`Veterans for Peace Okinawa` 只作 alias。地点边表示其在冲绳组成并持续开展公开活动，不把美国母体的全部决议／行动自动转给该 chapter，也不从共同声明生成稳定联盟。

## 8. AP117/AP118 · 和平市民联络会重复实体

### 8.1 官方材料已经消除歧义

宫古岛市议会官方材料明确写：

> `沖縄から基地をなくし世界の平和を求める市民連絡会（略称：沖縄平和市民連絡会）`

并列出同一代表世话人和那霸地址。冲绳县议会材料也用“全称（短称）”方式记录该组织。组织当前网站继续使用短称 `沖縄平和市民連絡会`，记录从那霸方向运营前往边野古／安和的交通及其他县内行动。

来源：

- `https://www.city.miyakojima.lg.jp/gyosei/gikai/files/eeeeee.pdf`
- `https://www.jca.apc.org/heiwa-sr/jp/`

S031 是 `沖縄平和運動センター` 官方网站，没有直接证明 A071/A072；必须从这两个 actor 的 source refs 中移除，避免跨组织借用来源。

### 8.2 实体合并建议

**保留 A071；A072=`merged_duplicate_of=A071` 并退役。**

A071 字段建议：

- canonical name：`沖縄から基地をなくし世界の平和を求める市民連絡会`；
- alias：`沖縄平和市民連絡会`；
- actor class：保持 `citizen_network`；
- source refs：改用组织网站及市／县议会官方记录；
- 不把 `沖縄平和運動センター` 当作别名、上级单位或同一组织。

保留 A071 是为了尽量少改已经映射到 A071 的 2020 S006 event participation；但所有 A072 的边和历史记录仍须重键／去重并保留 provenance。

### 8.3 地点边建议

- **AP117=`accept_with_revision`，保留 A071→P001 `site_presence`；**
- **AP118=`retire_duplicate_edge`。**

AP117 的 `site_presence` 表示该组织在冲绳县内持续公开行动；组织网站及官方记录中的那霸地址可另行生成 A071→P020 `headquarters` 候选，但不得把 P001 全县节点直接改写为精确办公室。

## 9. AP125 · 冲绳县女性团体联络协议会—Okinawa Prefecture

HR-013 已经人工确认：

- 组织成立与全县性女性团体网络身份；
- 1995 与 2024 的有界公开动员；
- 2024 年组织负责人及县民大会筹备。

S200/S201 中的活动地点包含那霸，但当前 AP125 的 P001 记录的是全县组织／动员尺度，不是总部定位。

### 辅助建议

**AP125=`accept`，`site_presence`。**

不向具体市町自动扇出，不据县民大会共同参与推断成员关系或稳定联盟，也不把 A111 与 A115 等其他女性组织合并。

## 10. AP133 · 全港湾冲绳地方本部—Naha

法律／官方材料直接支持：

- 中央劳动委员会命令把 `全日本港湾労働組合沖縄地方本部` 列为位于冲绳县那霸市的案件当事人；
- 较早命令书给出那霸市通堂町的地方本部地址；
- 冲绳县持续公布该地方本部的争议行为通知，支持组织持续性。

来源：

- `https://www.mhlw.go.jp/churoi/meirei_db/mei/pdf/m11367.pdf`
- `https://www.mhlw.go.jp/churoi/meirei_db/mei/pdf/m11056.pdf`
- `https://www.pref.okinawa.jp/shigoto/koyorodo/1012030/1012056.html`

### 辅助建议

**AP133=`accept`，`headquarters`。**

这里确认的是冲绳地方本部办公室／正式组织所在地在那霸；不代表其活动只限那霸，也不批准任何争议行为的合法性、效果或政治解释。

## 11. AP135 · 新日本妇人会冲绳县本部—Okinawa Prefecture

现有证据支持：

- 全国组织的都道府县本部结构；
- 冲绳县本部在 2008、2012、2018、2024 等有独立或共同请求／签名／抗议记录；
- 2018 年那霸签名行动和后续县域请求证明冲绳本部的本地活动。

公开地图目录虽给出那霸地址，但不是本批使用的主要 E4 来源。现有 P001 是县域节点，因此不应为了“县本部”名称就把语义机械改为 `headquarters`。

### 辅助建议

**AP135=`accept`，`site_presence`。**

限制：

- P001 只表示冲绳县本部的县域组织／行动在场；
- 若以后以组织方或官方地址材料建立 P020 Naha 边，可另编码 `headquarters`；
- 全国本部行动不自动转给 A115；
- 不推断政党隶属、选举效果或与其他女性组织的联盟。

## 12. 如负责人确认，本批主线程动作

1. AP029、AP092、AP099、AP125、AP133、AP135 按建议直接接受。
2. AP081 保留 `site_presence`，修正 S038 证据边界并补冲绳当地程序来源；A048 与关东板块保持不同 actor 层级。
3. A059 canonical name 改为正式全称，`島ぐるみ会議` 作 alias；AP097 保留 `site_presence`。
4. A070 canonical name 改为 `Veterans For Peace Ryukyu/Okinawa Chapter Kokusai (VFP-ROCK)`，旧名作 alias；AP116 保留 `site_presence`。
5. 合并 A072→A071，A071 使用正式全称＋短称 alias；所有 A072 边、审查记录和派生表重键／去重并保留 provenance。
6. AP117 保留为合并后单一 `site_presence` 边；AP118 退役为重复边。
7. 从 A071/A072 source refs 移除不相关的 S031，补入组织网站及市／县议会官方记录。
8. 不因本批合并生成新的 actor–actor relation edge；“同一实体”通过 alias／merge provenance 表达。
9. 合并后重跑 actor registry validation、R1/R2、R03、R05 coaction、严格 place–issue、schema alias freeze、claim audit 与 HR-029 输入。

本报告本身未修改中央 CSV、source log、archive manifest 或 HR 队列。

## 13. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议，并明确批准 A072→A071 合并：

- AP029、AP092、AP099、AP125、AP133、AP135：`accept`；
- AP081、AP097、AP116、AP117：`accept_with_revision`，保留报告中的来源、名称与解释边界；
- AP118：`retire_duplicate_edge`；
- A072：`merged_duplicate_of=A071`；
- A071 保留，canonical name 改为 `沖縄から基地をなくし世界の平和を求める市民連絡会`，alias 记录 `沖縄平和市民連絡会`。

负责人同时确认：

- A059 使用全县组织正式全称，地方岛举会议不得自动并入；
- A070 使用 VFP-ROCK 精确 chapter 名；
- A048 与关东板块保持不同 actor 层级；
- S031 不再作为 A071/A072 的身份或地点来源。

上述决定不批准组织间联盟、资助关系、行动效果、法律结论或未审事件字段。
