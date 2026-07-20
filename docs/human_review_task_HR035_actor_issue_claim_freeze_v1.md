# HR-035：actor–issue 事实与字段冻结

日期：2026-07-20  
当前派发：**Batch 1，共 15 条案件／公投／程序边**  
任务性质：事实边人工复核；不重做 HR-019 的解释范围决定

## 为什么新建这个任务

当前 238 条有效 actor–issue 边中：

- 65 条已被旧批次人工接受；
- 173 条仍为事实候选；
- 其中 59 条已经由 HR-019 决定了应按长期定位、案件角色还是事件标签解释，但这只审了
  “怎么解释”，没有审“现有来源是否足以确认这条 actor–issue 事实”。

HR-035 补的正是这层事实门禁。它不重开 30 个 bridge 决定、不改变 HR-019 已批 scope，
也不新增 actor、地点、事件、组织关系、资金关系或因果结论。

## 本批为什么选这 15 条

第一批只选案件、公投和制度程序边，原因是：

- 直接影响一期最重要的法律／公投／制度路径解释；
- 15 条的来源均已有中央编号和本地归档；
- 多数有明确的时间、案件或程序边界，适合先做出可审计的接受／修订／拒绝决定；
- 其中 AI106、AI164、AI178 暴露了来源错位、组织谱系和“争议对象≠政治立场”等高价值
  编码问题。

权威任务表：

`outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv`

逐来源辅助表：

`outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch01_v1.csv`

## 15 个复核对象

| edge | actor—issue | 已批解释范围 | 本轮注意点 |
|---|---|---|---|
| AI021 | Earthjustice—international_advocacy | 儒艮案法律渠道 | Earthjustice 是 counsel，不是 plaintiff |
| AI025 | 石垣市住民投票を求める会—referendum | 住民投票请求／程序 | requester 不等于诉讼 plaintiff |
| AI027 | 同上—anti_military | 石垣陆自部署公投 | 不外推一般反军事定位 |
| AI048 | JELF—legal | 逐案法律角色 | Dugong=plaintiff；泡瀬=supporter／host |
| AI049 | JELF—biodiversity | 2020 MMC 事件 | 不支持长期 biodiversity 定位 |
| AI050 | JELF—dugong | Dugong 案／MMC 事件分开 | 共同行动不等于稳定联盟 |
| AI106 | CBD—legal | 冲绳儒艮案原告角色 | 当前 S004 不足，须核 caption 并修 source_ref |
| AI126 | 「辺野古」県民投票の会—Henoko | 2018–2019 县民投票 | 临时组织／解散边界 |
| AI127 | 同上—local_autonomy | 直接请求／投票程序 | 不是无限期自治定位 |
| AI129 | 嘉手纳原告团—life_safety | 各轮噪音诉讼 | 认赔不等于运行停止 |
| AI132 | 普天间原告团—life_safety | 各轮噪音诉讼 | 部分赔偿不等于禁令 |
| AI164 | 名护市民投票推进组织—anti_base | 1997 公投程序 | actor 名称／谱系须保守 |
| AI178 | 沖縄防衛局—anti_base | 工程／行政争议端点 | 争议对象不等于反基地立场 |
| AI231 | 宜野湾ちゅら水会—legal | 请愿／公害调停程序 | 不是一般法律组织 |
| AI241 | 新婦人沖縄県本部—referendum | 2018–2019 签名动员 | 不转嫁全国本部行动 |

## 每条要回答什么

只回答一个事实问题：

> 现有来源是否足以确认这个确切 actor 与这个确切 issue 的关系，而且只能支持到 HR-019
> 已批准的时间／案件／事件范围？

允许决定：

- `accept`：原命题及范围成立；
- `revise`：事实成立，但 source、措辞、issue 或范围必须修订；
- `defer_second_source`：现有材料不足，线上仍需独立二源；
- `defer_local`：线上已尽，必须当地／馆藏／内部材料；
- `reject`：来源不能支持这条 actor–issue 映射，或该映射本身造成错误政治立场／角色。

状态映射：

- `accept` → `human_checked`
- `revise` → `human_revised`
- `defer_second_source` → `needs_second_source`
- `defer_local` → `needs_local_retrieval`
- `reject` → `rejected`，同时 `claim_status=unsupported`

如果选择 `supported_bounded`，必须同时填写：

- `confirmed_scope`
- `missing_scope`
- `interpretation_limit`

如果认为 HR-019 的既有 scope 也有问题，不要静默覆盖；填写
`scope_revision_required=yes` 并说明冲突，交主线程单独处理。

## 最省时的回交格式

可以直接在 CSV 填决定栏，也可以按下面格式回复主线程：

```text
HR035-B01-AI021
decision:
revised_review_status:
evidence_level_final:
approved_formulation:
reviewed_fields:
claim_status:
confirmed_scope:
missing_scope:
interpretation_limit:
scope_revision_required:
review_note:
```

`reviewed_fields` 至少应说明本次实际看过哪些字段；不要因为整行被看过就默认所有字段均已确认。

## 强制边界

- HR-019 的 scope 决定只读，不因本轮事实接受而扩大；
- 同案、共同请求、共同署名或同场行动不生成稳定联盟；
- 原告、律师、requester、supporter、proponent、target 严格分开；
- 行政机构成为争议对象，不等于该机构持反对立场；
- 接受 actor–issue 不批准组织—组织边、资金、影响力、胜诉或工程改变；
- 不使用已拒绝的 S051；
- 本批不处理 HR-010 batch 6、HR-024 A073、HR-025 地点、HR-029 alias 或 HR-031
  解释强度。

## 交回后的主线程动作

主线程合并决定后，依次重生 R1/R2、strict place–issue、coverage 和探索系统数据，并检查：

- 已核／研究层零泄漏；
- scope 未被静默覆盖；
- `supported_bounded` 字段完整；
- 前端计数从 manifest 自动更新；
- AI178 若被拒绝，不再把沖縄防衛局显示成具有 anti-base 立场。
