# HR-033 legacy `verified` 关系状态归一化回交报告 Batch 30

日期：2026-07-20  
承办人：项目负责人  
辅助调查：Codex  
来源任务：`docs/human_review_task_HR033_legacy_relation_status_v1.md`  
本批范围：F006、F007、F021、F022、F023、F025，共 6 项  
状态：**负责人已确认——4 项 accept、2 项 revise**

## 0. 批次边界

- 本批是 HR-033 全批，不再拆分。
- 本批逐行核对关系存在、端点、角色方向、金额、时间和解释边界。
- `E4` 不自动等于人审通过；legacy `verified` 不自动映射为
  `human_checked`。
- AWWA 成员关系只表示伞状协调结构，不表示上下级控制、资助、政治联盟或共同立场。
- 服务于美军人员及家属的组织按公开功能编码，不据此推断亲基地或反基地立场。
- 本报告不修改中央关系表、actor registry、source log、HR CSV、图或前端数据，留待主线程统一合并。

## 1. 本轮实际调查结论

### 1.1 四条 AWWA 成员关系可接受，但不能继续写“五会总数”

当前 NOSCO 官方 AWWA 页面明确写：

- AWWA 由 NOSCO、KOSC、MOSC、OESC 等冲绳美军配偶俱乐部的代表组成；
- AWWA 为其 member clubs 提供协调和集中资源的机制；
- 各俱乐部代表按月开会讨论资金承诺。

NOSCO 当前 About Us 页面还直接称 NOSCO 是 AWWA 的 member。KOSC 当前政策页写明其慈善资金
通过 AWWA 分配；MOSCO 当前 About 页面写明其每月通过 AWWA 向冲绳的美国和日本组织捐赠。
2012 年 DVIDS 历史报道则明确列出当时五个配偶组织。

因此，F006、F007、F022、F023 四条具名关系都有足够支持。方向
`AWWA → member club` 可保留为结构编码方向：

- `source_role=umbrella_coordination_association`
- `target_role=member_club`

这个箭头只表示“伞状组织—成员”的角色朝向，不表示资金流、控制权或影响方向。

但当前 NOSCO 页面自身有文案残留：它一处写“四个具名俱乐部”，另一处写“五个组织”却仍只列出
四个名称。2012 年的第五个组织是 Army Community Group of Okinawa；其他材料显示该构成后来
发生过变化。因此，本批接受四条具名关系，不同时接受“当前固定由五个配偶会构成”这一总数命题。

### 1.2 F021 是直接慈善捐赠，不是 sponsorship

S053 明确记录：

- donor：Okinawa Enlisted Spouses Club；
- recipient：USO Okinawa；
- amount：USD 3,250；
- 捐赠事件日期：2025-12-02；
- 文章发布日期：2025-12-12；
- 款项用于 USO 在冲绳各地面向军人及家属的项目。

所以原记录的 `relation_type=donation`、方向和金额成立；但
`funding_relation_confidence=confirmed_sponsorship` 使用了错误语义，必须改为
`confirmed_donation`。事件日期和文章发布日期也应分列。

USO Okinawa 端点可由现有 S097 和当前 USO 官方页面独立解析；它是 USO 在冲绳的地区服务网络，
不是由这次捐赠事件临时构造的对象。

### 1.3 F025 应保留一条无金额的有界组织关系，并另存汇总金额观察

KOSC 官方慈善页面包含两个不同层次的命题：

1. “KOSC charitable funds are also distributed to AWWA”——明确支持
   `KOSC → AWWA` 的资金贡献关系；
2. “Last year, KOSC donated $102,000 to scholarships and AWWA”——只给出
   scholarships 与 AWWA 的合计 102,000 美元。

因此，若把 F025 整条改成 aggregate observation，会丢失网页明确给出的具名
`KOSC → AWWA` 关系；若把 102,000 美元写到该组织边上，又会虚构金额分配。

最稳妥的迁移是拆分两个观察：

- F025 保留为 `KOSC → AWWA` 的 `funding_contribution`，金额为空，
  `claim_status=supported_bounded`，`graph_eligibility=dyadic_relation`；
