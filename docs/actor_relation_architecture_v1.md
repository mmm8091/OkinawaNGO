# 组织关系与证据状态呈现架构 v1

日期：2026-07-20  
状态：负责人批准；L0／L1 已实现，L2 等待历史锚点
替代：`docs/actor_relation_architecture_v0.md`  
状态规则：`data/metadata/coding_schema_v1.md`

## 1. 已批准的方向

- 不做一张混合的“组织关系网”；
- 组织面板关系区、组织关系图和谱系泳道分阶段实现；
- 已核视图允许显示证据不完整但边界明确的 `supported_bounded`；
- 研究视图显示候选与线索，但持续标注状态；
- 前端显示“确认了什么／缺什么”，不只显示 E3／E4；
- 用户界面把“演示视图”改名为“已核视图”。

## 2. 现有数据的正确盘点

`15_funding_or_support_edges_sample_v0.csv` 是 43 条异质关系／支持观察，不是 43 条
组织—组织边：

| 类型 | 数量 |
|---|---:|
| 两端均解析到 registry actor | 27 |
| 一端为 place／program／unknown recipient／临时机构标签 | 16 |
| 总计 | 43 |

HR-033 合并后的状态：

| 状态 | 数量 |
|---|---:|
| human_checked | 18 |
| human_revised | 8 |
| ai_seeded | 12 |
| needs_second_source | 2 |
| needs_local_retrieval | 2 |
| rejected | 1 |

六条 legacy `verified` 已全部由 HR-033 决定，旧值清零。这里的 26 条
`human_checked + human_revised` 只是中央行状态计数，不能直接写成“26 条已核组织关系”：
最终展示数量继续经过 endpoint、claim 和 graph eligibility gate。

当前构建读取 43 条中央观察，并另纳入 R10R029 一条独立汇总观察，共 44 条输入。gate 后
的集合为：

| 展示层 | 类型 | 数量 |
|---|---|---:|
| 已核 | dyadic relation | 14 |
| 已核 | administrative record | 6 |
| 已核 | aggregate observation | 2 |
| 已核 | typed event participation | 4 |
| 已核 | case role | 27 |
| 研究 | candidate dyadic relation | 8 |
| 研究 | administrative candidate | 5 |
| 研究 | relation lead | 4 |

行政记录、汇总观察、事件参与和 case role 均不得计作组织—组织关系；44 条输入也不得与
27 条独立的 R8 case-role 行相加后称为“关系边”。

R8 的 27 行是 case-role 记录，不是 27 条同案协作边：

- 13 行 registry actor；
- 14 行 person、institution 或 provisional procedural node；
- 原告、律师、被告、supporter、commenter、requester、non_party 等角色保持不同。

## 3. 数据 seam

前端不消费一个宽泛的 `relation_edges` 数组，也不在浏览器中判断状态。NR-02 构建模块
输出以下类型化集合：

```text
dyadic_relations
case_roles
event_participation
administrative_records
aggregate_observations
relation_leads
genealogy_anchors
```

每个集合共用 `coding_schema_v1.md` 的证据、人工决定、claim、graph eligibility 和
display tier 字段。L0／L1／L2 是前端呈现层，不进入研究数据字段名。

### dyadic_relations

只有两端均为 registry actor，且材料支持明确关系语义的记录进入。数据保留方向、端点角色、
案件／事件／项目范围、证据和解释边界。

### case_roles

保留：

```text
entity → case → role
```

不得把同案全部主体两两相连。只有已核 `legal_counsel`、正式 organizational affiliation
等独立关系，才能另行进入 `dyadic_relations`。

### event_participation

共同署名、共同声明、同场行动和 repeated co-action 保留为事件参与。它们可以出现在组织
面板和时间页，但不派生稳定联盟。

### administrative_records / aggregate_observations

actor—place、actor—program、服务存在、累计捐赠范围、project cost 等进入各自记录区，
不冒充组织—组织关系。

### relation_leads

NOFO、grant opportunity、co-presence lead、unknown recipient 进入“研究线索”区，永不
进入组织关系图。

