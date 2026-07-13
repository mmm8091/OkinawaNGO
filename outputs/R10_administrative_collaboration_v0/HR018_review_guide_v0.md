# HR-018 R10 关系级人工复核指南

日期：2026-07-13

## 复核范围

本包只将尚非 `human_checked`／`human_revised` 的 **26 条 relation observation** 作为主复核项。关联的金额和功能通过 `linked_amount_ids`、`linked_function_ids` 回指，不拆成额外人工任务。已有 9 条 human_checked／human_revised 关系不重复进入本包。

## 填写规则

1. 每个主条目只在 `accept`、`revise`、`reject` 三栏之一填 `X`。
2. 选择 `revise` 时，在 `revision_instructions` 写明应修改的字段与安全措辞；`human_notes` 可记录来源页码、actor crosswalk 或方向判断。
3. `accept` 表示接受该条关系的机制、范围、来源与解释边界，不表示把所有关联 project cost 接受为付款。
4. `reject` 后仍保留原始来源追溯，不从本包直接删除中央数据。
5. 本包不自动修改 actor registry、source log、funding 主表或中央任务簿；完成签审后另行执行 merge proposal。

## 来源前置条件

`HR018_source_prerequisites_v0.csv` 单列 R10S05–R10S12 共 8 项归档／source-log 前置条件。`archive_verified`、`main_source_id` 和 `human_notes` 当前留空，不能把 `pending_archive_and_source_log_prerequisite` 当成人审通过。

## 影响范围

每条主复核项列出会影响的 main-table proposal、两张 R10 图与 brief 章节。任何 project cost、aggregate、sponsor tier、membership、service presence 或 NOFO 的 revise，都应同步检查资金证据边界图；任何 relation_type 的 revise，都应同步检查机制生态图 16+19=35 的完整计数。
