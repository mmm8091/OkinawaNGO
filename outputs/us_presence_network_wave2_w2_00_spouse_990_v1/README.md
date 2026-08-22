# W2-00：AWWA／五家军属俱乐部 IRS 锚点包 v1

日期：2026-08-22
状态：`research_only / principal_checkpoint_confirmed`；官方收据已冻结，三期 OESC→AWWA 行已由负责人确认。尚未授权中央事实层、关系表、publication adapter 或前端写回。

## 1. 本包完成了什么

本包把 `tmp/service_recon_990/` 中的第三方 IRS 可视化缓存，替换为可复查的官方 IRS bulk XML 收据，并按税期拆开 AWWA、KOSC、MOSCO、NOSCO、OESC 的财务锚点。

- 冻结 **14 份官方 IRS XML**：AWWA 2 个税期；KOSC、MOSCO、NOSCO、OESC 各 3 个税期。
- 建立 **83 条锚点候选**，包括申报级收入、支出、grants line、期末资产／净资产，AWWA 的两类拨出桶与具名 program-service 行，以及 OESC→AWWA 的 Schedule I 行。
- 建立 **15 条 source receipt**：14 份官方 XML 加 1 份官方年度索引的规范化筛选摘录。
- 记录 **25 条相邻税期索引匹配**、**24 份既有缓存文件**和 **8 条口径变更说明**。
- 没有分配中央 `S-ID`，没有新增中央资金边，没有更新 actor registry、relation tables、publication adapter 或前端。

验证结果见 `validation_report_v1.json`：`PASS_RESEARCH_ONLY_W2_00_SPOUSE_990`。

## 2. 官方 XML 与既有缓存的区别

| 层 | 本包中的用途 | 能否支持锚点 | 能否直接进中央关系表 |
|---|---|---:|---:|
| IRS 官方 bulk XML | 申报值、税期、EIN、Schedule I／O 原文与对象号的正式收据 | 是，仍保留 `ai_seeded`／既有人审状态 | 否，另需负责人批准受控写回 |
| IRS 年度 index 筛选摘录 | 定位 object ID、税期与相邻申报 | 只支持“申报记录存在”，不支持金额 | 否 |
| `tmp/service_recon_990` 中的 ProPublica visual render | 侦察字段、检查渲染、提示可能的 Schedule 行 | 否；本包不再用它作权威收据 | 否 |
| `.html.txt` 派生文本 | 检索便利 | 否 | 否 |

官方 XML 都从 [IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads) 所列压缩包中按 byte range 抽取；成员的 ZIP CRC-32、解压后字节数和 SHA-256 均已核验。`source_receipts_v1.csv` 记录压缩包 URL、object ID、精确成员名、本地路径和哈希。

## 3. 三税期覆盖

| 组织 | 官方 XML 税期 | 当前覆盖判断 |
|---|---|---|
| AWWA | 2022-06-01—2023-05-31；2023-06-01—2024-05-31 | 2 个税期。IRS index 另列 2022-05 期末申报，但目标 XML 已不在当前 2022 官方 bulk ZIP 中；只记 index gap，不搬用第三方金额 |
| KOSC | 2022-06-01—2023-05-31；2023-06-01—2024-05-31；2024-06-01—2025-05-31 | 3 个连续税期 |
| MOSCO | 2022-06-01—2023-05-31；2023-06-01—2024-05-31；2024-06-01—2025-05-31 | 3 个连续税期；最新期 grants-and-similar-paid XML 元素为空，未强制写成 0 |
| NOSCO | 2022-07-01—2023-06-30；2023-07-01—2024-06-30；2024-07-01—2025-06-30 | 3 个连续税期 |
| OESC | 2022-07-01—2023-06-30；2023-07-01—2024-06-30；2024-07-01—2025-06-30 | 3 个连续税期 |

完整相邻申报匹配见 `official_index_matches_v1.csv`。本包已经达到 W2-00 的锚点目的；AWWA 第三份 XML 的缺失按任务要求收束为 gap，不继续无限检索。

## 4. 当前可直接读出的事实

### 4.1 OESC→AWWA 不是单年线索

OESC 的三份官方 Schedule I 连续报告 AWWA（EIN `98-0227149`）为 recipient：

| OESC 税期 | Cash grant |
|---|---:|
| 2022-07-01—2023-06-30 | USD 16,308 |
| 2023-07-01—2024-06-30 | USD 14,371 |
| 2024-07-01—2025-06-30 | USD 8,479 |

负责人于 2026-08-22 确认三行金额与身份，三期均记为 `human_checked` research-only 锚点。三份官方 XML 的 recipient EIN 均为 `98-0227149`。这里可以说“申报连续三期出现”，不能说三期之外持续发生，也不能推断 AWWA 下游 recipient、资金最初来源或政治立场。

### 4.2 AWWA 明确把拨出资金分成基地关联侧与日本地方侧

AWWA 两份 990-EZ 的 Schedule O 对 Part I line 10 作了同口径拆分：

| AWWA 税期 | 日本组织 | 驻冲美军基地关联组织 | line 10 合计 |
|---|---:|---:|---:|
| 2022-06-01—2023-05-31 | USD 91,838 | USD 33,320 | USD 125,158 |
| 2023-06-01—2024-05-31 | USD 64,077 | USD 30,812 | USD 94,889 |

