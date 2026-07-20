# H2 当前基地社区服务／慈善组织宇宙：P0 线上审计

日期：2026-07-20
范围：`research_only`，不修改中央 registry、关系表或前端。

## 最小闭环

MCIPAC/MCCS 的现行 Private Organizations 页面标注更新于 2026-07-07，页面表格实际列出 82 个实体，其中 81 个 `ACTIVE`、1 个 `INACTIVE`。页面同时说明：

- 这些组织是获书面许可在 MCIPAC 设施活动的 self-sustaining non-federal entities；
- 它们受 MCIPAC 监管，但 **不隶属于 MCCS**；
- 总体范围还包括 Camp Fuji 与 MCAS Iwakuni，且 USO、American Red Cross、NMCRS 等服务机构并不在该 PO 表中。

因此这张表只能作为“当前获准活动的 private-organization 宇宙”，不能当作冲绳基地社区服务组织的完整普查。

## 对 H2 的直接增量

现有 registry 九个服务侧 actor 不是 census。官方目录中只有 AWWA（X004）与 MOSCO（X016）可直接匹配；筛选产生四个高价值缺口：

1. `Marine Thrift Shop Okinawa`：独立董事会、旧货再销售、免费制服、奖学金和拨款；自有页面还明确称其为 AWWA member/contributor。建议 `add`，AWWA 接口另行人审。
2. `Neighborhood Pantry - Camp Butler`：2023 年形成、Foster 与 Kinser 多点食品／生活资源支持。建议 `add`。
3. `North Island Okinawa Spouses' Club`：现行全军种、全军衔配偶网络，公开使命含 philanthropy 与军属／冲绳社区支持。建议 `add`。
4. `Okinawa Global Military Lactation Community DBA Mom2Mom`：官方 PO 名单与 Global MilCom 的 Okinawa chapter 可相互指向，形成专业化健康支持节点。建议 `add`，但须先决定“本地 PO＝全球组织章节”还是两个关联 actor。

`Marine Gift Shop` 暂缓：现行目录把它单列为 PO，但历史治理材料把它写成 MOSCO 的 entity，直接入表会造成双计。`Helping Japan International` 只有 official-active 身份，本轮未找到足以确认现行使命的第一方页面，也暂缓。

## P0 三路检索已经闭合

本包不只做了目录筛选，还完成了三个可以复算的在线切面：

- `public_person_roles_v1.csv`：55 条公开人物—职务—时间观察，覆盖 9 个既有
  service-core actor 中的 8 个；ACGO 留作有检索记录的 `no_person_record_found`。
- `person_crosswalk_candidates_v1.csv`：10 组同名、近似名、年度衔接或同组织名称变体候选。
  其中 Trinicia Kloepper、Amber Tracy 等跨组织匹配具有较高核查价值，但全部仍需人审，
  不能生成 person node 或组织关系边。
- `service_stance_search_v1.csv`：9 个 service-core actor 均完成日英双语
  “组织名×辺野古／普天間／嘉手納／PFAS／反基地／和平／基地政策”检索；在该检索语料中
  未找到组织正式基地政策立场。这个结果只能写成 `searched-corpus not found`，不能写成
  “没有政治立场”“亲基地”或“非政治”。
- `accountability_reverse_interface_search_v1.csv`：18 个具有人审锚点议题边的问责侧 actor
  均完成对 USO／AWWA／spouse club／charity／donation／board／staff／recipient 的反向
  精确名称检索；未找到可直接编码的组织接口。人物与完整 recipient overlap 不在该查询的
  测量范围内。

## 最重要的新修正：不是两个封闭世界，而是选择性通透的三层

`welfare_interface_candidates_v1.csv` 给出了六条服务侧进入冲绳一般福利领域的正面观察。
其中，AWWA 在 2014 年和 2018 年均被认定 NPO 法人アンビシャス的自有材料记录为设备或
项目捐赠者；后者又以两个名称表记出现在冲绳县 2024 年度 NPO 协作来源总体的 8 行中，
涉及委托、补助、委员会、事业协力和讲师等机制。AWWA 对市町村社会福祉協議会及沖縄
ダルク的公开支持记录也指向同一边界。

因此，当前更有解释力的比较不是“美军相关组织与冲绳社会完全隔绝”，而是：

1. **基地问责倡议层**：环境、噪音、健康、自治、法律和反前线化；
2. **驻军照护／慈善层**：军属互助、应急、贷款、配偶社交、筹资和 grantmaking；
3. **一般福利／行政 NPO 层**：残障、难病、康复、社会福祉与地方行政协作。

