# 基地内私人组织制度位置：有界侦察包 v1

日期：2026-08-22
状态：`research_only / lead_only`。本包最多三步、十条观察；不修改中央事实层、人工复核队列、publication adapter 或前端。

## 1. 研究问题与最短回答

问题是：AWWA、军属配偶俱乐部和 Marine Thrift Shop 这类民间组织，怎样获得在美军基地内持续运作、筹资或零售的制度位置？这种位置由谁授权和监督，是否意味着 MCCS／DoD 控制或财政支持？

本轮最有价值的结构性线索是：这些组织处在一种**“经基地授权的私人自治”**中。

- 组织本身被规则明示为 non-federal entity／private organization，而不是 MCCS 部门、NAFI 或政府机构；内部章程、人员、财产和债务仍由私人组织承担。
- installation command 决定它能否在基地内运作；MCCS 或 FSS 承担申请流转、财务报送、合规检查和状态管理。MCIPAC 与 Kadena 使用各自的授权链，并不是一条统一的 MCCS 隶属体系。
- 对持续使用的场地，MCIPAC 要求 real-estate license，并要求组织预付或偿还水电、材料和服务成本；Kadena 规定使用 18 FSS 设备、服务或支持按正常费用收费。公开材料没有证明这些组织获得免费房间或隐性补贴。
- thrift shop／authorized gift shop 获得的是一般禁止持续零售规则中的明确例外。这个例外创造了可持续筹资位置，但不能直接编码成政府拨款、控制或背书。
- 基地管理端保存章程、预算、季度账目、银行流水、会议纪要、donation receipts、人员名单和审计材料。它构成一套与 IRS 990 平行的“行政档案”，比继续搜活动网页更可能回答“谁组织、钱怎么走”。

因此，后续社会网络研究若获负责人批准，应单列 `installation_authorization / administrative_monitor / facility_license / reimbursable_support / resale_exception`，不能把这些关系塞进 affiliation、control 或 funding。

## 2. 四个字段的核验结果

| 问题 | MCIPAC／Camp Butler | Kadena AB | 本轮允许的解释 |
|---|---|---|---|
| 场地／房间是免费、成本回收还是未说明 | 持续使用 DoD 场地须 real-estate license；水电、材料、服务及其他成本须偿还。license 本身的租金／房价没有公开 | 募款场地须由 facility manager 同意；持续零售例外点名 KOSC Gift Corner 与 Kadena Enlisted Spouses Club Thrift Store。固定房间和租金未写 | MCIPAC 可写“持续使用采取许可＋成本偿还”；Kadena 的固定空间价格为 `not_stated`。均不能写免费场地 |
| 水电／设备／后勤能否由政府提供 | 组织原则上自备设备、耗材；有限后勤可依法、经法律审查和 CG／designee 批准提供；持续场地的水电、材料、服务须报销 | 政府设备和系统的非公务使用“极为有限”；使用 18 FSS 设备、服务或支持按正常费用收费；涉 base water 的活动另需审批 | 可写“有条件准入或成本回收支持”，不能写日常政府供养 |
| 是否明确 non-federal／non-NAFI，债务是否由政府承担 | 明确为 NFE、不是联邦机构、不是 NAFI；成员在资产不足时依法承担个人责任；MCIPAC 不承担 PO 活动或资产责任 | 本地 OI 写明组织由个人在联邦公务身份之外设立、职能与军务分开；章程须写成员对债务承担共同及个别责任。本地 OI 未使用完整 `not NAFI` 句式 | 两个制度都支持私人责任；不能把 PO 写成政府机构。Kadena 的 `non-NAFI` 只可由上位政策说明，不冒充本地 OI 原文 |
| command／MCCS 能否暂停或撤销 | CG／designee 可 probation、suspend、revoke；MCCS Director 可管理 active／probation／suspended 状态 | 18 MSG 可撤销授权；文件不全可逐级暂停，第四次可 dissolution | 这是基地运作许可与合规权，不是组织所有权或内部控制 |

完整字段及 locator 见 `regime_governance_matrix_lead_only_v1.csv`。

## 3. 组织映射

当前只能形成有界 crosswalk：

