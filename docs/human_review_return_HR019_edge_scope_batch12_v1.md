# HR-019 actor–issue edge 范围第二组回交报告 Batch 12

日期：2026-07-20  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**已完成——10/10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列第 11–20 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 服务型军属组织只按观察到的服务功能编码，不赋予拥基地或反基地立场。
- 非冲绳的资助／方法样本不得因 actor 后来出现先岛活动而倒推成冲绳项目或资金关系。
- 原告团的生活安全 edge 必须限定于具体噪音诉讼及轮次，不等于所有基地生活风险的代表组织。
- 本报告不直接修改中央 edge 表、source log、HR CSV 或图。

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI057 | X005 NOSCO—military_family_service | `organizational_positioning` | 军属配偶俱乐部的持续服务／慈善功能；AWWA membership 是组织 affiliation，不是政治立场 |
| AI068 | X015 Peace Winds Japan—international_cooperation | `event_specific` | 当前 edge 只由 2018 年西日本／北海道 USAID 灾害救援样本支持；与先岛活动和冲绳资金无关 |
| AI106 | A045 Center for Biological Diversity—legal | `institutional_or_case_role` | 严格限于冲绳儒艮案具名组织原告角色 |
| AI116 | A048 沖縄一坪反戦地主会—legal | `remain_unclear` | 土地拒租／收用法律机制可信，但 S038 属关东 block；组织单位未修复前不能归给 A048 本体 |
| AI119 | A049 行动する女たちの会—life_safety | `organizational_positioning` | 女性人权、军事性暴力与日常安全是持续组织框架，不是一般化“治安”标签 |
| AI121 | A049—anti_military | `organizational_positioning` | 反对军事结构性暴力是持续定位；不代表每次行动或所有成员观点完全相同 |
| AI126 | A051 「辺野古」県民投票の会—Henoko | `institutional_or_case_role` | 严格限于 2018–2019 边野古填海县民投票过程；组织已解散 |
| AI127 | A051—local_autonomy | `institutional_or_case_role` | 地方自治通过直接请求／县民投票程序表达，不是无限期一般自治组织 |
| AI129 | A052 嘉手纳爆音诉讼原告团—life_safety | `institutional_or_case_role` | 噪音、睡眠与日常生活损害进入各轮诉讼；轮次成员不得假定相同 |
| AI132 | A053 普天间爆音诉讼团—life_safety | `institutional_or_case_role` | 同样限定于普天间各轮噪音诉讼；部分赔偿不等于噪音停止或运行禁令 |

建议分布：

- `organizational_positioning`：3 条；
- `institutional_or_case_role`：5 条；
- `event_specific`：1 条；
- `remain_unclear`：1 条。

## 2. AI057 · X005 NOSCO—military_family_service

### 证据判断

HR-005 已人工确认：

- NOSCO 是独立的军属配偶俱乐部；
- S055 组织官网确认其属于 AWWA umbrella 下五个 spouse clubs 之一；
- 组织的公开功能是军属社区服务、慈善筹款／grant 活动；
- 完整受益机构和年度金额仍需要 Form 990 或内部年度记录。

### 辅助建议

**AI057=`organizational_positioning`。**

安全范围：

> `military_family_service` 表示 NOSCO 作为军属配偶俱乐部持续面向基地／军属社区开展服务和慈善活动。

限制：

- 不从军属服务推断拥基地、反基地或其他安全政策立场；
- AWWA membership 是组织 affiliation，不是 funding edge，也不证明具体 grant recipient；
- 不把 AWWA 或其他 spouse clubs 的活动自动转移给 NOSCO；
- 具体 recipient、金额和年度仍须关系级证据。

建议 review notes：`core_spouse_club_service_function;AWWA_affiliation_not_political_or_funding_inference`。

## 3. AI068 · X015 Peace Winds Japan—international_cooperation

### 原 edge 与后续补查的区别

AI068 当前依据是：

