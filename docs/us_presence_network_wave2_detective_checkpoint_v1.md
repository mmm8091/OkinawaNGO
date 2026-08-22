# 对美主线第二轮：侦察检查点 v1

日期：2026-08-22

状态：`principal_checkpoint / research_only / W2-F_still_blocked / central_writeback=no / not_frontend_ready`

历史状态说明：本页记录人物决定与公开规则层升格之前的侦察暂停。负责人后续决定及当前结构见 `docs/us_presence_network_wave2_detective_checkpoint_v2.md`；本页不据此回写原先的条件情景。

## 一、这轮侦察把问题推进到了哪里

原来的问题是“谁给这些 NGO 钱、谁组织、为谁服务”。现在可以把它拆成一条可调查的四层结构：

```text
基地 command／行政接口
    └─书面准入、场地许可、合规检查、资格暂停／撤销
基地内 Private Organizations
    └─人员兼任／轮换、俱乐部筹资、组织间资金流
AWWA 等中介
    └─recipient 筛选、资源再分配、地方端叙事
冲绳福利／儿童／医疗／教育机构
```

目前最值得继续检验的不是“这些组织是不是亲美”，而是：**基地准入、私人筹资、人员轮换和地方福利中介是否共同构成一套不完全依赖政府直接拨款的社会基础设施；其中哪些环节由驻军制度安排，哪些来自私人组织自身运作。**

这仍是待检验的工作模型。各层事实、候选人物和 `lead_only` 线索继续分开保存。

## 二、负责人决定已经落账

1. non-entry 的严格筛查结果 `arm_not_established` 获接受；2004 公害调停只作 post-entry gate-control。2018-12-19 琉球水泥收件／退件原件已列为具名任务 T2-H。
2. Himawari／Ambitious 继续按不同事件处理；Kana-san 只闭合 recipient 回应。AWWA 下一税期补查没有在 IRS 公开索引中找到 2025-05-31 期末申报，故 Himawari 两条记录仍不闭合，但不推断“没有申报”。
3. Kana-san 与 Ambitious 的地方文本可编码为 `relationship_frame_local`；ToiToi 是下游回应；Himawari 只到受领、感谢和既往交流。均不升为 `narrative_uptake` 或 LEG3。
4. Marine Thrift Shop→Lions 的 USD 10,000 停在 Lions 中介。完整下游账簿与最终儿童医疗端点已列为具名任务 T2-I。

正式部分回传：`docs/human_review_return_USN_wave2_prerequisite_partial_v1.md`。

## 三、四条新线索

### 1. “民间”与“军方”之间不是隶属，而是经基地授权的私人自治

MCIPAC 与 Kadena 的官方规则指向同一种基本结构：私人组织是 non-federal／私人责任主体，不是 MCCS 部门或 NAFI；但能否在基地设施内活动、持续零售、使用场地并保持 active status，受 installation command 的书面授权、报表、检查和撤销机制约束。

现有材料还显示，MCIPAC 的持续场地使用要求 license 与水电／材料／服务成本偿还，Kadena 对 FSS 支持原则上按正常费用收费。公开证据没有证明免费房间或政府日常供养。因而应把以下关系单独建模：

- `installation_authorization`
- `administrative_monitor`
- `facility_license`
- `reimbursable_support`
- `resale_exception`

它们不是 affiliation、control 或 funding。真正有价值的新资料入口，是 command／MCCS／FSS 保存的章程、预算、季度账目、银行流水、捐赠收据、会议纪要、人员名单和审计材料。

证据包：`outputs/us_presence_network_wave2_base_private_org_governance_lead_v1/`。当前为 10 条 `lead_only` 观察。

### 2. AWWA 可能同时是资金中介与人员轮换接口

人物补证使五组判断出现明显分层：Trinicia 为很高收敛的 AWWA／KOSC 同一人候选；Brooke 与 Amber 为高收敛；Jen／Jennifer 为中等；Lesilee 只影响 OESC 内部连续性。它们都在服务侧内部，不是服务侧—问责侧人物桥。

情景网络不替负责人作人物合并，只计算“如果接受”的后果：

| 情景 | AWWA 所在分量 | 结构变化 |
|---|---:|---|
| 仅 very_high | 3／5 个焦点组织 | AWWA—KOSC 条件人物边与 OESC→AWWA 已核资金边把 AWWA、KOSC、OESC 放进同一分量 |
| 再加入 high | 3／5 | 若 Amber 获接受，AWWA—OESC 成为唯一同时有人物候选与已核资源流的组织对 |
| 再加入 moderate | 4／5 | Jen／Jennifer 获接受后，NOSCO 才接入；MTS 仍在五组织内部网络之外 |

