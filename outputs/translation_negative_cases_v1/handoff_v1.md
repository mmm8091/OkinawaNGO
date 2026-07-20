# Translation negative cases v1 — handoff

## 完成

- 5个统一结构的 `research_only` 候选对照，覆盖议会入口、行政对象适格、司法权利门槛、
  行政回应方式与跨国请愿回应追踪。
- 21条纳入来源；每案至少2源，并至少有1条官方／一手程序材料。
- 5条方法／背景／排除记录：石垣只作为既有TE05的负向阶段；县政府PFAS立入申请因主体不是NGO
  排除；县议会陳情库仅保留为未来搜索底盘；大阪安保判决明确排除，未误写为冲绳案；
  2004年基地公害调停仅作长期制度门槛背景，不把913名个人申请人组织化。
- 5项空白负责人判断候选，未做AI自审，也未写入正式HR总账。
- 生成与验证命令均通过。

## 没有改

- 中央 actor、issue、place、event、relation、source log 与 source archive；
- `outputs/translation_episode_comparison_v1/`；
- 前端、控制文档与工作台。

## 关键判断

- TN01 是“受理并审议后不採択”，不是未受理。
- TN02 是适用对象／资格阻断，不是PFAS实体败诉；原申请与决定书仍需补。
- TN03 只编码冲绳国家赔偿案；法院原文使用现行 `assets` 地址，
  福冈高裁现行保存目录第13项交叉锁定案号／案名／终局日；不借用大阪差止却下。
- TN04 只编码居民转述的书面形式被拒；后续公开问答存在，但与原質問状的程序对应未闭合，
  不能称完全无回应，也不能称原提出者获得部分救济。
- TN05 只称本轮未找到议题专属更新；不能称现实中没有正式回应。

## 建议下一步

负责人在检查点决定是否把 `human_review_queue_v1.csv` 转为正式HR任务。若其后接受至少3个跨门槛负例，再由新session
建立与原13案的案例匹配（相近议题、相近时间、不同gate outcome）；不要先合并为“成功／失败”
二元变量。

复现：

```powershell
python scripts\make_translation_negative_cases_v1.py
python scripts\make_translation_negative_cases_v1.py --check
```

生成日期：2026-07-20。
