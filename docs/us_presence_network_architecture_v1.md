# 对美功能与多层关系网络研究架构 v1

日期：2026-08-19

状态：建议案；`research_only / not_frontend_ready / no_central_writeback`

上位规则：`data/metadata/coding_schema_v0.md`、`data/metadata/coding_schema_v1.md`、`docs/actor_relation_architecture_v1.md`

配套机读契约：`outputs/us_presence_network_architecture_v1/`

## 1. 这一轮要回答什么

客户提出的问题可以转成一个可检验的研究主轴：

> 围绕美国驻军及美日军事体系，冲绳的民间组织通过哪些行动、资源、人员、服务和制度渠道，限制、问责、缓冲、维持或正当化美国军事存在？这些功能之间通过谁的钱、谁的组织、谁的服务和哪些制度接口发生联系？

“帝国扩张”可以是论文的理论语言，但不是数据库对组织的标签。数据库只编码可观察的行动、关系、目标、中间产出和结果；“是否阻碍／帮助扩张”必须在有边界的比较分析中回答。

## 2. 现有数据为什么不能直接做社会网络分析

当前数据已经给出了很好的起点，但观察单位不同：

- 121 个有效 actor 和 283 条有效 actor–issue 边回答“哪些组织在公开材料中与哪些议题相连”，不是谁给谁钱、谁控制谁或谁与谁协调的关系网。
- `15_funding_or_support_edges_sample_v0.csv` 的 43 条是资助、服务、场所、结构、法律等异质观察，不是 43 条同质组织边。
- R8 的 27 条是 entity–case–role；同案不产生两两组织边。
- AEV 与 R6/R7/R11 保存事件参与和制度入口；共同署名和同场不产生稳定联盟边。
- H2 目前的“跨组关系观测为 0”来自多个目的性小样本；人员交叉、完整 recipient 网络和历史关系仍未对称测量。

因此下一轮不是把现有数据压成一张网，而是建立六个分层关系表，共用一套证据和人审包络，再在各自合法的观察单位上做网络分析。

## 3. 数据模型：先记录事实，后解释功能

```text
来源页／档案／财报／法院文书
  ↓ 定位到具体页面、条目或段落
类型化事实层
  ├─ money flow
  ├─ person–actor–time
  ├─ service–recipient
  ├─ affiliation / control
  └─ action–institution
  ↓ 人工复核指定字段
行动／关系级功能观察
  └─ constraint / accountability / mitigation /
     garrison_reproduction / community_mediation /
     legitimation / mixed / unknown
  ↓ 选择框、分母、时间窗口、缺失报告
分层网络结果与案例比较
  ↓ 负责人解释门
报告／论文／前端发布快照
```

四层不能相互代替：

1. **事实关系**：材料是否支持资金转移、职务、服务、隶属或制度行动。
2. **功能观察**：该具体行动或关系的明示目标和可观察作用是什么。
3. **分析结果**：在明确选择框和时间窗口内的分布、路径、中介或零观测。
4. **理论主张**：是否“阻碍扩张”、“降低驻军社会成本”或“生产合法性”。

## 4. 不对组织贴二元标签

新架构不在 actor registry 中新增 `pro_us`、`anti_us`、`helps_expansion`或 `blocks_expansion`。功能编码附着在带时间、对象和来源的具体观察上。同一组织在不同时期、项目或案件中可以出现多种功能。

| 功能码 | 编码对象 | 最低事实条件 | 不能自动推出 |
|---|---|---|---|
| `constraint` | 明示试图停止、延缓、禁止、撤回许可或限制建设／运行／部署的行动 | 行动目标和对象可核 | 行动已经成功，或已改变美军存在 |
| `accountability` | 调查、损害认定、赔偿、信息公开、评价、法律／行政审查或责任归属 | 制度角色或可核的问责行动 | 纠正、停工、政策改变或运行限制 |
| `mitigation` | 在不必然改变底层军事存在的前提下减少噪音、污染、健康、安全或生活损害 | 具体缓解措施或服务对象 | 支持或反对基地的立场 |
| `garrison_reproduction` | 维持军人、军属、基地社区或与驻军生活相连的服务、互助、筹资和分配能力 | 可核的服务／资源流和明确对象 | 亲基地立场、政治影响或合法性效果 |
| `community_mediation` | 资源、服务、转介或关系接口实际跨过基地／军属组织与冲绳地方社会的边界，进入福利、教育、儿童、医疗、社协或地方 NPO 等场域 | 跨界两端、方向和具体资源／服务／转介事实可核 | 地方政治接受、对基地的赞同、合法化、依赖、影响或持续关系 |
| `legitimation` | 组织或机构明示以信任、善意、理解、伙伴关系或可接受性为目标，或有第三方接受／效果证据 | 特殊高门槛，见下 | 从慈善或服务存在自动推出合法化 |
| `mixed` | 同一个不可再分的观察明确包含两种以上功能 | 必须列出 `component_function_codes` | 用 mixed 回避对事实的分解 |
| `unknown` | 观察在选择框内，但材料不足以分类 | 保留缺失范围 | 中立、无政治性、无效果 |

