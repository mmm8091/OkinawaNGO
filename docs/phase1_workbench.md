# Phase 1 工作台

硬规则：本工作台永远不能超过 300 行；只记录当前状态、计划、阻塞和下一步，详细材料放到独立文档或数据表。

更新时间：2026-07-01

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
- [x] 补充来源日志中 URL 占位符条目（MT-003：24/25 已解决为真实 URL，仅剩 S020 待当地补查）。
- [ ] 继续扩充 actor registry 到 120-150 条。
- [ ] 处理 HR 复核后的剩余 `needs_second_source` / `needs_local_retrieval` 条目。
- [ ] 根据复核结果更新 evidence_level 和可发布措辞。
- [x] 建立信息源本地备份机制并完成归档（85 archived / 2 manual / 2 failed 瞬时 SSL / 1 inferred(S020) / 2 non-url）。
- [x] 处理 S007 手工归档。
- [x] MT-003：核实并回填 13 条 inferred_url（年份校正 S027/S030/S037/S040），本地归档；仅 S020 留当地补查。

阶段 D：分析、可视化与进度沟通。

- [x] 生成第一次进度沟通图表（outputs/progress_sync_v0/）。
- [x] 起草第一版内部进度稿（docs/progress_report_v1.md；暂不交付）。
- [x] 生成解释性图表包 v0：组织-议题桥接网络、地点-议题矩阵、边野古国际化路径图、共同行动样本构成、证据缺口图。
- [x] 生成模块完成包 v0：R2、R3/R4、R5、R11、R14 brief、event table、任务表。
- [x] 抽取 2020 OEJP / MMC 71 团体完整 participant list，并生成 actor registry extension candidates。
- [x] 生成第二次进度同步稿 formal_comm_v0：对齐第一次文风的简洁 MD（`第二次进度同步_v0.md`），含研究模块菜单进度、七周工期对照、四张截图主图；图源由脚本生成。
- [x] 重写当地材料任务书 v1：分 Tier 1 线上可完成 / Tier 2 需当地协作两层（沟通稿中只保留一句概括）。
- [ ] 准备组织-议题矩阵和组织-地点矩阵分析。

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

## 当前样本状态

- actor 初版：102 条（HR-001 后新增 A076；HR-005 后新增 X016/X017；MT-001 Tier A 新增 A077–A085 九条，均 E2 signatory-only 待核）。
- funding/support edge 样本：30 条（MT-005 新增命名 AWWA recipient 边 F028–F030）。
- actor_issue_edges 初版：180 条。
- actor_place_edges 初版：124 条。
- actor alias 初版：14 条。
- source log 初版：94 条（含 91 条真实 URL、1 条占位符 URL(S020)、2 条非 URL 参考；S093 儒艮诉讼 court docket、S094 AWWA recipient DVIDS）。
- issue taxonomy：19 个一级议题。
- place registry：20 个地点 / 场域节点。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 解释性图表包 v0：5 张 PNG 图、4 个配套 CSV、1 个 README。
- 模块完成包 v0：覆盖 R2、R3/R4、R5、R11、R14；含 5 个 brief、模块状态表、共同行动 event/participant 表、2020 MMC 71 团体完整表、下一步模块调查任务表。
- 第一版进度稿已完成，但暂作为内部草稿；下一次沟通需先完成解释性图表包。
- 已完成 HR-001 至 HR-009 正式人工复核，并建立 9 条 human review log。
- 信息源备份机制已跑通：89 条已归档，2 条手工归档，1 条 `inferred_url`(S020) 待当地补查，2 条非 URL 书目参考（最近一次 0 失败；偶发瞬时 SSL 失败重试即恢复）。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核状态：HR-001 至 HR-009 已完成首轮；actor 表仍保留 P1/P2/P3 复核优先级，用于后续补源和当地材料收集，不等于未完成 HR 数。

当前当地补查优先级：与那国早期反部署组织、军属配偶俱乐部慈善 recipient、外务省 / JICA / ONC 关系链。

当前人类决策状态：HD-001 至 HD-008 已决策完成；下一次沟通采用普通 / 保守口径，但必须先完成解释性图表包；暂不急派当地协作者。

## 问题抛出机制

目前不使用云表格；人工复核和当地补查都以任务书为准。

遇到以下情况，直接抛给人类确认：

- 公开资料显示"可能重要"，但缺少可复核来源。
- 资助 / 委托 / 赞助关系只有线索，没有 award、contract、财报或正式项目报告。
- 组织名、别名、法律身份或组织延续性无法确认。
- 需要当地数据库、图书馆、纸质资料、组织年报或当地联系人。
- 是否写入对外沟通稿存在政治或解释风险。

## 下一步

1. 第二次进度同步稿已交付（source_docs/current 两份 PDF 并列）；下一轮沟通再议。
2. MT-001 Tier A 9 条已写入 registry（93→102）并接入 2020 MMC event（R5，2→11）；剩：补 alias（tentative 日文名待核）、二次核实后加议题/地点候选边。B=12 暂缓 / C=31 署名限定。
3. MT-003 基本完成：24/25 已解决为真实 URL 并归档（年份校正 S027/S030/S037/S040），仅 S020（宫古地下水）留当地补查。
4. MT-007 基本完成：`lawsuit_actor_role_table_v0.csv` 已定案 Okinawa Dugong v. Rumsfeld 各方角色（A076 原告确认、A002/A019 非当事方、JELF 原告、Earthjustice 律师）；剩 Turtle Island Restoration Network 未入表可作候选。
5. MT-005 进行中：已把 AWWA aggregate 落成命名 recipient 边 F028–F030（Yomitan Quegoen / Uruma 社福 / Boy Scouts Far East，E3 DVIDS 源）；剩完整年表需 Form 990 / 年报。见 `MT005_awwa_recipient_note.md`。
6. 执行 LR v1 Tier 1 剩余项：T1-B USO 赞助、T1-D/E 线上公开报告；继续扩 registry 到 120+。
7. 根据 2020 MMC 71 团体表和 event table 结果生成 R5/R11 的下一版网络图。
