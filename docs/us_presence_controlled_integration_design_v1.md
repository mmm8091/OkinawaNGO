# 美国军事存在多层网络：受控集成设计 v1

日期：2026-08-21

状态：设计完成，等待负责人批准实际写入

范围：承接 USN wave 1 的四份正式回传与五项架构决定

## 1. 结论

本轮不能把新材料继续塞进 `15_funding_or_support_edges_sample_v0.csv`。那张表混有资金、服务、隶属、案件行动、据点和线索，继续扩写会把不同证据门槛重新混在一起。

安全的中央接口是：

```text
actor / source 主表（只做窄写回）
        │
        ├── 旧 43 条事实行（保持原样）── relation_retype_overlay
        │
        └── data/interim/usn_v1/ 类型化事实层
              ├── money / accounting
              ├── person–actor–time
              ├── service–recipient
              ├── affiliation / control
              ├── action–institution
              ├── official-site / research-endpoint
              └── function / LEG0–LEG3
```

旧关系由 overlay 映射到新关系族，不复制事实、不升级状态。新关系进入独立类型化表。前端仍从 publication adapter 读取；本设计不授权 adapter 或前端发布。

## 2. 本设计锁定的基线

| 中央文件 | 当前行数 | SHA-256 | 本次设计阶段 |
|---|---:|---|---|
| actor registry | 122 | `c77dbc62e2a1019269a9a5ef5d64d1ac14f4cd54e4abf4b45953e33a67c22df4` | 不写 |
| actor aliases | 39 | `e1e8160d33aa975d6374ba38f8490e182b832a96b7bbed285cd94d29b522b52d` | 不写 |
| source log | 295 | `363f21256d074cc9577752728b1f950c5c899991fefeea633e86fb78c2aaf902` | 不写 |
| legacy relation sample | 43 | `3b11795150e7630ccf4cdab371ac135fab019c260609ee1272df518638f3ef23` | 永久保持事实行不变 |

实际 merger 必须先复核这四个哈希。任一漂移即停止，重新生成 expected diff，不能在新基线上盲写。

## 3. 深模块边界

建议未来获准后建立 `data/interim/usn_v1/`，由单一集成模块管理：

| 表 | 粒度 | 关键边界 |
|---|---|---|
| `selection_frames_v1.csv` | 一套版本化比较分母 | 旧 9／6／2 框永久冻结，不因新增 actor 追溯改写 |
| `actor_admission_overlay_v1.csv` | 一项 actor 准入决定 | admission 与关系、立场、资金分开 |
| `function_observations_v1.csv` | 一项有日期的功能判断 | 功能属于行动／关系，不属于 actor 永久属性 |
| `money_flows_v1.csv` | 一次转移或交易链的一步 | provider、recipient、金额、期间和 amount semantics 分列 |
| `resource_accounting_observations_v1.csv` | 一条会计／裁判／付款机制记录 | 不把 accrued award 硬写成 directed cash flow |
| `person_actor_time_v1.csv` | 一个人在一组织的一项有期职务 | `role_observed_at` 不自动变成任期起点 |
| `service_recipient_v1.csv` | 一项服务／实物／受益对象观察 | 现金、实物估值、汇总受益类和具名 recipient 分开 |
| `affiliation_control_v1.csv` | 一项成员、分支、伞状或控制关系 | membership／regional branch 不等于 governance control |
| `action_institution_v1.csv` | 一项行动进入案件、机关、项目、地点或事件 | event-only endpoint 不进入组织主图 |
| `official_site_crosswalk_v1.csv` | 一 actor 对一查证入口 | 官网决定不批准立场、关系或持续性 |
| `research_endpoint_crosswalk_v1.csv` | 一项非 registry 端点解析 | 保留 person、case、program、recipient、aggregate 和 raw label |
| `record_source_evidence_v1.csv` | 一条记录对一 source locator | 事实证据与解释证据分开 |
| `relation_retype_overlay_v1.csv` | 一条旧事实行的语义归位 | F-ID 不变；overlay 不升级原事实状态 |
| `source_capture_overlay_v1.csv` | 同一 URL 的一次日期化抓取 | 新抓取不得覆盖旧归档 bytes／hash |

`resource_accounting_observations` 和 `source_capture_overlay` 是 wave 1 暴露出的两个必要新增 seam：前者容纳 Earthjustice 的会计申报金额和 Judgment Fund 付款机制，后者保存同一 URL 的不同时间快照。

## 4. 已批准、但尚未授权写入的最小变化

### 4.1 Actor

若实际写入时 actor registry 仍以 X017 为最大 X-ID，预留：

| 预留 ID | actor | 准入边界 |
|---|---|---|
| X018 | Marine Thrift Shop Okinawa | 基地社区服务背景 actor；不随身份准入关系或立场 |
| X019 | Marine Gift Shop | 当前联邦免税状态 unresolved；不推历史隶属 |
| X020 | Neighborhood Pantry – Camp Butler | 独立服务 actor；法人／税务状态 unknown |
| X021 | North Island Okinawa Spouses Club | `base_spouse_club`；历史法律名只作 alias |
| X022 | Army Emergency Relief | 建全国 actor；Torii 只作 local presence |
| X023 | Air & Space Forces Aid Society | 建全国 actor；Kadena 只作 local presence |

X017 ACGO 只新增“FY2018 最后观察、当前状态未知”的 lifecycle overlay；不写解散日，不认 successor。SA016／SA017 继续 defer，不生成 actor。

