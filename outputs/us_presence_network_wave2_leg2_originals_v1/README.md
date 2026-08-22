# W2 LEG2 recipient/local-response 原件补强 v1

日期：2026-08-22

状态：`research_only`；W2-F 前置有界证据包。未进入 W2-F 合成、中央事实层、publication adapter 或前端。

## 1. 本包回答什么

本包只补一个问题：当基地侧慈善资源进入冲绳地方福利机构后，受赠方自己怎样记录、使用和解释这些资源？它不重新调查全部服务生态，也不测量“合法性提升”。

四个冻结端点是：

1. AWWA → かなさん沖縄；
2. AWWA → アンビシャス；
3. AWWA → 石垣ひまわり；
4. Marine Thrift Shop → Lions → 最终儿童医疗端点（仍未闭合）。

ToiToi 只作为 Ambitious 2024 年便携电源分发中的下游回应证据，不另开第五个端点。

## 2. 当前最强结果

- **Kana-san：超出礼节性致谢。** 受赠方官网确认直接收讫，说明资金将用于医养儿童/家庭写真展，并把资金解释为包含美军相关人士的善意；其活动传单再次确认写真展由 AWWA 捐款运营。
- **Ambitious：同时看到用途与关系叙事。** 2023 年受赠方刊物明确把 AWWA 的长期活动称作“冲绳与美国的桥梁”；2024 年材料则闭合了一笔 200 万日元、33 台便携电源、六个借用点的实际用途。独立地方报道还保留了下游 recipient 对“跨越国境的支援”的直接回应。
- **Himawari：目前只到收讫、致谢和往来。** 运营方通讯确认 2024-08-09 收到 200 万日元并提到既往交流，但本页没有说明该笔款项用途，也没有明确的桥梁叙事。
- **MTS → Lions：仍停在中介。** 本轮未找到 Lions 或最终受益机构的原始收讫材料；不得建立 Lions → 最终机构关系边或 LEG2 回应。

因此，选定端点已能支持一个有界判断：部分基地侧慈善资源不仅被地方机构收讫，也被转化为可核的地方福利用途；在 Kana-san、Ambitious 和 Ambitious 下游回应中，地方文本本身出现了 goodwill、bridge 或 cross-border support 类关系语言。这支持 `relationship_frame_local`，但在同一行动的先行 LEG1 尚未闭合时，不编码为 `narrative_uptake`，更不是 LEG3 的态度或合法性效果。

## 3. Ambitious 的时间必须拆开

| 时段 | 能支持什么 | 不能支持什么 |
|---|---|---|
| 2012 | AWWA 到访进行受赠资格确认；recipient 刊物传播其长期福利贡献叙事 | 不能验证刊物中的累计金额；不能把同刊具名个人短评写成机构立场 |
| 2023 | 具体回忆过往设备/刊物用途，并明确使用“冲绳与美国的桥梁” | 不能闭合 2024 行动或任何特定 990 行 |
| 2024 | 200 万日元购买 33 台便携电源并形成地方借用/分发链 | 不能据此闭合 AWWA 申报中的 USD 13,423 行 |

## 4. 数量与文件

- 4 个冻结端点；
- 8 条 response evidence；
- 9 条带本地归档和 SHA-256 的 source receipt；
- 6 条竞争解释；
- 7 条负检索记录；
- 7 个负责人复核输入，全部复用既有 `HR-USN2-04/05/06b`，不另建人工任务；
- 1 条 `lead_only` 意外发现。

核心文件：

- `endpoint_action_crosswalk_v1.csv`：四端点、行动段、金额边界和 HR 对照；
- `response_evidence_excerpts_v1.csv`：recipient/local 原文定位、短锚点和分类候选；
- `source_receipts_v1.csv`：URL、本地路径、locator、SHA-256；
- `principal_review_queue_v1.csv`：需负责人决定的交易闭合和 LEG2 分类；
- `competing_interpretations_v1.csv`：对“福利中介／关系叙事／礼仪性／资源依赖”的竞争解释；
- `negative_search_log_v1.csv`：有界负检索；
- `principal_checkpoint_v1.md`：负责人阅读顺序和拟决项；
- `validation_report_v1.json`、`manifest_v1.json`：结构、边界和字节验证。

## 5. 方法边界

- 行动方新闻稿没有被编码成 recipient response。
- 受赠方致谢、goodwill、bridge、cross-border support 与具体用途分别编码；它们不自动串成因果链。
- 表中的 `partner_or_bridge_narration` 是为兼容既有 HR-USN2-05 而保留的宽类；在本包只表示地方文本出现关系语言，对应红队口径的 `relationship_frame_local`，不自动表示受赠方复述了行动方先行叙事。
- 没找到 rights/compensation、保持距离或拒绝类回应，只表示这四端点及所选公开体裁中未见，不表示地方社会不存在。
- 所有金额匹配均保持原币和原税期；Kana-san、Ambitious、Himawari 的地方材料都没有闭合相应 990 行。
- 本包没有修改任何已有 W2-A 数据，也没有向中央层写回。

## 意外发现登记

`unexpected_findings_register_v1.csv` 记录 1 条 `lead_only` 观察：Ambitious 127 号把机构受赠叙事与另一个具名个人短评分区刊载。该短评不能自动等同于组织政治立场；本轮没有沿线索继续侦察，也不进入结论、人工复核、中央层或发布层。

## 6. 复现验证

```powershell
python scripts\validate_us_presence_network_wave2_leg2_originals_v1.py
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_leg2_originals_v1
```
