# HR-019 跨议题 actor 第一组回交报告 Batch 08

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_bridge_actor_review_queue_v0.csv`  
状态：**已完成——10/10 条**

## 0. 批次边界

- 本批复核 HR-019 bridge actor 队列的前 10 个 actor。
- 推荐决定仅使用队列允许值：`include_with_scope`、`candidate_only`、`exclude_from_narrative`。
- “bridge”只表示同一 actor 的可观察行动把不同议题表达、行动场域或制度渠道连接起来，不表示影响力、领导地位、中心性、联盟或因果效果。
- issue 数量不是桥接强度。`groundwater→health_risk→life_safety`、`noise→life_safety→legal` 等常是同一问题被转译成多个分析标签，不能当成彼此独立的五个议题。
- 本批决定 actor 是否可进入跨议题正文及其必要范围；各条 actor–issue edge 的最终时间范围仍由 HR-019 edge-scope 队列逐条决定。
- 本报告不直接修改中央 registry、actor–issue 表、HR CSV、source log、图或报告正文。

## 1. 建议结论总表

| actor | 当前候选 | 辅助建议 | 建议的桥接机制／限制 |
|---|---|---|---|
| A113 宜野湾ちゅら水会 | `mixed_candidate_bridge`，5 issues | `include_with_scope` | PFAS 居民采样／健康请求→市议会请愿、公害调停等程序；是单一污染风险的多渠道转译，不是五个独立议题 |
| A114 全日本港湾労働組合沖縄地方本部 | `mixed_candidate_bridge`，5 | `include_with_scope` | 港湾劳动／罢工能力把基地、先岛军舰寄港与职业安全带入工作场所；多数政治议题边有事件时间 |
| A115 新日本婦人の会沖縄県本部 | `mixed_candidate_bridge`，5 | `include_with_scope` | 县本部把女性／人权、军事性暴力、和平、边野古和公投动员连接；不得转移全国母体全部行动 |
| A047 沖縄平和運動センター | `positioning_bridge`，4 | `include_with_scope` | 长期和平／反基地定位连接边野古与先岛反军事化；4 个标签有明显语义重叠 |
| A048 沖縄一坪反戦地主会 | `positioning_bridge`，4 | `candidate_only` | 土地拒租／收用程序确有反基地—法律—和平连接，但当前 actor 与关东 block 来源发生单位混淆 |
| A052 嘉手納基地爆音差止訴訟原告団 | `case_or_institutional_bridge`，4 | `include_with_scope` | 仅作为嘉手纳各轮噪音诉讼的案件／原告团桥梁：噪音与生活损害→法律程序 |
| A053 普天間基地爆音訴訟団 | `case_or_institutional_bridge`，4 | `include_with_scope` | 仅作为普天间各轮噪音诉讼的案件／原告团桥梁：噪音与生活损害→法律程序 |
| A112 宮古島地下水研究会 | `mixed_candidate_bridge`，4 | `include_with_scope` | 地下水研究／风险表达→水源保护、监测条例与市政回应；不证明自卫队设施污染 |
| A001 Okinawa Environmental Justice Project | `positioning_bridge`，3 | `include_with_scope` | 边野古—儒艮环境争议→美国海洋哺乳动物委员会；是国际制度翻译桥梁 |
| A007 ピースボート | `mixed_candidate_bridge`，3 | `include_with_scope` | 长期 Okinawa project 把和平／反基地、环境传播与对美国社会的倡议连接；不由 NGO 身份自动生成国际边 |

建议分布：`include_with_scope` 9 条，`candidate_only` 1 条，`exclude_from_narrative` 0 条。

## 2. A113 · 宜野湾ちゅら水会

现有五个 issue：

- I006 `groundwater`
- I007 `life_safety`
- I008 `health_risk`
- I011 `legal`
- I020 `environment`

### 证据判断

HR-027 已确认组织身份和 2021–2026 持续性。其可观察机制不是共同署名，而是：

1. 居民筹资委托 PFAS 采样；
2. 围绕学校、社区和饮用水风险提出调查／信息公开请求；
3. 请求血液／健康调查和基地进入调查；
4. 通过市议会请愿、意见书与公害调停等程序推进诉求。

宜野湾市议会记录直接点名该会、共同代表和请愿；地方报道又记录采样、健康调查请求和意见交换要求。

主要来源：

- S273：宜野湾市议会福祉教育常任委员会请愿审查记录；
- S274：宜野湾市议会 PFOS／PFOA 污染对策意见书；
- S275–S278：采样、学校／社区风险和行政请求报道。

### 辅助建议

**A113=`include_with_scope`。**

正文安全表述：

> 宜野湾ちゅら水会把居民主导的 PFAS 采样和健康／生活安全诉求转入市议会请愿、行政请求与公害调停等程序，是“环境风险—生活安全—制度渠道”的在地转译 actor。

限制：

- 五个标签主要是同一 PFAS 问题的不同表达，不写成横跨五个彼此独立领域；
- 记录采样、请求和程序使用，不断言 PFAS 健康因果或污染源已经证明；
- 不与 A099 合并；同场参与不构成联盟。

建议 notes 机制标签：`resident_sampling_to_procedural_request_bridge`。

## 3. A114 · 全日本港湾労働組合沖縄地方本部

现有五个 issue：

- I001 `anti_base`
- I002 `anti_military`
- I007 `life_safety`
- I019 `peace`
- I026 `mobilization`

### 证据判断

HR-027 已确认地方本部身份、2014–2026 连续性以及两个特别重要的行动机制：

- 2015 年以地方本部身份开展反安保法案／边野古相关工作场所行动；
- 2024 年石垣港美国军舰寄港争议中实际发生港湾罢工，并公开使用港湾劳动者安全和民用港军事利用框架；
- 2025 年地方本部报告继续记录 5·15 和平行进及基地议题学习。

主要来源：

- S284：中央劳动委员会命令书；
- S285：冲绳县争议行为届出；
- S286：2015 年地方本部行动报道；
- S287、S288：石垣港寄港争议的议会／国会材料；
- S289：2025 年地方本部和平行进报告。

### 辅助建议

**A114=`include_with_scope`。**

正文安全表述：

> 全港湾沖縄地方本部把基地／先岛军事设施争议转入港湾工作场所，通过集会、游行与罢工等劳动行动表达职业安全和民用港军事利用问题。

范围拆分：

- `life_safety` 可写成地方本部公开的持续职业安全框架；
- `anti_base`、`anti_military`、`peace`、`mobilization` 以 2015、2024、2025 等有日期行动为证，不直接泛化为每位会员或全部时期；
- 不裁断 2024 罢工合法性、实际政策效果或政治影响；
- 共同游行、共同声明或同一港口行动不生成稳定联盟。

建议 notes 机制标签：`port_workplace_and_labor_repertoire_bridge`。

## 4. A115 · 新日本婦人の会沖縄県本部

现有五个 issue：

- I001 `anti_base`
- I010 `referendum`
- I019 `peace`
- I022 `women`
- I023 `human_rights`

### 证据判断

HR-027 已确认这是全国组织的冲绳县本部，并确认 2008、2014、2018、2024 的地方单位行动：

- 县本部围绕驻冲美军性暴力提出请求；
- 官方全国组织材料明确把 2014 年反新基地行动归属于冲绳县本部成员；
- 2018 年开展边野古县民投票签名活动；
- 2024 年县本部与中央本部共同署名军事性暴力／人权请求。

S280 只证明全国组织结构和女性组织身份；S254/S281 中只有明确点名冲绳县本部的部分可以转入 A115；S283 支持 2018 年县本部公投签名行动。

### 辅助建议

**A115=`include_with_scope`。**

正文安全表述：

> 新日本婦人の会沖縄県本部通过地方请求、反新基地行动和县民投票签名，把女性组织参与、军事性暴力／人权、和平与地方程序连接起来。

限制：

- 只使用明确归属于冲绳县本部的行动；
- 全国母体的所有声明和行动不得自动转移给 A115；
- `women` 不仅由组织名称推出，还应由成员组织性质与地方女性议题行动共同支持；
- 党报报道不证明政党隶属，签名行动不证明公投结果或选举效果。

建议 notes 机制标签：`womens_human_rights_to_referendum_bridge`。

## 5. A047 · 沖縄平和運動センター

现有四个 issue：

- I001 `anti_base`
- I002 `anti_military`
- I003 `Henoko`
- I019 `peace`

### 原来源问题

S031 是组织网站首页，可以支持身份和当前存在，但现有 edge 文本把四条议题全部压在同一来源上，证据定位不足。补查获得：

- 2009 年 QAB 报道明确记载由该中心举行反对与那国自卫队配备的集会，支持 `anti_military`；
- 2015、2018、2020 多个材料记录中心及其负责人在边野古行动、5·15 和平行进中的持续角色；
- 2018 年地方报道记录第 26 次定期总会及县民投票活动方针，证明它不是单次事件 actor；
- 2026 年材料仍显示组织结构与活动连续性，但本批不处理成员／政党组织关系。

补查来源：

- `https://www.qab.co.jp/news/2009072910863.html`
- `https://www.peace-forum.com/houkoku/20180511.html`
- `https://ryukyushimpo.jp/news/entry-1113157.html`
- `https://www.okinawatimes.co.jp/articles/-/351573`

