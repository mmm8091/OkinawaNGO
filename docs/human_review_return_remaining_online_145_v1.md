# 剩余在线人工复核整包回传与合并记录 v1

日期：2026-07-20

负责人：项目负责人

辅助整理与受控合并：Codex

状态：**145条全部确认并合并；12条当地材料任务继续开放**

## 1. 确认范围

项目负责人于 2026-07-20 确认
`docs/principal_human_review_master_return_2026-07-20_v1.md` 中的全部145条决定：

| 任务 | 条数 | 确认分布 |
|---|---:|---|
| HR-010 batch 6 | 47 | accept 46；defer 1 |
| LCR001–004 | 4 | accept_status 1；revise_status 3 |
| HR-034 | 50 | revise 49；reject 1 |
| HR-029 | 41 | accept 28；revise 13 |
| HR-031 | 3 | B 3 |
| **合计** | **145** | **全部负责人确认** |

五张任务表的 reviewer 已统一改为 `project_principal_user`，日期为 2026-07-20。
确认仅覆盖任务表列明的事实、字段和解释边界，不批准稳定联盟、资金关系、因果链或未写明的
组织连续性。

## 2. 合并前一致性勘误

总审核包中 HR029-020 的原辅助说明误把 P004 建议为 `Futenma Air Station`，会与既有
P010 `MCAS Futenma` 重复，并违反该行自身的强制边界。合并前按任务原始语义作一致性勘误：

- P004：`Futenma`，`type=site`，`parent=P018`，aliases=`Futenma;普天間`；
- P010：继续作为 `MCAS Futenma` 实体基地层；
- 地域／议题层与实体军事设施层不因名称近似合并。

该勘误修复审核包内部矛盾，不新增组织、地点关系或解释性结论。

## 3. 中央事实合并结果

### HR-035 Batch 1

此前已确认的15条案件／公投／制度程序事实一并合并：

- accept 6；
- revise 8；
- reject 1（AI178）。

AI178 已成为 `rejected/unsupported/excluded` 历史行；沖縄防衛局的行政实施者／争议对象角色
不得转写成反基地立场。其余14条按各自 approved formulation、source、evidence level 和
interpretation limit 冻结。

### HR-010 batch 6

- 46条接受项新增为 AI249–AI294；
- 中央 source ID 由38个 package-local `EA-S*` URL 精确回连；
- HR010-B6-019 维持 defer，没有生成中央 edge；
- 新增边全部为 `human_checked/supported_bounded`，并保留 positioning、event 或
  institutional/case 范围。

### LCR001–004

生命周期继续保留在独立表，不塞进普通 actor `review_status`：

- A011：`dissolved`，2024-11-27；
- A068：`reorganized`，以 1997-10-18 作为后继 A019 成立／重组边界，不宣称精确解散决议日；
- A065：`continuity_unverified`，最后可见活动更新至 2023-06-01；
- A069：`continuity_unverified`，最后可见活动更新至 2015-06-22。

`continuity_unverified` 不等于解散或休止；A068 与 A019 不作实体合并。

### HR-034

- 45条 source-log legacy status 已按逐行决定迁移：44条 `ai_seeded`、S051 为 `rejected`；
- AI068 归 `ai_seeded`，同时继续排除于默认冲绳叙事；
- R4 的 `qa_safe_online` 已移到 `qa_usability_status`；
- R9 的 `accepted` 已移到 `formal_inclusion_status`，有明确 HR-017 决定的5行保留
  `human_checked/human_revised`，其余不冒充人审；
- heterogeneous repertoire 的49条 `accepted` 已移到
  `derivation_or_formal_inclusion_status`，法定 review status 为 `ai_seeded`；
- lifecycle 新增 `lifecycle_workflow_status`，实体生命周期结论与工作流状态分栏。

## 4. HR-029 schema／alias 冻结

在 HR-010、LCR 和 HR-034 合并后，按规定重新生成了一次505-candidate／41-item 快照，
41条负责人决定全部由稳定 ID 保留。随后完成中央冻结：

- 366个 actor 字段单元全部按受控映射核对；87个单元发生机械规范化；
- 39条 alias 全部进入受控类型；15条类型发生规范化；
- 21个 place 增加 `parent_place_id` 和查询 aliases；岛屿与市町不互作 alias；
- 18个 `R10_VENUE` 占位全部处理：12条映射到受控 venue，6条明确为
  `no_applicable_venue`；
