# Phase-1 module source integration v1

- 主来源表当前共 198 条；本轮集成 39 条（S160–S198）。
- 模块来源交叉表共 57 条，覆盖 R4／R9／R10 的全部 57 条可用来源记录。
- S160–S198 归档结果：archived 37、failed 2。
- 当前失败项：S197, S198；保留失败状态，不作为来源失效或证据否定。
- 新来源统一保持 `ai_seeded`；已有来源保留原 review status 与元数据。
- `relation_or_claim_approved=no`：来源入表与归档不批准 actor relation、金额、角色或解释性结论。
- HR-016、HR-017、HR-018 仍分别控制语义／角色／敏感行政与资金关系；HR-022 控制 49 个来源元数据／支持范围项。

运行 `python scripts/integrate_phase1_module_sources.py` 可幂等复现。
