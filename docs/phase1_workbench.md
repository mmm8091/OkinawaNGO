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
- [x] 扩充 actor registry 到 90 条。
- [x] 扩充 source log 到 48 条。
- [x] 扩充 actor-issue edges 到 178 条。
- [x] 扩充 actor-place edges 到 122 条。
- [x] 扩充 funding/support edges 到 20 条。
- [x] 扩充 place registry 到 20 个地点。
- [x] 为高风险条目标注复核优先级（P1/P2/P3）。

阶段 C：人工复核与数据质量提升。

- [x] 定义人工复核任务书（HR-001 至 HR-009）。
- [x] 对 P1 条目进行第一轮 web 核实（AWWA/OESC/ヘリ基地反対協/イソバの会/石垣住民投票）。
- [ ] 对剩余 P1 条目进行人工复核（与那国改革会議/意見広告委、领馆项目 recipient、NED/USAID）。
- [ ] 补充来源日志中 URL 占位符条目（标记 inferred_url 的需核实）。
- [ ] 继续扩充 actor registry 到 120-150 条。
- [ ] 完成 P2 条目人工复核。
- [ ] 根据复核结果更新 evidence_level 和可发布措辞。

阶段 D：分析、可视化与进度沟通。

- [x] 生成第一次进度沟通图表（outputs/progress_sync_v0/）。
- [x] 起草第一版进度沟通稿（docs/progress_report_v1.md）。
- [ ] 更新可视化图表以反映扩充后的数据。
- [ ] 根据人工复核结果修订沟通稿。
- [ ] 准备组织-议题矩阵和组织-地点矩阵分析。

## 文件索引

- `docs/phase1_workbench.md`
- `docs/human_review_tasks_v0.md`
- `docs/local_retrieval_tasks_v0.md`
- `docs/human_decision_tasks_v0.md`
- `docs/progress_sync_assets_v0.md`
- `docs/progress_report_v1.md`
- `data/metadata/coding_schema_v0.md`
- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/03_issue_taxonomy_v0.csv`
- `data/interim/04_place_registry_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `outputs/progress_sync_v0/`

## 当前样本状态

- actor 初版：90 条（含冲绳本土 ~36、国内 NGO ~18、国际/美国 ~28、混合网络 ~3、制度节点 ~5）。
- funding/support edge 样本：22 条。
- actor_issue_edges 初版：178 条。
- actor_place_edges 初版：122 条。
- source log 初版：56 条（含 30+ 条已验证 URL、20+ 条占位符 URL 需核实）。
- issue taxonomy：19 个一级议题。
- place registry：20 个地点 / 场域节点。
- 第一次沟通素材：7 张 PNG 图（v0）、9 张 PNG 图（v1）。
- 第一版进度沟通稿已完成。
- 已完成第一轮 P1 web 核实：AWWA/OESC/ヘリ基地反対協/イソバの会/石垣住民投票。

## 任务索引

- 人工复核任务书：`docs/human_review_tasks_v0.md`
- 当地补查任务书：`docs/local_retrieval_tasks_v0.md`
- 人类决策任务书：`docs/human_decision_tasks_v0.md`
- 进度沟通稿：`docs/progress_report_v1.md`

当前人工复核优先级：与那国组织、军属服务/慈善网络、美国领馆 grant recipient、NED/USAID watchlist、2015 海外署名组织身份。

当前当地补查优先级：与那国早期反部署组织、军属配偶俱乐部慈善 recipient、外务省 / JICA / ONC 关系链。

当前人类决策状态：HD-001 至 HD-006 已决策完成；第一次沟通稿采用保守口径，不急派当地协作者。

## 问题抛出机制

目前不使用云表格；人工复核和当地补查都以任务书为准。

遇到以下情况，直接抛给人类确认：

- 公开资料显示"可能重要"，但缺少可复核来源。
- 资助 / 委托 / 赞助关系只有线索，没有 award、contract、财报或正式项目报告。
- 组织名、别名、法律身份或组织延续性无法确认。
- 需要当地数据库、图书馆、纸质资料、组织年报或当地联系人。
- 是否写入对外沟通稿存在政治或解释风险。

## 下一步

1. 对 P1 条目进行第一轮人工复核。
2. 补充来源日志中 URL 占位符条目。
3. 继续扩充 actor registry 到 120 条以上。
4. 更新可视化图表。
5. 整理当地材料收集需求。
