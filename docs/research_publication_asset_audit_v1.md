# 已有研究成果发布准入审计 v1

日期：2026-07-20  
机器目录：`data/metadata/research_publication_catalog_v1.json`  
核心表面：`data/metadata/research_publication_core_surfaces_v1.json`

## 结论

本轮不是把旧图搬进网站，而是逐项判断：

1. 分析单位和选择边界是否符合当前研究方法；
2. 允许支持哪句话，禁止外推到哪一步；
3. 现有页面是完整模块、有限事实子层、待研究候选，还是退役产物。

审计后 catalog 共 **26 项**：

| 处置 | 数量 | 含义 |
|---|---:|---|
| architecture integrated | 3 | 修复 lifecycle、类型化关系、事件参与三个旧架构缺口 |
| method module integrated | 5 | 已形成完整 publication object |
| partial bounded | 4 | 安全事实子层可展示，完整模块仍缺 adapter／下钻 |
| adapter needed | 5 | 方法已就绪，但没有公开模块表面 |
| method research required | 5 | 有价值，仍需测量、人审或负责人解释门禁 |
| retired prohibited | 4 | 永久禁止回流当前展示 |

完整发布对象为 **8 项**；另有 4 个有限 core surface。不能把“当前页面能查到某些行”写成
“该研究模块已经完整接入”。

## A. 三个架构对象

| ID | 内容 | 当前展示 | 方法边界 |
|---|---|---|---|
| PUB-ARC-001 | LC001–LC005 生命周期锚点 | 时间页五条 | 最后观察不是解散；重组不是简单改名或 actor 合并 |
| PUB-ARC-002 | 类型化关系与非关系分层 | 组织关系图／面板 | funding、affiliation、case role、event、aggregate、lead 不混合 |
| PUB-ARC-003 | 经核事件参与事实层 | 时间页／组织面板 | 同场、联署、诉讼参与不生成稳定 actor–actor 边 |

`reviewed` profile 会物理排除 F027 等 deferred/local 记录；`client_preview` 可以显示这些记录，
但必须保留“待当地”“非组织关系边”等边界。

## B. 五个完整方法模块

| ID | 内容 | 当前最强可说内容 | 重要限制 |
|---|---|---|---|
| PUB-MR-004 | 先岛三地框架语料 | 限定线上语料中三地框架可见差异 | 9条观察／5条摘录为人审；另10／19条仅 QA-safe 研究层；不是居民态度 |
| PUB-MR-005 | 三次名单与重复参与 | 169条名单观察中有21个严格重复身份 | 三份目的性名单不是行动总体；重复参与不是联盟 |
| PUB-MR-012 | 县政府616行官方协作总体 | 可比较15部门、19事業分野、10机制 | 616行不是616组织、合同或拨款；365机器标签不 actorize |
| PUB-MR-013 | 六维覆盖偏差审计 | 可说明样本在哪些时期、地点、功能、议题、来源和复核层更可见 | 无总体分母；source数不是活动强度 |
| PUB-MR-014 | 13个制度转译 episode | 可比较场域进入、中间产出、有限结果和底层变化 | reviewed只有TE01–09；TE10–13只在研究层；不能算成功率 |

其中 `PUB-MR-004/005/012` 由专用 adapter 从正式行表重建；`PUB-MR-013/014` 从已存在但
过去绕过 catalog 的核心研究表面正式升格。升格依据不是“页面已经有”，而是重新核对了单位、
分母、状态分层、解释限制和物理 profile。

## C. 四个有限事实子层

| ID | 当前可保留内容 | 为什么仍不算完整模块 | 下一门禁 |
|---|---|---|---|
| PUB-MR-001 | 121 actor 搜索、141已核／142候选 actor–issue 分层 | edge 尚缺通用 source 下钻；网络布局易被误读为中心性 | 行级证据和来源敏感性方法卡 |
| PUB-MR-003 | 同源 actor×place×issue 的已核／候选区域计数 | 当前格数不能完整回到 actor→source→event | 建 strict triple 下钻 |
| PUB-MR-008 | actor 面板中的已核案件角色 | 未完整呈现6案、27角色、13 registered／14 provisional 对照 | case＋role 两级 adapter |
| PUB-MR-011 | 关系面板中的行政、服务、金额语义子层 | 不等于R10 35/28/43正式模块；F027仍待当地 | mechanism／amount／review 分层 adapter |

