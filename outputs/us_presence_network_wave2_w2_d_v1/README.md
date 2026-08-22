# W2-D Bridge audit v1

日期：2026-08-22  
状态：`research_only / principal_review_pending / not_frontend_ready`。

## 1. 审计对象与计数

- 深描 tracer：S0 9 个服务 actor × A0 6 个问责 actor × 6 类关系 = **324** 条 pair-family 审计行。
- 确认性生态屏幕：S0 9 × A1R 41 × 6 = **2,214** 条；只表示现行 typed inputs 的覆盖，不产生生态级零关系。
- 候选敏感性屏幕：S0 9 × A1C 36 × 6 = **1,944** 条；绝不升级 candidate actor-issue 事实。
- 总矩阵：**4482** 条。
- 15 个 tracer × 5 个来源族 = **75** 条对称来源覆盖记录。
- 人物消歧队列 **9** 条；负检索 **13** 条；负责人判断 **9** 条。
- 通过 actor identity/function admission 且进入新版本选择框的 S1 actor 当前为 **0**。Marine Thrift Shop（X018）仍是 tracer/admission 候选。

## 2. 当前最强发现

### 直接组织关系：有界零，不是现实零

S0×A0 的 54 个直接组织配对中，**36 个**满足本轮 `audited_public_record_zero`：两端在 2023–2025 有活动锚点，A0 官方材料与服务侧 W2-A/W2-B corpus 已作对称名称／关系检索，没有确认命中。其余 18 个不进入零关系计数：X008/X009 的全国财务／roster 来源族不完整，X017 缺同期活动锚点。

因此可写：**“在声明的 2023–2025 公开资料窗口中，尚未确认两侧 actor 的直接组织关系。”** 不能写“两套生态现实中没有共享组织和人员”。

### 人物、recipient 与资助方仍是三种不同的缺口

- 现有提取人物没有 identity-resolved 的跨侧命中，但人物披露结构不对称，不能给 shared-person zero。
- W2-A 的六个 AWWA recipient 候选中三项有地方侧回应，零项闭合同一金额／税期，也没有确认问责侧端点。
- Schedule B 匿名性与部分 funder extraction 缺口，使“没有共同资助方”不可检验；未来即使命中，也只表示来源相交，不表示组织协调。

### 真正闭合的是共同制度接口

DoD 一边是 USO 全国 `HQ00342310002` prime award 的拨款机构，另一边是 Okinawa Dugong 诉讼的被告／问责对象。它说明两套组织生态围绕同一制度核心运作，但**不是 USO Okinawa 与 Earthjustice／CBD／TIRN 的组织桥**，也不能把全国 USD 72m award 分配给冲绳。

服务侧另有一条官方来源支持、但尚未过负责人审定的有向候选：**NMCRS→ARC**。它表示 NMCRS 委托 ARC 在非营业时段提供入口，并使用 NMCRS 资金；审定前不写成已确认服务中介。

## 3. 关系语法

六类桥分别保存：直接组织、人物、recipient／中介、共同资助方、同一事件、同一地点。共享地点永不计 bridge；同场参与永不升联盟；共同资助方永不自动解释为协调。

`audited_public_record_zero` 只在 tracer frame 的直接组织关系中使用。A1R/A1C 仍是覆盖屏幕；没有经过逐 actor 对称来源审计的 pair 一律 `unresolved`。

## 4. 文件

| 文件 | 用途 |
|---|---|
| `bridge_audit_matrix_v1.csv` | 4,482 条 pair×关系族审计矩阵 |
| `actor_window_observability_v1.csv` | actor 在主窗口的可观察性与锚点 |
| `source_family_actor_coverage_v1.csv` | 15 tracer × 5 来源族 |
| `relation_family_coverage_v1.csv` | 三个 frame 的关系族覆盖摘要 |
| `person_disambiguation_queue_v1.csv` | 人物／拼写／别名人工消歧 |
| `negative_search_log_v1.csv` | no-hit、不可观察和结构性缺口 |
| `typed_egonet_nodes_v1.csv` / `typed_egonet_edges_v1.csv` | 不混关系类型的解释性 egonet 数据 |
| `fig_bounded_bridge_egonet_v1.svg` / `.png` | 共同制度接口与两侧内部关系图及 QA 预览 |
| `claim_table_v1.csv` | 可写／不可写的结论表 |
| `principal_review_queue_v1.csv` | 负责人判断队列 |
| `source_receipts_v1.csv` | 官方与内部输入的 URL／哈希收据 |
| `unexpected_findings_register_v1.csv` | 包内 `lead_only` 线索登记；本轮仅保留 19 列表头 |
| `validation_report_v1.json` / `manifest_v1.json` | 验证与文件清单 |

## 意外发现登记

本轮登记 **0 条**。`unexpected_findings_register_v1.csv` 只保留统一表头。以后如出现超出本包既定问题的观察，可以标为 `lead_only` 并沿单条线索追查最多三步，单包起点与跟进合计最多十条。这些记录不进入本包结论、中央事实、人工复核队列、publication snapshot 或前端。

## 6. 负责人当前需要决定

1. 是否接受 36 个 direct pair 的有界零措辞；
2. W2-A 四组跨组织姓名候选和 A070 chapter／人物别名；
3. DoD 是否作为独立 `system_interface` 层进入合成，而不进入 bridge 计数；
4. X018 是否在 actor admission 后进入新版本 S1 frame；
5. 是否维持人物层 tracer egonet，而不做覆盖不足的全网中心性。
6. 是否按 `NMCRS→ARC` 批准非营业时段入口／资金方向；批准前保持 candidate。

## 7. 不得误读为

- 不是现实中“两套生态零连接”的证明；
- 不是人物网络、资助网络或 recipient 网络已经穷尽；
- 不是共享地点／同场／共同资助方自动构成组织联盟；
- 不是把 DoD award、诉讼角色或系统接口写成 NGO 间资金边；
- 不是中央写回、publication adapter 或前端发布授权。

## 8. 复现

```powershell
python scripts/build_us_presence_network_wave2_w2_d_v1.py
python -m unittest tests.test_build_us_presence_network_wave2_w2_d_v1
python scripts/validate_research_work_package_v1.py outputs/us_presence_network_wave2_w2_d_v1
```
