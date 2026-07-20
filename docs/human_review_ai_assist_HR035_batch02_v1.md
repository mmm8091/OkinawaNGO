# HR-035 Batch 2 AI 辅助复核报告（负责人已确认）

日期：2026-07-20
状态：**项目负责人已于 2026-07-20 确认全部 23 项；正式回传见
`docs/human_review_return_HR035_batch02_v1.md`**

## 1. 本轮结果

- 身份配套：5 项全部形成建议，其中 `accept_identity` 1 项、`revise_identity` 4 项；
- actor–issue 事实：18 项全部形成建议，其中 `accept` 7 项、`revise` 9 项、
  `defer_second_source` 2 项；
- `reject` 0 项，`defer_local` 0 项；
- reviewer 已统一更新为 `project_principal_user`，`review_date=2026-07-20`；
- 本报告形成时只填写 Batch 2 两张复核表并修复 AI044 的来源引用；中央 actor registry、
  actor–issue 表、图数据和前端随后由主线程专用合并器受控更新。

## 2. 建议项目负责人优先确认的判断

### 2.1 四项身份法律形态修订

| actor | 建议 | 核心理由 |
|---|---|---|
| A007 ピースボート | `revise_identity` | S005 可确认独立 NGO 身份，但不证明精确法人形态；改为 `nonprofit_form_unresolved` |
| A018 ノーモア沖縄戦 命どぅ宝の会 | `revise_identity` | S023 可确认市民团体，但“市民グループ”不等于已证 `informal_association`；改为 `legal_form_unresolved_citizen_group` |
| A049 基地・軍隊を許さない行動する女たちの会 | `revise_identity` | S039 可确认组织身份，最高直接支持 E3；法律形态改为 `legal_form_unresolved_citizen_group` |
| A066 新外交イニシアティブ（ND） | `revise_identity` | S032 首页可确认 NGO／智库身份，但未列示特定非营利法人资格；改为 `nonprofit_form_unresolved` |

A017 沖縄対話プロジェクト建议直接 `accept_identity`：S022 的固定名称、共同代表、规约、
企划书、发足记录和活动日程足以将其作为独立市民网络识别，法律形态继续保持
`legal_form_unresolved`。

### 2.2 两项等待线上二源

| edge | 建议 | 当前证据能确认什么 | 仍缺什么 |
|---|---|---|---|
| AI157 ND—legal | `defer_second_source` | S032 确认政策倡议／外交智库与沖縄、基地研究主题 | ND 自有报告或提言中直接可定位的行政法、地方自治法或制度论证 |
| AI158 ND—local_autonomy | `defer_second_source` | S032 确认沖縄政策与“地域外交”研究 | 直接讨论国—地方权限、地方自治或冲绳地方政府权限的 ND 文本 |

这里没有把“政策研究”“地域外交”机械等同于 `legal` 或 `local_autonomy`。两项仍有在线
补证空间，因此不是 `defer_local`。

### 2.3 两项要求重开 HR-019 scope

| edge | 建议 | scope 修订 |
|---|---|---|
| AI016 ピースボート—international_advocacy | `revise` | S005 只能确认 2015 年一次共同声明参与；从 `organizational_positioning` 收窄为 `event_specific` |
| AI233 全港湾沖縄地方本部—anti_military | `revise` | S287/S288 直接闭合 2024 年军舰使用民用港争议；从一般组织定位收窄为 `event_specific` |

两项均填写 `scope_revision_required=yes`，没有静默覆盖 HR-019。

### 2.4 AI044 来源错位修复

AI044 原 edge 引用 S024，但 S024 是沖縄対話プロジェクト页面，不能承担 A018
ノーモア沖縄戦 命どぅ宝の会的组织立场。

建议改为：

- `source_ref=S023`；
- `decision=revise`；
- `evidence_level_final=E4`；
- 只确认 2021 年成立／2022 年发足语境中，该会反对“台湾有事”想定下南西诸岛成为
  攻击据点；
- 不确认成立期之后全部年份的连续活动。