这四项在 core surface registry 中为 `partial_bounded`。公开快照只投影获准的 JSON 子层，
不会复制整份混合 `relations.json`。

## D. 五个方法就绪但尚无公开模块表面

| ID | 模块 | 已有研究价值 | 缺少什么 |
|---|---|---|---|
| PUB-MR-002 | 来源依赖与审核层稳健性 | S004 显著影响国际外围可见性，较小核心仍在 | 删除单位、分母与情景对照 adapter |
| PUB-MR-006 | 异质行动 repertory | 39唯一单元、15行动类、9场域类 | case/action/venue 行级比较 |
| PUB-MR-007 | 诉求入口、场域迁移、外部进入 | 80 formal、6路径族、3案9阶段、53 entry observations | formal 与 analytical seed 严格分层 |
| PUB-MR-009 | 四案公投门槛 | 29阶段＋29角色能比较不同制度停点 | local gap 不能显示为空或负事实 |
| PUB-MR-010 | 选举—民间组织公共接口 | 19条人审记录，18发生＋1 announcement-only | 明确不是投票效果或政策因果 |

当前时间页事件记录不是 PUB-MR-006，路径页 episode 也不是 PUB-MR-007 或 PUB-MR-009 的
替代。相邻内容不能因为复用页面而自动取得模块资格。

## E. 五个有价值但需重新研究的方向

| ID | 方向 | 当前支持 | 不能写 |
|---|---|---|---|
| PUB-RR-001 | 资料留存与观测网络可见性 | 现有指标关系不稳定，有dense-low／thin-high反例 | “中心性就是留存能力” |
| PUB-RR-002 | 两套功能生态 | 限定typed inputs未编码直接跨组组织关系 | “没有共享人员”“两个社会隔绝” |
| PUB-RR-003 | 前线化／战争记忆共同语言 | 有共同文件和跨区域载体记录 | 词汇增长、单向扩散、全日本共同语言 |
| PUB-RR-004 | 1998–2012制度化与载体史 | 有日期的组织载体史可能构成增量 | 法人／非正式整齐二分 |
| PUB-RR-005 | 制度转译负案例 | 候选案提示entry/processing/relief/implementation门禁 | 失败率或全部失败诉求的分母 |

五项仅进 `internal`。负责人阅读、变量测量、竞争解释和允许措辞完成前，前端缺内容不能反向
降低门槛。

## F. 四个永久退役家族

| ID | 退役内容 | 原因 | 替代 |
|---|---|---|---|
| PUB-RET-001 | 旧地点×议题宽矩阵 | actor 名下地点和议题笛卡尔拼接 | PUB-MR-003 |
| PUB-RET-002 | 旧 bridge network | 把度数误读为骨干、影响力或联盟 | PUB-MR-001＋002 |
| PUB-RET-003 | 旧边野古国际化单一路径 | 混合方向、署名、法律角色和因果 | PUB-MR-007＋008 |
| PUB-RET-004 | 其他旧生态／名单／证据图 | 计数与语义已被当前模块替代 | 当前R1/R3/R5/coverage |

退役文件仍可留作 provenance，但不能进入 snapshot、缩略图、搜索或同步稿。

## 编译器实际门禁

当前编译器会机械拒绝：

- catalog ID 重复、资产不存在或状态不合法；
- retired／candidate hypothesis 进入公开 profile；
- core builder 多出、少出或存在未被 registry 决定的文件；
- core surface owner 未 integrated／explicit partial；
- surface profile 超过 owner profile；
- adapter／core object envelope 与 catalog 不一致；
- research 目录与 profile 不一致；
- snapshot 出现 manifest/checksum 未登记文件；
- channel profile、release ID 或 manifest hash 不一致。

公开站不再包含 `demo/relations.json`、`research/candidates.json`、`views/global.json`、
`views/overview.json`、`views/actors.json` 或重复 `demo/historical_anchors.json`。

## 下一批接入顺序

1. `PUB-MR-008` 法律六案与 `PUB-MR-009` 公投四案：最能形成甲方可自主比较的制度处理图；
2. `PUB-MR-002` 来源敏感性：直接保护所有网络解释；
3. `PUB-MR-001/003/011`：把现有有限表面补成可下钻完整模块；
4. `PUB-MR-006/007/010`：行动、场域和选举接口。

每项仍须同时交付：行级 adapter、方法卡、selection boundary、publication envelope、三语
显示语义、测试和页面消费面。不得只复制图片。
