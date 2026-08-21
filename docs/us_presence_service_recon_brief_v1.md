# 美国驻军社会服务／慈善侧：第一轮线上普查简报

状态：`research_only`。未改中央 actor、relation、source、person 或前端数据，不可直接写成结论。

## 这一轮回答什么

H2 只能说明：现有数据库里有 9 个服务侧核心组织，它们与问责侧没有已经编码的组织关系。但甲方现在问的是更具体的问题：这些组织由谁经营，钱从哪里来，给了谁，军方和组织又怎样解释这些服务。第一轮普查因此不再扩一张笼统的“组织关系网”，而是把四种对象拆开：组织身份、人物职务、资源流、受益机构；另把“友好／联系／共同体”的语言单列为话语观察。

## 数据增量

- 组织普查 18 条：现有 9 个核心节点、4 个高优先缺漏候选、2 个全国性救济组织的冲绳服务点、2 个 roster 身份线索和 1 个协调项目。
- 人物—组织—职务候选 29 条，均带年份或“当前页面观察日”。
- 资源流候选 14 条；受益对象观察 16 条。
- 服务／合法化观察12条，其中 LEG0 服务事实3条、LEG1 组织或军方叙事9条；LEG2 需另建有界反应候选，LEG3 效果证据为0。
- 新来源提案38条；负面检索11条；明确缺口10条；负责人13项决定已完成，仍未中央合并。

## 三条最值得继续追的线索

### 1. 现有九个组织低估了服务侧的组织和项目密度

MCIPAC/MCCS 当前页面列出 81 个 private-organization 条目，但这个名单同时覆盖冲绳、Camp Fuji 和 MCAS Iwakuni，不能直接说“冲绳有 81 个”。逐项筛查后，至少有四个与本题直接相关而未进入现有九节点：Marine Thrift Shop、Marine Gift Shop、Neighborhood Pantry–Camp Butler、NIOSC。前两者连接礼品店/旧货店收入、军属俱乐部和 AWWA；Pantry 把物资、志愿者和基地家庭连接起来；NIOSC 则补上北部、多军种配偶网络。

这一发现首先说明 registry 需要增加一层“服务组织/服务项目的范围审定”，还不能说明这些节点支持基地。

### 2. AWWA 不是唯一的“施予者”，更像军属俱乐部资金进入日美福利端点的中介层

当前底层申报核查把两笔候选分开处理：KOSC FY2025 的 USD 2,580 位于异常的个人援助表且缺组织 recipient 字段，已暂缓精确 flow；OESC FY2025 的 USD 8,479 由官方 XML 明确给出 AWWA EIN、金额和期间，已接受为有期申报 flow。NOSCO 同期列出10项奖学金承诺、合计 USD 20,000。Marine Thrift Shop 的组织页面和2024年军方报道又把 AWWA、USO、学校 PTO、儿童／青少年机构及日本侧福利对象串到同一条年度分配链上。

这使下一版数据库可以真正回答“谁的钱、经谁、给谁、做什么”：

`商店/企业 → 军属俱乐部或 USO → AWWA/直接受益机构 → 用途与年份`

但具体转账、umbrella membership、grant channel 和实物捐赠必须分开。AWWA 的完整 recipient 年表仍需 990/Schedule I、年报或内部记录，网上材料只能形成不完整样本。

资金表已经把币种和金额性质拆开：`currency` 统一记 `USD`，`amount_semantics` 另行说明它是原文确数、最低数、实物折价、汇总数还是承诺额。只有来源明确出现中介步骤时才建立 transaction chain；目前只有 Marine Thrift Shop→Lions Clubs 可编码为第一步，Lions 之后的具体机构未公开，因此不补造第二步。KOSC 的 USD 2,580 只保留异常 filing 检索动作，历史 F025 不被覆盖。

### 3. “合法化”目前只做到话语机制，尚未做到社会效果

USO 与 AWWA 的材料持续出现 `goodwill`、`friendship`、`bond`、`bridge`、`unity`、`community relationship`。这些词不是我们替组织加的，而是来源中可定位的自我叙述。它们说明服务和公益活动被怎样包装成跨社区联系，也为“基地周边社会再生产如何被解释为公共价值”提供了可编码材料。

这里采用四级证据门：

- LEG0：服务、捐赠、项目和受益对象确实被记录；
- LEG1：组织或军方把它解释成友好、纽带、共同体；
- LEG2：受益方、地方机构或独立媒体出现可定位的接受、转述、抵制或重释；
- LEG3：重复、基线／比较或明确研究设计支持的态度、行为或制度效果。

本轮正式行只有 LEG0 和 LEG1；LEG2 可另建有界候选，LEG3 为0，不能把慈善直接写成“替基地提供合法性”。进入 LEG2 需要受益机构一侧的日文材料、地方报道或访谈并保留反向回应；进入 LEG3 还需明确效果设计。

## 证据结构

这轮有意保留三种来源的差别。

- **official/installation**：证明 roster 授权、办公室、服务点和制度位置；
- **IRS/Form 990**：证明报税年度的负责人、金额、用途类别和申报关系；
- **organization/military publicity**：证明组织怎样叙述活动，以及军方怎样公开呈现活动。

前两类仍需按获批字段受控整合。第三类可做 LEG1 话语证据，却不能充当当地民意或项目效果证据。

## 负责人决定摘要

1. MTS、Marine Gift Shop、Neighborhood Pantry、NIOSC 的 research-only actor 决定已完成；AER、AFAS 采用全国 actor＋冲绳 presence。
2. Helping Japan International 与 OAO Civilian Welfare Council 继续补第二来源；ACGO 保留 historical/current status unknown。
3. KOSC USD 2,580 暂缓；OESC USD 8,479 接受为有期申报 flow。
4. MTS—AWWA membership、渠道角色与年度金额分开；USO roster 只作2026-08-19快照。
5. 采用 LEG0–LEG3；现有材料不批准任何 LEG3 效果结论。

## 下一轮

线上下一轮应优先做三件事：下载并逐页核对相关 Form 990/Schedule I；补 Marine Gift Shop、NIOSC、Pantry 的连续年份与治理结构；把 Marine Thrift Shop 英文 recipient 名称逐一对到日本侧法人/机构。当地任务则集中到 AWWA 年报/会议记录、日方受益机构的接收与使用记录，以及受益者如何理解这些资源。

具体候选、URL、locator、短摘录、日期、证据等级、claim status 和解释边界见 `outputs/us_presence_service_recon_v1/`。13项决定已回填；正式结果见 `docs/human_review_return_USN_service_ecology_v1.md`。中央整合与发布仍未执行。
