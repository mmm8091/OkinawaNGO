# W2-B：USO 全国—地区—冲绳层级研究包 v1

日期：2026-08-22

状态：`research_only`／`ai_seeded`／`not_frontend_ready`。本包没有修改中央事实表、publication adapter、前端或控制文档。

## 1. 本包回答什么

本包沿着三条相互分开的链调查：

1. USO 全国组织、Indo-Pacific、Japan 与 Okinawa 的组织／站点层级；
2. DoD/WHS award、USO 全国财务与冲绳本地赞助／服务事实之间能否闭合；
3. USO、American Red Cross 与 Navy-Marine Corps Relief Society 在冲绳服务体系中的功能边界。

结论先行：**公开记录能同时看见同一 award 的两个全国报送视图、地区组织层级、冲绳目录条目和若干本地赞助，但没有公开连接 USO, Inc. 与 Indo-Pacific／Japan／Okinawa 的地区金额分配层。** 因而本包支持的是“并列报送口径可见、地区分配缺口未闭合”，不是资金逐层流下的链条或冲绳预算估计。

## 2. 交付计数

| 文件 | 行数 | 内容 |
|---|---:|---|
| `hierarchy_and_site_year_v1.csv` | 17 | dated 层级、center／terminal／office／outreach 类型 |
| `service_capacity_observations_v1.csv` | 15 | 全国 impact、本地人员／志愿者、选定活动人数 |
| `sponsor_and_local_flow_observations_v1.csv` | 17 | sponsor roster、现金／实物的具名事件 |
| `federal_award_allocation_audit_v1.csv` | 19 | award／transaction／account／subaward／allocation gap |
| `service_function_boundary_v1.csv` | 10 | USO／Red Cross／NMCRS 十类功能对照 |
| `allocation_waterfall_v1.csv` | 11 | 并列 award/account 视图、共同分配缺口及 gross/in-kind/net 财务口径 |
| `source_receipts_v1.csv` | 34 | 来源收据；33 件本地哈希归档，1 件 403 日志 |
| `negative_search_log_v1.csv` | 10 | 十项有界负检索与下一材料入口 |
| `change_notes_v1.csv` | 6 | 六项口径调整 |
| `principal_review_queue_v1.csv` | 7 | 七项负责人判断 |
| `w2_d_endpoint_candidates_v1.csv` | 28 | 12 个组织／机构端点、15 个人物角色候选、1 条服务中介接口 |

图：`fig_allocation_visibility_waterfall_v1.svg`。文件名保留旧契约；图内 USD 72m 与 USD 41.21246329m 是同一 award 的并列报送视图，共同指向 regional allocation gap，连线不表示资金逐层流下。框宽不编码金额。

## 3. 精确发现

### 3.1 站点数不是一个口径

- 2021 年官方故事是 **7 listed locations**：Schwab、Hansen、Kadena、Kadena Air Terminal、Foster、Futenma、Kinser；另列 10 个 outreach sites。
- 2025 年官方材料是 **6 physical centers**。
- 当前是 **8 directory entries = 6 centers + 1 terminal entry + 1 area office**。Torii Station 被官方材料明确写成没有 dedicated center 的 outreach site。

这三组数可以并存。不将 8 directory entries 称为 8 个站点；三个时间截面也不能推出中心开闭、组织解散或任何生命周期变化。

### 3.2 已知金额与未知金额

已知：

- `HQ00342310002` 有两个并列报送视图：award-level cumulative obligation 为 USD 72m，而 federal-account reporting 视图为 USD 41.21246329m（USD 24m - USD 6.78753671m + USD 24m）。两者都是同一 award 的全国报送口径，不是先后流动的两层资金；两者共同指向未公开的 regional allocation gap。
- USO 2024 审计合并财务表 p.8 列出 **gross program services / functional expenses USD 204.912m**，其中已包含 **in-kind USD 105.538m**，并同时列出 **net program services USD 99.374m**。这是全国组织合并财务口径，不是上述 award 的分配表。
- 冲绳层存在若干具名、具日的独立流入个案，包括 AEC USD 18k（2024）、AK Kogyo JPY 1m（2025）、AEC USD 16k（2025）与 OESC USD 3.25k（2025）。这些记录不是完整本地收入表。