优先将一个复合行动拆成多条事实观察，分别编码。只有材料不允许拆分时才用 `mixed`。

`community_mediation` 和 `garrison_reproduction` 可以在同一 underlying fact 上分别成为两条功能观察，但不互相代替：前者的必要条件是可核的跨界接口，后者的必要条件是可核的驻军生活维持功能。一笔基地侧向地方福利机构的捐赠可以证明跨界资源接口，却不必然证明它维持了驻军生活；反之，一项只面向基地内军属的服务可以是 `garrison_reproduction`，却没有跨界，不是 `community_mediation`。

### 4.1 `legitimation` 的特殊证据梯度

| 层级 | 证据 | 允许的表述 |
|---|---|---|
| L0 | 捐赠、服务、合作或同场事实 | 只写资源转移或服务；不编码 `legitimation` |
| L1 | 行动方／美军／领馆明示使用“增进理解”“信任”“社区伙伴”“善意”等目标语言 | “关系建构／正当化的明示意图或公开叙事” |
| L2 | 受益方、地方机构或独立媒体对该叙事的接受、转述、抵制或重新解释 | “观察到接受／争议的公共反应” |
| L3 | 可重复的态度、信任、行为或制度效果材料 | 在明确设计和竞争解释下讨论“合法性效果” |

L1 不等于效果，官方宣传不是独立影响评估。没有 L2/L3 时，报告可以分析“合法化尝试／公开叙事”，不得写“已为美国军事存在提供合法性”。

## 5. 共用证据包络

全部新表继承 v1 的五轴分离：

```text
evidence_level
review_status
human_decision
claim_status
graph_eligibility / display_tier
```

每条记录还必须具有：

- 稳定记录 ID 和 `schema_version`；
- `selection_frame_id`，说明为何这条记录在样本中；
- 原始端点文本与解析后端点 ID，不丢失未解析名称；
- `source_ids` 及通过 `record_source_evidence` 定位的页码／条目／段落；
- `review_scope` 和 `reviewed_fields`，不因一行被人看过就批准整行；
- `confirmed_scope`、`missing_scope`、`interpretation_limit`；
- `period_start`、`period_end`、`time_precision`、`period_semantics`；
- `provenance_input_ids`，保留与中央表或既有研究包的对照；
- `package_scope=research_only`、`frontend_eligibility=not_frontend_ready`。

证据门与来源等级不等价。E4 官网可以证明组织自述，但不一定证明独立影响；第三方来源也不会因“独立”而自动强于官方财报或法院文书。证据门按字段和命题设置。

## 6. 拟议的表与关系 seam

详细字段、主键、证据门、图资格、时间语义和禁止推断见 `proposed_table_contracts_v1.csv`。

### USN00 `selection_frames`

记录每个分析的 actor universe、关系家族、年份、地点、来源范围、包含／排除规则和搜索完成度。没有这张表，不能把“未编码到”写成负面发现，也不能报告网络密度。

### USN01 `function_observations`

每行是一个已存在的行动、角色或关系的功能判断，必须通过 `underlying_record_type + underlying_record_id` 回到事实层。它是分析 overlay，不是 actor 属性，不自己产生组织边。

### USN02 `money_flows`

每行是一个日期／期间可核的资金转移或正式 award，结构为：

```text
provider → intermediary (optional) → recipient
+ amount + currency + year/period + purpose + flow_type + amount_semantics + source
```

NOFO、grant opportunity、sponsor tier、project cost、汇总多 recipient 金额不能伪装成直接付款。多步流用 `transaction_chain_id + flow_step_no` 保留，不从首尾自动生成穿透边。

### USN03 `person_actor_time`

每行是一个人在某一观测时点／期间与组织的公开职务或治理角色：

```text
person_research_id → actor_id → role → period → source
```

同名和近似名只保留候选 crosswalk；未经人审不分配共享 person ID。IRS 或年度报表只证明该年观察，不自动生成连续任期。只有人物身份、两端角色和时间重叠均已核时，才可生成 research-only 的人员二模图；现行 v1 中 `dyadic_relation` 只允许两端都是 registry actor，因此 person–actor 行在未批准新 schema/adapter 前使用 `administrative_record`，不进入现行组织关系图，也不自动投影组织联盟。

### USN04 `service_recipient`

每行是一次服务、实物、设备、奖学金、救济或转介的提供者–受益对象观察。受益方原文名称、法律实体解析和 registry crosswalk 必须分开。受益不等于政治赞同、联盟、依赖或合法化。

