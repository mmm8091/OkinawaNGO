# OkinawaNGO

冲绳民间组织 / NGO 分类与议题网络一期研究仓库。

本仓库用于保存研究方案、阶段工作文档、数据底座、脚本、可视化输出和多代理协作说明。

## 1. 项目定位

当前一期定位：

> 以公开资料为基础，建立可复核、可扩展的冲绳民间组织 / NGO 分类底库与重点议题网络原型，并支持研究报告和课程论文写作。

一期不承诺：

- 1972 年以来全量 NGO 网络。
- 冲绳所有 NPO 法人全量名录。
- 完整媒体可见度。
- 完整人物互锁网络。
- 完整组织谱系。

一期当前工作重点：

- actor registry 初版。
- source log 初版。
- 组织分类、议题分类、地点分类。
- 组织-议题、组织-地点候选关系。
- 外来 NGO、军属服务组织、公共外交 / 资助关系作为观察层。
- 边野古国际倡议、石垣 / 宫古生活安全、与那国 / 先岛前线化专题。
- 证据分级、人工复核和当地材料收集机制。

## 2. 先读文件

协作代理或新成员应按这个顺序读：

1. `AGENTS.md`
2. `CLAUDE.md`
3. `docs/phase1_workbench.md`
4. `data/metadata/coding_schema_v0.md`
5. `docs/human_review_tasks_v0.md`
6. `docs/local_retrieval_tasks_v0.md`
7. `docs/human_decision_tasks_v0.md`
8. `docs/progress_sync_assets_v0.md`

## 3. 目录结构

```text
/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── CONTEXT.md
├── source_docs/
│   ├── current/      # 当前最新版方案
│   └── archive/      # 旧版方案归档
├── docs/             # 审计、报价、交付逻辑、模块核查等工作文档
│   ├── agents/        # agent / Claude / issue-tracker 配置
│   ├── module_audits/
│   └── archive_working/
├── data/
│   ├── interim/       # 当前阶段 CSV 数据底座
│   └── metadata/      # 字段与编码规则
├── outputs/           # 可视化和阶段输出
└── scripts/           # 生成图表和处理数据的脚本
```

## 4. 当前数据状态

截至 2026-07-01 当前工作台与 `data/interim` 实表：

- actor 初版：93 条。
- source log 初版：92 条。
- source log 当前 URL 状态：76 条真实 URL、14 条 `inferred_url` 占位符、2 条非 URL 参考。
- actor-issue 候选边：180 条。
- actor-place 候选边：124 条。
- support/funding sample edge：27 条。
- issue taxonomy：19 个一级议题。
- place registry：20 个地点 / 场域节点。

人工复核优先对象：

- P1：6 个。
- P2：17 个。
- P3：10 个。

主要数据文件：

- `data/interim/01_actor_registry_initial_v0.csv`
- `data/interim/02_actor_aliases_initial_v0.csv`
- `data/interim/05_source_log_initial_v0.csv`
- `data/interim/07_actor_issue_edges_initial_v0.csv`
- `data/interim/08_actor_place_edges_initial_v0.csv`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`

解释性图表包：

- `outputs/explanatory_v0/`
- 5 张解释型 PNG：组织-议题桥接网络、地点-议题矩阵、边野古国际化路径、共同行动样本构成、证据缺口图。
- 配套 CSV 用于继续调查：`next_investigation_candidates.csv`、`actor_issue_bridge_nodes.csv` 等。

模块完成包：

- `outputs/module_completion_v0/`
- 覆盖 R2、R3/R4、R5、R11、R14。
- 含模块 brief、共同行动 event/participant 表、2020 OEJP/MMC 71 团体完整 participant 表、跨国路径节点表和下一步模块调查任务表。

来源备份：

- `source_docs/source_archive/source_archive_manifest.csv`
- 当前状态：74 archived、2 manual archived、14 skipped inferred URL、2 skipped non-URL reference、0 pending archive。

MT 任务状态：

- MT-001：2020 OEJP/MMC 71 团体抽取阶段基本完成，剩余 registry review。
- MT-002：真实 URL 来源归档第一轮基本完成。
- MT-003：25 条 inferred URL 中 11 条已回填并归档，剩余 14 条继续处理。

## 5. 当前方案文件

当前最新版方案：

- `source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案.md`
- `source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx`

旧版方案：

- `source_docs/archive/复归后冲绳民间组织 _ NGO 网络演变研究.docx`

## 6. 协作规则

- 候选关系不等于最终发现。
- 共同署名不等于稳定联盟。
- grant opportunity 不等于已获资助。
- 服务型 NGO 不自动归入反基地或亲基地阵营。
- 与那国专题主轴是前线化、地方自治、住民投票、台湾周边安全环境和健康 / 生活安全风险，不强行写成环保拒止案例。
- 工作台 `docs/phase1_workbench.md` 永远不能超过 300 行。

## 7. 模块核查

第5节模块菜单已逐项核查。正式索引：

- `docs/module_audits/module_audit_index_v0.md`

核心模块：

- B0 基础数据底座。
- R1 组织分类。
- R2 组织—议题网络。
- R3 地点与空间分布，含与那国 / 先岛专题。
- R4 环保 / 生活安全框架。
- R5 联盟 / 共同行动网络。
- R7 场域与对象转移。
- R10 法律 / 环境程序渠道。
- R11 跨国 / 国际倡议网络。
- R14 资料覆盖与偏差审计。

扩展模块：

- R6 媒体可见度。
- R12 人物—组织互锁。
- R13 组织谱系与长期演变。