### 辅助建议

**A047=`include_with_scope`，保留 `positioning_bridge`。**

正文安全表述：

> 沖縄平和運動センター长期把和平运动与反基地行动连接，并分别进入边野古新基地和与那国／先岛自卫队部署争议，是可观察的长期定位型 bridge。

限制：

- `anti_base`、`Henoko` 与 `peace` 高度重叠，不能把四个标签当成四倍桥接强度；
- 中心是组织协调 actor，不等于所有参加者、构成团体或合作行动均持完全相同立场；
- 补查来源应进入 source proposal，S031 不再单独承担全部议题边。

建议 notes 机制标签：`peace_anti_base_and_sakishima_positioning_bridge`。

## 6. A048 · 沖縄一坪反戦地主会

现有四个 issue：

- I001 `anti_base`
- I009 `local_autonomy`
- I011 `legal`
- I019 `peace`

### 证据与实体问题

一坪反战地主运动本身有明确桥接机制：

- 以共有军事用地和拒绝租赁支持反战地主；
- 通过土地使用裁决、收用程序和相关诉讼进入法律渠道；
- 把军用地返还表达为生活／生产空间和反基地／和平问题。

但是当前 registry 和来源存在组织单位错配：

- A048 的 canonical name 是不带地区限定的 `沖縄一坪反戦地主会`；
- S038 `https://www.jca.apc.org/HHK/` 明确是东京地址的 `沖縄・一坪反戦地主会関東ブロック`；
- 该网站的历史材料同时出现关东 block、关西 block、反战地主会和“一坪反戦地主会代表世話人”，说明这些名称不能无条件合并成一个当前 actor；
- Batch 06 已决定 S038 不能被写成 A048 的冲绳办公室；这同样影响 bridge 归属。

