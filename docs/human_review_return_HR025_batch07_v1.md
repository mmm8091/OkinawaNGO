# HR-025 县域地点语义收尾回交报告 Batch 07

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——11/11 条**

## 0. 批次边界

- 本批覆盖 HR-025 尚未进入既有 Batch 04–06 报告的最后 11 条 actor–place 候选边。
- 核心任务仍是区分 `headquarters`、`site_presence`、`event_site`、`advocacy_target`、`institutional_venue` 与不能成立／应退役的候选边。
- 本批特别检查“名称含冲绳”是否真的表示冲绳在地组织，并检查县级地点边是否与更精确地点边重复。
- 接受地点边不批准组织间联盟、共同声明之外的稳定合作、议题因果、政治效果或当前连续运作。
- 本报告不直接修改中央 registry、actor–place、actor–issue、source log、archive manifest 或 HR CSV。

## 1. 建议结论总表

| 项目 | 当前候选 | 辅助建议 | 核心理由 |
|---|---|---|---|
| AP005 | A003 ジュゴンネットワーク沖縄→P001 `unclear` | `accept_with_revision`：`site_presence` | 独立材料证明该组织长期在冲绳海域调查，并以组织身份参加政府交涉；不再仅靠 2010 共同署名 |
| AP024 | A018 ノーモア沖縄戦 命どぅ宝の会→P001 `site_presence` | `accept` | 官方网站持续记录冲绳县内活动并更新至 2026 年，足以支持县域在场 |
| AP052 | A023 美ら海にもやんばるにも基地はいらない市民の会→P001 `unclear` | `accept_with_revision`：`advocacy_target` | 可证活动主要是围绕边野古／高江的东京政府交涉与院内活动，未证实冲绳办公室或在地节点 |
| AP056 | A026 ピース・ニュース→P001 `unclear` | `accept_with_revision`：`advocacy_target` | 组织自述证明它是开展反战学习、行动和实地考察的市民团体；本条原始依据仍是边野古声明，不能写成常设在场 |
| AP060 | A029 沖縄・生物多様性市民ネットワーク→P001 `unclear` | `accept_with_revision`：`site_presence` | 冲绳现场活动、在地成员和国际倡议材料交叉支持持续在场 |
| AP085 | A051 「辺野古」県民投票の会→P001 `event_site` | `accept` | 2018–2019 全县公投条例直接请求和宣传活动是明确、有界的程序／动员场域 |
| AP091 | A054 沖縄人権協会→P001 `unclear` | `accept_with_revision`：有时间边界的 `site_presence` | 1961 年成立、2019 年在那霸召开第 56 次总会可证历史在场；未找到更新的连续性材料 |
| AP093 | A055 泡瀬干潟を守る連絡会→P001 `unclear` | `retire_redundant_parent_place_edge` | AP092 已精确记录 A055→P019 Awase `site_presence`；P001 只重复上位地理层级，没有独立全县功能 |
| AP094 | A056 沖縄環境ネットワーク→P001 `unclear` | `accept_with_revision`：`site_presence` | 官方通信已达 104 号并含 2025 年总会材料，证明持续的冲绳环境网络活动 |
| AP095 | A057 沖縄意見広告運動→P001 `event_site` | `accept_with_revision`：`advocacy_target` | 官方联系方式在东京，广告同时投向冲绳、全国及海外媒体；“冲绳”是核心诉求对象而非组织地点 |
| AP096 | A058 沖縄県統一連→P001 `unclear` | `accept_with_revision`：`site_presence` | 多年份材料给出那霸地址、全称及县内行动；原 S031 属于另一组织，必须撤掉 |

## 2. AP005 · ジュゴンネットワーク沖縄—Okinawa Prefecture

S003 只能证明该名称出现在 2010 年 67 团体共同声明中，不能独立支持组织持续在场。补查材料显示：

