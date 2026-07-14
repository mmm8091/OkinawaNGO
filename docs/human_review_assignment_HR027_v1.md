# HR-027 正式人工复核派工单：registry 价值门槛批

派工日期：2026-07-14  
派工人：主线程  
承办人：项目负责人（人工复核）  
状态：**已正式派出 / awaiting human return**  
批次：B01_REGISTRY_GATE  
优先级：**P0，当前第一优先**

## 1. 本批目标

对 4 个已经通过机器“四门”预筛的组织级候选，分别作出 `add`、`defer` 或 `reject` 的人工决定，并冻结组织单位、规范名、别名、分类、议题范围和禁止外推项。

本批不是“从 118 凑到 120”。即使最终不足两个 `add`，也必须按证据与模块价值决定；不能为了满足数量下限放宽组织身份或一期直接连接标准。

## 2. 权威输入

- 决定回填表：`outputs/registry_value_gate_v2/HR027_registry_value_review_v0.csv`
- 候选解释：`outputs/registry_value_gate_v2/registry_value_gate_brief_v2.md`
- 四门证据：`outputs/registry_value_gate_v2/four_gate_evidence_matrix_v2.csv`
- 来源与 locator：`outputs/registry_value_gate_v2/source_proposals_v2.csv`
- 近名／重复风险：`outputs/registry_value_gate_v2/alias_duplicate_crosswalk_v2.csv`
- 中央来源号映射：`outputs/registry_value_gate_v2/source_log_provenance_v2.csv`

机器预筛只说明“达到人工判断门槛”，不构成入表建议的最终批准。S248–S294 的来源索引状态也不批准 actor、edge、联盟、金额、因果或政策效果。

## 3. 允许的决定值

### `add`

只有在你确认以下四项都成立时使用：

1. 是可区分的组织单位，而不是活动名、一次署名、全国组织的模糊简称或既有 actor 的别名；
2. 有跨时点持续组织证据；
3. 有与一期问题的直接公开角色；
4. 能修复明确模块薄层，而非仅增加数量。

`add` 时必须同时决定：

- `canonical_name`
- 可接受 alias 及不可接受 alias
- `actor_class`
- `origin_type`
- `legal_status`
- `primary_places`
- 窄口径 `issue_tags`
- 证据等级
- 与近名／母体／既有 actor 的边界
- 可写角色与不可写结论

不要分配 A 号；主线程将在全批回收后按顺序分配。

本批 `issue_tags` 只能从当前 26 项 taxonomy 中选择。行政协作、采样、请愿、公害调停、港口、劳工、罢工等属于 function／action／venue／notes，不得临时塞入 issue tag。若你认为现有 taxonomy 确实缺项，请单列 `taxonomy_change_proposal` 及理由，主线程将送入重生后的 HR-029；本批不自动扩词。

### `defer`

当身份基本可信但仍缺一个会改变判断的关键证据时使用。必须写明：

- 缺什么；
- 线上继续查、当地查还是等待组织原件；
- 缺口关闭后重新进入哪一批；
- 当前不得进入哪些图、表和结论。

### `reject`

当候选属于重复单位、范围外一般公益、一期连接不足、组织级证据不足，或新增后没有独立分析价值时使用。必须写明拒绝原因，并说明是否保留为事件参与者、背景节点或线索。

## 4. 四个决定对象

### HR027-RV2C001　宮古島地下水研究会

机器排序：1  
中央来源：S158、S204、S269–S272  
近名检查：C015、A012、A097

待你决定：

1. 是否作为持续的宫古地下水研究／倡议 actor 入表；
2. `local_civic_research_and_advocacy_group` 是否为合适分类，或应改用现有受控词；
3. issue scope 是否限于 `groundwater;health_risk;life_safety;environment`；行政协作只能写 function／action／notes；
4. 2018 与 2020–2025 不同共同代表应如何写成时间化 leadership note；
5. 明确它与 C015、A012、A097 均不自动合并，也不自动建立隶属／联盟关系。

强制边界：组织提出“自卫队设施排水风险”和监管主张，可以编码为公开立场与行政接口；**不能写成已证实发生自卫队设施污染或健康损害**。

### HR027-RV2C002　宜野湾ちゅら水会

机器排序：2  
中央来源：S273–S279  
近名检查：简称「ちゅら水会」、A099

待你决定：