- 另建一条 `KOSC → scholarships + AWWA composite scope` 的
  `aggregate_observation`，记录合计 USD 102,000。

现有公开网页已经足以接受这个有界关系，不必让整条继续处于
`needs_local_retrieval`。年报／内部明细只影响具体年度和金额拆分，仍可作为非阻断后续任务。

## 2. 辅助建议总表

| relation_id | 辅助建议 | new_review_status | claim_status | graph_eligibility | 核心处理 |
|---|---|---|---|---|---|
| F006 | `accept` | `human_checked` | `supported` | `dyadic_relation` | AWWA 伞状协调组织 → NOSCO member club |
| F007 | `accept` | `human_checked` | `supported` | `dyadic_relation` | AWWA 伞状协调组织 → KOSC member club |
| F021 | `revise` | `human_revised` | `supported` | `dyadic_relation` | sponsorship 改 donation；分开事件日和发布日期 |
| F022 | `accept` | `human_checked` | `supported` | `dyadic_relation` | AWWA 伞状协调组织 → OESC member club |
| F023 | `accept` | `human_checked` | `supported` | `dyadic_relation` | AWWA 伞状协调组织 → MOSCO member club |
| F025 | `revise` | `human_revised` | `supported_bounded` | `dyadic_relation` | 关系保留但金额留空；102,000 美元另作 aggregate observation |

建议分布：

- `accept`：4 项；
- `revise`：2 项；
- `defer`／`reject`：0 项。

## 3. F006 · AWWA → NOSCO

### 调查结果

S055 是 NOSCO 当前官方页面。其 AWWA 页面把 NOSCO 列在构成 AWWA 的 chartered U.S.
Forces spouses clubs 中，并使用 `member clubs`；NOSCO About Us 页面又直接称 NOSCO 是
AWWA member。S072 提供 2012 年历史交叉支持。

### 辅助建议

**`accept` → `human_checked`。**

- `review_scope`：
  `endpoint_identity;relation_existence;direction;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;source_role;target_role;source_ids;evidence_level;date_or_period;interpretation_limit`
- `claim_status=supported`
- `confirmed_scope`：
  AWWA 是伞状协调组织，NOSCO 是其 member club；关系在 2012 年材料和当前 NOSCO 页面中均可见。
- `missing_scope`：
  本批不核正式章程条款、法律控制关系和精确生效／终止日期。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  结构箭头不表示控制、资助、政治联盟、共同政策立场或影响方向；不由本行接受“当前共有五个成员”。

## 4. F007 · AWWA → KOSC

### 调查结果

S055 当前页面把 KOSC 列为构成 AWWA 的俱乐部。S075 当前 KOSC 政策和慈善页面进一步写明，
KOSC 慈善资金通过／向 AWWA 分配。S072 提供 2012 年历史交叉支持。

### 辅助建议

**`accept` → `human_checked`。**

- `review_scope`：
  `endpoint_identity;relation_existence;direction;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;source_role;target_role;source_ids;evidence_level;date_or_period;interpretation_limit`
- `claim_status=supported`
- `confirmed_scope`：
  AWWA 是伞状协调组织，KOSC 是具名 member club／参与组织。
- `missing_scope`：
  本批不核正式章程、代表席位数量和精确成员期间。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  membership 本身不是 funding；KOSC→AWWA 的资金贡献另由 F025 编码；不表示政治联盟或控制。

## 5. F021 · OESC → USO Okinawa

### 调查结果

S053 对 donor、recipient、金额、事件日期和用途均有明确记载。文章署名／发布主体为 USO
Okinawa，S097 和当前 USO 官方地区页面可独立支持 recipient 端点。

原行唯一实质错误是把 donation 的 confidence 写成了 sponsorship；此外只写
`Dec 2025` 会混淆 12 月 2 日事件日和 12 月 12 日发布日期。

### 辅助建议

**`revise` → `human_revised`。**

- `review_scope`：
  `endpoint_identity;relation_existence;direction;amount;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;funding_relation_confidence;amount;currency;amount_semantics;event_date;publication_date;source_ids;evidence_level;interpretation_limit`
