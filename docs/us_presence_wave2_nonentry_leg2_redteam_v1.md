# W2-F 前置研究方法红队：matched non-entry 与 LEG2 v1

日期：2026-08-22

状态：`research_only / design_audit_only / principal_review_pending / W2-F_still_blocked`

本件只审查两个有界前置包如何成立，不新增案例事实、不改中央层，也不把现有候选升为结论。审查依据是第二轮研究指挥书、W2-A—E 负责人检查点、W2-A recipient／LEG2 表与 W2-C 的 comparison、gate/control、negative-search 和 principal-review 表。

## 先给结论

1. **“未进入”不能由查不到案号或没有结果推出。** 必须先证明某个行动确实向一个具名场域发起进入，再用该场域自己的受理门槛与终局记录证明它没有越过入口；同时核查后来是否补正进入、改走其他场域或只是在公开资料中暂时不可见。
2. **一个 matched non-entry arm 只能回答一个入口机制。** 最小设计是同一路径内至少一个可确认未进入的行动，与至少一个确认进入的行动作有界比较；它不能估计冲绳行动的总体进入率或制度效果。
3. **recipient/local response 与“合法性效果”之间仍隔着一层。** 收到物资、说明用途、礼节性致谢、复述“桥梁／友好”话语、把捐赠改写为生活需要／权利／补偿、保持距离或拒绝，必须分开编码。
4. **行动方转载不等于独立地方回应。** 地方媒体只有在提供可归属的 recipient／地方原话或自己的独立框架时，才形成新的 response observation；照抄行动方新闻稿只增加传播渠道，不增加独立回应。
5. **当前最值得做的 LEG2 微型案例是 Ambitious 线，但必须拆事件。** 其自有刊物可检验关系叙事，2024 年蓄电池事件可检验具体地方回应；二者都不能反向闭合 W2-A 的 USD 13,423 申报行，除非账簿证明是同一交易。

## 一、什么才是真正的 matched non-entry

### 1.1 分析单位与入口门槛

分析单位固定为：

> `具名行动／请求 × 具名制度场域 × 预先声明的观察窗口`

“进入”不是统一抽象状态，必须按场域登记门槛：

| 场域 | 本包采用的最低进入门槛 | 已经过门后仍失败，编码为何 |
|---|---|---|
| 法院 | 获得案号／正式立案或法院以案件形式审理 | `entered_then_jurisdiction_or_merits_gate`，不是 non-entry |
| 议会／行政 | 正式收件并进入议程、审议、答复或法定处理流程 | `entered_then_disposition_gate` |
| 公投直接请求 | 签名／条例请求获正式接收并进入审查或议会流程 | 后续否决、改题或不投票仍属 post-entry gate |
| EIA／意见程序 | 在法定窗口内被官方接收为意见／评论 | 未被采纳是 post-entry outcome，不是 non-entry |
| 国际请愿／机构 | 达到该制度明示的登记、受理或阈值状态 | 达标后无政策改变是 response／outcome gap |

因此，W2-C 现有六行不能直接充当 non-entry：宫古陳情已入议会、PFAS 调停至少被报告为收件后却下、安保诉讼与 EIA 诉讼均进入法院、白宫请愿达到阈值，与那国书面答复则原件和对应关系未闭合。它们分别是 post-entry gate、response trace 或 `not_yet_observable`。

### 1.2 真正 non-entry 的六项必要条件

一条记录只有同时满足下列条件，才可进入本轮的 `confirmed_venue_specific_nonentry`：

1. **行动存在**：有具日请求书、送达记录、申请方原件或机构记录，证明不是媒体口号或一般倡议。
2. **场域明确**：请求指向一个具名法院、议会、行政程序、EIA 窗口或国际机制，不能把“政府”当成一个场域。
3. **门槛预先登记**：在看结果前写明该场域何时算进入；不能因案例失败而把门槛移到更后面。
4. **非进入有正面证据**：有退件、不受理、未予登记、资格审查前终止等正式处置，或“申请方原件＋制度规则＋机构 no-record／不受理回应”闭合。单纯搜不到案号不够。
5. **观察窗口闭合**：窗口以该程序的法定截止、正式终局或预先声明的追踪日结束；开放中的请求记 `pending`。
6. **替代路径已审计**：查同一行动是否后来补正进入同一场域、由关联主体重提，或改走另一制度场域。

