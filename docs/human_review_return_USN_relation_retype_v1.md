# USN-HR-01：现有 43 条关系分层归位——负责人回传 v1

日期：2026-08-21

状态：负责人已确认；6/6 分组决定完成。当前只回填规则表，尚未展开到 43 行 crosswalk，也未写入中央数据或前端。

负责人：`project_principal_user`

## 决定汇总

| 规则 | 目标 | 覆盖行数 | 决定 | 执行边界 |
|---|---|---:|---|---|
| USN-RT-R01 | USN02 `money_flows` | 8 | `accept` | 只确认资金类语义归位；不补金额、不把汇总额拆给具体 recipient，不把 sponsor tier 换算金额 |
| USN-RT-R02 | USN04 `service_recipient` | 4 | `accept` | 保留实物／共同交付语义；未解析 recipient 继续走 USN08，不生成联盟边 |
| USN-RT-R03 | USN05 `affiliation_control` | 9 | `revise` | 九行仍全进 USN05；仅 F017、F043 改为 `regional_branch`，其余七行为 `umbrella_membership` |
| USN-RT-R04 | USN06 `action_institution` | 20 | `accept` | 保留地点、案件、项目或事件 scope；共同参与不生成两两联盟边，commission 不自动成为付款 |
| USN-RT-R05 | LEAD `research_lead` | 1 | `accept` | F012 仍为 NOFO／机会线索，不是 award 或 money flow |
| USN-RT-R06 | EXCLUDE `history_only` | 1 | `accept` | 同意 F008 留在历史排除层；不是接受或恢复该关系 |

合计：`accept 5 / revise 1`，覆盖 F001–F043 全部 43 条历史样本。

## 唯一映射修订

- F017：`organizational_affiliation` → `regional_branch`；保留原 `ai_seeded` 事实状态，不翻转端点，不自动确认治理控制。
- F043：`organizational_affiliation` → `regional_branch`；不推定 A105 与 A107 法律人格相同、治理控制或行动继承。

其余 41 行的 proposed destination 与 record family 均按提案接受。所有 43 行原有的事实、review/claim、金额、端点、时间和图资格均原样继承。

## 未授权动作

- 不把这次语义归位解释为对旧关系事实的重新确认；
- 不将 membership、regional branch、共同参与或共同协调解释为资金、控制、政治联盟或共同立场；
- 不将 NOFO、总可用额度、project cost 或 sponsor tier 改写成实际 award／付款；
- 不运行会清空负责人决定的 pre-human builder；
- 五项 principal architecture checkpoint 现已完成；43行 crosswalk 仍保持未展开，须先提交受控集成设计、预期 diff 与幂等测试，不自动建立中央 merger 或 publication adapter。

## QA

- 规则表 6 行均已填写决定、说明、负责人和日期；
- 行数合计 43，edge ID 与 crosswalk 完整一一覆盖；
- R03 明确点名 F017、F043 及 `regional_branch`；
- crosswalk 的 `mapping_decision` 仍为空，证明本轮尚未执行展开；
- post-return validator：`scripts/validate_hr_usn_relation_retype_return_v1.py`；结果固化于 `outputs/us_presence_relation_retype_v1/post_return_validation_report_v1.json`。
- 原 `validation_report_v1.json` 与 `manifest.json` 保留为派发前快照；回传文件使用独立 `post_return_manifest_v1.json`，不覆盖历史 receipt。
