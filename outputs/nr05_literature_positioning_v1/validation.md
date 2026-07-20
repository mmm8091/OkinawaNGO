# NR-05 文献定位包验证

验证日期：2026-07-20
包状态：`research_only`

## 文件与范围

- `brief_v1.md`：存在。
- `source_crosswalk.csv`：存在，共 14 条定位记录（13 条外部文献／制度来源，1 条内部有界审计信号）。
- 本包没有修改 NR-05 任务书、中央表、前端、控制文档或既有研究输出。
- `central_writeback=no`、`frontend_eligibility=not_frontend_ready` 已逐行写入 crosswalk。

## 来源核验层级

- 已读全文／官方 PDF：鈴木（1998）、安里・池田（2001）、JICA（2000）、JICA（2003）、Taylor（2006）、沖縄21世紀ビジョン付属資料。
- 已核官方制度或组织页面：内阁府 NPO 制度页、e-Gov、沖縄県法人名册、沖縄NGOセンター沿革。
- 只核出版社摘要：Spencer（2003）、Inoue（2004）；brief 明确禁止扩写全文级事实。
- 只核出版说明页：2012《沖縄県NPO白書》；不使用正文结论。
- 只作 catalog locator：桐山（2023）；不作为本轮实质证据。
- 只作馆藏／公文书 locator：1997–1998 环境伙伴关系报告；不使用目录外推内容。

## 强制字段检查

`source_crosswalk.csv` 每行均包含：

- `prior_claim`
- `our_possible_increment`
- `forbidden_novelty_claim`
- `evidence_limit`

每行也均设置：

- `research_status=research_only`
- `frontend_eligibility=not_frontend_ready`
- `central_writeback=no`

## 解释边界检查

- 未用全县 NPO 法人数量推导基地 actor 的法人化。
- 未用当前目的性 registry 的 legal status 分布推导总体比例。
- 明确把 51 个目的性 actor 中 1 个显式 NPO 法人编码限制为审计信号；未将 `1/51` 写成比例发现。
- “专业能力经律师／外部法人 NGO／程序接口取得”仅作为待验证机制，未写成已证事实。
- 未把 NPO 法实施写成专业化、长寿化或影响力提升的原因。
- 未把网页留存写成活动强度或网络影响力。
- 未把环保／女性／人权进入反基地运动写成本项目首次发现。
- 未把环境、国际合作与基地问责载体写成已经证实的两个互斥世界。
- catalog 仅作 locator。

## 红队判定

**PASS（作为文献定位与研究设计约束包）。**

本包不证明“制度化与案件型载体二分”成立；它证明该命题必须改写为带匹配组、分母、日期语义和材料留存控制的组织级检验。
