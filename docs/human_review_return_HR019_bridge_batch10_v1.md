# HR-019 跨议题 actor 第三组回交报告 Batch 10

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv`  
状态：**已完成——10/10 条**

## 0. 批次边界

- 本批复核 HR-019 bridge actor 队列第 21–30 条。
- 推荐决定仅使用：`include_with_scope`、`candidate_only`、`exclude_from_narrative`。
- `exclude_from_narrative` 只表示不作为“跨议题桥梁”写入正文，不等于从 actor registry 删除，也不否定其组织身份或单议题价值。
- 历史性公投组织可以作为有明确时间范围的程序 actor，但不得写成当前持续组织。
- 组织全称、简称、地方分会和后继组织必须分开；名称相似或组织谱系相连不等于同一 actor。
- 本报告不直接修改中央 registry、actor–issue 表、HR CSV、source log、图或报告正文。

## 1. 建议结论总表

| actor | 当前候选 | 辅助建议 | 建议的桥接机制／限制 |
|---|---|---|---|
| A050 沖縄弁護士会 | `event_only_bridge`，3 issues | `include_with_scope` | 以律师会决议／会长声明连接基地人权、地方自治和法律论证；不是单次事件 actor |
| A051 「辺野古」県民投票の会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 2018–2019 年严格程序桥梁：边野古填海争议→直接请求与县民投票；2019-03-26 已决议解散 |
| A059 島ぐるみ会議 | `mixed_candidate_bridge`，3 | `include_with_scope` | 全县 umbrella 把《建白书》、边野古反对、地方组织和自治／自决表达连接；须补全正式名称并与市町村分会分开 |
| A065 南西諸島ピースネット | `positioning_bridge`，3 | `include_with_scope` | 2016–2018 可证的先岛／琉球弧反军事化—前线化预防定位；当前持续性不外推 |
| A066 新外交イニシアティブ（ND） | `mixed_candidate_bridge`，3 | `include_with_scope` | 通过政策研究、法律／自治论证和对美／外交传播连接冲绳基地替代方案；不代表冲绳整体 |
| A067 辺野古土砂搬入反対全国協議会 | `mixed_candidate_bridge`，3 | `include_with_scope` | 土砂搬出地网络把边野古新基地、外来物种／生物多样性和跨县行动连接；正式名称需纠正 |
| A068 名護市民投票の会 | `mixed_candidate_bridge`，3 | `candidate_only` | 1997 公投机制成立，但 registry 名称未获史料支持；须改为正式推進協議会并处理其发展性解散／后继关系 |
| A069 沖縄ジュゴン環境アセスメント監視団 | `mixed_candidate_bridge`，3 | `include_with_scope` | 2003–2012 至少可证的项目型环境评估监督：边野古工程程序→儒艮／生物多样性意见与监测 |
| A070 Veterans for Peace Okinawa | `mixed_candidate_bridge`，3 | `include_with_scope` | VFP Ryukyu/Okinawa 国际分会把美国退伍军人和平行动与冲绳反基地诉求连接；规范名称待统一 |
| A003 ジュゴンネットワーク沖縄 | `event_only_bridge`，2 | `exclude_from_narrative` | 组织身份和持续性得到补强，但当前两边均属同一儒艮／生物多样性生态簇，不构成有解释价值的跨议题 bridge |

建议分布：`include_with_scope` 8 条，`candidate_only` 1 条，`exclude_from_narrative` 1 条。

## 2. A050 · 沖縄弁護士会

现有三个 issue：

- I001 `anti_base`
- I009 `local_autonomy`
- I011 `legal`

### 证据判断

沖縄弁護士会是法定专业团体。官网决议／声明档案表明，它不是只参加一次事件：

- 2017 年定期总会通过要求停止边野古新基地建设、与冲绳县对话的决议；
- 2018 年会长声明把基地设施提供程序与居民生命、身体、财产及地方自治连接；
- 声明同时使用法律程序、地方自治、人权和环境不可逆性论证；
- 后续档案还存在相关决议／声明，但本批不把律师会全部公益活动归为基地议题。

来源：

- S037；
- `https://okiben.org/resolution/629/`
- `https://okiben.org/resolution/`

