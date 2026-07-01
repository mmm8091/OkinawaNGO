# MT-001 registry 审入 triage 说明 v0

日期：2026-07-01

**状态：AI 初筛提案，待人工确认后才实际写入 registry（遵守"不做 AI 写 AI 审"）。**

## 输入

- `coaction_participants_2020_mmc_71_full_v0.csv`：2020 OEJP/MMC 71 团体完整名单（来源 S006）。
- `actor_registry_extension_candidates_2020_mmc_v0.csv`：71 中未匹配现有 registry 的 52 个候选。
- `01_actor_registry_initial_v0.csv`：现有 93 条 actor（去重基准）。

52 个候选按抽取说明均与现有 93 条未匹配。本 triage 不新建关系边，只对"是否录入 registry"给分层建议。

## 分层逻辑

以抽取自带的 `origin_guess × actor_class_guess` 为骨架，加对个别在地组织的判断：

- **Tier A — 建议纳入（9 个，P2）**：冲绳本地、功能清晰（儒艮/珊瑚礁/海域/流域环境组，或边野古—名护现场 civic 组）。它们最可能在运动中重复出现、能加深 R2/R11/R5，优先录入。录入时 `evidence_level=E2`、`review_status=needs_second_source`、notes 标"2020 MMC 署名，signatory-only，别名/法律身份待核"。
- **Tier B — 暂缓（12 个，P3）**：两类。① 冲绳本地但身份/持续性/功能存疑（医护、纪念性、疑似福祉设施）；② 本土/奄美环境声援组织（含本土守护边野古·高江 NGO 网络）。等 R5/R11 需要"本土声援层"时再复评，其中 #36 守护边野古高江网络、#51/52/65/66 反边野古行动组相关度较高，可优先复评。
- **Tier C — 保持署名限定、不入 registry（31 个，P3）**：本土一次性声援署名的福祉/保育/宗教/农场/工会/政党地方组织，及场所类（民宿）、企业、单个国际团体。全加入会把 registry 灌成"本土远端一次性署名"，稀释冲绳 civic 网络焦点。这些只留在共同行动 participant 表里，作为"广泛声援"的证据，不作 actor。

## 计数

| Tier | 决策 | 数量 | 优先级 |
|---|---|---|---|
| A | add_as_signatory_candidate | 9 | P2 |
| B | defer | 12 | P3 |
| C | signatory_only_no_add | 31 | P3 |
| 合计 | | 52 | |

若人工确认 Tier A 全部录入，registry 将从 93 → 102 条（仍需继续向 120+ 推进）。

## 口径边界

- 这些组织只证明在 2020 request letter 中作为 undersigned 出现，**不得写成稳定联盟**。
- Tier A 录入后为 **E2 signatory-only**，别名/法律身份/持续性仍需二次来源或当地核实。
- 表中"疑为…（tentative）"的日文名/别名均为 AI 推断，**未经核实，人工确认前不得当作定名**。
- #14（冲绳中心）与 #46（东京本部）为同名机构的不同层级，需保持区分。

## 建议下一步

1. 人工过一遍 Tier A 9 条，确认身份与是否录入；确认后写入 registry 并补 actor_alias。
2. Tier A 录入后，把这 9 条接入 2020 MMC 共同行动 event（R5）与议题/地点边（作 E2 候选）。
3. Tier B 待 R5/R11"本土声援层"启动时复评。
4. Tier C 维持在 participant 表，不进 registry。
