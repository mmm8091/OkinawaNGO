# 第二次进度同步包 formal_comm_v0

日期：2026-07-01

本目录是面向甲方的第二次进度同步材料，文风对齐第一次同步（简洁、保守、图表截图嵌入）。

> 状态说明（2026-07-13）：`第二次进度同步_v0.md` 与 `fig/*.png` 是甲方已收到的历史快照，不随内部数据追改。`index.html` 与 `fig/*.html` 可由脚本重算当前数据；只有完成重新截图和人工图文复核后，才可另起版本对外发送。

## 对外交付物（发飞书云文档用）

- `第二次进度同步_v0.md` — **主交付物**，手写的简洁进度稿。结构：本轮进展、研究模块菜单进度、
  是否符合七周工期、核心图表、人工复核与口径、下一步。图片用相对路径引用 `fig/` 下的截图。

## 图源（由脚本生成，用于截图嵌入 MD）

- `fig/fig1_place_issue.png` — 地点 × 议题框架矩阵（R3 / R4）
- `fig/fig2_pathway.png` — 边野古 / 大浦湾国际化路径（R6 / R11）
- `fig/fig3_bridge.png` — 跨议题桥接组织 Top 14（R2）
- `fig/fig4_coaction.png` — 共同行动样本构成 2010 / 2015 / 2020（R5）
- `index.html` — 四张图合成的单页网页预览（内部用，非对外文风）。
- `fig/*.html` — 单图页，供导出上面的 PNG。

## 生成图表

```powershell
python scripts\make_formal_comm_package.py
```

脚本读取 `data/interim` 各表、`outputs/explanatory_v0` 的矩阵 / 桥接 / 共同行动 CSV、
`source_docs/source_archive` 归档 manifest 与 2020 MMC 候选表，因此 HTML 图源反映当前数据。
PNG 属已交付快照；数据更新后需重跑脚本、重截 PNG、检查图注，再以新版本号发布，不能静默覆盖既有对外材料。

## 口径

全部保守：候选关系不当结论、共同署名不写联盟、grant opportunity 不写拨款、
军属服务组织按功能编码、与那国按前线 / 自治 / 生命安全读取。旧的
`docs/progress_report_v1.md` 是内部草稿，不作为本次对外交付。