### 辅助建议

**A050=`include_with_scope`；将 `event_only_bridge` 收窄修正为专业团体／制度声明桥梁。**

正文安全表述：

> 沖縄弁護士会通过总会决议和会长声明，把边野古基地建设争议表述为居民权利、地方自治与法治程序问题，是专业法律团体的制度性桥梁。

限制：

- `anti_base` 只按特定决议／声明中的基地工程立场使用，不推定全体会员个人意见；
- 决议和声明是公共立场与法律论证，不等同于诉讼代理、具名原告或政策效果；
- 同时提及环境、自治和法律并不产生多个独立行动领域。

建议 notes 机制标签：`bar_resolution_local_autonomy_and_legal_bridge`。

## 3. A051 · 「辺野古」県民投票の会

现有三个 issue：

- I003 `Henoko`
- I009 `local_autonomy`
- I010 `referendum`

### 证据判断

既有正式 AEV 已人工确认 A051 是 2019 年县民投票的发起／直接请求 actor。补查又明确其完整生命周期：

- 2018 年组织签名、提出条例制定直接请求并推动县民投票实施；
- 投票问题严格针对边野古美军基地建设填海；
- 2019 年 3 月 26 日总会全票通过解散；
- 因此它是强程序角色，但不是当前持续组织。

来源：

- S025；
- `data/interim/26_actor_event_venue_target_entry_modes_v0.csv`，OBS_AEV0050；
- `https://ryukyushimpo.jp/tag/%E7%9C%8C%E6%B0%91%E6%8A%95%E7%A5%A8%E3%81%AE%E4%BC%9A`

### 辅助建议

**A051=`include_with_scope`，严格限定为 2018–2019 referendum-process bridge。**

正文安全表述：

> 「辺野古」県民投票の会在 2018–2019 年把边野古填海争议转入条例制定直接请求、签名动员和县民投票程序；组织在完成该阶段后于 2019 年 3 月决议解散。

限制：

- 不写成 2019 年以后持续组织；
- 不把公投结果、选举结果或政府政策变化归因为该会；
- 不把签名人、投票者或后续新组织自动视为其成员／后继；
- 解散后的个人行动不归给 A051。

建议 notes 机制标签：`2018_2019_henoko_prefectural_referendum_bridge`。

## 4. A059 · 島ぐるみ会議

现有三个 issue：

- I001 `anti_base`
- I003 `Henoko`
- I009 `local_autonomy`

### 证据与名称边界

S029 的存档正文明确点名正式组织：

`沖縄「建白書」を実現し未来を拓く島ぐるみ会議`

并记录：

- 2014 年成立；
- 2015 年总会及其与自治体单位岛ぐるみ会議／地方反新基地组织的协作规则；
- 边野古现场交通动员、全国宣传、国连／访美部会等不同活动渠道；
- 国立国会图书馆团体典据也确认正式名称和 2014 年成立；
- 2023 年 All Okinawa 文件仍把 `市町村島ぐるみ会議` 作为一类收件组织，但这不能证明每个地方分会都是 A059 本体。

来源：

- S029 存档正文；
- `https://id.ndl.go.jp/auth/ndlna/001186459`
- `https://all-okinawa.jp/wp-content/uploads/2023/10/8aa7e929698f3c4c75b1199918c5eaee.pdf`

### 辅助建议

**A059=`include_with_scope`，同时把 canonical name 补全为正式全称。**

正文安全表述：

> 沖縄「建白書」を実現し未来を拓く島ぐるみ会議把边野古新基地反对、《建白书》所表达的地方尊严／自治诉求以及各地动员渠道连接起来，是全县层级的 umbrella actor。

限制：

- 不把 A059 与“オール沖縄会議”视为同名同体；
- 市町村岛ぐるみ会議是可区分的地方组织，不能把各分会全部行动直接归给 A059；
- “全县层级”描述组织活动尺度，不表示代表所有冲绳居民；
- 与地方组织的协作不自动构成稳定联盟边。