由此形成一个可证伪的假设：**AWWA 可能不仅承接资源输入，也承接俱乐部换届人员和行政经验；服务网络靠人员轮换与重复资金输入保持连续，而不是靠正式上下级。** 这不是组织控制、正式伞状隶属或影响力排名。

证据包：`outputs/us_presence_network_wave2_person_disambiguation_supplement_v1/` 与 `outputs/us_presence_network_wave2_service_person_scenario_v1/`。

### 3. 地方 recipient 目前不是“多家组织直接汇聚”，而是“中介后不可透视”

端点侦察包机械读取 6 张表、137 行，整理 30 条相关观察和 11 个具名／暂定地方福利端点。在这个 `lead_only` 抽取框内，去重前有 2 组疑似多 provider，去重后没有一组达到“独立多源汇聚”的闭合门槛：

- ARU 是直接申报描述与 MTS 多跳页面之间的英文近名候选；
- 平敷屋是同一次交付中的四名贡献者，不是四次独立流入；
- Kana-san、Ambitious、Himawari 是同一 provider AWWA 的重复材料；
- KOSC／OESC／MOSCO／MTS→AWWA 不能在没有 earmark 时投影成它们各自对 AWWA 下游 recipient 的直接资助。

这项包内观察只登记一个待检验方向：公开材料可能更容易显示“AWWA 汇总上游资源后再分配”，而不是“多个俱乐部分别直达同一地方机构”。它不进入当前研究结论；完整 recipient 年表和受赠方账簿到位、并通过正式事实门后，才能重算并比较两种结构。

证据包：`outputs/us_presence_network_wave2_recurrent_recipient_lead_v1/`。

### 4. 福利合作与基地政治可能按角色和栏目分仓

Ambitious 的有界侦察发现，同一名资深内部人士照喜名通在个人署名栏目中保留对美军暴力的有限问责与政治距离，又在 2024 年具名参加 AWWA 活动、致谢并说明设备配置。AWWA 的正面活动报道则是未署名的机构刊物声音，不能归到他个人。

更值得检验的问题因此不是“收了资源后是否变亲美”，而是：**地方福利组织能否通过角色、栏目和体裁分区，让福利合作在不要求政治认同的情况下持续。** 现有 9 条观察只到 `lead_only`，不能写成 Ambitious 的组织立场或合法性效果。

证据包：`outputs/us_presence_network_wave2_recipient_voice_recon_v1/`。

## 四、这轮仍未闭合的关键事实

- 本轮人物补证只覆盖服务侧内部，尚未确认服务侧与问责侧的共享人物；问责侧 roster 与同期任职覆盖不足，不能据此报告跨生态人物零值。
- 没有闭合两个以上基地侧 provider 分别流入同一地方 recipient。
- 没有证明 military command／MCCS 为这些私人组织提供免费场地、日常财政供养或组织控制。
- 没有把 Lions 的 USD 10,000 闭合到最终儿童医疗机构。
- 没有把地方感谢、bridge／goodwill 语言证明为对美军存在的接受。

这些是有界公开资料结果，不是现实世界的绝对零。

## 五、下一步研究管理建议

在继续扩大网页采集之前，建议负责人先决定两件事：

1. **人物判断**：完成 HR-USN2-01a—01e。01c Amber 决定是否存在目前唯一的“人物＋资金”同组织对重叠；01b Jen／Jennifer 决定 NOSCO 是否进入 AWWA 分量。
2. **是否把新结构升为正式工作包**：若同意，下一包只做“基地准入—私人组织—AWWA—recipient”四层网络，先取每组织 authorization／license／财务报送目录，再选择 3—5 个 recipient 做完整端点与地方回应比较。角色分仓另作为小型话语比较，不与资金因果混写。

W2-F 仍未放行：除上述解释性决定外，HR-USN2-02／03、06a／06c、07—14 与三份信息公开请求的实际发送仍未完成。W2-G、中央事实、publication adapter 与前端继续无授权。

## 意外发现登记

本检查点不新增观察，只索引各包自己的登记表。所有 `lead_only` 记录继续留在包内，不进入结论、中央事实、人工复核队列、publication snapshot 或前端。
