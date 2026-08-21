# USN 第一轮五项研究架构检查点——负责人回传 v1

日期：2026-08-21

负责人：`project_principal_user`

状态：五项全部完成决定（`accept 2 / revise 3 / defer 0`）。四份正式人工任务与本架构检查点现已全部闭环；中央数据、publication adapter 与前端尚未写入。

## 决定

| 项目 | 决定 | 获批规则 |
|---|---|---|
| USN-ARCH-01 功能编码位置 | `accept` | 功能附着于有日期、对象和来源的行动／关系，不新增 actor 级亲美／反美或帮助／阻碍扩张标签 |
| USN-ARCH-02 合法化证据门 | `revise` | 采用 LEG0–LEG3：事实、行动方叙事、地方有界反应、可重复效果四级分离 |
| USN-ARCH-03 9／6／2 报告框 | `revise` | `USF-US-ORIGIN17-2026-08-19` 保留为冻结基线；不追溯加入新 actor，也不自动改成15／6／2 |
| USN-ARCH-04 第一张人物 tracer | `revise` | 使用 VFP-ROCK 具名人物及吉川秀樹的 OEJP—SDCC 点时 person bridge；从 USAA005 tracer 删除 A019，event-only coalition 留在行动层 |
| USN-ARCH-05 第一张资源网 | `accept` | AWWA／军属俱乐部、MTS／recipient、Earthjustice／Dugong case 分层并列，不压成同一种 funding edge |

## 必须继承的边界

1. LEG2 的单次接受、转述、抵制或重释不是 LEG3 社会效果；当前 LEG3 为零。
2. 17节点冻结框是版本化比较分母，不是永久 actor universe；新服务 actor 须另建新版 selection frame。
3. A019 的撤回只修正 USAA005 错配，不否定 A019 作为既有 registry actor。
4. 人物共享、webinar 共现和 coalition coordination 不生成组织联盟边。
5. KOSC 的 USD 2,580 暂缓；OESC 的 USD 8,479 只作有期申报 flow；Earthjustice 的 USD 276,345.50 与 Judgment Fund USD 280,000 分开，均不得被压成未经证明的简单付款边。
6. MTS—AWWA membership、grant-selection/distribution channel、每年金额及 MTS／recipient 服务事实分别编码。

## 机器契约兼容状态

`outputs/us_presence_network_architecture_v1/` 的派发前 CSV 仍使用 `L1/L2/L3` 后缀作为旧机器别名。负责人批准的是 LEG0–LEG3 语义；旧别名不得被解释成不同门槛。由于本轮表格运行时不可用，机器码改名留作后续机械迁移，并须保持70项词表、44条门禁和10个纵向切片的行数与非目标字段零漂移。

## 授权范围

本次拍板授权下一步编写“受控集成设计＋预期字段级 diff＋幂等测试方案”。它不等于授权直接修改中央 actor／relation／source／person 表，不授权 publication adapter 或前端发布。

机读决定：`outputs/us_presence_network_architecture_v1/principal_checkpoint_return_v1.json`。
