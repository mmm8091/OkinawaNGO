# research_wave_h1_documentation_visibility_v1

独立、可复算的 H1 研究外挂包。它不修改中央 registry、source、edge、前端或现有 robustness 包。

## 复现

```powershell
python scripts\make_h1_documentation_visibility_v1.py
python -m unittest tests.test_make_h1_documentation_visibility_v1
```

## 输入

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/24_r01_r02_actor_issue_layered_v0.csv`

## 输出

- `actor_source_incidence_v1.csv`：registry source-ref token 展开；角色未知不推断。
- `actor_issue_edge_source_incidence_v1.csv`：E3/E4 actor–issue edge×support-token 下钻。
- `source_host_mapping_proposals_v1.csv`：S003/S004/S006 与 A005/A004/A001 的研究配对提案。
- `actor_visibility_diagnostics_v1.csv`：每 actor 的引用／议题机械计数；capacity 与 lifecycle 均未知。
- `sensitivity_scenarios_v1.csv`：current gate、source-support deletion 与 actor-node deletion。
- `scenario_removed_edges_v1.csv`：四个 source scenario 逐边删除明细。
- `leave_one_source_out_v1.csv`：所有 source ID 在相同单源删除单位下的分布。
- `paired_deletion_comparison_v1.csv`：四组不同单位的描述性对照；不是匹配反事实。
- `further_research_queue_v1.csv`：6 项未闭合验证任务。
- `metrics_v1.json`：机器可读指标、输入 hash 与解释边界。
- `brief_v1.md`：研究解释。
- `validation_report.md`：构建门禁。

## 状态

全包固定为：

- `research_status=research_only`
- `display_tier=research`
- `claim_status=candidate`
- `review_status=ai_seeded`

不得进入已核视图。source 删除表示当前编码支持被耗尽，不表示真实组织或社会关系消失。