- relation vocabulary 8处发生规范化；
- action vocabulary 217处发生规范化；
- `funding_contribution` 的 F025 冻结为 `donation`，金额仍为空，USD 102,000 不挂到该边；
- membership、NOFO、区域 sponsor perimeter 不再伪装成发生场所。

冻结只规范字段和受控词，不提升候选事实证据等级。

## 5. HR-031 报告措辞

三项均按负责人选择 B 应用：

1. “转译”降为当前公开样本中的分析框架；
2. 地点比较只写“当前公开材料呈现差异”，不写显著地点依赖；
3. 边野古／大浦湾国际化改为并列的可观察入口／角色，不写连续转换因果链。

`docs/phase1_research_report_v0.md` 的相关摘要、机制段和结论段已经改写。报告其他早期模块计数
仍须在正式 DOCX/PDF 装配时统一机械更新。

## 6. 合并后计数

- Actor registry：122条历史／121个有效 actor；
- Actor–issue：294条历史／283条有效；
- 有效 actor–issue：125条人审／158条候选；
- 已连接有效 actor：116；孤立有效 actor：5；
- Actor–place：135条历史／130条有效；
- Source log：295条；
- strict same-source place–issue：305条，其中298条 E3/E4、71条双边人审、97条有正式事件附着。

R1/R2、strict place–issue 和 coverage audit 已按新中央层重生；coverage 当前口径为
121 actors／283 actor–issue／130 actor–place／295 sources。

## 7. 可复现文件

- 合并脚本：`scripts/merge_confirmed_remaining_online_reviews_v1.py`
- HR-010 edge ID crosswalk：
  `outputs/principal_review_merge_v1/hr010_batch6_edge_id_crosswalk_v1.csv`
- 前置合并摘要：
  `outputs/principal_review_merge_v1/remaining_online_upstream_merge_summary_v1.csv`
- HR-029 freeze manifest：
  `outputs/schema_alias_freeze_v1/hr029_confirmed_freeze_manifest_v1.csv`
- HR-029 merge summary：
  `outputs/schema_alias_freeze_v1/hr029_central_merge_summary_v1.csv`
- HR-031 application：
  `outputs/report_claim_audit_v1/hr031_principal_application_v1.csv`
- 最终验证报告：
  `outputs/principal_review_merge_v1/remaining_online_merge_validation_v1.md`

前置合并与冻结阶段均已重复执行并比较中央文件 SHA-256；第二次执行未产生字节级变化，确认
合并脚本可安全重复运行。

## 8. 仍未关闭

正式未闭合人工任务只剩12条当地／新一手材料项：

- HR-017：9；
- HR-018：2（已有 defer 决定，等待新材料）；
- HR-024/A073：1。

HR-035 审计识别的后续 actor–issue 候选债务尚未正式派发，不自动计入这12条，也不因本次
整包确认而自动升级为已审事实。

## 9. 集成验证与技术债

已通过：

- 专用合并验证：PASS；
- `validate_phase1_data.py`：CSV、唯一 ID、外键和 evidence level 结构检查 PASS；
- 当前探索数据 adapter 在临时目录完整构建：PASS，283条有效 actor–issue 正确分为
  125条 reviewed／158条 research；
- adapter 当前契约测试：22/22 PASS；
- R10 current renderer：5/5 PASS；
- R1/R2 current gate：7/7 PASS；
- `git diff --check`：无空白错误；
- 工作台仍为244行，未超过300行硬限制。

HR-029 后另修复两项下游兼容：

1. 18条 actor–place 冗余地点标签已与冻结后的 place registry 同步，避免把53条已审地点边中
   的7条错误隔离为 label conflict；
2. exploration adapter 和 R10 current renderer 已识别
   `co_presence_observation`、`aggregate_financial_history_observation` 与
   `institutional_designation` 等冻结后受控词。

全仓 `unittest discover` 当前运行124项，结果为19 failures／5 errors。剩余失败均来自
冻结前／历史包的硬编码契约：238／248旧 actor–issue 计数、H1/H2/H3旧研究波次快照、
HR-034“生成空白任务”的 pre-human builder，以及 HR-018 前报告 SHA。根据 AGENTS 规则，
这些历史 builder 不得直接对当前合并层重跑。应另开一次测试迁移／历史 fixture 隔离维护，
不能为了让旧断言变绿而回退负责人决定或中央数据。

探索系统输出和当前未提交的界面改动本轮没有被覆盖；其 adapter 已兼容冻结词表，但正式
前端数据重生、五张冻结后图件重绘／QA 和最终 codebook/lint 仍是下游生产任务，不是未做的
人工决定。
