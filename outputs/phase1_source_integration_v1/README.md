# Phase-1 cross-module source merge proposal v1

本包是来源主表合并建议，不是合并结果。脚本不修改 `05_source_log_initial_v0.csv`，也不下载或归档任何 URL。

## 输入与覆盖

- R4 QA-safe sources：19 条。
- R9 `accepted` / `usable_with_limit`：30 条；2 条 rejected 未纳入。
- R10 `module_candidate_not_in_main_log`：8 条。
- 模块记录合计：57 条；规范化 URL 后：54 条唯一候选。

## 合并状态

- `current_main_match`：15 条，复用已有 S 编号。
- `cross_module_duplicate` 主状态：0 条；独立重复标记共 3 条。当前重复 URL 若已在主表，主状态仍优先记为 `current_main_match`。
- `proposed_new`：39 条。
- 待新增唯一 URL：39 条，按规范化 URL 排序后从 S160 连续编号。

## 跨模块重复 URL

- `SMC008` · R9:R9S014;R4:R4S011 · main=S138 · proposed=none
- `SMC025` · R9:R9S015;R4:R4S010 · main=S137 · proposed=none
- `SMC048` · R9:R9S032;R4:R4S017 · main=S010 · proposed=none

## 待新增编号

- `S160` · `proposed_new` · 令和5年行コ第6号判決 · R9
- `S161` · `proposed_new` · 石垣市住民投票を求める裁判 CALL4案件页 · R9
- `S162` · `proposed_new` · 国民保护计划改正要请决议 · R4
- `S163` · `proposed_new` · 令和3年第5回石垣市議会定例会議事日程 · R9
- `S164` · `proposed_new` · 石垣市自治基本条例 これまでの見直し・改正 · R9
- `S165` · `proposed_new` · 石垣市避難実施要領概要 · R4
- `S166` · `proposed_new` · 令和元年第1回石垣市議会臨時会提出議案と議決結果 · R9
- `S167` · `proposed_new` · 令和元年第4回石垣市議会定例会提出議案と議決結果 · R9
- `S168` · `proposed_new` · 宮古島市新市施策：水源保护条例 · R4
- `S169` · `proposed_new` · 宮古島市国民保護計画 · R4
- `S170` · `proposed_new` · 国民保護共同訓練住民意見と回答 · R4
- `S171` · `proposed_new` · その他の選挙（県民投票・市民投票） · R9
- `S172` · `proposed_new` · 1997年12月21日名護市民投票結果 · R9
- `S173` · `proposed_new` · 冲绳市 FY2019 交付金事业检证表 · R10
- `S174` · `proposed_new` · 冲绳市 FY2020 交付金事业检证表 · R10
- `S175` · `proposed_new` · 冲绳市 FY2024 交付金事业检证表 · R10
- `S176` · `proposed_new` · Koza International Plaza 设施页 · R10
- `S177` · `proposed_new` · 福岡高等裁判所特別保存事件一覧 · R9
- `S178` · `proposed_new` · 那覇地方裁判所特別保存事件一覧 · R9
- `S179` · `proposed_new` · 辺野古県民投票の民意とこれから・元山仁士郎講座記録 · R9
- `S180` · `proposed_new` · 与那国町住民避难联合训练 · R4
- `S181` · `proposed_new` · ONC 的活动 · R10
- `S182` · `proposed_new` · 石垣市住民投票を求める会が解散 · R9
- `S183` · `proposed_new` · 冲绳县 FY2024 NPO 协作调查结果汇总 · R10
- `S184` · `proposed_new` · 冲绳县 FY2024 第一季度随意合同实绩（知事公室） · R10
- `S185` · `proposed_new` · 沖縄県議会軍特委員会記録 県民投票条例請求代表者参考人 · R9
- `S186` · `proposed_new` · FY2024 第3回多文化共生万国津梁会议纪要 · R10
- `S187` · `proposed_new` · 辺野古新基地建設問題の経緯 · R9
- `S188` · `proposed_new` · 沖縄県公報号外第43号・県民投票条例第62号 · R9
- `S189` · `proposed_new` · 沖縄県公報号外第17号 条例制定請求代表者証明書 · R9
- `S190` · `proposed_new` · 沖縄県公報号外第2号・県民投票条例一部改正 · R9
- `S191` · `proposed_new` · 平成30年第6回沖縄県議会臨時会 提案説明 · R9
- `S192` · `proposed_new` · 沖縄の米軍基地・基地問題の沿革（1997年部分） · R9
- `S193` · `proposed_new` · 沖縄県国民保護共同図上訓練结果 · R4
- `S194` · `proposed_new` · 石垣住民投票訴訟 最高裁で敗訴確定 · R9
- `S195` · `proposed_new` · 平成27年度 与那国町施政方針 · R9
- `S196` · `proposed_new` · 与那国町国民保護計画 · R4
- `S197` · `proposed_new` · 沖縄県議会会議録・県民投票条例直接請求 · R9
- `S198` · `proposed_new` · 石垣自卫队配备环境质询 · R4

## 归档与人工复核边界

- 所有待新增来源必须先归档，再由人工确认 title、type、year/period、evidence level 与支持范围；本包不授权直接写入主表。
- R9 `usable_with_limit` 必须把原 interpretation limit 原样带入，不能因来源进入主表而升级结论。
- R10 的 type/year/evidence 是 proposal 层推定，必须在人审和归档后才能落主表。
- 已在主表但归档 manifest 仍失败或缺失、建议重试/检查：1 条。
- `human_review_required=yes`：49 条；逐行原因见 CSV 的 `human_review_prerequisite`。
- `current_main_match` 只表示 URL 或声明的 existing ID 已对应主表，不代表该来源支持模块的全部解释。

### 主表已有但需重试／检查归档

- `SMC025` · main=S137 · manifest=failed

## 元数据或 URL 冲突

- `SMC008`：source_type=local_news/official_legislative_record;year=2019/2020
- `SMC025`：declared_existing_id_url_mismatch=S137
- `SMC048`：evidence=E3/E2

## URL 规范化口径

scheme/host 小写；移除 fragment、默认端口、尾斜杠和常见 tracking query；保留并排序其余 query。该口径保守，不合并不同 path 的主页与子页。

## 复现与验证

运行 `python scripts/make_phase1_source_merge_proposal.py`。脚本验证 57 条可用模块记录全部覆盖、rejected 不进入、每个规范化 URL 仅一行、待新增 URL 不重复、S160 起编号稳定。
为保留合并前审计基线，脚本会识别 notes 中带 `Phase-1 module source integration` 的本包既有落表行，并在 proposal 比对时排除这些行；不会排除其他主来源。
