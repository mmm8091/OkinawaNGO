# 对美主线第二轮 W2-E：1972-2012 历史双线 v1

日期：2026-08-22

状态：`research_only / principal_checkpoint_pending / not_frontend_ready / central_writeback=no`

## 这包做了什么

- 30 条历史锚点：问责侧 18 条，服务／照护侧 12 条；
- 46 条来源收据，其中本轮新增冻结 5 件官方原件；
- 9 类记录制度、15 条文献定位、7 条候选判断和 10 项精确当地／新一手任务；
- 一张两条泳道的历史图，不把来源密度当作活动强度。

## 当前最重要的研究修正

历史材料不支持把两套生态写成 1972 年以来始终封闭。国際福祉相談所至少留下了一条可追踪链：
照护与无国籍儿童个案被汇总为 1979 年提言，随后进入地方行政请求、法务省听证和国会证言。
1984 年国会记录还明确回指该提言和沖縄个案。这个案例支持“历史上的选择性通透”，但不能外推给
今天的 AWWA、军属俱乐部或 USO，也不能把 1985 年国籍法修改归因于单一组织。

第二个修正是：两条历史线首先由不同记录制度保存。法院、EIA、公投、福利档案、军方公共关系材料
和后来的税务申报留下的痕迹不同。1998 年 12 月施行的 NPO 法，只为采用该法人形态的组织新增了一种
标准化认证／公开通道；它不是整个冲绳 NGO 网络或互联网可见性的统一断点。历史网络密度必须按来源族比较。

## 主文件

- `historical_spine_v1.csv`：两条历史线的 30 个锚点；
- `record_regime_comparison_v1.csv`：9 类记录制度及其系统性遗漏；
- `source_receipts_v1.csv`：来源、locator、本地路径与 SHA-256；
- `source_coverage_v1.csv`：按泳道／时期显示覆盖，不作为活动计数；
- `literature_comparison_v1.csv`：先行研究、项目增量与不可声称的新颖性；
- `claim_table_v1.csv`：候选结论、允许表述与禁止外推；
- `local_retrieval_candidates_v1.csv`：取到后会改变哪条判断；
- `fig_w2e_two_spines_v1.svg`：历史双线图；
- `principal_checkpoint_v1.md`：负责人只需处理四项解释性判断；
- `validation_report_v1.json` 与 `manifest.json`：结构、引用与哈希验证。

## 边界

本包没有给国際福祉相談所、琉米福祉協議会、Amer-Asian School 等历史接口分配 actor ID，
没有建立 AWWA 前身关系，也没有改中央表、publication adapter 或前端。`ai_seeded` 锚点仍需负责人
判断；来源是官方原件，也不自动把解释升级成人审结论。

## 意外发现登记

- `unexpected_findings_register_v1.csv`：本轮 0 条；本次构建没有登记新的偶发线索。
- 登记项全部使用 `lead_only`，不进入本包结论、中央事实层或前端，也不触发人工复核。
- 每条根线索最多向外追查 3 步，每包最多 10 条新观察；空表不表示现实中不存在其他关系或材料。

## 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_e_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_e_v1
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_w2_e_v1
```
