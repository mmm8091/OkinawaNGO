# Translation negative cases v1 — validation

验证日期：2026-07-20

## 结果

**PASS**

- PASS baseline input remains 13 episodes
- PASS five candidate negative cases
- PASS unique case IDs
- PASS five distinct gate families
- PASS case fields and research-only state contract
- PASS per-case multi-source and official-source gates
- PASS duplicate/misattribution exclusion guards
- PASS 2004 defense-facility mediation retained as non-actor contextual precedent
- PASS TN03 current judgment locator and legacy-URL boundary
- PASS TN03 current Fukuoka preservation-directory cross-check
- PASS TN04 later-Q&A linkage and original-submission relief remain unconfirmed
- PASS bounded nonresponse wording
- PASS comparison table contains baseline plus five cases
- PASS five blank human-review decisions

## 计数

- 原13案输入：13。
- 候选负例：5。
- 纳入来源：21。
- 方法／排除记录：5。
- 人审队列：5，决定栏全部空白。
- 每案来源数：TN01=4；TN02=4；TN03=4；TN04=5；TN05=4。

## 状态边界

- 全部候选为 `research_only / candidate / ai_seeded / not_frontend_ready`。
- 全部 `central_writeback=no`；本地 `TNS*` 不是中央 `S*`。
- 没有把石垣既有R9阶段重复算作新案例。
- 没有把大阪安保差止判决误配给冲绳国家赔偿案。
- 2004年基地公害调停只作TN02的制度背景，不把913名个人申请人组织化或另算案例。
- TN03 法院原文已迁至现行 `assets` 地址；旧 `app/files` 地址仅作失效 locator 备注。
- TN03 另由福冈高裁现行保存目录第13项交叉锁定案号、案名与终局日。
- 只有 TN01、TN03 具官方个案处分／判决原文；TN02 的却下结果、TN04 的拒绝形式、TN05 的确认函仍是官方程序材料与报道／公开通信组合而成的混合证据链，不因“每案有官方来源”而升级。
- TN04 后续官方问答材料与原10项質問状的逐项、程序或因果对应未闭合；不得编码为原提出者获得部分救济。
- 没有把检索未找到回应写成现实无回应。

复验命令：

```powershell
python scripts\make_translation_negative_cases_v1.py --check
```
