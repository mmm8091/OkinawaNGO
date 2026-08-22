# USN Wave 2 information-disclosure pilot design v1

日期：2026-08-22
状态：`planning_only / draft_not_sent / research_only`

## 问题

能否把三项现有信息公开草稿收缩为一个低成本、可复核、不会要求机关新造统计表的小型试验？试验只检验**既有记录的可见性与保有层级**，不预设任何资金流、地区分配、补贴或隐瞒事实。

本包使用美国司法部、WHS、美国海军陆战队、美国空军、防卫省、冲绳防卫局和 e-Gov 的官方入口。它不发送请求、不注册账户、不致电机关，也不修改中央事实层、publication adapter 或前端。

## 先纠正一处费用说法

“非商业研究”不是一个自动统一的费用类别。

- 若请求确实由教育机构或非商业科学机构授权、并用于其学术／科学研究，通常只就超过首 100 页的复制收费，不收检索或 review 费；机构身份和研究用途要能据实说明。
- 其他非商业请求人可获首两小时检索和首 100 页复制的法定免费额度；之后可能支付检索和复制费。
- fee waiver 是另一套门槛：请求人须说明披露很可能显著增进公众对政府运作／活动的理解，且不主要服务于其商业利益。不能仅以“没有预算”申请。

因此本项目不能预填“教育科研”或 fee waiver。最小试验应由负责人按真实身份选择类别；不能证明机构授权时，先用 `all_other/non-commercial`，设费用上限并要求估价后协商缩窄。

## 结论：建议的最小可行发送批次

建议把三份大草稿改为**三个单年度、单一保有层级、只请求既存记录的微型请求**。这样既保留 W2-F 所需的三条公开记录路线，也避免把“请解释钱去哪了”写成机关必须新造答案。

| 微请求 | 首投机关 | 先请求什么 | 为什么足够小 | 当前发送条件 |
|---|---|---|---|---|
| `MVP-01` | WHS OSW/JS FOIA | `HQ00342310002` 的 award instrument/附件/修改，以及已保有的 SF-425、progress/performance report 中含地区、国家、site 或 center 字段者 | 有 FAIN、prime recipient、日期和授奖办公室；不要求 WHS 新做 Okinawa 分配表 | 负责人填真实 requester 类别、费用上限、联系方式和实际截止日期 |
| `MVP-02` | MCIPAC/MCB Camp Butler record custodian | 仅一个最近完整 retail FY 的既有 installation-level balance sheet 与 operating statement/P&L（或其实际标题）；另要 cover sheet／custodian locator | 把五年、审计、预算、成本中心、各类转移拆开；先判本地是否保有账表 | 提交前在实时门户确认 MCIPAC 路由；负责人填真实费用类别与上限 |
| `MVP-03` | 冲绳防卫局长 | 经事前咨询确认后的 FY2024（令和6年度）、一个保有部课、一个既存预算—执行或合同执行汇总表及字段说明 | 日本侧请求费按文书／保有部课／年度计算；先以一年度判定文件名和复制方式 | 先完成非正式电话咨询，确认文件名、部课、件数和印纸金额，再邮寄／柜台提交 |

这不是发送授权，也不等于 W2-F 已解除。它只说明：若负责人日后决定实际发出，应优先发这三个缩窄版，而不是现有五年宽口径版本。

## 入口与制度边界

详见 [official_rules_matrix_v1.csv](official_rules_matrix_v1.csv)。关键入口为：

- WHS 接受电子、邮寄或传真提交，且只处理 OSW/JS 控制的记录；记录在其他 DoD component 时应直投持有机关或接受转送。
- USMC 官方说明要求尽可能直投实际保有记录的 command；其页面还要求联系方式、具体描述、愿意支付的金额及（如适用）fee-waiver 依据。
- USAF 的 PAL 是 Air Force 持有记录的线上入口；注册页显示费用类别下拉项，但它不是本次三项请求的默认路线。
- 防卫省／冲绳防卫局的正式行政文书开示不是电话、传真或电邮提交；地方防卫局保有的文书由该局信息公开窗口受理。请求费为每行政文书 300 日元；决定后再按实施方式缴纳复制／阅览／邮寄费。

“电子记录”是可请求的行政文书类型；但在已核的防卫省工作流中，**正式递交**仍是表格的柜台或邮寄，且并不保证以 Excel/CSV 交付。请求文本可表达“若机关已保有电子副本，希望按现有电子形式复制”，最终实施方法以开示决定后的机关说明为准。

## 返回与拒绝如何编码

每一回复先进入 [response_visibility_coding_v1.csv](response_visibility_coding_v1.csv) 的 request ledger，不直接变成资金、关系或政治结论。

只有满足下列条件，负面结果才可写成有界的“可见性结果”：请求有日期、保有机关、期间、文件描述和正式书面答复；并保存案号／受付番号、全文、任何转送或补正往来。

允许的写法示例：

> 在声明的机关、期间和文件类型内，机关以正式 `no_records`／`not_held`／`partial_withholding` 回应；这说明该记录在该公开程序中的可得性，不证明底层资金、服务或地区分配不存在。

不得写成“政府没有这笔钱”“机关隐瞒了资金”或“拒绝本身证明合法性效果”。

## 本包交付

- `official_rules_matrix_v1.csv`：官方规则与入口的逐项核验；
- `request_readiness_matrix_v1.csv`：三份现有草稿的缩窄建议和发送前条件；
- `minimum_viable_batch_v1.csv`：三条微请求的发送顺序；
- `response_visibility_coding_v1.csv`：回函／拒绝／费用／转送的编码规则；
- `principal_checkpoint_v1.md`：负责人日后真正发送前应审的最小选择；
- `unexpected_findings_register_v1.csv`：本轮无额外侦察线索，保留空表头。

## 复现与验证

```powershell
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_information_disclosure_pilot_v1
```

## 意外发现登记

本轮 0 条。费用类别与可见性结果均直接服务于本包问题，已写入主研究设计而非 `lead_only` 线索簿。

## 不得误读为

- 没有实际发送任何 FOIA 或行政文书开示请求；
- 不声称负责人符合教育机构、非商业科学机构、新闻媒体或 fee-waiver 资格；
- 不声称三机关一定持有或会披露请求文件；
- 不把未来 `no records`、转送、费用估价、部分不公开或无回复解释为底层资源流是否存在；
- 不构成 W2-F 放行、中央写回或前端发布授权。
