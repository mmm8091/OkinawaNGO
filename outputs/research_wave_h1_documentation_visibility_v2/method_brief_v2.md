# H1 v2：资料留存与“观测中心性”到底重合多少

日期：2026-07-20

状态：**research_only / candidate / not_frontend_ready**

## 结论先行

当前材料不能确认、也不能否定“资料留存能力制造了网络中心”这个命题。它能确认的是：**来源、编码和审核过程共同塑造了当前可见层；不同 proxy 给出的方向并不一致。**

总 `linked_source_count` 与 active actor×issue 度数的 ρ=0.331、与 betweenness 的 ρ=0.215。但横轴把 actor×issue 本身的支持来源也算进去，所以这里只是 **construction diagnostic**，不能当作“资料能力→中心性”的检验。排除 9 个 legacy-token 来源未解析 actor 后，总来源相关为 0.313；改用 registry 身份层来源，度数相关为 0.257；再剔除 actor×issue 自身 support sources，相关变为 -0.138。betweenness 对应为 0.111 与 -0.193。

审核状态同样改变结果。在来源 crosswalk 可用的 actor 中，reviewed-only 65 边的 registry／outcome-excluded 相关为 0.525/0.282，candidate-only 173 边则为 -0.169/-0.330。reviewed-only 不是“更真实”的随机样本，而是当前人审顺序的产物。图 2 因此把 238 active、65 reviewed 和 173 candidate 明确拆开。

## 五种对象，不能再统称 network centrality

- `actor_issue_bipartite`：238 条输入观察；103 个可见 registry actor；238 actor×issue evidence rows (65 reviewed + 173 candidate); degree counts coded issue categories, not organizational relationships；总来源相关=0.331（construction diagnostic），outcome-excluded=-0.138
- `strict_same_source_triples`：312 条输入观察；85 个可见 registry actor；same-source actor–place–issue observations; not a network centrality measure；总来源相关=0.179（construction diagnostic），outcome-excluded=-0.268
- `event_hyperedge_incidence`：50 条输入观察；47 个可见 registry actor；human-checked event participation incidence; co-signing is an event hyperedge, not a stable alliance；总来源相关=0.057（construction diagnostic），outcome-excluded=-0.406
- `reviewed_typed_dyadic`：14 条输入观察；15 个可见 registry actor；14 reviewed typed organization relations; relation families retain their semantics and are not alliances by default；总来源相关=0.425（construction diagnostic），outcome-excluded=-0.177
- `accepted_case_role_incidence`：13 条输入观察；12 个可见 registry actor；accepted actor×case role incidence; role is case-specific and does not establish a durable organization tie；总来源相关=0.466（construction diagnostic），outcome-excluded=0.306

图 1 对每种对象先剔除该对象自身的 support sources，并排除 9 个来源 crosswalk 未解析 actor；各纵轴仍不合并。event 保持 hyperedge incidence，不做共同署名投影；case-role 也不投影成同案协作。

## 来源 crosswalk 缺口

共有 9 个 actor 保留 `X...` legacy token，不能自动映射成某条 `S...` source；其中 6 个因此显示为 0 条已解析 S-source。它们在 `unresolved_reference_audit_v2.csv` 单列，并从主要 proxy sensitivity 与配对中排除。**0 条已解析来源不等于现实中没有材料。**

以 registry 身份层来源定义 dense/thin，并排除上述 9 个 actor 后，粗分层匹配得到 12 对；dense actor 平均多 1.25 条 active actor×issue 边（7 高／5 同／0 低）。在已有 issue edge 的子集中为 10 对、平均差 0.70。该配对仍未控制年代、规模、真实活动量、议题显著性和地点，只是人工抽读队列，不是因果设计。

## 来源集中与 actor capacity 是两件不同的事

S004 的证据支持若被移除，当前 234 条 E3/E4 编码边中有 41 条会失去全部已列支持，25 个 actor 会失去该层全部边；S003/S004/S006 合计对应 49 条边、30 个 actor。这个结果描述的是**当前编码层对几份名单的依赖**，不是现实网络在删网页后消失。

