# Translation negative cases v1

本包是对 `outputs/translation_episode_comparison_v1/` 的**加法型、研究专用对照包**。原包
13 个 episode 全部因已有可观察的场域进入和中间产出而入选；本包定向寻找入口受阻、
资格排除、可司法化失败、指定回应方式被拒或回应追踪停滞的案例，用来检查“制度让步上限”
是否受到入场选择偏差影响。

## 内容

- `negative_case_candidates_v1.csv`：5 个统一字段候选案例。
- `source_search_log_v1.csv`：21 条纳入来源与5条方法／背景／排除记录；`TNS*` 仅为本包本地编号，
  不是中央 `S*` source ID。
- `comparison_table_v1.csv`：原13案选择边界与5个候选负例的同口径比较。
- `human_review_queue_v1.csv`：5项负责人判断候选；决定栏保持空白，尚未进入正式HR总账。
- `brief_v1.md`：研究结论、竞争解释与不能说什么。
- `validation_report_v1.md`：结构、状态与边界检查。
- `handoff_v1.md`：主线程换手说明。

## 强制边界

所有行都是 `research_only / candidate / ai_seeded / not_frontend_ready /
central_writeback=no`。它们不是中央事实、前端数据或正式报告结论。未找到公开回应只能写成
“本轮限定检索未找到”，不得写成现实中没有回应；不採択不等于未受理；同案、联名、共同
申请不生成稳定联盟。

## 复现

```powershell
python scripts\make_translation_negative_cases_v1.py
python scripts\make_translation_negative_cases_v1.py --check
```

生成日期：2026-07-20。