- 2019 年日本自然保护协会把 `ジュゴンネットワーク沖縄` 列为紧急院内集会及政府交涉的共同主办方；
- 该报道明确称细川太郎为组织事务局长，并记录他过去 20 年在冲绳海域开展儒艮食痕调查；
- 2000 年参议院质问书已出现组织名称、代表和冲绳东海岸调查活动。

来源：

- `https://www.nacsj.or.jp/report/15803/`
- `https://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/147/syuh/s147023.htm`

### 辅助建议

**AP005=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> ジュゴンネットワーク沖縄以组织身份长期参与冲绳海域儒艮调查、公开报告和相关行政交涉，支持其在冲绳县的持续活动在场。

限制：

- 不再把 2010 共同署名作为地点边的唯一依据；
- 长期调查不等于已确认法定登记地或总部；
- 与日本自然保护协会共同主办一次活动不自动生成稳定联盟。

## 3. AP024 · ノーモア沖縄戦 命どぅ宝の会—Okinawa Prefecture

S023 已证明该会于 2022 年在冲绳结成。其官方网站继续记录：

- 冲绳市、名护、先岛及县域层面的集会、讲演、请求和传播活动；
- “不让岛屿再次成为战场”的组织性倡议；
- 2026 年仍有连续更新。

来源：

- `https://nomore-okinawasen.org/`
- `https://www.qab.co.jp/news/20220321148994.html`

### 辅助建议

**AP024=`accept`，保留 P001 `site_presence`。**

本边表示县域层面的持续组织活动，不表示该会在冲绳县每个岛屿都有分支，也不把先岛安全化议题强制转换成环境阻工框架。

## 4. AP052 · 美ら海にもやんばるにも基地はいらない市民の会—Okinawa Prefecture

S004 只证明该会参加 2015 年边野古声明。补查到的多项活动包括：

- 2019 年与 FoE Japan 在东京众议院第二议员会馆共同主办边野古政府交涉和院内集会；
- 2017–2020 年围绕高江、边野古施工和软弱地基继续参与东京政府交涉、院内活动及声明；
- 公开材料没有给出冲绳办公室、冲绳常设分支或持续驻点。

来源：

- `https://www.foejapan.org/aid/henoko/191122.html`
- `https://www.foejapan.org/aid/takae/170821.html`
- `https://www.nacsj.or.jp/statement/50663/`

### 辅助建议

**AP052=`accept_with_revision`，`unclear→advocacy_target`。**

关系文本改为：

> 该会持续把冲绳的边野古、高江及山原基地建设问题作为声明、政府交涉和院内倡议对象；现有材料未证明冲绳常设组织节点。

伴随修复建议：

- registry 的 `origin_type=okinawa_local` 缺乏地点证据，主线程应改为 `japan_domestic`；若希望把组织地址作为 origin 的唯一判断依据，则先记为 `unclear`，待找到章程／地址；
- 不因为组织名称含“美ら海”“やんばる”而推断在地身份；
- 东京活动是支持“非冲绳在地”的反证背景，不另把 AP052 改成东京事件边；如研究需要，应从具体事件另建候选。

## 5. AP056 · ピース・ニュース—Okinawa Prefecture

S004 只证明该名称出现在 2015 年边野古声明。组织自己的“关于 PN”页面明确：

- `ピース・ニュース` 是团体本身的名称，不只是通讯刊物；
- 有会则、会员、会费、联络方式和持续活动目标；
- 以神奈川、冲绳、韩国、中国等地的实地考察、学习会和反战和平行动为主要活动。

来源：

- `https://www.jca.apc.org/~p-news/about_PN.htm`

### 辅助建议

**AP056=`accept_with_revision`，`unclear→advocacy_target`。**

关系文本改为：

> ピース・ニュース把冲绳的基地、战争记忆与和平问题作为声明、学习及实地考察对象；本条不表示冲绳常设分支或总部。

伴随修复建议：

- `actor_class=media_or_advocacy_actor` 容易误把团体当媒体，建议规范为现有较宽的 `citizen_group`；
- 组织自述中的“冲绳 fieldwork”说明曾有实地活动，但缺少具体日期和地点，暂不足以把县域边写成 `event_site` 或持续 `site_presence`；
- 后续若找到可定位的实地考察记录，应新建有日期的事件地点边，而不是增强本条。

