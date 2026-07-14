# Phase 1 工作台

硬规则：本工作台永远不能超过 300 行；只记录当前状态、计划、阻塞和下一步，详细材料放到独立文档或数据表。

更新时间：2026-07-14

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
- [x] 扩充 actor-place edges 到 129 条（HR-013 新增 A111；HR-011 补 A107–A110 的有界地点语义）。
- [x] 扩充 funding/support edges 到 27 条。
- [x] 扩充 place registry 到 20 个地点。
- [x] 为高风险条目标注复核优先级（P1/P2/P3）。

阶段 C：人工复核与数据质量提升。

- [x] 定义人工复核任务书（HR-001 至 HR-009）。
- [x] 对 P1 条目进行第一轮 web 核实（AWWA/OESC/ヘリ基地反対協/イソバの会/石垣住民投票）。
- [x] 完成正式人工复核任务 HR-001 至 HR-009，并写入 `human_review_log_v0.csv`。
- [x] 补充来源日志中 URL 占位符条目（MT-003/W1：25/25 已解决；S020 恢复为 2016 年真实 URL）。
- [x] 曾按原方案和模块缺口扩充 actor registry 至 123；HR-015 撤出 9 个仅有 E2 一次署名线索的名称，HR-013/HR-010 又执行 A094→A111 范围替换，当前仍为 118。
- [ ] 以组织身份／持续性可核的 actor 补足合同 120 下限；不得把一次署名者重新塞回主表凑数。
- [ ] 处理 HR 复核后的剩余 `needs_second_source` / `needs_local_retrieval` 条目。
- [x] HR-011 至 HR-015 已落库；HR-013 新增 A111、保留 C010/C034 为背景、剔除 C029–C033，C015 仍属 HR-011 defer。
- [x] 根据本批复核结果更新 evidence_level、案件角色、事件边界和可发布措辞。
- [x] 建立信息源本地备份机制并持续归档（2026-07-13：265 archived / 2 manual / 26 failed / 2 non-url；失败含 403、SSL、动态页与瞬时网络波动，不等于证据不存在）。
- [x] 处理 S007 手工归档。
- [x] MT-003/W1：25 条 inferred_url 全部解决；S020 恢复为 2016 年琉球新报真实 URL并归档。

阶段 D：分析、可视化与进度沟通。

