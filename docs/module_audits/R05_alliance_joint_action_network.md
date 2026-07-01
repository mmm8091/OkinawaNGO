# R5 联盟 / 共同行动网络

## 结论

可做，价值高，但一期应做小样本网络，不做全量联盟网络。该模块适合回答“冲绳 NGO 如何连接起来”的问题，也适合展示边野古 / 大浦湾议题如何从地方运动扩展到日本国内和国际倡议网络。

## 已主动探查的资料

1. 2010 年 WWF Japan 页面记录 67 个国内团体和 550 多个全球团体围绕边野古 / 儒艮发表共同声明。
   - https://www.wwf.or.jp/activities/statement/3436.html

2. 2015 年日本自然保护协会页面记录 31 个 NGO 围绕边野古和大浦湾发表紧急共同声明。
   - https://www.nacsj.or.jp/statement/50827/

3. 2015 年 Peace Boat 页面提供和平 / 环保 / 反基地联盟材料，可用于识别和平运动和环保运动的桥接。
   - https://peaceboat.org/3620.html

4. 2020 年 OEJP 牵头 71 个团体向美国 Marine Mammal Commission 提交请求。
   - https://okinawaejp.blogspot.com/2020/07/

5. 2025 年高市“台湾有事”答辩后，16 个冲绳市民团体联合抗议，可作为近期反前线化联盟样本。
   - https://ryukyushimpo.jp/news/national/entry-4802441.html

## 能抽取的数据关系

- actor co-signs statement with actor
- actor participates in request / petition
- actor co-hosts event
- actor supports lawsuit or referendum
- actor targets institution
- actor bridges local group and national / international NGO

## 推荐字段

- event_id
- event_name
- event_date
- source_id
- actor_id
- actor_name
- actor_role: organizer / co-signer / plaintiff / attorney / supporter / target
- issue_tags
- place_tags
- target_institution
- relation_strength
- confidence

## 可交付物

- `coalition_events.csv`
- `coalition_edges.csv`
- 共同行动网络图
- 联署团体类型统计
- 跨国节点清单
- “稳定联盟 vs 一次性署名”说明

## 难点

共同声明网络容易把“一次性联署”误读为稳定联盟。必须区分：

- stable organization
- temporary committee
- signatory only
- organizing group
- supporting group
- repeated collaborator

另一个难点是共同声明中外部团体很多，如果全部纳入，网络图会过密。建议一期只纳入核心组织、重复出现组织和明确与冲绳议题有关的外部团体。

## 判断

一期做 3-5 个联盟事件样本即可。最适合的样本是 2010 WWF 共同声明、2015 NACSJ / Peace Boat 声明、2020 OEJP / MMC 请求、2019 县民投票相关行动、2025 反前线化抗议。完整联盟网络应留到扩展阶段。
