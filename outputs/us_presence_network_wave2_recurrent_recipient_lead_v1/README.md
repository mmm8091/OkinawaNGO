# 冲绳地方 recipient 重复流入侦察包 v1

日期：2026-08-22
状态：`lead_only`
范围：W2-A、LEG2、中央关系样本与 service recon 的现有研究材料；只对两个最高价值端点各追加三步线上跟进。

## 包内侦察观察

**在本包抽取并去重的 11 个端点中，尚无闭合的独立多源汇聚。**

本包机械读取 6 张现有表的 137 行，整理出 30 条与端点审计有关的观察，落到 11 个具名或暂定的冲绳地方福利、儿童、医疗、教育端点。去重前只有两组看起来涉及多个基地侧提供者；逐条检查交易链、事件和身份以后，确认的“两个以上不同基地侧组织分别、独立流入同一地方 recipient”仍为 **0**：

- `NPO ARU` 同时出现在 AWWA 申报和 Marine Thrift Shop 页面，但 MTS 原文是斜杠连接的多跳路线，现有人工边界也将它暂缓为英文近名候选；`一般社団法人ある` 的官网可以说明组织性质，不能闭合这两个英文标签或收款事实。
- 平敷屋的课后儿童中心确有四个具名贡献者，但四者都属于 2025-08-15 同一次三台风扇交付，物品没有按贡献者拆分；这是一项共同事件，不是四次独立流入。
- `かなさん沖縄`、`アンビシャス`、`ひまわり` 有重复记录，但提供者始终是 AWWA，属于同一 provider 的跨期或多材料复现，不是跨 provider 汇聚。
- KOSC、OESC、MOSCO、MTS 向 AWWA 的流入，不能沿着 AWWA 再投影给每一个地方 recipient。没有 earmark 或同一笔款项的闭合链时，`provider → AWWA → recipient` 只是一条中介结构，不能重复计作若干条直接资助。

这是 `lead_only` 包内部的机械观察，不是当前研究结论，也不是“现实中不存在共同 recipient”。它不支持组织联盟、政治认同、地方接受或合法性效果。

## 三类去重判定

本包把每个疑似重叠端点优先放进以下三类；另外保留“同一事件共同贡献”这一必要的事件类：

1. `independent_provider_to_recipient`：两个 provider 分别有端点、日期／期间和来源闭合的直接流入。本轮在地方 recipient 中为 0。USO 有多来源记录，但它是基地侧服务节点，不在地方 recipient 分母内。
2. `same_chain_via_awwa`：上游组织先给 AWWA，AWWA 再向地方端点分配。若没有 earmark，不把上游组织投影成地方端点的直接 provider。
3. `english_near_name_candidate`：英文近名、译名或项目标签相似，但法人身份或交易端点未闭合。ARU 属于这一类。
4. `same_event_joint_contribution`：多个贡献者出现在同一交付事件中。平敷屋属于这一类；贡献者数不能替代独立事件数。

逐案处置见 `endpoint_dedup_disambiguation_v1.csv`；11 个端点的 provider／event 计数见 `recurrent_recipient_audit_v1.csv`。

## 分母与筛选

纳入的地方端点须同时满足：

- 位于冲绳地方福利、儿童、医疗或教育语境；
- 至少有具名 recipient，或像平敷屋一样有明确而暂定的描述性端点；
- provider、recipient 和动作能在现有表或已归档来源中定位。

下列记录被保留在审计库存中但不进入 11 个端点的确认分母：

- AWWA、Lions 等中介节点；
- USO 等基地侧服务组织；
- Ashibina Child Development Center 的基地侧受益群体；
- `Miyako Facilities`、`Ishigaki Facilities` 等无具名最终端点的区域桶；
- 不能闭合到某一 recipient 的 aggregate 或 transitive projection。

因此，0 的分母不是“所有冲绳机构”，而是本轮现有材料中可被整理为 11 个地方端点的有界观察框。`audit_summary_v1.csv` 保存完整计数。

## 两条三步跟进链

