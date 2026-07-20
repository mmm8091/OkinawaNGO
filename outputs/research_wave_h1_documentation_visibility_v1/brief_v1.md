# H1：高承载名单对 actor–issue 可见层的来源依赖 v1

日期：2026-07-20
状态：**research-only / candidate / not_frontend_ready**

## 当前可复算边界

- current gate：121 个有效 actor；`analysis_inclusion=active` 的 238 条 actor–issue 边。
- 敏感性 evidence gate：E3/E4，共 234 条边、101 个有边 actor。
- actor–source incidence：212 个 registry 引用 token，其中 204 个解析到 source log、8 个为显式 legacy unresolved token。
- E3/E4 的 234 条边中，有 12 条没有可解析的 `S` 来源（空值或仅非 `S` token），按保守规则不会被 source-ID 删除实验移除。
- 全来源 leave-one-out 覆盖 source log 和 E3/E4 边中的 source ID；其中 109 个 source ID 实际出现在该层。
- 所有 source-host 配对均为 `proposal_not_human_reviewed`；producer、self/external、source language 均保持 `unknown`。

## 成对删除结果

| 配对 | 删 source support：边 / 有边 actor | 删 actor node：边 / 有边 actor | 两种不匹配单位的 actor 差值 |
|---|---:|---:|---:|
| S003_A005 | 227 / 97 | 232 / 100 | 3 |
| S004_A004 | 193 / 76 | 232 / 100 | 24 |
| S006_A001 | 234 / 101 | 231 / 100 | -1 |
| BIG3 | 185 / 71 | 227 / 98 | 27 |

最强的单源敏感性来自 S004，在全来源 leave-one-out 中按删除边数列第 1：E3/E4 观测层由 234 边／101 个有边 actor 降至 193／76。三份来源同时删除造成 49 条边、30 个有边 actor 的损失，其中 S004 单独贡献 41 条边（83.7%）和 25 个 actor（83.3%）。因此当前效应主要是一份 2015 年高承载名单的来源集中，而不是三类组织反复呈现相同机制。

“删 source support”和“删 actor node”具有不同单位和最大影响范围：一份名单可以支撑几十个 actor–issue 编码，删除一个 actor 只能直接去掉该节点。上表只保留为描述性尺度对照，**不是匹配反事实**。

这支持的弱命题是：

> 当前 E3/E4 actor–issue 可见层对 S004 等高承载名单存在显著来源依赖；研究者看到的组织—议题覆盖会随少数列表材料的可得性明显收缩。

它不支持：

- 这些拟配对 actor 已被确认是材料作者、唯一生产者或真实协调中心；
- 三份材料共同证明“官网、律师或英文能力”反复制造中心性；
- 社会网络本身会因文件不可见而断裂；
- 官网、英文能力、律师或专职人员已经造成中心性；
- 资料较少的组织寿命更短。

## 辅助诊断

Registry 已解析 source-ref 数与 active issue degree 的 Spearman 为 0.284。这是两个项目编码量之间的机械相关，不是组织能力或社会中心性的因果估计。

## 替代解释

1. 专业组织可能真实承担协调角色，同时也更容易留下材料。
2. 法律、国际倡议和大型联署场域本身会强制或鼓励文档生产。
3. 当前样本由 2010／2015／2020 三份名单播种，存在研究设计内生性。
4. 组织规模、法人身份、年代和地点可能同时影响材料存续与可观察议题数。
5. 临时实行委员会可能按任务设计解散，不能等同于能力不足或短寿失败。

## 下一步验证门槛

需要完成 `further_research_queue_v1.csv`：先确认 producer/host 与材料类型，再用同单位、同覆盖度来源作比较；另补官网、人员／法律支援、语言和右删失生命周期字段。事件名单应继续作为 hyperedge，不投影成稳定联盟。

## 强制解释边界

Research-only sensitivity of documented actor-issue visibility; it does not establish social-network centrality, alliance, influence, activity strength, organizational lifespan, or a causal documentation effect.
