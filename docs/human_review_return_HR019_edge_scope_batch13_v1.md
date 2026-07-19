# HR-019 actor–issue edge 范围第三组回交报告 Batch 13

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**负责人已确认——10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 21–30 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 公共机构连到一个争议议题，可能表示管辖、实施、审批或被诉角色，不能自动解释为赞成／反对立场。
- 长期存在的组织参加一次或数次具日动员，不等于该 issue 在组织全生命周期内持续不变。
- umbrella 的成员数量、共同集会和共同声明不生成稳定组织关系。
- 本报告不直接修改中央 edge 表、source log、HR CSV 或图。

## 0A. 重新调查说明

负责人指出初版未展示独立调查过程后，本批撤回初版建议，并于 2026-07-20 对 10 条 edge 逐项补查。调查优先使用组织官网、政府部门官网和正式政府文件；地方媒体用于补足组织行动史。以下新检索页尚未写入中央 source log，只有负责人确认后才形成后续 source proposal／归档任务。

| actor | 本轮新核查材料 | 调查所得 |
|---|---|---|
| A066 ND | [2017 冲绳与亚太安全提言](https://www.nd-initiative.org/research/4750/)、[2024 冲绳地域外交论述](https://www.nd-initiative.org/research/12401/)、[ND 冲绳研究目录](https://www.nd-initiative.org/research/okinawa/)、[边野古替代方案项目](https://www.nd-initiative.org/project/) | 2017–2025 可见持续的边野古替代方案、基地政策和地域外交研究；2024 文本明确讨论地方自治法、代执行和国—地方权限。未找到足够材料维持原 relation basis 中笼统的“国际法”表述。 |
| A074 基地対策課 | [基地対策課现行官网](https://www.pref.okinawa.jp/kensei/kencho/1000011/1017547/1017553.html)、[2022 年县公文书馆所载所掌事务](https://www.archives.pref.okinawa.jp/wp-content/uploads/57165228404c2028cb26c1d476dd1d58.pdf)、[知事公室组织表](https://www.pref.okinawa.jp/kensei/kencho/1000011/1017547/index.html) | 能证明基地政策调查、返还、地位协定、周边生活环境和基地事件应对等行政职责；但官网同时把“边野古新基地建設問題対策課”列为独立部门。本轮没有找到把 A074 本身明确置于“地方自治”论证或案件角色的材料。 |
| A075 沖縄防衛局 | [机构职责](https://www.mod.go.jp/rdb/okinawa/about/information/index.html)、[防卫设施建设](https://www.mod.go.jp/rdb/okinawa/effort/construction/index.html)、[基地负担／普天间替代设施](https://www.mod.go.jp/rdb/okinawa/effort/base/index.html) | 官方资料直接确认其建设、取得、管理防卫设施及实施普天间替代设施相关工作的制度角色；不能解释为反基地立场。 |
| X016 MOSCO | [MOSCO 官网](https://www.moscoki.com/)、[美国海军陆战队 2012 年奖学金报道](https://www.mcipac.marines.mil/Media-Room/News/Article/531919/club-awards-scholarships/) | 当前官网仍将连接社区、支持美日地方组织写为目标；2012 官方军方记录说明奖学金、社区服务、慈善捐赠和 AWWA 参与，支持持续服务功能。 |
| A108 県民の会 | [2023 年成立报道](https://www.qab.co.jp/news/20230919186700.html)、[2023 年组织集会记录](https://nomore-okinawasen.org/12189/)、[2024 年与那国调查记录所在站点](https://nomore-okinawasen.org/) | 成立目的、组织名称及此后反对战场化、和平外交和先岛军事强化调查持续一致，支持 2023 年以来的组织定位。 |
| A111 女団協 | [冲绳县官方女性史资料](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/039/818/16_shiryouhen.pdf)、[冲绳县 2002 年基地问题记录](https://www.pref.okinawa.lg.jp/kititaisaku/DP-08-13.pdf)、[2024 年读谷村议会审查报告](https://www.vill.yomitan.okinawa.jp/material/files/group/49/540T4.pdf)、[2024 年组织行动史报道](https://ryukyushimpo.jp/national/entry-3299439.html)、[2024 年人权动员报道](https://www.okinawatimes.co.jp/articles/-/1474162) | 1995 有明确基地撤去行动，2002 有美军性暴力抗议，2012、2019 再有性暴力／人权相关公开行动，2024 由该会推动县民大会并明确使用人权与尊严框架。反基地仍只能由具日且明确带有基地撤去诉求的行动支持；人权则已呈跨时期反复出现的组织功能。 |

### 调查后的两处实质修订

1. **AI176 从 `institutional_or_case_role` 改为 `remain_unclear`。**“县政府基地事务”只证明 A074 的基地行政职责；不能自行推出 `local_autonomy`。边野古代执行和诉讼材料还存在部门归属混淆风险。
2. **AI222 从 `event_specific` 改为 `organizational_positioning`。**人权／尊严／美军性暴力问责不是 2024 单次标签，而是至少在 1995、2002、2012、2019、2024 多个时期重复出现；这不表示逐年连续或活动强度不变。

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI157 | A066 ND—legal | `organizational_positioning` | 持续政策研究中的行政法、地方自治法和制度论证；删除目前证据不足的笼统“国际法”表述 |
| AI158 | A066 ND—local_autonomy | `organizational_positioning` | 持续讨论国—地方权限、地域外交和冲绳政策替代方案；不代表冲绳整体 |
| AI159 | A066 ND—anti_base | `organizational_positioning` | 由持续边野古／基地政策替代研究支持；须按具体政策主张表述 |
| AI176 | A074 沖縄県知事公室基地対策課—local_autonomy | `remain_unclear` | 现有资料只证明基地行政职责；地方自治论证及边野古程序还可能属于另设部门 |
| AI178 | A075 沖縄防衛局—anti_base | `institutional_or_case_role` | 仅表示基地建设实施／行政争议 actor；绝不表示沖縄防衛局持反基地立场 |
| AI179 | X016 MOSCO—military_family_service | `organizational_positioning` | 军属配偶俱乐部的持续服务／慈善功能；AWWA membership 不生成政治或资金推断 |
| AI206 | A108 沖縄を再び戦場にさせない県民の会—peace | `organizational_positioning` | 自 2023 年成立以来的和平／前线化预防核心目的 |
| AI217 | A108—anti_war | `organizational_positioning` | 组织名称、目的和持续活动直接支持；与 peace 属同一框架 |
| AI221 | A111 沖縄県女性団体連絡協議会—anti_base | `event_specific` | 只按 1995 等具日且明确提出基地撤去的行动使用；2024 人权动员本身不自动证明反基地立场 |
| AI222 | A111—human_rights | `organizational_positioning` | 1995–2024 多期重复的人权、尊严和美军性暴力问责功能；不表示逐年连续 |

建议分布：

- `organizational_positioning`：7 条；
- `institutional_or_case_role`：1 条；
- `event_specific`：1 条；
- `remain_unclear`：1 条。

## 2. AI157 · A066 新外交イニシアティブ（ND）—legal

### 证据判断

S032 组织官网以及本轮补查的具日期政策材料显示，ND 长期使用：

- 行政法、地方自治法、日美地位协定与安全政策制度论证；
- 行政不服、国—地方权限和地方自治讨论；
- 对冲绳基地替代方案的政策研究与传播。

它在本 edge 中是政策研究／倡议组织，不是案件律师、原告或法院程序主体。
本轮未找到足够直接材料证明原 relation basis 中笼统的 `International law`，因此不能原样保留该措辞。

### 辅助建议

**AI157=`organizational_positioning`。**

安全范围：

> `legal` 表示 ND 在持续的冲绳基地政策研究中使用行政法、地方自治法和制度论证。

限制：

- 不写成诉讼代理或具名案件当事人；
- 不从法律论证推断法院采纳或政策效果；
- 未有新增具体来源前，不写成持续使用国际法论证；
- S032 首页应配合具体研究页／发布日期使用，不能由官网身份页单独承担全部时期。

建议 review notes：`sustained_administrative_law_and_policy_argumentation_not_litigation_role;international_law_wording_not_yet_supported`。

## 3. AI158 · A066—local_autonomy

ND 的公开材料持续讨论：

- 冲绳县与中央政府的权限冲突；
- 地方自治法和国—地方“对等／协力”原则；
- 冲绳地域外交和地方层级政策替代方案。

### 辅助建议

**AI158=`organizational_positioning`。**

安全范围：

> `local_autonomy` 表示 ND 持续把冲绳基地／外交政策讨论连接到国—地方权限和地域外交。

限制：

- 不写成 ND 代表冲绳县政府或冲绳居民；
- 不把县政府委托／行政合作候选用于证明政治立场或资金关系；
- 时间范围由具日期政策材料界定。

建议 review notes：`sustained_Okinawa_local_autonomy_and_regional_diplomacy_policy_frame`。

## 4. AI159 · A066—anti_base

ND 的基地政策替代研究、边野古工程批判和海军陆战队运用替代方案并非一次共同声明，而是持续政策议程。

### 辅助建议

**AI159=`organizational_positioning`。**

安全范围：

> `anti_base` 仅表示 ND 在可证研究／政策建议中反对边野古新基地或主张基地政策替代方案。

限制：

- 不把 `anti_base` 扩展成反对所有军事设施或所有日美安保安排；
- 逐份材料记录政策对象、年份和主张，不使用无期限笼统标签；
- 不推断建议获政府或美国机构采纳。

建议 review notes：`sustained_but_policy_specific_base_alternatives_positioning`。

## 5. AI176 · A074 沖縄県知事公室基地対策課—local_autonomy

### 补查所得

A074 是冲绳县政府基地事务部门，不是 NGO。官方所掌事务能够直接证明：

- 基地对策综合企划与协调；
- 驻留军基地调查、返还、地位协定和周边生活环境事务；
- 美军行为所生问题及基地行政联络。

但是，“承担县级基地事务”不能自动推出它以 `local_autonomy` 为议题。现行组织表还把 `辺野古新基地建設問題対策課` 单列；已检出的边野古代执行／诉讼材料主要由该课承担。若把这些材料转归 A074，会混淆两个部门。

### 辅助建议

**修订为 AI176=`remain_unclear`。**

安全范围：

> 目前只能确认 A074 是县级基地行政部门；尚不能确认 AI176 所称 `local_autonomy` edge。

限制：

- 不把部门写成独立社会运动组织；
- 不把冲绳县整体、知事个人或其他部门的全部立场转移给 A074；
- 不把 `辺野古新基地建設問題対策課` 的代执行／诉讼角色无依据地转移给 A074；
- 只有出现由 A074 发布、承办或具名参与的地方自治论证／程序材料，才重新判断为 `institutional_or_case_role`。

建议 review notes：`base_affairs_duties_confirmed_but_local_autonomy_link_not_directly_supported;avoid_Henoko_division_role_transfer`。

## 6. AI178 · A075 沖縄防衛局—anti_base

### 语义问题

S047 支持沖縄防衛局作为边野古工程环境评估／基地建设实施机关，但不能支持其“反基地立场”。当前 `anti_base` issue edge 只能理解为：

- A075 是反基地争议所针对／涉及的公共机构；
- 在工程实施、评估、审批材料和行政争议中承担制度角色。

如果图表把所有 actor–issue edge 解释为“组织持有该立场”，AI178 会产生相反含义。

### 辅助建议

**AI178=`institutional_or_case_role`，并强制标记为 `implementer_or_dispute_target`。**

安全范围：

> 沖縄防衛局因基地建设实施／行政角色进入 `anti_base` 争议场域；该 edge 不表示其反对基地。

限制：

- 禁止进入未显示 relation role／polarity 的立场型二部网络；
- 不把“涉及反基地争议”写成“反基地 actor”；
- HR-029 应考虑增加简洁的 `issue_relation_role`，至少区分 `positioning`、`procedural_actor`、`implementer_or_target`；
- 如最终 actor–issue 数据模型只允许立场边，AI178 应退役并改放程序／行政角色表。

建议 review notes：`base_construction_implementer_or_dispute_target;not_anti_base_position`。

## 7. AI179 · X016 MOSCO—military_family_service

### 证据判断

HR-005 已确认：

- MOSCO／MOSC 的组织身份及税务记录；
- AWWA member club 身份；
- 军属礼品店筹款、奖学金及面向冲绳美／日组织的慈善支持。

这是重复可见的组织功能，不是单次事件。

### 辅助建议

**AI179=`organizational_positioning`。**

安全范围：

> `military_family_service` 表示 MOSCO 作为军属配偶俱乐部持续开展社区、奖学金和慈善服务。

限制：

- 不赋予拥基地、反基地或军事政策立场；
- AWWA membership 是 affiliation，不自动证明资金流；
- 每笔 donation、recipient 和金额须另有年度／关系级证据。

建议 review notes：`core_spouse_club_service_and_charity_function;no_political_inference`。

## 8. AI206 · A108 沖縄を再び戦場にさせない県民の会—peace

### 证据判断

HR-011 已人工确认：

- A108 于 2023 年成立；
- 正式名称、代表、事务局、目的和活动均有组织官网及地方新闻支持；
- 组织明确以防止冲绳再次成为战场、举行全县和平动员为目的；
- 63 团体／个人的 umbrella 形成和集会参与不生成稳定成员／联盟边。

### 辅助建议

**AI206=`organizational_positioning`。**

安全范围：

> `peace` 是 A108 自 2023 年成立以来的核心组织目的和公开动员框架。

限制：

- 不追溯到 2023 年成立前；
- 不由 umbrella 数量推断所有参与团体持续成员关系；
- 不从集会动员推断政策效果。

建议 review notes：`core_peace_and_frontline_prevention_positioning_since_2023`。

## 9. AI217 · A108—anti_war

组织名称、成立目的和持续活动直接以“不要让冲绳再次成为战场”为中心，因此 `anti_war` 不是单次活动标签。

### 辅助建议

**AI217=`organizational_positioning`。**

安全范围：

> `anti_war` 表示 A108 自成立以来防止冲绳战场化的持续定位。

限制：

- 与 AI206、`frontline_prevention`、`Taiwan_contingency` 属同一反战／前线化预防框架；
- 不按多个标签重复计算桥接强度；
- 不推断所有 umbrella 参与者在全部政策细节上立场一致。

建议 review notes：`core_anti_war_positioning_since_2023;overlaps_peace_and_frontline_prevention`。

## 10. AI221 · A111 沖縄県女性団体連絡協議会—anti_base

### 证据判断

HR-013 已人工确认 A111：

- 1967 年成立的全县女性团体网络；
- 1995 年有基地撤去相关行动；
- 2024 年组织反美军性暴力／问责县民大会；
- 现有材料明确要求把这些作为具日期行动，而非证明组织在 1967–2024 全期保持同一反基地行动强度或联盟结构。

本轮补查还发现一项重要反向边界：2024 年会长把女性人权表述为“不论基地赞否都应共同要求”的议题。因此，2024 人权／问责动员不能自行承担 `anti_base` polarity；AI221 应以 1995 等明确提出基地撤去的具日行动为限。

### 辅助建议

**AI221=`event_specific`。**

安全范围：

> A111 的 `anti_base` edge 目前只由 1995 年等明确提出基地撤去的具日组织行动支持。

限制：

- 可以记录多个具日事件，但不得填充中间年份为连续定位；
- 不把活动共同参与者写成稳定联盟；
- 不由女性组织身份自动生成反基地立场。

建议 review notes：`dated_1995_and_2024_base_related_mobilizations_not_full_lifecycle_positioning`。

## 11. AI222 · A111—human_rights

初版只使用 2024 年材料，因此误判为单次事件。本轮补查发现：

- 1995 年官方女性史材料记录女团协等就美军少女性暴力举行抗议，且将基地问题与女性人权连接；
- 2002 年冲绳县基地问题正式记录载有女团协对美军少佐女性暴行未遂事件提出抗议与要求；
- 2012 年有女团协围绕美军集体性暴力事件发表抗议；
- 2019 年有同类女性生命、尊严与人权行动参与记录；
- 2024 年女团协推动县民大会，其会长明确以“县民人权被践踏”、女性尊严、预防和问责表述行动。

这是一项跨时期反复出现的公开组织功能，已经超过单次事件标签。它仍不能证明 1967 年以来逐年连续，也不能把所有加盟团体编码成完全一致的人权组织。

### 辅助建议

**修订为 AI222=`organizational_positioning`。**

安全范围：

> `human_rights` 表示 A111 在多个时期反复把美军性暴力、女性／县民尊严、预防与问责作为公开组织行动议题。

限制：

- 不写成 1967–2024 逐年连续或活动强度恒定；
- 每次行动仍保留年份、事件对象和诉求差异；
- 不把案件事实、犯罪率、制度因果或政策结果归因于组织；
- 共同组织／出席只生成事件角色，不生成联盟。

建议 review notes：`recurrent_1995_2002_2012_2019_2024_rights_dignity_and_US_military_sexual_violence_accountability_function;not_annual_continuity`。

## 12. 本批数据修复项

若负责人确认：

1. AI157–AI159 补入 ND 具日期研究／政策页，不由 S032 首页承担全部时间范围；AI157 删除目前证据不足的笼统 `international law` relation basis。
2. AI176 暂不进入任何地方自治定位／制度图；先查找 A074 本身具名的地方自治论证或程序材料，并避免与边野古新基地建設問題対策課混同。
3. AI178 增加 `implementer_or_dispute_target` 边界：
   - 有 relation role 的程序图可以保留；
   - 无 polarity／role 的立场图必须排除；
   - 若最终 schema 不容纳非立场 edge，则退役 AI178 并转入程序表。
4. AI179 继承 HR-005 服务功能边界，不生成政治或资金推断。
5. AI206、AI217 自 2023 年起算，并与其他前线化标签去重复权。
6. AI221 保持具日事件性，且 2024 人权动员不能自动承担 `anti_base` polarity；AI222 可作为跨时期组织功能，但各次行动仍保留年份，不能用组织成立年份填补无证据年份。

本报告本身不修改中央表、source log、HR CSV 或图。

## 13. 负责人决定

负责人于 2026-07-20 确认本报告全部 10 条建议：

- `organizational_positioning`：AI157、AI158、AI159、AI179、AI206、AI217、AI222；
- `institutional_or_case_role`：AI178；
- `event_specific`：AI221；
- `remain_unclear`：AI176。

本确认只冻结本批人工判断；中央 edge 表、source log、HR CSV 和图留待后续受控合并。
