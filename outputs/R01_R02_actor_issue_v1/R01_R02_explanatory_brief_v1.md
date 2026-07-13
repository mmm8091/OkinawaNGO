
# R1/R2 解释性验收 brief v1

## 验收结论

按《复归后冲绳民间组织 / NGO 分类与议题网络一期研究方案》的原始标准，R1/R2 已从“桥梁组织示例图”推进为可验收的完整 v1 包：R1 有 118 个 actor 的分类审计、标准化分析映射和组织生态图；R2 有 118 actors × 26 issues 的完整二模网络、议题共现图、跨议题 actor 表和证据／时间范围分层。它仍是公开资料驱动的候选网络，不是冲绳组织总体名录，也不是稳定联盟图。

## Q1：冲绳有哪些相关民间组织？

当前 registry 有 118 个 actor，覆盖冲绳本地公民团体与 NPO、日本国内 NGO、国际倡议组织、法律网络、劳工／教育组织、女性／人权组织、基地社区服务与军属慈善、国际合作／公共外交项目，以及资助／赞助／公共机构节点。这个宽生态符合方案“不预设全部 actor 都是反基地阵营”的边界。

但“118”不是完成指标。17 个 actor 尚无正式 actor–issue edge：A073 琉球沖縄国際支援プログラム、A076 ジュゴン保護基金委員会（Save the Dugong Foundation）、A086 Turtle Island Restoration Network、A087 NPO法人世界版「平和の礎」を提案する会、A088 特定非営利活動法人沖縄平和協力センター、A089 沖縄県教職員組合、A090 沖縄県高等学校障害児学校教職員組合、A091 日本労働組合総連合会沖縄県連合会（連合沖縄）、A092 沖縄県労働組合総連合、A093 全日本自治団体労働組合沖縄県本部、A095 止めよう「自衛隊配備」宮古郡民の会、A096 宮古平和運動連絡協議会、A097 宮古島環境クラブ、A098 特定非営利活動法人宮古島海の環境ネットワーク、A099 有機フッ素化合物（PFAS）汚染から市民の生命を守る連絡会、A100 ミサイル配備から命を守るうるま市民の会、A101 沖縄・琉球弧の声を届ける会。其中多为最近扩入的宫古、劳工、女性、PFAS 和和平教育组织。它们已有 registry `issue_tags`，但这些标签不能自动当成 edge；必须逐条回到来源建立关系证据。因此，下一轮线上工作的第一优先级是补齐这 17 个现有 actor 的 edge-level evidence，而不是机械补到 120。

## Q2 / R1：这些组织如何分类？

R1 采用“两层分类”：registry 保留具体 `actor_class`，生态图另建 10 个 `analysis_family_v1` 功能层。这样既能显示组织生态，又不会把法人身份、行动形态和政治立场压成一个标签。

- 当前共有 25 个不同 `actor_class` 值，其中 6 个超出 `coding_schema_v0` 的建议词表，涉及 9 个 actor。它们不是自动错误，而是需要 HR-019 决定“扩充受控词”还是“映射到现有宽类”。
- “劳工／教育”“女性／人权／社区”作为独立分析层有解释价值，因为它们回答方案明确提出的组织类型问题；若直接并入 `local_civic_actor`，会丢失组织生态差异。
- 军属服务、慈善、公共外交和资助节点按实际功能单列，不推断亲基地或反基地立场。

## R2：哪些组织连接了哪些议题？

当前 actor–issue 表有 222 条 edge，连接 101 个 actor 与 26 个议题；另有 17 个 registry actor 在图中保留为孤立节点。按复核层，59 条已人审，163 条仍是候选。按解释范围，43 条暂归为长期组织定位／持续角色，40 条为制度／案件角色，74 条为事件性声明／署名／行动，65 条仍待判定。

这四层解决了旧 R2 的核心缺口：同一个 actor 同时出现于多个议题，并不自动证明它长期以这些议题为组织定位。`event_specific` 只能写成“公开参与某次声明／署名／行动”；`institutional_or_case_role` 只能写成“在某诉讼、服务或项目中承担公开角色”；只有来源支持使命、持续行动或组织目的时，才暂列 `organizational_positioning`。

当前共有 72 个 actor 在 edge 表中连接至少两个议题，但只有 16 个 actor 至少有两个议题在 edge 两侧均已人审，10 个可暂归为长期定位型 bridge。正文优先使用双侧人审者：

