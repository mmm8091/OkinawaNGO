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
- 已建立 125 条 actor-place 候选／人审关系。
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

## 12. 2026-07-13 主线程状态更新

前述第 1–11 节保留为第一次/第二次同步时的历史快照，不再用于判断当前内部进度。当前数据为 118 个组织级 actors、295 sources、222 actor–issue 候选/人审边、129 actor–place 边、43 funding/support/non-funding relation 样本边；另有 49 条正式 evidence note、67 条 actor–event–venue、6 案 R8 case registry 和 27 条人审角色。HR-011–15 已回写；HR-013 新增 A111，HR-010 范围修正移出 A094，净数仍为 118。S248–S294 为 47 条 provisional、`ai_seeded` 新来源，40 archived、7 failed；S295 是 HR-011 定位补充。来源入表不批准候选关系或解释。

当前推进原则已经纠偏：先按原始 DOCX 完成三个基础问题、基础建设、R1–R11、指定核心图和最终交付的线上可做部分，再派当地协作者。当前报告和补图只是 v0，不代表一期收口。验收总表见 `docs/phase1_scheme_acceptance_audit_v1.md`。

Registry 必须满足原方案 120–180 的一期范围；当前仍少 2。HR-027 已把宮古島地下水研究会、宜野湾ちゅら水会、全日本港湾労働組合沖縄地方本部和新日本婦人の会沖縄県本部送交人工决定；若至少两项按模块价值获准即可达到 120。八重山大地会因持续性缺口 defer。四项都未自动分 A 号；不得把旧 A077–A085、A094 或一般公益组织重新入表凑数。

下一轮对外沟通前，应优先形成：

1. R3 已覆盖 129/129 空间边并形成三地 dossier；41 项语义进入 HR-025。R9 三届选举候选层有 19 项 HR-026；R5/R7 已将 148 条观察形成 39 个去重行动单元，不新增事实。
2. Registry 四候选进入 HR-027；schema／alias／place／venue／relation／action 有 34 项 HR-029。顺序必须是先完成 HR-027，再重生并冻结 schema；AP123 只由 HR-025 决定。
3. R10 已完成 S002 86 页／616 行官方来源总体、公开资源类型表和两张 `ready_now` 图；365 个机器标签不是 actor。8 项 HR-032 只控制未来 canonical alias／JV／registry crosswalk，不阻断当前图。
4. 新来源 22 个 metadata/archive 问题进入 HR-030。报告 claim 审计已把 78 条主张分为可安全表述、需修订措辞和依赖 HR-018 的阻断项，32 组数字全部匹配，3 个研究解释强度问题进入 HR-031；共同出现、流程顺序和选举介入均不作稳定联盟或因果效果解释。
5. 正式报告装配蓝图建议 32 页：36 个逻辑图件中 14 个可直接用、13 个需人审冻结、9 个淘汰；正式汇报建议扩为 20 页，使 R6/R7、R9 公投/选举、R10/R11 不被压成同页。完成冻结后生成 DOCX/PDF、8k–12k 论文、PPT、先岛 dossier 与公开数据包；蓝图不计作合同成品。

## 13. 2026-07-14 学术／甲方红队更新

当前最严厉判断是：研究基础设施和线上模块底稿已经有明显价值，但今日仍不能提交一期验收，也还不是可投稿论文。正式整改清单见 `docs/phase1_academic_client_redteam_audit_v1.md`。

必须主动纠错：旧 `fig_place_issue_matrix_explanatory.png` 由 actor 层全部地点 × 全部议题的笛卡尔投影生成，已退役。正式 MA002 只能从同一 source／event／date 中可证的 actor-place-issue 三元事实重建。在重建完成前，原方案五类核心图只有四类具备可继续冻结的线上 v1。

下一次甲方同步不得静默替换第二次同步。`docs/third_sync_correction_ledger_v1.md` 已锁定四项明示更正：地点—议题旧图、桥梁强度、边野古“完整／唯一国际化”和“进度没有落后”。第三次同步应改为 findings-led：六项发现、六至八张可读图、五至七个验收 gate 和当地材料的具体解释增量。

当前正式人工派工为 `docs/human_review_assignment_HR027_v1.md`：四个 registry 候选由项目负责人决定，主线程不预填决定、不预分 A 号。HD-012 并行请求前期 1990–2022 知事选研究原文、数据、图表与参考文献；收到前不得写组织机制与票数／胜负／政策结果之间的关系。