## 6. AP060 · 沖縄・生物多様性市民ネットワーク—Okinawa Prefecture

S004 的共同声明不足以单独决定地点。补查材料包括：

- 2014 年日本自然保护协会记录在那霸举办的“生物多样性おきなわ战略”论坛，并把该网络列为共同主办方；
- 相关材料把组织与冲绳地方生物多样性战略、边野古及冲绳当地参与者直接连接；
- 国际倡议材料把它列为 `Okinawa, Japan` 的民间网络。

来源：

- `https://what-we-do.nacsj.or.jp/2014/01/2109/`
- `https://www.nacsj.or.jp/statement/50880/`
- `https://www.data-max.co.jp/2014/01/17/post_16455_y_ymh_01.html`

### 辅助建议

**AP060=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> 沖縄・生物多様性市民ネットワーク在冲绳参与地方生物多样性政策讨论、论坛和相关国内外倡议，支持县域持续活动在场。

这是一条组织活动地点边；不从共同主办、国际联署或联合国倡议反推正式联盟。

## 7. AP085 · 「辺野古」県民投票の会—Okinawa Prefecture

S025 是官方公投结果页，证明公投发生，却没有独立确认民间组织。冲绳合同法律事务所 2018 年材料直接说明：

- `「辺野古」県民投票の会` 在 2018 年 5 月 23 日至 7 月 23 日推动县条例制定直接请求签名；
- 签名活动以冲绳县民投票为明确程序目标；
- 法律事务所作为签名点参与该有界动员。

来源：

- `https://okinawagodo.org/blog/1044/`
- `https://www.city.nago.okinawa.jp/kurashi/2019020300029/`

### 辅助建议

**AP085=`accept`，保留 P001 `event_site`。**

关系文本改为：

> 「辺野古」県民投票の会在 2018–2019 年冲绳县民投票的直接请求、签名和宣传过程中开展县域动员。

时间边界必须保留。本边不证明 2019 年以后仍有常设组织能力，也不把公投结果归因于该会。

## 8. AP091 · 沖縄人権協会—Okinawa Prefecture

S033 是一般学术书目，不能确认组织地点或当前连续性。补查材料显示：

- 琉球新报词典资料把冲绳人权协会追溯到 1961 年，说明其成立背景是美国统治下冲绳居民的人权保护；
- 2019 年地方报道记录协会在那霸召开第 56 次定期总会、选举新理事长并通过人权宣言；
- 未找到 2020–2026 年间足以确认当前连续运作的直接组织材料。

来源：

- `https://ryukyushimpo.jp/okinawa-dic/prentry-40693.html`
- `https://ryukyushimpo.jp/news/entry-1038626.html`

### 辅助建议

**AP091=`accept_with_revision`，改为有时间边界的 `site_presence`。**

关系文本改为：

> 1961–2019 年公开材料证明沖縄人権協会作为冲绳民间人权组织持续存在，并在那霸举行定期总会。

限制：

- 不写成“当前仍在活动”，除非补到更新来源；
- 不由那霸总会推断法定总部；
- registry 的 `legal_status_guess=npo_or_association` 应收窄为 `association_or_unclear`，因为现有材料没有证明 NPO 法人格。

## 9. AP093 · 泡瀬干潟を守る連絡会—Okinawa Prefecture

Batch 05 已确认：

- AP092：A055→P019 Awase `site_presence`；
- 冲绳县地域环境中心给出组织地址、2001 年成立、调查、干潟导览、宣传以及向国家／县／市请求等直接材料。

AP093 的 S030 只是泡濑诉讼新闻，关系文本仅称“Okinawa environmental actor”。它没有证明区别于泡濑现场的全县活动功能。

来源：