- A102 全国公害弁護団連絡会議：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A103 全国基地爆音訴訟原告団連絡会議：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A104 普天間基地爆音訴訟弁護団：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A105 日本YWCA：全部 4 个议题，双侧人审可用 4 个；positioning_bridge。
- A106 辺野古の海を土砂で埋めるな！首都圏連絡会：全部 4 个议题，双侧人审可用 4 个；event_only_bridge。
- A107 沖縄YWCA：全部 4 个议题，双侧人审可用 4 个；positioning_bridge。
- A108 沖縄を再び戦場にさせない県民の会：全部 4 个议题，双侧人审可用 4 个；positioning_bridge。
- A109 第4次嘉手納基地爆音差止訴訟弁護団：全部 4 个议题，双侧人审可用 4 个；case_or_institutional_bridge。
- A110 辺野古に基地を絶対つくらせない大阪行動：全部 4 个议题，双侧人审可用 4 个；mixed_candidate_bridge。
- A111 沖縄県女性団体連絡協議会：全部 4 个议题，双侧人审可用 4 个；mixed_candidate_bridge。
- A002 ジュゴン保護キャンペーンセンター（Save the Dugong Campaign Center）：全部 2 个议题，双侧人审可用 2 个；case_or_institutional_bridge。
- A008 NGO非戦ネット：全部 2 个议题，双侧人审可用 2 个；mixed_candidate_bridge。

## 议题转化的当前证据

共现最高的议题对如下。它们说明“同一 actor 的议题组合”，不表示 actor 之间结盟：

- `anti_base × peace`：12 个共享 actor，其中 3 个在两侧均已人审，4 个在两侧均有长期定位标记。
- `anti_base × Henoko`：9 个共享 actor，其中 3 个在两侧均已人审，1 个在两侧均有长期定位标记。
- `anti_base × biodiversity`：8 个共享 actor，其中 0 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `anti_base × legal`：8 个共享 actor，其中 3 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `anti_base × life_safety`：6 个共享 actor，其中 3 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `life_safety × legal`：6 个共享 actor，其中 4 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `life_safety × noise`：6 个共享 actor，其中 4 个在两侧均已人审，0 个在两侧均有长期定位标记。
- `legal × noise`：6 个共享 actor，其中 4 个在两侧均已人审，0 个在两侧均有长期定位标记。

目前最稳妥的总体解释是：反基地议题不是孤立存在，而是经由三种不同机制被转译。第一，环保／生物多样性与边野古、大浦湾等地点议题结合；第二，噪声、生活安全与法律程序通过原告团和律师网络结合；第三，和平、人权、地方自治与国际倡议通过声明、网络使命或制度渠道结合。三种机制的证据形态不同，不能合并成一个“联盟强度”指标。

## 明显缺口与继续补材料的标准

- **数据联接缺口**：17 个已登记 actor 没有 actor–issue edge。优先补来源摘录和 edge，不从 registry `issue_tags` 自动生成。
- **薄议题层**：当前 actor 数不超过 3 的议题为：groundwater(3)、health_risk(1)、referendum(3)、international_cooperation(3)、environment(2)、women(3)、human_rights(3)、solidarity(2)、anti_war(1)、mobilization(1)。薄层中若又没有双侧人审，不能承担核心叙事。
- **分类词表缺口**：6 个超出 schema 的 actor_class 术语和 2 个 `watchlist_only` 状态需 HR-019 决策。
- **时间范围缺口**：65 条 edge 仍无法从当前 `relation_basis` 稳妥区分长期／案件／事件；已全部进入 HR-019 scope queue。
- **历史覆盖缺口**：当前网络明显偏向可在线检索的近年行动、2010/2015/2020 联署和现存官网，不能据此描述 1972 年以来各时期的总体组织结构。

## Registry 扩样：数量从属于模块缺层

本包提出 9 个组织级候选，全部明确排除“一次性署名凑数”，且暂不计入 registry。7 个已有在线可核的持续组织／法人证据，但仍需找到与一期议题直接相连的 edge-level source；其余先解决组织身份或持续性。推荐顺序是：先激活现有 17 个孤立 actor，再对候选执行直接议题连接检索，最后才决定是否扩表。Registry 可以超过 120，也可以暂不超过；验收看的是新增 actor 是否补上 R1/R2 的解释层。

## 图件怎么读

1. `fig1_r01_actor_ecology.png`：回答“有哪些组织、如何分类”，同时显示来源层和 actor-level 人审量。
2. `fig2_r02_full_bipartite_network.png`：方案要求的完整组织—议题二模网络；保留全部 118 actors 和 26 issues。
3. `fig3_r02_issue_cooccurrence.png`：显示同一 actor 连接的议题对，并单列双侧人审计数。
4. `fig4_r02_cross_issue_actors.png`：把 bridge 拆为长期定位、制度／案件、事件性和待判定四种机制。
