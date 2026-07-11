# R14 覆盖与偏差审计 brief v0

## 当前完成度

R14 已达到 `audit_v0`：已有 source archive manifest、HR review log、next investigation candidates 和证据缺口图。

## 可交付图表

- `outputs/explanatory_v0/fig_evidence_gap_map.png`
- `outputs/explanatory_v0/next_investigation_candidates.csv`
- `outputs/module_completion_v0/coverage_gap_summary_v0.csv`

## 当前可讲结论

1. 当前数据不是全量冲绳 NGO 网络，而是公开资料驱动的议题相关 actor registry。
2. 来源覆盖明显偏向边野古 / 大浦湾、公开声明、组织官网、近期网页和国际倡议材料。
3. 离岛小团体、旧组织、报刊数据库材料、军属慈善 recipient 和行政 / 委托合同材料仍需要补。

## 下一轮缺口计数

- actor / needs_local_retrieval: 2
- actor / needs_second_source: 23
- actor / watchlist_only: 2
- source / skipped_non_url_reference: 2

## 必须保留的解释边界

- 不能从当前样本推论冲绳所有 NGO 的数量。
- 不能把 NPO 法人生态等同于抗争型市民社会生态。
- 不能把共同署名等同于稳定联盟。
- 不能把 grant opportunity 等同于拨款事实。

## 还需要继续做

- 维护 source archive manifest；新增真实 URL 后继续归档。
- 继续核实剩余 14 条 inferred_url，并使用 `data/interim/16_inferred_url_resolution_queue_v0.csv` 跟踪 archived_resolved / candidate / local retrieval 状态。
- 给 source log 增加 source_access / archive_status / coverage_note 字段，或继续使用 manifest 旁表。
- 建立 missing_cases_log，专门记录离岛、旧组织、失效网站和馆内数据库缺口。