- `https://kankyo-center.okinawa/environmental-organization-facility/%E6%B3%A1%E7%80%AC%E5%B9%B2%E6%BD%9F%E3%82%92%E5%AE%88%E3%82%8B%E9%80%A3%E7%B5%A1%E4%BC%9A`
- `https://ryukyushimpo.jp/news/prentry-239394.html`

### 辅助建议

**AP093=`retire_redundant_parent_place_edge`。**

这不是否认 A055 位于冲绳，而是做地点层级规范：

- 保留更精确、证据更强的 AP092→P019 Awase；
- 退役只重复“泡濑属于冲绳”的 P001 父级边；
- 图表需要县级汇总时，应由 place hierarchy 机械汇总，而不是同时保留精确边和父级边造成双计数。

## 10. AP094 · 沖縄環境ネットワーク—Okinawa Prefecture

S033 不能承担组织结构和当前活动证明。组织官方网站的通信档案显示：

- 网络通信已从创刊准备号延续至 104 号；
- 100 号材料回顾约 24 年活动和组织成立过程；
- 2024、2025 年材料包含年度总会、PFAS、边野古、大浦湾、浦添西海岸、先岛军事化和国际环境倡议等内容；
- 日本自然保护协会国际请求材料也把它列为冲绳的民间网络。

来源：

- `https://oki-kan.net/tsushin/`
- `https://www.nacsj.or.jp/statement/50880/`

### 辅助建议

**AP094=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> 沖縄環境ネットワーク通过持续通信、总会和跨地区环境议题活动，形成可验证的冲绳县域网络在场。

S033 不再作为主要地点来源；官方通信与组织来源应先进入 source proposal，再由主线程分配 S 编号。

## 11. AP095 · 沖縄意見広告運動—Okinawa Prefecture

S034 官方网站本身有效，但原语义 `event_site` 不准确。官方网站显示：

- 运动于 2010 年发起，持续在冲绳地方报纸、全国性报纸及海外媒体刊登意见广告；
- 当前联络地址在东京都新宿区；
- 历史材料还显示东京、关西等地的事务和活动节点；
- 其核心诉求对象是普天间、边野古、海兵队及冲绳军事化，而不是以冲绳为唯一活动地点。

来源：

- `https://www.okinawaiken.org/`
- `https://www.okinawaiken.org/untilnow/untilnow.html`
- `https://www.okinawaiken.org/ouridea/ouridea.html`

### 辅助建议

**AP095=`accept_with_revision`，`event_site→advocacy_target`。**

关系文本改为：

> 沖縄意見広告運動持续把冲绳的基地负担、普天间、边野古及军事化作为全国／跨地域意见广告和传播的倡议对象。

伴随修复建议：

- registry 的 `origin_type=okinawa_local` 改为 `japan_domestic`；
- P001 不是广告发布的唯一事件地点，更不是组织总部；
- 全国世话人、冲绳发言者或地方报纸刊登不自动构成冲绳在地分支。

## 12. AP096 · 沖縄県統一連—Okinawa Prefecture

原 S031 是 `沖縄平和運動センター` 官方网站，属于另一 actor，不能支持 A058。补查材料显示：

- 2022 年报道使用全称 `安保廃棄・くらしと民主主義を守る沖縄県統一行動連絡会議`，简称 `沖縄県統一連`；
- 2018 年《統一連 NEWS》给出那霸市地址，并使用 `安保廃棄 沖縄県統一連`；
- 多年份材料持续记录该组织在那霸、边野古及县内的行动。

来源：

- `https://www.jcp.or.jp/akahata/aik21/2022-03-06/2022030604_01_0.html`
- `https://www.kanagawa-rouren.jp/archives/6613`
- `https://www.anpo-osk.jp/down/touithuren-new/news240628-24-19.pdf`

### 辅助建议

**AP096=`accept_with_revision`，`unclear→site_presence`。**

关系文本改为：

> 多年份组织通信和行动报道证明沖縄県統一連在那霸及冲绳县内持续开展反战、基地和生活／民主议题活动。

伴随修复建议：