未知：

- national prime → Indo-Pacific 的分配；
- Indo-Pacific → Japan/Okinawa 的分配；
- USO Okinawa 年度预算和中心费用；
- 与全球 `uses／visits／people reached` 同定义的冲绳年度分母；
- current sponsor tier 的金额；
- 具名实物支持的货币估值。

因此 USD 72m 和 USD 41.21246329m 不能相加；USD 105.538m 已包在 USD 204.912m gross 中，也不能再加一次。这些全国口径与本地个案金额都不能按中心数、人口或全球服务使用次数机械分配。

### 3.3 服务生态不是三家同质机构

- USO 的可见核心是 center/outreach、连接、士气与生活服务。
- American Red Cross 的可见核心包括紧急通信、医院志愿、灾害与海外军事社区支持。
- NMCRS 的可见核心包括无息贷款／补助、应急旅行、预算教育与灾害救助。
- 官方材料支持一条有方向的候选接口：**NMCRS -> American Red Cross (ARC)**。NMCRS 委托 ARC 处理非营业时段的 intake/disbursement；ARC 代表 NMCRS 并使用 **NMCRS funds**。状态为 `official_source_supported_candidate_pending_principal`，不是 confirmed，也不是组织间 funding、joint grant、合并或政治联盟。

## 4. 最强可支持表述

> 同一 award 的两个全国报送视图、Indo-Pacific／Japan／Okinawa 组织层级、冲绳目录条目和部分本地赞助分别可见，但公开记录没有披露连接全国与地区层的金额分配。由此可以确认服务基础设施的存在和若干本地资源输入，不能据此估算 USO Okinawa 的联邦资金额度或年度预算。

服务侧进一步显示出功能分工与有限接口，而不是单一同质网络；现有材料仍只到行动／组织自述和服务结构层，不能证明地方接受、态度改变或军事存在获得合法性。

## 5. 可改变判断的材料

1. award agreement／terms、WHS 项目报告或 later File C submissions，能解释 USD 72m 与 USD 41.21246329m 两个并列报送视图的时序／范围差异；
2. USO Indo-Pacific／Japan／Okinawa 年报、area budget 或 center-level expense schedule，能闭合地区金额层；
3. 与全球口径一致的 Okinawa `uses／visits／people reached` 年度表，能支持 service-use weighting；
4. USO Okinawa 的完整 donor schedule、sponsor agreement、in-kind valuation 或内部收入表，能判断本地个案覆盖；
5. Red Cross Okinawa 官方页面的人工归档件，可替代本轮 HTTP 403 日志；
6. recipient／使用者或独立地方来源对具体服务的回应，才可能把 LEG0／行动方 LEG1 推向 LEG2。

## 6. 负责人需要判断

七项判断已集中在 `principal_review_queue_v1.csv`：站点语义、两组联邦金额、哪些本地资源流进入共享 ledger、regional/local sponsor scope、Red Cross—NMCRS service interface、层级缺口结论，以及 LEG0/LEG1 边界。没有任何一项在本包内代替负责人完成。

供 W2-D 使用的端点另列在 `w2_d_endpoint_candidates_v1.csv`。人物行只保留资料中实际观察到的职务日期；`J. Phil VanEtten / Phil VanEtten` 与 `E.J. Schulz / Shultz` 仍需要姓名规范化。唯一进入关系复核的服务接口候选是 NMCRS -> ARC 的非营业时段 intake/disbursement 委托；ARC 代表 NMCRS 并使用 NMCRS funds。它仍是 `official_source_supported_candidate_pending_principal`。同址、一般转介、共同服务对象或功能重叠都没有自动升格为组织桥。

## 7. 复现与验证

```powershell
python scripts\build_us_presence_wave2_w2_b_v1.py
python -m unittest tests.test_build_us_presence_wave2_w2_b_v1
```

`validation_report_v1.json` 必须为 `PASS_RESEARCH_ONLY`。`manifest_v1.json` 给出本包表格、图、README、验证报告与来源下载件的 SHA-256。构建只读取已经冻结的官方／既有归档件，不联网，也不分配中央 S-ID。
