# USN-HR-02：美国来源问责节点补强复核

日期：2026-08-19

任务量：9 项；建议先做 P0 四项

回填表：`outputs/us_presence_accountability_recon_v1/human_review_queue_v1.csv`

## 本轮要判断什么

这批材料把六个“美国来源／参与问责”的 actor 拆成案件组织、在地退伍军人章节和一次性国际声明参与者，并补出人物、案件资源与协调关系。请在回填表填写：

- `principal_decision`：`accept`／`revise`／`defer`／`reject`；
- `principal_note`：接受范围、修改内容或缺失材料。

只批准 `linked_rows` 指定的字段与命题，不连带批准组织立场、一般资金关系或稳定联盟。

## P0：决定第一张人物—组织—案件图能否做

### USHR001 Earthjustice 案件资源

- 材料：Earthjustice FY2021 Form 990，PDF 第 54 页 Schedule O。
- 观察：`1272 OKINAWA DUGONG` 出现在十大 `court-awarded attorney fees & costs` 中，金额 276,345.50 美元。
- 建议：接受“Earthjustice 报告了一项案件级法院判给律师费／成本金额”；付款方、fee order、收款链条继续 `defer`。
- 不应改写成：捐赠、项目预算、Earthjustice 支出、冲绳组织付款或一般 grant。

### USHR002 A070 VFP-ROCK 身份与连续性

- 材料：VFP 2020 章节目录、2021 官方活动页、2023 官方会报。
- 观察：三份 VFP 自有材料分别确认 chapter 1003、负责人／协调人和持续公开活动。
- 建议：按三个观察日期接受 A070 章节身份与连续出现；不要推成 2020–2023 每日连续任期。

### USHR003 A070 → A019 协调

- 材料：VFP 2023 春季会报第 23 页。
- 观察：chapter 1003 自述继续与包括 No Heliport Base Association 在内的 coalition 工作。
- 建议：接受有界的 recurring coordination；关系类型不是 membership、funding 或完整联盟名单。

### USHR004 吉川秀樹人物桥

- 材料：VFP 2021 官方活动页的讲者简介。
- 观察：同一段简介、同一观察日同时写明其在 A002 SDCC 与 A001 OEJP 的公开职务。
- 建议：确认同一人物及两个同日职务；时间只按 2021-02-08 观察，不自动生成完整任期。

## P1：边界与未解析端点

### USHR005 Network for Okinawa

CBD 官网使用该英文名，但现有材料不足以仅凭名称并入 A028/JUCON。建议 `defer`，保留原文端点。

### USHR006 两个英文 coalition 标签

`Protect Henoko/Takae` 与 `Henoko Anti-Base Project` 暂无独立 identity crosswalk。建议 `defer`，不映射现有 actor。

### USHR007 A033／A042 的冲绳持续性

当前可核的是 2015 NACSJ 共同声明；本轮各自官网检索未找到持续冲绳项目。建议接受“事件参与可证、持续项目待证”的范围判断。

### USHR008 X013 公共外交 NOFO

现有材料只有 2024 Okinawa Youth Council Program 的机会与额度区间，没有 named award／recipient。建议继续留在线索层，不建资金边。

### USHR009 X014 NED

本轮 NED 官方 grant-list 检索未找到冲绳／日本 recipient。建议只接受“本轮官方列表未找到”的负检索记录，X014 保持观察节点。

## 主要证据入口

- Earthjustice 990：`https://earthjustice.org/document/irs-form-990-fy2021`
- CBD 项目页：`https://www.biologicaldiversity.org/species/mammals/Okinawa_dugong/`
- CBD 起诉公告：`https://www.biologicaldiversity.org/news/press_releases/dugong9-25-03.html`
- VFP 2020 章节目录：`https://www.veteransforpeace.org/files/1415/8938/5791/20.05.13.ChapterContact.pdf`
- VFP 2021 活动页：`https://www.veteransforpeace.org/who-we-are/member-highlights/2021/02/08/okinawa-understanding-history-and-resistance-us-militarism`
- VFP 2023 会报：`https://www.veteransforpeace.org/files/8616/8433/7175/VFPNews_2023.Spring-FULL_SMALL_FIN.pdf`

## 完成标准

- 9 行均填 `principal_decision`；
- `revise`／`defer` 有说明；
- USHR001 分开“金额类别已证”与“付款方未证”；
- USHR002／004 使用观察日期，不自行补完整任期；
- USHR003 不升级为 membership／funding；
- USHR005／006 未解析名称不强行并入 actor；
- USHR008 不把机会写成 award。