只对两个会改变“多源汇聚”判断的端点跟进：

### ARU

1. 复看 MTS 原始页面：确认它是多跳路线文本，不是清楚的 `MTS → ARU` 直接边。
2. 查 `一般社団法人ある` 官网：确认其法人形态、2020 年法人化及青年／福利项目；同时保留与 `NPO ARU` 的法律形态冲突。
3. 查 recipient 官网及精确名称组合：未找到 AWWA／MTS 的受赠确认，按三步上限停止。

### 平敷屋／Kimutaka

1. 复看 DVIDS：四个贡献者属于同一交付事件，三台设备无份额拆分。
2. 查うるま市官方目录：`きむたかこどもセンター学童クラブ` 位于平敷屋、服务平敷屋小学学区，是地理身份候选。
3. 查市政府及名称组合：未找到把 Kimutaka 与该交付闭合的 recipient-side 回执，也没有第二次独立流入，按三步上限停止。

新归档原件在 `artifacts/`；查询、否定结果与其不能证明的内容分别在 `source_receipts_v1.csv` 和 `negative_search_log_v1.csv`。

## 文件

- `recipient_observation_inventory_v1.csv`：30 条直接、间接、同事件和明确排除观察。
- `recurrent_recipient_audit_v1.csv`：11 个地方端点的 provider／event 去重结果。
- `endpoint_dedup_disambiguation_v1.csv`：AWWA 同链、ARU 近名、平敷屋同事件和 USO 范围排除。
- `audit_summary_v1.csv`：分母、候选重叠、确认重叠与跟进数量。
- `lead_only_online_followup_v1.csv`：两条链共 6 条线上跟进观察。
- `source_receipts_v1.csv`：4 份关键网页／PDF 收据与哈希。
- `negative_search_log_v1.csv`：4 组有界否定检索及不确定性。
- `input_manifest_v1.csv`：6 张表和 4 份来源／跟进原件的输入哈希。
- `unexpected_findings_register_v1.csv`：标准 19 列、8 条意外发现登记。
- `manifest_v1.json`、`validation_report_v1.json`：输出哈希和机械验证。
- `reproduce_recurrent_recipient_audit_v1.py`：复现脚本。

## 复现与验证

在仓库根目录运行：

```powershell
python outputs\us_presence_network_wave2_recurrent_recipient_lead_v1\reproduce_recurrent_recipient_audit_v1.py
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_recurrent_recipient_lead_v1
python outputs\us_presence_network_wave2_recurrent_recipient_lead_v1\validate_recurrent_recipient_package_v1.py
```

复现脚本会核对关键行、输入哈希、11 个端点、三类去重语法、观察上限和 `lead_only` 状态。`PASS` 只说明封包机械一致，不能把本包提升为中央事实、人审决定或发布结论。

## 边界

- 不改 actor registry、关系中央表、HR 任务、publication adapter 或 frontend。
- 不把共享 recipient 写成组织联盟、协调关系或政治立场。
- 不把 recipient 的实用性受赠或感谢写成对驻军的接受或合法性提升。
- 不把一次共同交付拆成多个独立流入；不把 AWWA 上游资金投影给下游端点。
- 否定检索只表示声明的来源族和三步范围内未找到，不能证明现实中的绝对不存在。
- 若以后拿到 AWWA／MTS recipient 年表、地方机构回执或有 earmark 的正式申报，应重新运行端点与事件去重，而不是沿用本轮 0。

## 意外发现登记

登记表共 8 条，分成 `ARU` 与 `HESHIKIYA` 两条链，每条从机械异常开始，最多跟进三步。所有记录固定为：

- `workflow_status=lead_only`
- `claim_eligibility=no`
- `central_writeback=no`
- `human_review_trigger=no`
- `publication_eligibility=no`

本轮的意外发现不是“共同 recipient 网络”，而是：现有材料中最像多源汇聚的两个端点，分别被交易链、身份和事件去重消解了。继续寻找真正的汇聚端点，需要 recipient 年表或受赠方原件，而不是继续叠加 donor-side 新闻稿。
