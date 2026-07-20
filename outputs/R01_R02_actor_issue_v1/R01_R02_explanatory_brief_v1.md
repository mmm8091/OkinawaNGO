
# R1/R2 解释性验收 brief v1

## 验收结论

按《复归后冲绳民间组织 / NGO 分类与议题网络一期研究方案》的原始标准，R1/R2 已从“桥梁组织示例图”推进为可验收的完整 v1 包。历史审计保留 122 个 registry rows 与 294 条 actor–issue rows；当前图表和统计只使用 121 个有效 actor 与 283 条有效 edge。R1 提供分类审计、标准化分析映射和组织生态图；R2 提供 121 active actors × 26 issues 的二模网络、议题共现图、跨议题 actor 表和证据／时间范围分层。它仍是公开资料驱动的候选网络，不是冲绳组织总体名录，也不是稳定联盟图。

## Q1：冲绳有哪些相关民间组织？

中央 registry 的历史底稿有 122 行，其中 121 个 actor 进入当前分析；1 行仅保留为历史审计：A072 沖縄から基地をなくし世界の平和を求める市民連絡会（merged_duplicate）。当前有效层覆盖冲绳本地公民团体与 NPO、日本国内 NGO、国际倡议组织、法律网络、劳工／教育组织、女性／人权组织、基地社区服务与军属慈善、国际合作／公共外交项目，以及资助／赞助／公共机构节点。这个宽生态符合方案“不预设全部 actor 都是反基地阵营”的边界。

数量不是完成指标。5 个有效 actor 尚无当前有效 actor–issue edge：X014 NED National Endowment for Democracy、X015 Peace Winds Japan、A054 沖縄人権協会、A073 琉球沖縄国際支援プログラム、A075 沖縄防衛局。它们已有 registry `issue_tags`，但这些标签不能自动当成 edge；必须逐条回到来源建立关系证据。已拒绝、停用或排除的 edge 不计入候选，也不能据此消除孤立状态。

## Q2 / R1：这些组织如何分类？

R1 采用“两层分类”：registry 保留具体 `actor_class`，生态图另建 10 个 `analysis_family_v1` 功能层。这样既能显示组织生态，又不会把法人身份、行动形态和政治立场压成一个标签。

- 当前有效层共有 21 个不同 `actor_class` 值，其中 0 个超出 `coding_schema_v0` 的建议词表，涉及 0 个有效 actor。`actor_class_controlled_mapping_v1.csv` 同时保留历史计数，避免把墓碑行重新带回生态图。
- “劳工／教育”“女性／人权／社区”作为独立分析层有解释价值，因为它们回答方案明确提出的组织类型问题；若直接并入 `local_civic_actor`，会丢失组织生态差异。
- 军属服务、慈善、公共外交和资助节点按实际功能单列，不推断亲基地或反基地立场。

## R2：哪些组织连接了哪些议题？

历史表保留 294 条 edge，其中 11 条因 `rejected`、`unsupported`、`excluded`、`retired_*`、`deactivated_*` 或默认叙事排除状态而不进入当前网络。当前有效层有 283 条 edge，连接 116 个 actor 与 26 个议题；另有 5 个有效 actor 在图中保留为孤立节点。按复核层，141 条已人审，142 条仍是候选。按解释范围，122 条暂归为长期组织定位／持续角色，62 条为制度／案件角色，99 条为事件性声明／署名／行动，0 条仍待判定。

这四层解决了旧 R2 的核心缺口：同一个 actor 同时出现于多个议题，并不自动证明它长期以这些议题为组织定位。`event_specific` 只能写成“公开参与某次声明／署名／行动”；`institutional_or_case_role` 只能写成“在某诉讼、服务或项目中承担公开角色”；只有来源支持使命、持续行动或组织目的时，才暂列 `organizational_positioning`。

当前共有 88 个 actor 在 edge 表中连接至少两个议题，但只有 41 个 actor 至少有两个议题在 edge 两侧均已人审，39 个可暂归为长期定位型 bridge。正文优先使用双侧人审者：

