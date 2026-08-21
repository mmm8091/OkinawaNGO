# USN-HR-01：现有 43 条关系的分层归位

日期：2026-08-19

状态：负责人已于 2026-08-21 确认；六行规则决定全部回填。研究支持见 `docs/human_review_research_USN_relation_retype_v1.md`，正式回传见 `docs/human_review_return_USN_relation_retype_v1.md`。

任务性质：语义归位，不复核原事实，不新增关系

## 为什么要做

旧表把资金、服务、隶属、法律角色、共同活动和机会线索放在同一张 43 行样本表里。现在准备做社会网络分析，需要先决定每一行属于哪一种观察单位。

候选明细：

`outputs/us_presence_relation_retype_v1/relation_retype_crosswalk_v1.csv`

负责人回填表：

`outputs/us_presence_relation_retype_v1/HR_USN_relation_retype_rules_v1.csv`

## 需要填写

默认只填写六行规则表的 `decision`：

- `accept`：同意 `proposed_usn_table_id` 和 `proposed_record_family`；
- `revise`：部分或全部不同意归位，请在 `principal_note_or_exceptions` 写明例外 edge ID、应去的表及理由；
- `exclude`：这条历史记录不应进入新架构；
- `defer`：需要先补事实或端点判断。

## 六项决定

1. `USN02 money_flows`（8 行）：捐赠、赞助、grant 与汇总财务观察；重点检查是否真有资金方向，commission 不在这一组。
2. `USN04 service_recipient`（4 行）：实物捐赠、共同捐赠和采购协助；重点检查 recipient 是实名机构还是未解析标签。
3. `USN05 affiliation_control`（9 行）：会员／伞状组织／全国—地方隶属；这里只确认结构类型，不把 membership 改成 control。
4. `USN06 action_institution`（20 行）：案件角色、行政委托、共同活动、协调及基地服务点；这些行保留案件／事件／机构／地点节点，不生成同场组织两两边。
5. `LEAD`（F012）：NOFO 仍是机会线索，不进入资金流。
6. `EXCLUDE`（F008）：已拒绝的重复行只留历史。

## 本次决定不会联动什么

这次只审“归哪张表”。原来的 `review_status`、`claim_status`、金额、端点身份和图资格全部原样保留；候选事实不会因为归位而变成已核事实。

不需要机械填写 43 个相同决定。六条规则获批后，由合并器把决定展开到 43 行；有例外时只处理 note 中点名的 edge ID。

## 验收

- 六条规则均有决定；
- `revise`／`defer` 规则有简短说明；
- F012 不得进入资金流；
- F008 保持历史排除；
- 任何 commission 不因本次归位新增付款金额；
- 任何共同活动不因本次归位生成联盟边。
