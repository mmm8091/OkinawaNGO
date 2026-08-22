# W2-B：USO 全国—地区—冲绳层级研究包 v1

日期：2026-08-22

状态：`research_only`／`ai_seeded`／`not_frontend_ready`。本包没有修改中央事实表、publication adapter、前端或控制文档。

## 1. 本包回答什么

本包沿着三条相互分开的链调查：

1. USO 全国组织、Indo-Pacific、Japan 与 Okinawa 的组织／站点层级；
2. DoD/WHS award、USO 全国财务与冲绳本地赞助／服务事实之间能否闭合；
3. USO、American Red Cross 与 Navy-Marine Corps Relief Society 在冲绳服务体系中的功能边界。

结论先行：**公开记录能同时看见全国资金、地区组织层级、冲绳站点和若干本地赞助，但没有公开连接 USO, Inc. → Indo-Pacific → Japan/Okinawa 的金额分配层。** 因而本包支持的是“层级可见、金额链中断”，不是冲绳预算估计。

## 2. 交付计数

| 文件 | 行数 | 内容 |
|---|---:|---|
| `hierarchy_and_site_year_v1.csv` | 16 | dated 层级、center／terminal／office／outreach 类型 |
| `service_capacity_observations_v1.csv` | 15 | 全国 impact、本地人员／志愿者、选定活动人数 |
| `sponsor_and_local_flow_observations_v1.csv` | 17 | sponsor roster、现金／实物的具名事件 |
| `federal_award_allocation_audit_v1.csv` | 19 | award／transaction／account／subaward／allocation gap |
| `service_function_boundary_v1.csv` | 10 | USO／Red Cross／NMCRS 十类功能对照 |
| `allocation_waterfall_v1.csv` | 9 | 瀑布图使用的九层可见性数据 |
| `source_receipts_v1.csv` | 34 | 来源收据；33 件本地哈希归档，1 件 403 日志 |
| `negative_search_log_v1.csv` | 10 | 十项有界负检索与下一材料入口 |
| `change_notes_v1.csv` | 6 | 六项口径调整 |
| `principal_review_queue_v1.csv` | 7 | 七项负责人判断 |
| `w2_d_endpoint_candidates_v1.csv` | 28 | 12 个组织／机构端点、15 个人物角色候选、1 条服务中介接口 |

图：`fig_allocation_visibility_waterfall_v1.svg`。框宽不编码金额，所有不同口径金额明确分栏。

## 3. 精确发现

### 3.1 站点数不是一个口径

- 2021 年官方故事使用“7 locations”：Schwab、Hansen、Kadena、Kadena Air Terminal、Foster、Futenma、Kinser；另列 10 个 outreach sites。
- 2025 年官方材料使用“6 centers”。
- 当前目录可拆成 8 个 typed presences：6 个 operating centers、1 个 Kadena AMC terminal presence、1 个 Okinawa Area Office。Torii Station 被官方材料明确写成没有 dedicated center 的 outreach site。

这三组数可以并存。它们不能直接推出中心开闭、组织解散或年度服务量变化。

### 3.2 已知金额与未知金额

已知：

- `HQ00342310002` 的 award-level cumulative obligation 为 USD 72m，prime recipient 是 United Service Organizations, Inc.，期间为 2023-09-30—2028-09-29。
- 同一 award 的 federal-account reporting layer 显示 USD 41.21246329m；本包将其分解为 USD 24m − USD 6.78753671m + USD 24m。交易历史另有 2025 年第三笔 USD 24m continuation，因此两层尚未闭合。
- USO 2024 consolidated program-services expense 为 USD 204.912m；这是组织合并财务口径，不是上述 award 的分配表。
- 冲绳层存在若干具名、具日的独立流入个案，包括 AEC USD 18k（2024）、AK Kogyo JPY 1m（2025）、AEC USD 16k（2025）与 OESC USD 3.25k（2025）。这些记录不是完整本地收入表。

未知：

- national prime → Indo-Pacific 的分配；
- Indo-Pacific → Japan/Okinawa 的分配；
- USO Okinawa 年度预算和中心费用；
- 与全球 `uses／visits／people reached` 同定义的冲绳年度分母；
- current sponsor tier 的金额；
- 具名实物支持的货币估值。

因此 USD 72m、USD 41.212m、USD 204.912m 与本地个案金额不能相加，也不能按中心数、人口或全球服务使用次数机械分配。

### 3.3 服务生态不是三家同质机构

- USO 的可见核心是 center/outreach、连接、士气与生活服务。
- American Red Cross 的可见核心包括紧急通信、医院志愿、灾害与海外军事社区支持。
- NMCRS 的可见核心包括无息贷款／补助、应急旅行、预算教育与灾害救助。
- 一条具体的跨组织接口得到官方材料支持：Red Cross 在 NMCRS 非营业时段代为处理入口，并使用 **NMCRS funds**。本包将其编码为 `confirmed_service_intermediation`，不是 Red Cross→NMCRS funding、joint grant、合并或政治联盟。

## 4. 最强可支持表述

> USO 的全国资金、Indo-Pacific／Japan／Okinawa 组织层级、冲绳站点和部分本地赞助分别可见，但公开记录没有披露连接这些层级的地区金额分配。由此可以确认服务基础设施的存在和若干本地资源输入，不能据此估算 USO Okinawa 的联邦资金额度或年度预算。

服务侧进一步显示出功能分工与有限接口，而不是单一同质网络；现有材料仍只到行动／组织自述和服务结构层，不能证明地方接受、态度改变或军事存在获得合法性。

## 5. 可改变判断的材料

1. award agreement／terms、WHS 项目报告或 later File C submissions，能解释 USD 72m 与 USD 41.212m 的时序／范围差异；
2. USO Indo-Pacific／Japan／Okinawa 年报、area budget 或 center-level expense schedule，能闭合地区金额层；
3. 与全球口径一致的 Okinawa `uses／visits／people reached` 年度表，能支持 service-use weighting；
4. USO Okinawa 的完整 donor schedule、sponsor agreement、in-kind valuation 或内部收入表，能判断本地个案覆盖；
5. Red Cross Okinawa 官方页面的人工归档件，可替代本轮 HTTP 403 日志；
6. recipient／使用者或独立地方来源对具体服务的回应，才可能把 LEG0／行动方 LEG1 推向 LEG2。

## 6. 负责人需要判断

七项判断已集中在 `principal_review_queue_v1.csv`：站点语义、两组联邦金额、哪些本地资源流进入共享 ledger、regional/local sponsor scope、Red Cross—NMCRS service interface、层级缺口结论，以及 LEG0/LEG1 边界。没有任何一项在本包内代替负责人完成。

供 W2-D 使用的端点另列在 `w2_d_endpoint_candidates_v1.csv`。人物行只保留资料中实际观察到的职务日期；`J. Phil VanEtten / Phil VanEtten` 与 `E.J. Schulz / Shultz` 仍需要姓名规范化。唯一可直接进入关系复核的服务接口是 Red Cross 代 NMCRS 处理非营业时段求助、使用 NMCRS funds；同址、一般转介、共同服务对象或功能重叠都没有自动升格为组织桥。

## 7. 复现与验证

```powershell
python scripts\build_us_presence_wave2_w2_b_v1.py
python -m unittest tests.test_build_us_presence_wave2_w2_b_v1
```

`validation_report_v1.json` 必须为 `PASS_RESEARCH_ONLY`。`manifest_v1.json` 给出本包表格、图、README、验证报告与来源下载件的 SHA-256。构建只读取已经冻结的官方／既有归档件，不联网，也不分配中央 S-ID。
