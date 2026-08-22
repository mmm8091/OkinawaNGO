# 研究工作包协议 v1

日期：2026-08-22
状态：`principal_approved`
适用范围：本日起新建或重新打开的线上研究工作包。冻结的历史包只有在继续研究时才需补齐本协议。

## 1. 工作包仍以研究问题为中心

每个工作包先声明问题、选择框、观察单位、来源范围、方法、预期交付和负责人检查点。执行者可以调整检索入口、公式、样本窗口和图形形式，但须留下 change note；不能借“发现了新东西”无记录地改变原问题、分母或结论等级。

工作包同时保留两条相互隔离的通道：

- **主研究通道**：服务于已声明问题，按中央 schema 或模块 schema 形成来源收据、研究观察、分析结果、候选 claim、缺口和人工任务。
- **有限侦察通道**：只保存执行中偶然出现、尚未进入本包问题设计的线索，统一标为 `lead_only`。

## 2. 每包强制增加《意外发现登记》

每个适用工作包必须同时具备：

1. README 中的 `## 意外发现登记` 栏目；
2. 包根目录的 `unexpected_findings_register_v1.csv`；
3. 复现或验证步骤中对该表的结构与边界检查。

没有意外发现时，CSV 保留表头，README 明写“本轮 0 条”，这不是交付缺失。已经进入正式结果表、gap table、change note、负检索日志、当地任务或人工队列的事项不重复塞入线索簿。

固定字段见 `data/metadata/unexpected_findings_register_template_v1.csv`。关键字段语义如下：

| 字段 | 含义 |
|---|---|
| `record_kind` | `origin_observation` 或 `followup_observation` |
| `chain_id` | 同一条侦察链的稳定编号 |
| `parent_lead_id` | 跟进观察直接来自哪一条记录 |
| `recon_step` | 起点为 0，向外追查为 1—3 |
| `source_or_query_locator` | 观察所在来源、精确 locator，或产生 no-hit 的查询入口 |
| `potential_value` | 为什么值得将来另开问题；不是结论 |
| `next_test` | 若以后升级，最先应检验什么 |
| `stop_reason` | 达到边界、材料中断、已转正式任务等收束原因 |

线索表故意不设置 `review_status`。每行固定为：

```text
workflow_status=lead_only
claim_eligibility=no
central_writeback=no
human_review_trigger=no
publication_eligibility=no
```

## 3. 有限侦察模式

执行者在完成本包主任务时，可以自行进入侦察模式，不需逐条等待负责人批准，但必须同时满足：

- 从一条已登记的 `origin_observation` 出发；
- 一次“步”指从上一条观察沿一个人物、组织、recipient、资金、制度或来源端点再向外核一次，不以搜索词或打开网页次数计步；
- `recon_step` 最大为 3；
- 每包包括起点与跟进在内最多 10 条观察；
- 每条都保留来源或查询 locator、与父记录的关系和下一项可检验问题；每条侦察链的当前末端记录停手原因；
- 所有产物只留在该包的线索登记中，不进入主结果计数、网络图、claim table、中央表、人工队列或 publication adapter。

达到三步或十条后即停止。若继续追查会改变选择框、核心比较或对外结论，应先把现有线索整理成新的研究提案，交负责人决定，而不是继续扩包。

## 4. 何时不能留在线索簿

下列事项使用现有正式通道，不得用 `lead_only` 规避：

- 已在本包选择框内、会直接改变主结果的反例或口径错误：进入主表、change note 或 competing explanation；
- 组织身份、人物同一性、金额语义或因果归因已达到人工判断门槛：进入正式人工任务；
- 线上已尽且需要馆藏、内部年报或当地回应：进入当地／新一手材料任务；
- 已获负责人批准的信息公开请求：进入 request ledger；
- 已形成关系命题并准备进入研究视图：另建候选记录，接受现行 `review_status`、`claim_status` 和展示门禁。

## 5. 升级路径

`lead_only` 没有自动升级路径。若线索值得继续：

1. 新建一份简短研究提案，声明问题、选择框、预期材料、竞争解释和停手点；
2. 负责人决定继续、合并、暂缓或放弃；
3. 获批后给新研究对象分配新的正式 ID，并按正常来源、证据、复核与 publication 规则处理；
4. 原 `lead_only` 行只保留 provenance，并在 `stop_reason` 记录转入哪个任务或工作包。

因此，“被登记”只说明值得记住；“被追查”只说明在有限范围内做过侦察；二者都不表示事实成立、重要性已证、需要人工判断或可以对外展示。

## 6. 验证

通用验证命令：

```powershell
python scripts\validate_research_work_package_v1.py outputs\<package_dir>
```

验证只检查栏目、表结构、步数、条数、父子链和固定隔离字段。它不判断线索真假，也不授予任何事实、解释或发布资格。
