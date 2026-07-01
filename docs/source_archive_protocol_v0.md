# 信息源文件备份规则 v0

日期：2026-07-01

## 1. 目标

所有进入 `source_log` 的线上来源，除保留 URL 引用外，尽量建立本地文件备份。备份用于复核、断链恢复和后续人工审查，不自动等同于可公开分发材料。

## 2. 当前口径

- 已确认 URL：可以立即备份 HTML、PDF 或原始响应文件。
- `inferred_url:` 占位符：不能备份为正式来源，必须先核成真实 URL，或标记为 `not_found`。
- 需要馆内数据库、付费数据库或纸质资料的来源：可保存截图、PDF 或照片，但对外引用时只写出处、日期、标题、页码和访问条件。
- 涉及版权或访问限制的全文材料：只进入内部备份，不直接对外公开传播。

## 3. 当前状态

执行时间：2026-07-01

结果：

- `archived`：74 条。
- `manual_archived`：2 条，S007 APJJF 和 S078 Ryukyu Shimpo 已用手工方式归档。
- `pending_archive`：0 条，已有真实 URL 的来源已完成第一轮归档。
- `skipped_inferred_url`：14 条，等待核实真实 URL。
- `skipped_non_url_reference`：2 条，书籍参考需人工做书目信息或扫描页归档。

## 4. 文件结构

归档根目录：

`source_docs/source_archive/`

每条来源一个目录：

`source_docs/source_archive/S003/`

常见文件：

- `raw.html` / `raw.pdf` / `raw.bin`：下载到的原始材料。
- `metadata.json`：来源日志字段、URL、下载时间、HTTP 信息、hash、归档状态。

总清单：

`source_docs/source_archive/source_archive_manifest.csv`

## 5. 状态字段

- `archived`：已成功保存原始文件。
- `manual_archived`：已通过手工下载、截图、网页打印或其他方式保存。
- `pending_archive`：已有真实 URL，但尚未归档。
- `skipped_inferred_url`：URL 仍是占位符，等待核实。
- `skipped_non_url_reference`：书籍或非 URL 参考，等待人工书目归档。
- `failed`：下载失败，需要人工重试或改用截图、网页打印、Internet Archive。

当前没有 `failed` 或 `pending_archive` 条目；下一轮重点不是下载，而是把剩余 14 条 `inferred_url` 占位符核成真实 URL 或标记为未找到。

## 6. 运行方式

```powershell
python scripts/archive_sources.py
```

脚本会读取：

`data/interim/05_source_log_initial_v0.csv`

并写入：

`source_docs/source_archive/`

## 7. 后续补强

下一步建议给 `source_log` 增加以下字段，或用 manifest 作为旁表维护：

- `archive_status`
- `local_archive_path`
- `archived_at`
- `content_hash`
- `archive_note`

这一步建议在 source log 字段稳定后再做，避免手工维护两套不一致的状态。