补查来源：

- `https://www.jca.apc.org/HHK/`
- `https://www.jca.apc.org/HHK/Kokaishinri/sojyo980814.html`
- `https://www.jca.apc.org/HHK/Kokaishinri/Kokaishinri_copy.html`
- `https://kotobank.jp/word/%E4%B8%80%E5%9D%AA%E5%8F%8D%E6%88%A6%E5%9C%B0%E4%B8%BB%E4%BC%9A-154581`

### 辅助建议

**A048=`candidate_only`。**

理由不是桥接机制不存在，而是当前 actor 归属未冻结。主线程在进入正文前应先决定：

1. A048 是否表示 1982 年成立的总体／原始一坪反战地主会；
2. 关东 block 是否应作为独立 actor，或只作为 A048 的地区组织 relation；
3. 关东 block 的 2020–2026 行动能否归入 A048，还是必须分开；
4. `local_autonomy` 是否有 A048 本体的直接来源，而不只是研究者的解释性标签。

候选安全表述：

> 一坪反战地主运动可能通过军用地共有、拒租和收用程序连接反基地、和平与法律行动；现有 registry 尚未充分区分冲绳本体和关东 block，暂不作为已冻结 actor bridge 写入正文。

建议 notes 机制标签：`land_ownership_legal_resistance_candidate_bridge`。

