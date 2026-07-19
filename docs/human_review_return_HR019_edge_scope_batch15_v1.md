# HR-019 actor–issue edge 范围第五组回交报告 Batch 15

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**负责人已确认——10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 41–50 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 本批把“议题内容在某次行动中出现”和“该名称对应持续组织”分开判断。
- `groundwater`、`life_safety`、`health_risk` 不得互相替代：
  - 地下水担忧不自动构成医学健康风险；
  - 生活安全可包括事故、交通、撤离、弹药运输和日常生活风险；
  - `health_risk` 需要电磁波、弹药、污染、暴露或健康影响等直接材料。
- 与那国仍以部署／演习、前线化、自治、公投、台湾邻近和生活安全为主要框架，不机械补环境或健康标签。
- 军属福利组织只按公开可见服务／慈善功能编码，不赋予拥基地或反基地政治立场。
- 本报告不直接修改中央 edge 表、source log、HR CSV 或图。

## 0A. 本轮调查与反向核查

| actor | 本轮核查材料 | 调查所得 |
|---|---|---|
| A115 新婦人沖縄県本部 | [2018 县民投票条例签名报道](https://www.jcp.or.jp/akahata/aik18/2018-06-18/2018061801_03_1.html)、S283 | 2018-06-17 县本部具名启动边野古县民投票条例签名，并由县本部会长说明要推动县民投票成功。它是一个有明确对象和阶段的正式县民投票程序角色，不等于该会对所有公投议题的长期定位。 |
| A010 石垣市民連絡会 | S016、[2017 冲绳县议会一般质询通告](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/020/841/170705ippannsitumon4.pdf)、[石垣部署运动过程报告](https://www.jichiro.gr.jp/jichiken_kako/report/rep_tosa37/08/0802_yre/index.htm)、[2023 住民说明会不参加报道](https://ryukyushimpo.jp/news/entry-1681087.html) | S016 只证明该会参加 2016 年市主办公开讨论会，单独不足以支持 `local_autonomy`。补查材料显示该会在不同阶段反复提出地方住民同意、居民意见表达、信息公开、说明方式和地方决策正当性，支持持续但范围明确的自治／参与定位。必须与 A011 的住民投票直接请求程序角色分开。 |
| A012 宮古島いのちの水を守ろう！ | S020、[宫古每日 2016 年同场报道](https://www.miyakomainichi.com/news/post-89649/)、R4 actor/source QA、HR019 bridge Batch 09 | 两家地方报纸均确认 2016-06-11 的“宮古島 いのちの水を守ろう！ 6・11自衛隊配備を止める市民集会”及其执行委员会，把反部署、地下水源保护和生活／后代关切并置。但具名主体是该场集会执行委员会；未找到该精确名称在事件后作为持续独立组织活动的第二来源。 |
| A013 ミサイル基地いらない宮古島住民連絡会 | S021、[2018 地下水／地质调查报道](https://www.jcp.or.jp/akahata/aik18/2018-12-25/2018122515_01_1.html)、[2019 宫古每日地下水抗议](https://www.miyakomainichi.com/news/post-118211/)、[2020 弹药库安全公开质问](https://ryukyuheiwa.blog.fc2.com/blog-entry-843.html)、[2020 住民生活安全声明](https://www.miyakomainichi.com/news/post-129181/)、[2023 市地域联络会记录](https://www.city.miyakojima.lg.jp/soshiki/shityo/kikaku/hisyokouhou/files/00_kaigirokuR5.7.3.pdf)、[2025 地域联络会记录](https://www.city.miyakojima.lg.jp/soshiki/shityo/kikaku/hisyokouhou/oshirase/files/20250901tiikirennrakukai.pdf) | 原 S021 只支持反导弹／弾药库定位，不支持 AI032/AI033。补查材料则在 2018–2019 多次具名连接地下水、燃料设施、软弱地盘和信息开示，并在 2020–2025 反复提出弹药库事故、运输、交通、居民说明及枪械携行等生活安全要求。可以补强为持续组织定位，但全部风险均按组织主张／请求记录，不确认污染、事故或损害已经发生。 |
| A016 イソバの会 | S011、S052、S068、R4 corrected dispositions；另检索组织名＋`健康`、`電磁波`、`弾薬`、`汚染`、`医療` | S011 是 2015 与那国住民投票结果报道，不支持 A016 健康风险。S052 的可定位组织博文支持“军事实基地不需要”、住民主体自治及岛上生活变得困难；S068 支持 2024 年停止日美联合演习／限制鱼鹰飞行的请求。R4 QA 已明确判定二者都不足以编码 `health_risk`；本轮也未找到可修复该标签的直接材料。反部署／反演习则有跨时期组织材料支持。 |
| X004 AWWA | S041、[NOSCO 的 AWWA 正式功能页](https://nosco.wildapricot.org/awwa)、S077、[琉球新报 40 年福利捐赠报道](https://english.ryukyushimpo.jp/2012/05/09/6954/) | AWWA 由军属配偶俱乐部代表组成，持续审查来自美方与冲绳组织的申请并向福利设施／社区项目提供物品或资金。跨数十年的公开材料支持福利／grantmaking 为持续组织功能；但年度 recipient、金额和成员俱乐部分担仍须逐笔证明。 |

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI241 | A115—referendum | `institutional_or_case_role` | 限于 2018–2019 边野古县民投票条例／投票程序中的签名动员角色 |
| AI024 | A010—local_autonomy | `organizational_positioning` | 多阶段持续提出住民同意、信息公开、居民说明和地方决策参与；不是 A011 的公投程序角色 |
| AI028 | A012—groundwater | `event_specific` | 只限 2016-06-11 集会执行委员会的水源保护框架；持续 actor 身份未闭合 |
| AI029 | A012—anti_military | `event_specific` | 只限同一 6・11 反陆自部署集会／次日抗议安排 |
| AI030 | A012—life_safety | `event_specific` | 只限同一事件把饮用水源、后代生活和部署风险并置；不新增健康因果 |
| AI032 | A013—groundwater | `organizational_positioning` | 2018–2020 多期调查、信息开示和抗议持续提出地下水／燃料设施风险 |
| AI033 | A013—life_safety | `organizational_positioning` | 2020–2025 重复提出弹药库、运输、交通、说明和居民日常安全要求 |
| AI038 | A016—health_risk | `remain_unclear` | 当前三份 source ref 均不能支持 I008；建议从可发布层停用，等待直接健康／暴露材料 |
| AI039 | A016—anti_military | `organizational_positioning` | 2011 年以来博客及 2024 行动支持持续反部署／反演习定位 |
| AI056 | X004—base_community_welfare | `organizational_positioning` | 福利／慈善申请审查与支持是持续功能；不产生政治立场或未证 recipient 边 |

建议分布：

- `organizational_positioning`：5 条；
- `institutional_or_case_role`：1 条；
- `event_specific`：3 条；
- `remain_unclear`：1 条。

## 2. AI241 · A115 新日本婦人の会沖縄県本部—referendum

S283 明确记录：

- 2018-06-17，A115 启动要求制定边野古新基地县民投票条例的签名运动；
- 县本部成员与另一地方团体在那霸地区收集签名；
- 县本部会长说明目标是汇集县民声音并推动县民投票成功。

这是正式县民投票过程中的组织化参加，不只是普通宣传活动；但 A115 并非专门为该公投成立的组织，现有材料也不支持其对各种住民投票的一般长期定位。

### 辅助建议

**AI241=`institutional_or_case_role`。**

安全范围：

> `referendum` 表示 A115 在 2018 年边野古县民投票条例直接请求／签名阶段承担具名动员角色。

限制：

- 不写成县民投票发起组织或唯一组织者；
- 不从签名动员推断投票结果、知事支持效果或工程变化；
- 与地方团体合作收集签名不生成稳定联盟；
- 与 AI240 `anti_base` 属同一具日行动的一部分，不重复计算为两次行动。

建议 review notes：`named_signature_mobilizer_in_2018_Henoko_prefectural_referendum_procedure;not_general_referendum_positioning_or_outcome_claim`。

## 3. AI024 · A010 石垣島に軍事基地をつくらせない市民連絡会—local_autonomy

### 原来源问题

S016 记录的是 2016 年石垣市主办公开讨论会：

- A010 共同代表、事务局成员和推荐发言人出席；
- 市长表示将观察市民／议会是否要求住民投票；
- 但报道没有直接把 A010 的主张写成地方自治或住民自治。

因此 S016 单独只能支持 `event_specific` 的公开讨论参与。

### 补查后的连续性

后续材料显示 A010 跨阶段反复处理：

- 部署候选地周边公民馆／住民反对意见是否被中央政府尊重；
- 未获地方同意是否继续推进部署；
- 市民意见、署名和说明责任如何进入市政／防卫程序；
- 住民说明会是否允许自由提问、是否只是形成既成事实；
- 市有地提供及信息公开的地方决策正当性。

这已超过一次公开讨论会，但不应和 A011 的住民投票直接请求、议会处理及诉讼程序混为一体。

### 辅助建议

**AI024=`organizational_positioning`。**

安全范围：

> `local_autonomy` 表示 A010 在持续反对石垣军事部署的行动中，反复要求居民意见、地方同意、信息公开和说明程序进入地方决策。

限制：

- 不写成 A010 代表全体石垣居民；
- 不把周边公民馆、A011 或共同活动者自动并入 A010；
- 不从自治诉求推断居民多数、住民投票结果或政策效果；
- S016 需由补查来源共同承担，不能单独支持长期定位。

建议 review notes：`recurrent_resident_consent_information_disclosure_and_local_decision_participation_frame;distinct_from_A011_referendum_procedure`。

## 4. AI028/AI029/AI030 · A012 宮古島いのちの水を守ろう！

### 身份与事件范围

S020 和宫古每日的独立报道共同确认：

- 事件全名为“宮古島 いのちの水を守ろう！ 6・11自衛隊配備を止める市民集会”；
- 主体为“同実行委員会”／该集会执行委员会；
- 2016-06-11 约百人参加，诉求包括停止陆自部署、保护地下水源以及把和平生活留给后代；
- 执行委员会安排 6 月 12 日防卫局说明会场外无言抗议。

这改善了事件事实的交叉来源，但没有解决“宮古島いのちの水を守ろう！”是否为事件后继续存在的独立组织。HR019 bridge Batch 09 已由负责人确认其维持 `candidate_only`，不与 A112、A013 或近似名称团体合并。

### 辅助建议

**AI028=`event_specific`。**  
**AI029=`event_specific`。**  
**AI030=`event_specific`。**

安全范围：

> 三条 edge 共同描述 2016 年 6・11 集会执行委员会在一个事件链中把地下水保护、反陆自部署和生活／后代安全并置。

限制：

- 三个 issue 是同一集会框架，不是三个独立组织行动；
- 正式表述应优先使用 `PROV_R4_611_EXECUTIVE_COMMITTEE` 或注明“6・11 集会执行委员会”，不能把活动标题直接当作已证持续组织；
- `life_safety` 只表示饮用水源和生活风险关切，不写成已有健康损害；
- 不与 A112、A013、C015 或其他近似名称团体合并；
- 在身份修复前不得进入长期组织定位层或 bridge 排名。

建议 review notes：

- AI028：`2016_06_11_event_groundwater_frame;event_committee_identity_only`；
- AI029：`2016_06_11_event_anti_JSDF_deployment_frame;event_committee_identity_only`；
- AI030：`2016_06_11_event_drinking_water_and_intergenerational_life_safety_frame;no_health_causality`。

## 5. AI032 · A013 ミサイル基地いらない宮古島住民連絡会—groundwater

### 原来源问题

S021 记录 A013 反对导弹基地和弹药库、向县政府／防卫局提出请求以及参加报告会；正文没有地下水内容。它不能作为 AI032 的直接来源。

### 补查所得

具名材料显示：

- 2018 年 A013 通过信息开示取得燃料设施、弹药库和钻探资料，提出地下水、软弱地盘、空洞／断层风险；
- 2019 年具名抗议要求保护地下水，并继续追问燃料设施与地质条件；
- 后续公开质问把设施事故、燃料和地下水风险继续并置。

这是跨年份重复出现的组织工作，不宜只降为一场活动。证据支持的是 A013 的调查、风险主张和行政追问，不是科学上已确认的污染链。

### 辅助建议

**AI032=`organizational_positioning`。**

安全范围：

> `groundwater` 表示 A013 持续调查并提出军事设施、燃料储存、地质条件与宫古地下水源之间的风险关切。

限制：

- 所有污染／地质风险均归属为组织提出或调查所得；
- 不断言地下水已经被设施污染；
- 不把一般宫古地下水政策或 A112 的研究成果自动转给 A013；
- S021 只能支持 AI031 `anti_military`，AI032 必须补入直接地下水来源。

建议 review notes：`recurrent_group_attributed_groundwater_fuel_and_geological_risk_investigation_2018_onward;no_contamination_causality_finding`。

## 6. AI033 · A013—life_safety

A013 的生活安全材料跨越多个行动阶段：

- 2020 年公开质问弹药库保安距离、火灾／爆炸、弹药运输事故和周边民居安全；
- 2020 年紧急声明直接使用“住民や住民生活の安全”；
- 2021 年要求说明弹药量、住宅邻接、国民保护计划和住民说明；
- 2023 年市地域联络会记录其关于自卫队车辆、集落交通、会议公开和基地对策窗口的请求；
- 2025 年又出现枪械携行所生居民不安等具名意见。

这不是一次附带标签，而是重复进入公开请求和市政协调渠道的组织议题。

### 辅助建议

**AI033=`organizational_positioning`。**

安全范围：

> `life_safety` 表示 A013 持续从弹药库／燃料设施事故、运输、交通、说明责任和居民日常安全角度提出请求。

限制：

- 不推断事故已经发生或官方安全措施无效；
- 不把组织担忧写成独立技术鉴定结论；
- `life_safety` 与 AI032、AI031 常来自同一行动链，分析时去重复；
- S021 不能单独承担本 edge，须补入 2020–2025 直接材料。

建议 review notes：`recurrent_ammunition_transport_traffic_and_resident_daily_safety_requests_2020_2025;group_claims_not_proven_harm`。

## 7. AI038 · A016 与那国島の明るい未来を願うイソバの会—health_risk

### 反向核查

当前 source refs 不能闭合 I008：

- S011：2015 与那国住民投票结果，没有 A016 健康风险主张；
- S052：组织博客可以支持军事部署、住民主体自治、岛上生活和透明度关切，但当前可定位文章没有电磁波、弹药、污染、暴露或健康影响主张；
- S068：2024 年停止日美联合演习及限制鱼鹰飞行请求，没有健康风险内容。

R4 corrected dispositions 已据此拒绝 A016 的 `life_safety` frame 候选。本轮按 A016 精确名称与 `健康`、`電磁波`、`弾薬`、`汚染`、`医療` 组合检索，仍未找到能够修复 I008 的组织原文、直接引语或正式请求。

A016 的组织身份和反部署活动被 HR-003 人工确认，不等于 AI038 这个具体议题 edge 也已经被证明。

### 辅助建议

**AI038=`remain_unclear`，并建议从当前可发布／制图层停用。**

安全范围：

> 当前只能确认 A016 关注部署、联合演习、岛民自治和岛上生活；不能确认其存在 I008 所定义的健康风险主张。

重新激活门槛：

1. A016 自有博文、请求书、声明或采访直接出现电磁波、弹药、污染、暴露或健康影响；
2. 材料须具名 A016，不能以一般与那国居民、政府撤离预案或其他组织替代；
3. 风险仍按组织主张记录，不认证医学因果。

建议 review notes：`current_S011_S052_S068_do_not_support_I008_health_risk;R4_QA_rejected_life_safety_attribution;deactivate_until_direct_group_evidence`。

## 8. AI039 · A016—anti_military

与 AI038 不同，A016 的反部署／反演习定位有直接材料：

- 组织博客自 2011 年起记录与那国军事部署争议；
- 可定位博文明确写“军事实基地不需要”，并把配备后岛上生活／自治变化写为组织关切；
- 2019 年向宫古相关集会发送反对离岛进一步军事化的信息；
- S068 记录 2024 年该会要求停止日美联合演习并限制鱼鹰飞行。

这支持有时间边界的持续组织定位，不仅是 2024 一次请求。

### 辅助建议

**AI039=`organizational_positioning`。**

安全范围：

> `anti_military` 表示 A016 持续反对与那国自卫队部署扩张及日美联合演习，并将其与岛民自治和前线化关切连接。

限制：

- 不把与那国环境化；
- 不写成代表全岛居民或推翻 2015 公投结果；
- 不从反演习请求推断训练停止或政策改变；
- 共同消息／行动不生成 A016 与其他离岛团体的稳定联盟。

建议 review notes：`sustained_Yonaguni_deployment_expansion_and_joint_exercise_opposition;frontline_and_local_autonomy_frame_not_environmentalized`。

## 9. AI056 · X004 American Welfare & Works Association—base_community_welfare

AWWA 正式功能页与跨时期报道支持：

- 由冲绳美军军属配偶俱乐部代表组成；
- 定期审查来自美方组织和冲绳地方福利机构的申请；
- 通过礼品店／旧货店收益购置车辆、医疗／福利设备和其他社区物品；
- 长期向军人社区与冲绳社区提供福利支持。

这是组织的持续服务／慈善功能，不是单次 donation；但它不等于完整的资金网络证据。

### 辅助建议

**AI056=`organizational_positioning`。**

安全范围：

> `base_community_welfare` 表示 AWWA 作为军属俱乐部 umbrella，持续协调申请审查和面向美方／冲绳社区的福利支持。

限制：

- 不赋予 AWWA 拥基地、反基地或基地政策立场；
- umbrella membership 只证明组织隶属／协调结构，不自动证明每个成员俱乐部参与每笔 grant；
- 40 年累计金额不能分配给具体年份、recipient 或成员俱乐部；
- 每笔 recipient、金额、日期和实物／现金性质须由关系级材料另审；
- 与 AI055 `military_family_service` 高度重叠，不作为两个独立政治议题计算桥接。

建议 review notes：`core_long_running_spouse_club_umbrella_welfare_and_grant_review_function;no_political_stance_or_unverified_recipient_inference`。

## 10. 如负责人确认，本批后续动作

1. AI241 继承 2018–2019 边野古县民投票程序边界，不能泛化为 A115 的一般公投定位。
2. AI024 补入地方同意、信息公开和说明程序材料；S016 不单独承担 `local_autonomy`。
3. AI028–AI030 全部限定为 2016 年 6・11 集会执行委员会的事件层，并保留 A012 `candidate_only` 身份边界。
4. AI032／AI033 删除 S021 作为直接 issue 支持的错误用法，补入 2018–2025 具名地下水／生活安全材料。
5. AI038 从可发布／制图层停用，直到出现 A016 自有或直接归属的健康／暴露风险材料；不得用一般与那国生活安全背景补足。
6. AI039 保持反部署／反演习持续定位，并固定与那国前线／自治／生活语境，不环境化。
7. AI056 保持福利服务功能；recipient 与金额继续由 HR-018／关系级证据另审。
8. 所有新增 URL 先进入 source proposal；source inclusion 不自动批准组织关系、风险因果、资金关系或政策效果。
9. 本报告本身不修改中央表、source log、HR CSV 或图，留待 HR019 全批完成后统一合并。

## 11. 负责人确认记录

负责人于 2026-07-20 确认本批全部辅助建议：

- AI241 A115 新日本婦人の会沖縄県本部—`referendum`：`institutional_or_case_role`；
- AI024 A010 石垣島に軍事基地をつくらせない市民連絡会—`local_autonomy`：`organizational_positioning`；
- AI028 A012 宮古島いのちの水を守ろう！—`groundwater`：`event_specific`；
- AI029 A012—`anti_military`：`event_specific`；
- AI030 A012—`life_safety`：`event_specific`；
- AI032 A013 ミサイル基地いらない宮古島住民連絡会—`groundwater`：`organizational_positioning`；
- AI033 A013—`life_safety`：`organizational_positioning`；
- AI038 A016 与那国島の明るい未来を願うイソバの会—`health_risk`：`remain_unclear`，从当前可发布／制图层停用，等待直接组织健康／暴露风险材料；
- AI039 A016—`anti_military`：`organizational_positioning`；
- AI056 X004 American Welfare & Works Association—`base_community_welfare`：`organizational_positioning`。

负责人同时确认：

- A012 三条 edge 只属于 2016 年 6・11 集会执行委员会事件，不把活动标题升级为持续组织，也不与 A112、A013 或近似名称团体合并；
- A013 的地下水／生活安全 edge 须用 2018–2025 直接材料替换或补足 S021，风险均按组织主张记录；
- A016 的反部署／反演习定位成立，但现有来源不能支持 `health_risk`；
- AWWA 只按持续福利／慈善功能编码，不赋予基地政策立场或未证 recipient／资金关系。

本报告作为 10 条人工决定的回交记录；中央 edge 表、HR CSV、source log 与图表仍留待主线程统一合并。
