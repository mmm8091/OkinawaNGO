# R10 可视化草图 v0

## 推荐图：行政关系机制分面图

不要画成单一“资金网络”。推荐用四个并列面板，每条边按关系机制着色，只有 `documented_payment_flow` 使用金额宽度：

```text
[A 委托 / designated]
JICA ──受托・金额不公开──> ONC
MOFA ──NGO相談員・指定──> ONC
Okinawa City ──KIP委托费──> ONC
Okinawa Prefecture ──多文化会议支援──> ONC

[B 国际交流 / 服务]
Okinawa Prefecture ──服务──> 世界若者ウチナーンチュ連合会
Okinawa Prefecture ──服务──> 青年海外协力协会冲绳事务所

[C grant]
Okinawa Prefecture ──补助关系・award金额待核──> 冲绳县国际交流・人才育成财团

[D non-funding / joint role]
Okinawa Prefecture ──共同实施──> 冲绳和平协力中心
Okinawa Prefecture ──会议事务局──> ONC
```

### 视觉编码

- 实线深蓝：`commission`，但线宽只在 `documented_payment_flow` 时按金额缩放。
- 细虚线蓝：`commission` 或 `designated_role`，金额未知或只有 project cost。
- 绿色：`grant`；若只有 whole project cost，则固定宽度并加 `award amount unresolved`。
- 橙色：`service`，不表达资金。
- 灰色点线：`non_funding_relation`。
- 复合受托体使用双边框节点，禁止把总项目费拆给成员。

### 必须显示的金额脚注

> 图中“project cost”是行政表或组织年报的项目总成本观察，不等于合同支付额。只有冲绳市资金流表明确标示的 KIP `委託料` 可作为 documented commission payment flow。相同项目的行政侧和组织侧数值并存时不平均、不相加。

### 备选图：ONC 口径对照时间线

```text
2019 KIP 市资金流：17.157m（委託料）
2020 KIP 市资金流：16.970m（委託料）
2024 KIP 市资金流：16.662m（委託料）
2024 KIP ONC年报：16.040m（project cost）  ← 不同口径
2024 县多文化表：5.140m（whole project cost）
2024 ONC年报：5.530m（project cost）       ← 不同口径
2024 MOFA相談員 ONC年报：2.894m（project cost）
2026 MOFA相談員：指定持续，金额不公开
```

此时间线的解释重点是制度角色连续性和会计口径差异，不是比较“谁拿钱更多”。