1. 是否作为宜野湾／普天间周边的地方 PFAS actor 入表；
2. 规范名是否固定为「宜野湾ちゅら水会」，「ちゅら水会」是否只作有地域语境的 alias；
3. 是否与 A099 保持独立组织单位；
4. issue scope 是否限于 `groundwater;health_risk;life_safety;environment;legal`；居民筹资采样、健康调查请求、议会请愿、公害调停分别写入 action／procedure／notes；
5. 是否接受 `local_civic_health_environment_group / informal_civic_group`，或映射到现有受控词。

强制边界：可以写采样、请求、请愿和程序使用；**不能据本批认定 PFAS 的健康因果、污染源归属、调查效果或与 A099 的稳定联盟**。

### HR027-RV2C004　全日本港湾労働組合沖縄地方本部

机器排序：3  
中央来源：S284–S289  
近名检查：「全港湾沖縄地方本部」「全港湾沖縄」及 A089–A093

待你决定：

1. 是否将地方本部作为独立 actor，而非只保留全国工会母体；
2. 规范名、两个简称 alias 和地方本部边界；
3. `labor_union_regional_branch / labor_union_regional_headquarters` 是否合适；
4. 2015 边野古／安保行动、2024 石垣港军舰寄港争议和 2025 和平行进能否支持 `anti_base;anti_military;peace;life_safety;mobilization` 的窄口径 issue scope；劳工、港口、职业安全和行动方式写 function／venue／action／notes；
5. 与 A089–A093 只作同层不同组织，不因共同活动建立联盟。

强制边界：可以记录行动存在与公开理由；**不能裁断罢工合法性、实际效果、政治影响或稳定联盟关系**。

### HR027-RV2C003　新日本婦人の会沖縄県本部

机器排序：4  
中央来源：S280、S254、S281–S283  
近名检查：「新婦人」、A049、A105、A107、A111

待你决定：

1. 是否把全国性组织的冲绳县本部作为持续的地方 actor 独立入表；
2. 规范名与 branch-level actor policy；
3. 模糊简称「新婦人」是否拒绝作为无条件 alias；
4. 2008、2014、2018、2024 的本地单位行动是否足以支撑 women／human_rights／peace／anti_base／referendum 的窄口径连接；
5. 与 A049、A107、A111 的功能重叠是否具有分析增量而不是重复。

强制边界：**不得把全国本部所有行动转嫁给冲绳县本部，也不得因党报报道推定政党隶属**。

## 5. 回交格式

可以直接编辑权威 CSV 的 `decision/reviewer/review_date/review_note`，也可以像 HR-011～015 一样在对话中按以下模板交回。若在对话中交回，主线程负责结构化写入。

```text
HR-027 人工复核记录
复核日期：YYYY-MM-DD

HR027-RV2C00X 候选名 —— add / defer / reject
- canonical_name：
- aliases：
- actor_class：
- origin_type：
- legal_status：
- primary_places：
- issue_tags：
- taxonomy_change_proposal（如无写“无”）：
- evidence_level_final：
- identity / continuity 判断：
- 一期直接连接：
- 模块增量：
- 与既有 actor／近名的边界：
- 可写结论：
- 禁止外推：
- review_note：

全批摘要：
- add：
- defer：
- reject：
- 是否有需要新建 alias／事件／关系候选：只列候选，不自动批准
```

## 6. 本批完成标准

- 四个对象 4/4 均有明确决定；
- 每个 `add` 都完成组织单位、alias、分类、议题与边界判断；
- 每个 `defer/reject` 都写清缺口或拒绝原因；
- 不以达到 120 为理由；
- 不生成未经审核的关系边；
- 不把风险主张写成科学因果，不把共同活动写成稳定联盟。

主线程收到后将：分配新 A 号、合并 registry/alias、只生成被本批明确允许的候选 issue/place/event 记录、重跑全库计数，并据新 actor 状态重生 HR-029。当前 HR-029 是 118-actor 旧快照，**在 HR-027 合并前不得执行**。

## 7. 并行输入请求（HD-012，不属于四项决定）

请同时把前期 **1990–2022 年冲绳县知事选举研究**的下列原始材料放入项目目录，或直接发给主线程：

- 研究正文 DOCX／PDF；
- 使用过的数据表、图表源文件与变量说明；
- 参考文献／来源表；
- 若有多个版本，请注明哪一版可作为一期衔接权威。

这不是 actor 审核项，也不阻塞 HR-027 回交；它决定一期论文能否实质完成原方案要求的“与前期选举研究衔接”。在收到原文前，主线程只允许写“组织进入选举公共接口”，不得推断组织机制与票数、胜负或政策结果之间的关系。
