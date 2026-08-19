# 美国驻军社会服务／慈善侧：第一轮线上普查简报

状态：`research_only`。未改中央 actor、relation、source、person 或前端数据，不可直接写成结论。

## 这一轮回答什么

H2 只能说明：现有数据库里有 9 个服务侧核心组织，它们与问责侧没有已经编码的组织关系。但甲方现在问的是更具体的问题：这些组织由谁经营，钱从哪里来，给了谁，军方和组织又怎样解释这些服务。第一轮普查因此不再扩一张笼统的“组织关系网”，而是把四种对象拆开：组织身份、人物职务、资源流、受益机构；另把“友好／联系／共同体”的语言单列为话语观察。

## 数据增量

- 组织普查 18 条：现有 9 个核心节点、4 个高优先缺漏候选、2 个全国性救济组织的冲绳服务点、2 个 roster 身份线索和 1 个协调项目。
- 人物—组织—职务候选 29 条，均带年份或“当前页面观察日”。
- 资源流候选 14 条；受益对象观察 16 条。
- 服务/合法化观察 12 条，其中 L0 服务事实 3 条、L1 组织或军方叙事 9 条；L2 实际合法化效果 0 条。
- 新来源提案 38 条；负面检索 11 条；明确缺口 10 条；待负责人判断 13 项。

## 三条最值得继续追的线索

### 1. 现有九个组织低估了服务侧的组织和项目密度

MCIPAC/MCCS 当前页面列出 81 个 private-organization 条目，但这个名单同时覆盖冲绳、Camp Fuji 和 MCAS Iwakuni，不能直接说“冲绳有 81 个”。逐项筛查后，至少有四个与本题直接相关而未进入现有九节点：Marine Thrift Shop、Marine Gift Shop、Neighborhood Pantry–Camp Butler、NIOSC。前两者连接礼品店/旧货店收入、军属俱乐部和 AWWA；Pantry 把物资、志愿者和基地家庭连接起来；NIOSC 则补上北部、多军种配偶网络。

这一发现首先说明 registry 需要增加一层“服务组织/服务项目的范围审定”，还不能说明这些节点支持基地。

### 2. AWWA 不是唯一的“施予者”，更像军属俱乐部资金进入日美福利端点的中介层

当前 IRS-derived Schedule I 给出两笔可核的新候选：KOSC 在 FY2025 报告 AWWA 2,580 美元，OESC 在 FY2025 报告 AWWA 8,479 美元。NOSCO 同期列出 10 项奖学金承诺、合计 20,000 美元。Marine Thrift Shop 的组织页面和 2024 年军方报道又把 AWWA、USO、学校 PTO、儿童/青少年机构及日本侧福利对象串到同一条年度分配链上。

这使下一版数据库可以真正回答“谁的钱、经谁、给谁、做什么”：

`商店/企业 → 军属俱乐部或 USO → AWWA/直接受益机构 → 用途与年份`

但具体转账、umbrella membership、grant channel 和实物捐赠必须分开。AWWA 的完整 recipient 年表仍需 990/Schedule I、年报或内部记录，网上材料只能形成不完整样本。

资金表已经把币种和金额性质拆开：`currency` 统一记 `USD`，`amount_semantics` 另行说明它是原文确数、最低数、实物折价、汇总数还是承诺额。只有来源明确出现中介步骤时才建立 transaction chain；目前只有 Marine Thrift Shop→Lions Clubs 可编码为第一步，Lions 之后的具体机构未公开，因此不补造第二步。KOSC→AWWA 的 2,580 美元是一条新的 FY2025 flow 候选，历史 F025 继续作为有界关系保留，两者不互相覆盖。

### 3. “合法化”目前只做到话语机制，尚未做到社会效果

USO 与 AWWA 的材料持续出现 `goodwill`、`friendship`、`bond`、`bridge`、`unity`、`community relationship`。这些词不是我们替组织加的，而是来源中可定位的自我叙述。它们说明服务和公益活动被怎样包装成跨社区联系，也为“基地周边社会再生产如何被解释为公共价值”提供了可编码材料。

不过，这里必须守住三级边界：

- L0：服务、捐赠、项目和受益对象确实被记录；
- L1：组织或军方把它解释成友好、纽带、共同体；
- L2：当地受益者或公众因此更接受美国军事存在。

本轮只取得 L0 和 L1。L2 为 0，不能把慈善直接写成“替基地提供合法性”。要进入 L2，需要受益机构一侧的日文材料、地方报道、访谈、项目评估或态度资料，也要收集拒绝、冷淡或反向利用资源的反例。

## 证据结构

这轮有意保留三种来源的差别。

- **official/installation**：证明 roster 授权、办公室、服务点和制度位置；
- **IRS/Form 990**：证明报税年度的负责人、金额、用途类别和申报关系；
- **organization/military publicity**：证明组织怎样叙述活动，以及军方怎样公开呈现活动。

前两类仍需人审端点和年度。第三类可做 L1 话语证据，却不能充当当地民意或项目效果证据。

## 建议负责人先拍板的事项

1. Marine Thrift Shop 与 NIOSC 是否进入 service-side background actor；Marine Gift Shop 是否待 IRS 状态查清后再入。
2. Neighborhood Pantry 是独立 actor，还是 Marine Thrift Shop/CARES 下的 program node。
3. AER、AFAS 是否沿用 Red Cross/NMCRS 的做法，建为“全国组织＋冲绳服务 presence”，而不是冲绳本地 NGO。
4. KOSC→AWWA 2,580 美元、OESC→AWWA 8,479 美元是否送正式资金边复核。
5. 是否正式采用 L0/L1/L2 三层：前端和报告可以展示 L0、L1；L2 只有在受众证据出现后才开放。

## 下一轮

线上下一轮应优先做三件事：下载并逐页核对相关 Form 990/Schedule I；补 Marine Gift Shop、NIOSC、Pantry 的连续年份与治理结构；把 Marine Thrift Shop 英文 recipient 名称逐一对到日本侧法人/机构。当地任务则集中到 AWWA 年报/会议记录、日方受益机构的接收与使用记录，以及受益者如何理解这些资源。

具体候选、URL、locator、短摘录、日期、证据等级、claim status 和解释边界见 `outputs/us_presence_service_recon_v1/`。所有人工决定字段保持空白。

负责人可直接填写的 13 项任务见 `docs/human_review_assignment_USN_service_ecology_v1.md`；任务书只列证据、建议和允许决定，不替负责人作判断。
