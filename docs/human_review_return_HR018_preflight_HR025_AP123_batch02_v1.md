# HR-018 来源前置＋HR-025 AP123 回交报告 Batch 02

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——8/8 个来源前置核查＋1/1 个地点边决定**

## 0. 批次边界

- HR-018-S01–S08 只确认 URL、archive、main source ID 和指定 locator 是否存在，不批准对应关系、金额或解释。
- AP123 只决定 X016—地点的键与空间语义，不批准政治立场、资金关系或与其他组织的联盟。
- 本报告不直接修改 source log、archive manifest、中央 actor-place 表或 HR CSV。
- 所有负责人决定需在本报告确认后由主线程回填和合并。

## 1. HR-018 八个来源前置

### 总体核查结果

八个 URL 已经在主 source log 中分别映射为 S173、S174、S175、S186、S181、S176、S184、S183；八项均已在 `source_archive_manifest.csv` 记为 `archived`、HTTP 200，并存在本地 raw artifact。原前置队列中的 `pending_archive_and_source_log_prerequisite` 已与当前主线状态不一致。

建议负责人统一确认：

- `archive_verified=yes`；
- 按下表写入 `main_source_id`；
- 前置状态改为 `prerequisite_satisfied`；
- 仅解除相应 HR-018 关系行的“来源尚未入表／归档”阻塞，不预判关系结论。

| 前置项 | module ref → main source | locator 核查结果 | 必须保留的支持边界 |
|---|---|---|---|
| HR-018-S01 | R10S05 → S173 | PDF pp.9–10 点名沖縄NGOセンター、KIP 运营、`委託料 17,157千円` | 可送 HR-018-02 关系判断；来源前置本身不批准 commission edge |
| HR-018-S02 | R10S06 → S174 | PDF pp.9–10 点名沖縄NGOセンター、KIP 运营、`委託料 16,970千円` | 可送 HR-018-03；不从归档成功自动批准金额流 |
| HR-018-S03 | R10S07 → S175 | PDF pp.5–6 载总事业费 18,858 千円、ONC 委托料 16,662 千円及另列交付对象外 3 月运营费 2,196 千円 | 三个数的关系语义仍由 HR-018-04 决定；不得在前置层合并或推定同一 recipient |
| HR-018-S04 | R10S08 → S186 | 会议纪要参加者表把四名沖縄NGOセンター人员列在【事務局】 | 只支持会议的事务局参与；不单独证明合同、付款或完整职责 |
| HR-018-S05 | R10S09 → S181 | ONC 自有活动页明确写 KIP `運営（沖縄市委託）`，并分别介绍 NGO相談員功能 | 支持自报角色与功能；不支持具体金额，也不能替代公共机构方向证据 |
| HR-018-S06 | R10S10 → S176 | 冲绳市设施页说明 KIP 地址、国际交流据点、语学讲座、多语言交流与活动范围 | 只支持设施／服务范围；页面没有单独承担 ONC recipient 或金额证明 |
| HR-018-S07 | R10S11 → S184 | PDF p.1 点名新外交イニシアティブ、合同 12,842,500 円；p.2 点名沖縄平和協力センター两份独立合同 26,439,000 円与 8,479,000 円 | 可支持合同记录送 HR-018-08/09/10；仍须分别核 actor crosswalk 与项目边界 |
| HR-018-S08 | R10S12 → S183 | PDF p.2 给出协作形态字典：委託、提案型公募による委託、指定管理、補助等 | 只支持机制代码解释；不能用汇总字典单独批准某一 actor 关系或金额 |

### 负责人决定

**统一确认八项 `prerequisite_satisfied`。**

### 负责人理由／限制

八项均已进入主 source log、完成 HTTP 200 归档并核到指定 locator。该决定只解除来源前置阻塞，不批准对应 relation、amount、actor crosswalk 或解释。

## 2. HR-025 AP123 · X016—Camp Foster/Schwab 键冲突

现有行：

