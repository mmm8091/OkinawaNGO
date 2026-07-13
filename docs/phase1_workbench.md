# Phase 1 工作台

硬规则：本工作台永远不能超过 300 行；只记录当前状态、计划、阻塞和下一步，详细材料放到独立文档或数据表。

更新时间：2026-07-13

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
- [x] 曾按原方案和模块缺口扩充 actor registry 至 123；HR-015 后撤出 9 个仅有 E2 一次署名线索的名称，当前为 118。
- [ ] 以组织身份／持续性可核的 actor 补足合同 120 下限；不得把一次署名者重新塞回主表凑数。
- [ ] 处理 HR 复核后的剩余 `needs_second_source` / `needs_local_retrieval` 条目。
- [x] HR-011、HR-012、HR-014、HR-015 已落库；HR-013 未收到记录，不作推定。
- [x] 根据本批复核结果更新 evidence_level、案件角色、事件边界和可发布措辞。
- [x] 建立信息源本地备份机制并持续归档（2026-07-13：176 archived / 2 manual / 18 failed / 2 non-url；失败含 403、SSL 与瞬时网络波动，不等于证据不存在）。
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
- `outputs/R06_R07_R11_pathways_v1/`
- `outputs/phase1_source_integration_v1/`
- `outputs/R01_R02_actor_issue_v1/`
- `outputs/R05_coaction_v1/`
- `outputs/coverage_audit_v1/`

## 当前样本状态

- actor registry：118 条。HR-011 新增 A107–A110；HR-015 将旧 A077–A085 撤出主表、保留为 E2 事件参与线索。A087–A101 仍为 E4 身份级安全合并待分类／关系复核。
- funding/support/relation edge 样本：43 条；F042 为 A109→A052 第4次嘉手纳法律代理，F043 为 A105→A107 全国／地域 YWCA 组织隶属，均明确 `not_funding_relation`。
- actor_issue_edges：218 条；本批补足 A107–A110 的 women／human_rights／anti_war／mobilization／noise／legal 等人审议题边。
- R1/R2 分层：100 个 actor 有正式议题边、18 个仍为 edge-isolated；218 条边中 55 条人审、163 条候选，42 条长期定位、40 条制度／案件、73 条事件性、63 条范围待定。完整二模图、议题共现图和 bridge mechanism 图已形成线上 v1。
- actor_place_edges 初版：124 条。
- actor alias：以主表为准；A010 前身、A052/A053 诉讼轮次及正式名已按 HR-012 处理。
- source log：198 条；S160–S198 为 R4／R9／R10 的模块来源整合，统一保持 `ai_seeded`，来源入表不批准相应关系或解释；S051 为 E0 `rejected_archive_mismatch`，不得再用于 A011。
- issue taxonomy：26 个一级议题；本批新增 anti_war、mobilization。
- place registry：20 个地点 / 场域节点。
- venue taxonomy：16 类，已作为非结论性元数据合并。
- evidence notes：49 条正式表，HR-015 全批复核；其中五条 locator 仍明确待精确定位。
- actor-event-venue：64 条正式表；九个 MMC 小团体为 E2 `unverified_event_participant`，四条 pathway 为 `analytical_seed`。
- R5 三名单：2010／2015／2020 共 169 条参与观察，63 条 registry actor、84 条 event-only、22 条 alias pending；严格口径有 15 个重复参与 actor。共同出现只作事件关系。
- R8 case registry：6 案全部 `human_checked`；27 个角色全部 accept，正式表区分 registry actor 与 provisional procedural node。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 解释性图表包 v0：5 张 PNG 图、4 个配套 CSV、1 个 README。
- 旧编号模块包 v0：含 R2、R3/R4、R5、跨国路径和 coverage 等现有 brief；最终方案中跨国路径属于 R6，coverage 属基础建设，不能用旧 R11/R14 编号判定验收。
- 第一版进度稿已完成，但暂作为内部草稿；下一次沟通需先完成解释性图表包。
- 已完成 HR-001 至 HR-012、HR-014、HR-015 的已提供记录，共 31 条 human review log；HR-013 未收到材料，未代填。
- 信息源备份机制已跑通：2026-07-13 manifest 为 176 archived、2 manual_archived、18 failed、2 non-URL。S160–S198 中 37 条归档成功，S197/S198 因旧议会系统 SSL EOF 失败；archive 脚本支持定向重试与 artifact SHA 强校验。178 个已归档／手工归档 artifact 当前 0 mismatch；26 个历史 metadata 漂移项已显式对账并保留 hash 历史，失败记录保留访问错误供后续手工归档。
- 六维 coverage audit v1 已形成：2020+ 来源 125/198，1972–1997 仅 4；Henoko 与全县宽泛节点合计 83/124 个地点观察。统计只描述公开资料样本可见性；archive failure 不等于证据不存在，source 数不等于组织活跃度。无新增判断，故不创建 HR-023。
- 方案验收后第一批实作：16 类 venue、20 个 E4 actor 身份、41 条来源和 R8 六案元数据已安全合并；49 evidence、64 actor-event-venue、E3/沿革/范围候选及 R8 角色已进入 HR-010、011、012、014、015；HR-013 尚未收到。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核状态：HR-001 至 HR-012、HR-014、HR-015 的已提供记录均已合并；HR-013 无记录，保持空缺。R4／R9／R10 分别形成 HR-016（12项）、HR-017（18项）、HR-018（26条关系＋8项来源前置）；R1/R2 形成 HR-019（9 条规则＋30 个 bridge＋63 条 scope），R5 形成 HR-020（14 项名称／切分），R6/R7/R11 形成依赖 HR-018 的 HR-021（8项），来源层形成 HR-022（49项）。所有新任务决定栏为空；coverage 为机械审计，不创建 HR-023。A087-A101 仍待分批做分类／关系复核，C015 维持 `needs_second_source`。

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