建议 notes 机制标签：`kenpakusho_henoko_and_local_mobilization_umbrella_bridge`。

## 5. A065 · 南西諸島ピースネット

现有三个 issue：

- I002 `anti_military`
- I017 `frontline_prevention`
- I018 `Taiwan_contingency`

### 补查结果

补查找到组织自有网站，使用全称／变体：

`琉球弧（南西諸島）ピースネット`

网站与 S036 可以交叉支持：

- 它连接与那国、宫古、石垣、奄美和冲绳岛的自卫队配备信息；
- 公开框架强调军事部署可能使岛屿成为冲突前线，以及避难、粮食燃料运输和居民生活风险；
- 2016 年有共同代表对外讲演，2017–2018 年网站记录多岛活动；
- 现有材料仍不足以确认 2019 年以后组织活动连续性。

来源：

- S036；
- `https://peacenet-nansei-islands.jimdofree.com/`
- `https://iwj.co.jp/wj/open/archives/304004`

### 辅助建议

**A065=`include_with_scope`，时间暂定为 2016–2018 可证阶段。**

正文安全表述：

> 琉球弧（南西諸島）ピースネット通过跨岛信息交流，把自卫队配备、岛屿前线化和台湾／区域冲突风险放入居民生活与避难问题框架。

限制：

- 三个 issue 属于同一先岛前线化预防框架；
- 不把其主张写成已经发生战争、必然成为攻击目标或已证明政策后果；
- 不推断其代表所有成员岛屿居民；
- 当前持续性不超过现有可证阶段，2019 年以后须补来源。

建议 notes 机制标签：`2016_2018_cross_island_frontline_prevention_bridge`。

## 6. A066 · 新外交イニシアティブ（ND）

现有三个 issue：

- I001 `anti_base`
- I009 `local_autonomy`
- I011 `legal`

### 证据判断

ND 官网的持续研究／政策材料支持：

- 对冲绳海军陆战队、边野古替代方案和亚太安全框架开展政策研究；
- 把国—地方权限、行政法争议和地方自治原则纳入边野古讨论；
- 通过日英文本、访美／外交政策渠道传播冲绳基地政策替代方案；
- 2024 年仍发布冲绳地域外交、台湾有事和地方自治相关研究。

来源：

- S032；
- `https://www.nd-initiative.org/topics/4296/`
- `https://www.nd-initiative.org/research/12401/`
- `https://www.nd-initiative.org/en/research/thejapantimes-3/`

### 辅助建议

**A066=`include_with_scope`。**

正文安全表述：

> 新外交イニシアティブ通过政策研究、法律／地方自治论证和对美／外交传播，把冲绳基地替代方案带入日本国内及国际政策讨论。

限制：

- 不把智库研究写成代表冲绳居民整体意见；
- 不从政策建议推断政府采纳、政策效果或与受访／合作组织的稳定联盟；
- 当前 issue 队列缺 I012 `international_advocacy`，本批不自动新增，只列入后续缺边审查；
- R10 中的行政合作／委托候选不用于本批 bridge 判断，也不由此作资金推断。

建议 notes 机制标签：`okinawa_base_policy_to_legal_and_diplomatic_channel_bridge`。

## 7. A067 · 辺野古土砂搬入反対全国協議会

现有三个 issue：

- I001 `anti_base`
- I003 `Henoko`
- I005 `biodiversity`

### 补查结果与规范名称

组织自有网站、规约、历年会报和决算材料足以确认 2015–2026 持续性，但 registry 当前名称有两处误差。正式自称是：

`辺野古土砂搬出反対全国連絡協議会`

而非：

`辺野古土砂搬入反対全国協議会`

官网还确认：

- 2015 年由七团体发足；
- 当前由 12 都县 16 团体构成；
- 行动围绕西日本／奄美等土砂搬出地、边野古填海、外来物种与生物多样性风险；
- 通过签名、防卫省／环境省交涉、意见书和地方组织联络开展行动。

来源：

