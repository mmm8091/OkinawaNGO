# HR-035 Batch 01 人工复核回传（负责人已确认）

日期：2026-07-20

任务：案件、公投和制度程序 actor–issue 事实冻结

状态：**负责人已于 2026-07-20 确认本批全部 15 条建议；可交主线程受控合并**

## 1. 回传文件

- 实际填写表：`outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv`
- 更新后的逐来源辅助表：`outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch01_v1.csv`
- 可重放填写脚本：`scripts/apply_hr035_batch01_ai_assist.ps1`

工作表已写入 `human_reviewer=project_principal_user`、
`review_date=2026-07-20`。本报告只批准本批 actor–issue 事实决定；中央表和派生包仍须由主线程
按任务说明受控合并与重生。

## 2. 辅助判断总览

| edge | actor—issue | 建议 | 最终证据 | 核心判断 |
|---|---|---:|---:|---|
| AI021 | Earthjustice—international_advocacy | revise | E4 | S128 明列 Earthjustice 律师为原告上诉人代理；不是 plaintiff |
| AI025 | A011—referendum | accept | E3 | S018/S019 闭合签名、直接请求和议会程序 |
| AI027 | A011—anti_military | accept | E3 | 只表示介入石垣陆自部署争议，不是一般反军事定位 |
| AI048 | JELF—legal | revise | E4 | Dugong=plaintiff/appellant；Awase=supporter/host |
| AI049 | JELF—biodiversity | accept | E4 | 只接受 2020 MMC 请求／报告事件 |
| AI050 | JELF—dugong | revise | E4 | 补入诉讼来源；诉讼与 2020 MMC 事件分开 |
| AI106 | CBD—legal | revise | E4 | S128/S129 caption 取代错位的 S004 |
| AI126 | A051—Henoko | revise | E4 | S185 闭合组织—请求角色；限 2018–2019，继承解散边界 |
| AI127 | A051—local_autonomy | revise | E4 | 只表示该次直接请求／县民投票程序 |
| AI129 | 嘉手纳原告团—life_safety | accept | E3 | 噪音、睡眠、健康风险和生活损害进入第三次诉讼 |
| AI132 | 普天间诉讼团—life_safety | accept | E3 | 人格权／生活损害进入第二次诉讼；差止未获支持 |
| AI164 | A068—anti_base | revise | E3 | 正式全称、1997 程序和谱系边界须同时保留 |
| AI178 | 沖縄防衛局—anti_base | reject | E4 | 实施者／行政端点／争议对象不等于反基地立场 |
| AI231 | 宜野湾ちゅら水会—legal | revise | E4 | 当前中央来源只冻结到 2022 请愿；后续调停需登记来源 |
| AI241 | 新婦人沖縄県本部—referendum | accept | E3 | 只接受 2018 冲绳县本部签名动员 |

建议计数：

- `accept`：6
- `revise`：8
- `reject`：1
- `defer_second_source`／`defer_local`：0

## 3. 三条重点结论

### AI106：CBD—legal

原 `source_ref=S004` 确属错位。S004 是 2015 年共同声明，不能证明诉讼角色。

已渲染并目视核验 S128 第九巡回法院判决首页：

- `CENTER FOR BIOLOGICAL DIVERSITY` 位于 `Plaintiffs-Appellants` caption；
- JELF、Turtle Island Restoration Network、Save the Dugong Foundation 同列组织原告；
- S129 的 2020 年终局判决 caption 继续列示该角色。

因此建议 `revise`，将本 edge 来源改为 `S128;S129`。安全表述仅为冲绳儒艮案具名组织
原告／上诉人；不得写成 counsel，也不得把 2017 发回或 2020 终局写成停工。

### AI164：A068—anti_base

S042 只闭合公投及反对票多数，不能单独识别组织。S192 冲绳县官方沿革材料闭合：

- 1997 年事件期组织名和宫城康博代表；
- 请求代表证明、签名、直接请求、条例和投票程序；
- 1997-10-18 后继的反基地组织成立节点。

工作表据此使用完整事件期名称
`ヘリポート基地建設の是非を問う名護市民投票推進協議会`，而不是旧工作名
`名護市民投票の会`。

建议仍只到 E3：程序角色有 E4 支持，但 A068 的精确反基地立场及其向 A019 的发展性
改组／后继谱系不能由相邻时间点静默合并。A068 只限 1997 年，A019 后续行动不得回填。

### AI178：沖縄防衛局—anti_base

S047 确认沖縄防衛局承载普天间替代设施建设环境影响评价等工程／行政角色，却没有任何
反基地立场证据。

建议：

- `human_decision=reject`
- `claim_status=unsupported`
- `scope_revision_required=yes`

可以在程序、行政或 target 层保留沖縄防衛局，但必须从无 polarity／role 的 actor–issue
立场网络中排除。HR-019 的 `implementer_or_dispute_target` 解释若要保留，应迁出这条
`anti_base` 事实边。

## 4. 其他来源修订

- AI021：`S009` 增补 `S128`，用官方判决固定 Earthjustice counsel 角色。
- AI048：原 `S006;S007` 不能承担 legal 边；改为 `S061;S128;S142`。
- AI050：保留 `S006;S007` 的 2020 MMC 事件，并补 `S061;S128` 的诉讼 plaintiff 角色。
- AI126／AI127：S025 只证明投票问题与结果；补 `S185` 闭合 A051 的组织身份及请求代表
  角色，解散边界另继承 LC001。
- AI164：补 `S192` 闭合正式组织名和程序链。
- AI129／AI132：事实可接受，但 S026/S027 是新闻而非法院判决原文，证据从 E4 下调 E3。

逐来源辅助表已按修订后的 `source_ref` 重生为 29 行，不再保留与当前建议不一致的来源包。

## 5. AI231 的在线补查

本轮不是因为“没有调查”而删去 2025–2026 调停事实。在线补查确认：

- 宜野湾市截至 2026-03-27 仍把 2022 年 PFAS 血液检查请愿列为审查中：
  `https://www.city.ginowan.lg.jp/shisei/gikai/5/14043.html`
- 沖縄タイムス 2025-10-28 报道宜野湾ちゅら水会等三团体于 10 月 27 日申请公害调停：
  `https://www.okinawatimes.co.jp/articles/-/1700743`
- OTV 2026-02-22 报道该申请因防卫设施适用除外被程序性驳回：
  `https://www.otv.co.jp/okitive/news/post/00015363/index.html`

但后两条尚无中央 source ID 和本地归档，HR-035 的问题是“现有中央来源能否冻结事实”。
因此 AI231 建议 `revise`：当前只冻结 S273/S274 支持的 2022 请愿／委员会程序；待后续
来源登记与归档后，再把 2025–2026 公害调停补回正式范围。程序性驳回不得写成 PFAS
实体主张败诉。

## 6. 负责人确认

负责人于 2026-07-20 确认整批建议：

1. 接受 6 条、修订 8 条、拒绝 AI178；
2. AI027 保留为“特定石垣陆自部署争议介入”，不解释为一般反军事立场；
3. AI164 冻结到 E3，并保持 A068/A019 谱系分离；
4. AI231 暂只冻结 2022 请愿，2025–2026 调停待中央来源登记；
5. AI178 要求单独修订 HR-019 scope 的数据落点。

主线程合并时才可重生 R1/R2、strict place–issue、coverage 和探索系统；本轮未直接修改中央
actor–issue 表，也未新增 actor、组织关系、资金关系、联盟或因果结论。
