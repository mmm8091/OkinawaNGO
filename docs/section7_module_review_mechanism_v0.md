# 第7节：模块核查机制 v0

本文件用于替代原方案第7节中较概括的“模块核查机制”，形成真正可执行的核查表。

## 1. 核查目的

每个模块进入正式项目之前，都必须先做小样本核查。核查的目的不是证明模块“理论上有价值”，而是判断：

1. 是否能找到公开资料。
2. 是否能稳定抽取 actor、issue、place、event、action、target、source。
3. 是否能形成可复核的 CSV / Excel 表。
4. 是否能形成图表或分析段落。
5. 是否值得进入轻量版、标准一期或扩展版。

## 2. 核查样本要求

每个模块先找 10-20 条高质量资料。资料可以包括：

- 官方资料。
- 组织官网。
- 共同声明。
- 新闻报道。
- 诉讼 / 法律材料。
- 行政资料。
- 国际倡议资料。
- 学术或研究资料。

每条资料都必须进入 `source_log`，至少记录 URL、标题、年份、source_type、可支持模块、可抽取字段和偏差说明。

## 3. 模块核查表字段

建议核查表字段如下：

| 字段 | 说明 |
|---|---|
| module_id | B0 / R1 / R2 等 |
| module_name | 模块名称 |
| core_question | 该模块回答什么问题 |
| sample_sources | 已探查的代表性资料 |
| source_access | open_web / database_needed / archive_needed / fieldwork_needed |
| extraction_stability | high / medium / low |
| actor_extractable | yes / partial / no |
| issue_extractable | yes / partial / no |
| place_extractable | yes / partial / no |
| action_extractable | yes / partial / no |
| evidence_quality | high / medium / low |
| visualization_value | high / medium / low |
| research_value | high / medium / low |
| difficulty | low / medium / high |
| main_bias | 主要偏差 |
| recommended_package | must_do / standard_core / standard_sample / background / extension / long_term |
| decision | up / keep / down / exclude |
| reason | 决策理由 |
| next_step | 若进入项目，下一步做什么 |

## 4. 判定规则

### 上调优先级

满足以下条件时上调：

- 资料公开且稳定。
- 可抽取字段清楚。
- 能直接回答核心问题。
- 能形成图表或案例说明。
- 可用 AI / 代码辅助清洗和可视化。

### 保持优先级

满足以下条件时保持：

- 有资料，但需要人工判断。
- 可形成样本，不适合全量。
- 对核心问题有帮助，但不是主轴。

### 下调优先级

满足以下条件时下调：

- 需要馆内数据库、付费数据库、档案或访谈。
- 资料碎片化。
- 很难稳定抽字段。
- 可能涉及隐私或名誉风险。
- 容易偏离项目核心问题。

### 排除或长期化

满足以下条件时放到长期：

- 需要完整历史档案。
- 需要大规模媒体数据库。
- 需要人物访谈。
- 不能用公开资料充分验证。
- 工期显著超过标准一期。

## 5. 本轮核查后的模块分层

### 必做质控 / 底座

- B0 基础数据底座
- R14 资料覆盖与偏差审计

### 标准一期核心

- R1 组织分类与组织生态
- R2 组织—议题网络
- R3 地点与空间分布，含与那国 / 先岛专题
- R4 环保 / 生活安全框架与军事设施争议
- R5 联盟 / 共同行动网络
- R11 跨国 / 国际倡议网络
- R7 场域与对象转移
- R10 法律 / 政策 / 环境程序渠道

### 背景 / 小样本连接

- R9 选举 / 县民投票与市民组织连接
- R8 公开资源 / 行政协作渠道

### 扩展 / 长期

- R6 媒体可见度与“谁在发声”
- R12 人物—组织互锁与关键经纪人
- R13 组织谱系与长期演变

## 6. 核查表使用方式

1. 每新增一个模块或子模块，先填核查表。
2. 核查表先填小样本，不等到全量数据完成。
3. 每个模块必须给出 up / keep / down / exclude 决策。
4. 决策直接反馈到第5节排序和第6节报价工期。
5. 每轮核查后生成一个版本号，如 `module_review_table_v1.csv`。

