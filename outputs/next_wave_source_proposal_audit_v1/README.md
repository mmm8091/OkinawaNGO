# Next-wave source proposal audit v1

日期：2026-07-13

本包合并审计 NW2-B（R9 election–civic interface）与 NW2-C（registry value gate）的来源提案。它不是中央 source-log merge，也没有下载、归档或批准任何事实关系。

## 核心结果

- 输入：50 条（R9 21；registry gate 29）。
- URL 规范化后：49 个唯一 URL；两批之间有 1 个重复 URL。
- 相对于历史 S001–S247 基线，既有 URL 为 2 个，即 S158、S204；都已有 archived artifact。
- 历史审计判为新候选：47 个唯一 URL；原建议顺序固定为 S248–S294。
- 当前观察到中央 source log 295 条；其中识别出 47 个 NW2-H provisional batch match。即使已合并，历史 `proposal_only_not_reserved` 字段仍只描述合并前审计，不表示 metadata 已获认可。
- provisional source indexing 是机器／来源层状态，不需要人工 claim approval；这不等于任何 claim 获批。49/49 URL 与 50/50 proposal 仍保持 `relation_or_claim_approved=no`。
- 元数据例外：11 个唯一 URL 进入人工队列；没有 title/publisher/URL/type/date/locator/support/caveat 的空字段。
- Web／归档前复核：11 个唯一 URL，原因包括动态页面、付费墙边界、滚动页面、未定年附件或既有域名归档风险。
- 49/49 唯一 URL 均保持 `relation_or_claim_approved=no`；caveat 与敏感边界标签均非空。

## 唯一重复与既有来源

- 跨批重复：R9EC_S007 与 RV2SP015 指向同一新日本婦人の会 2014-11-19 声明；只建议一个来源行，两个模块引用并存。
- S158：宮古島地下水研究会 `about_us.html`；复用现有来源，不新增。
- S204：宮古島地下水研究会主页；复用现有来源，不新增。

## 文件

- `unique_url_crosswalk_v1.csv`：49 个唯一 URL 的总审计；与 `data/interim/37_next_wave_source_proposal_crosswalk_v1.csv` 字节一致。
- `proposal_record_audit_v1.csv`：保留全部 50 条输入提案及其去重归属。
- `suggested_new_source_sequence_v1.csv`：47 条建议编号顺序；编号未预留。
- `source_type_crosswalk_v1.csv`：输入类型到当前中央词汇的建议映射；三类保留人工选择。
- `metadata_review_queue_v1.csv`：规范化元数据例外。
- `web_archive_review_queue_v1.csv`：打开／归档前需确认的 URL。
- `sensitive_claim_boundary_audit_v1.csv`：49 条敏感解释边界；全部不批准 claim/relation。
- `validation_report_v1.md`：机械校验与中央只读证明。

## 强制边界

- S248–S294 的原建议顺序已由 NW2-H 受控 provisional merge 采用；`snapshot_state=postmerge_provisional_batch_match` 明示当前状态。
- source inclusion 不批准 actor 入表、alias、edge、联盟、资金、污染或健康因果、罢工合法性、选举效果或临时动员体的持续性。
- NW2-H 的 provisional source-log merge 不等于 metadata 已审；11 个 metadata 问题仍须 HR-030。archive failed 不撤销 provisional S 号，但该来源不得用于正式关系结论。
