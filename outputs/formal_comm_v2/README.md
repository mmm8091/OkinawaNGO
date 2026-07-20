# 第三次进度同步包 formal_comm_v2

日期：2026-07-16（图 6 current-only 重绘：2026-07-20）

这是对 `formal_comm_v1` 的 findings-led 重写。v1 以方法修正和证据稳健性为主；v2 将其移到边界说明，正文改为六项机制性发现。

## 主文件

- `第三次进度同步_v2.md`：面向甲方的解释性发现版 Markdown。
- `fig/`：六张横版 PNG。
- `data/`：每张图的派生数据和解释状态。

`第三次进度同步_v2.md` 是当前经过数据断言与口径复核的主文件。目录内的 `第三次进度同步_v2_改写稿.md` 是并行产生、尚未完成证据对账的备选文字，其中“13案”及桥接组织等表述与正式图表口径不一致，当前不得作为交付稿使用；本轮不覆盖或删除该文件。

## 六张图

1. `fig1_translation_mechanisms_v2.png`：三类物质争议如何进入不同制度语法。
2. `fig2_institutional_conversion_v2.png`：制度如何将诉求转换为记录、赔偿、投票或有限结果。
3. `fig3_referendum_gates_v2.png`：四个公投案例的放行、重新设计、阻断和结果再解释。
4. `fig4_sakishima_hypothesis_v2.png`：宫古—石垣—与那国比较假设及当地材料 gate。
5. `fig5_official_civic_ecology_v2.png`：FY2024 官方协作总体的公共服务基线。
6. `fig6_event_reassembly_v2.png`：三个目的性公开行动中的 registry 重复骨架与事件性重新组队；另行标明 registry 外、经人审核定的 event-only 重复身份。

## 当前安全重绘

```powershell
python scripts\render_formal_comm_v2_r5_current.py
```

该命令只读取中央 R5 参与表和当前 R5 event／bridge／overlap 表，只写 `data/fig6_event_reassembly_v2.csv` 与 `fig/fig6_event_reassembly_v2.png`。它在写图前锁定 169 条名单观察、三次 registry 行 16／31／17、15 个重复 registry actor、3 个贯穿三次和 6 个经人审的 event-only 重复身份。

`scripts/make_third_progress_sync_v2.py` 是 2026-07-16 的审前全包生成器，会一次覆盖六张图，且图 6 内置旧的 2020 registry=16 快照；**当前不得运行**。图 1–5 保留现有已对账资产，后续如需重绘应分别增加 current-only renderer，不能用旧全包脚本覆盖。

图 1–3 复用 R8／R9 和 8 个正式证据 translation episodes；图 4 读取 R4 线上安全摘录层并明确标为待当地检验假设；图 5 读取 S002 的 616 行机械聚合总体；图 6 读取当前 R5 三次完整名单和分层身份数据。

## 强制边界

- 机制比较不是因果规律。
- 8 个案例是已进入制度场域的目的性样本，不是总体成功率。
- 先岛摘录数不是现实动员强度；来源缺失不等于议题不存在。
- 616 是官方表来源行，不是组织、合同或拨款数。
- 公投流程顺序不证明前一阶段造成后一结果。
- 三张名单是目的性样本；重复公开参与不证明稳定联盟、成员关系或持续协调。
- 图 6 的“15 个”只指重复出现的 registry actor；另有 6 个经人审核定、但未进入 registry 的 event-only identity 跨事件重复，两层不得混计。