- S087：2018 年西日本水灾／北海道地震中的 USAID 灾害救援支持；
- S088：Peace Winds 在日本的灾害救援背景；
- 该事实与冲绳、基地、先岛安全或当地项目资金没有关系。

HR019 Batch 01 后续另查到：

- PWJ FY2024 把社区防灾联系网络扩展到先岛；
- 冲绳国民保护训练材料把其医疗支援船列为“正在协调”的候选资源；
- 这些新事实支持有限的 Sakishima／`life_safety` 候选，不支持把 2018 USAID 资金连接至先岛，也不自动支持 `international_cooperation` edge。

### 辅助建议

**AI068=`event_specific`。**

安全范围：

> 当前 `international_cooperation` edge 只记录 2018 年 USAID 支持的西日本／北海道灾害救援方法样本，并保持在方法／比较样本层。

限制：

- 不进入冲绳 actor–issue 正文或默认网络；
- 不把 2018 USAID support 写成先岛项目资金；
- FY2024 先岛防灾与候选船角色须分别走 `life_safety`、place 和 event/procedure review；
- 不推断实际撤离任务、合同、稳定政府合作或军事立场。

建议 review notes：`2018_non_okinawa_USAID_disaster_relief_sample_only;Sakishima_facts_separate_review`。

## 4. AI106 · A045 Center for Biological Diversity—legal

### 证据判断

S004 只记录 2015 年共同声明，不能单独支持 `legal` edge。HR-014 的官方第九巡回法院判决已经确认：

- A045 是冲绳儒艮案具名组织原告／上诉人；
- 不是律师；
- 其法律角色只在该案成立；
- 2020 年终局维持国防部合规判断，没有停止工程。

### 辅助建议

**AI106=`institutional_or_case_role`。**

安全范围：

> A045 的 `legal` edge 严格表示其在冲绳儒艮案中的具名组织原告／上诉人角色。

限制：

- 补入 HR-014 官方判决来源；S004 共同声明不能独立承担该 edge；
- 不写成 counsel；
- 不从共同诉讼或共同声明推断稳定联盟；
- 不推断胜诉、政策采纳或项目停止。

建议 review notes：`okinawa_dugong_case_named_plaintiff_only;replace_S004_as_legal_support`。

## 5. AI116 · A048 沖縄一坪反戦地主会—legal

### 机制与实体归属冲突

军用地共有、拒绝租赁、土地使用裁决／收用程序确实形成法律行动机制。但 Batch 08 已确认：

- A048 canonical name 是无地区限定的 `沖縄一坪反戦地主会`；
- S038 明确属于东京地址的 `沖縄・一坪反戦地主会関東ブロック`；
- 网站历史材料同时出现总体／原始组织、关东 block、关西 block 和其他反战地主名称；
- 当前 registry 尚未冻结这些组织单位的 crosswalk。

### 辅助建议

**AI116=`remain_unclear`。**

理由：

- 不是法律机制不成立，而是现有来源不能可靠把该机制和活动时期归给 A048 本体；
- 若现在标为 `organizational_positioning`，会把关东 block 的材料无条件转移给 A048；
- 若标为 `institutional_or_case_role`，又缺少具体案件／程序与 A048 本体的精确 crosswalk。

后续门槛：

1. 决定 A048 是否表示 1982 年成立的总体／原始组织；
2. 建立关东／关西 block 的独立 actor 或地区组织关系；
3. 为 A048 本体找到直接土地拒租／收用程序来源；
4. 再决定是长期定位还是制度角色。

建议 review notes：`legal_mechanism_real_but_actor_unit_unresolved;S038_is_Kanto_block`。

## 6. AI119 · A049 行动する女たちの会—life_safety

### 证据判断

S039 与组织关联空间 `すぺーす結` 的官网／声明档案显示：

