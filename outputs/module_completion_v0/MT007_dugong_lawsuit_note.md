# MT-007 儒艮诉讼原告映射 note v0

日期：2026-07-02

**目标**：把美国 Okinawa Dugong 诉讼里的各方对应到有来源支撑的法律角色，避免误配（尤其不把 A002 SDCC 写成原告）。

## 案件

- **Okinawa Dugong v. Rumsfeld**（后续 Gates / Mattis / Esper），No. C 03-4350 MHP，美国加州北区联邦地方法院，2003-09-25 提起；依据《国家历史保护法》(NHPA) 第 402 条。
- 上诉延续为 **Center for Biological Diversity v. Esper**（第九巡回上诉法院，2020）。
- 一手 docket：`https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_03-cv-04350/`（court PDF 为扫描件、机读受限；原告 caption 经 WebSearch 引court文书 + 案例摘要与 JELF 自述互相印证）。

## 角色判定（见 `lawsuit_actor_role_table_v0.csv`）

- **原告（组织）**：Center for Biological Diversity (A045)、Turtle Island Restoration Network（未入表）、日本環境法律家連盟 JELF (A020)、ジュゴン保護基金委員会 / Save the Dugong Foundation (A076)。
- **原告（个人）**：Anna Shimabukuro、東恩納琢磨、真喜志好一。
- **律师 / counsel**：Earthjustice (A009) —— 代理律师，**非原告**。
- **非当事方**：ジュゴン保護キャンペーンセンター SDCC (A002)（倡议组织，非原告）；ヘリ基地反対協議会 (A019)（现场运动组织，非原告）。
- **被告**：美国国防部。

## 收口的悬案

1. **A076 原告身份确认**（HR-001/HR-004 曾标"未确认"）：A076 是 named plaintiff，E4。
2. **A002 非原告**：再次确认 A002 SDCC 与原告 A076 是两个主体，A002 不写成法律原告。
3. **A019 组织非原告**：A019 是现场运动组织，不是诉讼当事方；其共同代表東恩納琢磨为个人原告（人—组织不等同）。
4. **A020 JELF 是原告不是律师**：MT-007 澄清 JELF 的角色是 co-plaintiff，代理律师是 Earthjustice。

## 待办

- **Turtle Island Restoration Network 未入 actor registry**：作为美国 NGO 原告，建议作为 R10/R11 法律—原告层的候选 actor（signatory/plaintiff 证据 E4）。
- 个人原告（3 人）只登记在本诉讼角色表，不进 org registry。
- 已把 A076、A020 的 registry note 补上确认的法律角色（不改动其组织身份 evidence_level）。
