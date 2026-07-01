# R12 人物—组织互锁与关键经纪人

## 结论

这个模块可以做“公开人物角色线索表”，但不适合一期承诺完整人物网络。它很有价值，因为很多冲绳市民运动不是只靠组织名称运转，而是由少数跨议题、跨地点、跨制度场域的人物把组织、媒体、法律程序、选举、公投和国际倡议串起来。

一期的安全做法是只记录公开资料中已经出现的身份、角色和发言，不推断私人关系、幕后关系或未公开协作。

## 已主动探查的资料

1. Yoshikawa Hideki / Okinawa Environmental Justice Project：APJJF 文章署名显示 Yoshikawa Hideki 与 OEJP 深度参与儒艮保护、Marine Mammal Commission 沟通和边野古议题国际化。
   - https://apjjf.org/2020/16/yoshikawaoejp

2. Earthjustice dugong case：案件材料显示 Earthjustice 与 JELF、Save the Dugong Foundation、个人原告等共同推进美国法院路径。这类材料可以用于识别“法律 / 国际倡议经纪人”，但人物角色需要谨慎，只能按公开文件记录。
   - https://earthjustice.org/case/okinawa-dugong-proposed-airbase

3. ヘリ基地反対協議会官网：该组织说明其由 1997 年名护市民投票相关组织发展而来，1998 年结成，现在有 12 个加盟团体。官网还说明其围绕边野古海上行动、帐篷村、安和、gate 前行动、学习会等活动展开，这为识别组织层面的经纪关系提供入口。
   - https://lovehenoko.org/わたしたちの立場/

4. 安次富浩相关公开资料：地方媒体和运动资料中经常出现其作为ヘリ基地反対協议会共同代表 / 顾问的角色，适合作为边野古现场运动的公开人物节点，但不宜扩展为私人网络判断。
   - https://www.qab.co.jp/news/tag/ヘリ基地反対協議会

5. 元山仁士郎相关公开资料：多篇资料显示其作为“辺野古”県民投票の会代表 / 元代表，是把边野古议题转化为县民投票、直接请求和民主程序议题的重要节点。
   - https://webronza.asahi.com/journalism/articles/2019061700008.html
   - https://www.min-iren.gr.jp/news-press/shinbun/20190122_36904.html

6. 石垣、宫古、与那国：这些离岛议题中可看到共同代表、住民投票团体代表、反自卫队部署团体发言人等公开角色，但资料更分散，必须按地点逐个补。

## 能抽取的数据关系

- person_to_actor：某人公开担任某组织代表、共同代表、顾问、发言人、原告、律师、研究者、署名人。
- person_to_event：某人参与某次记者会、声明、诉讼、县民投票、住民投票、国际倡议、学习会。
- person_to_issue：某人反复连接哪些议题，例如边野古、儒艮、环境影响评价、县民投票、反导弹部署、生活用水。
- bridge_role：某人是否连接了不同场域，例如现场抗议 + 法律程序、地方团体 + 国际 NGO、县民投票 + 选举政治。

## 推荐字段

- person_id
- person_name
- name_variants
- public_role
- actor_id
- actor_name
- issue_tags
- place_tags
- event_id
- event_date
- source_id
- relation_type: representative / co-representative / attorney / plaintiff / researcher / spokesperson / organizer / signer
- public_visibility_level
- confidence
- privacy_note
- review_status

## 可交付物

- `public_person_role_log.csv`
- `person_actor_edges_public.csv`
- “关键经纪人线索表”：只列公开角色，不做私人关系判断
- “经纪人类型说明”：现场型、法律型、国际倡议型、选举 / 公投型、离岛生活安全型

## 难点

人物网络的风险比组织网络高。公开资料会偏向媒体常引用的人，容易漏掉后台协调者；同一个人的角色也会随时间变化。更重要的是，人物关系容易越过公开信息边界，产生隐私和名誉风险。

因此不能把“同场出现”“同一声明署名”“同一组织成员”直接解释为私人关系或稳定政治同盟。所有边都必须有 source_id，并标明是公开角色、公开发言还是共同事件。

## 判断

一期可做，但只做“公开人物角色与经纪线索”。完整人物—组织互锁网络应留到扩展阶段，最好结合访谈、组织内部资料或更系统的报刊数据库。