新 actor 不加入 `USF-US-ORIGIN17-2026-08-19`。若需要比较扩展后的服务侧，另建 successor selection frame，由负责人重新批准分母。

### 4.2 旧 43 条关系

中央 43 行保持 byte-identical。只在 `relation_retype_overlay` 中展开负责人已批的 6 条规则：

- 43 个 F-ID 一一覆盖；
- F017、F043 的 overlay `proposed_record_family` 改为 `regional_branch`；
- 其余 41 行 proposal 不变；
- 所有原 endpoint、review status、claim status、amount 与 graph eligibility 原样继承。

### 4.3 新事实

- 接受一条 X007 OESC → X004 AWWA、USD 8,479、2024-07-01—2025-06-30 的有期 grant flow。
- KOSC → AWWA USD 2,580 继续 defer，不生成 flow。
- MTS—AWWA 至少拆为 membership、grant-selection/distribution channel、年度 flow 三种记录；本轮只有前两种结构／渠道决定获批，不能压成泛化合作。
- Earthjustice USD 276,345.50 记为申报期内 court-award accounting observation；Treasury USD 280,000 记为另一条付款机制观察。两数不合并，不生成 OSD → Earthjustice 简单资金边。
- Hideki Yoshikawa 的 OEJP／SDCC 同日职务生成两条 person-role observation；不生成 A001 ↔ A002 组织边。
- USAA005 撤销 A019 端点，改为 `EO_R5_FUTAMI_TEN_DISTRICTS` 或来源 raw label，继续 off-graph。
- AER／AFAS 的 Torii／Kadena 记录为 national actor local presence，不另造地方 actor。
- 2026-08-19 USO sponsor roster 是定点快照；tier 不换算金额，不补开始日。
- 三个 recipient identity crosswalk 可接受；identity 决定不连带批准资金、服务或 partnership。

## 5. Source 准入

现有正式 proposal 有 service 38 行、accountability 7 行，另有 actor-directory 58 个 accept／revise 页面。它们存在交叠，不能直接顺序编号。

当前只锁定流程：

1. 规范化 URL，按 source owner、document date、record type 和 locator 去重；
2. 先复用中央现有 source；
3. ProPublica 展示页优先补／换成 IRS TEOS 或官方 XML receipt；
4. 新 source 默认 `ai_seeded` 且 `relation_or_claim_approved=no`；
5. 完成 URL freeze 后才分配连续 S-ID；
6. source-log merge 后另跑 archive，不由 merger 同时抓取；
7. S097 的新页面观察进入 `source_capture_overlay`，不得覆盖既有归档 bytes。

去重预审得到 58 个候选引用、57 个规范化 URL，其中 4 个与中央 source 精确复用，53 个为新增候选上界；其中 9 个是 ProPublica 接口，必须先补官方 IRS receipt。`53` 不是获准新增数。

## 6. LEG 迁移

批准后的语义为：

- LEG0：服务、转移、事件或关系事实；
- LEG1：行动方／官方的 goodwill、trust、friendship、partnership 等自我叙述；
- LEG2：recipient、地方机构或独立来源的有界接受、转述、抵制或重释；
- LEG3：有重复、比较或明确设计的态度、行为、制度效果。

不能全仓字符串替换。架构契约中的旧 L1／L2／L3 可机械迁移；旧 gap 文案里的 “L2 actual effect” 实际应迁到 LEG3。迁移后必须保持 70 条词表、44 条门禁、10 个切片、12 条 LC 观察（LEG0=3／LEG1=9）以及非目标字段零漂移。

## 7. Merger 接口

未来获准后只暴露两个接口：

```text
plan_usn_wave1_integration(root) -> frozen_expected_diff
apply_usn_wave1_integration(root, frozen_expected_diff, approval_receipt)
```

执行顺序：校验权威回传与中央哈希 → 生成只读 diff → 在临时副本应用 → 跑全门禁 → 原子替换批准文件 → 第二次执行应零新增且字节不变 → source archive 单独运行。

任何失败都不得留下半写中央文件。

## 8. 前端门禁

本轮不接前端。原因不是“资料不够”，而是 publication catalog 尚无 USN surface，且不同观察必须先有各自 adapter：

- person bridge 不生成组织边；
- accounting observation 不进入 money graph；
- service episode 和 event role 不进入 dyadic graph；
- LEG1 只能显示“组织如何表述”，不能显示“已产生合法化效果”；
- frozen frame 与 successor frame 必须分别计数。

中央集成完成并再次批准后，先做三个小型公开表面：可核组织名录、分层资源网、人物—职务—时间 tracer。不要先做一张全量毛线球。

## 9. 验收与停止条件

详细门禁见 `outputs/us_presence_controlled_integration_design_v1/test_matrix_v1.csv`。最关键的停止条件是：

- 基线哈希漂移；
- 预留 X-ID 已被占用；
- source URL 尚未冻结却开始分配 S-ID；
- defer／reject／event-only 端点被升格；
- 43 行旧关系发生任何事实字段变化；
- 资金机会、project cost、sponsor tier、汇总金额或实物估值被写成直接付款；
- failure injection 后中央文件发生变化。

## 10. 下一次负责人检查点

负责人只需决定三件事：

1. 是否批准上述 seam 与 `data/interim/usn_v1/` 表组；
2. 是否批准生成 merger 的 `plan` 模式和临时副本测试；
3. plan 输出逐字段 diff 后，是否另行授权 `apply`。

第 1／2 项的批准仍不等于第 3 项。