- `relation_type=donation`
- `funding_relation_confidence=confirmed_donation`
- `amount=3250`
- `currency=USD`
- `amount_semantics=direct_charitable_donation`
- `event_date=2025-12-02`
- `publication_date=2025-12-12`
- `claim_status=supported`
- `confirmed_scope`：
  OESC 于 2025-12-02 向 USO Okinawa 捐赠 3,250 美元，用于其冲绳服务项目。
- `missing_scope`：
  本批不核实际拨款到账日、会计科目或项目级使用明细。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  一次慈善捐赠不自动构成长期 sponsorship、稳定联盟、基地政策立场或政治影响关系。

## 6. F022 · AWWA → OESC

### 调查结果

S055 当前页面把 OESC 列为构成 AWWA 的俱乐部，并使用 member-club 语义。S041 提供旧社区材料
交叉支持；既有 HR-006 已分别确认 OESC 身份、AWWA membership 和 F008 为 F022 的重复项。

### 辅助建议

**`accept` → `human_checked`。**

- `review_scope`：
  `endpoint_identity;relation_existence;direction;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;source_role;target_role;duplicate_crosswalk;source_ids;evidence_level;date_or_period;interpretation_limit`
- `claim_status=supported`
- `confirmed_scope`：
  AWWA 是伞状协调组织，OESC 是具名 member club；F008 是本关系的重复行，不另生成边。
- `missing_scope`：
  本批不核正式章程和精确成员期间。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  membership 不是 funding；不得把 F008 恢复成第二条关系，也不推断政治联盟或共同政策立场。

## 7. F023 · AWWA → MOSCO

### 调查结果

S055 当前页面把 MOSC／MOSCO 列为构成 AWWA 的俱乐部。S079 当前 MOSCO 官方 About 页面称，
MOSCO 每月通过 AWWA 向冲绳的美国和日本组织捐赠，支持其持续的结构参与。

### 辅助建议

**`accept` → `human_checked`。**

- `review_scope`：
  `endpoint_identity;relation_existence;direction;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;source_role;target_role;actor_alias;source_ids;evidence_level;date_or_period;interpretation_limit`
- `claim_status=supported`
- `confirmed_scope`：
  AWWA 是伞状协调组织，MOSCO／MOSC 是具名 member club／参与组织。
- `missing_scope`：
  本批不核正式章程、代表席位和精确成员期间。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  MOSC 与 MOSCO 是同一组织的简称／表记，不新增 actor；membership 不等于资助、控制或政治联盟。

## 8. F025 · KOSC → AWWA／奖学金项目

### 调查结果

S075 同时直接支持：

- KOSC 的慈善资金向／通过 AWWA 分配；
- “上一年度”对 scholarships 与 AWWA 的合计捐赠为 102,000 美元。

它没有公开：

- 102,000 美元中分给 AWWA 的金额；
- scholarship 的具体 recipients 与金额；
- 网页所称 `last year` 对应的明确财年；
- 转款日期或完整年度明细。

### 辅助建议

**`revise` → `human_revised`。**

F025 关系行：

- `review_scope`：
  `endpoint_identity;relation_existence;direction;amount;time_period;interpretation_boundary`
- `reviewed_fields`：
  `source_actor_id;target_actor_id;relation_type;source_role;target_role;amount;currency;amount_semantics;date_or_period;source_ids;evidence_level;claim_status;graph_eligibility;interpretation_limit`
- `relation_type=funding_contribution`
- `amount=` 空值
- `currency=USD`
- `amount_semantics=named_contribution_amount_unknown`
- `claim_status=supported_bounded`
- `confirmed_scope`：
  KOSC 官方页面明确称 KOSC 慈善资金向／通过 AWWA 分配，因此
  `KOSC → AWWA` 的具名贡献关系成立。
- `missing_scope`：
  AWWA 分得金额、奖学金 recipients 与分项金额、`last year` 的明确财年、转款日期和完整年度明细。
- `graph_eligibility=dyadic_relation`
- `interpretation_limit`：
  关系图可显示 KOSC→AWWA 的“金额未公开”贡献边；不得把 102,000 美元附到这条边，
  不得把 scholarships 解释为单一 actor，也不由资金贡献推断政治联盟或控制。

