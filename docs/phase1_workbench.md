# Phase 1 工作台

硬规则：本工作台永远不能超过 300 行；只记录当前状态、计划、阻塞和下一步，详细材料放到独立文档或数据表。

更新时间：2026-07-12

## 当前定位

一期不做"复归以来全量 NGO 网络"，先做可复核的小型研究：

> 冲绳民间组织 / NGO 如何把基地问题转译为环保、生活安全、地方自治、人权、法律程序和国际倡议等议题？这些组织在边野古、与那国、先岛等关键地点中扮演了什么样的公开角色？

当前 actor 范围：

- 冲绳本土市民团体、NPO、住民の会、連絡会、実行委員会。
- 日本本土环保、和平、法律、人权和国际合作 NGO。
- 国际倡议组织和海外支援组织。
- 美军基地社区服务组织、军属福利组织、军属配偶慈善组织。
- 公共外交、青年交流、奖学金、JICA / 外务省 / 美国使领馆相关项目。
- 作为资助方、委托方、赞助方或制度节点出现的政府机构、企业、基金会和国际组织。

## 不可踩线

- 不把共同署名等同于稳定联盟。
- 不把服务型 NGO 自动解释成反基地或亲基地。
- 不把 grant opportunity 写成已拨款事实。
- 不把 NED / USAID / 外务省 / 美国使领馆关系写成"资金链"，除非有官方 grant、award、contract、财报或项目报告。
- 不做 AI 写 AI 审；敏感关系必须人工复核。
- 标准一期不承诺完整媒体可见度、完整人物网络、完整组织谱系。

## 当前阶段任务

阶段 A：问题、边界、样本口径和编码规则。

- [x] 确认一期主问题。
- [x] 确认 actor universe 扩展到外来 NGO / 军属服务 / 资助节点。
- [x] 建立 evidence_level 分级。
- [x] 建立人工复核要求：人工参与度至少 30%。
- [x] 建立工作台。
- [x] 建立编码字段说明。
- [x] 建立正式 `source_log_initial`。
- [x] 把新版方案中的模块编号冲突记入待修。

阶段 B：NPO / NGO / 市民团体资料收集与组织样本初版。

- [x] 汇总既有 20 个运动 / 国际倡议 actor seed。
- [x] 汇总 15 个外来 NGO / 军属服务 / 资助节点 seed。
- [x] 建立初版 actor registry。
- [x] 扩 actor seed 到 60 个左右。
- [x] 建立 funding/support edge 样本表。
- [x] 建立 issue taxonomy 初版。
- [x] 建立 place registry 初版。
- [x] 建立当地补查队列初版。
- [x] 建立 actor_issue_edges 初版。
- [x] 建立 actor_place_edges 初版。
- [x] 扩充 actor registry 到 93 条。
- [x] 扩充 source log 到 92 条。
- [x] 扩充 actor-issue edges 到 180 条。
- [x] 扩充 actor-place edges 到 124 条。
- [x] 扩充 funding/support edges 到 27 条。
- [x] 扩充 place registry 到 20 个地点。
- [x] 为高风险条目标注复核优先级（P1/P2/P3）。

阶段 C：人工复核与数据质量提升。

- [x] 定义人工复核任务书（HR-001 至 HR-009）。
- [x] 对 P1 条目进行第一轮 web 核实（AWWA/OESC/ヘリ基地反対協/イソバの会/石垣住民投票）。
- [x] 完成正式人工复核任务 HR-001 至 HR-009，并写入 `human_review_log_v0.csv`。
- [x] 补充来源日志中 URL 占位符条目（MT-003/W1：25/25 已解决；S020 恢复为 2016 年真实 URL）。
- [ ] 按原方案和模块缺口扩充 actor registry 至至少 120（合同范围 120–180；模块未饱和时可超过 180）。
- [ ] 处理 HR 复核后的剩余 `needs_second_source` / `needs_local_retrieval` 条目。
- [ ] 根据复核结果更新 evidence_level 和可发布措辞。
- [x] 建立信息源本地备份机制并持续归档（2026-07-12：93 archived / 2 manual / 5 failed / 2 non-url；失败含 MOFA 403 与瞬时网络波动）。
- [x] 处理 S007 手工归档。
- [x] MT-003/W1：25 条 inferred_url 全部解决；S020 恢复为 2016 年琉球新报真实 URL并归档。

