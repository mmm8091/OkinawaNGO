# Next-wave source integration v1

日期：2026-07-13

## 合并结果

- NW2-F 的 49 个唯一 URL 是本轮唯一权威输入：复用 S158/S204，新增 47 条 S248–S294。
- 中央 source log 当前为 295 条；S248–S294 全部保持 `review_status=ai_seeded` 和 proposal-derived 元数据；若存在 S295，它是 HR-011 后续定位补充，不属于 NW2-H 波次。
- S248–S294 只是 provisional source-log index：metadata 尚未经人工认可；archive failed 不撤销 provisional S 号，也不允许把该来源用于正式关系结论。
- S248–S294 归档状态：archived 40 / failed 7。
- HR-030：22 个唯一 URL。去重规则为 `source_id + audit_row_id`；合并 NW2-F 的 11 个 metadata 与 11 个 web/archive 队列（5 个交集），并追加任何实际 archive failure。review item ID 稳定使用该复合键，当前已填写 decision 0 条。
- 当前实际归档失败：S258, S261, S263, S279, S290, S291, S294。失败状态原样保留、不伪造 artifact，也不阻断 provisional source ID；其 metadata/可用性仍由 HR-030 决定。
- 50 条原始提案仍可经 `proposal_to_source_crosswalk_v1.csv` 追溯；跨批重复 R9EC_S007/RV2SP015 共同映射一个 S 号。

## 验证边界

- source ID 为唯一连续 S001–S295；47 个 NW2-H 新 URL 无任何新旧或批内重复。
- 历史遗留 S022/S024 共用同一 URL，因下游引用不同而原样保留；本轮没有扩大或修改这一既有重复组。
- 14 张 actor/alias/edge/role 中央表在脚本运行前后 SHA-256 一致。
- 已保存 artifact 共核验 267 个，manifest SHA 与本地文件一致。
- 中央 source log 在所有内存校验、archive 校验、HR-030 合并和受保护表 SHA 校验完成后，才通过同目录临时文件与 `os.replace` 原子更新；失败注入不得改变原文件。
- 所有 crosswalk 均为 `relation_or_claim_approved=no`。来源入表与归档不批准 actor、edge、联盟、资金、污染/健康因果、罢工合法性、选举效果或组织分类。

## 文件

- `source_merge_manifest_v1.csv`：49 个唯一 URL 的最终 S 号与归档状态。
- `proposal_to_source_crosswalk_v1.csv`：50 条输入提案到中央来源的映射。
- `integrated_source_rows_S248_S294_v1.csv`：47 条新增中央来源行的可核副本。
- `HR030_source_metadata_archive_review_v0.csv`：元数据／归档人工复核；既有人审字段按稳定复合键保留。
- `protected_actor_edge_sha_v1.csv`：受保护中央表的运行前后 SHA。
- `validation_report_v1.md`：机械校验结果。

## 可重复命令

```powershell
python scripts\integrate_next_wave_sources_v1.py
python scripts\archive_sources.py --from-id 248 --to-id 294
python scripts\integrate_next_wave_sources_v1.py
```