- 组织在 1995 年军事性暴力事件后形成；
- 长期以女性人权、军事结构性暴力和日常生活安全讨论基地／军队问题；
- `life_safety` 不是一般治安标签，而是性别化的人身安全与生活风险框架。

补充来源：

- `https://space-yui.com/`
- `https://space-yui.com/?cat=3`

### 辅助建议

**AI119=`organizational_positioning`。**

安全范围：

> A049 的 `life_safety` edge 表示其持续从女性人权和军事性暴力角度处理人身／日常安全问题。

限制：

- 不把所有美军相关犯罪或个案归给该组织；
- 不从组织框架推断犯罪因果、发生率或政策效果；
- I022 `women`、I023 `human_rights` 仍须作为缺边候选另审，不能由本项自动加入。

建议 review notes：`gendered_life_safety_and_military_violence_positioning`。

## 7. AI121 · A049—anti_military

组织名称、自 1995 年以来的成立脉络和持续声明均显示，对军事结构性暴力的批判不是单次事件标签。

### 辅助建议

**AI121=`organizational_positioning`。**

安全范围：

> `anti_military` 表示 A049 对军队／基地结构性暴力的持续组织定位，并与女性人权及生活安全框架相连。

限制：

- 与 AI119 属同一性别化军事暴力框架，不按两个独立机制加权；
- 不把所有参与者、共同声明者或使用 `すぺーす結` 的团体视为 A049 成员；
- 不推定所有成员对每项军事政策持完全一致立场。

建议 review notes：`core_anti_military_positioning_through_gendered_violence_frame`。

## 8. AI126 · A051 「辺野古」県民投票の会—Henoko

### 证据判断

2019 年县民投票问题明确针对边野古美军基地建设填海。A051 是该程序的发起／直接请求 actor，且生命周期已确认：

- 可证核心活动期为 2018–2019；
- 2019-03-26 决议解散；
- 解散后的个人或新组织活动不得归给 A051。

### 辅助建议

**AI126=`institutional_or_case_role`。**

安全范围：

> `Henoko` edge 只限于 A051 推动边野古填海县民投票的程序期。

限制：

- 不写成长期边野古行动组织；
- 不把所有投票参与者、签名者或后续运动视为 A051 成员；
- 不从公投程序推断政府响应或工程变化。

建议 review notes：`2018_2019_henoko_prefectural_referendum_object;dissolved_2019_03_26`。

## 9. AI127 · A051—local_autonomy

`local_autonomy` 的可观察机制是：

- 条例制定直接请求；
- 县民投票；
- 通过地方制度表达对边野古填海的意见。

它不是 A051 对所有地方自治议题的长期介入。

### 辅助建议

**AI127=`institutional_or_case_role`。**

安全范围：

> 此 edge 只表示 A051 在边野古县民投票过程中使用直接民主／地方程序表达地方自治诉求。

限制：

- 与 AI126 和 referendum edge 属于同一程序链；
- 不按三个独立桥接领域计算；
- 不推断 A051 代表全体冲绳居民或所有地方自治议题。

建议 review notes：`local_autonomy_through_specific_prefectural_referendum_procedure`。

## 10. AI129 · A052 嘉手纳爆音诉讼原告团—life_safety

### 证据判断

HR-012、HR-014 已确认：

- A052 是从第一轮延续至第四轮的原告团 actor；
- 具体诉讼轮次使用 `round_of`，不得假定个体成员恒定；
- 噪音、睡眠、健康焦虑和日常生活负担被转译为损害赔偿／运行差止请求；
- 部分历史损害获赔不等于运行差止获得支持。

### 辅助建议

**AI129=`institutional_or_case_role`。**

安全范围：

> `life_safety` edge 限于嘉手纳各轮噪音诉讼中主张的日常生活、睡眠、健康焦虑和人格利益损害。

限制：

- 不泛化为所有嘉手纳生活安全议题；
- 不把不同轮次原告个体视为完全相同；
- 不把赔偿写成噪音停止、运行受限或案件全面胜诉。