只有提供方与受益／接收方分属已声明的基地侧与地方社会侧，且方向、时间和跨界事实已核时，才可在 USN01 另建 `community_mediation` 功能观察。USN04 的 recipient 边本身不自动生成该功能码。

### USN05 `affiliation_control`

每行是一个带方向和角色的结构关系，例如 umbrella–member、national–regional branch、operator–facility、fiscal sponsor–sponsored project。`control` 只能在章程、法律文件或正式治理材料明示任命、所有、否决、预算或运营权时编码。成员、伙伴、参与、赞助或同场都不是控制。

### USN06 `action_institution`

每行是：

```text
actor/person → action/role → case/event/program/institution → target
+ entry_date + intermediate_output + substantive_change_status
```

它统一承接 R8 case role、AEV 事件角色和 R6/R7 入口，但不破坏各自语义。公投、诉讼、环评、请求、公共外交项目保持不同 `action_type`。同事件主体不两两相连，`non_party` 不生成关系边。

### USN07 `official_site_crosswalk`

为 NGO directory 提供 actor 到官方网站／正式组织页的统一入口。保留 URL、站点类型、官方性依据、语言、最后检查日期、归档状态和来源作用。上级组织介绍页、政府名录、法人登记和新闻报道不得统称“官网”。“有官网”也不等于组织更活跃或更有影响。

### USN08 `research_endpoint_crosswalk`

保存非 registry 端点：人物、政府机构、基地、案件、项目、受益方原文标签和 provisional organization。这张表是防止“为了画边就把对象当成 NGO”的类型安全层，不自动新增 actor。

### USN09 `record_source_evidence`

每行把一条事实／功能观察连到一个具体来源 locator，并说明它支持哪些字段。用它取代不可拆分的分号 `source_ids`。同一网站的多个页面不自动算独立二源。

## 7. 与现有数据的对接，不重写事实

| 现有层 | 新架构中的作用 | 强制边界 |
|---|---|---|
| 中央 43 条 funding/support/relation sample | 作为 USN02/04/05/06 的来源候选，按语义逐条映射 | 不批量改状态；不把 43 写成同质关系数 |
| `typed_relation_observations_v1` | 继承 v1 envelope 的派生参考 | 它不是新事实源；回到中央 row 和人审记录 |
| R8 27 case roles | USN06 的 case-role 子类 | 保留 case node、role 和 non-party；不两两投影 |
| 67 AEV／80 入口观察 | USN06 的 event/program 子类 | 事件参与不生成联盟 |
| R10 35 条目的性关系 | 行政／委托可进 USN02/06 | project cost、委托身份和实际付款分开 |
| H2 `public_person_roles_v1` | USN03 的 research-only seed pool | 同名候选未经人审，不生成 person node |
| H2 recipient rosters／Schedule I candidates | USN02/04 的 research-only seed pool | 原始申报、recipient 身份和金额语义未核前不升级 |

新波次的首次实作应该生成独立 package，不改中央 registry、actor–issue、actor–place、AEV、case-role、source log 或前端契约。只有人工任务逐字段决定后，才可另建受控 merger。

## 8. 图与社会网络分析资格

不建立一张把钱、人、服务、隶属和同案混在一起的网。允许的视图是：

1. **资金流图**：方向表示 provider 到 recipient；金额用文字，不用边宽；币种不自动汇总。
2. **人物–组织二模图**：必须使用时间窗口；没有时间重叠不投影为组织间接口。它是专用 research-only 分析图，不复用现行 `dyadic_relation` 组织边。
3. **服务–受益方图**：一次性、重复项目、汇总未知 recipient 分层；不写联盟。
4. **隶属／治理图**：成员、分支、运营和控制用不同边型；不用“关系强度”边宽。
5. **行动–制度图**：保留案件／事件／项目节点和角色；分开中间产出与底层军事项目改变。
6. **功能分布**：以已审观察条数和时间分布表示，分开驻军生活维持与基地—地方跨界中介，不把 actor 固定涂成“亲美／反美”。
7. **NGO directory**：以表格展示名称、类型、官方网站、已观察功能和证据入口；不是网络图。

任何中心性、密度或社群结果必须同时满足：

- 只使用一个明确关系家族或明示的多层模型；
- 固定 actor universe、时间窗口和包含／排除规则；
- 边的两端、方向、时间和关系语义可解析；
- 用已审事实计算，候选仅作单独敏感性上界；
- 报告未解析端点、缺年、来源家族和搜索覆盖；
- 做来源家族删除、未解析端点和时间窗口敏感性；
- 把结果写为“当前有界公开记录的结构”，不写影响力、控制力或总体社会结构。

在满足上述条件前，`network_metric_eligibility=not_eligible`。满足后也只先升为 `bounded_descriptive`，不自动成为因果结论。