- actor：X016 Marine Officers' Spouses' Club Okinawa；
- `place_id=P006`；
- 行内 `place_name=Camp Foster`；
- place registry 中 P006 实际是 `Camp Schwab`；
- P007 才是 `Camp Foster`；
- 当前候选 semantic：`site_presence`；
- 原证据：S079、S080。

### 补查结果

- S079 支持 MOSCO 当前组织身份与冲绳慈善／社区功能；S080 支持其税务身份和 EIN。两者适合作 actor 身份证据，但单独承担 Camp Foster 地点证明显得不足。
- 美国海军陆战队官方 2012 年记录明确写明，MOSC 在 Camp Foster 的 Marine Gift Shop 举行奖学金活动；同文把奖学金描述为半年一次，并说明 MOSC 的资金来自 Marine Gift Shop 利润及定期拍卖。这支持 Camp Foster 是有界、重复性慈善／筹资活动场域，而不是 Camp Schwab。
- MCCS 当前 private-organizations 名单继续将 Marine Officers' Spouses' Club Okinawa 列为 `ACTIVE`，并明确这些组织是获准在 MCIPAC 设施活动的 non-federal private organizations。该名单支持当前组织状态与制度性质，但不应被误写成 MCCS 附属关系，也不单独证明 MOSCO 的具体 Camp Foster 地址。
- 没有发现 AP123 应指向 Camp Schwab 的证据。Camp Schwab 在本项目中另有 USO/AEC 等不同 actor 的地点记录，不能因 place ID 已存在而转移到 X016。

### 辅助建议

负责人决定建议写为：

- `review_decision=revise`；
- `place_id: P006 → P007`；
- `place_name=Camp Foster`；
- `place_semantic=site_presence`；
- 地点说明限定为“至少在来源所覆盖时期，MOSCO 的奖学金／Marine Gift Shop 筹资活动在 Camp Foster 有公开记录”；
- 不编码为 headquarters；
- S079/S080 继续支持身份，新发现的两项官方页面按正常 source proposal／archive 流程补入，其中 Marine Corps 2012 记录承担 Camp Foster 地点证据；
- 保留边界：服务／慈善活动在基地内出现，不等于拥基地或反基地立场，也不证明与基地管理机构形成组织联盟。

补查来源：

- MCIPAC 2012 奖学金记录：`https://www.mcipac.marines.mil/Media-Room/News/Article/531919/club-awards-scholarships/`
- MCCS 当前 private-organizations 名单：`https://www.okinawa.usmc-mccs.org/more/private-organizations`

### 负责人决定

**`revise`——AP123 的 `place_id` 从 P006 改为 P007，保留 `place_name=Camp Foster` 与 `place_semantic=site_presence`。**

### 负责人理由／限制

现有及补查证据支持 MOSCO 在 Camp Foster 的奖学金／Marine Gift Shop 慈善筹资活动，不支持 Camp Schwab。该地点边不是 headquarters 声明；服务／慈善在场不推定拥基地、反基地、政治立场、MCCS 隶属或组织联盟。S079/S080 继续支持身份，新增官方地点来源须按正常 source proposal／archive 流程进入主线。

## 3. 本批确认后的主线程动作

1. 在 `HR018_source_prerequisites_v0.csv` 为 S01–S08 回填 `archive_verified=yes`、对应 S173/S174/S175/S186/S181/S176/S184/S183，并记 `prerequisite_satisfied`。
2. 解除 HR-018-02–16 相应行的来源前置阻塞；仍须逐行完成人工关系判断。
3. 在 HR-025 回填 AP123=`revise`，中央 actor-place 边改为 X016→P007 Camp Foster、`site_presence`。
4. 将 MCIPAC 2012 记录和 MCCS current private-organizations 页面送入 source proposal／metadata／archive；来源纳入不扩大地点边的时间、政治或组织关系含义。
5. 合并 AP123 后重新生成 R03 空间语义、place-key validation、相关图表和最终 HR-029 输入；不得由 HR-029 再次改写 AP123。

本报告本身未修改中央 CSV、source log、archive manifest 或 HR 队列。