- [x] 生成第一次进度沟通图表（outputs/progress_sync_v0/）。
- [x] 起草第一版内部进度稿（docs/progress_report_v1.md；暂不交付）。
- [x] 生成解释性图表包 v0 并保留为历史探索包：组织-议题桥接网络、旧地点-议题宽投影、边野古国际化路径图、共同行动样本构成、证据缺口图。2026-07-14 方法审计确认旧地点×议题图存在 actor 层笛卡尔投影，已退役；正式 MA002 须用同源／同事件三元事实重建。
- [x] 生成旧编号模块包 v0：R2、R3/R4、R5、跨国路径、coverage brief、event table、任务表；仅作现有产出索引，不代表原方案 R1–R11 验收。
- [x] 抽取 2020 OEJP / MMC 71 团体完整 participant list，并生成 actor registry extension candidates。
- [x] 生成第二次进度同步稿 formal_comm_v0：对齐第一次文风的简洁 MD（`第二次进度同步_v0.md`），含研究模块菜单进度、七周工期对照、四张截图主图；图源由脚本生成。
- [x] 重写当地材料任务书 v1：分 Tier 1 线上可完成 / Tier 2 需当地协作两层（沟通稿中只保留一句概括）。
- [x] 完成原方案指定图的线上 v1：完整组织—议题网络、先岛三地专题图、组织—地点补图和六维覆盖偏差图；人审冻结与最终排版仍未完成。
- [x] 完成 W1 线上材料 pass、一期补图包和研究报告 v0 草稿；不等于一期线上收口或最终验收。
- [x] 按原始 DOCX 完成基础建设、R1–R11、五图及最终交付验收审计。
- [x] 完成 R4／R9／R10 候选包交叉 QA，并从 corrected/reviewed 层生成正式数据、解释性 brief 与图；HR-016／017／018 继续控制待审语义、角色和敏感行政关系。
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
- `docs/phase1_next_wave_plan_v1.md`
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
- `data/interim/06_evidence_notes_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/09_actor_event_venue_edges_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `data/interim/17_legal_policy_procedure_cases_v0.csv`
- `data/interim/18_legal_policy_actor_roles_v0.csv`
- `outputs/progress_sync_v0/`
- `outputs/online_completion_v0/`
- `outputs/phase1_visuals_v1/`
- `docs/phase1_research_report_v0.md`
- `docs/phase1_scheme_acceptance_audit_v1.md`
- `outputs/phase1_acceptance_audit_v0/`
- `outputs/phase1_foundation_v1/`
- `outputs/registry_expansion_v1/`
- `outputs/R08_legal_procedure_v0/`
- `outputs/R04_sakishima_frame_corpus_v0/`
- `outputs/R09_referendum_process_v0/`
- `outputs/R10_administrative_collaboration_v0/`
- `outputs/R10_completeness_audit_v1/`
- `outputs/R06_R07_R11_pathways_v1/`
- `outputs/R08_legal_procedure_v1/`
- `outputs/edge_activation_v1/`
- `outputs/registry_expansion_gate_v1/`
- `outputs/hr013_online_wave_integration_v1/`
- `outputs/phase1_source_integration_v1/`
- `outputs/R01_R02_actor_issue_v1/`
- `outputs/R05_coaction_v1/`
- `outputs/coverage_audit_v1/`
- `docs/phase1_next_wave_execution_v2.md`

## 当前样本状态

- actor registry：118 条。HR-013 新增 A111；用户对 HR-010 的范围勘误移出 A094，净数不变。A087–A093/A095–A101 仍为 E4 身份级安全合并待分类／关系复核；A094 的历史证据保留但不得自动回流。
- funding/support/relation edge 样本：43 条；F042 为 A109→A052 第4次嘉手纳法律代理，F043 为 A105→A107 全国／地域 YWCA 组织隶属，均明确 `not_funding_relation`。
- actor_issue_edges：222 条；A111 新增 women／peace／anti_base／human_rights 四条 HR-013 人审边。
- R1/R2 分层：101 个 actor 有正式议题边、17 个仍为 edge-isolated；222 条边中 59 条人审、163 条候选，43 条长期定位、40 条制度／案件、74 条事件性、65 条范围待定。完整二模图、议题共现图和 bridge mechanism 图已重生。
- actor_place_edges：129 条；A111/A107/A108 的 P001 仅表示全县组织／动员场域，A109 的 P005 为案件场域，A110 的 P002 为倡议对象，均不推定无来源的具体据点。
- actor alias：以主表为准；A010 前身、A052/A053 诉讼轮次及正式名已按 HR-012 处理。
- source log：295 条；NW2-H 复用 S158/S204，并将 47 个新 URL 以 provisional、`ai_seeded` 口径编为 S248–S294；S295 是 HR-011 精确定位补充，不属于该波次，也不构成独立组织身份二源。来源入表不批准 actor、候选边、联盟、资金、选举角色或解释；S051 仍为 E0 `rejected_archive_mismatch`。
- R10 的 35／26／43 为目的性跨来源样本内计数，不是官方年度或部门全量；完整性审计已机械索引 S002 的 86 页／616 行，确认当前 R10 只用 10 行，并把来源总体层与 HR-018 敏感关系层分开。
- issue taxonomy：26 个一级议题；本批新增 anti_war、mobilization。
- place registry：20 个地点 / 场域节点。
- venue taxonomy：16 类，已作为非结论性元数据合并。
- evidence notes：49 条正式表，HR-015 全批复核；其中五条 locator 仍明确待精确定位。
- actor-event-venue：67 条；63 条 `human_checked`、4 条 pathway `analytical_seed`。AEV0065–0067 只记录 A111/A108 的有界县民大会角色与 A109 的第4次嘉手纳诉讼角色；九个 MMC 小团体仍为 E2 event-only。
- R5 三名单：2010／2015／2020 共 169 条参与观察，63 条 registry actor、84 条 event-only、22 条 alias pending；严格口径有 15 个重复参与 actor。共同出现只作事件关系。
- R8 case registry：6 案全部 `human_checked`；27 个角色全部 accept，正式表区分 registry actor 与 provisional procedural node。
- R8 比较 v1：27 行 case×channel×place×role×result 矩阵、54 格 role-family 表和两张 SVG/HTML 图已完成；13 条 registered role／14 条 provisional node，泡濑两波分列，无 HR-026。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 解释性图表包 v0：5 张 PNG 图、4 个配套 CSV、1 个 README。
- 旧编号模块包 v0：含 R2、R3/R4、R5、跨国路径和 coverage 等现有 brief；最终方案中跨国路径属于 R6，coverage 属基础建设，不能用旧 R11/R14 编号判定验收。
- 第一版进度稿已完成，但暂作为内部草稿；下一次沟通需先完成解释性图表包。
- 已完成 HR-001 至 HR-015 的已提供记录，共 40 条 human review log；HR-016–022 与 HR-024–027／029–032 的决定栏保持空白，HR-023／028 为零项任务。
- 信息源备份机制已跑通：manifest 为 265 archived、2 manual_archived、26 failed、2 non-URL。S248–S294 中 40 条归档成功、7 条失败；267 个已保存 artifact 当前 0 SHA mismatch，失败记录保留访问错误。
- 六维 coverage audit v1 已重生：2020+ 来源 185/295，1972–1997 仅 4；Henoko 与全县宽泛节点合计 87/129 个地点观察。统计只描述公开资料样本可见性；无新增判断，故不创建 HR-023。
- post-HR013 edge activation 当前层覆盖 17 个孤立 actor：16 个形成 54 条候选边和 38 条来源，A073 为 `online_exhausted`；HR-010 补证 47 项、HR-024 8 项均留给人工。
- R3 空间语义已覆盖 129/129 边；60 target、37 site、6 institutional venue、5 event、4 HQ、17 unclear，41 项进入 HR-025。边野古 45 条中 42 条为 target；AP123 的 Camp Schwab/Foster 键值冲突保持显式。
- R9 选举候选层覆盖 2014/2018/2022 三届 19 条 actor-event，全部进入 HR-026；不得写票数、胜负或政策因果。
- Registry 价值门槛送入 HR-027 四个候选，若人工接受至少两个可达到 120；八重山大地会因持续性不足 defer，当前未新增 actor。
- R5/R7 异质行动把 148 条正式观察去重为 39 个行动单元、15 类行动、9 类场域；无新事实，HR-028=0。
- Schema/alias 冻结审计有 467 个候选、34 项 HR-029；中央 schema 尚未冻结。新来源 metadata/archive 的 22 个唯一 URL 进入 HR-030。
- R10 已对 S002 全部 86 页／616 行建立来源总体、行政资源类型表和两张 `ready_now` 图；365 个机器标签不是 actor，未来 canonical/JV/registry crosswalk 由 HR-032 的 8 项空白决定控制。
- 正式报告装配盘点 73 个现有资源并形成 32 页报告／20 页 PPT 蓝图；27 张非 superseded 正文图已有完整图—数据—来源—脚本—人审 gate 追溯链（14 ready、13 pending gate）。78 条报告主张的 32 组数字全部匹配，缺失 source／formal path 为 0；三项解释强度进入 HR-031。正式 DOCX/PDF、论文、PPT、先岛 dossier DOCX、public data 和冻结 codebook 仍是待生产合同成品，不能把蓝图计为完成。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核状态：HR-001 至 HR-015 的已提供记录均已合并。R4／公投／R10 分别形成 HR-016（12项）、HR-017（18项）、HR-018（26条关系＋8项来源前置）；R1/R2 为 HR-019（9 条规则＋30 个 bridge＋65 条 scope），R5 为 HR-020（14项），R6/R7/R11 为 HR-021（8项），来源层为 HR-022（49项），HR-024 为 8 项，HR-025 空间 41 项，HR-026 选举 19 项，HR-027 扩表 4 项，HR-029 schema 34 项，HR-030 来源 22 项，HR-031 报告解释强度 3 项，HR-032 partner alias/JV crosswalk 8 项。统一编排为 378 行，其中 370 个空白决策、8 个 ancillary 前置、13 个批次；coverage 不创建 HR-023，异质行动不创建事实任务且 HR-028=0。C015 维持 `needs_second_source`。

2026-07-14 正式派工：HR-027 四候选已作为 B01 第一优先批交给项目负责人，派工单为 `docs/human_review_assignment_HR027_v1.md`。回收前不分配 A 号、不为达到 120 自动接受，也不执行当前 118-actor 快照上的 HR-029。

当前当地补查优先级：与那国早期反部署组织、先岛/边野古核心组织报刊时间线、军属配偶俱乐部完整 recipient 年表。ONC 公开年度事业费和 S020 已在线解决。

当前人类决策状态：HD-001 至 HD-011 已决策完成。HD-011 以原始 DOCX 为唯一验收合同，并纠正 HD-010：registry 必须达到 120–180，仍由模块价值驱动，模块未饱和时可超过 180；Tier B 分层纳入、Tier C 事件限定。

当前最严厉验收判断：若今日交付，甲方应判“拒收后限期整改”；若今日投稿，学术上应判“desk reject／major reject”。原因不是数据量不足，而是合同成品未生产、registry 仍为 118、正式地点—议题图缺失、论文缺理论与可操作化转译、核心网络人审不足、复归后长期主张与来源年代不匹配。完整审计见 `docs/phase1_academic_client_redteam_audit_v1.md`。

## 问题抛出机制

目前不使用云表格；人工复核和当地补查都以任务书为准。

遇到以下情况，直接抛给人类确认：

- 公开资料显示"可能重要"，但缺少可复核来源。
- 资助 / 委托 / 赞助关系只有线索，没有 award、contract、财报或正式项目报告。
- 组织名、别名、法律身份或组织延续性无法确认。
- 需要当地数据库、图书馆、纸质资料、组织年报或当地联系人。
- 是否写入对外沟通稿存在政治或解释风险。

## 下一步

1. 以 `docs/phase1_scheme_acceptance_audit_v1.md` 为合同验收权威，以 `docs/phase1_academic_client_redteam_audit_v1.md` 为学术／最严甲方整改清单；第二次进度同步仍是甲方已知历史快照，第三次同步须按 correction ledger 主动更正四项旧口径。
2. P0 先做 HR-027 四候选，决定能否以模块价值把 registry 从 118 补到至少 120；不得为数字接受候选。
3. P0 完成会改变 actor／edge 的 HR-010／019／024、空间 HR-025 和选举 HR-026；修复 AP123。只有 HR-027 与这些合并后，才重跑并执行 HR-029，冻结 schema/alias/place/venue/relation/action 与 `R10_VENUE`。
4. P0 完成敏感关系 HR-018，再处理依赖它的 HR-021；报告 claim→source/evidence 审计已形成 78 条 claim、32 个数字组和 HR-031 三项解释决定。来源 HR-022／030 只审 metadata／支持边界，不等于关系复核；HR-032 只控制未来 actor-level R10 crosswalk，不阻断当前两张来源总体图。
5. P1 先以同源／同事件三元事实重建 MA002，旧地点×议题宽投影不得入正文；再依 32 页装配蓝图使用可用图和冻结图形成 25–35 页 DOCX/PDF。取得 HD-012 前期选举研究输入后，再派生 8k–12k 论文和 20 页 PPT，并交付先岛 dossier 与公开数据包。
6. R3、R4、R5/R7、R6、R8、R9、R10、R11 不再做无目标扩搜；只有相关 HR 否决关键事实或报告 claim 审计发现精确缺口时补源。
7. 学术线聚焦 R4＋R8＋R9：建立 12–18 条 translation episode、负案例和 reviewed-only／leave-one-source-out／身份不确定性等稳健性分析；甲方报告线仍覆盖 R1–R11，两条交付线不得混作一份。
8. 当地协作者只接报告明确指出、线上已耗尽且会改变图或解释的 Tier 2 字段；不覆盖第二次同步历史快照。
