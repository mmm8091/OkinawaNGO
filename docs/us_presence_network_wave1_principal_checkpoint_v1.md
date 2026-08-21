# 对美研究网络扩展：第一轮负责人检查点

日期：2026-08-19

状态：第一轮线上普查、四份正式人工任务及五项研究架构决定均已于 2026-08-21 完成；中央数据库与前端尚未写入

2026-08-21 交叉核查见 `docs/human_review_research_USN_architecture_checkpoint_v1.md`，正式决定见 `docs/human_review_return_USN_architecture_checkpoint_v1.md`。

## 现在得到的结构

当前 registry 有 17 个 `us_origin` actor。准确拆分是：

- 9 个驻军服务／军属慈善比较 actor；
- 6 个美国来源问责比较 actor；
- 2 个单列节点：X013 领馆公共外交项目、X014 NED 资助观察节点。

因此，“9 对 6”是两组 NGO／组织比较，不是全部 17 个美国来源节点的穷尽分类。

新主轴已经转成可入库的问题：

> 哪些人物、资源、服务、案件和组织结构提高了美国军事存在的问责成本；哪些维持了驻军社会及其地方接口；两类作用在哪里发生连接？

组织不固定贴“亲美／反美”标签。数据库记录具体行动和关系的作用，同一组织可以在不同时间承担不同功能。

## 第一轮实质结果

### 1. 121 个现行 actor 已有一张完整名录候选表

- 121 个有效 actor 全部入表，A072 历史合并记录已排除；
- 65 个找到官网、官方分支页、正式登记页或母组织页；
- 56 个本轮未确认正式页面；
- 17 个美国来源节点中 16 个有正式页面候选；
- 40 个页面批量区与25个冲突区均已完成决定：`accept 54 / revise 4 / defer 5 / reject 2`。

页面决定已经完成；正式目录 overlay 尚待受控集成。未来前端应首先回答“数据库到底收了谁、用户到哪里核查”，而不是一打开就看网络图。

### 2. 原来 43 条 support／funding 样本已经拆开

- 8 条资金资源；
- 4 条服务—受赠；
- 9 条组织隶属；
- 20 条行动—制度；
- 1 条机会线索；
- 1 条历史排除。

六项规则决定已经完成（`accept 5 / revise 1`），43行 crosswalk 尚未展开。这一步没有新增事实，只把观察单位归位；以后资金流、服务受赠、结构隶属和案件行动分别成图。

### 3. 驻军服务侧比现有九节点密得多

本轮筛出18条组织／项目观察；Marine Thrift Shop、Marine Gift Shop、Neighborhood Pantry、NIOSC 的 research-only actor 决定已完成，AER、AFAS 采用全国 actor＋冲绳 presence。另形成29条人物职务、14条资源流、16条 recipient 观察和38条来源提案。

最有价值的新线索是：

- KOSC FY2025 Schedule I 中有一条标作 AWWA 的 2,580 美元异常个人援助行；组织间精确 flow 已暂缓，等待底层 filing／crosswalk 补证；
- OESC 在 FY2025 申报对 AWWA 8,479 美元；
- NOSCO 同期列出十项奖学金承诺，合计 20,000 美元；
- Marine Thrift Shop 把旧货店收入和军属组织资源接到 AWWA、USO、学校 PTO、军属项目及日本侧福利机构。

现有九节点因此不再只是“服务组织清单”，而开始显出一条可追踪的资源中介链。

### 4. 六个问责 actor 不是同一种参与

- Earthjustice、CBD、TIRN 属于案件型问责网络；
- VFP-ROCK 是在地化的美国退伍军人反军事化节点；
- Friends of the Earth U.S. 有2015、2019两个离散冲绳事件；Pacific Environment 的冲绳材料仍主要停在2015。两者均未达到持续项目门槛。

新材料补出 11 条人物职务和 9 条案件／协调观察。VFP 官方材料支持 VFP-ROCK 的具名人物与吉川秀樹在 OEJP／SDCC 的点时职务桥；原 USAA005 的 A019 端点已撤回，改为 event-only 十区会端点或保留 raw label。Earthjustice FY2021 Form 990 的 USD 276,345.50 court-award amount 与 Judgment Fund USD 280,000 付款记录分别保留；差额与付款机制未闭合前，不生成 OSD→Earthjustice 简单资金边。

