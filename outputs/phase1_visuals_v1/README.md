# 一期核心可视化补图包 v1

日期：2026-07-12

本包补足一期现有 `explanatory_v0` / `module_completion_v0` 尚未充分回答的三个问题。它不是对既有图的替换，也不把候选关系升级为最终发现。

验收说明：本包是补图包，不代表对应 R1/R3/R10 模块已经完成，也不能替代原方案指定但仍缺失的完整组织—议题网络、与那国/先岛专题图和多维覆盖偏差图。权威状态见 `docs/phase1_scheme_acceptance_audit_v1.md`。

## 图件

1. `fig1_functional_ecology.png` — 组织功能生态（功能层 × 来源层）。回答 registry 中不同功能 actor 如何构成，并把军属服务、行政协作和公共外交观察层与倡议网络分开；A102-A106 使用 HR-010 人审分类，A087-A101 单列为“待人工分类”。配套 `functional_ecology_matrix.csv`。
2. `fig2_actor_place_matrix.png` — 组织—地点矩阵。直接显示哪些组织在关键地点的公开资料中出现，证据等级由圆点颜色与大小标注。配套 `actor_place_matrix_selected.csv`。
3. `fig3_support_service_layers_strict.png` — 严格 E3/E4 的支持、委托与服务分层图。仅保留 confirmed 类或明确的 `not_funding_relation`，排除 probable funding、NOFO/grant opportunity、E2 线索。配套 `support_relations_strict_e3e4.csv`。

## 审计表

- `visualization_audit.csv`：研究模块 → 现有图 → 缺口 → 建议／补图 → 报告段落。

审计结论：现有地点—议题矩阵、边野古国际化路径、桥接 actor 图与事件 repertoire 时间线应保留；不应为了数量再画一张静态“联盟网络”。R7/R8/R9 的进一步网络图需要更多跨事件、法律程序和参与者数据后再做。

## 共同证据边界

- actor–place 与 actor–issue 均为候选边，不是最终关系。
- 共同署名、共同要请、共同在场不等于稳定联盟。
- 服务组织按观察到的服务／慈善功能编码，不推断亲基地或反基地立场。
- grant opportunity／NOFO 不等于 award；`probable_funding` 不进入严格图。
- 与那国按前线／安全环境、地方自治、公投、台湾邻近和生命安全解释，不强行环保化。
- 所有图描述当前公开资料驱动样本，不代表复归后冲绳全部 NGO 的总体分布。

## 复现

```powershell
python scripts\make_phase1_visuals.py
```