## 4. L0：组织面板

组织详情新增两个相邻但分开的区：

### 与其他组织的关系

只显示 `graph_eligibility=dyadic_relation`：

- 关系家族和关系类型；
- 对方组织与方向；
- `supported`／`supported_bounded`／`candidate`；
- 已确认字段与缺失字段；
- E4／E3／E2；
- 来源、locator 和解释边界。

已核视图显示 `supported` 与 `supported_bounded`。研究视图追加 `candidate`。

### 其他记录与研究线索

显示：

- administrative record；
- aggregate observation；
- event participation；
- relation lead。

必须明确写“非组织关系边”“线索，非资助事实”或相应边界。

## 5. L1：组织关系图

组织页新增“关系”图形状态。关系家族独立开关：

- 资源与资助；
- 委托与服务中的真正 actor—actor 关系；
- 结构隶属；
- 明确的法律代理／法律支持；
- 人审后的协调关系。

视觉规则：

- 颜色编码关系家族；
- 箭头编码方向；
- 实线编码已核；
- 虚线编码候选；
- E4／E3／E2 使用标签；
- 缺失字段使用文字标签；
- 边宽固定，不表示证据、金额或强度；
- 节点面积和度数不表示影响力；
- 不显示无类型“联盟边”。

结构关系在数据中保留 source／target 角色，即使某些视觉状态暂不画箭头，也不能把
parent—member、national—regional 等关系存成无向事实。

法律案件默认使用 case-role 视图；不得以“同案”为由生成组织两两边。`non_party` 永不
生成边。

## 6. L2：谱系泳道

等待 NR-04／NR-05 的历史锚点和人工决定：

- formed／renamed／split／merged：实线谱系；
- coalition_successor：换轨虚线；
- issue／place／person continuity：弱连续性，不证明同一组织；
- candidate：虚线框；
- human accepted：实心；
- 每个锚点可打开证据抽屉。

当前 0 锚点继续作为明确缺口显示，不用当前网络反推。

## 7. 前端状态语言

已核视图：

- `supported`
- `supported_bounded`

研究视图：

- 已核视图全部内容；
- `candidate`
- 独立“研究线索”区的 `lead`

禁止只写“证据不足”。推荐字段级语言：

```text
关系存在　✓ 已核
方向　　　✓ 已核
期间　　　? 待核
金额　　　— 未公开
端点身份　✓ 已核
```

## 8. 四个控制案例

| 记录 | 正确身份 | 展示 |
|---|---|---|
| F021 OESC→USO 3,250 美元捐赠 | HR-033 `human_revised`；直接捐赠，非 sponsorship | 已核关系面板＋关系图 |
| F025 KOSC→AWWA资金贡献 | HR-033 `supported_bounded`；组织边金额为空 | 已核面板／关系图，显示“金额未公开” |
| R10R029 KOSC 102,000 美元合计 | scholarships＋AWWA composite scope | 其他记录，不上关系图，不分配给 F025 |
| F027 AWWA长期累计捐赠 | aggregate observation；recipient未逐一列名 | 其他记录，不上关系图 |
| F012 NOFO、recipient未知 | research lead | 研究线索，不上关系图 |

## 9. R10 与谱系 gate

- HR-032 的 8 条 canonical／JV／registry crosswalk 已完成；R10 的 365 个机器展示标签
  仍不 actor 化，也不生成 payment edge；
- AWWA recipient 完整年表等待 Form 990／内部年报；
- NR-04／05 的历史候选未经人审不进入谱系已核层；
- 没有官方 grant、award、contract、财报或组织报告，不新增已核资金关系。

## 10. 实现顺序

1. ~~完成 HR-033 和 schema legacy crosswalk~~（2026-07-20 已完成）；
2. ~~NR-02 构建模块生成类型化关系集合与派生状态~~（已完成；44 条输入通过 gate）；
3. ~~实现 L0 两区面板~~（已完成）；
4. ~~实现 L1 分层关系图~~（已完成）；
5. NR-04／05 人审锚点到达后实现 L2；
6. NR-06 做 claim／evidence／交互验收。