1. 以 `docs/phase1_scheme_acceptance_audit_v1.md` 为验收权威：第二次进度同步仍是甲方已知快照；当前不具备一期最终验收条件。
2. Registry 最终仍须达到合同 120–180；但 R1/R2 显示当前更紧迫的是 18 个在表 actor 缺 edge-level evidence，9 个新扩样候选也全部 `count_ready=no`。先激活 18 个孤立 actor，再为能补足薄议题／地点／功能层的候选闭合“持续组织身份＋一期直接连接”；禁止为越过 120 重纳 A077-A085 或未审候选。
3. R4 线上正式层已完成：11 条安全事实、19 条安全来源、两张先岛比较图和 brief；7 条语义＋5 条 locator/speaker 进入 HR-016，8 条 reject 不回流。
4. R9 线上正式层已完成：24 个 accepted 阶段、25 个 accepted 角色、四案时间线和制度门槛图；9＋9 条待审层进入 HR-017，图中空心／星号不属于正式事实。
5. R10 规范层已完成：35 条关系、26 条金额、43 条功能观察及两张边界图；仅 9 条沿用既有人审，26 条敏感关系进入 HR-018。project cost、aggregate、NOFO、sponsor tier 不得写成 actor payment。
6. R8 已完成人审：六案与 27 角色进入正式表；A002/A019 non-party、A011 requester、A055/A020 supporter、A020 跨案异角均为强制边界。
7. HR-015 已形成 49 evidence notes 与 64 AEV 正式表；后续图表优先从正式表读取，event participation 与 analytical seed 不进入稳定关系结论。
8. MT-003、MT-005、MT-006、MT-007、MT-008 与 LR T1-B 的线上 pass 结论继续有效；金额、服务、署名和案件角色按最新人审边界解释。
9. C015、A014/A015、完整 AWWA recipient 年表等真正线上耗尽项，继续留在复核／当地任务书；未到派当地协作者阶段前，不用当地材料掩盖线上模块缺口。
10. R6/R7/R11 线上解释层已完成：69 条正式事实、6 类目标路径、3 案×3阶段场域图、44 条外来 actor 进入观察；4 条 analytical seed 分表，HR-021 前7项依赖 HR-018。
11. R1/R2 线上 v1 已完成 118×26 完整二模网络、议题共现、bridge mechanism 和分类生态；HR-019 控制受控词、30 个 bridge 和 63 条范围未决边。R5 已完成三次全名单和重复参与图，HR-020 控制 14 个身份问题。六维 coverage 图已完成且不需另设人审。
12. 下一次甲方材料必须以研究报告与解释性图为主，不直接覆盖第二次同步历史快照；下一轮优先补 18 个议题孤立 actor、完成 HR-019/020 所需线上证据、制作 R8 比较图，并把报告推进到正式 DOCX/PDF 与 PPT 结构。
