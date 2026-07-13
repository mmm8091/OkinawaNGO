# edge-isolated actor 在线补证 brief v1

## 取证快照（HR-013 前）

- 18/18 已逐项检索并形成可回溯结论。
- 17 个 actor 找到至少一条直接 actor–issue 候选，共 58 条；全部仍待人审，未写回主表。
- A073 `琉球沖縄国際支援プログラム` 在多轮日/英精确名称与变体检索中没有可核实体；现有 S033 只是泛化学术背景，不能证明身份。该对象标为 `online_exhausted_needs_local_or_registry_reconsideration`。
- A076/A086 的诉讼事实继承 HR-014 案件锚点，但“案件角色 → issue edge”的映射仍进入 HR-024，不能由 AI 自动批准。
- A087–A101 原本就在未完成 HR-010 的分类/新增边范围内，因此不重复编号：本包提供 `HR010_batch6_edge_evidence_addendum_v0.csv`。补证不等于 HR-010 已完成。

## HR-013 后当前队列

- HR-013 已将 A094 `沖縄県女性連合会` 判为一般妇人会并剔除；其 4 条候选边、2 条来源提案和 4 个 HR-010 addendum 项只保留为取证历史，不得回流 registry 或当前复核队列。
- 当前可用过滤层为 17 个保留对象、16 个有候选边的 actor、54 条候选边和 38 条来源；HR-010 batch 6 当前队列为 47 项，原 task/activation ID 不重排。
- 当前复核应使用 `post_hr013_*` 文件；HR-024 仍为 A073/A076/A086 的 8 项，不受 A094 处置影响。

## 薄议题得到的候选补强

- `groundwater`：3 条候选
- `health_risk`：1 条候选
- `environment`：5 条候选
- `women`：1 条候选
- `human_rights`：2 条候选
- `international_cooperation`：2 条候选
- `international_advocacy`：2 条候选
- `frontline_prevention`：2 条候选
- `Taiwan_contingency`：2 条候选

以上为 HR-013 前取证快照计数。groundwater 由 A095（部署地点水源担忧）、A097（持续地下水保全）和 A099（PFAS/饮用水）三种不同机制进入；health_risk 只由 A099 的调查/倡议进入，不能写成医学因果。HR-013 后 A094 的 women/environment 等候选不再进入当前队列；保留的 environment 候选来自 A097/A098/A099/A101，仍须区分一般环境定位、污染倡议与事件性环境程序。

## 强制解释边界

1. 所有候选仅是 actor–issue 连接，不是 actor–actor 联盟。
2. A076/A086 只确认 Dugong 案件角色，不外推其他案件或持续组织活动。
3. A088 是和平/国际合作机构，不因研究基地或安全保障而编码为反基地 actor。
4. A097/A098 的一般环境工作不自动连接军事部署。
5. A099 的污染来源与健康影响保持组织归属；edge 不认证因果。
6. A095/A100 的目标化、前线化与台湾有事情境是公开框架，不是预测事实。
7. A089 的边野古材料来自国头支部，本批未提出 A089–Henoko 正式 edge。

## 文件

- `data/interim/28_edge_activation_candidates_v1.csv`：58 条候选边及逐条来源/locator/边界。
- `source_evidence_crosswalk_v1.csv`：40 条来源，明确拆分 identity support 与 direct issue support。
- `actor_online_conclusions_v1.csv`：18/18 逐项结论。
- `online_search_log_v1.csv`：每个 actor 的查询、来源家族与线上结论。
- `HR024_edge_activation_review_v0.csv`：A073/A076/A086 的 8 项新问题，决定栏全空。
- `HR010_batch6_edge_evidence_addendum_v0.csv`：HR-013 前 51 条取证快照，决定栏全空，不再作为当前队列。
- `post_hr013_edge_activation_candidates_v1.csv`：当前 54 条候选边。
- `post_hr013_source_evidence_crosswalk_v1.csv`：当前 38 条来源提案。
- `post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv`：当前 47 项，决定栏全空。
- `post_hr013_disposition_v1.csv`：A094 的 HR-013 排除处置及受影响 ID。
- `post_hr013_validation_summary_v1.csv`：过滤层机械验收。