- MCIPAC 2026 roster 将 AWWA、MOSCO 与 Marine Thrift Shop 列为 active PO；这证明当前行政准入，不证明 MCCS 隶属或资金支持。
- Kadena 2024 OI 明确授权 Kadena Officers' Spouses Club 的 Gift Corner 与 Kadena Enlisted Spouses Club 的 Thrift Store 持续零售。
- 现有 AWWA 组织关系把 KOSC 与 MOSCO 都列为成员，因此 AWWA 伞状网络至少横跨 Kadena 与 MCIPAC 两套行政授权环境；AWWA 不能被画成某一基地 command 的下属组织。
- `Okinawa Enlisted Spouses' Club` 与 Kadena OI 的 `Kadena Enlisted Spouses Club` 名称并不完全相同，本包不自动合并。
- NOSCO／ACGO 的当前 installation authorization 没有在本轮官方公开页中闭合；它们没出现在 MCIPAC roster 也不能推出“没有基地授权”。

逐组织字段见 `actor_regime_crosswalk_lead_only_v1.csv`。

## 4. 对研究设计真正有用的变化

现有“组织—组织”与 990 资金图缺少一个上游层：**基地授予的运作位置**。如果只画 AWWA、俱乐部和 recipient，会看见资源流，却看不见谁决定它们能否进场、开店、使用场地、保留资格，以及管理端掌握哪些资料。

本线索建议未来另开正式工作包，最先检验两件事：

1. 以每个组织为单位取得 authorization letter、license／out-grant、active-status history 和费用条款，确认“场地准入”到底到组织哪一层；
2. 向相应 installation records office 定向索取 constitution／bylaws、annual budget、quarterly financial statements、bank statements、donation receipts、minutes、officer roster 和 audit／review。请求对象应按 MCIPAC、Kadena、Navy／Army 分开，不再笼统向 “MCCS” 要一套总账。

这仍然只是研究设计线索。未获负责人批准前，不创建请求、不建中央边、不把 command 画成 funder 或 controller。

## 5. 负检索与边界

`negative_search_log_v1.csv` 记录五类未闭合项：NOSCO／ACGO 当前授权、OESC—Kadena Enlisted 名称 crosswalk、各组织具体 license／房租条款、Kadena 2025 新分类以及 MCIPAC roster 的辖区边界。

本包不得被误读为：

- 基地准入等于 DoD／MCCS 所有、指挥或控制该组织；
- 监管、审计或保留文件等于政府提供资金；
- 可依法提供有限后勤等于该组织实际得到免费场地、设备或水电；
- thrift／gift shop 的零售例外等于政府补贴、独占权或合法性效果；
- 未在某一军种 roster 出现等于没有授权、已经解散或在基地外运作；
- command 端保存 donation receipt 等于该记录已经公开、已经取得或已经批准进入本项目事实层。

## 6. 文件

| 文件 | 用途 |
|---|---|
| `regime_governance_matrix_lead_only_v1.csv` | 两套基地制度的授权、费用、后勤、责任、撤销和档案字段 |
| `actor_regime_crosswalk_lead_only_v1.csv` | AWWA／五个俱乐部／Marine Thrift Shop 的有界制度映射 |
| `source_receipts_v1.csv` | 十个官方来源入口、locator、归档状态与解释边界 |
| `local_artifact_manifest_v1.csv` | 两份成功冻结原件的大小与 SHA-256；其余官方站点的 CLI 拒绝页没有冒充档案 |
| `negative_search_log_v1.csv` | no-hit、名称未闭合和费用未公开记录 |
| `unexpected_findings_register_v1.csv` | 三条侦察链、十条 `lead_only` 观察 |
| `validate_package_v1.ps1` | 本包条数、隔离字段、关键字段和本地哈希验证 |

## 意外发现登记

本包登记 10 条观察，最大 `recon_step=3`。所有记录固定为 `lead_only / claim_eligibility=no / central_writeback=no / human_review_trigger=no / publication_eligibility=no`。最重要的线索是“私人内部治理＋基地运作许可＋成本回收支持”三者必须分层；它不进入本轮结论或展示。

## 7. 复现与验证

```powershell
powershell -ExecutionPolicy Bypass -File outputs\us_presence_network_wave2_base_private_org_governance_lead_v1\validate_package_v1.ps1
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_base_private_org_governance_lead_v1
```
