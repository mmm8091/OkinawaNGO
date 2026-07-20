# research_wave_h1_documentation_visibility_v2

H1 第二轮独立研究包。它检验“观测中心性有多少与资料留存／索引痕迹重合”，但不把相关性写成因果。

## 复现

```powershell
python scripts\make_h1_documentation_visibility_v2.py
python -m unittest tests.test_make_h1_documentation_visibility_v2
```

## 关键输出

- `actor_documentation_visibility_v2.csv`：121 个 current actor 的资料痕迹和五类分开测量的可见度。
- `source_feature_audit_v2.csv`：295 sources 的机械 channel／title-language／archive 分类。
- `graph_object_summary_v2.csv`：actor×issue、strict triple、event hyperedge、typed dyadic、case-role 的对象边界。
- `association_estimates_v2.csv`：construction diagnostic 与 registry／outcome-excluded proxy 分栏。
- `review_layer_sensitivity_v2.csv`：238 active、65 reviewed、173 candidate 的审核层敏感性。
- `stratified_associations_v2.csv`：同一 actor×issue 图对象内、仅 n≥10 的 analysis-family 描述。
- `unresolved_reference_audit_v2.csv`：9 个 legacy X-token 来源 crosswalk 缺口。
- `matched_actor_pairs_v2.csv`、`matched_pair_summary_v2.csv`：以 registry 来源定义 dense/thin 的有界匹配。
- `negative_case_audit_v2.csv`：反驳简单单调机制的对照案例。
- `source_dependency_v2.csv`、`sensitivity_scenarios_v2.csv`：来源支持删除与 actor 节点删除，严格分栏。
- `method_literature_v2.csv`：两项方法文献接口及不可转移边界。
- 3 组 SVG／HTML 图。
- `method_brief_v2.md`、`principal_checkpoint_v2.md`、`validation_report_v2.md`。

## 固定边界

全包为 `research_only / candidate / ai_seeded / not_frontend_ready`。总 linked-source 相关只作 construction diagnostic；主要敏感性使用 registry-only／outcome-excluded proxy，并排除 9 个未解析 legacy-token actor。65 条 reviewed edge 与 173 条 candidate edge 不合并解释。organization-hosted trace 不等于 actor 自有官网；英文标题不等于组织英文能力；source-year span 不等于 lifespan；共同事件和同案角色不投影成稳定组织关系。
