# USN 第一轮受控集成：plan／沙箱检查点 v1

日期：2026-08-21

负责人授权：只允许生成合并计划和临时副本测试。

本轮未授权：中央表写回、43 行旧关系表扩写、publication adapter、前端发布。

## 结果

plan 已生成，真实状态为 `blocked_pending_source_freeze`。沙箱测试为
`PASS_SYNTHETIC_SANDBOX_ONLY`：它证明计划可重复生成、临时投影可二次零变化，
并且三处故障注入不会污染源仓；它不表示真实资料已经达到写回条件。

本轮固化了：

- 37 项预期动作与 18 项表变化；所有动作的 `write_eligible` 均为 `no`。
- 6 个拟新增 actor（X018–X023）及 2 个继续 defer 的组织线索；六个新增项均等待 source freeze。
- 43 条旧关系的一对一类型化 overlay：41 条 accept，F017／F043 两条 revise 为 `regional_branch`；中央 43 行保持原字节。
- 65 个官网决定：54 accept／4 revise／5 defer／2 reject；51 条来源已解析，14 条仍需新增或修订来源。
- 57 个当前机器提案 URL cluster：4 条复用 S054／S055／S076／S080，44 条非 ProPublica 新候选，9 条 ProPublica 接口等待 IRS 官方回执。没有分配任何最终 S-ID。
- LEG 语义迁移的 copy-transform：70 条 vocabulary、44 条 gate、10 条 slice、12 条 LC 和 10 条 table contract 保持原行数，只改 33 个获准字段单元；LC 仍是 LEG0=3、LEG1=9、LEG2=0、LEG3=0。
- 敏感事实的分表预览：RF002、RF001、两条 Earthjustice accounting 记录、6 条人物角色、4 条 off-graph action、2 条 MTS–AWWA 关系、6 条 sponsor snapshot、8 条 endpoint crosswalk。它们保留各自的来源、端点和 selection-frame 阻断，不被压成一张泛化关系网。

## plan 新发现的缺口

### 1. 57 个 URL cluster 不是最终 source delta

当前 union 只覆盖 38 条服务侧 proposal、7 条问责侧 proposal 和 13 条官网新来源需求。
RF002 的 IRS bulk XML、Treasury Judgment Fund 记录、FoE 2019、A070 的 2018／2025／2026
时点材料、NED 有界检索和若干 endpoint identity 尚未进入这个 union。plan 另列 8 项
`derived_source_requirements`，因此不能把“最多新增 53 个 source”写成最终新增量。

### 2. 三个分析层不能塞回冻结的 9／6／2 样本

官网目录需要 ACTIVE121 frame；吉川秀樹人物 tracer 涉及 A001／A002；MTS 与
Earthjustice 资源路径又含新 actor 和案件 accounting。三者都已列为 candidate frame，
但成员与分母尚未单独批准。旧 `USF-US-ORIGIN17-2026-08-19` 继续保持 9／6／2，
不得机械改成 15／6／2。

### 3. Sponsor snapshot 缺少合适的表缝

2026-08-19 页面可保留 6 条有日期、无金额的 tier observation。F002／F034／F035
只能复用，UMGC、AIG 与 Billabong 仍是 provisional endpoint。现有 money／affiliation
表都会诱导金额、控制或隶属含义，因此 plan 将它们留在
`hold_schema_sponsor_snapshot`，没有硬塞进现表。

### 4. 37-action 设计漏了 A070 的部分已批时点

负责人已经批准 A070 的离散时点与人物边界，但 37 项动作只覆盖部分角色修订，
未为 2018／2025／2026 的时点记录声明精确目标行。plan 将其列为
`hold_design_gap`，没有自行补中央生命周期或连续性。

## 关键语义保留

- RF002 是 X007 OESC → X004 AWWA、USD 8,479、2024-07-01—2025-06-30、
  `exact_reported`；真实写回仍等官方来源冻结。
- RF001 的 USD 2,580 继续 defer，不生成 money flow。
- Earthjustice 的 USD 276,345.50 是权责发生制申报中的 court-award accounting；
  USD 280,000 是 2021-03-05 Judgment Fund payment-mechanism record。两条不合并，
  也不生成简单 OSD → Earthjustice 资金边。
- USAPN006–011 的 `role_start` 全部留空，只保留 `role_observed_at`；吉川秀樹的
  A001／A002 双重角色不投影成组织关系。
- USAA005 的目标已从 A019 撤回，保留为
  `EO_R5_FUTAMI_TEN_DISTRICTS` event-only endpoint，继续 off-graph。
- MTS–AWWA 的 membership、selection/distribution channel 与年度金额是三种记录，
  不能合并成“合作关系”。

## 复现

```powershell
python scripts\plan_usn_wave1_integration_v1.py --verify-sandbox
python scripts\validate_us_presence_integration_plan_v1.py
python -m unittest tests.test_plan_usn_wave1_integration_v1
```

预期：14 项测试通过；validator 输出 `PASS_PLAN_PACKAGE_BLOCKED`；四个中央基线文件、
旧关系表、exploration publication 和前端均零变化。

## 下一道负责人门禁

当前不应批准 central apply。下一步应先完成 source cluster／官方 IRS receipt 冻结，
补齐 8 项派生来源需求，并分别决定三个 candidate selection frame 与 sponsor-snapshot
表契约。完成后重新生成 exact diff，再单独请求中央写回授权。

主交付：`outputs/us_presence_integration_plan_v1/`。

旧 `PASS_DESIGN_ONLY` 收据固定在 commit `6e7bd51`。它曾把 AGENTS、CONTEXT 和
workbench 一并纳入哈希；控制文档在本检查点后继续更新时，不应静默重算该历史收据。
当前状态以本 plan 的 parent-commit 引用和 `validate_us_presence_integration_plan_v1.py`
为准。
