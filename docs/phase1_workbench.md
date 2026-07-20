# Phase 1 工作台

硬规则：本工作台永远不能超过 300 行；只记录当前状态、计划、阻塞和下一步，详细材料放到独立文档或数据表。

更新时间：2026-07-20

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
- [x] 按原方案和模块缺口清理后，HR-027 又以四项模块修复把 actor registry 历史记录从 118 扩至 122；A072 合并 tombstone 后当前有效 actor 为 121，达到 120 下限，但不以数字本身作为准入理由。
- [x] 以组织身份／持续性和模块价值为准补足合同 120 下限；HR-027 四项均获负责人批准，未把一次署名者或 tombstone 塞回有效层凑数。
- [ ] 处理 HR 复核后的剩余 `needs_second_source` / `needs_local_retrieval` 条目。
- [x] HR-011 至 HR-015 已落库；HR-013 新增 A111、保留 C010/C034 为背景、剔除 C029–C033，C015 仍属 HR-011 defer。
- [x] 根据本批复核结果更新 evidence_level、案件角色、事件边界和可发布措辞。
- [x] 建立信息源本地备份机制并持续归档（2026-07-20：273 archived / 2 manual / 18 failed / 2 non-url；失败含 403、SSL、动态页与瞬时网络波动，不等于证据不存在）。
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
- [x] 完成原方案指定图的线上 v1：完整组织—议题网络、先岛三地专题图、组织—地点补图和六维覆盖偏差图；人审冻结已完成，冻结后五图重绘／QA 与最终排版仍未完成。
- [x] 完成 W1 线上材料 pass、一期补图包和研究报告 v0 草稿；不等于一期线上收口或最终验收。
- [x] 按原始 DOCX 完成基础建设、R1–R11、五图及最终交付验收审计。
- [x] 完成 R4／R9／R10 候选包交叉 QA，并从 corrected/reviewed 层生成正式数据、解释性 brief 与图；HR-016 线上项已清零，HR-017／018 线上决定已合并，只保留当地材料 9＋2 项。
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
- `outputs/formal_comm_v1/`
- `outputs/formal_comm_v2/`
- `docs/source_archive_protocol_v0.md`
- `docs/phase1_online_completion_plan_v0.md`
- `docs/phase1_next_wave_plan_v1.md`
- `docs/p1_review_prompt_v0.md`
- `docs/human_review_merge_package_v0.md`
- `data/interim/16_inferred_url_resolution_queue_v0.csv`
- `outputs/explanatory_v0/`
- `outputs/module_completion_v0/`
- `data/metadata/coding_schema_v0.md`
- `data/metadata/coding_schema_v1.md`
- `docs/nr3_recheck_and_relation_frontend_brief_v1.md`
- `docs/actor_relation_architecture_v1.md`
- `docs/human_review_task_HR033_legacy_relation_status_v1.md`
- `docs/human_review_task_HR035_actor_issue_claim_freeze_v1.md`
- `docs/frontend_actor_issue_state_handoff_v1.md`
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
- `docs/next_round_exploration_system_sessions_v1.md`

## 当前样本状态

