# Phase 1 编码与展示状态规则 v1

日期：2026-07-20  
状态：负责人已批准  
继承：`data/metadata/coding_schema_v0.md` 的 actor、issue、place、evidence_level 与基础字段定义  
覆盖：v0 中关于 `review_status`、关系准入和前端展示资格的含糊部分

## 1. 核心原则

以下五个维度必须分开，不得由其中一个字段推断其余字段：

1. `evidence_level`：公开材料本身能提供多强的支持；
2. `review_status`：记录处于什么人工复核流程状态；
3. `human_decision`：负责人对本次复核作了什么决定；
4. `claim_status`：当前材料可以支持到多强的主张；
5. `graph_eligibility` / `display_tier`：该记录可在哪里、以什么身份展示。

固定解释：

> E4 不等于人审通过；人审通过不等于整行所有字段都成立；关系成立不等于可以画成
> 组织—组织边；可以画边不等于联盟、影响力或因果关系。

## 2. evidence_level

沿用 v0 的 E0–E4。它只评价材料支持强度，不记录谁看过，也不决定是否进入前端默认层。

## 3. review_status

合法值固定为：

| 值 | 含义 |
|---|---|
| `ai_seeded` | AI 收集或结构化，尚无负责人决定 |
| `human_checked` | 人工检查后原命题被接受 |
| `human_revised` | 人工检查后经修改才被接受 |
| `needs_second_source` | 关系、身份或关键字段仍需独立二源 |
| `needs_local_retrieval` | 线上已尽，关键字段需当地／馆藏／内部材料 |
| `rejected` | 命题被否决、误配或重复，不能进入展示层 |

`verified`、`human_verified`、`accepted` 等不得继续写入 `review_status`。旧值必须经过人工
crosswalk 后迁移，不能由构建脚本自动视为 `human_checked`。

## 4. human_decision

合法值：

- `accept`
- `revise`
- `defer`
- `reject`
- 空值：尚未形成负责人决定

`human_checked` 通常对应 `accept`；`human_revised` 对应 `revise`。流程状态和决定分列，是
为了保留“已看过但仍 defer”的情况。

每次人工决定同时记录：

- `review_task_id`
- `human_reviewer`
- `review_date`
- `review_scope`
- `reviewed_fields`

## 5. review_scope 与 reviewed_fields

`review_scope` 可多选：

- `source_accessibility`
- `source_metadata`
- `actor_identity`
- `endpoint_identity`
- `relation_existence`
- `direction`
- `amount`
- `time_period`
- `case_role`
- `event_participation`
- `interpretation_boundary`

`reviewed_fields` 写具体字段名。未列入 `reviewed_fields` 的字段不得因同一行被人审而自动
视为已确认。

## 6. claim_status

| 值 | 前端含义 |
|---|---|
| `supported` | 关系及当前展示所需主要字段已确认 |
| `supported_bounded` | 核心关系／观察已确认，但金额、期间、端点范围等字段不完整 |
| `candidate` | 有材料线索但尚无人审决定 |
| `lead` | 只确认检索机会、同场线索或未知 recipient；尚未形成关系命题 |
| `unsupported` | 材料不能支持当前命题 |

### 6.1 `lead_only` 不属于 claim_status

`lead_only` 是研究工作包《意外发现登记》使用的包内 workflow state，不是本节合法的
`claim_status`，也不是第 3 节的 `review_status`。它位于 `lead` 之前：只表示执行中遇到一条
值得保留并可作有限侦察的线索，尚未形成关系或解释命题。

`lead_only` 不进入中央表、人工复核任务、研究视图或 publication snapshot。若以后要升级为
`claim_status=lead`、`candidate` 或其他研究观察，必须另开问题与选择框，重新经过现行证据、
复核和展示门禁。具体登记与三步／十条边界见 `docs/research_work_package_protocol_v1.md`。

`supported_bounded` 必须同时提供：

- `confirmed_scope`
- `missing_scope`
- `interpretation_limit`

前端不得只写笼统的“证据不足”，必须说明具体缺什么。

## 7. graph_eligibility

| 值 | 可视化语义 |
|---|---|
| `dyadic_relation` | 两端均为已解析 actor，可进入组织关系面板／关系图 |
| `case_role` | actor／person／institution—case—role，只进入案件结构 |
| `event_participation` | 事件级参与，不生成稳定组织关系边 |
| `administrative_record` | actor—program／place／institution 记录，不进入组织关系图 |
| `aggregate_observation` | 汇总范围或未知 recipient，只作记录 |
| `research_lead` | NOFO、co-presence、未知对象等检索线索 |
| `genealogy_anchor` | 形成、改名、分裂、合并或连续性锚点 |
| `excluded` | rejected、duplicate 或不支持命题 |

只有 `dyadic_relation` 可以进入组织—组织关系图。`case_role` 必须保留案件节点与角色；
`non_party` 永不派生关系边。

## 8. display_tier

内部数据与前端用户文案分开：

| 内部值 | 用户界面 | 准入 |
|---|---|---|
| `reviewed` | 已核视图 | `supported` 与 `supported_bounded` |
| `research` | 研究视图 | 已核视图内容，加 `candidate` 与 `lead` |
| `hidden` | 不展示 | `unsupported`、`rejected`、`excluded` |