阶段 D：分析、可视化与进度沟通。

- [x] 生成第一次进度沟通图表（outputs/progress_sync_v0/）。
- [x] 起草第一版内部进度稿（docs/progress_report_v1.md；暂不交付）。
- [x] 生成解释性图表包 v0：组织-议题桥接网络、地点-议题矩阵、边野古国际化路径图、共同行动样本构成、证据缺口图。
- [x] 生成旧编号模块包 v0：R2、R3/R4、R5、跨国路径、coverage brief、event table、任务表；仅作现有产出索引，不代表原方案 R1–R11 验收。
- [x] 抽取 2020 OEJP / MMC 71 团体完整 participant list，并生成 actor registry extension candidates。
- [x] 生成第二次进度同步稿 formal_comm_v0：对齐第一次文风的简洁 MD（`第二次进度同步_v0.md`），含研究模块菜单进度、七周工期对照、四张截图主图；图源由脚本生成。
- [x] 重写当地材料任务书 v1：分 Tier 1 线上可完成 / Tier 2 需当地协作两层（沟通稿中只保留一句概括）。
- [ ] 完成原方案指定的完整组织—议题网络和与那国/先岛专题图；组织—地点补图已完成。
- [x] 完成 W1 线上材料 pass、一期补图包和研究报告 v0 草稿；不等于一期线上收口或最终验收。
- [x] 按原始 DOCX 完成基础建设、R1–R11、五图及最终交付验收审计。
- [ ] 完成 R1–R11 缺口补料、解释性成果、论文、25–35 页报告和 15–20 页 PPT。

## 文件索引

- `docs/phase1_workbench.md`
- `docs/human_review_tasks_v0.md`
- `docs/local_retrieval_tasks_v0.md`
- `docs/human_decision_tasks_v0.md`
- `docs/local_retrieval_tasks_v1.md`
- `docs/progress_sync_assets_v0.md`
- `docs/progress_report_v1.md`
- `outputs/formal_comm_v0/`
- `docs/source_archive_protocol_v0.md`
- `docs/phase1_online_completion_plan_v0.md`
- `docs/p1_review_prompt_v0.md`
- `docs/human_review_merge_package_v0.md`
- `data/interim/16_inferred_url_resolution_queue_v0.csv`
- `outputs/explanatory_v0/`
- `outputs/module_completion_v0/`
- `data/metadata/coding_schema_v0.md`
- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/02_actor_aliases_initial_v0.csv`
- `data/interim/03_issue_taxonomy_v0.csv`
- `data/interim/04_place_registry_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `outputs/progress_sync_v0/`
- `outputs/online_completion_v0/`
- `outputs/phase1_visuals_v1/`
- `docs/phase1_research_report_v0.md`
- `docs/phase1_scheme_acceptance_audit_v1.md`
- `outputs/phase1_acceptance_audit_v0/`

## 当前样本状态

- actor 初版：103 条（HR-001 后新增 A076；HR-005 后新增 X016/X017；MT-001 Tier A 新增 A077–A085 九条 E2 signatory-only；MT-007 新增 A086 Turtle Island Restoration Network）。
- funding/support edge 样本：36 条（新增 NOSCO 共同实物捐赠事件 F036；不得归为 NOSCO 单独捐赠）。
- actor_issue_edges 初版：180 条。
- actor_place_edges 初版：124 条。
- actor alias 初版：14 条。
- source log：102 条（100 条真实 URL、2 条非 URL 参考；S020 已恢复，新增 S099-S102：ONC 法定报告 / JICA 受托报告 / MOFA 名单 / NOSCO 共同捐赠）。
- issue taxonomy：19 个一级议题。
- place registry：20 个地点 / 场域节点。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 解释性图表包 v0：5 张 PNG 图、4 个配套 CSV、1 个 README。
- 旧编号模块包 v0：含 R2、R3/R4、R5、跨国路径和 coverage 等现有 brief；最终方案中跨国路径属于 R6，coverage 属基础建设，不能用旧 R11/R14 编号判定验收。
- 第一版进度稿已完成，但暂作为内部草稿；下一次沟通需先完成解释性图表包。
- 已完成 HR-001 至 HR-009 正式人工复核，并建立 9 条 human review log。
- 信息源备份机制已跑通：2026-07-12 manifest 为 93 archived、2 manual_archived、5 failed、2 non-URL；S020/S099/S100/S102 已归档，S096/S101 MOFA 页面与若干来源可能失败，归档/失败数会因瞬时网络波动变化。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核状态：HR-001 至 HR-009 已完成首轮；actor 表仍保留 P1/P2/P3 复核优先级，用于后续补源和当地材料收集，不等于未完成 HR 数。