### 5. “合法化”已经变成一个可检验问题

服务侧材料中有 9 条组织或军方使用 `goodwill`、`friendship`、`bond`、`bridge`、`unity`、`community relationship` 的公开叙事。数据库另设 `community_mediation`，记录资源或服务实际跨过基地／军属组织—冲绳地方社会边界。当前可以同时展示：

- LEG0：服务和资源确实到达了哪些对象；
- LEG1：组织或军方怎样解释这些行动；
- LEG2：受益方、地方机构或独立媒体如何接受、转述、抵制或重释；
- LEG3：是否存在可重复、可比较的态度、行为或制度效果。

本轮正式 LC 行只有 LEG0、LEG1；定向检索出现了可另建的 LEG2 research-only 候选，LEG3 仍为零。下一步应主动找受赠机构回应、地方报道、访谈和态度研究，而不是继续只收军方宣传稿。

## 学术上能新增什么

18 项文献核查表明，议题多元化、基地家庭与社区服务、良邻活动、跨国环境问责都已有充分研究。本项目的增量不是再次证明它们存在，而是：

1. 在同一组织层资料中并列追踪“提高问责成本”与“维持驻军社会”两套机制；
2. 用人物—组织、资金—recipient、服务—受赠、组织—案件、结构隶属五层网络解释这些机制如何运作；
3. 把资源实际抵达、公开合法化话语、地方有界反应和态度／行为／制度效果拆成四个不同命题；
4. 对中心性做来源删除、无官网组织和未解析人物／recipient 的敏感性分析。

这比“NGO 把基地问题翻译成多种议题”更接近一篇有新材料和新方法的论文。

## 负责人决定

### A. 研究架构（5 项）

1. `accept`：作用附着于行动／关系，不新增 actor 级亲美／反美标签；
2. `revise`：采用 LEG0 服务／资源事实、LEG1 行动方叙事、LEG2 地方／受益方有界反应、LEG3 态度／行为／制度效果四级；
3. `revise`：将 17 个美国来源节点的 9 服务、6 问责、2 单列报告为 `USF-US-ORIGIN17-2026-08-19` 冻结基线，不把新批准 actor 自动加入旧分母；
4. `revise`：第一张人物网以 VFP-ROCK 具名人物及吉川秀樹连接 OEJP／SDCC 的点时职务为 tracer；USAA005 的 A019 错配已撤回，event-only coalition 留在行动／协调层；
5. `accept`：第一张资源网并列 AWWA／军属俱乐部、Marine Thrift Shop／recipient、Earthjustice／Dugong case，并保持 money、service-recipient、affiliation/channel 与 case-resource 分层，不把三者压成同一种 funding edge。

### B. 已完成的人工任务（实际执行顺序）

1. `docs/human_review_assignment_USN_service_ecology_v1.md`：13 项服务侧身份、金额、结构和 LEG0–LEG3 判断；
2. `docs/human_review_assignment_USN_accountability_v1.md`：9 项问责侧人物、案件资源和协调判断；
3. `docs/human_review_assignment_USN_actor_directory_v1.md`：65 个页面字段，其中 40 个可批量确认、25 个逐项判断；
4. `docs/human_review_assignment_USN_relation_retype_v1.md`：已完成 6 条分组决定，覆盖现有 43 行语义归位。

四份人工任务与五项架构决定均已回交。下一步先写受控集成设计、预期字段级 diff 和幂等测试方案；本次拍板不授权直接手改中央 CSV、publication adapter 或前端。

## 下一轮三个可独立 session

### USN-04 人物—组织—案件

完成 VFP-ROCK tracer 的人物同一性、职务时间和案件／行动节点，交一张时间感知二部图。

### USN-05 资源—中介—recipient

完成 AWWA／Marine Thrift Shop／USO 三条资源路径，保留金额、用途、年份、流动类型和未解析 recipient。

### USN-06 公共外交与合法化反应

把 NOFO、award、recipient、program、contract 分开查；同时为 LEG1 行动寻找地方受赠者和媒体的 LEG2 有界回应材料。

三条 session 都先生成 research-only 包，经过对应人工决定后才进入中央数据和前端。
