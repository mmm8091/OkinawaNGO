# Lions 冲绳受领侧最小线索包 v1

日期：2026-08-22

状态：`research_only / lead_only`。本包不改 W2-A 派生表、中央事实层、人工复核队列、publication adapter 或前端。

## 1. 问题与包内侦察观察

问题是：Lions Clubs International 337-D 地区沖縄リジョン自己的网页，能否从受领侧补强 Marine Thrift Shop Okinawa → Lions 的公开记录？

可以补强，但须分三层：

| 层 | 本包实际闭合 | 当前边界 |
|---|---|---|
| Lions 正文 | 该组织自称“从美军基地的商店收到用于小儿癌症支援的义援金” | 可作 `recipient_side_generic_receipt` 与 `purpose_childhood_cancer_support`；正文没有日期、金额或最终受赠机构 |
| 图片交叉核对 | Lions 页面嵌图与 DVIDS Photo ID 8251055 为高度近似的同一场景图：尺寸分别为 886×560 与 1000×667；统一算法 pHash 距离为 4/64 | 只形成 `visual_crosswalk_candidate`；不在本包自动通过 exact transaction match |
| 具体交易与下游 | DVIDS 图页把 Photo ID 8251055 写为 2024-02-22、Marine Thrift Shop、USD 10,000、Lions Okinawa，并称将转给 Cancer Children's Parents Association | Lions 地方页本身仍未独立写出 USD 10,000，也未给最终机构正式名称、金额或受赠原件；资金链继续停在 MTS→Lions |

即便以后人工接受“Lions 嵌图与 DVIDS 8251055 指向同一场活动”，也只能闭合事件身份；不能把 Lions 页面说成对 USD 10,000 数额和下游端点的独立确认。

## 2. 可复核入口

- Lions 自有活动页：`artifacts/lions_okinawa_activity.html`，正文 identity 与活动描述见本地第 104、114、122 行。
- Lions 页面原嵌图：`artifacts/lions_okinawa_military_shop_child_cancer_image.png`。
- DVIDS Photo ID 8251055 图页：`artifacts/dvids_8251055_image_page.html`，日期与说明见本地第 625、728、740、747—748 行。
- DVIDS Photo ID 8251055 图像：`artifacts/dvids_8251055_group_photo.jpg`。
- 已冻结的行动方新闻原件继续复用 `outputs/us_presence_network_wave2_w2_a_v1/artifacts/tracer/dvids_mts_lions_20240222.html`（W2A2-SR018），本包没有改写它。
- URL、观察时间、SHA-256 和 locator 见 `lead_only_source_receipts_v1.csv`。
- 两图尺寸、pHash 与算法见 `visual_crosswalk_lead_only_v1.csv`；运行 `python reproduce_visual_crosswalk_v1.py` 可复算。

## 3. 文件

| 文件 | 用途 |
|---|---|
| `lead_only_observations_v1.csv` | 三层证据与边界 |
| `lead_only_source_receipts_v1.csv` | 来源、归档路径、哈希和 locator |
| `visual_crosswalk_lead_only_v1.csv` | 图片交叉核对结果 |
| `reproduce_visual_crosswalk_v1.py` | 复算尺寸、pHash 与汉明距离 |
| `unexpected_findings_register_v1.csv` | 3 条有限侦察链，全部 `lead_only` |
| `artifacts/` | Lions 与 DVIDS 页面／图片的本地冻结副本 |

## 4. 停手点

线上公开材料已经足以提出同一事件的图片交叉核对候选，但没有 Lions 的收据、入账簿、汇款记录或最终受赠方回执。继续追查属于 `docs/local_retrieval_tasks_v1.md` 的 T2-I／USN-MTS-LCI-001，不在本包向下建边。

## 意外发现登记

本包登记 3 条观察，形成 `正文 → 嵌图 → DVIDS 图页` 两步跟进链。所有记录均固定为 `lead_only / claim_eligibility=no / central_writeback=no / human_review_trigger=no / publication_eligibility=no`。它们不进入本轮结论，只提供可复核的后续取证线索。

## 5. 验证

```powershell
python outputs\us_presence_network_wave2_lions_recipient_lead_v1\reproduce_visual_crosswalk_v1.py
python scripts\validate_research_work_package_v1.py outputs\us_presence_network_wave2_lions_recipient_lead_v1
```
