# 冻结后前端任务书 v1

日期：2026-07-20
状态：可直接交给前端 session

## 任务目标

前端已经正确同步 145 项线上决定。本轮不再“修同步”，而是完成两个解释层缺口：

1. 解释为什么已核图与研究图的视觉差距很大；
2. 把已经人审的生命周期事实导出到时间页 L2 谱系层。

`docs/nr3_handoff_v1.md` 是现状、历史整改和验收记录；本文件才是下一轮前端执行任务书。

## FE-01 · 已核／研究差距解释

### 当前事实

- 有效 actor–issue：283＝125 人审＋158 候选。
- 已核图连接 47/121 个可见 actor；研究图连接 116/121，另有 5 个无边 actor。
- 125 条人审边＝67 `frozen_bounded`＋58 `accepted_unfrozen`。
- 158 条候选边＝44 `scope_reviewed_fact_pending`＋114 `fact_pending`。
- 候选事实门进一步分为 128 普通待审、25 待二源、5 待当地材料。

视觉差距来自**人审边集中在 47 个组织，而候选边分散覆盖另外 69 个组织**，不是前端漏数。

### 呈现要求

- 保留“已核／研究”两档，不新增会混淆事实等级的第三张网络。
- 在组织页切换器旁增加可展开的“为何差这么多？”说明：
  - 已核：125 条事实边／47 个连通组织；
  - 研究：另加 158 条候选边／总计 116 个连通组织；
  - 候选组成：44 范围已审、114 事实待审，其中 25 待二源、5 待当地。
- 明确写出：组织身份状态、议题边事实状态、字段冻结状态是三个不同门禁。
- 不以动画、边粗细或节点大小把候选层误读成影响力更大。
- 五个无边组织继续可搜索；不得为了图面饱满自动生成议题边。

## FE-02 · L2 生命周期／谱系导出

### 权威输入

`outputs/actor_lifecycle_v1/actor_lifecycle_v0.csv`

只导出：

- `registry_scope=central_registry`
- `review_status=human_checked|human_revised`
- `lifecycle_workflow_status=resolved`

因此当前应导出 **5 条中央记录**；其中 4 条是本轮 LCR001–004 新决定，A051 是此前已核记录。
LC006 是 out-of-registry control case，禁止进入普通谱系图。

| lifecycle | actor | 前端语义 |
|---|---|---|
| LC001 | A051 | 2019-03-26 dissolved；解散后的个人活动不归回该组织 |
| LC002 | A068→A019 | 1997-10-18 reorganized／successor；不合并为同一 actor，不写精确解散日 |
| LC003 | A011 | 2024-11-27 dissolved；不使用失配的 S051 |
| LC004 | A065 | continuity_unverified；只显示 last observed 2023-06-01，不画解散 |
| LC005 | A069 | continuity_unverified；只显示 last observed 2015-06-22，不画解散 |

### 数据与界面要求

- builder 生成 `demo/genealogy_anchors.json`；研究层新增历史候选时仍走独立 candidate gate。
- dissolved、reorganized／successor、last-observed／continuity-unverified 使用不同形状与图例。
- `last_observed_activity_date` 不能显示成“解散日”或“存续至今”。
- A068→A019 使用有方向的后继／重组线；不得改写 registry ID 或自动合并。
- 每条锚点可下钻 evidence drawer；原始 URL 与 S-source 都应保留。
- 时间页把“谱系锚点 0 条”替换为真实计数，并继续显示新增历史材料缺口。

## FE-03 · QA 与换手

- 更新 manifest、validation report、adapter tests、时间页测试与三语文案。
- 复验总览／组织／时间／路径／证据五页：
  - 1280×900；
  - 390×844；
  - 控制台 0 app-origin error/warning；
  - 无横向溢出。
- 更新 `docs/nr3_handoff_v1.md` 与 `design-qa.md`，记录当前 build ID 和五条谱系记录。

## 禁止事项

- 不修改中央 registry、actor–issue、actor–place、relation 或 lifecycle CSV。
- 不把候选边升级为人审边。
- 不把共同署名、同场参与或同案角色画成稳定联盟。
- 不把 `continuity_unverified` 画成 dissolved、dormant 或 current。
- 不在本 session 重绘五张正式报告图；那属于独立的图件冻结 session。

## 验收命令

```powershell
python scripts\build_exploration_system_data_v1.py
python -m unittest tests.test_build_exploration_system_data_v1
python scripts\validate_phase1_data.py
cd prototypes\nr3_explorer
npm run build
```

完成后由主线程使用浏览器复验，不以单纯构建通过代替视觉验收。
