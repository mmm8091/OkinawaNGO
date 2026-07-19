# HR-019 actor–issue edge 范围第一组回交报告 Batch 11

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
来源队列：`outputs/R01_R02_actor_issue_v1/HR019/HR019_edge_scope_review_queue_v0.csv`  
状态：**已完成——10/10 条**

## 0. 批次边界

- 本批复核 HR-019 edge-scope 队列前 10 条。
- 允许决定：
  - `organizational_positioning`
  - `institutional_or_case_role`
  - `event_specific`
  - `remain_unclear`
- 本批只判断 actor–issue edge 的时间／机制范围，不新增 actor 间关系，也不把共同声明写成联盟。
- `organizational_positioning` 不表示无期限持续；正文仍须说明可证活动期。
- `institutional_or_case_role` 包括诉讼、直接请求、公投和其他多阶段正式程序，不等于单次事件。
- 若原 source ref 错位，本批可以记录修复建议，但不直接修改中央表或 source log。

## 1. 建议结论总表

| edge | actor–issue | 辅助建议 | 核心边界 |
|---|---|---|---|
| AI016 | A007 ピースボート—international_advocacy | `organizational_positioning` | 由长期 Okinawa project 的对美／跨国传播支持；S005 单次声明不足，须补官网项目页 |
| AI021 | A009 Earthjustice—international_advocacy | `institutional_or_case_role` | 严格限于冲绳儒艮案的美国法律渠道；Earthjustice 是律师，不是原告 |
| AI025 | A011 石垣市住民投票を求める会—referendum | `institutional_or_case_role` | 住民投票直接请求及后续程序的核心角色，不是无限期组织定位 |
| AI027 | A011—anti_military | `institutional_or_case_role` | 仅限该公投程序所针对的石垣陆自部署，不泛化为所有反军事议题 |
| AI040 | A017 沖縄対話プロジェクト—Taiwan_contingency | `organizational_positioning` | 台湾有事是其持续对话／前线化预防框架的一部分 |
| AI042 | A017—peace | `organizational_positioning` | 和平／冲突预防是组织目的；不表示活动已产生和平政策效果 |
| AI044 | A018 ノーモア沖縄戦 命どぅ宝の会—Taiwan_contingency | `organizational_positioning` | 组织成立以来的持续框架；S024 错位，须改用 S023＋组织官网 |
| AI048 | A020 JELF—legal | `institutional_or_case_role` | 冲绳议题中的法律角色须逐案确定，不由律师组织身份无限外推 |
| AI049 | A020—biodiversity | `event_specific` | 当前 S006/S007 只闭合 2020 MMC 儒艮请求／报告语境，不能支撑一般长期 biodiversity 定位 |
| AI050 | A020—dugong | `institutional_or_case_role` | 以冲绳儒艮案具名原告角色为主；2020 MMC 共同请求是另一个事件，不是联盟 |

建议分布：

- `organizational_positioning`：4 条；
- `institutional_or_case_role`：5 条；
- `event_specific`：1 条；
- `remain_unclear`：0 条。

## 2. AI016 · A007 ピースボート—international_advocacy

### 原证据问题

当前 source ref 只有 S005，即 2015 年边野古／珊瑚礁紧急声明。S005 可以证明一次公开倡议参与，但单独不足以把 `international_advocacy` 定为长期组织定位。

补查的 Peace Boat 官方 Okinawa project 页显示：

- 组织长期开展沖縄项目；
- 通过船上交流、日本本土传播及面向美国社会的行动处理冲绳和平／基地议题；
- 国际性不是只从组织名称或 NGO 身份推定，而有具体项目机制。

补充来源：

- `https://peaceboat.org/projects/okinawa.html`
- `https://peaceboat.org/about.html`

### 辅助建议

**AI016=`organizational_positioning`。**

安全范围：

> Peace Boat 的 `international_advocacy` edge 由其长期 Okinawa project 中的跨国交流、对美传播和日本本土外展支持，而非只由 2015 年共同声明支持。

限制：

- 合并时必须增加官方项目页 source ref；若只保留 S005，本 edge 应退回 `event_specific`；
- 不把共同声明者、乘船者或合作网络全部行为归给 A007；
- 不推断政策效果或稳定联盟。

建议 review notes：`long_term_okinawa_project_transnational_outreach;S005_alone_event_only`。

## 3. AI021 · A009 Earthjustice—international_advocacy

当前 S009 和 HR-014 已确认：

- Earthjustice 在冲绳儒艮案中是原告方律师组织；
- 不是具名组织原告；
- 它把冲绳儒艮／边野古争议带入美国联邦司法程序；
- 2020 年终局没有停止工程。

### 辅助建议

**AI021=`institutional_or_case_role`。**

安全范围：

> 此 edge 表示 Earthjustice 在冲绳儒艮案中提供的美国法律／跨境制度渠道，不表示其全部国际倡议或全部冲绳活动。

限制：

- 固定角色词 `counsel`；
- 不写成 plaintiff；
- 不由案件代理推断与各原告形成稳定联盟；
- 不从司法入口推断胜诉或项目改变。

