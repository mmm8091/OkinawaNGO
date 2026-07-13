# REG-01 安全合并与人工复核分流记录 v1

日期：2026-07-12

## 已直接合并

- 20 个由 E4 一手来源确认、无明显重名风险的主体身份，正式编号 A087-A106。
- 与这些主体及 R8 六案有关、按 URL 去重后的 41 条来源，正式编号接续写入 source log。
- 16 行 venue taxonomy，作为编码元数据使用，不代表任何主体已在某场域行动。
- R8 六个案件/程序的 case metadata，全部标记 `needs_human_review`。

actor 合并只确认“这个组织可核验存在”。候选包中的 `actor_class`、`legal_status`、`primary_places`、`issue_tags` 用于组织复核，不构成最终审定；本轮没有为新增主体自动生成 actor-issue、actor-place、actor-event 或 actor-relation 边。

后续状态：2026-07-13 HR-010 批5已完成 A102-A106 的人工审定并新增人审议题/关系边；具体见 `hr010_batch5_merge_note.md`。上述身份级边界继续适用于 A087-A101。

正式 actor/source 映射见 `merge_manifest_v1.csv`。合并脚本为 `scripts/merge_phase1_candidate_seeds.py`，可重复运行而不重复新增行。

## 未直接合并

- C009、C012、C015、C023、C036：E3 首批候选，进入 HR-011 补第二来源。
- C026-C028：存在别名、前身/后继或诉讼代际重复风险，进入 HR-012。
- C010、C011、C029-C034：研究范围或直接议题连接不足，进入 HR-013。
- R8 的 actor-case role、法律结果摘要和跨表 actor crosswalk：进入 HR-014。
- 49 条 evidence note seed 和 64 条 actor-event-venue seed：进入 HR-015。

## 解释边界

- 达到 123 个 actor 只表示满足方案 120–180 的数量下限，不表示 R1-R11 已饱和或一期已经验收。
- 共同署名、同场行动、请求书和诉讼支持不得据此写成稳定联盟。
- 法律程序存在不等于某组织实际使用该程序；未复核角色不进入主关系数据。
- 一般环境、教育、女性、劳工或服务组织不按名称预设政治立场，只按可核行动与功能编码。

## 人工交付入口

完整逐项要求见 `docs/human_review_tasks_v0.md` 的 HR-010 至 HR-015。人工完成后应写入 reviewer、date、status、note 与最终证据等级；复核结果再由主线程合并并重生成图表和报告。
