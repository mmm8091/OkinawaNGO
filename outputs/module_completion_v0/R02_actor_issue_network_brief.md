# R2 组织-议题网络 brief v0

## 当前完成度

R2 已达到 `module_v0`：已有 actor-issue edge 表、Top bridge actors 图、桥接组织清单。

## 可交付图件

- `outputs/explanatory_v0/fig_actor_issue_bridge_network.png`
- `outputs/module_completion_v0/R02_bridge_actor_shortlist_v0.csv`

## 当前可讲结论

1. 当前网络中，反基地不是孤立标签，而是经由环保、法律、地方自治、国际倡议和生活安全等框架扩展。
2. 桥接 actor 分成三类：本地运动 / 法律节点、日本国内 NGO / 倡议节点、海外签名 / 国际倡议节点。
3. 该图只能说明“公开资料中的议题连接”，不能说明组织长期主打议题，也不能把共同署名写成稳定联盟。

## Top bridge actors

- A045 Center for Biological Diversity：连接 biodiversity;international_advocacy;legal；状态 `ai_seeded`。
- A048 沖縄一坪反戦地主会：连接 anti_base;legal;local_autonomy；状态 `ai_seeded`。
- A050 沖縄弁護士会：连接 anti_base;legal;local_autonomy；状态 `ai_seeded`。
- A052 嘉手納爆音訴訟原告団：连接 anti_base;legal;life_safety；状态 `ai_seeded`。
- A053 普天間爆音訴訟団：连接 anti_base;legal;life_safety；状态 `ai_seeded`。
- A066 新外交イニシアティブ（ND）：连接 anti_base;legal;local_autonomy；状态 `ai_seeded`。
- A006 グリーンピース・ジャパン：连接 anti_base;biodiversity；状态 `ai_seeded`。
- A007 ピースボート：连接 anti_base;international_advocacy；状态 `ai_seeded`。

## 还需要继续做

- 给 actor-issue edge 增加 `event_id` / `action_type` / `relation_strength`。
- 区分长期组织定位、事件性署名、法律程序角色。
- 对 `needs_second_source` 的桥接 actor 优先补证。