建议 review notes：`okinawa_dugong_case_us_counsel_channel_only`。

## 4. AI025 · A011 石垣市住民投票を求める会—referendum

S018、S019 和 HR-014 已确认：

- A011 组织签名并提出条例制定直接请求；
- 石垣市议会处理／否决相关条例案；
- A011 是 requester／campaign body；
- 后续司法过程不使其自动成为具名组织原告。

这不是单日事件，也不是无期限一般定位，而是一个有开始、程序阶段和组织终点的住民投票过程。

### 辅助建议

**AI025=`institutional_or_case_role`。**

安全范围：

> `referendum` edge 限于石垣陆自部署住民投票的签名、直接请求、议会处理及可核后续程序。

限制：

- 不泛化为所有住民投票议题；
- 不推断代表全市多数意见、投票结果或政策因果；
- A011 的解散状态由生命周期表另审，不用来替代本 edge 的程序判断。

建议 review notes：`ishigaki_referendum_request_and_procedure_role`。

## 5. AI027 · A011—anti_military

`anti_military` 的依据不是一般反军队宣言，而是：

- 住民投票问题所针对的石垣岛陆上自卫队部署；
- A011 把该具体部署争议转入直接请求和地方制度程序。

### 辅助建议

**AI027=`institutional_or_case_role`。**

安全范围：

> 此 edge 只表示 A011 在石垣陆自部署住民投票过程中对该具体军事设施争议的介入。

限制：

- 不把 A011 写成涵盖所有基地、自卫队或安全政策的长期反军事组织；
- 不从 `anti_military` 标签推断其成员对所有军事议题立场一致；
- 与 AI025 属于同一程序链，不能计算成两个独立行动机制。

建议 review notes：`anti_military_limited_to_ishigaki_jsdf_referendum_object`。

## 6. AI040 · A017 沖縄対話プロジェクト—Taiwan_contingency

S022、组织规约和官网活动显示：

- 台湾有事不是一次被动参与的活动标签；
- 项目持续以对话方式讨论台湾／东亚紧张、冲绳成为战场或前线的风险；
- 该 edge 与 `frontline_prevention`、`peace` 高度重叠。

来源：

- `https://okinawataiwa.net/`
- `https://okinawataiwa.net/index.php/about-us/about_terms/`

### 辅助建议

**AI040=`organizational_positioning`。**

安全范围：

> `Taiwan_contingency` 是沖縄対話プロジェクト自成立以来公开对话和前线化预防框架的一部分。

限制：

- 只覆盖项目可证活动期，不追溯到组织成立前；
- 不把情景讨论写成战争必然发生；
- 不从对话参与推断参与者接受项目全部立场。

建议 review notes：`core_dialogue_frame_with_frontline_prevention_overlap`。

## 7. AI042 · A017—peace

组织规约把对话、避免冲突／战场化和和平讨论置于项目目的与活动方式中，因此 `peace` 不只是单次活动标签。

### 辅助建议

**AI042=`organizational_positioning`。**

安全范围：

> `peace` 表示项目持续采用对话和冲突预防框架，不表示已产生政策或安全环境效果。

限制：

- 与 AI040、`frontline_prevention` 是同一项目框架的不同分析层；
- 不按三个 issue 计算三倍桥接强度；
- 时间范围限于项目可证存在期。

建议 review notes：`core_dialogue_and_conflict_prevention_positioning`。

## 8. AI044 · A018 ノーモア沖縄戦 命どぅ宝の会—Taiwan_contingency

### 来源错位

当前 AI044 只引用 S024，但 S024 的 URL 是：

`https://okinawataiwa.net/`

它属于 A017 沖縄対話プロジェクト，不能支持 A018。

A018 的正确来源包括：

- S023：QAB 2022 年成立报道；
- `https://nomore-okinawasen.org/`：组织官网及持续声明／活动。

这些来源显示，台湾有事、冲绳／先岛前线化和“不要再次发生冲绳战”是组织成立以来持续框架，而非单次共同活动。

### 辅助建议

**AI044=`organizational_positioning`，但必须先修复 source ref。**

安全范围：

> `Taiwan_contingency` 是 A018 自 2022 年成立以来反战／前线化预防定位的一部分。

限制：

- 删除 AI044 对 S024 的依赖，改用 S023 和组织官网；
- 不把 A018 写成其所有共同声明者的 umbrella；
- 不从组织警告推断战争、撤离失败或攻击后果必然发生。

建议 review notes：`source_ref_repair_S024_to_S023_plus_official_site;core_positioning_since_2022`。

## 9. AI048 · A020 JELF—legal

S006／S007 主要记录 2020 年 MMC 请求／报告，不能单独精确说明 JELF 的法律角色。HR-014 已补足逐案角色：

- 冲绳儒艮案：JELF 是具名组织原告，不是律师；
- 泡濑案：JELF 仅为支持者／正式材料发布者，不是具名原告或律师。

### 辅助建议

**AI048=`institutional_or_case_role`。**

安全范围：