这两期支持把 AWWA 当作“基地组织资源与日本地方机构之间的分配中介”继续追踪。它们仍不是完整 Schedule I recipient 表：日本组织桶内只有部分具名 program-service 行，其他金额仍为汇总。

本包保留六个具名申报描述与金额，全部是 `research_only` recipient candidates：Children Kana-san Okinawa、Okinawa Nanbu Rehabilitation and Medical Center、NPO ARU、Ambitious、Himawari Day Care on Ishigaki Island、Okinawa Southern Medical Center。申报原文能证明“该描述与金额同列”，但组织身份、正式名称和中央 flow 尚待人工复核。

### 4.3 五份“最新申报”只能作混合税期量尺

选择每家当前最新的一份官方 XML，可机械得到：

- 收入行合计：USD 1,010,655；
- 支出行合计：USD 1,145,622；
- 已编码 grants-and-similar-paid 行的下限：USD 239,424；
- 共同口径的期末 net assets / fund balances：USD 625,527。

这五份申报横跨 2023-06-01—2025-06-30，且 OESC→AWWA 等内部转移尚未去重。因此它们只能说明五个已选组织的**低百万美元毛运作量级**，不能写成某一年度的生态总量、合并预算、人均数或冲绳全部服务支出。

先前约 USD 668,387 的“期末资产”粗数混用了 Form 990 的 `TotalAssetsEOYAmt` 和 990-EZ 的 `NetAssetsOrFundBalancesEOYAmt`。本包已退休该混合定义，改用五份申报共同存在的 net-assets/fund-balances 字段，得到 USD 625,527。

## 5. 明确保留的两个门禁

1. **KOSC USD 2,580 不升格。** KOSC FY2025 XML 的 Schedule I 把 “American Womens Welfare Association” USD 2,580 放在 individual-assistance group，而不是干净的 organization `RecipientTable`。本包只在 `W2A-CN007` 记录它，`anchor_candidates_v1.csv` 中没有 KOSC→AWWA USD 2,580 flow。
2. **MOSCO 最新 grants line 不强制写零。** 官方 XML 没有 `GrantsAndSimilarAmountsPaidAmt` 元素；本包记录“没有正值元素”与 `xml_zero_or_blank_semantics`，不把缓存渲染中的 0 当作已完成的字段语义判断。

## 6. 文件说明

| 文件 | 内容 |
|---|---|
| `anchor_candidates_v1.csv` | 83 条研究锚点；使用 `W2A-A###` |
| `source_receipts_v1.csv` | 15 条收据；使用 `W2A-SR###` |
| `change_notes_v1.csv` | 8 条口径／执行调整；使用 `W2A-CN###` |
| `official_index_matches_v1.csv` | 五个 EIN 的 2021—2026 相邻申报筛选表 |
| `cache_inventory_v1.csv` | 24 个既有第三方缓存文件的大小、SHA-256 与准入边界 |
| `raw/*.xml` | 14 份官方 IRS bulk XML 成员 |
| `validation_report_v1.json` | 行数、唯一键、哈希、KOSC 2580 门禁和无中央写回验证 |
| `package_manifest_v1.csv` | 本包除自身外所有文件的字节数与 SHA-256 |

CSV 使用 UTF-8 BOM，便于 Windows Excel 直接打开。金额保留原始美元整数，不换汇；税期按申报起止日记录，不按提交年替换。

## 7. 复现与验证

重新构建三张主表、索引摘录、缓存盘点与验证报告：

```powershell
python scripts\build_w2_00_spouse_990_v1.py
```

从官方压缩包重新抽取普通 Deflate XML 的形式：

```powershell
python scripts\extract_remote_irs_xml_v1.py `
  --url "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11A.zip" `
  --object-id 202443189349200514 `
  --output "outputs/us_presence_network_wave2_w2_00_spouse_990_v1/raw/awwa_fy2024_202443189349200514.xml"
```

NOSCO FY2025 的 IRS ZIP 成员使用 Deflate64。标准库不能解压 method 9；本轮把 `inflate64` 安装在忽略目录 `tmp/w2_00_python_deps`，再通过 `PYTHONPATH` 调用。无该可选依赖时，抽取器会明确退出，不会悄悄下载整份 494 MB ZIP 或退回第三方收据。

## 8. 负责人检查点结果

负责人于 2026-08-22 完成四项判断：

1. OESC→AWWA 三期 Schedule I 行全部确认为 `human_checked` research-only 锚点；
2. 四个“混合税期毛量级”可作为内部诊断和后续案例比较使用，必须保留精确口径标题；
3. 六个 AWWA 具名 recipient descriptor 全部进入 W2-A 身份、收款端与 LEG2 地方回应补查；
4. MOSCO 最新 grants 元素维持缺失语义，不改写为 0。

KOSC USD 2,580 继续 defer；AWWA 2022-05 期末申报继续记官方 index gap。W2-A 已放行研究层工作，中央事实和前端仍需另行授权。

## 9. 不得被主线程误读为

- 不是五家组织的合并年度财报；
- 不是全冲绳军属慈善／服务生态的总体；
- 不是 donor 名单，公开 990 通常不能穿透 Schedule B 捐赠者；
- 不是 AWWA 完整 recipient 年表；
- 不是服务或捐赠提升美军合法性的效果证据；
- 不是对组织“亲美／反美”的分类；
- 不是中央关系写回或前端发布授权。
