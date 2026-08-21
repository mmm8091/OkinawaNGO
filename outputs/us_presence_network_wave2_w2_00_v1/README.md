# 对美主线第二轮 W2-00 统一锚点包 v1

日期：2026-08-22

状态：`research_only / not_frontend_ready / central_writeback=no`

W2-00 的任务不是提前下结论，而是先把第二轮的选择框、量尺、权威原件和口径冲突固定下来。本包合并了军属组织 990、USO 全国—冲绳层级、人口分母与问责尺度三条工作线，不改中央数据和前端。

## 1. 完成量

- 9 套版本化选择框，包括五家军属组织、USO 层级、13 个正向入场 episode、未入场匹配框、项目改变反例框、15 actor Bridge tracer、S0＋A1R 确认框和 S0＋A1C 敏感性框；
- 152 条锚点：W2-A 83、W2-B 32、W2-C 37；
- 43 条权威来源收据，其中 41 件原件已本地冻结并校验 SHA-256，2 个官方页面因 403 保留 URL、locator 与失败状态；
- 24 条 change note，记录预期口径在原件面前为什么失效、如何修订、会改变哪条结论；
- 4 套案例量尺和 7 项负责人决定队列。

152 条锚点中，151 条仍为 `ai_seeded`，1 条是既有的 `human_checked` OESC→AWWA USD 8,479。“已归档官方原件”不等于“已经负责人批准写入结论”。

## 2. W2-00 已经改变的研究认识

### AWWA 不再只是一个组织名，而是可追踪的中介节点

OESC 三个连续税期的 Schedule I 均列 AWWA 为 recipient：USD 16,308、14,371 和 8,479。AWWA 两个可比税期又分别披露向日本组织拨出 USD 91,838／64,077，向基地关联组织拨出 USD 33,320／30,812。六个日本侧具名收款描述已成为反向查证的 tracer。

这些记录可以支持“AWWA 承担基地组织资源与日本地方机构之间的分配中介”作为下一轮假设，但还不能说明下游 recipient 的态度，也不能说明资源产生了合法性效果。

### USO 的全国规模可见，冲绳分配层仍断裂

USO 2024 审计合并财报与 USO Inc. Form 990 是两个不同报告边界，不能相加或互换。USD 72m DoD award 可以闭合到 USO Inc. 全国 prime recipient，却不能闭合到 Indo-Pacific、Japan 或 Okinawa 的金额分配。

“冲绳 6 个中心”与目录中的“8 个地点”也已定位为类型差异：6 个 operating centers＋Kadena AMC terminal＋Okinawa Area Office。下一轮应继续查地区分配层和冲绳同口径服务量，不再按站点平均估算。

### 当前人口分母不能闭合，问责案例也需要重新取样

冲绳县同口径“军人＋军属＋家属”合计最后可闭合到 2011-06-30 的 47,300 人；县方同时说明 2012 年以后未继续获得同口径数据。47,000 医疗服务人口、57,100 具名构成小计和“接近 80,000”都不是同一个当前总体。W2-A／W2-B 因此不应发布当前人均数。

现有 13 个问责 episode 本来就按“已进入制度并留下记录”选入。`ENTRY=1`、`RECORD=1` 是选择条件，不是成功发现；在匹配的未入场案例和项目改变反例查完前，不应继续扩大“结果有明确上限”的总体表述。

## 3. 主文件

| 文件 | 用途 |
|---|---|
| `selection_frames_v1.csv` | 9 套选择框及各自的纳入、排除和解释边界 |
| `selection_frame_actor_members_v1.csv` | S0、A0、A1R、A1C 与 tracer 成员 |
| `selection_frame_episode_members_v1.csv` | TE01–TE13；9 个 reviewed-process 与 4 个 candidate-event 分层 |
| `anchor_ledger_v1.csv` | 152 条统一锚点，含期间、单位、locator、允许表述与禁止外推 |
| `source_receipts_v1.csv` | 43 条权威收据及本地原件哈希 |
| `change_notes_v1.csv` | 24 条口径调整及对数字／结论的影响 |
| `case_scale_registry_v1.csv` | AWWA／军属俱乐部、USO、问责、公共资源四套初始与当前量尺 |
| `principal_review_queue_v1.csv` | 7 项负责人决定，未回传前均不改事实状态 |
| `validation_report_v1.json` | 唯一键、引用、原件哈希、选择框计数和中央／前端零写入检查 |

三个子包保留更细的原始表与说明：

- `outputs/us_presence_network_wave2_w2_00_spouse_990_v1/`
- `outputs/us_presence_network_wave2_w2_00_uso_v1/`
- `outputs/us_presence_network_wave2_w2_00_system_accountability_v1/`

## 4. 下一步的放行条件

负责人检查点见 `docs/us_presence_network_wave2_w2_00_principal_checkpoint_v1.md`。七项决定完成后：

- W2-A 可做五家组织的三税期资源流、人物和 recipient 反向核查；
- W2-B 可做 USO 全国—地区—冲绳的层级瀑布图和服务量缺口；
- W2-C 可开始匹配未入场案例、项目改变反例与并列结果轴；
- W2-E 可并行整理 1972–2012 两条历史背景线；
- W2-D 等 W2-A 的人物与 recipient 端点出来后再展开六类 Bridge audit。

## 5. 复现

```powershell
python scripts\build_us_presence_wave2_w2_00_v1.py
python -m unittest tests.test_build_us_presence_wave2_w2_00_v1
```

验证通过只说明这个 research-only 包的结构、引用和哈希闭合，不是中央事实升级、前端发布或对外结论授权。