## 7. A052 · 嘉手納基地爆音差止訴訟原告団

现有四个 issue：

- I001 `anti_base`
- I007 `life_safety`
- I011 `legal`
- I021 `noise`

### 证据判断

HR-012 已确认 A052 是从第一轮延续至第四轮的原告团 actor，并把具体轮次作为 `round_of`，但不推定各轮个体成员恒定。HR-014 又确认第三次嘉手纳案件：

- 原告通过民事差止与损害赔偿诉讼表达航空器噪音和生活负担；
- 过去噪音损害赔偿获维持；
- 运营／噪音差止和未来损害请求未获支持；
- A052 是案件特定 plaintiff-group crosswalk。

主要材料：

- `outputs/R08_legal_procedure_v0/cases_v0.csv`
- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`
- S149、S151、S155 的跨轮次身份材料；
- S133、S134 的第三次案件材料。

### 辅助建议

**A052=`include_with_scope`，保留 `case_or_institutional_bridge`。**

正文安全表述：

> 嘉手纳基地爆音差止诉讼原告团把航空器噪音和日常生活损害转译为人格利益、损害赔偿和运行差止等法律请求，是严格案件／诉讼轮次范围内的制度桥梁。

限制：

- 不写成全领域长期反基地协调中心；
- `anti_base` 只限其对基地噪音／运行负担的诉讼性表达；
- 赔偿不表示噪音停止，未获得运行禁令；
- 各轮原告个体和律师团不得视为恒定不变。

建议 notes 机制标签：`noise_life_harm_to_litigation_bridge`。

## 8. A053 · 普天間基地爆音訴訟団

现有 issue 与 A052 相同：

- I001 `anti_base`
- I007 `life_safety`
- I011 `legal`
- I021 `noise`

### 证据判断

HR-012 已确认 A053 跨第一、第二、第三次普天间噪音诉讼的持续组织身份，并把具体轮次与本体分开。HR-014 确认：

- 官方判决记录航空器噪音、睡眠／健康焦虑和日常生活负担；
- 2018／2020 并合案件对部分原告、部分期间判给赔偿；
- 其余请求被驳回，本案没有形成运营禁令；
- A053 是案件特定 plaintiff-group crosswalk。

主要材料：

- `https://www.courts.go.jp/assets/hanrei/hanrei-pdf-91354.pdf`
- `https://okinawagodo.org/blog/1230/`
- `outputs/R08_legal_procedure_v0/cases_v0.csv`
- `outputs/R08_legal_procedure_v0/case_actor_roles_v0.csv`

### 辅助建议

**A053=`include_with_scope`，保留 `case_or_institutional_bridge`。**

正文安全表述：

> 普天间基地爆音诉讼团把航空器噪音及睡眠、健康焦虑和日常生活负担转入期间损害赔偿等司法程序，是严格诉讼范围的制度桥梁。

限制与 A052 相同：

- 不泛化为所有普天间生活安全组织；
- 不推定并合案、不同轮次或个体成员完全相同；
- 部分赔偿不等于运行被限制或基地争议获得实质解决。

建议 notes 机制标签：`noise_life_harm_to_litigation_bridge`。

## 9. A112 · 宮古島地下水研究会

现有四个 issue：

- I006 `groundwater`
- I007 `life_safety`
- I008 `health_risk`
- I020 `environment`

### 证据判断