- canonical name 改为 `安保廃棄・くらしと民主主義を守る沖縄県統一行動連絡会議`；
- aliases 保留 `沖縄県統一連`、`安保廃棄沖縄県統一連`；
- 删除 A058 对 S031 的引用，改用本批直接材料；
- 可在后续地点补充中提出 A058→P020 Naha `headquarters` 候选，但本批只确认现有 P001 县域 `site_presence`；
- 共同参加行动不自动证明报道中其他组织都是 A058 的正式成员。

## 13. 本批的整体判断

建议分布：

- `accept`：2 条（AP024、AP085）；
- `accept_with_revision`：8 条（AP005、AP052、AP056、AP060、AP091、AP094、AP095、AP096）；
- `retire_redundant_parent_place_edge`：1 条（AP093）。

语义结果：

- `site_presence`：AP005、AP024、AP060、AP091、AP094、AP096；
- `event_site`：AP085；
- `advocacy_target`：AP052、AP056、AP095；
- 退役重复父级地点边：AP093。

这组决定修复四类系统误差：

1. 不能用共同署名单独证明组织在场；
2. 不能因名称含“冲绳”就编码为 `okinawa_local`；
3. 不能把倡议对象或报纸投放地写成组织据点；
4. 精确地点与其父级地点若没有独立功能，不应重复计边。

## 14. 如负责人确认，本批主线程动作

1. 按第 13 节分布填写 HR-025 的最后 11 条决定。
2. AP005、AP060、AP091、AP094、AP096 更换／补充直接来源，不能继续由 S003、S004、S033、S031 单独承担地点证明。
3. AP052、AP095 的 `origin_type` 从 `okinawa_local` 改为 `japan_domestic`；AP052 如坚持地址优先规则，可暂标 `unclear`。
4. A026 的 `actor_class` 改为较宽的 `citizen_group`；A054 的法律状态收窄为 `association_or_unclear`。
5. A058 规范 canonical name 和 aliases，并删除错配的 S031。
6. AP093 退役但保留 AP092→P019 Awase；县级图表使用地点层级汇总，不重复计边。
7. 新增网页先作为 source proposal 进入来源整合，所有 `relation_or_claim_approved` 仍为 `no`，再由主线程分配 S 编号与归档。
8. 合并后重跑 R03 spatial dossier、strict place–issue、source crosswalk、schema alias freeze、claim audit 和 HR-029 输入。

负责人确认本批后，HR-025 的 47/47 条决定即全部完成；中央表仍留待主线程统一合并。

## 15. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议：

- AP005：`accept_with_revision`，`unclear→site_presence`；
- AP024：`accept`，保留 `site_presence`；
- AP052：`accept_with_revision`，`unclear→advocacy_target`，并确认后续修复 origin；
- AP056：`accept_with_revision`，`unclear→advocacy_target`，并将 actor class 规范为 `citizen_group`；
- AP060：`accept_with_revision`，`unclear→site_presence`；
- AP085：`accept`，保留有时间边界的 `event_site`；
- AP091：`accept_with_revision`，使用截至 2019 年可证的历史性 `site_presence`；
- AP093：`retire_redundant_parent_place_edge`，保留更精确的 AP092→P019 Awase；
- AP094：`accept_with_revision`，`unclear→site_presence`；
- AP095：`accept_with_revision`，`event_site→advocacy_target`，并将 origin 规范为 `japan_domestic`；
- AP096：`accept_with_revision`，`unclear→site_presence`，规范 canonical name／aliases 并删除错配的 S031。

负责人同时确认本批所有解释边界：

- 名称含“冲绳”不自动等于冲绳在地组织；
- 共同署名、共同主办、国际倡议或报纸刊登不自动形成常设节点、联盟或因果效果；
- AP093 的退役是地点层级去重，不是否认 A055 位于冲绳；
- A051、A054 等时间有界组织不得被写成当前持续运作，除非后续补到连续性来源；
- 本报告作为 HR-025 最后 11 条人工决定的回交记录；中央表、source log 与 HR CSV 仍留待主线程统一合并。

至此，HR-025 的 47/47 条人工决定均已完成。