- S040；
- `https://dosyazenkyo.com/`
- `https://dosyazenkyo.com/news/No26.pdf`

### 辅助建议

**A067=`include_with_scope`，但合并时必须同步修正 canonical name。**

正文安全表述：

> 辺野古土砂搬出反対全国連絡協議会把边野古新基地填海与土砂搬出地的自然环境、外来物种风险及跨县市民行动连接起来。

限制：

- 生物多样性风险按组织公开依据和行动记录表述，不把所有预期风险写成已发生破坏；
- 正会员关系可以按官网记录，但不等于所有成员间形成一般性稳定联盟；
- 不把全国网络全部活动归给任何单一成员组织；
- 修正名称属于 identity normalization，不自动批准新 edge。

建议 notes 机制标签：`soil_source_biodiversity_and_henoko_national_network_bridge`。

## 8. A068 · 名護市民投票の会

现有三个 issue：

- I001 `anti_base`
- I003 `Henoko`
- I010 `referendum`

### 实体核查发现

1997 年名护市民投票及其公民发起过程确有充分史料，但可靠材料使用的组织名称是：

`ヘリポート基地建設の是非を問う名護市民投票推進協議会`

或简称：

`名護市民投票推進協議会`／`市民投票推進協議会`

补查没有找到 `名護市民投票の会` 这一名称。更重要的是：

- 推进协议会于 1997 年 6 月成立，组织条例制定签名；
- 1997 年 10 月在投票前已发展性解散／改组；
- 后续成立 `海上ヘリ基地建設反対・平和と名護市政民主化を求める協議会`，即现在的 A019 ヘリ基地反対協議会；
- 当前正式 AEV 虽已人工接受 A068 的 referendum-initiator 角色，但使用了未被来源支持的 actor 名。

来源：

- S042；
- `https://ryukyushimpo.jp/news/entry-634713.html`
- `https://lovehenoko.org/%E3%82%8F%E3%81%9F%E3%81%97%E3%81%9F%E3%81%A1%E3%81%AE%E7%AB%8B%E5%A0%B4/`
- `https://www.jca.apc.org/HHK/Tsushin/112/112_nago.html`

### 辅助建议

**A068=`candidate_only`。**

理由不是程序桥梁不存在，而是中央 actor 的规范名称和组织谱系尚未修复。主线程须先决定：

1. 将 A068 更名为正式的 `名護市民投票推進協議会`；
2. 时间范围限定为 1997 年成立至发展性解散；
3. A068→A019 编码为 `predecessor_to`／`reorganized_into`，而不是把两者合并成一个跨期 actor；
4. 修正 OBS_AEV0051 的 actor label，同时保留其已人工接受的事件角色边界。

候选安全表述：

> 1997 年名護市民投票推進協議会把海上直升机基地争议转入条例制定签名和市民投票程序；现有 registry 名称及其与后继 A019 的组织谱系尚待修复。

建议 notes 机制标签：`1997_nago_referendum_actor_identity_repair_required`。

## 9. A069 · 沖縄ジュゴン環境アセスメント監視団

现有三个 issue：

- I003 `Henoko`
- I004 `dugong`
- I005 `biodiversity`

### 补查结果

S047 是冲绳防卫局 EIA 索引，只能证明官方评估程序存在，不能单独证明 A069。补查获得独立组织证据：

- 2003 年结成，目标是监督边野古替代设施的环境影响评估；
- 2007 年以组织名义编印 701 页方法书意见／资料集，CiNii 记录作者和出版信息；
- 2007 年向防卫局提交意见并向县议会陈情；
- 2009 年进入县环境影响评价审查会居民意见场域；
- 2011–2012 年仍以主办者／意见材料收集者身份活动；
- 当前材料不支持把其连续性写到 2013 年以后。

来源：

- `https://ci.nii.ac.jp/ncid/BB01359003`
- `https://www.jca.apc.org/HHK/Tsushin/2007_184.193Tsushin.html`
- `https://disagree.okinawaforum.org/`
- `https://www.nacsj.or.jp/archives/files/katsudo/henoko/pdf/20121225henoko-ikensyosoufusyo.pdf`

