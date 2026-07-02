# MT-008 关系边事件化 note v0

日期：2026-07-03

**目标**：把静态的 actor-issue / actor-place 边升级成"事件感知"数据——即每条关系尽量挂上 `event_id`、`action_type`、`relation_strength`，从而区分长期组织定位、事件性署名、法律程序角色、公投参与等不同性质。

## 本轮产出：`actor_relation_events_v1.csv`

由 `scripts/make_relation_events.py` 生成，把已有的事件角色统一成一张表，覆盖 9 个事件、5 类 action、54 行：

| action_type | 事件 | 行数 |
|---|---|---|
| co_signing | 2010 WWF / 2015 NACSJ 共同署名 | 33 |
| request_letter | 2020 OEJP/MMC 共同要请 | 11 |
| litigation | 2003 Okinawa Dugong v. Rumsfeld | 5 |
| referendum | 2019 县民投票 / 1997 名护 / 石垣 / 与那国 | 4 |
| opinion_ad | 2012 与那国意见广告 | 1 |

字段：`event_id, event_name, event_year, action_type, actor_id, canonical_name, role, relation_strength, evidence_level, source_ref, interpretation_limit`。

`relation_strength` 取值：`one_off_co_signatory`（一次性联署）、`request_participant`（要请参与）、`named_plaintiff` / `plaintiff_counsel`（诉讼）、`referendum_initiator` / `referendum_committee`、`opinion_ad_committee`。

数据来源：co-action 部分从 `coaction_participants_v0.csv` 派生（不重复录入），诉讼部分从 `lawsuit_actor_role_table_v0.csv` 派生（只取有 actor_id 的原告/律师，个人原告不进网络层），公投/意见广告为手工 spec。

## 价值

- 同一个 actor 在不同事件里的角色现在可分开读：例如 A020 JELF 既是 2020 共同要请参与者（request_participant），又是儒艮诉讼原告（named_plaintiff）——静态议题标签看不出这种差别。
- `action_type` 让"共同署名"和"诉讼""公投"不再混为一谈，直接支撑 R5/R10/R11 的事件化叙事。
- 保守口径内置：`interpretation_limit` 每行标注"一次性联署≠稳定联盟"。

## schema 增强提案（下一版 edge 表）

建议给 `07_actor_issue_edges` / `08_actor_place_edges` 增补三列（默认可空）：

- `event_id`：关系若来自具体事件，回指本表 event_id；长期组织定位留空。
- `action_type`：`co_signing / request_letter / litigation / referendum / opinion_ad / protest / statement / administrative`。
- `relation_strength`：`one_off / repeated / sustained_core / named_plaintiff / …`。

暂不直接改写 07/08（避免破坏现有图脚本），先以本 `actor_relation_events_v1.csv` 作为事件层旁表；确认可用后再决定是否并入主边表 v1。

## 待办

- 补 2010/2015 联署里更细的 role（organizer / signer / host），目前统一为 co_signer_or_participant。
- 噪音诉讼（A052 嘉手納 / A053 普天間）与泡瀬诉讼可作为额外 litigation 事件补入。
- 抗议/直接行动（A019 现场、A060 高江）作为 protest action_type 补入。