建议 review notes：`Kadena_noise_litigation_life_harm_role_across_bounded_rounds`。

## 11. AI132 · A053 普天间爆音诉讼团—life_safety

### 证据判断

HR-012、HR-014 已确认：

- A053 跨第一、第二、第三次普天间噪音诉讼持续；
- 各轮和并合案件不意味着个体成员完全相同；
- 法院材料记录噪音、睡眠／健康焦虑和日常生活负担；
- 部分期间／原告获赔，但没有形成运行禁令。

### 辅助建议

**AI132=`institutional_or_case_role`。**

安全范围：

> `life_safety` edge 限于普天间各轮噪音诉讼中进入司法程序的日常生活和健康／睡眠损害主张。

限制：

- 不泛化为所有普天间生活安全组织；
- 不把轮次、并合案和成员身份无条件合并；
- 部分赔偿不表示基地运行或噪音已经停止。

建议 review notes：`Futenma_noise_litigation_life_harm_role_across_bounded_rounds`。

## 12. 本批数据修复项

若负责人确认：

1. AI057 保持服务功能定位；AWWA membership 不转成资金或政治 edge。
2. AI068 只保留为 2018 年非冲绳方法样本，并从默认冲绳 narrative 排除；先岛新事实走独立 edge/place/event review。
3. AI106 以 HR-014 官方判决替换 S004 作为 `legal` edge 的主要支持。
4. AI116 保持 `remain_unclear`，与 A048 identity repair 绑定。
5. AI119、AI121 补入 A049 组织关联官网／声明档案；I022/I023 只作后续缺边候选。
6. AI126、AI127 继承 A051 2019-03-26 解散边界。
7. AI129、AI132 继承 HR-012 round crosswalk 和 HR-014 案件限制。

本报告本身不修改中央表、source log、HR CSV 或图。

## 13. 负责人决定

负责人于 2026-07-20 确认本批全部辅助建议：

- AI057 X005 NOSCO—`military_family_service`：`organizational_positioning`；
- AI068 X015 Peace Winds Japan—`international_cooperation`：`event_specific`；
- AI106 A045 Center for Biological Diversity—`legal`：`institutional_or_case_role`；
- AI116 A048 沖縄一坪反戦地主会—`legal`：`remain_unclear`；
- AI119 A049 行动する女たちの会—`life_safety`：`organizational_positioning`；
- AI121 A049—`anti_military`：`organizational_positioning`；
- AI126 A051 「辺野古」県民投票の会—`Henoko`：`institutional_or_case_role`；
- AI127 A051—`local_autonomy`：`institutional_or_case_role`；
- AI129 A052 嘉手纳爆音诉讼原告团—`life_safety`：`institutional_or_case_role`；
- AI132 A053 普天间爆音诉讼团—`life_safety`：`institutional_or_case_role`。

负责人同时确认：

- NOSCO 只按军属配偶俱乐部的服务／慈善功能编码；AWWA membership 不生成资金关系或政治立场；
- AI068 只记录 2018 年西日本／北海道 USAID 灾害救援方法样本，不连接 FY2024 先岛防灾活动或冲绳资金；
- AI106 使用 HR-014 官方判决固定 CBD 的具名组织原告角色，S004 共同声明不承担法律 edge；
- AI116 在 A048 本体与关东 block 的组织单位修复前保持 `remain_unclear`；
- AI119、AI121 属同一女性人权／军事性暴力框架，不重复计算桥接强度；
- AI126、AI127 限于 2018–2019 县民投票程序，并保留 A051 于 2019-03-26 解散的生命周期边界；
- AI129、AI132 只适用于各轮噪音诉讼；不得假定轮次成员相同，也不得把部分赔偿写成运行禁令或噪音停止。

本报告作为 10 条人工决定的回交记录；中央 edge 表、HR CSV、source log 与图表仍留待主线程统一合并。
