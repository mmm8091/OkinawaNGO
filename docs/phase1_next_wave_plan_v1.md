# 一期下一轮线上推进与子线程回收计划 v1

日期：2026-07-13

起点提交：`3fe5c38`
验收权威：`source_docs/current/复归后冲绳民间组织 _ NGO 分类与议题网络一期研究方案 (3).docx`

## 1. 本轮判断

本轮三条线上执行线已回收。HR-013 以 A111 替换范围不符的 A094，主 registry 仍为 118 个 organization-level actor，低于方案 120–180 的下限。当前底盘为：

- 222 条 actor–issue edge：101 个 actor 已连接、17 个仍 edge-isolated；59 条 human-reviewed、163 条 candidate；scope 为 43 positioning、40 case/institution、74 event、65 unclear；
- 125 条 actor–place edge；65 条 AEV，其中 61 条 human-checked、4 条 analytical seed；
- 247 条 source：224 archived、2 manual_archived、19 failed、2 non-URL；
- human-review log 40 行；HR-016–HR-024 的未决字段继续留空。

结论仍是先补现有样本的数据联接，再按模块缺层扩样。最终仍须恢复 120 下限，但不得以一次署名、名称相似、一般公益使命或已被人审剔除的主体凑数。

## 2. 三条并行执行线

### A. 现有 actor 的议题边激活 — online pass completed

原对象为 A073、A076、A086、A087–A101；HR-013 撤出 A094 后，post-HR-013 正式回收对象为 17 个在表 actor。

结果：17/17 已有在线结论，形成 54 条 `ai_seeded` candidate edge 和 38 条来源记录；这些边未并入主 actor–issue 表。A087-A093、A095-A101 的 47 条补证项回送 HR-010；A073、A076、A086 的 8 条新项目进入 HR-024，所有人工决定字段留空。

交付目录：`outputs/edge_activation_v1/`。其中 `post_hr013_*` 是当前有效版本；原始 18 actor 文件保留为检索轨迹。

下一门槛：HR-010／HR-024 逐条人工接受、修订或拒绝后，才可合并候选边并重生 R1/R2；不得从 registry `issue_tags` 自动生边。

### B. 9 个扩样候选的 count-ready gate — completed and superseded by HR-013

对象：`outputs/R01_R02_actor_issue_v1/registry_expansion_candidates_v1.csv` 的 9 个候选。

机器 gate 已完成身份／持续性、origin layer 和一期直接连接检索，但其建议现已被人工决定覆盖：

- C011 以 A111 入表；同时按 HR-010 范围修正撤出 A094，registry 净数仍为 118；
- C010、C034 只作 background actor；C029-C033 `out_of_scope`／`rejected`；
- C015 仍是 HR-011 defer，reopen addendum 只是补证包，不构成加入决定；
- `okinawajosei.org` 属 `公益財団法人おきなわ女性財団`，不是 A111 官网；A111 不接歧义简称 `沖女連`。

交付目录：`outputs/registry_expansion_gate_v1/`。机器 gate 与 evidence addendum 保留为审计轨迹，不再代表待定入表建议；未建立重复 HR-025。

### C. R8 六案法律／程序比较 — completed

对象：HR-014 已审核的 6 案和 27 条角色。

结果：已形成 case × channel × place × role × result 的 27 行比较矩阵、两张解释图和 brief；覆盖六案、13 个 registered-actor role 与 14 个 provisional node role。

交付目录：`outputs/R08_legal_procedure_v1/`。

验收边界已保持：plaintiff／counsel／requester／supporter／non-party、组织／个人／provisional node 分离；泡濑两波相反结果分开；图不是胜败排行或因果效果图。该包没有新建 HR-026。

## 3. 主线程回收状态与下一步

1. 三包覆盖、计数、来源定位、空白 HR 字段、脚本和图件已完成主线程验证。
2. 新 URL 已去重进入 source log；来源扩至 247 条。来源入表仍不批准 edge、actor 或解释。
3. 新来源已归档并校验：224 archived、2 manual_archived、19 failed、2 non-URL；失败只表示访问状态。
4. HR-013 已落库；A111 的 4 条议题边、1 条地点边和 1 条事件记录进入 human-reviewed 层，A094 及其候选补证从 post-HR-013 包撤出。
5. A 线的 54 条候选边继续等待 HR-010／HR-024，不自动合并；B 线只剩 C015 defer；C 线 R8 v1 已接入验收矩阵和报告。
6. 下一轮先复核现有候选边，并单列评估能修复薄层的组织级候选，优先 `宮古島地下水研究会` 等具有地下水—部署直接连接的持续组织。

## 4. 下一轮分支

- C015 继续 defer；不降低门槛。围绕薄议题和地点做下一轮组织级检索，优先 labor、women/human-rights、PFAS/health、Miyako groundwater/life-safety 和持续性本地组织。
- HR-010／HR-024 完成后：重生完整 actor–issue 网络、共现和 bridge mechanism；检查当前 17 个孤立 actor 是否真正减少。
- 新候选只有同时满足“组织持续身份＋一期直接连接＋修复模块缺层”，并经人工决定后，才补 actor ID、alias、issue/place/event edge、evidence note 和来源归档。
- R8 v1 已把方案指定的法律／程序路径从单一边野古示意升级为六案比较成果；后续只补明确残余字段，不扩写成诉讼效果因果评估。
- 以上完成后：进入正式 25–35 页 DOCX/PDF 报告、8,000–12,000 字论文和 15–20 页 PPT 的结构化制作，而不是继续扩充进度同步稿。

## 5. 当地协作者启动门槛

本轮三线不会派当地协作者。只有线上检索留下对象、时间范围、已查来源、缺失字段和它会改变的图／段落后，才从 Tier 2 正式派单。当前高价值当地任务仍是：

- 与那国 A014／A015 的组织身份、代表和持续性；
- 先岛／边野古核心组织地方报刊数据库时间线；
- AWWA／配偶俱乐部 Form 990 Schedule I 或完整 recipient 年表；
- 只有报告确需合同支付额时，才追 ONC 未公开合同／调达材料。

当地回收材料先进入人工复核日志，再进入主数据、图和报告；口头判断或无出处摘要不直接入结论。