HR-027 已确认 2018–2025 持续性、正式规则、领导时间线和市政府正式回应。组织的桥接机制包括：

- 地下水／水文研究和公开学习；
- 把自卫队设施用水与排水作为其提出的地下水风险类别；
- 提议扩大水道水源保护区域、监测和条例覆盖；
- 通过请求和政策文件进入宫古岛市行政回应。

主要来源：

- S158、S204：组织概要与活动档案；
- S269：组织对地下水风险的公开框架；
- S270：水源保护区域和监测政策主张；
- S271：宫古岛市正式回应。

### 辅助建议

**A112=`include_with_scope`。**

正文安全表述：

> 宮古島地下水研究会把地下水研究和环境风险表达转入饮用水源保护、监测规则与市政回应，形成“环境知识—生活安全—行政接口”的持续 bridge。

限制：

- 四个标签主要是同一地下水问题的风险／治理分层，不作四个独立运动领域；
- 组织提出自卫队设施排水风险，不等于已经证实设施造成污染或健康损害；
- 不与 C015、A012、A097 合并，也不从相同议题推断组织关系。

建议 notes 机制标签：`groundwater_knowledge_to_municipal_policy_bridge`。

## 10. A001 · Okinawa Environmental Justice Project

现有三个 issue：

- I003 `Henoko`
- I004 `dugong`
- I012 `international_advocacy`

### 证据判断

OEJP 自有材料明确：

- 项目以连接冲绳环境议题为公开使命；
- 2020 年由 OEJP 牵头，71 个冲绳、日本及菲律宾民间团体向美国海洋哺乳动物委员会提交请求与公民社会报告；
- 请求把边野古—大浦湾基地工程与冲绳儒艮保护、美国国防部的保护判断和美国联邦机构监督联系起来；
- 官方博客档案持续更新到 2026 年，说明它不是一次性活动名称。

来源：

- `https://okinawaejp.blogspot.com/`
- `https://okinawaejp.blogspot.com/2020/07/`
- S006、S007、S008。

### 辅助建议

**A001=`include_with_scope`，保留 `positioning_bridge`，但明确它是项目型／国际制度翻译 bridge。**

正文安全表述：

> Okinawa Environmental Justice Project 把边野古—大浦湾的儒艮与环境争议翻译成面向美国海洋哺乳动物委员会和美国国防部保护责任的国际制度诉求。

限制：

- Henoko、dugong 与 international advocacy 在这里属于同一倡议链，不是三个独立领域；
- 71 团体共同提交不等于稳定联盟；
- “牵头”只按 2020 年材料的公开角色使用，不推断政策影响、委员会采纳或项目规模。

建议 notes 机制标签：`local_environment_to_us_institution_translation_bridge`。

## 11. A007 · ピースボート

现有三个 issue：

- I001 `anti_base`
- I012 `international_advocacy`
- I019 `peace`

### 原来源问题

S005 证明 Peace Boat 参与 2015 年边野古／珊瑚礁紧急声明，但单条声明不足以支持长期 bridge。补查官方项目页显示：

- Peace Boat 有独立、长期的 `OKINAWA` 项目；
- 1984 年以来多次访问冲绳，并开展普天间、边野古、战迹等主题活动；
- 参与边野古／大浦湾环境网络、国会行动、媒体传播和意见广告；
- 官方项目页明确写其同时面向美国社会和日本本土舆论开展工作；
- 2019 年日韩 cruise 让参与县民投票的冲绳青年与跨国乘船者交流；
- 组织本身是以和平教育、冲突预防和国际交流为持续定位的国际 NGO。

补查来源：

- `https://peaceboat.org/projects/okinawa.html`
- `https://peaceboat.org/about.html`
- `https://peaceboat.org/3620.html`
- `https://peaceboat.org/4442.html`

### 辅助建议

**A007=`include_with_scope`。**

正文安全表述：

> ピースボート通过长期 Okinawa 项目，把冲绳和平／反基地议题与环境传播、船上交流、日本本土舆论及面向美国社会的倡议连接起来。

