# HR-024 议题边＋HR-025 AP048/AP049 回交报告 Batch 03

日期：2026-07-19  
承办人：项目负责人  
辅助核查：Codex  
状态：**已完成——9/9 项决定**

## 0. 批次边界

- 本批处理 HR-024 可在线判断的 7 条 A076/A086 actor–issue edge，以及 HR-025 的 AP048/AP049。
- A073 的身份问题是 online-exhausted／当地核实项，不进入本批，也不据 E0 材料强行决定。
- A076/A086 的案件当事人角色已经 HR-014 人工确认；本批只决定是否从案件角色生成相应的、严格 `scope=case` 的 issue edge。
- 接受 case-specific issue edge 不等于持续组织定位、稳定国际联盟、案件胜诉、阻止工程或政策效果。
- 本报告不直接修改中央 actor–issue、actor–place、place registry、source log 或 HR CSV。

## 1. HR-024 · A076 三条案件议题边

共同证据基础：

- A076 是 Okinawa Dugong v. Rumsfeld / Center for Biological Diversity v. Esper 的具名组织原告，已经 HR-014 R8R004 人工确认；
- 法院／诉讼材料将案件对象限定在冲绳儒艮、NHPA §402 程序与普天间迁移至边野古沿岸的计划；
- A076 的成立、法律形式和诉讼后持续性仍须当地／组织级材料，本批不得据案件角色补闭合。

| 项目 | 候选 edge | 辅助建议 | 精确限制 |
|---|---|---|---|
| HR024-002 | A076→I004 `dugong` | `accept` | 仅指其作为具名原告参加冲绳儒艮／栖息地案件 |
| HR024-003 | A076→I011 `legal` | `accept` | 仅指通过美国 NHPA／APA 司法程序进入法律路径；不外推其他案件 |
| HR024-004 | A076→I003 `Henoko` | `accept` | 仅指该案件以边野古沿岸迁移计划为对象；不证明 A076 在所有时期都有独立边野古现场行动 |

建议三条统一写：

- `review_status=human_checked`；
- `scope=case`；
- `case_id=R8C01`；
- 不改变 A076 registry 的持续性／法律身份未闭合状态。

### 负责人决定

**三条全部 `accept`，统一保持 `scope=case`、`case_id=R8C01`、`review_status=human_checked`。**

负责人理由／限制：A076 的具名原告角色及案件对象已有 E4 法律材料和 HR-014 人工锚点。接受 I004/I011/I003 只表示同一案件中的儒艮、法律程序和边野古对象连接，不补闭合 A076 的法律形式、诉讼后持续性或独立现场行动。

## 2. HR-024 · A086 四条案件议题边

共同证据基础：

- A086 Turtle Island Restoration Network 是同案具名美国组织原告，已经 HR-014 R8R002 人工确认；
- 具名原告材料支持它进入儒艮与美国联邦法律程序；
- Earthjustice 2003 案件材料明确将美日保护组织共同诉讼、边野古珊瑚礁、海草床和儒艮栖息地置于同一案件背景；
- Form 990 只支持 A086 的一般海洋／野生动物使命，不能单独证明冲绳项目。

| 项目 | 候选 edge | 辅助建议 | 精确限制 |
|---|---|---|---|
| HR024-005 | A086→I004 `dugong` | `accept` | 只确认同案具名原告与冲绳儒艮议题连接 |
| HR024-006 | A086→I011 `legal` | `accept` | 只确认 NHPA／APA 案件程序；不外推其他冲绳诉讼 |
| HR024-007 | A086→I012 `international_advocacy` | `revise` | 把“跨太平洋法律倡议路径的一环”改成可观察事实：“美国海洋保护组织以具名原告身份参加涉及冲绳儒艮的美国联邦诉讼”；共同诉讼不等于稳定联盟 |
| HR024-008 | A086→I005 `biodiversity` | `accept_with_revision` | 写成“案件材料把珊瑚礁、海草床与濒危儒艮栖息地作为案件背景”；不写成 A086 在冲绳另有持续、全面的 biodiversity program |

四条均保持：

- `review_status=human_checked`；
- `scope=case`；
- `case_id=R8C01`；
- 不推定诉讼结果、工程影响、政策效果或持续组织合作。

案件材料：

- Earthjustice 2003：`https://earthjustice.org/press/2003/us-japanese-conservation-groups-join-in-legal-effort-to-save-okinawa-dugong-from-extinction`
- A086 opening brief：`https://seaturtles.org/wp-content/uploads/2019/01/19-01-02-OPENING-BRIEF.pdf`

### 负责人决定

**HR024-005、006 `accept`；HR024-007 `revise`；HR024-008 `accept_with_revision`。四条均保持 `scope=case`、`case_id=R8C01`、`review_status=human_checked`。**

负责人理由／限制：I012 改为可观察的跨境诉讼参与，不使用“路径的一环”作为事实措辞；I005 只记录案件材料中的珊瑚礁、海草床和儒艮栖息地背景，不推定 A086 在冲绳另有持续的综合 biodiversity program。共同诉讼不等于稳定联盟，案件参加不证明工程、政策或因果效果。

