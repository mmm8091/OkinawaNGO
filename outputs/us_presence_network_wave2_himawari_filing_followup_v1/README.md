# AWWA→Himawari 下一期 IRS 申报核查 v1

日期：2026-08-22

状态：`research_only`。这是 HR-USN2-04a 的定向补查；不修改中央事实层、关系表、publication adapter 或前端。

## 1. 核查问题

2024-08-09，石垣市社会福祉協議会的通讯记录 AWWA 向其运营的障がい児通所支援事業所ひまわり赠呈 200 万日元。负责人要求核查：AWWA 在紧随 2023-06-01—2024-05-31 税期之后的下一期 IRS 申报中，是否出现 Himawari、石垣市社会福祉協議会或可对应的英文描述，并能否与该事件闭合。

如果 AWWA 延续原有 5 月 31 日税期，待查期应为 2024-06-01—2025-05-31。这个日期是根据前两期申报周期得到的检索预期，不替代尚未公开的正式申报表头。

## 2. 核查结果

截至 2026-08-22，**IRS 官方公开系统中未检出 AWWA 的 2025-05-31 期末申报**：

- 完整下载并检索 IRS `index_2026.csv`，共 385,891 行、47,506,032 bytes；EIN `980227149` 和法定名 `AMERICAN WELFARE AND WORKS ASSOCIATION` 均为 0 命中；
- W2-00 已冻结的 2021—2026 官方年度索引筛选收据中，AWWA 最新记录仍是 2023-06-01—2024-05-31、object ID `202443189349200514`；其中没有 2025-05 期末记录；
- 现有 FY2024 官方 XML 的 Himawari 行为 USD 13,378，税期结束于 2024-05-31，并明确描述医疗床及儿童室内外设备；地方通讯中的 200 万日元赠呈发生在 2024-08-09，晚于该税期。

因此，本轮没有发现可用于闭合 2024-08-09 事件的“下一期 AWWA 申报行”。最强表述是：

> 截至 2026-08-22，在已核 IRS 官方公开索引中尚未检出 AWWA 2024-06-01—2025-05-31 申报；现有 USD 13,378 行与 2024-08-09 的 200 万日元赠呈继续作为两个独立记录保存。

这不等于 AWWA 未申报、未捐赠，或下一期申报将不会出现 Himawari；也不允许用汇率把两个金额反推为同一交易。

## 3. 对 HR-USN2-04a 的建议

负责人已经接受“USD 13,378 申报行与 2024-08-09 JPY 2m 事件分开”。本补查支持维持该决定：

- `transaction_closure = not_closed`；
- 2024-08-09 事件保留为 recipient-operator 原件确认的 `receipt + gratitude + reciprocal_exchange`；
- 该通讯没有写出 200 万日元的用途，也没有出现 bridge 语言；
- 下一期申报公开后，应按 EIN、税期、program-service/Schedule O 原文重新核查，不预先建立金额边。

## 4. 文件

- `filing_search_result_v1.csv`：三层核查结果与允许表述；
- `source_receipts_v1.csv`：官方索引、FY2024 XML 和地方 recipient-operator 原件的哈希收据；
- `negative_search_log_v1.csv`：EIN、法定名和目标税期的负检索；
- `decision_recommendation_v1.csv`：对 HR-USN2-04a 的补充建议；
- `artifacts/irs/index_2026_20260822.zip`：完整 IRS 官方 2026 年索引的本地压缩原件；
- `artifacts/irs/index_2026_http_headers_v1.txt`：下载时的官方响应元数据；
- `unexpected_findings_register_v1.csv`：本轮无意外发现，保留标准空表。

## 5. 不得被误读为

- 没有证明 AWWA 没有提交下一期申报；
- 没有证明 2024-08-09 的 200 万日元事件未发生；
- 没有把 USD 13,378 与 JPY 2m 视为同一交易；
- 没有确认 200 万日元的具体用途；
- 没有新增中央资金边或 LEG3 合法性结论。

## 意外发现登记

`unexpected_findings_register_v1.csv` 为统一 19 列、0 行。此次定向补查没有产生新的 `lead_only` 观察。
