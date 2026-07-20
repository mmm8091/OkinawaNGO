# 冻结后 H1／H2／H3 兼容性复算 v1

日期：2026-07-20
状态：`research_only / candidate_analysis / not_frontend_ready / central_writeback=no`

本包不覆盖 H1/H2/H3 既有研究包。它只给历史快照加一层冻结后兼容 overlay。

## 当前机械基线

- Registry：122 历史／121 current。
- Actor–issue：283 active＝125 reviewed＋158 candidate；116 connected＋5 isolated。
- E3/E4：271 边／114 actor；其中 reviewed 117 边／47 actor，candidate 154／76。
- Strict triple：305 总数／298 E3/E4／71 dual-reviewed／97 event-attached。

## H1

旧 H1 的 `238/65/173`、234 条 E3/E4 和 312 strict triples 都必须视为历史快照。
当前 E3/E4 删除仅由 S004 可解析支持的 40 条边后，
保留 231 条／90 actor。

必须区分两个分母：

- 25 个 actor 至少碰到一条被删边；
- 其中 24 个 actor 失去全部 E3/E4 边。

S003/S004/S006 合计删除 48 条，S004 占
83.3%。这仍只描述当前编码支持集中，
不证明真实网络中心性或组织能力。

## H2

服务侧 registry 子集仍为 9 个 actor。问责侧按同一锚点规则由
65 扩至 77 个，其中
35 个有 reviewed anchor，
42 个仅有 candidate anchor。
当前有界 typed-dyadic／event／R10 输入中的直接跨组组织关系仍为
0/
0/
0；只能写“当前有界输入未编码”，不能写“没有共享人员”。

服务 universe 与 recipient 包的来源行仍可使用，但两个 18-anchor 搜索不是当前
77-actor 比较组的完整分母，状态为 `not_comparable`。

## H3

中央 tag snapshot 由 `4/4/1` 变为：

- `frontline_prevention=6`；
- `Taiwan_contingency=6`；
- `anti_war=5`。

H3 v1 的来源观察／载体／参与候选和 H3 v2 的共同文件语料保持 source-level invariant；
旧 manifest 的 registry/source-log hash 需要刷新。标签增加仍不能证明历史词汇增长、
传播方向、独立采用或持续共同动员。

## 复现

```powershell
python scripts\make_research_wave_postfreeze_compatibility_v1.py
python -m unittest tests.test_make_research_wave_postfreeze_compatibility_v1
```

## 阅读顺序

1. `package_compatibility_overlay_v1.csv`
2. `stale_asset_inventory_v1.csv`
3. `h1_recomputed_metrics_v1.json`
4. `h2_recomputed_metrics_v1.json`
5. `h3_recomputed_metrics_v1.json`
6. `next_generator_recommendations_v1.csv`
7. `handoff_v1.md`

本包不进入中央表，不进入前端，不升级任何解释性命题。