## 3. HR-025 AP048 · X014 NED—Okinawa Prefecture

既有补查与负责人范围决定已经确认：

- 没有公开证据支持 NED—冲绳 recipient、项目或地点关系；
- X014 保持 `scope_status=watchlist_only`，排除于默认冲绳组织网络；
- “未确认”不能扩写为跨年度“从未存在”。

辅助建议：在 HR-025 专门队列中正式写：

- `review_decision=reject_edge`／`retire_candidate`；
- 删除 AP048 作为 actor-place candidate；
- 不从 `unclear` 中选择任何地点 semantic，因为问题不是语义不明，而是地点边缺乏证据；
- X014 registry/watchlist 记录本身保留。

### 负责人决定

**确认继承前批决定：AP048=`reject_edge`／`retire_candidate`。**

负责人理由／限制：保留 X014 的 registry/watchlist 记录，但不保留缺乏公开关系证据的 Okinawa actor-place edge。“未确认”不得扩写为跨年度“从未存在”。

## 4. HR-025 AP049 · X015 Peace Winds Japan—先岛

原行：

- `place_id=P001`、`place_name=Okinawa Prefecture`；
- 旧说明是“Peace Winds Japan Okinawa link not confirmed”；
- 旧 evidence level E2、semantic `unclear`。

新证据已经使旧说明失效：

- PWJ FY2024 官方年报明确写其社区防灾联系网络扩展到 `the Sakishima Islands of Okinawa`；
- 来源没有把该联系分别落到 Yonaguni、Ishigaki 或 Miyako，不能机械复制为三个市町边；
- 现有 place registry 没有 Sakishima 集体节点，P001 又过宽，无法保存来源的实际空间尺度；
- 国民保护训练材料中的 `candidate_vessel_under_coordination` 是另一条 event/procedure 候选，不应塞进 AP049。

辅助建议：

1. `review_decision=revise_pending_source_and_place_integration`；
2. 新增地区节点候选：
   - `place_id=P021`；
   - `place_name=Sakishima Islands`；
   - `place_type=region`；
   - `region=Okinawa`；
   - 边界说明：“只用于来源明确指称先岛整体、但不能下沉到与那国／石垣／宫古的观察；不得向三个市町自动扇出”；
3. AP049 改为 X015→P021；
4. `place_semantic=site_presence`，精确写成“PWJ 自报 FY2024 将社区防灾联系网络扩展至先岛”；
5. 不编码 headquarters、分支、永久驻点或三个市町的分别在场；
6. 先把 PWJ 年报按 source proposal／metadata／archive 流程赋予主 source ID，再把 AP049 升为人审地点边；
7. `candidate_vessel_under_coordination` 另送 event/procedure 人审，不改变 AP049。

备选但不推荐：继续使用 P001 Okinawa Prefecture 并在 notes 中写 Sakishima。这样不会新增 place node，但会把来源的区域尺度压扁到全县，降低后续空间分析的可解释性。

来源：

- PWJ FY2024 年报：`https://en.peace-winds.org/wp-content/themes/pwj2024/assets/pdf/PWJ_AR2024en.pdf`
- 国民保护共同图上训练材料：`https://www.town.yonaguni.okinawa.jp/docs/2024081400014/file_contents/02_.pdf`

### 负责人决定

**确认辅助建议：AP049=`revise_pending_source_and_place_integration`；新增 P021 Sakishima Islands 地区节点，AP049 改为 X015→P021、`place_semantic=site_presence`。**

负责人理由／限制：来源只支持“先岛整体”的 FY2024 社区防灾联系网络扩展，不能下沉或扇出为与那国、石垣、宫古三条边，也不支持 headquarters、分支或永久驻点。PWJ 年报须先完成 source proposal／metadata／archive；医疗船 `candidate_vessel_under_coordination` 另进 event/procedure 人审。

## 5. 本批确认后的主线程动作

1. 在 HR-024 回填 A076 三条 accept、A086 两条 accept／一条 revise／一条 accept_with_revision，并保留所有 case-specific 限制。
2. 只激活上述七条 actor–issue case edge；不得改变 A076 registry 的持续性／法律形式状态，也不得生成 actor–actor alliance edge。
3. 在 HR-025 将 AP048 记为 reject／retire；X014 watchlist 记录保留。
4. 在 place registry 提议新增 `P021,Sakishima Islands,region,Okinawa`，并写入“不得自动向 P011/P012/P013 扇出”的层级限制。
5. 将 PWJ FY2024 年报和国民保护训练材料送入 source proposal／metadata／archive。年报赋主 source ID 后，把 AP049 改为 X015→P021 `site_presence`；训练材料只生成另行人审的 event/procedure candidate。
6. 合并后重新生成 R1/R2 edge、R03 空间 dossier、place-key validation、报告 claim audit 和最终 HR-029 输入。
7. A073 继续留在 online-exhausted／当地核实队列，本批不作 registry 决定。

本报告本身未修改中央 CSV、place registry、source log、archive manifest 或 HR 队列。
