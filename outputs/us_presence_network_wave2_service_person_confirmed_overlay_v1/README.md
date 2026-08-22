# W2 服务侧人物—资金分层确认 overlay v1

日期：2026-08-22

状态：`research_only / principal_confirmed_identity_overlay / no_central_writeback / not_frontend_ready / W2-F_not_released`

## 1. 这张 overlay 回答什么

负责人完成 `HR-USN2-01a—01e` 后，本包把已确认的人物身份重新投影到服务侧组织网络，并与既有已核资金流并列。它只回答两个结构问题：哪些申报姓名现在可以在研究层视为同一人，以及这些人物桥是否与已确认资金流落在同一 actor pair。

人物、资金使用两套边表和两种语义，不合成总权重：

- `person_actor_role_edges_principal_confirmed_v1.csv` 保存人物—组织—角色／联系字段—时间—来源；
- `money_edges_principal_confirmed_v1.csv` 保存资金提供者—接收者—金额—期间／日期—资金语义—来源；
- `layered_network_edges_v1.csv` 只是把两层放进同一可计算接口，`relation_layer` 始终保留；
- `actor_person_projection_principal_confirmed_v1.csv` 只投影负责人确认的跨组织人物，不把近名候选投进去。

上述逐行表的 `cross_ecology_bridge` 统一使用 `not_applicable_service_only`：它说明该行两端本来就在服务侧，跨生态判断对该行不适用。包级 `cross_ecology_bridge_status=not_assessed` 则说明本包没有覆盖问责侧 roster。两者都不能读成“审计后为零”。

## 2. 确认后发生的结构变化

负责人确认 4 个统一人物身份，其中 3 人跨组织：

- AWWA—KOSC：Brooke Epp／Epps 与 Trinicia Kloepper，共 2 名共享人物；
- AWWA—OESC：Amber Tracy，共 1 名共享人物；
- OESC 内部：Lesilee DuFresne 的两期角色归入同一时间线；
- AWWA—NOSCO：Jen Yapsing／Jennifer Yapshing 保持未解决，确认投影中没有人物边。

人物层因此从 0 个负责人确认的跨组织人物，变为 3 人、2 组 actor pair。资金层没有因人物判断而增删：OESC→AWWA 仍是三个已核税期流，合计 USD 39,158；OESC→USO Okinawa 仍是一笔 USD 3,250 的已核捐赠。

AWWA—OESC 现在是本 overlay 中唯一同时出现负责人确认人物桥与已核资金流的 pair。这个多层重合说明两组织间同时存在人员流动／连续性与组织间资源流，不能进一步推导谁控制谁、资金由该人物决定、稳定联盟或政治立场。AWWA—KOSC 有两名确认共享人物，但没有确认资金边；KOSC 申报中 USD 2,580 的 AWWA 名称行仍是个人援助组语义，不进入本包资金层。

## 3. 文件

| 文件 | 内容 |
|---|---|
| `person_nodes_principal_confirmed_v1.csv` | 4 个负责人确认的 research-overlay 人物身份与 aliases |
| `person_actor_role_edges_principal_confirmed_v1.csv` | 13 条具来源人物—组织观察，区分申报期角色、申报时点角色与联系字段 |
| `actor_person_projection_principal_confirmed_v1.csv` | 2 组服务侧 actor pair 人物投影 |
| `unresolved_identity_pairs_v1.csv` | 01b 未解决姓名对；明确排除出确认投影 |
| `money_edges_principal_confirmed_v1.csv` | 4 条既有已核资金流；与人物身份决定相互独立 |
| `actor_pair_layer_summary_v1.csv` | 五组 service-side pair 的人物／资金／既有隶属层对照 |
| `layered_network_nodes_v1.csv` | 6 个服务侧 actor 与 4 个人物节点 |
| `layered_network_edges_v1.csv` | 13 条人物观察边与 4 条资金边；层标签不可删除 |
| `fig_service_person_money_overlay_v1.svg` | 人物层与资金层并列的内部研究图；未解决姓名不进入实线投影 |
| `structure_change_summary_v1.csv` | 决定前后结构计数与解释边界 |
| `unexpected_findings_register_v1.csv` | 19 列 `lead_only` 登记；本包新增观察为 0 |
| `validation_report_v1.json` | 结构、引用、层分离和边界验证 |
| `validate_overlay_v1.py` | 包内语义验证器：强制检查逐行 N/A 与包级未评估的区别 |
| `manifest_v1.json` | 本包非 manifest 文件的 SHA-256 清单 |

## 意外发现登记

本包是负责人决定后的机械重建，没有沿新线索侦察，`unexpected_findings_register_v1.csv` 只有 19 列表头、0 条观察。上游人物补证包已有的 Part VII／return-header 字段遗漏线索继续留在原包，不在这里复制或升级。

## 5. 不得被误读为

- 不是中央 person registry、中央关系表或 publication adapter；
- 不是前端可发布数据，也不放行 W2-F；
- 不是服务侧与问责侧的人物桥审计：本包所有人物与组织端点都在 service-side，未覆盖问责侧 roster，因此不能报告跨生态零；
- 不是组织控制、联盟或政治立场网络；
- 不是把 return header、Part VII 与 `BooksInCareOf` 当作同一种任期证据；
- 不是从人物桥反推资金授权，也不是从资金流反推人物控制；
- 不是把 01b 的 near-name 候选合并为一人。

## 6. 验证

```powershell
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_service_person_confirmed_overlay_v1
python outputs/us_presence_network_wave2_service_person_confirmed_overlay_v1/validate_overlay_v1.py
```
