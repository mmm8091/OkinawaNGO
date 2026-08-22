# W2-A：军属俱乐部资源网络与受赠端核查 v1

日期：2026-08-22  
状态：`research_only / principal_review_pending`。本包没有写回中央事实、旧 43 行、publication adapter、前端或控制文档。

## 1. 完成状态

- 五家核心组织登记 **15 个目标税期**，其中 **14 份官方 IRS XML** 可用；AWWA 第三税期维持官方 index-only gap。
- Marine Thrift Shop 渠道 tracer 新增 **2 份官方 IRS XML**，第三期只见官方索引。
- `filing_metric_long_v1.csv` 有 **72 条**组织×税期×指标长表记录。
- `person_actor_role_time_v1.csv` 有 **104 条** filing-role observations；它们是姓名字符串×组织×申报期，不是已消歧人物网络。
- `resource_flow_ledger_v1.csv` 有 **55 条**类型化资金／物资／服务观察，所有总额、子项、bucket、residual 与宣传口径均带去重字段。
- 六个 AWWA 英文 recipient descriptor 均找到日文实体候选；**3/6** 找到 recipient 自身或地方侧 AWWA 回应；**0/6** 闭合到同一申报行的金额与税期。
- 建立 **16 项**负责人复核队列和 **8 条**有界负检索日志。

验证：`validation_report_v1.json` = `PASS_RESEARCH_ONLY_W2_A`。

## 2. 目前最强、但仍有边界的发现

### AWWA 是重复出现的分配中介，不是唯一渠道

官方申报现在显示两种重复输入：OESC 连续三期向 AWWA 报告 USD 16,308、14,371、8,479；Marine Thrift Shop 两期向 AWWA 报告 USD 41,183、19,669。AWWA 自身两期又把拨出分成日本组织与基地关联组织两个桶。因此可以把 AWWA 描述为**多家军属组织反复使用的分配中介**。

但这不是一条可追踪的“某笔上游钱→某个下游 recipient”链：各组织税期不同，AWWA 申报不提供 earmarking。五笔输入不能相加成某一年度收入，也不能分摊给六个具名 recipient。

Marine Thrift Shop 另有一条 2024-02-22 经 Lions 的 USD 10,000 路径；行动方明确说这是首次绕开 AWWA 直接选择地方组织。它支持“AWWA 重要但并非唯一渠道”，但当前只闭合 MTS→Lions，未闭合 Lions→最终机构。

### AWWA 的具名端点只覆盖拨出的一部分

两期六个具名描述合计 USD 84,016，占日本组织桶 USD 155,915 的 **53.89%**，占两期 grant line USD 220,047 的 **38.18%**。分期分别为：FY ending 2023，48.07%／35.27%；FY ending 2024，62.23%／42.02%。其余部分仍是汇总桶或未具名端点。

这两个百分比是**申报可见度**，不是受益覆盖、地方接受度或完整 recipient universe。

### recipient 回应能做到 LEG2，但不能越级为合法性效果

Kana-san 的自有传单说明写真展由 AWWA 捐款运营；Ambitious 的自有材料记录设备、会报和彩印等具体用途，并出现“冲绳与美国的桥”叙事；石垣市社协的 2024 年通讯记录向“ひまわり”赠款及既有交流。它们支持 practical use、gratitude、bridge narrative 等 LEG2 候选。

Ambitious 与 Himawari 的金额／日期并不与当前 AWWA 申报行直接闭合；这些话语也没有测量地方对美军存在的态度变化。因此本包不生成 LEG3。

## 3. 什么证据会削弱或推翻当前解释

1. AWWA 或 recipient 账簿若表明 OESC／MTS 输入全部指定给基地内部项目，会削弱“跨基地—地方中介”的范围。
2. 若六个英文 descriptor 中的日文实体 crosswalk 被否决，具名端点与 LEG2 覆盖率都应下调。
3. 若 MTS→Lions 的最终 recipient 无法核实，绕行路径只能停在中介层；若实际仍由 AWWA 决定，则“绕开”解释应撤回。
4. recipient 侧若把捐赠明确重释为权利、补偿或行政责任，或拒绝伙伴叙事，会削弱“关系建构叙事被接受”的机制。
5. 独立调查若显示服务曝光与态度无变化／反向变化，将反驳任何合法性效果；本包目前没有这类 LEG3 设计。
6. 同期原始账簿若解释 MTS 的 >110k、>126k 与 IRS 125,218 为不同口径，当前“口径冲突”可收紧；否则不得任选一个当真值。

## 4. 负责人必须判断

`principal_review_queue_v1.csv` 集中列出：4 组跨组织人物／近名消歧、3 个 recipient name crosswalk、Kana-san／Ambitious／Himawari 的 exact transaction match、LEG2 分类强度、MTS 三种 2023 总额口径、Lions 下游、MOSCO USD 7,500 语义与 KOSC USD 2,580 standing defer。

在负责人处理前：exact-string 人名只算候选，六个 recipient 不进入中央关系，KOSC 2,580 不生成 flow，MOSCO blank 不改成 0。

## 5. 文件

| 文件 | 用途 |
|---|---|
| `filing_period_register_v1.csv` | 五家 15 槽 + MTS 三槽覆盖 |
| `filing_metric_long_v1.csv` | 组织×税期×四指标长表 |
| `person_actor_role_time_v1.csv` | 官方申报中的姓名—组织—职务—税期观察 |
| `resource_flow_ledger_v1.csv` | 类型化资金／物资／服务观察与去重字段 |
| `resource_flow_dedup_summary_v1.csv` | 各申报 grant line 的组件闭合 |
| `awwa_recipient_identity_leg2_v1.csv` | 六端点身份、受赠端证据和 LEG2 候选 |
| `recipient_coverage_v1.csv` | named/bucket/total 与回应覆盖率 |
| `awwa_mediation_structure_v1.csv` | AWWA 输入、输出与 MTS 绕行步骤 |
| `marine_thrift_shop_tracer_v1.csv` | MTS filing 与渠道观察 |
| `negative_search_log_v1.csv` | no-hit 与未闭合端点，不作现实零关系 |
| `principal_review_queue_v1.csv` | 正式负责人判断队列 |
| `w2d_endpoint_handoff_v1.csv` | 给 W2-D 的人物、recipient 与组织流端点；候选不升格为 bridge |
| `source_receipts_v1.csv` | 官方 IRS、recipient、地方与 tracer 收据／哈希 |
| `change_notes_v1.csv` | 口径调整与影响 |
| `fig_awwa_mediation_structure_v1.svg` | 中介结构解释图 |

## 6. 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_a_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_a_v1
```

脚本只重建本包的派生 CSV／SVG／README／validation／manifest，原始网络收据已冻结在 `artifacts/`；W2-00 的 14 份核心 IRS XML 通过原包路径与哈希引用。

## 7. 不得误读为

- 不是五家组织的合并年度财报或全冲绳生态总额；
- 不是上游捐款到下游 recipient 的 earmarked money trail；
- 不是六个 recipient identity、人物桥或 KOSC/MOSCO 敏感语义的人审结果；
- 不是 recipient 感谢等于对军事存在的接受；
- 不是中央写回、publication 或前端发布授权。