### 辅助建议

**A069=`include_with_scope`，限定为至少 2003–2012 的项目型 EIA bridge。**

正文安全表述：

> 沖縄ジュゴン環境アセスメント監視団把边野古替代设施工程的环境评估程序与儒艮／生物多样性调查、意见书和行政审查连接起来。

限制：

- 三个 issue 高度集中于同一边野古环境评估链，不按三个独立运动领域加权；
- 组织提出评估缺陷和生态风险，不等于这些判断已被行政机关或法院全部采纳；
- 不从共同意见书推断与其他环境组织形成稳定联盟；
- 不外推 2013 年以后的持续性。

建议 notes 机制标签：`2003_2012_henoko_eia_monitoring_bridge`。

## 10. A070 · Veterans for Peace Okinawa

现有三个 issue：

- I001 `anti_base`
- I012 `international_advocacy`
- I019 `peace`

### 补查结果

Veterans For Peace 官方材料解决了分会身份的主要疑问：

- 2016 年官网保存 `Veterans for Peace, Ryukyu/Okinawa (VFP ROC)` 与 VFP Ryukyu Working Group 的声明；
- 2024 年决议把 Okinawa 与其他国际分会并列；
- 2025 年 1 月官方 chapter contact listing 明确列出 `1003 - Ryukyu Okinawa`；
- 2025 年冲绳军事扩张／环境破坏决议把 Ryukyu/Okinawa chapter 列为相关行动 actor。

来源：

- S048；
- `https://www.veteransforpeace.org/position-statements`
- `https://www.veteransforpeace.org/download_file/view/2580/144`
- `https://www.veteransforpeace.org/who-we-are/2024-ballot/resolution-2024-04-recognizing-veterans-peace-chapter-113-hawaii-international-chapter`

### 辅助建议

**A070=`include_with_scope`。**

正文安全表述：

> Veterans For Peace 的 Ryukyu/Okinawa 国际分会把美国退伍军人和平行动与冲绳反基地、人权／环境诉求带入 VFP 的跨国组织渠道。

限制：

- 合并时统一 canonical name 与别名：`Veterans For Peace Ryukyu/Okinawa`、`VFP ROC`、`Chapter 1003 - Ryukyu Okinawa`；
- 不把美国母体全部立场和活动转移给 A070；
- 分会／母体关系属于组织 affiliation，不代表与共同声明者形成稳定联盟；
- 不从决议或声明推断政策效果。

建议 notes 机制标签：`veterans_peace_to_ryukyu_okinawa_transnational_bridge`。

## 11. A003 · ジュゴンネットワーク沖縄

现有两个 issue：

- I004 `dugong`
- I005 `biodiversity`

### 补查结果

虽然 registry 目前仍是 `needs_second_source`，补查足以支持其真实、持续的组织身份：

- 2004 年材料已有组织事务局长／副团长等明确角色；
- 2010 年参加 WWF 67 团体声明；
- 2016、2018、2019 年持续以组织名义提出调查／保护请求；
- 冲绳县儒艮保护对策事业检讨委员会正式列出该组织事务局长作为专家委员。

来源：

- S003；
- `https://www.nacsj.or.jp/archives/files/katsudo/henoko/ikensyohonbun.pdf`
- `https://www.nacsj.or.jp/media/2019/04/15337/`
- `https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/004/859/3syou-4syou.pdf`

### 辅助建议

**A003=`exclude_from_narrative`，但保留 actor 与现有 issue edges。**

理由：

- A003 是真实、持续且有研究价值的儒艮保护组织；
- 但当前两个标签 `dugong`、`biodiversity` 是同一生态保护簇；
- 仅凭两个相邻标签把它写成“跨议题桥梁”会夸大 bridge 数量；
- 2016／2019 材料可能支持 Henoko／environment 等缺边，但必须进入后续 edge review，不能在本批自动补边后再反向批准 bridge。

正文处理：