- actor registry：122 条历史记录／121 个有效 actor。A072 是并入 A071 的重复组织 tombstone，不进入当前图或普通搜索；A112–A115 是模块修复型新增 actor。有效数仍达到方案 120 下限；A094 不得自动回流。
- funding/support/relation edge 样本：43 条；F042 为 A109→A052 第4次嘉手纳法律代理，F043 为 A105→A107 全国／地域 YWCA 组织隶属，均明确 `not_funding_relation`。
- actor_issue_edges：中央表 294 条历史记录；当前有效网络 283 条（125 人审／158 候选），连接 116 个有效 actor，5 个孤立。11 条 rejected／deactivated／excluded 边只保留审计历史；AI068 和 AI178 不进默认冲绳叙事。
- R1/R2 分层：HR-019 已完整合并，当前图、共现、bridge 和 coverage 均只读有效层；稳健性分析仍显示删除 S004 后生态→国际桥由 8 降至 4，去三源后 A001/A002/A009/A046 仍在。
- actor_place_edges：135 条历史记录；130 条有效（53 人审／77 候选），5 条 retired。总部、现场、活动场域、倡议对象和制度场域保持分开。
- actor alias：39 条；A010 前身、A052/A053 诉讼轮次及正式名已按 HR-012 处理。
- source log：295 条；NW2-H 复用 S158/S204，并将 47 个新 URL 以 provisional、`ai_seeded` 口径编为 S248–S294；S295 是 HR-011 精确定位补充，不属于该波次，也不构成独立组织身份二源。来源入表不批准 actor、候选边、联盟、资金、选举角色或解释；S051 仍为 E0 `rejected_archive_mismatch`。
- R10 的 35／28／43 为目的性跨来源样本内计数，不是官方年度或部门全量；关系／金额／功能层的人审状态分别为 24/10/1、21/6/1、29/13/1（checked/revised/local）。完整性审计已机械索引 S002 的 86 页／616 行，确认当前 R10 只用 10 行，并把来源总体层与 HR-018 敏感关系层分开。
- issue taxonomy：26 个一级议题；本批新增 anti_war、mobilization。
- place registry：21 个地点／场域节点，含 P021 Sakishima Islands。
- venue taxonomy：16 类，已作为非结论性元数据合并。
- evidence notes：49 条正式表，HR-015 全批复核；其中五条 locator 仍明确待精确定位。
- actor-event-venue：67 条；63 条 `human_checked`、4 条 pathway `analytical_seed`。AEV0065–0067 只记录 A111/A108 的有界县民大会角色与 A109 的第4次嘉手纳诉讼角色；九个 MMC 小团体仍为 E2 event-only。
- R4 先岛框架：19 条人审／QA-safe 事实、24 条安全摘录、14 个分层实体；HR-016 线上队列为 0，2 个 registry actor 对 9 个制度节点的结构仍提示来源偏差。
- R5 三名单：169 条参与观察＝64 条 registry actor、22 条人审核定的 event-only identity、83 条其他 event-only name，alias pending 为 0；6 个 event-only identity 跨事件重复。共同出现只作事件关系。
- R6/R7/R11 共用正式层：80 条 observation＋4 条独立 seed；R6 六类路径、R7 三案／九阶段、R11 53 条外来进入观察。六个 SVG/HTML 已由只读当前模块表的 renderer 重绘；A066 县基地政策合同单列，不误归 USO/service。
- R8 case registry：6 案全部 `human_checked`；27 个角色全部 accept，正式表区分 registry actor 与 provisional procedural node。
- R8 比较 v1：27 行 case×channel×place×role×result 矩阵、54 格 role-family 表和两张 SVG/HTML 图已完成；13 条 registered role／14 条 provisional node，泡濑两波分列，无 HR-026。
- R9：公投正式层 29 stages／29 roles，HR-017 仍有当地 9 项；选举层 19/19 已人审，其中 18 条确认发生、1 条只确认预告。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 解释性图表包 v0：5 张 PNG 图、4 个配套 CSV、1 个 README。
- 旧编号模块包 v0：含 R2、R3/R4、R5、跨国路径和 coverage 等现有 brief；最终方案中跨国路径属于 R6，coverage 属基础建设，不能用旧 R11/R14 编号判定验收。
- 第一版进度稿仍是内部历史草稿；第三次 findings-led v2 与探索前端已经形成，下一次沟通应从当前系统和冻结后图件取材。
- HR-035 Batch 1、HR-010 batch 6、LCR001–004、HR-034、HR-029 和 HR-031 已于 2026-07-20 全部由负责人确认并完成受控合并；HR-023／028 为零项任务。当前正式未闭合总账只剩 12 项当地／新一手材料任务，其中 HR-018 的 2 项已有 defer 决定、等待新材料后闭合。详见 `docs/principal_human_review_remaining_v17.md`。
- 信息源备份机制已跑通：manifest 为 273 archived、2 manual_archived、18 failed、2 non-URL；失败条目不等于证据不存在。
- 六维 coverage audit v1 已按冻结后有效层重生：121 actors／283 actor-issue／130 actor-place／295 sources，中央历史边界为 122／294／135。当前生成有 120 个 category cells，但 cell 数不是稳定契约；统计只描述公开资料样本可见性，不创建 HR-023。
- post-HR013 edge activation 的 17 actor／54 edge 是历史审计包，不是当前网络总量；HR-024 线上决定已合并，A073 为 `online_exhausted`／当地项。HR-010 batch 6 已接受46条并新增 AI249–AI294，HR010-B6-019 保持 defer。
- R3 空间语义已完成 HR-025：135 条历史／130 条有效，当前先岛 dossier 13 条（与那国6／石垣3／宫古4）；AP106 仅作 rejected history，AP123 已固定为 P007 Camp Foster。
- R9 选举层 19/19 已人审：18 条确认公开参与发生，1 条仅确认活动预告；不得写票数、胜负或政策因果。
- HR-027 已完成 4/4 `add` 并回填，中央 AEV 未新增；17 个事件仅进入 `outputs/hr027_integration_v1/event_candidates_v1.csv`，关系边新增 0。八重山大地会维持 defer。
- R5/R7 异质行动把 148 条正式观察去重为 39 个行动单元、15 类行动、9 类场域；无新事实，HR-028=0。
- Schema/alias 冻结审计已在 HR-010／LCR／HR-034 后最终重生为 505 个候选、41 项 HR-029，并完成中央冻结。P004 Futenma 议题／地域层与 P010 MCAS Futenma 实体基地层保持分离；18个 `R10_VENUE` 占位已全部处置。
- 地点×议题正式替代层已按冻结后中央边重生：305 条有效同源三元事实，298 条为 E3/E4，71 条两边均经人审，97 条可附着正式事件观察。旧宽投影只作方法上界。
- 转译机制比较已形成 13 个 episode（R8/R9 已核案件 9 个＋HR-027 事件候选 4 个）：所有入选 episode 均产生可观察中间产出，但底层项目／政策按诉求明确改变为 0，泡濑仅为跨波次 mixed；这是“已进入场域的案例”比较，不是总体成功率或因果估计。
- R10 已对 S002 全部 86 页／616 行建立来源总体；365 个机器标签不是 actor。HR-032 的 8 项 canonical／JV／registry crosswalk 已合并，未把复合体成员展开成付款或稳定关系。
- 正式报告装配盘点 73 个现有资源并形成 32 页报告／20 页 PPT 蓝图；HR-029 数据冻结门已清除，但原五张 freeze-required 图仍须按冻结词表重绘／QA 后才能改为 ready。HR-031 三项均选择 B，报告相关段落已降为样本分析框架、公开材料地点差异和并列国际化入口。正式 DOCX/PDF、论文、PPT、先岛 dossier DOCX、public data 和最终 codebook/lint 仍是待生产合同成品，不能把蓝图计为完成。
- 第三次同步已重写为 findings-led v2：`outputs/formal_comm_v2/第三次进度同步_v2.md` 与 6 张机制图，主线为“地方损害如何被组织翻译进不同制度语法，以及制度如何把诉求转换为有限结果”；新增 R5“小型重复骨架＋事件性变动外围”解释。图 6 已由 current-only renderer 重绘：2020 registry 行为 17，15 个重复 registry actor 与 6 个重复 human-reviewed event-only identity 分层呈现。v1 的 4 张方法／稳健性图退到附录。两版均不生成 PDF，由项目负责人自行排版。
- 2026-07-17 起切换为共同研究节奏：项目负责人在解释性工作中的目标参与度约 50%。首轮项目回归表仍为暂停记录；2026-07-20 负责人另行明确授权启动一轮“边研究边选题”的全面探索。该授权仅覆盖不改中央事实层／现有前端契约的 H1–H3 独立研究包，新的强解释和模块取舍仍逐项设置负责人检查点。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核状态：所有正式线上任务均已回交并合并；当前只剩 12 项当地／新一手材料任务。HR-033 将 6 条 legacy relation 分层；HR-029 又把 F025 的 relation type 冻结为 `donation`，但仍不挂 102,000 美元，该金额只在 R10R029 汇总观察。C015 维持 `needs_second_source`。

