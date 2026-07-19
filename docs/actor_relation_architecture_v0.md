# 组织—组织关系呈现架构提案 v0

日期：2026-07-19
状态：已被 `docs/actor_relation_architecture_v1.md` 取代；不得作为实现依据
范围：NR-03 后续（前端呈现架构）；不改中央表，不改研究结论

## 1. 问题

一期前端目前只有"组织—议题生态图"，没有组织—组织关系。负责人决定：面板关系区与组织关系图都做，时间页的组织谱系一并设计。本提案回答三件事：

1. 现有数据能诚实支撑什么呈现；
2. 为什么按关系类型各自成层，而不是一张"组织关系网"；
3. 本期数据还能补多少，边界在哪。

## 2. 现有关系数据盘点

| 数据 | 量 | 人审状态 | 能否成为组织—组织边 |
|---|---|---|---|
| `15_funding_or_support_edges_sample_v0.csv` | 43 条样本边，24 种 relation_type | human_checked 11 + verified 6；ai_seeded 20；needs_second_source 4；needs_local 1；rejected 1；duplicate 1 | 可以，按类型分族；rejected/duplicate 不入任何层 |
| R8 法律角色（6 案 27 行） | 13 registry actor + 14 provisional 节点 | 全部 human_checked/accepted | 可以，作为"同案协作"（案件限定，不是联盟） |
| R5 共同行动（2010/2015/2020） | 169 参与观察，15 个严格重复 actor | human_checked | 只做面板级"反复共同行动"，永不上图（共同出现≠联盟） |
| R10 官方协作宇宙（S002 616 行） | 365 个机器标签 | HR-032 gate | 不能。标签不是 actor，crosswalk 未定 |
| 历史锚点（谱系） | 0 条 | — | 等 NR-04／NR-05 候选与人审 |

资助样本边的类型按语义强度归六族：

| 族 | relation_type | 方向性 | 演示门槛 |
|---|---|---|---|
| 资源与资助 | donation, sponsorship, grant, funding_contribution, in_kind_donation, co_in_kind_donation | 有向（谁给谁） | 官方记录（grant/award/contract/财报/组织报告） |
| 委托与服务 | commission, ngo_consultant_commission, service, site_presence | 有向 | 同上；project cost ≠ 合同付款 |
| 法律协作 | legal_counsel, legal_support | 案bounded | 案号与角色为准 |
| 结构隶属 | organizational_affiliation, network_membership, solidarity_branch | 无向 | 组织正式文件 |
| 协调与共同行动 | coordination, partnership, partner_action, administrative_collaboration, event_collaboration, event_affiliation | 弱 | 人审后才进演示层 |
| 线索 | grant_opportunity, co_presence_lead | — | 永不上图；grant opportunity ≠ 已资助 |

## 3. 为什么各自成层，而不是一张组织关系网

**第一，语义强度差一个数量级。** "AEC 赞助 USO（有 52 年官方记录）"和"两组织同场参会"若画成同一种边，就是把硬规则里"共同出现≠联盟"踩碎。分层让每类边只和同类边比。

**第二，证据门槛不同。** 资助层需要官方记录，隶属层是结构性事实，法律层以案号为准，协调层大多还在人审。各自的 demo gate 不同，就必须是各自可开关、各自有图例和计数的层——一张混图无法表达"这一层已过审、那一层还是候选"。

**第三，防止假中心。** 单图会被边野古周边的高可见度组织主导，让"资料保存得好"看起来是"影响力大"。本项目另有硬规则：来源密度≠活动强度。分层且不带度中心性编码，才守得住。

**第四，研究问题本来就是分的。** 谁给谁资源（资源流）、谁和谁有结构关系（隶属）、谁和谁同案（法律）、谁和谁协调（弱协作）——是四个不同问题，不该被一张图揉成一个答案。

## 4. 呈现架构（三层递进）

### L0 · 面板关系区（先做，NR-03.1）

组织详情面板新增"与其他组织的关系"区：

- 按六族分组；每行：方向箭头、对方组织（可点击跳转）、关系类型（三语）、证据等级、人审状态；
- 演示层只放 human_checked／verified 17 条；研究视图追加其余 26 条待审（含 4 条待二源、1 条待当地）；
- 线索类（grant_opportunity、co_presence_lead）仅在此区出现，明确标"线索，非资助事实"；
- 每行可下钻来源（证据抽屉，含 locator）。

数据要求：NR-02 契约把 43 条边以 `relation_edges` 纳入 `relations.json`（demo 17／research 26，rejected 与 duplicate 排除），构建脚本做 gate，不动中央表。

### L1 · 组织关系图（再议，NR-03.2）

组织页新增第三个图形状态："关系"（与"生态""议题连接"并列）：

- 默认三族可独立开关：资源与资助（实线、保方向箭头）、结构隶属（细实线、无向）、法律同案（虚线、带案号标签）；
- 协调族整层默认关（研究视图才可见，全虚线＋待审）；
- 布局按族分簇，不做全局力导向毛线球；节点大小与度数不编码；边粗细只对应证据等级，不对应金额或强度；
- 点击边显示：关系类型、依据、来源、人审状态，可进证据抽屉；
- 永不出现：同场参与边、grant opportunity 边、度数中心性、无类型"联盟边"。

### L2 · 组织谱系（NR-04／05 后启用）

时间页"组织谱系"带在锚点到达后启用，呈现为**泳道时间轴**而非网络图：

- 每条泳道一个组织谱系线；锚点按年份落在共享时间轴上，类型即 NR-04 任务书的 relation type：formed／renamed／split／merged／coalition_successor／issue_continuity／place_continuity／person_overlap_public／unknown；
- formed／renamed／split／merged 为实线连续；coalition_successor 为换轨虚线；issue／place／person 连续性为弱虚线，绝不连成"同一组织"；
- 候选锚点虚线框，人审后实心；每个锚点可下钻证据抽屉；
- 1972–1997／1998–2012 两个时段与现有时段节点共用轴；缺口继续显式显示，不用当前网络反推。

## 5. 本期数据还能补多少

- 可立即进包：43 条样本边（17 演示／26 研究）；R8 六案同案协作（27 行已全人审，无新数据需求）；R5 十五个严格重复 actor 仅作面板级"反复共同行动（非联盟）"。
- 本期补不了：R10 官方宇宙（365 标签等 HR-032 crosswalk）；AWWA recipient 年表（MT-005，需 Form 990／内部年报）；任何新资助边——没有官方记录就不画。
- 谱系数据：完全取决于 NR-04／NR-05 候选与人审；当前 0 锚点保持缺口显示。

## 6. 请主线程决定

1. 批准 NR-02 契约扩 `relation_edges`（43 条，demo gate = human_checked／verified，剔除 rejected／duplicate）。
2. 批准组织页"关系"状态的分层方案（三族默认层 + 协调族研究层；无中心性编码）。
3. 确认线索类（grant_opportunity／co_presence_lead）只在面板出现、永不上图。
4. 确认谱系泳道方案；NR-04／05 锚点未经人审不进该层。
5. R10 官方宇宙维持 HR-032 gate，本期不做 actor 化。

## 7. 明确不做

- 不做无类型组织关系网或"联盟图"；
- 不用同场参与、共同联署生成任何边；
- 不把 grant opportunity 写成已资助；
- 不以节点大小、度数、中心性暗示影响力；
- 不把 R10 机器标签当成组织。
