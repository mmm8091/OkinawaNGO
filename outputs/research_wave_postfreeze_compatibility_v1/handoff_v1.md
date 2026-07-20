# H1／H2／H3 冻结后兼容性复算换手

日期：2026-07-20

## 完成

- 中央基线锁定为 actor–issue 283 active／
  141 reviewed／
  142 candidate；
  strict triples 306。
- 兼容判定 17 项：
  `invariant=7`、
  `recompute_required=7`、
  `not_comparable=3`。
- 识别 59 个需版本化处理或限定使用的资产，
  105 个高置信旧快照字符串位置。
- H1 当前来源依赖／审核层／actor 计数已复算；
  H2 当前比较组与逐资产变化已复算；
  H3 当前目标 tag 与输入 hash／source-governance 已复核。

## 关键边界

- 既有 H1/H2/H3 目录均未改动，它们仍是历史 provenance snapshot。
- `invariant` 只表示对本次冻结变化不敏感，不等于人工确认或 publication-ready。
- `not_comparable` 表示原任务分母不同，不能用新总数给旧搜索补一个覆盖率。
- S004 的 25 个受影响 actor 与 24 个完全掉出 E3/E4 层 actor 已明确分列。
- H2 的跨组关系仍只是在有界输入中未编码；人物、完整 recipient 与非公开接触仍不完整。
- H3 的 tag 增加不构成词汇增长或扩散证据。

## 建议接手

1. H1 新建 v3 generator，删除硬编码计数与图中文字。
2. H2 新建 v2 generator，重生 77-actor 比较组及所有依赖表；recipient/service 包保持独立。
3. H3 新建 v3 manifest/crosswalk 层；保留 v2 共同文件语料，不升级解释。
4. 负责人分别阅读 H2/H3 原文后，再决定是否启动更深研究；本包不替代解释检查点。

## 禁止误读

- 本包不是新的中央事实层、人工复核结果或前端数据契约。
- 不得用本包把 candidate 边提升为已核边。
- 不得静默覆盖旧包、旧图、旧测试或历史沟通材料。
