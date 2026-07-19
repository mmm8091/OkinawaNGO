# NR-03 复验结论与组织关系前端整改／实现说明 v1

日期：2026-07-20  
接收方：前端／下一实现 session  
负责人决定：已确认  
本文件是可直接执行的换手说明；不授权修改中央研究事实表

## 1. NR-03 v2 复验结论

### 总体判定

NR-03 主体功能验收通过，保留三项非阻断性收尾整改。关系层尚未实现，本文件后半部分给出
已批准的 schema 和前端呈现规则。

### 已通过

- `npm run build` 通过；
- 浏览器控制台 0 warning／0 error；
- 地图→地区→episode→路径→来源抽屉完整跑通；
- 122 actor 全量搜索可达，A073 检索通过；
- 有事件的组织（复验使用 A002）→事件记录→2003 时间页跑通；
- 地区比较与 episode 六阶段比较通过；
- 证据抽屉显示 locator；
- 390×844 下无页面级横向溢出；
- 12 张换手截图哈希互异。

本轮复验截图：`docs/nr3_v2_acceptance_audit_assets/`。

### 三项收尾整改

1. **英文界面仍有中文 UI 残留。**  
   证据页标题、品牌／导航辅助名称、语言与视图切换 aria-label、地图与画布控制等需要完整
   i18n。组织名、来源原文和研究数据字段可按既定边界保留原文。

2. **换手件应拆开两条测试。**  
   A073 只证明“全量 registry 搜索可达”，因为其当前为 0 议题／0 事件。组织→事件→时间
   链由 A002 等有事件 actor 证明，不能写成 A073 自身完成全链。

3. **跨路由关闭证据抽屉。**  
   从路径页打开来源后切换到组织等页面，旧抽屉不应继续覆盖新页面；路由改变时清空 drawer
   selection。

### NR-03 收尾 done_when

- EN 模式下固定 UI 文案和 aria-label 不残留中文；
- 换手说明分别记录 A073 搜索测试与 A002 事件测试；
- 路由改变后证据抽屉关闭；
- 1280×900 与 390×844 回归通过；
- build 与 console 继续为 PASS／0。

## 2. 负责人本轮批准的产品决定

三项均为“是”：

1. 已核视图允许显示“关系已确认、部分字段待核”的记录；
2. 用户界面将“演示视图”改名为“已核视图”；
3. 前端主动显示“已确认什么／尚未确认什么”，不只显示证据等级。

内部 `demo/` 目录可暂时保留兼容，但界面不得继续显示“演示视图”。

## 3. 新状态模型

权威规则：`data/metadata/coding_schema_v1.md`。

前端必须把五个维度分开：

| 维度 | 回答的问题 |
|---|---|
| evidence_level | 材料本身有多强 |
| review_status | 当前处于什么复核流程 |
| human_decision | 负责人作了什么决定 |
| claim_status | 当前可以支持多强的主张 |
| graph_eligibility／display_tier | 可以在哪里、以什么身份展示 |

禁止推断：

> E4 ≠ 人审通过；人审通过 ≠ 全字段确认；关系存在 ≠ 组织关系边；组织关系边 ≠ 联盟。

## 4. 已核视图与研究视图

### 已核视图

- `supported`
- `supported_bounded`

`supported_bounded` 必须显示具体缺口，例如：

```text
关系存在　✓ 已核
方向　　　✓ 已核
期间　　　? 待核
金额　　　— 未公开
端点身份　✓ 已核
```

### 研究视图

- 包含已核视图全部内容；
- 增加 `candidate`；
- 在独立“研究线索”区增加 `lead`。

### 不展示

- `rejected`
- `unsupported`
- duplicate
- E0 claim

## 5. 关系数据不能使用单一 edges 数组

权威架构：`docs/actor_relation_architecture_v1.md`。

NR-02 构建模块应输出：

```text
dyadic_relations
case_roles
event_participation
administrative_records
aggregate_observations
relation_leads
genealogy_anchors
```

前端只消费这些已经分类和 gate 的集合，不读取中央 CSV，也不根据 `review_status` 自行决定
谁进入已核层。

### 当前43行的真实边界

- 27行两端均为 registry actor；
- 16行一端为 place、program、unknown recipient、临时机构／recipient标签；
- F008 是 rejected duplicate；
- 六条 legacy `verified` 已由 HR-033 决定并合并，旧值清零。

合并后 43 行按 review status 为：15 `human_checked`、2 `human_revised`、20
`ai_seeded`、4 `needs_second_source`、1 `needs_local_retrieval`、1 `rejected`。因此前端和
文案仍不得写“43 条组织关系”或直接写“17 条已核组织关系”；17 是人审行数上限，还须经过
endpoint／claim／graph eligibility gate。

HR-033 为构建模块提供了 6 条已决 dyadic relation 和 1 条 aggregate observation 的标准化
输入：`outputs/hr033_integration_v1/typed_relation_observations_v1.csv`。

## 6. L0 组织面板

新增两个独立区域：

### 与其他组织的关系

只接收 `graph_eligibility=dyadic_relation`。每行显示：

- 关系家族、关系类型；
- 对方组织、方向和角色；
- claim status；
- 已确认字段／缺失字段；
- evidence level；
- review status；
- 来源和 locator；
- interpretation limit。