另建汇总观察：

- `observation_kind=aggregate_observation`
- `source_endpoint=X006`
- `target_endpoint=P_R10_KOSC_MIXED_RECIPIENTS`
- `target_role=composite_recipient_scope`
- `relation_type=aggregate_financial_contribution`
- `amount=102000`
- `currency=USD`
- `amount_semantics=aggregate_mixed_recipient_no_allocation`
- `date_or_period=prior year stated on undated/current webpage`
- `claim_status=supported_bounded`
- `graph_eligibility=aggregate_observation`
- `confirmed_scope`：
  KOSC 页面报告上一年度向 scholarships 与 AWWA 合计捐赠 102,000 美元。
- `missing_scope`：
  明确财年、recipient 明细及两类对象之间的金额分配。
- `interpretation_limit`：
  合计金额不能拆给 AWWA、任何奖学金 recipient 或任何单一年度；该观察不上组织关系图。

此拆分吸收 `R10R029` 现有 aggregate proposal，但不删除原文能够支持的无金额
KOSC→AWWA 具名关系。

## 9. 来源

- S055，NOSCO 官方 AWWA 页面：  
  https://nosco.wildapricot.org/awwa
- NOSCO 官方 About Us 页面：  
  https://nosco.wildapricot.org/About-Us
- S072，DVIDS 2012 AWWA 历史报道：  
  https://www.dvidshub.net/news/87854/american-womens-welfare-association-celebrates-40-years
- S075，KOSC 官方 Charity 页面：  
  https://www.kadenaofficersspousesclub.com/charity
- KOSC 官方 Policy & Procedure 页面：  
  https://www.kadenaofficersspousesclub.com/policy-procedure
- S053，OESC 向 USO Okinawa 捐赠报道：  
  https://okinawa.stripes.com/community-news/okinawa-enlisted-spouses-club-uso-okinawa.html
- S079，MOSCO 官方页面：  
  https://www.moscoki.com/about
- S097／USO Okinawa 官方站点：  
  https://okinawa.uso.org/
- MCIPAC 当前 private-organization 清单，AWWA 状态为 ACTIVE：  
  https://www.okinawa.usmc-mccs.org/more/private-organizations

## 10. 建议负责人本批判断

建议一次确认：

1. F006：`accept` → `human_checked`；
2. F007：`accept` → `human_checked`；
3. F021：`revise` → `human_revised`；
4. F022：`accept` → `human_checked`；
5. F023：`accept` → `human_checked`；
6. F025：`revise` → `human_revised`，保留无金额的
   `KOSC → AWWA` 有界关系，并另建 102,000 美元 aggregate observation。

如负责人确认，HR-033 六项即全部完成。主线程合并时还应：

- 清除六行 legacy `verified`；
- 对四条 membership 写清 source／target roles；
- 不写“当前固定五会”；
- 将 F021 的 `confirmed_sponsorship` 改为 `confirmed_donation`；
- 分开 F021 事件日与发布日期；
- 清空 F025 dyadic relation 上的金额；
- 把 102,000 美元留在 composite-recipient aggregate observation；
- 不因本批接受服务／慈善关系而推断任何组织的基地政策立场。

## 11. 负责人确认

负责人于 2026-07-20 确认本批六项判断：

- `accept`：F006、F007、F022、F023，迁移为 `human_checked`；
- `revise`：F021、F025，迁移为 `human_revised`；
- `defer`／`reject`：0 项。

其中：

- F021 按直接慈善捐赠编码，使用 `confirmed_donation`，事件日为
  2025-12-02，发布日期为 2025-12-12；
- F025 保留金额为空的 KOSC→AWWA `supported_bounded`
  dyadic relation，102,000 美元另作 composite-recipient
  aggregate observation；
- 四条 membership 只表示伞状协调结构，不批准当前固定“五会”、资金、控制、政治联盟或共同立场。

本报告作为 HR-033 全部六项人工决定的回交记录。中央关系表、actor registry、source log、
HR CSV、图和前端数据仍留待主线程统一合并。
