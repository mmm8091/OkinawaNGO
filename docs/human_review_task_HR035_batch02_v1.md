# HR-035 Batch 2：E4 actor–issue 事实与组织身份配套复核

日期：2026-07-20
状态：**正式派发，等待项目负责人填写**

## 本批规模

- 18 条 actor–issue 事实决定；
- 5 条 actor identity 配套决定；
- 合计 **23 项人工决定**。

18 条边是当前有效层中满足以下条件的完整集合，不是为了让前端看起来更满而抽样：

1. `evidence_level=E4`；
2. actor–issue 事实仍为 `ai_seeded`；
3. HR-019 已完成人工 scope 复核；
4. 当前仍在有效研究层。

其中 A007、A017、A018、A049、A066 的组织身份仍为 `ai_seeded`，所以各增加一条配套身份
判断。身份只审一次，不在每条议题边上重复作决定。

## 权威填写文件

1. 议题事实表：
   `outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch02_v1.csv`
2. 组织身份配套表：
   `outputs/actor_issue_claim_freeze_v1/HR035_actor_identity_companion_batch02_v1.csv`
3. 逐来源辅助表：
   `outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch02_v1.csv`
4. 自动验证：
   `outputs/actor_issue_claim_freeze_v1/validation_report_batch02_v1.md`

所有决定栏均为空。逐来源表中的20个中央来源均有本地归档；S051 不在本批。

## 第一部分 · 18 条 actor–issue 事实

| edge | actor | issue | 身份配套 |
|---|---|---|---|
| AI016 | ピースボート | international_advocacy | A007需配套判断 |
| AI040 | 沖縄対話プロジェクト | Taiwan_contingency | A017需配套判断 |
| AI042 | 沖縄対話プロジェクト | peace | A017需配套判断 |
| AI044 | ノーモア沖縄戦 命どぅ宝の会 | Taiwan_contingency | A018需配套判断 |
| AI119 | 基地・軍隊を許さない行動する女たちの会 | life_safety | A049需配套判断 |
| AI121 | 基地・軍隊を許さない行動する女たちの会 | anti_military | A049需配套判断 |
| AI157 | 新外交イニシアティブ（ND） | legal | A066需配套判断 |
| AI158 | 新外交イニシアティブ（ND） | local_autonomy | A066需配套判断 |
| AI159 | 新外交イニシアティブ（ND） | anti_base | A066需配套判断 |
| AI223 | 宮古島地下水研究会 | groundwater | 已人审身份 |
| AI225 | 宮古島地下水研究会 | life_safety | 已人审身份 |
| AI226 | 宮古島地下水研究会 | environment | 已人审身份 |
| AI232 | 全日本港湾労働組合沖縄地方本部 | anti_base | 已人审身份 |
| AI233 | 全日本港湾労働組合沖縄地方本部 | anti_military | 已人审身份 |
| AI234 | 全日本港湾労働組合沖縄地方本部 | peace | 已人审身份 |
| AI236 | 全日本港湾労働組合沖縄地方本部 | mobilization | 已人审身份 |
| AI237 | 新日本婦人の会沖縄県本部 | women | 已人审身份 |
| AI240 | 新日本婦人の会沖縄県本部 | anti_base | 已人审身份 |

每条只回答：

> 现有归档来源是否足以确认这个确切 actor 与这个确切 issue 的关系，而且只能支持到
> HR-019 已批准的组织定位／时间／案件／事件范围？

允许决定：

- `accept`
- `revise`
- `defer_second_source`
- `defer_local`
- `reject`

状态映射：

- `accept` → `human_checked`
- `revise` → `human_revised`
- `defer_second_source` → `needs_second_source`
- `defer_local` → `needs_local_retrieval`
- `reject` → `rejected`，同时 `claim_status=unsupported`

如果选择 `supported_bounded`，必须填写：

- `confirmed_scope`
- `missing_scope`
- `interpretation_limit`

如果认为既有 HR-019 scope 本身也有问题，填写 `scope_revision_required=yes`，不得静默扩大。

## 第二部分 · 5 条组织身份配套决定

| item | actor | 关联边 |
|---|---|---|
| HR035-B02-ID-A007 | ピースボート | AI016 |
| HR035-B02-ID-A017 | 沖縄対話プロジェクト | AI040、AI042 |
| HR035-B02-ID-A018 | ノーモア沖縄戦 命どぅ宝の会 | AI044 |
| HR035-B02-ID-A049 | 基地・軍隊を許さない行動する女たちの会 | AI119、AI121 |
| HR035-B02-ID-A066 | 新外交イニシアティブ（ND） | AI157、AI158、AI159 |

每条只回答：

> 现有归档来源是否足以确认它是可独立识别的组织 actor，并足以确认当前 canonical name、
> actor class、origin type、legal status 与证据等级？

允许决定：

- `accept_identity`
- `revise_identity`
- `defer_second_source`
- `defer_local`
- `reject_identity`

若身份决定为 defer／reject，对应议题边即使事实本身接受，也不得自动进入默认已核图。

## 推荐阅读顺序

1. 先读5条 identity companion；
2. 再按 actor 成组判断18条边；
3. 同一组织的多条 issue 必须分别判断，不能因一条成立而批量接受其余标签；
4. 最后检查 `approved_formulation` 与 `interpretation_limit` 是否逐条有界。

## 最简回交格式

可以直接填写两个CSV，也可以按以下格式回交：

```text
HR035-B02-ID-A007
decision:
revised_review_status:
evidence_level_final:
canonical_name_final:
actor_class_final:
origin_type_final:
legal_status_final:
approved_identity_formulation:
reviewed_fields:
identity_interpretation_limit:
review_note:

HR035-B02-AI016
decision:
revised_review_status:
evidence_level_final:
approved_formulation:
review_scope_final:
reviewed_fields:
claim_status:
confirmed_scope:
missing_scope:
interpretation_limit:
scope_revision_required:
review_note:
```

## 强制边界

- 本批不重做 HR-019 scope，只审事实是否足够；
- E4 是“可复核材料较强”，不是自动接受；
- 一次声明、共同文件、同场行动或共同署名不生成稳定联盟；
- 组织定位不能从单一事件无限扩展到全部时期；
- `Taiwan_contingency`、`anti_military`、`anti_base` 等敏感标签必须写明组织自己的公开表达；
- 劳组地方本部与全国本部、地方分支与母体组织不得互相转嫁行动；
- 身份接受与议题边接受是两个决定；
- 本批不新增组织关系、资金边、人物节点、地点边、事件边或因果结论。

## 主线程合并条件

只有23项均有明确决定、reviewer、date 和实际 reviewed fields 后，主线程才生成 Batch 2
回交报告并受控合并。合并后再重生 R1/R2、strict place–issue、coverage 和探索系统；
不得为让前端两层接近而跳过 identity gate。