> A003 进入环保／儒艮组织分类和边野古环境行动案例，不进入正式“跨议题桥梁组织”名单。若后续独立批准项目程序、政府交涉或其他跨机制 edge，可重新评估。

建议 notes 机制标签：`valid_dugong_actor_not_current_cross_issue_bridge`。

## 12. 本批共同解释规则

若负责人确认，本批按以下机制处理：

1. **专业／政策制度桥梁**
   - A050：律师会决议—权利／自治／法律；
   - A066：基地政策研究—法律／自治—外交传播。
2. **历史公投程序**
   - A051：2018–2019 县民投票；
   - A068：1997 名护市民投票，但先留候选并修复名称／谱系。
3. **组织网络与跨地域转译**
   - A059：全县 umbrella 与地方组织；
   - A065：先岛／琉球弧跨岛信息网络；
   - A067：土砂搬出地全国网络；
   - A070：VFP 国际分会。
4. **项目型环境评估**
   - A069：边野古 EIA—儒艮／生物多样性。

A003 作为有效环保 actor 保留，但不进入当前 bridge narrative。

## 13. 如负责人确认，本批主线程动作

1. HR019 bridge queue 回填 8 条 `include_with_scope`、A068 一条 `candidate_only`、A003 一条 `exclude_from_narrative`。
2. A050 从 `event_only_bridge` 修正为专业团体／制度声明 bridge。
3. A051 明确写入 2019-03-26 解散边界。
4. A059 canonical name 补全为 `沖縄「建白書」を実現し未来を拓く島ぐるみ会議`；市町村分会不自动并入。
5. A065 暂以 2016–2018 为可证时间范围。
6. A066 的 I012 `international_advocacy` 仅进入缺边候选，不自动新增。
7. A067 canonical name 修正为 `辺野古土砂搬出反対全国連絡協議会`。
8. A068 建立 identity/genealogy repair：
   - 正式名称修复；
   - 1997 时间边界；
   - A068→A019 前身／改组关系；
   - OBS_AEV0051 actor label 修复。
9. A069 仅按 2003–2012 可证活动写入。
10. A070 统一分会名称与别名，保留母体／分会边界。
11. A003 的 actor review 可由新增来源另行提升，但 bridge 决定保持 `exclude_from_narrative`，除非后续缺边人工批准后重审。

本报告本身未修改中央表、HR CSV、source log 或图表。

## 14. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议：

- A050 沖縄弁護士会：`include_with_scope`；
- A051 「辺野古」県民投票の会：`include_with_scope`；
- A059 島ぐるみ会議：`include_with_scope`；
- A065 南西諸島ピースネット：`include_with_scope`；
- A066 新外交イニシアティブ（ND）：`include_with_scope`；
- A067 辺野古土砂搬入反対全国協議会：`include_with_scope`；
- A068 名護市民投票の会：`candidate_only`；
- A069 沖縄ジュゴン環境アセスメント監視団：`include_with_scope`；
- A070 Veterans for Peace Okinawa：`include_with_scope`；
- A003 ジュゴンネットワーク沖縄：`exclude_from_narrative`，但保留 actor 与现有环保议题边。

负责人同时确认：

- A051 只作为 2018–2019 县民投票程序 actor，并保留 2019-03-26 决议解散边界；
- A059 须补全正式组织名，并与各市町村岛ぐるみ会議、All Okinawa 相关组织分开；
- A065 暂以 2016–2018 为可证活动期，不外推当前持续性；
- A067 合并时修正为正式名称 `辺野古土砂搬出反対全国連絡協議会`；
- A068 在正式名称、1997 年活动期及 A068→A019 发展性改组关系修复前保持 `candidate_only`；
- A069 只按 2003–2012 可证的边野古环境评估监督机制使用；
- A070 统一 Ryukyu/Okinawa 分会名称和别名，并保留母体／分会边界；
- A003 不因两个相邻生态标签进入跨议题 bridge 正文；若后续批准新的跨机制 edge，再另行重审。

本报告作为 10 条人工决定的回交记录；中央表、HR CSV、source log 与图表仍留待主线程统一合并。