当前公开资料显示第 2 层可以通过捐赠、设备和福利项目进入第 3 层，而第 1—2 层之间在
本轮对称检索中仍没有可编码的直接组织接口。最值得继续检验的问题因而变成：

> 为什么军属慈善能够跨越基地社区边界进入冲绳福利领域，却没有以同样方式进入基地损害、
> 环境责任和地方自治倡议？

这是一项 `candidate interpretation`，不是已冻结结论。完整 recipient 年表、问责侧人物
名册、非公开接触和历史切片仍未测量。

## 人物层的初步结构

六个配偶俱乐部／慈善组织的 IRS 年度名单显示明显的领导轮换，同时也留下少数可能的内部
骨架：

- Trinicia Kloepper 在 KOSC 与 AWWA 出现；
- Amber Tracy 在 OESC 与 AWWA 相邻年度出现；
- Sylvia Black 在 AWWA 多个非连续年度担任 Interpreter／Cultural Liaison；
- 另有近似拼写和姓氏变化候选，必须保留为未决身份。

这说明服务生态内部的人员网络可以在线恢复一部分，但不能据此推出其与问责侧存在或不存在
共享人员。年度报表年份也不是精确任期。

## 形成机制与竞争解释

`formation_mechanism_candidates_v1.csv` 将当前可检验机制拆开：

- AWWA 的 1952 前身可能是冲绳女性与美国女性共同参与的福利组织，1972 年后才重组为以
  军属配偶俱乐部为中心的联合体；该谱系仍需档案二源。
- OESC 在 2008 年从 Kadena enlisted-spouse club 扩为全岛、跨军种组织，公开叙事指向
  驻外生活中的归属、互助和福利缺口。
- service／accountability 的零接口可能来自真实任务边界，也可能来自英语军事服务资料与
  日语运动／法律资料的渠道分裂、registry 选择边界和军属轮换。
- 82 行目录构成必要分母，但其中大量是学校、职业、文体、兄弟会或单位协会，不能全部称为
  NGO，也不能全部纳入 H2 核心。

## 目前最重要的方法修正

H2 服务侧不能再只画成“九个组织”。更稳妥的层级是：

1. **正式服务提供者**：USO、Red Cross、NMCRS；
2. **配偶俱乐部与 AWWA umbrella**；
3. **筹资／拨款基础设施**：Marine Thrift Shop、Marine Gift Shop 等；
4. **需求型服务组织**：Neighborhood Pantry、Mom2Mom／Global MilCom；
5. **外围社会资本组织**：NIOSC、Leadership Seminar、scouting 等。

这说明“第二套生态”内部也不是一类组织，而是服务、筹资、分配、互助和社会联结多个功能层。该结构目前是候选分析，不能进入已核图。

## 未完成队列

- 82 行目录已完成候选功能初筛；下一步只对 4 个高价值候选与 2 个 defer 项补身份二源，
  不把机器初筛当作人审分类。
- 取得 Kadena、Navy、Army 当前 private-organization 完整名录；本轮官方网页检索未发现公开 roster。
- 对四个 `add` 建立身份二源、成立年、负责人／董事、年度活动和 recipient 记录。
- 对 Marine Gift Shop—MOSCO、Marine Thrift Shop—AWWA、Pantry—MTS 做组织结构与事件关系人审。
- 对 Helping Japan International 补 IRS／Form 990、官网或持续活动记录。
- 对 10 组人物 crosswalk 逐项人审，并以相同方法建立问责侧公开人物—组织—时间表。
- 将完整 AWWA／KOSC／NOSCO／OESC／MOSCO recipient 表与 121 个有效 actor、S002 616 行
  来源总体做同规则 crosswalk。

## 强制边界

- `ACTIVE` 只表示目录时点获准活动，不表示活动强度、持续经营或 MCCS 隶属。
- 服务、慈善、军属互助不自动产生亲基地、反基地或“非政治”立场。
- recipient、共同志愿者、同场活动和共享地点均不自动产生稳定组织关系。
- 精确名称检索未返回接口，只是有边界的公开语料结果，不证明没有人员、非公开接触或历史关系。
- IRS／ProPublica 年度 officer 名单是年度观察，不是精确任期；同名不等于同一人。
- AWWA—一般福利机构的具名支持观察不自动变成持续 funding edge，也不证明 recipient 的
  基地政策立场。
- 本包不新增 actor ID，不批准 funding edge，不进入探索前端。