## 14. 2026-07-16 HR-027 合并与研究图更新

HR-027 已由项目负责人完成 4/4 `add`，合并为 A112–A115。当前为 122 actors、295 sources、241 actor–issue 边、135 actor–place 边；17 个新增事件描述仍在候选包，中央 AEV 未增，组织关系边新增 0。S279 已重试归档成功；S272/S284 metadata 勘误仍等待 HR-030 或负责人明确批准。

依赖包已按 122-actor 快照重生：HR-019 为 9 条规则＋30 个 bridge＋76 条 scope，HR-025 为 47 项，HR-029 为 36 项；统一人工编排为 397 行、389 个决策，其中 HR-027 四项完成、385 项仍空白。

三项新研究输出已形成，但暂不急写同步稿：

1. `outputs/R03_strict_place_issue_v1/`：330 条同源 actor×place×issue 三元事实，323 条 E3/E4，67 条双边人审，100 条附着正式事件观察；旧宽投影只作上界敏感性对照。
2. `outputs/R02_actor_issue_robustness_v1/`：S003/S006 删除影响小，S004 删除使“生态→国际”桥由 8 降到 4；四个核心 A001/A002/A009/A046 在去三源后仍存活，完整人审层仅 2 个。
3. `outputs/translation_episode_comparison_v1/`：13 个“诉求→场域→中间产出→有限救济→底层改变”episode。已入选案例都能形成记录／判决／投票／行政回答或行动，但底层项目按诉求明确改变为 0；这是已进入场域案例的比较，不是总体成功率或因果结论。

下一步不是马上写稿，而是补未进入制度场域的负案例、做身份不确定性敏感性，并把地点三元事实继续收紧到 source×event×date 可发表层，同时将 TE10–TE13 和 HR-027 事件候选送事件级人工复核。

## 15. 2026-07-16 第三次进度同步包

甲方催交后已建立独立版本目录 `outputs/formal_comm_v1/`，不覆盖第一／二次同步历史文件。本轮按用户要求只交付 Markdown 和 PNG，不生成 PDF。

主文件：

- `第三次进度同步_v1.md`：短版甲方同步稿，按“主要进展—方法更新—一图一句发现—人工复核—下一步”组织。
- `fig/fig1_place_issue_evidence_v1.png`：330／323／67 的严格地点—议题证据图，明确旧宽投影已停用。
- `fig/fig2_actor_issue_robustness_v1.png`：候选跨议题组织在名单来源删除后的 8→4 敏感性，并单列人审层 2 个。
- `fig/fig3_repeat_participation_v1.png`：169 条参与记录、15 个重复组织、3 个贯穿三次。
- `fig/fig4_translation_results_v1.png`：8 个正式证据案例的程序产出与底层改变分层。

生成脚本：`scripts/make_third_progress_sync_package.py`。脚本读取既有正式输出、生成四张统一风格横版 PNG 和配套派生 CSV，并对所有主数字设置断言。

本次对外主线：样本已达到数量下限，研究从扩表进入证据收紧；在已经进入法律、行政或公投场域的目的性案例中，常见结果是形成可观察记录，但程序进入、有限救济和底层项目改变必须分开解释。

## 16. 2026-07-16 第三次同步 findings-led v2

用户认为 v1 仍偏方法审计、缺少“所以呢”的解释性价值。v1 不删除，降为方法／稳健性附录；当前老板沟通主版本改为 `outputs/formal_comm_v2/第三次进度同步_v2.md`。

v2 的六项解释性发现：

1. 三类物质争议进入不同制度语法：海洋新建工程→生态／国际程序，既有基地慢性损害→赔偿／差止诉讼，新部署／前线化→自治、公投、地下水、撤离与行政程序；
2. 制度常通过记录、承认或补偿吸收部分诉求，同时把工程否决、运行停止或行政拘束留在门外；
3. 公投是一条会被条例重新设计、议会阻断和行政再解释的门槛链，而不是单点政策输出；
4. 宫古—石垣—与那国可能形成“地下水—自治—前线化”三种地方问题化方式，但须用当地民间组织原始材料检验；
5. FY2024 官方协作 616 行显示公共服务型行政协作是更大的基线，基地／和平倡议只是特定功能层，不能把全部主体压成一张抗争网络；
6. 三次公开行动呈现“小型重复骨架＋事件性变动外围”：15 个确认组织至少重复一次、3 个贯穿三次，说明共同署名有连续性价值但不能直接当稳定联盟。