- A101 沖縄・琉球弧の声を届ける会：全部 7 个议题，双侧人审可用 7 个；positioning_bridge。
- A091 日本労働組合総連合会沖縄県連合会（連合沖縄）：全部 5 个议题，双侧人审可用 5 个；positioning_bridge。
- A100 ミサイル配備から命を守るうるま市民の会：全部 5 个议题，双侧人审可用 5 个；positioning_bridge。
- A114 全日本港湾労働組合沖縄地方本部：全部 5 个议题，双侧人审可用 4 个；positioning_bridge。
- A086 Turtle Island Restoration Network：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A095 止めよう「自衛隊配備」宮古郡民の会：全部 4 个议题，双侧人审可用 4 个；mixed_candidate_bridge。
- A099 有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会：全部 4 个议题，双侧人审可用 4 个；positioning_bridge。
- A102 全国公害弁護団連絡会議：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A103 全国基地爆音訴訟原告団連絡会議：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A104 普天間基地爆音訴訟弁護団：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A105 日本YWCA：全部 4 个议题，双侧人审可用 4 个；positioning_bridge。
- A106 辺野古の海を土砂で埋めるな！首都圏連絡会：全部 4 个议题，双侧人审可用 4 个；event_only_bridge。

## 议题转化的当前证据

共现最高的议题对如下。它们说明“同一 actor 的议题组合”，不表示 actor 之间结盟：

- `anti_base × peace`：16 个共享 actor，其中 7 个在两侧均已人审，9 个在两侧均有长期定位标记。
- `anti_base × Henoko`：10 个共享 actor，其中 4 个在两侧均已人审，4 个在两侧均有长期定位标记。
- `anti_base × biodiversity`：8 个共享 actor，其中 0 个在两侧均已人审，3 个在两侧均有长期定位标记。
- `anti_base × life_safety`：8 个共享 actor，其中 4 个在两侧均已人审，2 个在两侧均有长期定位标记。
- `anti_base × legal`：7 个共享 actor，其中 3 个在两侧均已人审，1 个在两侧均有长期定位标记。
- `life_safety × legal`：7 个共享 actor，其中 4 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `anti_military × life_safety`：6 个共享 actor，其中 3 个在两侧均已人审，2 个在两侧均有长期定位标记。
- `biodiversity × international_advocacy`：6 个共享 actor，其中 2 个在两侧均已人审，0 个在两侧均有长期定位标记。

目前最稳妥的总体解释是：反基地议题不是孤立存在，而是经由三种不同机制被转译。第一，环保／生物多样性与边野古、大浦湾等地点议题结合；第二，噪声、生活安全与法律程序通过原告团和律师网络结合；第三，和平、人权、地方自治与国际倡议通过声明、网络使命或制度渠道结合。三种机制的证据形态不同，不能合并成一个“联盟强度”指标。

## 明显缺口与继续补材料的标准

- **数据联接缺口**：5 个已登记 actor 没有 actor–issue edge。优先补来源摘录和 edge，不从 registry `issue_tags` 自动生成。
- **薄议题层**：当前 actor 数不超过 3 的议题为：health_risk(3)、public_diplomacy(2)、solidarity(2)。薄层中若又没有双侧人审，不能承担核心叙事。
- **分类与状态边界**：当前有效 actor 的 schema 外分类术语为 0 个；历史状态或范围排除项只保留在审计表，不进入当前生态与网络。HR-019 的既有人工决定原样保留。
- **时间范围缺口**：0 条 edge 仍无法从当前 `relation_basis` 稳妥区分长期／案件／事件；已全部进入 HR-019 scope queue。
- **历史覆盖缺口**：当前网络明显偏向可在线检索的近年行动、2010/2015/2020 联署和现存官网，不能据此描述 1972 年以来各时期的总体组织结构。

## Registry 扩样：数量从属于模块缺层

`registry_expansion_candidates_v1.csv` 现在是这批 **9 行历史候选的 HR-013 最终处置账**，不是仍待补入的核心候选清单。其中 1 行已并入 registry（C011→A111），2 行只作背景节点（C010／C034），5 行已因缺少一期直接连接而剔除（C029–C033），另有 1 行 C015 因组织身份与独立二源不足继续 defer。背景与 rejected 项都没有继续扩表任务，C015 也不是 count-ready actor；它只能在身份、持续性及与“宮古島地下水研究会”的关系厘清后重新提交人审。当前扩表决定应读取独立的价值门槛包，不能把本表九行重新解释成 active shortlist。

## 图件怎么读

1. `fig1_r01_actor_ecology.png`：回答“当前有哪些有效组织、如何分类”，同时显示来源层和 actor-level 人审量；历史墓碑不进入气泡计数。
2. `fig2_r02_full_bipartite_network.png`：方案要求的当前组织—议题二模网络；保留全部 121 个有效 actors 和 26 个 issues，排除历史失效边。
3. `fig3_r02_issue_cooccurrence.png`：显示同一 actor 连接的议题对，并单列双侧人审计数。
4. `fig4_r02_cross_issue_actors.png`：把 bridge 拆为长期定位、制度／案件、事件性和待判定四种机制。