据此分四种状态：

- `confirmed_venue_specific_nonentry`：该次尝试未越过具名场域入口；
- `delayed_or_resubmitted_entry`：初次未入，后来在同一场域进入；
- `venue_specific_nonentry_with_alternate_entry`：该场域未入，但同一诉求进入另一场域；
- `not_observable`：行动、处置、窗口或后续路径任一项不闭合。

后面三类都不能被压成“制度未进入”。

### 1.3 怎样才叫 matched

一个 arm 至少包含一条确认 non-entry 与一条确认 entry 的参照行动。匹配不是名称相似，而是先固定下列维度：

| 维度 | 最低要求 |
|---|---|
| `route_family` 与场域 | 必须相同；法院、议会、公投、行政答复不能互换 |
| 请求／行动形式 | 同为诉状、条例直接请求、正式意见、调停申请等 |
| 目标事项 | 同一基地／部署项目或同类可比损害；差异必须明示 |
| 制度规则时期 | 同一规则版本或能说明规则变化 |
| 地理与权限层级 | 尽量同一自治层级／管辖；跨市町村须说明地方条例差异 |
| 主体资格与能力 | 个人／组织、法定资格、律师支持、签名规模等至少可观察 |
| 来源可见性 | 两端使用对称的官方记录族，不能一端查法院全卷、一端只查新闻 |

如果核心维度无法匹配，应交付 `arm_not_established`，而不是降低标准凑出一条“负案例”。一对一微型比较只识别可能的入口闸门；它不产生频率、平均效果或总体因果估计。

### 1.4 最强允许措辞

通过全部门槛后，最多写：

> 在预先声明的〔路径、场域、时期〕比较中，一项有正式发起证据的请求没有越过该场域的入口门槛，而匹配参照项进入了正式流程。这个对照显示该路径存在一个可观察的入口闸门；它不代表冲绳民间行动的一般进入率，也不说明该诉求没有通过其他场域产生作用。

不得写“制度拒绝民意”“未进入制度的行动通常失败”或“成功案例只因组织能力更强”，除非以后另有比较设计。

## 二、LEG2 到底在观察什么

### 2.1 先分 response ownership，再分内容

一条 response observation 必须指向一个具名行动／资源事件，并能识别是谁在说话。来源宿主与说话者要分开：

| 来源形态 | 是否构成新的 recipient/local response | 编码边界 |
|---|---|---|
| recipient／运营法人自己的年报、会报、网页、会议记录 | 是 | 原始 response；仍须匹配具体行动或明确的持续关系 |
| 地方政府、社协、学校、医院等直接受赠／执行机构原件 | 是 | 地方机构 response；行政礼仪与政策判断分开 |
| 地方媒体的 recipient／地方人士直接引语 | 是 | 说话者是地方端；媒体提供独立承载与语境 |
| 地方媒体自己的分析／框架 | 可以 | 记为 `independent_local_media_frame`，不冒充 recipient 意见 |
| 地方媒体照抄行动方新闻稿 | 否 | 只记传播／转载；文本指纹或署名显示复用时不得算独立来源 |
| AWWA、DVIDS、USO 等行动方转载 recipient 引语 | 有限 | 可保留 `action_side_hosted_recipient_quote`，但不是独立地方来源；优先找原件或独立报道 |
| 无法识别说话者的“双方表示……” | 否 | 只能作为未决线索，不能分配给地方端 |

### 2.2 内容分类不能压成接受／不接受