限制：

- `international_advocacy` 由沖縄项目的对美／跨国行动支持，不是从“国际 NGO”身份自动推出；
- 共同声明、网络成员或共同活动不构成稳定联盟；
- 不把乘船者、青年参与者或合作网络的全部行为归给 Peace Boat；
- 不从宣传和交流活动推断政策效果。

建议将 bridge 分类从宽泛 `mixed_candidate_bridge` 收窄为 notes 中的 `peace_environment_transnational_outreach_bridge`。

## 12. 本批共同解释规则

若负责人确认，本批正文层按三类机制写，不按 issue 数排名：

1. **持续定位／政策翻译**
   - A047：和平—反基地—先岛反军事化；
   - A112：地下水知识—水源保护—市政回应；
   - A001：儒艮／边野古—美国制度；
   - A007：和平／反基地—环境传播—跨国／对美倡议。
2. **行动场域／程序转换**
   - A113：居民采样—健康／生活诉求—请愿／调停；
   - A114：基地／军港争议—港湾劳动与职业安全；
   - A115：女性／人权—和平／边野古—公投动员。
3. **严格案件桥梁**
   - A052、A053：噪音／生活损害—诉讼请求与司法产出。

A048 暂留 candidate layer，待组织单位修复后再进入其中一类。

## 13. 如负责人确认，本批主线程动作

1. 在 HR019 bridge queue 回填 9 条 `include_with_scope`、A048 一条 `candidate_only`。
2. 将本报告的机制标签和限制写入 `review_notes`，不得只留下一个无范围的 include。
3. A047、A001、A007 的新增官网／独立材料先进入 source proposal；source inclusion 不自动批准其 edge。
4. A048 建立实体修复项，区分原始／总体一坪反战地主会、关东 block、关西 block 和反战地主会；修复前不进入正式 bridge 正文。
5. A052、A053 只使用 HR-014 已审案件事实，保留 round／individual-membership 边界。
6. A112–A115 的 HR-027 actor 决定不自动替代 edge review；后续 HR019 edge-scope 仍须逐条确认。
7. HR019 全部 bridge 与 edge-scope 完成后，重新生成 cross-issue actors、bridge mechanism figure 和报告段落；不得按当前 issue_count 直接排名影响力。

本报告本身未修改中央表、HR CSV、source log 或图表。

## 14. 负责人决定

负责人于 2026-07-19 确认本批全部辅助建议：

- A113 宜野湾ちゅら水会：`include_with_scope`；
- A114 全日本港湾労働組合沖縄地方本部：`include_with_scope`；
- A115 新日本婦人の会沖縄県本部：`include_with_scope`；
- A047 沖縄平和運動センター：`include_with_scope`；
- A048 沖縄一坪反戦地主会：`candidate_only`；
- A052 嘉手納基地爆音差止訴訟原告団：`include_with_scope`；
- A053 普天間基地爆音訴訟団：`include_with_scope`；
- A112 宮古島地下水研究会：`include_with_scope`；
- A001 Okinawa Environmental Justice Project：`include_with_scope`；
- A007 ピースボート：`include_with_scope`。

负责人同时确认：

- bridge 只按本报告所列机制与范围进入正文，不以 issue 数量作为影响力或桥接强度；
- A052、A053 只作为案件／诉讼轮次范围内的制度桥梁；
- A112、A113 的多个标签是同一地下水／PFAS 风险的分层表达，不得写成多个独立运动领域；
- A114 的罢工与港口行动只记录发生、公开理由和场域，不裁断合法性、效果或联盟；
- A115 只继承明确归属于冲绳县本部的地方行动；
- A001、A007 的国际渠道不生成稳定联盟或政策效果；
- A048 在原始／总体一坪反战地主会与关东 block 的组织单位修复完成前，只保留为 `candidate_only`。

本报告作为 10 条人工决定的回交记录；中央表、HR CSV、source log 与图表仍留待主线程统一合并。
