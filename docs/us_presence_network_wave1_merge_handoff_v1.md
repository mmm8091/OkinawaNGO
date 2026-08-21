# USN 第一轮负责人回传：主线程合并说明 v1

日期：2026-08-21

用途：供当前工作分支／会话合并回项目主线程。这里的“合并主线程”是合并研究与人审产物，不等于执行中央数据 merger。

## 当前结论

四份正式人工任务和五项架构检查点均已完成负责人决定：

- 服务生态：13/13；正式回传见 `docs/human_review_return_USN_service_ecology_v1.md`。
- 问责侧：9/9（`accept 2 / revise 7`）；正式回传见 `docs/human_review_return_USN_accountability_v1.md`。
- 组织官网：65/65（`accept 54 / revise 4 / defer 5 / reject 2`）；正式回传见 `docs/human_review_return_USN_actor_directory_v1.md`。
- 旧关系归位：6/6（`accept 5 / revise 1`），覆盖43行；正式回传见 `docs/human_review_return_USN_relation_retype_v1.md`。
- 架构检查点：5/5（`accept 2 / revise 3`）；正式回传见 `docs/human_review_return_USN_architecture_checkpoint_v1.md`，机读决定见 `outputs/us_presence_network_architecture_v1/principal_checkpoint_return_v1.json`。

## 合并时应纳入

1. 四组负责人回填表：service、accountability、actor directory、relation rules。
2. 五份 `human_review_research_USN_*` 研究支持稿与五份 `human_review_return_USN_*` 正式回传。
3. assignment、package README、USN checkpoint、research-wave、workbench 与 `AGENTS.md` 的状态同步。
4. actor-directory、relation-return 和全波次 validator，以及 relation post-return report／manifest。
5. 本合并说明、架构检查点 JSON，以及总体验证回执：
   `outputs/us_presence_network_wave1_v1/post_principal_validation_report_v1.json`
   和 `post_principal_manifest_v1.json`。

不要把 `outputs/formal_comm_v3/第三次进度同步_v3.md` 混入本次 USN 提交；它是进入本轮前已经存在的用户修改，本轮没有触碰。

## 已验证

```powershell
python scripts\validate_hr_usn_actor_directory_return_v1.py
python scripts\validate_hr_usn_relation_retype_return_v1.py
python scripts\validate_usn_wave1_principal_returns_v1.py
git diff --check
```

全波次 validator 应报告：service 13、accountability 9、directory 65、relation rules 6／覆盖43、architecture 5，核对23个清单文件哈希，并确认 relation crosswalk 尚未展开。

## 本次明确没有执行

- 未修改中央 actor、alias、source、relation、person、AEV、case-role 或前端数据；
- 未把六条 relation rules 展开到43行 crosswalk；
- 未新增 source-log 行或修改 archive manifest；
- 未运行任何会重建空白人审包的 pre-human builder；
- 未生成 merger、publication adapter 或前端发布快照。

## 合并后的第一个工作包

先编写“受控集成设计＋预期字段级 diff＋幂等测试方案”，再请求是否实际中央写入。设计至少要覆盖：

1. source proposal／归档的新增与旧 source receipt 保留；
2. actor admission、national actor local presence、person identity、recipient、money、service、affiliation、action 分表；
3. relation rules 展开时只有 F017、F043 改为 `regional_branch`，其余41行 proposal 不变且不升级原事实状态；
4. defer/reject/history-only/event-only/unresolved endpoint 不被提升；
5. NOFO、project cost、sponsor tier、实物估值、汇总金额和实际付款严格分开。

## 已知后续项

- 架构 CSV 仍保留派发前 `L1/L2/L3` 旧机器后缀；需在表格运行时可用后机械迁移为 LEG 命名，并验证70项词表、44条门禁、10个切片及非目标字段零漂移。
- 受控集成完成并再次获准后，才按一项一停顺序推进 USN-04 人物 tracer、USN-05 分层资源路径、USN-06 公共外交／LEG2 地方反应。
- 整个 Phase 1 仍有12项当地／新一手材料，以及正式报告、论文、PPT、先岛 dossier、公开数据包、核心图 QA 和最终 codebook/lint；USN 回传完成不等于一期最终验收。