配套新图：`fig1_translation_mechanisms_v2.png`、`fig2_institutional_conversion_v2.png`、`fig3_referendum_gates_v2.png`、`fig4_sakishima_hypothesis_v2.png`、`fig5_official_civic_ecology_v2.png`、`fig6_event_reassembly_v2.png`。

当地任务书同步新增：T2-D 先岛三地民间原始表达对照（P0）、T2-E 公投制度门槛一手材料（P1）、T2-F 1972–2012 组织谱系（P2／仅在保留长期标题时启动）。

## 17. 2026-07-20 当前覆盖层

本节覆盖第 12–16 节中作为“当前状态”使用的旧计数；旧节继续保留为形成过程和沟通快照，不得据此回退中央数据。

- Registry 为 122 条历史记录／121 个有效 actor；A072 是并入 A071 的 tombstone，不进入普通搜索或当前图。
- Actor–issue 为294条历史／283条有效，当前有效层141人审＋142候选，116 connected＋5
  isolated；AI068与被 HR-035 否决的 AI178 排除于默认冲绳叙事。
- Actor–place 为 135 条历史／130 条有效（53 人审＋77 候选）／5 retired；AP123 已固定为 P007 Camp Foster。
- 严格地点—议题层已按有效边重生为306条，其中299条 E3/E4、81条双边人审、97条可附
  正式事件；旧330／323／67、312／305／65与305／298／71只属于早期快照。
- R5 的 169 条参与观察现分为 64 registry rows、22 human-reviewed event-only identities、83 other event-only names；严格重复身份为 15 registry＋6 human-reviewed event-only，重复参与仍不等于联盟。
- R9 公投正式层为 29 stages／29 roles；选举 19 条均已人审，18 条确认发生、1 条只确认预告。
- R10 目的性样本为 35 relations／28 amounts／43 functions；与 S002 616-row 官方来源总体保持分层。实际合同金额只有 5 条，project cost 不是付款。
- R10 与 R9 的审前图件技术欠账已清除：F008 现在把 16 条严格记录分成 7 dyadic／6 administrative／1 event／2 panel-only，F030 锁定 18 held＋1 announcement-only，F032 把 5 条 actual contract 与 14 条 project cost 分开；三图都不把记录数解释为联盟、选举效果或资金规模。
- Source archive 当前为 273 archived、2 manual、18 failed、2 non-URL；HR-030 已合并。
- R6/R7/R11 的六个 SVG/HTML 已按当前 80 条正式观察／53 条 R11 进入观察重绘；A066 县基地政策合同与 USO/service 分列，4 条 analytical seed 不进事实图。
- 六维 coverage 已按 121 个有效 actor、283 条有效 actor–issue、130 条有效 actor–place 和 295 条来源重生；中央历史边界为 122／294／135。当前 120 个 category cells 是生成结果，不是固定契约。
- HR-035 Batch 1／2、HR-010 batch 6、LCR001–004、HR-034、HR-029／031 均已确认并合并。当前线上空白人工决定为0；另有12条当地／新一手材料任务。当前总账见 `docs/principal_human_review_remaining_v19.md`。
- HR-029 数据冻结门已清除，HR-031 三项均采用保守 B；原5张 `freeze_required` 图仍须按冻结词表重绘／QA 后才能改为 ready。蓝图仍不等于正式 DOCX/PDF、论文或 PPT。
- 探索系统已按冻结后的 relation/place/actor–issue 词表正式重生，当前为141人审／142候选；
  13个 episode 的7类内容已形成中／日／英273格正式 overlay，TE10–TE13 保持研究层。
  26项 adapter、2项前端语言、5项 R10 renderer 和7项 R1/R2 gate 测试通过。五页已在1280×900与390×844
  复验，控制台零错误。中央已有5条可导出 lifecycle 记录，但时间页仍因 adapter 未导出而显示0个谱系锚点；
  这是下一轮结构缺口。全仓历史测试仍含冻结前快照断言，不能宣称全绿。

对外使用时，第二次同步仍是最后已经交付的历史客户快照；`outputs/formal_comm_v2/` 是第三次同步准备稿，最终 PDF 由项目负责人排版。OPI-00 仍暂停／未完成，在其完成前不启动新的广泛研究波次。