当前当地补查优先级：与那国早期反部署组织、先岛/边野古核心组织报刊时间线、军属配偶俱乐部完整 recipient 年表。ONC 公开年度事业费和 S020 已在线解决。

当前人类决策状态：HD-001 至 HD-011 已决策完成。HD-011 以原始 DOCX 为唯一验收合同，并纠正 HD-010：registry 必须达到 120–180，仍由模块价值驱动，模块未饱和时可超过 180；Tier B 分层纳入、Tier C 事件限定。

## 问题抛出机制

目前不使用云表格；人工复核和当地补查都以任务书为准。

遇到以下情况，直接抛给人类确认：

- 公开资料显示"可能重要"，但缺少可复核来源。
- 资助 / 委托 / 赞助关系只有线索，没有 award、contract、财报或正式项目报告。
- 组织名、别名、法律身份或组织延续性无法确认。
- 需要当地数据库、图书馆、纸质资料、组织年报或当地联系人。
- 是否写入对外沟通稿存在政治或解释风险。

## 下一步

1. 以 `docs/phase1_scheme_acceptance_audit_v1.md` 为权威：当前不具备一期验收条件；第二次进度同步只代表甲方已知快照。
2. MT-001 Tier A 9 条已写入 registry（93→102）并接入 2020 MMC event（R5，2→11）；剩：补 alias（tentative 日文名待核）、二次核实后加议题/地点候选边。B=12 仅在建立独立本土声援层时分层纳入；C=31 署名限定。
3. MT-003 已完成：25/25 inferred URL 全部解决；S020 恢复为 2016 年琉球新报文章并归档，不再派当地补查。
4. MT-007 基本完成：`lawsuit_actor_role_table_v0.csv` 已定案 Okinawa Dugong v. Rumsfeld 各方角色（A076 原告确认、A002/A019 非当事方、JELF 原告、Earthjustice 律师）；Turtle Island Restoration Network 已作为 A086 入表。
5. MT-005 线上 pass 完成：AWWA 命名 recipient 边 F028–F030；新增 NOSCO 共同捐赠 F036。完整年表仍需 Form 990 / 内部年报。见 `outputs/online_completion_v0/`。
6. MT-008 基本完成：`actor_relation_events_v1.csv`（54 行 / 9 事件 / 5 action 类型）把 co-action+诉讼+公投统一成事件感知层；schema 增强提案待并入 07/08。见 `MT008_edge_enrichment_note.md`。
7. MT-006 线上公开记录基本完成：ONC 归入国际协作/多文化行政层；S099 补足 FY2024 年度事业费，S100 确认 JICA 受托角色。金额只写项目成本，不写合同支付额。
8. LR T1-B 基本完成：USO Okinawa 8 中心 + 命名赞助方（AEC 升 E4、MBC/Matson 边），服务对象=美军社区。见 `LR_T1B_uso_note.md`。
9. MT-004 线上 pass 完成：A014 事件语境有主流佐证（RS/OT/QAB）、A015 无非党派源保持 E2；组织级身份仍需与那国当地补查（LR Tier 2）。见 `MT004_yonaguni_online_pass_note.md`。
10. R5/R11 事件感知图已出：`fig/fig_event_repertoire.png`（集体行动 repertoire 时间线，`make_event_repertoire_fig.py`）。
11. 下一轮按 P0–P4 推进：schema/lint 与缺表 → 模块驱动 registry 扩样 → R7/R8/R9/R10 等缺口补料 → 指定核心图与各模块解释 → 正式报告/论文/PPT → 精确当地任务。详见方案验收总表。
