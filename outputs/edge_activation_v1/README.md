# edge_activation_v1

R1/R2 edge-isolated actor 的在线补证包。运行：

```powershell
python scripts\make_edge_activation_v1.py
```

`data/interim/28_edge_activation_candidates_v1.csv` 和未带 `post_hr013_` 的表保留 HR-013 前 18 actor / 58 edge / 40 source 的取证快照。HR-013 已人工剔除 A094；当前复核和后续合并必须使用本目录的 `post_hr013_*` 过滤表（17 actor / 54 edge / 38 source；HR-010 47 项）。

脚本只生成本目录和 `data/interim/28_edge_activation_candidates_v1.csv`；不读取或修改 registry、actor–issue 主表、source log 或中央文档。中央 registry 即使已移除 A094，脚本仍可重复运行；A094 只会出现在明确标为历史快照/排除处置的文件中。