原数据目录名 `demo/` 可为兼容性暂时保留，但用户界面统一显示“已核视图”，不再显示
“演示视图”。

`display_tier` 由构建模块根据本规则派生，不由前端或中央表作者手填。

## 9. 关系展示字段

进入前端的关系／观察至少包含：

```text
id
observation_kind
relation_family
relation_type
source_endpoint
target_endpoint
source_role
target_role
scope_kind
scope_id
evidence_level
review_status
human_decision
review_scope
reviewed_fields
claim_status
confirmed_scope
missing_scope
graph_eligibility
display_tier
source_ids
interpretation_limit
amount
amount_semantics
date_or_period
```

金额未知时保持空，不能用 0。project cost、sponsor tier、aggregate amount、in-kind value 与
direct payment 必须通过 `amount_semantics` 区分。

`funding_relation_confidence` 只描述资金语义，当前准用值至少包括：

- `confirmed_donation`：材料确认一次直接捐赠；
- `confirmed_contribution`：材料确认资金贡献关系，但金额或期间可仍不完整；
- `confirmed_grant`／`confirmed_commission`／`confirmed_sponsorship`：仅在材料明确使用相应机制时使用；
- `not_funding_relation`：结构、成员或协调关系，不是资金关系；
- `no_public_evidence`：只存在机会或检索线索，尚无 award／recipient 事实。

`confirmed_contribution` 不表示金额完整；金额、期间和 recipient 缺口仍由 `claim_status`、
`missing_scope` 与 `amount_semantics` 共同表达。不得把 donation 写成 sponsorship，也不得把
membership 仅因有资金讨论背景改写为 funding。

## 10. 前端视觉规则

- 关系家族使用颜色；
- 方向使用箭头；
- 已核记录使用实线；
- 候选记录使用虚线；
- 证据等级使用 E4／E3／E2 标签，不使用边粗细；
- 缺失字段使用明确文字，如“金额未公开”“期间待核”；
- 不仅依靠颜色表达状态；
- 不以节点面积、度数、边宽或透明度表达影响力、关系强度或资金规模。

法律案件使用案件节点和角色标签，不用虚线表示“法律”；虚线保留给候选状态。

## 11. 计数规则

禁止笼统报告“关系共 N 条”。至少分为：

- 已确认组织关系；
- 有限确认记录；
- 待审候选；
- 研究线索；
- 隔离／排除。

actor—place、actor—program、aggregate observation、case role 不得计入“组织—组织关系”。

## 12. legacy `verified` 迁移

`data/interim/15_funding_or_support_edges_sample_v0.csv` 中六条 `verified` 进入 HR-033：

- F006
- F007
- F021
- F022
- F023
- F025

迁移只能由人工决定产生：

- 接受原命题 → `human_checked`
- 修改边界后接受 → `human_revised`
- 关键关系仍缺证 → `needs_second_source`／`needs_local_retrieval`
- 否决 → `rejected`

HR-033 已于 2026-07-20 完成并合并：

- F006／F007／F022／F023 → `human_checked`；
- F021／F025 → `human_revised`；
- 六行 legacy `verified` 已清零；
- F025 保留无金额的 `KOSC → AWWA` 有界关系，102,000 美元仅保存在
  `R10R029` composite-recipient aggregate observation。

合并脚本与前端输入快照见 `scripts/merge_hr033.py` 和
`outputs/hr033_integration_v1/`。

## 13. 构建验证门禁

构建模块必须拒绝或隔离：

- 非法 `review_status`；
- `dyadic_relation` 的任一端无法解析到 registry actor；
- `lead` 进入关系图；
- `non_party` 派生关系边；
- event co-participation 自动生成组织边；
- `supported_bounded` 缺少 `missing_scope` 或 `interpretation_limit`；
- `rejected`／E0 进入已核或研究可见层；
- 前端自行根据 `review_status` 重算展示资格。

## 14. actor–issue 的三重门禁与 legacy 过渡

actor–issue 记录必须区分：

1. **事实门**：现有来源是否足以支持确切 actor—issue 映射；
2. **范围门**：该映射只可解释为长期定位、案件／制度角色，还是事件标签；
3. **字段冻结门**：`reviewed_fields`、`claim_status`、`confirmed_scope` 等 v1 字段是否完整。

HR-019 的 `scope_review_status` 只通过范围门，绝不自动通过事实门。`scope_claim_status` 也只
说明批准了有界解释范围，不能替代主记录的 `claim_status`。

构建端可派生以下展示辅助字段；它们不写回中央表：

- `fact_gate_status`
- `scope_gate_status`
- `schema_freeze_status`

现有旧批次中，部分 `human_checked`／`human_revised` actor–issue 行尚缺 v1 字段。完成
HR-035 等人工 crosswalk 前，可以为保持历史交付兼容而暂时留在已核层，但必须显示
`legacy_field_freeze_pending`／“人工接受·字段待冻结”，不得静默补成 `supported`。全部旧行
迁移完成后，应撤销这项兼容规则，严格按第 8 节的 `claim_status` 准入。

前端不得把：

- “范围已审”写成“事实已核”；
- “人工接受·字段待冻结”写成“字段完整”；
- `needs_second_source`／`needs_local_retrieval` 隐藏成普通候选；
- registry `issue_tags` 直接投影成 actor–issue 边。