### 其他记录与研究线索

显示：

- actor—place／program行政或服务记录；
- aggregate observation；
- event participation；
- NOFO、co-presence、unknown recipient等lead。

必须显式写“非组织关系边”或“线索，非资助事实”。

## 7. L1 组织关系图

关系家族独立开关，不做单张混合毛线球。

视觉编码固定为：

- 颜色＝关系家族；
- 箭头＝方向；
- 实线＝已核；
- 虚线＝候选；
- E4／E3／E2＝标签；
- 缺失字段＝文字标签；
- 边宽固定；
- 节点面积和度数不表示影响力。

法律案件使用 actor／person／institution—case—role 结构。不得把27行同案角色变成组织
两两协作边；原告、律师、被告、supporter、requester、commenter、non_party保持不同，
`non_party` 永不生成边。

结构关系在数据中保留 national—regional、umbrella—member 等方向与端点角色，不存成
无向事实。

## 8. L2 谱系泳道

等待 NR-04／NR-05 候选和人工决定后启用：

- formed／renamed／split／merged为实线；
- coalition_successor换轨虚线；
- issue／place／person continuity为弱连续性；
- 候选虚线框，人审后实心；
- 0锚点继续作为材料缺口显示。

## 9. 前端计数

禁止“关系共N条”的混合总数。至少分开：

- 已确认组织关系；
- 有限确认记录；
- 待审候选；
- 研究线索；
- 隔离／排除。

actor—place、actor—program、case role、aggregate observation不计入组织—组织关系。

## 10. 四个验收控制案例

| 记录 | 预期呈现 |
|---|---|
| F021 | 已核直接捐赠：3,250 美元、事件日 2025-12-02；不得显示为 sponsorship |
| F025 | 已核有界贡献边：KOSC→AWWA，金额为空，显示“金额未公开” |
| R10R029 | 102,000 美元混合 recipient 汇总观察；不上组织关系图，不分配给 F025 |
| F027 | 显示累计捐赠观察；recipient未列名，不上关系图 |
| F012 | 显示研究线索和“recipient未知／非拨款事实”；不上关系图 |

## 11. 实现顺序

1. 完成NR-03三项收尾整改；
2. ~~完成HR-033后，由构建模块迁移六条legacy `verified`~~（已完成）；
3. 扩NR-02构建模块和验证门禁；直接使用 HR-033 标准化输入，不再等待人工任务；
4. 实现L0两个面板区；
5. 实现L1分层关系图；
6. NR-04／05人工锚点到达后实现L2；
7. NR-06完成claim／evidence／交互验收。

## 12. 关系层 done_when

- 前端不读取中央CSV；
- 前端不自行重算display tier；
- 两端未解析为actor的记录不能进入组织关系图；
- supported_bounded始终显示confirmed scope、missing scope和interpretation limit；
- lead、NOFO、unknown recipient不上关系图；
- 同案参与不生成组织两两边；
- event共同参与不生成稳定联盟边；
- rejected／duplicate／E0不展示；
- 计数按确认／有限确认／候选／线索／排除分层；
- 已核／研究切换只增加候选，不改变已核记录的措辞和语义；
- 证据抽屉可追到source ID、locator和解释边界；
- build、validation、桌面与移动回归全部通过。

## 13. 不得被误读为

- “已核视图”不是“所有字段完整”；
- `supported_bounded`不是弱化版猜测，而是核心命题已核、字段缺口明确；
- 研究候选不是事实；
- membership不是funding；
- sponsor tier不是金额；
- project cost不是合同付款；
- service presence不是政治立场；
- 同案、同场、共同署名不是稳定联盟；
- 来源保存得多不等于组织影响力大。

## 15. 2026-07-20 前端启动同步

HR-033 已不再阻断关系层。前端 session 现在可以从第 3 步开始：

1. NR-02 增加类型化集合与统一 gate；
2. 首先接入 `outputs/hr033_integration_v1/typed_relation_observations_v1.csv` 的 7 条控制记录；
3. 用 F021、F025、R10R029 验证 donation／bounded dyadic／aggregate 三种呈现不会混淆；
4. 再扩到 43 行全表、R8 case roles 和 event participation；
5. 完成 L0 两区后再做 L1 分层关系图。

同步输入：

- `data/metadata/coding_schema_v1.md`
- `docs/actor_relation_architecture_v1.md`
- `docs/human_review_return_HR033_legacy_relation_status_batch30_v1.md`
- `outputs/hr033_integration_v1/`
- `data/interim/15_funding_or_support_edges_sample_v0.csv`
- `data/interim/21_admin_collaboration_relations_v0.csv`
- `data/interim/22_admin_amount_observations_v0.csv`
- `data/interim/23_admin_function_observations_v0.csv`

中央 CSV 仍只由构建模块读取；浏览器端只消费经过分类、验证并带 `display_tier` 的构建产物。

## 14. 建议使用的 skills

- `domain-modeling`：维护 evidence／review／claim／graph eligibility 的领域词义；
- `codebase-design`：把全部 gate 集中在 NR-02 构建模块的 interface 后面；
- `product-design:audit`：实现后用桌面／移动截图复验状态是否始终可见；
- `browser:control-in-app-browser`：跑地图、组织、案件、证据抽屉和双视图端到端链。
