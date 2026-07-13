# REG-01 安全合并与人工复核分流记录 v1

初始日期：2026-07-12

状态更新：2026-07-13

## 当前快照

- 主 registry 当前为 **118 actor**，不是历史中间状态 123。
- 数量变化：103 个历史 actor − A077-A085 九个一次性署名名称 + A087-A106 二十个 E4 身份级 actor + HR-011 的 A107-A110 四个 actor = 118。
- A077-A085 没有被删除为“事件不存在”；它们退出 organization registry，但其九条 E2 MMC 署名记录继续作为 `unverified_event_participant` 保留在正式 actor-event-venue 表。
- HR-011、HR-012、HR-014、HR-015 已按用户记录落库；HR-013 未收到结论，保持 pending，不作 AI 推断。
- A087-A101 仍只是 E4 身份级安全合并，分类、范围和关系继续属于 HR-010 待审部分；A102-A106 已完成 HR-010 批5。

## 2026-07-12 身份级安全合并（历史基线）

- 20 个由 E4 一手来源确认、无明显重名风险的主体身份，正式编号 A087-A106。
- 与这些主体及 R8 六案有关、按 URL 去重后的 41 条来源，正式编号接续写入 source log。
- 16 行 venue taxonomy，作为编码元数据使用，不代表任何主体已在某场域行动。
- R8 六个案件/程序的 case metadata，全部标记 `needs_human_review`。

actor 合并只确认“这个组织可核验存在”。候选包中的 `actor_class`、`legal_status`、`primary_places`、`issue_tags` 用于组织复核，不构成最终审定；本轮没有为新增主体自动生成 actor-issue、actor-place、actor-event 或 actor-relation 边。

后续状态：2026-07-13 HR-010 批5已完成 A102-A106 的人工审定并新增人审议题/关系边；具体见 `hr010_batch5_merge_note.md`。上述身份级边界继续适用于 A087-A101。历史中间值 123 后来因 HR-015 撤出 A077-A085、HR-011 新增 A107-A110，调整为当前 118。

正式 actor/source 映射见 `merge_manifest_v1.csv`。合并脚本为 `scripts/merge_phase1_candidate_seeds.py`，可重复运行而不重复新增行。

## 2026-07-12 人工分流及当前处置

- **HR-011 completed**：C009、C012、C023、C036 分别以 A107-A110 入表。C015 `defer`，不进入主表；补到能闭合组织身份和行动归属的一手／当地材料后才重开。
- **HR-012 completed**：C026/C027 分别作为 A052/A053 的 `round_of`，C028 作为 A010 的 `predecessor_of`；均不新建 actor。A052/A053 已完成规范名调整，A010 已补 2015-08-20 前身与 2016 年 9 月较广联盟形成时间。
- **HR-013 pending**：C010、C011、C029-C034 未收到用户结论，维持候选状态；不自动作 `core_actor`、`background_actor` 或 `out_of_scope` 判定。
- **HR-014 completed**：R8 六案和 27 条案件角色已按案件特定边界人审落库；程序、原告、律师、请求者、支援者和 non-party 不互相外推。
- **HR-015 completed**：49 条 evidence note、64 条 actor-event-venue 已形成正式人审表；A077-A085 撤出主 registry并保留事件级记录。

## 解释边界

- 历史中间状态曾达到 123；当前 118 低于方案 120–180 的数量下限。数量缺口不能通过恢复 A077-A085 一次性署名名称或自动接受 HR-013 候选来填补。
- 共同署名、同场行动、请求书和诉讼支持不得据此写成稳定联盟。
- 法律程序存在不等于某组织实际使用该程序；未复核角色不进入主关系数据。
- 一般环境、教育、女性、劳工或服务组织不按名称预设政治立场，只按可核行动与功能编码。

## 人工交付入口

完整逐项要求和历史任务原文见 `docs/human_review_tasks_v0.md` 的 HR-010 至 HR-015。当前只剩 HR-010 的 A087-A101 部分与 HR-013 尚未闭合；人工完成后仍须写入 reviewer、date、status、note 与最终证据等级，再由主线程决定是否合并并重生成图表和报告。

HR-011/012 具体落库说明见 `hr011_hr012_merge_note.md`；HR-014 见 `outputs/R08_legal_procedure_v0/hr014_merge_note.md`；HR-015 见 `outputs/phase1_foundation_v1/hr015_merge_note.md`。
