# H2 两套功能生态外挂研究包 v1

本目录是 `research_only`／`candidate_analysis` 包。它只读现有 registry、当前 actor–issue／actor–place、typed relations、案件角色、类型化事件和 R10 表，不修改中央数据，不进入探索前端，不批准政治立场、人物重叠或因果结论。

## 复现

```powershell
python scripts\make_h2_two_ecologies_v1.py
python -m unittest tests.test_make_h2_two_ecologies_v1
```

构建使用固定数据日期 `2026-07-20`，不写运行时间；相同输入应产生字节一致的输出。

## 文件

- `service_core_actors_v1.csv`：由 class＋origin 规则推导并断言的 9 个服务核心 actor。
- `accountability_comparison_actors_v1.csv`：由具体争议锚点议题机械选择的比较组。
- `issue_ecology_profile_v1.csv`：两组当前议题边构成。
- `dyadic_relation_ecology_audit_v1.csv`：14 条已核＋8 条候选 typed dyadic relation 的外挂分组。
- `case_role_ecology_audit_v1.csv`：27 条案件角色的外挂分组。
- `typed_event_ecology_audit_v1.csv`：类型化事件关系的外挂分组。
- `r10_interface_audit_v1.csv`：R10 目的性关系样本的外挂分组。
- `place_overlap_v1.csv`：同地点节点审计；同地不等于关系。
- `source_overlap_v1.csv`：议题边 source-ID 渠道审计；来源交集不等于社会联系。
- `coverage_gaps_v1.csv`：人物、recipient、立场、因果与历史覆盖缺口。
- `human_review_queue_v1.csv`：7 项空白人工决定。
- `further_search_queue_v1.csv`：线上／当地进一步检索任务。
- `metrics_v1.json`：机器可读计数与状态。
- `manifest.json`：输入 hash、行数、方法与输出清单。
- `H2_two_ecologies_brief_v1.md`：解释 brief。

## 强制边界

- “未观测到跨生态组织边”不是“不存在共享人员或社会联系”。
- 人物共享没有系统输入，状态只能是 `not_measured`，不能编码为零。
- 完整 recipient 网络没有取得，具名实例和 aggregate 不能补成全量。
- 服务／慈善功能不产生亲基地、反基地或非政治立场。
- “基地生产两套 NGO”仍是需要形成史、负案例与竞争解释的因果假设。
- 所有 CSV 行都带 `package_scope=research_only` 和 `frontend_eligibility=excluded_research_only`。