| `response_class` | 最小事实含义 | 对 LEG2 的最强含义 |
|---|---|---|
| `receipt_or_use_only` | 确认收到、用途、人数、设备配置 | 只加强 LEG0／地方使用事实，不证明关系叙事被接受 |
| `courtesy_gratitude` | 感谢、敬意、仪式性致辞 | 证明礼节性正面回应；不能写成对军事存在的支持 |
| `relationship_frame_local` | 地方端主动使用“桥梁、友好、跨境支持”等关系语言 | 地方端出现关系建构框架；若无先行 LEG1，不称“吸收了行动方叙事” |
| `narrative_uptake` | 可见的行动方 LEG1 在先，地方端随后明确复述或认领 | 支持“该事项中叙事被传递／复述”，仍不是态度效果 |
| `practical_reinterpretation` | 把资源解释为医疗、教育、福利或现实需要 | 支持实用化竞争解释，不等于伙伴关系接受 |
| `rights_or_compensation_reframe` | 以权利、补偿、行政责任或基地负担重释 | 削弱 goodwill→acceptance 机制，支持竞争框架 |
| `distance_or_refusal` | 明确保留距离、拒绝叙事或拒绝资源 | 反驳该事项上的叙事接受 |

同一段话可以同时有 practical use 与 courtesy，但每个判断都要保留说话者、原文 locator 和独立性。不得把“感谢物资”翻译成“接受美军存在”。

### 2.3 当前微型案例应怎样收紧

W2-A 的 Ambitious 线是最有信息量的首选，但必须拆成两项：

- Ambitious 自有刊物中对 AWWA 长期支持及“冲绳与美国的桥”表述，可检验 `relationship_frame_local` 或在先行 LEG1 闭合后检验 `narrative_uptake`；
- 2024 年蓄电池交付的地方报道含下游机构代表的具体用途与“跨越国境／桥渡”表述，可检验行动特定的 practical use 与地方关系框架。

两项都不自动等于 W2-A `W2A-A073 / USD 13,423` 申报交易。若没有账簿把日期与金额闭合，就给 2024 事件独立 `action_id`，并明确 `transaction_match=no`。Kana-san 的 2023 flyer 可作为更窄的 practical-use 对照，但其“由 AWWA 捐款运营”本身不是关系叙事。

## 三、两个前置包的最小交付结构

### 3.1 包 N：ONE matched non-entry arm

最少四张表：

1. `matched_nonentry_arm_v1.csv`：`unit_id, pair_id, action_actor, target_issue, place, period_start, period_end, route_family, intended_venue, entry_threshold, attempt_evidence_status, entry_status, terminal_disposition, later_same_venue_status, alternate_venue_status, matched_entry_unit_id, match_dimensions, match_limit, allowed_claim, prohibited_inference, review_status`。
2. `nonentry_route_audit_v1.csv`：逐项记录机构索引、案号／议程／收件、补正、关联主体重提与替代场域检索；`not_found` 不能直接生成 non-entry。
3. `source_receipts_v1.csv`：URL、publisher、retrieved_at、exact locator、本地原件、SHA-256、支持行。
4. `principal_review_queue_v1.csv`：只留“行动是否真实发起、入口门槛、终局处置、后续／替代进入、匹配有效性、最强措辞”六类决定。

验收指标不是样本量，而是闭合率：

- 1/1 non-entry 与至少 1/1 entry 参照有行动原件和场域原件；
- 2/2 的入口门槛、观察窗口和制度规则版本已登记；
- non-entry 的后来同场域与替代场域审计完成率 100%；
- 核心分类字段无 `unknown`；否则状态是 `arm_not_established`；
- 负责人逐项确认后，仍只标 `research_only`。

### 3.2 包 L：ONE key recipient／LEG2 microcase

最少四张表：

1. `leg2_response_ledger_v1.csv`：`response_id, tracer_id, action_id, resource_flow_id, response_actor, response_actor_type, source_owner, source_host, voice_attribution, source_date, action_date, exact_locator, original_or_repost, independence_status, action_match_status, transaction_match_status, prior_leg1_id, response_class, review_status, allowed_claim, prohibited_inference`。
2. `leg2_source_provenance_v1.csv`：标出原始地方文件、独立地方报道、行动方转载和疑似复用文本，避免把同一句话计算多次。
3. `leg2_coverage_v1.csv`：以预先选择的 tracer／action 为分母，报告 direct recipient/local original、独立地方来源、同一行动闭合、先行 LEG1、转载-only 与未观察项。
4. `principal_review_queue_v1.csv`：负责人读取日文原文后决定说话者、事件匹配、独立性、response class、是否存在 narrative uptake，以及最大允许措辞。