逐来源包已增加 AI044—S023 的 edge-fact 对照，同时保留 S023 的身份对照；唯一来源数仍为
20，S051 仍为 0。

## 3. 23 项建议总表

### 3.1 身份配套

| item | 建议 | final E | 关键修订 |
|---|---|---:|---|
| ID-A007 | `revise_identity` | E4 | 法律形态改为 `nonprofit_form_unresolved` |
| ID-A017 | `accept_identity` | E4 | 当前字段接受 |
| ID-A018 | `revise_identity` | E4 | 法律形态改为 `legal_form_unresolved_citizen_group` |
| ID-A049 | `revise_identity` | E3 | 降至来源上限；法律形态未解决 |
| ID-A066 | `revise_identity` | E4 | 法律形态改为 `nonprofit_form_unresolved` |

### 3.2 actor–issue 事实

| edge | actor—issue | 建议 | final E | 核心边界 |
|---|---|---|---:|---|
| AI016 | A007—international_advocacy | `revise` | E4 | 仅 2015 共同声明事件；重开 scope |
| AI040 | A017—Taiwan_contingency | `accept` | E4 | 组织公开问题框架，不是风险／效果事实 |
| AI042 | A017—peace | `accept` | E4 | 对话与防战目的，不是和平政策效果 |
| AI044 | A018—Taiwan_contingency | `revise` | E4 | S024 改 S023；只确认成立期公开定位 |
| AI119 | A049—life_safety | `revise` | E3 | 限女性人权、身体安全与军事性暴力，不是一般治安 |
| AI121 | A049—anti_military | `revise` | E3 | 降至 S039 上限，不外推全部成员／行动 |
| AI157 | A066—legal | `defer_second_source` | E4 | 官网首页不闭合法律论证 |
| AI158 | A066—local_autonomy | `defer_second_source` | E4 | “地域外交”不自动等于地方自治 |
| AI159 | A066—anti_base | `revise` | E4 | 限边野古新基地等具体政策提言 |
| AI223 | A112—groundwater | `accept` | E4 | 研究／监测／行政倡议，不证明污染因果 |
| AI225 | A112—life_safety | `accept` | E4 | 饮用水源安全，不证明健康损害 |
| AI226 | A112—environment | `accept` | E4 | 环境研究／预防倡议，不证明生态因果 |
| AI232 | A114—anti_base | `revise` | E3 | 仅 2015、2025 有证行动，不写 2015–2026 连续 |
| AI233 | A114—anti_military | `revise` | E4 | 仅 2024 民用港军事利用事件；重开 scope |
| AI234 | A114—peace | `revise` | E3 | 仅 2015、2025 有证行动，删除 2024–2026 连续性 |
| AI236 | A114—mobilization | `revise` | E4 | 记录集会、罢工、行进 repertoire，不推断能力／效果 |
| AI237 | A115—women | `accept` | E4 | 女性会员与县本部结构；不转嫁母体行动 |
| AI240 | A115—anti_base | `accept` | E4 | 2014、2018 地方本部具名行动；不推断全国／全时期 |

## 4. 负责人确认记录

负责人已确认全部建议，并已运行：

```powershell
& '.\scripts\apply_hr035_batch02_ai_assist.ps1' -ConfirmPrincipal
```

该步骤已把 reviewer 改为 `project_principal_user`、写入 2026-07-20 日期并将 review
note 前缀改成“项目负责人确认 AI 辅助建议”。此确认步骤本身不自动改中央表；随后主线程
已通过 `scripts/merge_hr035_batch02_v1.py` 完成中央合并和下游重生。

## 5. 强制解释边界

- 身份接受不等于议题边接受；
- E4 是强可复核来源，不是自动接受；
- 共同声明、共同活动、同行进不生成稳定联盟；
- 分支行动不转嫁母体，全国组织声明也不自动转嫁地方分支；
- 风险主张不升级为污染、健康、冲突或政策效果事实；
- 本轮不新增组织关系、资金边、人物、地点、事件或因果结论。