当前人工任务总账见 `docs/principal_human_review_remaining_v17.md`；OPI-00 仍是暂停／未完成的学习记录，但不再阻断负责人于 2026-07-20 明确批准的 H1 文档可见性、H2 两套功能生态、H3 前线化／战争记忆三个有界研究包。它仍阻断未经另行批准的中央表扩张或结论升级。

当前当地补查优先级：P0 为 T2-D 先岛三地民间组织原始表达对照，P1 为 T2-E 公投制度门槛一手材料；T2-A/B 的组织身份与报刊时间线同馆顺带完成。T2-G 已把 9 个 HR-017 公投尾项、2 个 HR-018 暂缓财务项和 A073 身份核查逐项映射为正式 closure 清单。T2-F 1972–2012 谱系仅在保留“复归后”长期主张时启动；AWWA recipient 年表不阻断机制主线。

2026-07-18 下一轮改为 session 化的“降熵”工程：NR-01 研究信息架构、NR-02 前端数据契约、NR-03 可点击最小演示、NR-04 1972–1997 线上补缺、NR-05 1998–2012 线上补缺、NR-06 证据集成与演示验收。总任务书为 `docs/next_round_exploration_system_sessions_v1.md`。不再无目标加 actor/source/图；NR-04/05 结果未经人工决定不得进入前端默认层。

