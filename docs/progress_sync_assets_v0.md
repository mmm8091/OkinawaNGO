# 进度沟通素材包 v0

日期：2026-06-17（v1 更新：2026-07-01）

## 1. 沟通稿主口径

本阶段不是直接做结论，而是先把一期研究的问题、资料边界和可复核数据底座搭起来。

建议主线：

> 本周已根据研究目标调整一期方案：在冲绳本土 NGO / 市民团体之外，新增外来 NGO、军属服务组织、公共外交项目和资助 / 委托关系作为观察层。当前已建立 actor registry、source log、issue taxonomy、place registry、组织-议题关系、组织-地点关系和 support/funding sample 表，为后续报告和论文提供可复核的数据底座。

## 2. 本次可以写入的进展

- 已将一期主问题收束为：冲绳民间组织 / NGO 如何把基地问题转译为环保、生活安全、地方自治、人权、法律程序和国际倡议等议题。
- 已明确一期不做复归以来全量 NGO 网络，而是先做可复核的分类底库与重点议题网络原型。
- 已将 actor universe 扩展到外来 NGO、军属服务组织、公共外交项目、资助 / 委托机构。
- 已建立 93 条 actor 初版样本。
- 已建立 92 条 source log 初版。
- 已建立 180 条 actor-issue 候选边。
- 已建立 124 条 actor-place 候选边。
- 已建立 27 条 support/funding sample edge。
- 已建立人工复核、当地材料收集和人类决策三个任务书。

## 3. 可截图图表

输出目录：`outputs/progress_sync_v0/`

- `fig_actor_class_counts.png`：actor 类型构成。
- `fig_actor_origin_counts.png`：actor 来源 / origin 构成。
- `fig_issue_edge_counts.png`：初版组织-议题关系中出现最多的议题。
- `fig_place_edge_counts.png`：初版组织-地点关系中出现最多的地点 / 场域。
- `fig_place_issue_matrix.png`：地点-议题矩阵。
- `fig_actor_evidence_counts.png`：actor 证据等级分布。
- `fig_support_relation_types.png`：support/funding 样本关系类型。

