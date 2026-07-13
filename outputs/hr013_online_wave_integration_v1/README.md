# HR-013 与下一轮线上来源主线程合并 v1

- Registry：118；A094 按 HR-010 范围勘误移出，A111 按 HR-013 加入，净数不变。
- Source log：247；本波 70 条来源引用归并为 67 个 URL，其中 49 个为 S199 以后新增来源。
- Actor–issue：222，其中 A111 仅有 4 条 HR-013 人工批准观察。
- Actor–place：125；A111 仅落 P001 全县场域。
- Event/venue：65；新增 AEV0065 为 2024 县民大会组织角色。
- 来源交叉表：70 条，全部 `relation_or_claim_approved=no`。
- 54 条 post-HR013 edge-activation 候选仍在人工任务队列，未写入 actor–issue 主表。
- C010/C034 仅作背景节点，C029–C033 明确 out_of_scope；均不占 actor registry 计数。
- `okinawajosei.org` 归属おきなわ女性財団，只作第三方项目记录；A111 不接收 `沖女連` 别名。
- A094 的历史基地行动证据保留在取证谱系中；移出是本期范围决定，不是宣称其从无相关行动。

运行 `python scripts/integrate_hr013_online_wave.py` 可幂等复现。