## 9. 负面发现的证据门

“两组没有相交组织关系”只能在下列条件下写成限定负面发现：

1. 两组的入组规则、actor 列表、时间窗口和地点已冻结；
2. 对两组使用同等的关系家族和双向检索方法；
3. 官网、财报、法律、军方公共事务、地方日文资料等 source family 的覆盖已逐类报告；
4. 人物身份、recipient 和组织关系分别测量，不用一种零代替其他零；
5. 负检索日志保留 query、日期、语言、来源范围和结果；
6. 表述限定为“在该选择框、时间窗和公开材料中未编码到”。

不得用“现实中不存在”、“两个社会完全隔绝”或“没有共享人员”代替这个有界结果。

## 10. 人工决策与责任分工

AI 可以执行：指定材料抽取、原文保留、名称规范化候选、表间 crosswalk、缺失盘点、负检索日志、验证和图表生成。

负责人必须决定：

- actor universe 和比较时间窗口；
- 人物同一性与组织身份 crosswalk；
- 资金方向、金额语义、资助／赞助／委托类型；
- `control`、`community_mediation`、`legitimation`、`mixed` 和全部功能分类；
- 负面发现是否达到可报告门槛；
- 中心性和多层网络的分析资格；
- 从“功能观察”上升到“帝国扩张／合法性”的论文措辞。

这些决定必须进入独立 HR 任务书和回传表，不散落在 README 或 AI 报告中。

## 11. tracer-bullet 推进顺序

本轮不按“先搜完所有钱，再搜完所有人”的水平分工。每个切片都要纵向穿透：

```text
有界问题 → 选择框 → 来源 → 类型表 → 人审 → 验证 → 一个小型解释成果
```

具体切片、依赖、停止条件和验收见 `vertical_slice_register_v1.csv`。推荐顺序：

1. **US-VS00 NGO directory／官方站点**：直接回应客户“到底收了哪些 NGO”，同时冻结对美子样本。
2. **US-VS01 既有关系重断言**：将 43 条异质观察和相关 R8/R10 行对照到新契约，不新增事实。
3. **US-VS02 驻军社会维持个案**：在一个地点和时间窗口内同时交付 money、service、affiliation 和功能 overlay。
4. **US-VS03 对美问责个案**：以一个美方被告／目标明确的案件，区分限制目标、问责中间产出和底层项目改变。
5. **US-VS04 人物–组织时间网**：从少数高价值组织建立经人审的年度角色表，不用同名自动连线。
6. **US-VS05 受益方与社区中介接口**：追踪一个资源中介的 provider–intermediary–recipient 小网，区分一次性和年度重复，并只对跨过基地—地方社会边界的已核观察编码 `community_mediation`。
7. **US-VS06 合法化证据测试**：对一个慈善／公共外交个案同时采集行动方叙事和地方反应；没有 L2 就停在意图／公开叙事。
8. **US-VS07 两侧对称接口比较**：在同地、同期和同搜索强度下分别测量组织、人物和 recipient 接口。
9. **US-VS08 有界多层 SNA**：只在前述切片达到覆盖门后运行，不把 actor–issue 度数写成影响力。
10. **US-VS09 1972–2011 历史切片**：使用当地／馆藏材料检验当代结构能否外推到复归后长时段。

每个强解释切片后都暂停，由负责人决定继续、修订或停止；不再一次堆积多个模块后统一交付。

## 12. 建议的第一个人工检查点

在任何新事实采集前，负责人只需拍板五项：

1. 数据库统一使用“对美功能／美国军事存在”作为经验语言，“帝国扩张”只留在理论和论证层；
2. 功能编码只附着行动／关系，不写回 actor 固定属性；
3. `community_mediation` 必须确认跨界两端和方向；`legitimation` 使用 L0–L3 门槛，慈善、服务或跨界中介都不自动通过；
4. 第一批用 US-VS00／01 冻结目录和现有关系语义，再从 US-VS02／03 各做一个成对案例；
5. 本架构保持 research-only，不改中央事实表或前端；首个纵向切片验收后再决定 merger 和 publication adapter。

## 13. 本架构的验收条件

- 六类核心关系各有独立表契约，不共用无语义 `edge_type`；
- 每张表都规定主键、必填字段、证据门、图资格、时间语义和禁止推断；
- 功能观察不写回 actor 立场，`mixed`、`unknown` 和多功能拆分有明确规则；
- 资金、人物、recipient、control、community mediation、legitimation 和负面发现各有特殊门禁；
- 只有已核、时间有界、端点可解析的单层关系可进入描述性 SNA；
- 后续任务按 tracer-bullet 交付闭环，而不是只交 CSV 或只交结论；
- 本轮没有修改中央数据、已有前端或客户沟通稿。
