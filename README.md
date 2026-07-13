# OkinawaNGO

复归后冲绳民间组织 / NGO 分类与议题网络一期研究仓库。

本仓库保存研究方案、证据与编码数据、审计文档、生成脚本、可视化以及报告草稿。一期目标是在公开资料基础上，建立可复核、可扩展的组织分类底库与重点议题网络，并为研究报告和论文提供可追溯的数据底盘。

## 项目入口

项目状态变化较快，本 README 不另行维护 actor、source、边数量或 MT 进度。请以下列文档为准：

1. [`AGENTS.md`](AGENTS.md) — 唯一通用协作与操作入口。
2. [`docs/phase1_workbench.md`](docs/phase1_workbench.md) — 当前控制文档与下一步。
3. [`docs/phase1_scheme_acceptance_audit_v1.md`](docs/phase1_scheme_acceptance_audit_v1.md) — 对原始一期方案的权威验收审计。
4. [`docs/phase1_research_report_v0.md`](docs/phase1_research_report_v0.md) — 内部研究报告草稿。

原始一期方案位于 `source_docs/current/`，字段与证据分级见 `data/metadata/coding_schema_v0.md`。

## 目录

- `source_docs/`：原始方案、来源归档与历史文档。
- `docs/`：工作台、验收审计、复核任务与研究文稿。
- `data/interim/`：当前阶段的结构化数据。
- `data/metadata/`：编码方案与字段规则。
- `outputs/`：模块数据、审计包、图表与报告组装资产。
- `scripts/`：数据处理、验证和生成脚本。

## 常用命令

```powershell
python scripts\archive_sources.py
python scripts\make_explanatory_graph_package.py
python scripts\make_module_completion_package.py
python scripts\make_phase1_visuals.py
python scripts\audit_report_claims_v1.py
python scripts\validate_phase1_data.py
```

运行脚本前先阅读 `AGENTS.md` 中的证据边界、生成顺序与写入规则。
