# R7 场域与对象转移

## 结论

可做，价值高。这个模块能解释冲绳民间组织如何把地方议题带到县政、日本中央政府、法院、美国机构和国际 NGO 场域。它比单纯列组织更有研究味道，因为它展示的是“行动路径”。

## 已主动探查的资料

1. Earthjustice 的 Okinawa dugong litigation 资料显示，边野古 / 儒艮议题进入美国法院和美国法律程序。
   - https://earthjustice.org/case/okinawa-dugong-proposed-airbase

2. OEJP 2020 年向美国 Marine Mammal Commission 提交资料，显示地方生态 / 基地争议进入美国联邦机构场域。
   - https://okinawaejp.blogspot.com/2020/07/

3. 2010 / 2015 边野古环保联署资料显示，地方基地争议进入日本国内环保 NGO 和国际署名网络。

4. 与那国、石垣、宫古本地运动中出现住民投票、行政要请、诉讼意向和公开声明，可作为地方自治 / 行政程序路径。

## 可抽取路径

- local protest -> municipal government
- local protest -> Okinawa prefectural government
- local protest -> Japanese central government
- local protest -> court
- local protest -> U.S. institution
- local protest -> international NGO / UN
- local protest -> media / public opinion

## 推荐字段

- action_id
- action_date
- actor_id
- actor_name
- place_tags
- issue_tags
- action_type
- target_type
- target_name
- arena: local / prefectural / national / legal / U.S. institution / international / media
- source_id
- evidence_note
- confidence

## 可交付物

- `action_target_edges.csv`
- 场域转移流程图
- “地方议题国际化路径”短文
- 边野古 / 儒艮案例图
- 石垣 / 宫古 / 与那国地方行政路径对照表

## 难点

不同场域的资料格式差异大。法院资料、美国机构资料、国际 NGO 资料、地方新闻和组织官网不能简单合并，需要统一 action_type 和 target_type。

另一个难点是目标对象可能多重。例如一封请求信可能同时指向日本政府、美国机构、国际舆论和地方公众，需要允许一项行动有多个 target。

## 判断

一期可做样本型场域转移。边野古 / 儒艮是最强案例；石垣 / 宫古 / 与那国可作为地方行政、住民投票和前线化路径补充。
