# Schema／alias／空间字段冻结审计 brief v1

日期：2026-07-20

状态：**最终依赖重生快照；41条决定已由负责人确认，中央冻结已通过受控 merge 另行完成。**

合并后记录见 `hr029_confirmed_freeze_manifest_v1.csv` 和
`hr029_central_merge_summary_v1.csv`。本 brief 下文保留“合并前候选”语态作为审计谱系；
不得据此误写为 HR-029 仍待决定。

## 1. 结论先行

当前 registry 的 122 个 actor，其 `actor_class`、`legal_status_guess`、`origin_type` 共 **366 个字段单元（N×3）**已逐项覆盖。HR-027 与后续身份修订已经受控合并，重生后的每个 actor 均自动进入三字段审计。当前共有 **505 条统一候选**，其中 **41 条进入 HR-029**；人工字段按稳定 review item ID 保留，当前已填写 41 条、待处理 0 条。

`origin_type` 的 7 个值已闭合，可原样冻结。`actor_class` 从 21 个表面值收敛为 21 个建议值；仍有 14 个 actor 字段 assignment 需要人工决定。`legal_status_guess` 从 44 种表面写法收敛到 34 个受控值；无法确认法人格者明确落到 `*_unresolved`，而不是猜成 NPO、基金会或正式网络。

![冻结准备度](fig_schema_freeze_readiness_v1.png)

## 2. Alias：查找等价不等于实体等价

现有 39 条 alias、20 种 alias_type 全部入审计。没有发现跨 actor 的规范化 alias 冲突；同一 actor 的来源敏感写法仍按各自来源保留。

三类名称必须和普通 alias 分开：

- A010 的「石垣島への自衛隊配備を止める住民の会」是 predecessor label，不是 A010 的简单旧名；
- A052 第4次嘉手纳、A053 第2次普天间是 case-round label，不表示每轮成员完全相同；
- A105 日本YWCA 与 A107 冲绳YWCA 是全国／地域两个 actor，以 affiliation 连接，不互作 alias，也不转移行动角色。

A106 的「首都圏連絡会／首都圏キャンペーン」canonical 选择仍需 HR-029。A111 的「女団協」不得转成已剔除 A094 所关联的「沖女連」，也不得借 alias 把 A094 重新放回 registry。

## 3. Place 与 venue：空间跨键已修复，venue 占位需分型处理

21 个 place 都获得 parent 与查询 alias 候选。P004 Futenma 与 P010 MCAS Futenma必须分别代表议题／地域层与实体基地层；P005 Kadena 需明确是 Kadena Air Base；P011–P013 的与那国、石垣、宫古必须区分町／市与岛屿／区域写法。这五项进入 HR-029。

135 条 actor–place 边目前有 **0 个交叉键冲突**。HR-025 已将 AP123 固定为 P007 Camp Foster，并批准只在来源明确指称先岛整体时使用 P021；本包不重复开启这些决定。

16 项 venue taxonomy 的 ID 与 label/group 本身无重复；但 event/pathway 表有 **18 条 `R10_VENUE` 占位引用**。其中明确的 USO 服务／捐赠观察可机械候选为 V016；伞状 membership、区域赞助、行政委托、JICA活动与公共外交 opportunity 并非同一种场域，所以 13 条进入 HR-029。V015 已实际使用，其“future expansion”旧 note 已过时，但本包不改 note。

## 4. Relation / action 受控值

`relation_type` 覆盖 78 行、29 个当前值，建议收敛为 26 个受控值。关键边界：

- `duplicate_replaced_by_F022` 是被拒绝重复记录，不应继续作为 relation type；
- `co_presence_lead` 只能候选为 co-presence observation，不能写成 coordination；
- `aggregate_history` 是金额历史观察，不是可分配给具体 recipient 的普通关系；
- `grant_opportunity` 保持 opportunity，不能升级为 grant 或 recipient；
- joint in-kind contribution 保留“共同贡献、份额未拆”的边界。

`action_type` 覆盖 255 行、14 个当前值，建议收敛为 12 个受控值。`co_signing` 与 `joint_statement`统一为事件参与；两种 request-letter 写法统一为 submission participation；`pathway_role`改为显式 analytical seed。共同署名、请求或同场出现仍不是稳定联盟。

![受控词汇收敛](fig_vocabulary_consolidation_v1.png)

## 5. 冻结后的可写与不可写

完成 HR-029 并由主线程另行合并后，可以写：本项目使用闭合 actor/origin/legal-status/alias/place/venue/relation/action 词汇；前身、诉讼轮次、全国—地方组织和空间层级各有显式边界；每个关系与行动值可以被 lint。

仍不可写：名称相似即同一组织；前身与后继是简单改名；不同诉讼轮次成员相同；全国组织行动自动转移到地方组织；`R10_VENUE` 九条可统一替换；NOFO 是已拨款；共同参与是稳定联盟。Schema freeze 也不批准任何候选 actor、edge、funding 或选举角色。

## 6. 后续顺序

1. HR-027、HR-019、HR-024、HR-025 与 HR-032 已完成受控合并，本包是其后的最终重生输入；
2. 负责人完成 `HR029_schema_alias_freeze_review_v0.csv`；
3. 主线程再受控合并 class assignment、alias lineage、place/venue 与 relation/action 语义；
4. 处理 `R10_VENUE` 后运行全库 FK/lint，再冻结正式 codebook；
5. 最后处理 HR-031 的解释强度决定，并生成报告、论文和 PPT。

复现命令：`python scripts/make_schema_alias_freeze_v1.py`。