删除 registry S-source 最多的 10 个 actor 会去掉 35 条 active 编码边；删除 actor×issue 度数最高的 10 个 actor 会去掉 43 条。两个 actor 集合并不相同；source-support deletion 与 actor-node deletion 也不是匹配反事实。来源 channel 的删除使用 `source_type` heuristic，图 3 已明确标注。

## 反例使简单单调命题不能成立

- registry 身份来源薄但 actor×issue 可见度高：A047（registry 1源／4议题）、A102（registry 1源／4议题）、A104（registry 1源／4议题）、A105（registry 1源／4议题）。
- registry 身份来源密但 actor×issue 度数不高：X016（registry 4源／1议题）、X004（registry 6源／2议题）、A002（registry 4源／2议题）、A008（registry 4源／2议题）。

这些反例只否定简单单调机制；不能说明资料留存不重要。organization-hosted trace 与议题度数的 construction-level ρ=0.046，英文标题痕迹为 -0.079，但前者不是 actor 自有官网，后者不是组织英文能力。**议题编码规则、研究范围和审核顺序都在塑造度数。**

## competing explanations

1. **制度生产文书**：诉讼、EIA、公投与正式行政程序本来就要求案号、意见书、判决或会议记录；文档多可能是真实制度角色的结果，而不是外生“保存能力”。
2. **播种来源内生性**：S004 等名单同时帮助发现 actor 并支持 issue 编码，来源数和网络度数共享建构过程。
3. **真实协调与留痕可能共存**：秘书处、律师或 Web team 既可能真实协调，也可能保存记录；不能把可见度全部扣成偏差。H3 若出现“秘书处＋Web team”同组织并存，只能作为下一轮机制例交叉核查，不能在本包中当作已证解释。
4. **范围和分类效应**：服务组织、公共机构、国际 NGO 与地方实行委员会被赋予的 issue taxonomy 宽度不同。
5. **审核选择效应**：65 条 reviewed edge 集中于最近优先复核的 actor，不是从 238 条 active edge 随机抽样。
6. **时间右删失**：linked source 的年份跨度不是 lifespan；当前 lifecycle 表只覆盖极少数 actor。

## 方法文献接口

- Shvydun（2025）在 113 个经验网络上比较不完整资料下的 centrality 稳健性，并明确指出：扰动策略应随网络性质与缺失类型调整，经验网络中的缺失通常不是随机的。本包因此不用随机删边代替实际缺失机制，而把 S004／来源 channel 的定向 support deletion 与 actor-node deletion 分开；但本包也没有复刻其 16 种 centrality 或 1,000 次扰动设计。DOI：<https://doi.org/10.1371/journal.pcsy.0000042>
- Mosca（2014）把线上社会运动研究的资料收集／归档、采样和线上—线下方法关系列为三个核心方法问题。本包据此只把 121 actors／295 sources 当作 purposive online working corpus；线上未见不等于线下不存在，早期通讯、地方报刊与组织内部材料仍须当地／馆藏补查。DOI：<https://doi.org/10.1093/acprof:oso/9780198719571.003.0016>

两篇文献只支持方法边界，不替本项目证明“真实中心性”或 documentation capacity。

## 目前不能说什么

- 不能说“网络中心性主要是信息留存能力”；
- 不能用总 linked-source 的 ρ=0.331 支持或反驳 H1，因为横轴含纵轴的证据；
- 不能把 reviewed-only 相关当作更接近真实网络；
- 不能把 legacy X-token 解析失败写成组织没有来源；
- 不能说删掉网页、律师或英文材料，现实组织网络就会断裂；
- 不能把 organization-hosted 来源说成 actor 自有官网；
- 不能把英文标题说成组织具有英文 staff capacity；
- 不能把 event 同场或 case 同案投影成稳定组织关系；
- 不能从当前 source-year span 推断组织寿命；
- 不能用 14 条 reviewed typed dyadic 样本概括整个冲绳组织关系结构。

## 可继续验证的最小下一步

若负责人希望把 H1 从方法附录升级为论文命题，下一轮不应再扩大 actor 数，而应先补 9 个 legacy-token crosswalk，再从 registry-proxy 匹配中人工冻结不超过 36 个 actor：自有官网／第三方 host、日英双语原文、staff／律师／秘书处／Web team、成立—终止日期、固定时间窗外部报道。只有这些字段被人工读过，documentation capacity 才能从 proxy 变成解释变量。
