# H1 v2：资料留存与“观测中心性”到底重合多少

日期：2026-07-20

状态：**research_only / candidate / not_frontend_ready**

## 结论先行

当前材料支持一个比原命题更窄、也更有方法价值的判断：

> 少数高承载名单会显著改变 actor×issue 可见层的大小；但组织层面的资料痕迹与 actor×issue 中心性只呈弱到中等的正相关，而且该关系在功能分层中方向不稳定。现有数据不支持“中心性主要是官网、英文能力或律师团队制造的资料幻象”。

在 121 个当前 actor 上，关联来源数与 actor×issue 度数的 Spearman ρ=0.331，与该二模图 betweenness 的 ρ=0.215。这说明两者有重叠，但远非一一对应。organization-hosted trace 与议题度数的 ρ=0.046；英文标题痕迹与议题度数的 ρ=-0.079。后两项尤其不能支持“有官网／英文材料就会成为中心”的强说法；它们还只是 host/title 代理，不是 actor 自有官网或语言能力。

## 五种对象，不能再统称 network centrality

- `actor_issue_bipartite`：238 条输入观察；103 个可见 registry actor；actor×issue evidence visibility; degree counts coded issue categories, not organizational relationships
- `strict_same_source_triples`：312 条输入观察；85 个可见 registry actor；same-source actor–place–issue observations; not a network centrality measure
- `event_hyperedge_incidence`：50 条输入观察；47 个可见 registry actor；human-checked event participation incidence; co-signing is an event hyperedge, not a stable alliance
- `reviewed_typed_dyadic`：14 条输入观察；15 个可见 registry actor；14 reviewed typed organization relations; relation families retain their semantics and are not alliances by default
- `accepted_case_role_incidence`：13 条输入观察；12 个可见 registry actor；accepted actor×case role incidence; role is case-specific and does not establish a durable organization tie

图 1 只把相同的 documentation-trace 横轴放在四种对象旁边；纵轴没有合并。event 仍以 hyperedge incidence 表示，不做共同署名 actor 投影。case-role 也不投影为同案协作。

## 组织层比较

- actor×issue：来源数—度数 ρ=0.331；来源数—betweenness ρ=0.215。
- event incidence：来源数—已核事件数 ρ=0.057；当前事件层高度受三份名单及案件记录的抽样边界影响。
- typed dyadic：来源数—已核类型化关系度数 ρ=0.425；这里只有 14 条目的性关系样本，不能概括冲绳组织关系总体。
- case-role：来源数—进入案件数 ρ=0.466。这很可能同时反映“法律场域真实产生更多正式文书”和“有程序角色的 actor 更容易被编码”，不是文档能力的独立效应。

精确分层匹配把 `dense_4plus` 与 `thin_0to1` actor 按 analysis family、local/nonlocal、法人／非正式猜测桶配对，再尽量匹配 registry evidence/review 状态。全 registry 得到 18 对，dense actor 平均多 1.06 条 actor×issue 边（10 对较高／7 对相同／1 对较低）；只看已有 issue edge 的 actor 后为 16 对、平均差 0.69（8/7/1）。差距收缩说明 registry 中尚未连边的 actor 会放大表面关联。该匹配没有控制组织年代、规模、实际活动量、议题显著性和地点，仍不是因果设计。

## 来源集中与 actor capacity 是两件不同的事

S004 单源删除会耗尽 41 条 E3/E4 actor×issue 边，并使 25 个 actor 失去该层全部边；删除 S003/S004/S006 合计耗尽 49 条边、30 个 actor。这仍是最强的、可复算的资料偏差证据，但它证明的是**研究设计对几份列表的依赖**。

删除“关联来源数最多的 10 个 actor”会去掉 33 条 active actor×issue 边；删除“actor×issue 度数最高的 10 个 actor”会去掉 43 条。两个 actor 集合并不相同。更重要的是，source-support deletion 与 actor-node deletion 的干预单位不同，图 3 分栏显示，不能写成匹配反事实。

## 反例使强命题不能成立

- 资料薄但 actor×issue 可见度高：A047（1源／4议题）、A102（1源／4议题）、A104（1源／4议题）、A007（1源／3议题）。
- 资料密但 actor×issue 度数不高：X006（5源／1议题）、X007（4源／1议题）、X013（4源／1议题）、X016（4源／1议题）。

这些反例不说明资料留存不重要；它们说明“更多资料痕迹 → 必然更中心”的单调机制不成立。比如有的组织只由一份资料支持，却在同一编码行上被赋予 3–4 个议题；也有服务／国际组织有较丰富的正式或英文材料，但一期问题只给它们 1–2 个功能议题。**议题编码规则和研究问题本身也在塑造度数。**

## competing explanations

1. **制度生产文书**：诉讼、EIA、公投与正式行政程序本来就要求案号、意见书、判决或会议记录；文档多可能是真实制度角色的结果，而不是外生“保存能力”。
2. **播种来源内生性**：S004 等名单同时帮助发现 actor 并支持 issue 编码，来源数和网络度数共享建构过程。
3. **真实协调与留痕可能共存**：秘书处、律师或 Web team 既可能真实协调，也可能保存记录；不能把可见度全部扣成偏差。H3 若出现“秘书处＋Web team”同组织并存，只能作为下一轮机制例交叉核查，不能在本包中当作已证解释。
4. **范围和分类效应**：服务组织、公共机构、国际 NGO 与地方实行委员会被赋予的 issue taxonomy 宽度不同。
5. **时间右删失**：linked source 的年份跨度不是 lifespan；当前 lifecycle 表只覆盖极少数 actor。

## 方法文献接口

- Shvydun（2025）在 113 个经验网络上比较不完整资料下的 centrality 稳健性，并明确指出：扰动策略应随网络性质与缺失类型调整，经验网络中的缺失通常不是随机的。本包因此不用随机删边代替实际缺失机制，而把 S004／来源 channel 的定向 support deletion 与 actor-node deletion 分开；但本包也没有复刻其 16 种 centrality 或 1,000 次扰动设计。DOI：<https://doi.org/10.1371/journal.pcsy.0000042>
- Mosca（2014）把线上社会运动研究的资料收集／归档、采样和线上—线下方法关系列为三个核心方法问题。本包据此只把 121 actors／295 sources 当作 purposive online working corpus；线上未见不等于线下不存在，早期通讯、地方报刊与组织内部材料仍须当地／馆藏补查。DOI：<https://doi.org/10.1093/acprof:oso/9780198719571.003.0016>

两篇文献只支持方法边界，不替本项目证明“真实中心性”或 documentation capacity。

## 目前不能说什么

- 不能说“网络中心性主要是信息留存能力”；
- 不能说删掉网页、律师或英文材料，现实组织网络就会断裂；
- 不能把 organization-hosted 来源说成 actor 自有官网；
- 不能把英文标题说成组织具有英文 staff capacity；
- 不能把 event 同场或 case 同案投影成稳定组织关系；
- 不能从当前 source-year span 推断组织寿命；
- 不能用 14 条 reviewed typed dyadic 样本概括整个冲绳组织关系结构。

## 可继续验证的最小下一步

若负责人希望把 H1 从“方法附录”升级为论文命题，下一轮不应再扩大 actor 数，而应对本包的 18 组 matched pairs 做人工字段冻结：actor 自有官网／非自有 host、日英双语原文、专职 staff、律师／秘书处支援、成立—终止日期、至少两个相同时间窗的外部报道。只有这些字段被人工读过，documentation capacity 才能从 proxy 变成可以讨论的解释变量。
