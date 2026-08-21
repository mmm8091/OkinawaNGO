# 对美主线第二轮：W2-00 负责人检查点

日期：2026-08-22

状态：`evidence_reading_required_before_W2-A_B_C_E`。W2-00 锚点冻结已完成；本检查点通过前，152 条锚点中的新提取项继续保持 `research_only`，不写中央事实层、publication adapter 或前端。

## 先看结果

W2-00 已建立 9 套选择框、152 条锚点、43 条权威来源收据、41 件本地冻结原件、24 条口径修订和 4 套案例量尺。统一包在 `outputs/us_presence_network_wave2_w2_00_v1/`。

这一轮有三个实质性结果：

1. **AWWA 中介链已有时间维度。** OESC→AWWA 在三个连续税期中申报 USD 16,308、14,371 和 8,479；AWWA 两期披露的日本组织拨出为 USD 91,838／64,077，基地关联组织拨出为 USD 33,320／30,812。这足以把“资源中介”从概念变成可追踪案例。
2. **USO 的全国资金可见，冲绳分配层不可见。** USD 72m award 能闭合到 USO Inc. 全国 prime recipient，但不能闭合到 Japan／Okinawa。“6 个中心”与“8 个地点”则已解决为站点类型差异。
3. **两个初始尺子不能直接使用。** 4.5 万–5.7 万不是当前同年同定义人口区间；13 个问责 episode 是按成功进入制度选出的正向样本。前者不能用来发布当前人均数，后者不能单独证明“制度结果有上限”。

## 负责人的 45–60 分钟阅读

### 1. AWWA／OESC，20 分钟

- 打开 `W2A-SR012`、`W2A-SR013`、`W2A-SR014` 对应的 OESC 官方 IRS XML，核 Schedule I 中 AWWA 的 EIN、金额和税期；
- 打开 `W2A-SR001`、`W2A-SR002` 对应的 AWWA XML，核两类拨出桶和六个具名描述；
- 读 `outputs/us_presence_network_wave2_w2_00_spouse_990_v1/README.md` 第 4–5 节，特别注意 KOSC USD 2,580 与 MOSCO 空元素。

### 2. USO，15 分钟

- 读 USO 2024 audited statement pp. 5–8 与 Form 990 的总收入／program-service／总支出行，确认两个 reporting perimeter；
- 核对 USAspending award overview、transactions 和 subaward response，区分 USD 72m award-level total、USD 41.212m 字段语义冲突和 0 reported subawards；
- 读 `outputs/us_presence_network_wave2_w2_00_uso_v1/site_hierarchy_probe_v1.csv` 的 12 行站点层级。

### 3. 人口与问责，15–25 分钟

- 核冲绳县统计年鉴 sheet `28_01` 的 2011 年 47,300 人和 2012 年后未提供同口径的脚注；
- 将“接近 80,000”、具名构成小计 57,100 和医疗服务人口 47,000 对照；
- 对照 Earthjustice USD 276,345.50 申报行与 Treasury USD 280,000 付款行；差额原因不明；
- 读 `selection_frames_v1.csv` 中 `ENTRY13`、`NONENTRY`、`PROJECTCHANGE` 三行。

## 请决定的七项

结构化回传表是 `outputs/us_presence_network_wave2_w2_00_v1/principal_review_queue_v1.csv`。

### PR001：当前人口分母

**建议确认**：当前同年同定义的全冲绳分母未闭合，W2-A／W2-B 不发布当前人均数，改用总额、申报内覆盖率和端点覆盖率。

### PR002：OESC→AWWA 三税期关系

**建议确认**：新补 USD 16,308 和 14,371 两行为 `human_checked`，与既有 USD 8,479 组成三税期连续申报关系。不外推资金最初来源、AWWA 下游去向或三期之外的持续性。

### PR003：AWWA 六个具名 recipient

**建议全部放行为 research tracer**：进入身份、收款端与 LEG2 地方回应补查；未确认正式名称和受赠端证据前，不进中央资金关系。

### PR004：五家组织的量级与异常字段

**建议确认**：USD 1.011m 收入、USD 1.146m 支出、USD 239k grants 下限、USD 625,527 net assets 只称“五家最新申报的跨税期毛运作量级”；KOSC USD 2,580 继续暂缓；MOSCO 最新 grants 元素保持缺失，不改写为 0。

### PR005：USO 财务与站点口径

**建议确认**：审计合并财报与 USO Inc. Form 990 并列保存，不相加或互换；以 6 个 operating centers＋AMC terminal＋area office 记录 8 个 typed presences。

### PR006：USD 72m DoD award 的边界

**建议确认**：只建立 DoD／WHS→USO Inc. 全国 prime award 锚点；USD 41.212m 保留为字段语义冲突；0 subaward 只是公开 subaward 检索结果；不生成 DoD→USO Okinawa 资金关系。

### PR007：问责研究的三组比较

**建议确认**：将 13 个正向入场 episode、匹配的未入场案例、项目改变反例并列建样；后两组完成前，暂停对“制度结果上限”的总体扩大。

## 检查点后的执行顺序

七项全部通过后，放行 W2-A、W2-B、W2-C 和 W2-E 四个 `research_only` 包；W2-D 等 W2-A 产生人物与 recipient 端点后再开始。

- W2-A 的首个交付不是网站摘要，而是五家组织三税期长表、去重流向表、人物职务表和 recipient 反向证据。
- W2-B 首先补 Indo-Pacific／Japan／Okinawa 分配层；仍找不到时，用层级瀑布图明确显示断点。
- W2-C 先建负案例和项目改变反例，再回编 13 个正向入场 episode；不反过来用 13 例选择后特征找结论。
- W2-E 以问责侧／服务照护侧两条历史线建背景，来源结构不对称时直接显示缺口。

本检查点只放行后续研究包，不同时授权中央写回、publication adapter 或前端发布。