当前人类决策状态：HD-001 至 HD-011 已决策完成。HD-011 以原始 DOCX 为唯一验收合同，并纠正 HD-010：registry 必须达到 120–180，仍由模块价值驱动，模块未饱和时可超过 180；Tier B 分层纳入、Tier C 事件限定。

当前最严厉验收判断：若今日交付，仍应判“拒收后限期整改”；若今日投稿，仍是 major reject。HR-027 已修复 120 下限，MA002 也有第一版同源替代层，转译 episode 与稳健性分析已启动；但合同成品未生产、核心网络／空间 edge 人审不足、复归后长期主张与来源年代不匹配，且新机制图仍须事件级复核。完整审计见 `docs/phase1_academic_client_redteam_audit_v1.md`。

## 问题抛出机制

目前不使用云表格；人工复核和当地补查都以任务书为准。

遇到以下情况，直接抛给人类确认：

- 公开资料显示"可能重要"，但缺少可复核来源。
- 资助 / 委托 / 赞助关系只有线索，没有 award、contract、财报或正式项目报告。
- 组织名、别名、法律身份或组织延续性无法确认。
- 需要当地数据库、图书馆、纸质资料、组织年报或当地联系人。
- 是否写入对外沟通稿存在政治或解释风险。

## 下一步

1. NR-01 检查点 A 的产品方向已由负责人确认并重写：前端是后端研究数据的自动化可视化客户端；固定四个主页面（总览／组织／路径／证据）、四个主可视化引擎、全局时间层与证据抽屉。`docs/exploration_system_information_architecture_v1.md`、module crosswalk 和 view/visual inventory 是 NR-02 输入；旧 `wireframe.html`／`route_map.svg` 仅为 superseded exploration，不得反推页面。
2. NR-02 已从冻结后中央层正式重生：122 条 actor 历史／121 条普通界面可见、294 条 actor-issue 历史／283 条有效（125人审／158候选）。四态为67 frozen-bounded／58 accepted-unfrozen／44 scope-reviewed fact-pending／114 fact-pending；R1/R2、strict place–issue、coverage 与探索前端计数一致。
3. NR-03 已完成可点击演示并经负责人三轮迭代：总览／组织／时间／路径四页上线（2026-07-19 负责人把时间层改为第五主页面、否决严格证据地图状态与总览证据深浅标记，IA 修订记录见 `docs/exploration_system_information_architecture_v1.md` §12）；演示／研究双视图已接入 `research/candidates.json`（虚线＋待审标记），字号规范、图名＋问号说明、文案纪律（非永久不入界面）已冻结进 `prototypes/nr3_explorer/AGENTS.md`；QA 截图证据在 `prototypes/nr3_explorer/qa/`，过程记录在根目录 `design-qa.md`。随后证据页（V4）、中／日／EN 三语（229 码映射＋全 UI 文案）与证据抽屉完成，负责人确认检查点 B 不再单独进行；正式换手件为 `docs/nr3_handoff_v1.md`（截图在 `docs/nr3_handoff_assets/`）。
4. NR-03 v2 的三项非阻断整改已完成：固定 UI/aria 三语化、A073 与 A002 验证职责分开、跨路由关闭证据抽屉。正式换手见 `docs/nr3_handoff_v1.md`。
5. 负责人已批准证据状态与前端展示规则：界面“演示视图”改为“已核视图”；已核层允许 `supported_bounded`，但必须显示已核／缺失字段；研究层增加 candidate／lead。权威规则为 `data/metadata/coding_schema_v1.md`。
6. 关系架构 v1 已批准：43 行是异质观察，其中 27 行两端为 registry actor、16 行含 place／program／unknown recipient 等非 actor 端点；R8 27 行保持 case-role，不得生成“同案协作边”。实现依据为 `docs/actor_relation_architecture_v1.md`。
7. HR-033 已完成并合并：标准化的 6 条 dyadic relations＋1 条 aggregate observation 在 `outputs/hr033_integration_v1/`；前端不得把 membership 当 funding，也不得把 R10R029 的 102,000 美元附到 F025。
8. 类型化关系与 L0/L1 前端已按冻结后数据重生：已核 14 dyadic／6 administrative／2 aggregate／4 event records／27 case roles；研究层 8 dyadic／5 administrative／4 leads。中央关系记录 F036 只作事件记录，R10R029 只作汇总观察。22项 adapter tests、5项 R10 renderer tests 和7项 R1/R2 current-gate tests 通过；五页在1280×900与390×844浏览器复验通过、控制台零错误。全仓124项历史套件仍有19 failures／5 errors，集中在冻结前计数、H1/H2/H3快照、pre-human HR-034 builder 与旧报告 SHA。不得为通过旧断言回退中央数据。中央已有5条可导出 lifecycle 记录（4条为本轮新决定），但 L2 adapter 仍导出0锚点，须作为前端结构缺口修复。
9. NR-04／NR-05 分别做两个时期的有界线上补缺；结果先进入候选和人工队列。NR-06 统一完成 claim/evidence QA、历史集成决定和已核／研究双层验收。
10. 既有 HR／报告 gate 保持有效；只有当其直接阻断前端默认 claim 时才按优先级处理，不恢复全面铺开。
11. 2026-07-20 选题波次第一轮已完成并经交叉审计收紧：H1 只支持 E3/E4 actor–issue 可见层的来源依赖，三源效应约 84% 由 S004 单源驱动，source／actor 删除不是匹配反事实；H2 得到 9 个服务侧 registry 子集与 65 个问责侧候选（18 人审锚点／47 候选锚点），限定小样本中未编码直接跨组组织关系，人物与完整 recipient 均未测；H3 建立 12 条观察、6 条事件级载体和 17 条参与候选，只支持接触／承载路径，传播方向、独立采用、词汇增长与持续共同动员均未确认。三包均 `not_frontend_ready`；统一 JSON 只是模块目录索引，状态 `module_index_ready_observation_exports_gated`。负责人证据阅读关见 `outputs/research_wave_topic_selection_v1/principal_checkpoint_v1.md`。
12. H2 当前线上 P0 已形成 `outputs/research_wave_h2_service_universe_v1/`：完整保存 MCIPAC 页面显示的 82 个 PO（81 active／1 inactive，但目录跨 Okinawa／Fuji／Iwakuni且不是 NGO census），提出 4 个高价值服务侧 actor 候选、2 个结构 defer，整理 55 条公开人物—职务—时间观察、10 组人物 crosswalk、9/9 服务侧立场检索、18/18 问责侧反向接口检索和 6 条一般福利接口候选。当前候选修正为“服务／慈善可进入一般福利—行政 NPO，但在有界公开语料中尚未观察到与基地问责倡议的直接组织接口”；人物共享、完整 recipient、历史机制和所有新增身份／关系仍待人审，中央表与前端均未改。
13. 前端 actor–issue 已按冻结后 `125/158/283` 正式重生，build `5ed5528a649de4d1`。HR-035 Batch 1 已合并，HR-010 新增46条人审边；剩余候选边不因 schema freeze 自动升级。旧 `docs/frontend_actor_issue_state_handoff_v1.md` 仅是冻结前交代。
14. 冻结后线上补强按 `docs/post_freeze_online_enrichment_plan_v1.md` 执行；前端专用任务见 `docs/post_freeze_frontend_tasks_v1.md`。先修 LC001–LC005 的 L2 导出与5张冻结图，再做 NR-05、转译负案例；H2/H3 的资料工作可由两个 session 并行，负责人解释检查点分别进行。HR-035 Batch 2 尚未正式派发。
