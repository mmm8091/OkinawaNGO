# 模块完成包 v0

日期：2026-07-13（状态更新；模块产出仍为 v0）

编号说明：本包沿用早期内部编号。对最终 DOCX 方案验收时，Henoko/跨国路径归入 R6，coverage audit 归入基础建设；最终方案 R11 是外来 actor 进入生态，R14 是扩展模块“组织谱系”。本包不能替代 `docs/phase1_scheme_acceptance_audit_v1.md` 的 R1–R11 验收状态。

本目录把解释性图表包进一步整理成模块交付物。目标是让下一次沟通不只展示统计，而是展示可解释机制和下一轮调查路线。

## 覆盖模块

- R2 组织-议题网络：`R02_actor_issue_network_brief.md`
- R3/R4 地点-议题框架：`R03_R04_place_frame_brief.md`
- R5 共同行动事件样本：`R05_coaction_event_brief.md`
- R6 跨国 / 国际倡议路径：`R11_transnational_pathway_brief.md`（旧文件名）
- 基础建设覆盖与偏差审计：`R14_coverage_bias_audit_brief.md`（旧文件名）

## 总表

- `module_status_table_v0.csv`
- `next_module_investigation_tasks_v0.csv`

## 沟通建议

下一次沟通建议主用三张图：

1. `outputs/explanatory_v0/fig_place_issue_matrix_explanatory.png`
2. `outputs/explanatory_v0/fig_henoko_internationalization_pathway.png`
3. `outputs/explanatory_v0/fig_actor_issue_bridge_network.png`

补充图：

- `fig_coaction_sample_composition.png` 用来说明 R5 已有样本但不能写成稳定联盟。
- `fig_evidence_gap_map.png` 用来说明下一轮调查为什么会更明确。

## 下一步调查优先级

1. 处理 HR-010 的 47 条 post-HR-013 议题边补证项和 HR-024 的 8 条新复核项；54 条候选边在人工决定前不进入主 actor–issue 表。
2. C015 继续 defer；按模块缺层单列评估 `宮古島地下水研究会` 等持续组织，不能为越过 120 下限而恢复已拒或只作背景的对象。
3. 使用 `outputs/phase1_visuals_v1/`、`outputs/R08_legal_procedure_v1/` 和 `docs/phase1_research_report_v0.md` 完成跨图、图文和证据一致性审查。
4. 把已经字段级 `online_exhausted` 的缺口整理为当地协作者正式任务包。

## 当前数据快照

- Registry：118 actors；HR-013 新增 A111，同时按 HR-010 范围修正撤出 A094，净数不变。
- Source log：247 sources；224 archived、2 manual_archived、19 failed、2 non-URL。
- Actor–issue：222 edges；101 connected／17 isolated，59 human-reviewed／163 candidate；scope 为 43 positioning、40 case/institution、74 event、65 unclear。
- Actor–place：125 edges。
- AEV：65 rows，其中 61 human-checked、4 analytical seed。
- Human-review log：40 rows；HR-016–HR-024 的未决决定字段继续留空。

## 当前状态

- MT-001：HR-015 已将九个 E2、身份未确认的署名名称撤出 registry，保留为 R5 事件参与线索；Tier B 仅在独立本土声援层中条件纳入，Tier C 继续事件限定。
- MT-002：归档机制持续运行；当前 247 条来源为 224 archived、2 manual、19 failed、2 non-URL；失败状态保留供手工处理，不等于证据不存在。
- MT-003：25 条 `inferred_url` 已全部解决；S020 已恢复为 2016 年真实 URL。
- MT-004：线上 pass 完成，组织级身份仍需当地材料。
- MT-005：线上 pass 完成，已有命名 recipient 与 NOSCO 共同捐赠事件；完整年度表仍需 Form 990 / 内部年报。
- MT-006：ONC 公开年报金额和 JICA 受托角色已补齐，按行政协作层解释。
- MT-007：诉讼角色表完成，Turtle Island Restoration Network 已作为 A086 入 registry。
- MT-008：registry-only 事件感知侧表为 45 行、9 事件、5 动作类型；主 AEV 表现为 65 行（61 human-checked、4 analytical seed），并继续把九个 E2 event-only 名称与组织 registry 分开。
- REG-01：HR-013 已完成。C011 以 A111 入表；A094 按范围修正撤出；C010/C034 只作 background，C029-C033 rejected，C015 仍 defer。`okinawajosei.org` 属おきなわ女性財団，不能支持 A111 官网归属；A111 不接 `沖女連` alias。Registry 仍为 118；A087-A093、A095-A101 的分类／边复核继续由 HR-010 承接。
- EDGE-01：post-HR-013 在线激活包覆盖 17 个在表 actor，形成 54 条候选边和 38 条来源记录；HR-010 补证 47 项、HR-024 8 项，决定字段均为空。
- R1/R2：222 条 actor–issue edge 中 59 条 human-reviewed、163 条 candidate；101 个 actor 连入议题层，17 个仍 isolated。
- R8：六案与 27 个角色均已完成 HR-014；v1 比较包、两张解释图和报告插入已完成，13 个 registered-actor role 与 14 个 provisional node role 保持分离。
- GATE-01：9 个扩样候选的机器 gate 已被 HR-013 人工决定覆盖；gate 文件只保留为检索／提案轨迹，不再代表待定入表建议。
