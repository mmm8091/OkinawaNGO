# USN 第一轮五项研究架构检查点：研究支持与决策建议 v1

日期：2026-08-21

状态：四份正式人工任务已全部回传；项目负责人于 2026-08-21 按本稿建议确认五项架构决定。中央 actor、relation、source、person、publication adapter 与 frontend 均未写入。正式回传见 `docs/human_review_return_USN_architecture_checkpoint_v1.md`。

本稿修正 `us_presence_network_wave1_principal_checkpoint_v1.md` 中两处已被后续人审推翻的旧表述：合法化证据应为 LEG0–LEG3，而不是把 L2 直接称为社会效果；人物 tracer 不再把 USAA005 的错误端点 A019 写入主线。

## 一页拍板表

| 项目 | 负责人决定 | 获批架构表述 |
|---|---|---|
| USN-ARCH-01 功能编码位置 | `accept` | 功能附着于有日期、对象和来源的行动／关系，不新增 actor 级亲美／反美或帮助／阻碍扩张标签 |
| USN-ARCH-02 合法化证据门 | `revise` | 采用与 E0–E4 正交的 LEG0–LEG3；LEG2 是有界地方反应，LEG3 才是态度／行为／制度效果 |
| USN-ARCH-03 9／6／2 报告框 | `revise` | 只保留为 `USF-US-ORIGIN17-2026-08-19` 冻结基线；不当作扩展后的完整分母，也不自动改成 15／6／2 |
| USN-ARCH-04 第一张人物 tracer | `revise` | 使用 A070/VFP-ROCK 具名人物与吉川秀樹的 A001/OEJP—A002/SDCC 同日 person bridge；删除 A019，event-only coalition 留在行动／协调层 |
| USN-ARCH-05 第一张资源网 | `accept` | 并列 AWWA／军属俱乐部、MTS／recipient、Earthjustice／Dugong case，严格保留 money、service-recipient、affiliation/channel 与 case-resource 分层 |

决定汇总：`accept 2 / revise 3 / defer 0`。

## 逐项边界

### USN-ARCH-01

四份回传均只批准具体身份、页面、职务、金额语义、服务／recipient、结构或行动事实，没有授权把组织固定编码成亲美、反美、维持或阻碍美国军事存在。负责人已接受该规则。

### USN-ARCH-02

服务侧 SR-HR-012 已由负责人确认 `revise_gate_with_explicit_rule`：

- LEG0：可核服务或资源转移事实；
- LEG1：行动方明示意图或公开叙事；
- LEG2：受益方、地方机构或独立媒体的有界接受、转述、抵制或重释；
- LEG3：有重复观察、基线／比较或明确研究设计支持的态度、行为或制度效果。

当前原 LC 表为9条 LEG1、3条 LEG0；另有可单独建立的 LEG2 research-only 候选，LEG3 为零。一次礼节性回应不等于 LEG3 效果，E0–E4 来源／证据等级也不等于 LEG 层级。

### USN-ARCH-03

`9 服务／6 问责／2 单列` 是 2026-08-19 冻结的17节点比较框，不是永久 actor universe。服务侧回传另批准 MTS、Marine Gift Shop、Neighborhood Pantry、NIOSC，以及 AER、AFAS 两个全国 actor 的地方 presence；这些对象须经受控 actor admission 与新版 selection-frame 决定后才可进入新分母，不能追溯改写旧框，也不能机械把服务组改成15。

### USN-ARCH-04

USHR003 已确认 USAA005 的 A019 是端点错配；正确目标是 `EO_R5_FUTAMI_TEN_DISTRICTS` 或保留 raw label，且继续 event-only/off-graph。第一张人物—组织二模图应只使用已确认的人物身份和点时角色：

- Charles Douglas／Doug Lummis → A070 VFP-ROCK；
- Peter／Pete Shimazaki Doktor → A070 VFP-ROCK；
- 吉川秀樹 → A001 OEJP 与 A002 SDCC 的 2021-02-08 同日职务观察。

VFP webinar 共现和 VFP-ROCK 与 coalition 的协调分别留在事件／行动层；人物共享不生成 A001↔A002 组织联盟边。撤回此 tracer 中的 A019 不否定 A019 作为既有 registry actor。

### USN-ARCH-05

负责人已接受三类资源路径并列；执行时继承以下人审边界：

- KOSC→AWWA 的 USD 2,580 暂缓，不建立精确组织 flow；OESC→AWWA 的 USD 8,479 只作 2024-07-01—2025-06-30 有期申报 flow；
- MTS—AWWA 拆成 membership 与 grant-selection/distribution channel，任何年度金额另建；MTS／recipient 保持 service-recipient 与身份 crosswalk 分离；
- Earthjustice 的 USD 276,345.50 Form 990 court-award amount 与 Judgment Fund USD 280,000 付款记录分开；付款机制未闭合前不建立 OSD→Earthjustice 简单资金边。

## 拍板后的受控动作

下一步首先交付“受控集成设计＋预期字段级 diff＋幂等测试方案”，而不是立即手改中央 CSV。该设计须覆盖四份 return 的 source proposals、actor／person／recipient／relation 分表、43行规则展开及所有 defer/reject/off-graph 边界；负责人再决定是否实际中央写入。

随后才可一项一停推进 USN-04 人物 tracer、USN-05 分层资源路径和 USN-06 公共外交／地方反应。三者先生成 research-only 包，各自经过解释检查点后才考虑 publication adapter 或前端。