## 4. 可截图表格

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`

## 5. 当地协作口径

第一次沟通稿只大概说明后续可能需要当地协作者帮助收集材料，不正式派任务。

建议写法：

> 后续如果进入更深入阶段，部分材料可能需要当地协作者协助收集，包括：冲绳本地 NPO 的事業報告書和财务资料、与那国 / 先岛相关地方报道与议会资料、军属服务和军属配偶慈善组织的活动手册与 recipient 记录、外务省 / JICA / ONC 项目资料等。下一周将整理一份更具体的当地查资料任务表，再决定是否正式派给当地协作者。

## 6. 不建议第一次展开的内容

- 不展开具体资金链。
- 不把 NED / USAID 写成已确认资助冲绳本地组织。
- 不把共同署名写成稳定联盟。
- 不把服务型 NGO 写成反基地或亲基地。
- 不把与那国写成环保拒止主案例。

## 7. 可写的证据分级说明

建议简写：

> 对资助、委托、赞助和项目合作关系，本项目采用证据分级。只有官方记录、组织财报、项目报告、grant / award / contract 等能够支持的关系，才会进入结论；新闻、活动页、社媒或二手资料仅作为待核查线索。

## 8. 下一周建议写法

> 下一步将继续补充 actor registry，并对初版组织-议题、组织-地点关系进行人工复核；同时整理当地资料收集任务表，为后续可能需要当地协作者查询的材料做好准备。

## 9. v1 更新（2026-07-01）

数据扩充后新增图表输出目录：`outputs/progress_sync_v1/`

新增图表（生成于 HR-001 回填前，图中 n 仍对应当时数据快照）：

- `fig_actor_origin_counts.png`：actor 来源分布（n=90）。
- `fig_actor_class_counts.png`：actor 类型分布（n=90）。
- `fig_actor_evidence_counts.png`：actor 证据等级分布。
- `fig_issue_edge_counts.png`：议题 edge 排名（n=178）。
- `fig_place_edge_counts.png`：地点 edge 排名（n=122）。
- `fig_review_status_counts.png`：复核状态分布。
- `fig_review_priority_counts.png`：人工复核优先级分布。
- `fig_source_type_counts.png`：来源类型分布（n=56）。
- `fig_support_relation_types.png`：支持/资助关系类型分布（n=22）。

正式进度沟通稿：`docs/progress_report_v1.md`

## 10. 解释性图表包 v0（2026-07-01）

输出目录：`outputs/explanatory_v0/`

用途：

- 不是正式报告，而是下一次沟通前的解释型图件包。
- 用于从“统计进度”转向“机制解释”：桥接组织、地点框架、国际化路径、共同行动样本和证据缺口。

图件：

- `fig_actor_issue_bridge_network.png`：Top bridge actors，显示哪些 actor 同时连接反基地、环保、法律、自治、国际倡议等议题。
- `fig_place_issue_matrix_explanatory.png`：地点 × 议题框架矩阵。
- `fig_henoko_internationalization_pathway.png`：边野古 / 大浦湾国际化路径图。
- `fig_coaction_sample_composition.png`：2010 / 2015 / 2020 共同行动样本的当前 registry 构成。
- `fig_evidence_gap_map.png`：HR 合并后的 actor 复核状态和 source archive 状态。

配套 CSV：

- `actor_issue_bridge_nodes.csv`
- `place_issue_matrix.csv`
- `coaction_sample_composition.csv`
- `next_investigation_candidates.csv`

推荐沟通用主图：

1. 地点 × 议题框架矩阵。
2. 边野古 / 大浦湾国际化路径图。
3. Top bridge actors 组织-议题桥接网络。

下一轮调查提示：

- 2020 OEJP/MMC 71 团体样本已抽取完整 list；下一步是复核 52 个 registry extension candidates。
- 已有真实 URL 的 source archive 已完成第一轮归档；25 条 `inferred_url` 已核实/回填 11 条，剩余 14 条需要核成真实 URL 或标记未找到。
- 与那国、军属慈善 recipient、外务省 / JICA / ONC 仍是最值得启动的当地材料方向。

## 11. 模块完成包 v0（2026-07-01）

输出目录：`outputs/module_completion_v0/`

用途：

- 把解释性图表整理成模块交付物。
- 让 R2、R3/R4、R5、R11、R14 每块都有 brief、表和下一步任务。

核心文件：

- `module_status_table_v0.csv`：模块完成状态总表。
- `next_module_investigation_tasks_v0.csv`：下一步调查任务表（MT-001 至 MT-008）。
- `R02_actor_issue_network_brief.md`
- `R03_R04_place_frame_brief.md`
- `R05_coaction_event_brief.md`
- `R11_transnational_pathway_brief.md`
- `R14_coverage_bias_audit_brief.md`
- `coaction_events_v0.csv`
- `coaction_participants_v0.csv`
- `coaction_participants_2020_mmc_71_full_v0.csv`
- `actor_registry_extension_candidates_2020_mmc_v0.csv`
- `coaction_2020_mmc_71_extraction_note.md`
- `transnational_pathway_nodes_v0.csv`

当前模块完成度：

- R2：`module_v0`
- R3/R4：`module_v0`
- R5：`full_event_list_v0`
- R11：`pathway_v0`
- R14：`audit_v0`

下一步优先任务：

1. MT-001：复核并吸收 2020 OEJP/MMC 71 团体中的 registry extension candidates。
2. MT-003：继续核实剩余 14 条 `inferred_url`。
3. MT-004：与那国 A014/A015 当地证据包。

已基本完工，可对老板汇报为“完成底稿”的 MT：

- MT-001 的抽取阶段：71 团体完整 participant list、52 个 registry extension candidates、抽取说明。
- MT-002：真实 URL 来源本地备份，当前 74 archived / 2 manual archived / 0 pending archive。
- MT-003 第一轮：25 条 `inferred_url` 中 11 条已回填真实 URL 并归档，14 条仍待处理。

## 12. 2026-07-12 主线程状态更新

前述第 1–11 节保留为第一次/第二次同步时的历史快照，不再用于判断当前内部进度。当前数据为 103 actors、102 sources、180 actor–issue 候选边、124 actor–place 候选边、36 funding/support 样本边；另有 54 行事件感知关系表。

当前推进原则已经明确：先完成所有合理的线上工作、一期核心可视化和研究报告 v0，再派当地协作者。正式门槛见 `docs/phase1_online_completion_plan_v0.md`。

Registry 不再为达到 120+ 而机械扩充。2020 MMC Tier A 9 个组织已入表；Tier B 12 个组织只有在形成独立“日本本土声援层”并服务 R5/R11 分析时才分层纳入；Tier C 31 个一次性署名者维持事件限定。

下一轮对外沟通前，应优先形成：

1. 已完成的一期可视化审计与三张补图：组织功能生态、组织—地点、严格证据分层的 support/service 图。
2. 已完成的一期研究报告 v0 草稿与 W1 线上收口结果。
3. 剩余事件层验证、Tier A 别名/第二来源及图文一致性审查。
4. 从报告证据缺口反推的当地协作者正式任务包。