> JELF 的 `legal` edge 只按已确认的具体案件角色使用，并逐案区分 plaintiff 与 supporter/formal-material host。

限制：

- 不从“环境法律家联盟”名称推出其在每个案件中的角色；
- 不把儒艮案角色转移至泡濑案；
- 补入 HR-014 案件来源，S006／S007 不应独立承担 `legal` edge。

建议 review notes：`case_specific_legal_roles_HR014;not_generic_counsel_role`。

## 10. AI049 · A020—biodiversity

S006 的 2020 年 MMC 请求：

- 将冲绳儒艮描述为濒危亚种群／生态保护对象；
- JELF 列于 71 个共同请求组织中；
- 但该材料只证明一次共同请求／报告参与；
- S007 是叙事性学术材料，不能把一次参与升级为 JELF 对冲绳一般生物多样性的长期定位。

### 辅助建议

**AI049=`event_specific`。**

安全范围：

> JELF 的 `biodiversity` edge 目前限于 2020 年面向美国海洋哺乳动物委员会的冲绳儒艮请求／报告语境。

限制：

- 不把 71 团体共同请求写成联盟；
- 不从 JELF 全国性环境法工作自动生成长期 Okinawa biodiversity edge；
- 若后续获得 JELF 自有长期冲绳生物多样性项目材料，再单独重审。

建议 review notes：`2020_MMC_dugong_request_event_only;co_signing_not_alliance`。

## 11. AI050 · A020—dugong

这一 edge 有两层证据：

1. S006／S007：2020 年 MMC 儒艮共同请求／报告；
2. HR-014：JELF 在冲绳儒艮案中的具名组织原告角色。

第二层是持续多阶段法律程序，强于单次共同请求，因此 edge 不宜只标 `event_specific`，但也不能写成无限期一般定位。

### 辅助建议

**AI050=`institutional_or_case_role`。**

安全范围：

> JELF 的 `dugong` edge 以其冲绳儒艮案具名原告角色为主要制度依据；2020 年 MMC 请求只作为另一项具日期倡议事件。

限制：

- JELF 是原告，不是该案律师；
- 不从共同起诉或共同请求推断稳定联盟；
- 不把案件参与写成诉讼成功或工程停止；
- 正文分别标示 litigation role 与 2020 advocacy event，不把二者合并成一条无时间边界的连续行动。

建议 review notes：`dugong_case_plaintiff_role_primary;2020_MMC_request_separate_event`。

## 12. 本批数据修复项

若负责人确认：

1. AI016 增加 Peace Boat Okinawa project 官方页；S005 保留为 2015 事件证据。
2. AI021 继承 HR-014 的 `counsel` 角色和案件边界。
3. AI025、AI027 继承 HR-014 的 requester／campaign body 边界。
4. AI044 移除错误 S024 支持，改用 S023＋A018 官网。
5. AI048、AI050 增加 HR-014 案件来源；逐案固定 JELF 角色。
6. AI049 只保留为 2020 MMC event，不参与长期定位层。
7. 所有新增 URL 先进入 source proposal；source inclusion 不自动批准组织关系或政策效果。

本报告本身不修改中央 edge 表、source log、HR CSV 或图。

## 13. 负责人决定

负责人于 2026-07-20 确认本批全部辅助建议：

- AI016 A007 ピースボート—`international_advocacy`：`organizational_positioning`；
- AI021 A009 Earthjustice—`international_advocacy`：`institutional_or_case_role`；
- AI025 A011 石垣市住民投票を求める会—`referendum`：`institutional_or_case_role`；
- AI027 A011—`anti_military`：`institutional_or_case_role`；
- AI040 A017 沖縄対話プロジェクト—`Taiwan_contingency`：`organizational_positioning`；
- AI042 A017—`peace`：`organizational_positioning`；
- AI044 A018 ノーモア沖縄戦 命どぅ宝の会—`Taiwan_contingency`：`organizational_positioning`；
- AI048 A020 JELF—`legal`：`institutional_or_case_role`；
- AI049 A020—`biodiversity`：`event_specific`；
- AI050 A020—`dugong`：`institutional_or_case_role`。

负责人同时确认：

- AI016 必须补充 Peace Boat Okinawa project 官方页；S005 单独只支持 2015 年事件；
- AI021 固定 Earthjustice 的 `counsel` 角色，不写成原告或诉讼成功；
- AI025、AI027 均限于石垣陆自部署住民投票程序，不把 A011 泛化为所有反军事议题的长期组织；
- AI040、AI042 是同一对话／冲突预防框架的不同标签，不重复计算桥接强度；
- AI044 删除错误的 S024 支持，改用 S023 和 A018 组织官网；
- AI048、AI050 按 HR-014 的逐案 JELF 角色使用；
- AI049 只作为 2020 年 MMC 儒艮请求／报告事件，不升级为一般长期生物多样性定位；
- 共同声明、共同请求和共同诉讼不生成稳定联盟。

本报告作为 10 条人工决定的回交记录；中央 edge 表、HR CSV、source log 与图表仍留待主线程统一合并。