最低验收为：一个预先声明的具体行动；一份 direct recipient／local original；一份独立地方来源或明确记录其不可得；100% 来源收据；所有引用能定位到具体说话者；若要写 `narrative_uptake`，必须另有时间在先且同一关系事件可比的 LEG1。交易金额可以不闭合，但必须与 990 flow 分离。覆盖率只描述“选定 tracer 中哪些回应层可见”，不得写成地方社会接受比例。

## 四、哪些发现会推翻或修正当前判断

### 对 non-entry 判断

- 找到案号、议程、正式收件或实质处理：改为 `entered` 或 post-entry gate；
- 后来补正进入同一场域：改为 `delayed_or_resubmitted_entry`；
- 同一诉求改走另一场域：只能写 venue-specific non-entry；
- 申请方原件、对象或送达无法核实：降为 `not_observable`；
- 参照案例适用不同规则、主体资格或管辖：取消 matched arm；
- 找到官方材料表明入口差异来自规则变更而非组织路径：比较解释改为制度时期差异。

### 对 LEG2 判断

- recipient 原件显示“桥梁”等文字来自行动方模板／新闻稿：从地方框架降为转载；
- 地方端只说明收到与用途：停在 response-side LEG0，不写叙事传递；
- 地方端以医疗需要、权利、补偿或行政责任重释：把“接受 goodwill”改为竞争性解释；
- recipient 明确拒绝、保持距离或否认伙伴叙事：反驳该 tracer 的叙事接受；
- 2024 事件与 USD 13,423 申报行无法闭合：保留两个事件，不互相验证；
- 出现可比态度／行为变化证据：另开 LEG3 设计，不能在本微型包内自动升级。

## 五、负责人需要作出的最小决定

1. 选择 ONE non-entry 路径与进入参照，并批准该场域的入口门槛与观察窗口；若没有合格候选，同意以 `arm_not_established` 结案。
2. 判断 non-entry 的发起、终局、后来同场域／替代场域状态和匹配有效性。
3. 选择 ONE LEG2 tracer：建议将 Ambitious 的关系叙事与 2024 蓄电池行动分成两个 `action_id`；决定本轮主检验哪一个。
4. 阅读关键日文原文，决定 response ownership、礼节／实用／关系框架／重释类别及最大措辞。
5. 明确两包完成只解除 W2-F 的这两个研究前置，不自动批准 HR-USN2、三份信息公开发送、W2-F 合成或 W2-G 写回。

## 六、lead_only 在这两包里怎样不被滥用

下列事项属于包内核心证据，**不得**放进 `lead_only`：

- 会改变 non-entry、入口门槛、匹配有效性、后来／替代进入的材料；
- 会改变 response 说话者、来源独立性、事件／交易匹配或 response class 的材料；
- 涉及人物同一性、recipient 身份、资金语义或因果归因并已达到人工判断门槛的材料；
- 需要当地原件或信息公开的明确缺口。

这些分别进入主表、change note、competing explanation、人工复核、当地任务或 request ledger。`lead_only` 只容纳真正超出本包选择框的旁线，例如发现另一种未设计的制度渠道、另一个不属于已选 tracer 的 recipient 网络，或一个值得以后另开问题的人物端点。若线索本身能成为当前 matched arm 的候选或推翻当前 LEG2 分类，它已经在包内，不能借 `lead_only` 绕开证据门。

本红队包登记 0 条意外发现；配套 CSV 仅保留 19 列表头。将来有限侦察仍受每链最多三步、单包最多十条、不得进入结论／中央层／人工队列／publication／前端的限制。

## 意外发现登记

本轮 **0 条**。`outputs/us_presence_wave2_nonentry_leg2_redteam_v1/unexpected_findings_register_v1.csv` 为 header-only。本文中的风险、反例和验收条件都是本次方法审计的正式内容，不是题外线索。

## 验收结论

- 当前 W2-C 尚未建立 matched non-entry arm；现有六行继续保持 gate/control。
- 当前 W2-A 已有可做 LEG2 微型案例的原件，但 action、transaction 和 narrative uptake 三种闭合仍须分开。
- 两个前置包可启动为有界调查；任何一个若无法闭合，应如实交付 `not_established／not_observable`，不能为了放行 W2-F 降低定义。
- W2-F、W2-G、中央写回、publication adapter 和前端继续保持未授权。
