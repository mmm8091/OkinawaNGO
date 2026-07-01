# R11 跨国 / 国际倡议网络

## 结论

这个模块可以做，而且价值高。它不是简单列出“海外也有人支持冲绳”，而是能说明冲绳地方反基地运动如何被翻译成环境正义、海洋生物保护、文化财保护、人权、国际法和美国行政程序等跨国议题。

一期建议做“样本型跨国倡议网络”，不要承诺全量跨国网络。合理目标是围绕边野古 / 大浦湾 / 儒艮议题，抽取 30-60 个冲绳、日本国内和海外节点，展示地方团体如何把国内难以解决的问题推向美国法院、美国联邦机构、国际环保组织和国际舆论空间。

## 已主动探查的资料

1. Okinawa Environmental Justice Project 2020 年记录：2020 年 7 月 10 日，由 OEJP 主导，71 个冲绳、日本及海外团体向美国 Marine Mammal Commission 提交请求信和市民社会报告，要求审查美国国防部关于边野古基地建设对冲绳儒艮“无不利影响”的判断。
   - https://okinawaejp.blogspot.com/2020/07/

2. Asia-Pacific Journal / Japan Focus 对同一事件有更完整说明。文章明确把该行动解释为冲绳市民社会与 Marine Mammal Commission 长期沟通的结果，并称其为“internationalize” 边野古基地建设和自然保护问题的努力。
   - https://apjjf.org/2020/16/yoshikawaoejp

3. Earthjustice 的 Okinawa dugong case 页面显示，Earthjustice 代表 Center for Biological Diversity、Turtle Island Restoration Network、Japan Environmental Lawyers Federation、Save the Dugong Foundation 以及冲绳个人原告等，围绕美国国防部是否充分考虑边野古基地对儒艮的影响展开诉讼。
   - https://earthjustice.org/case/okinawa-dugong-proposed-airbase

4. Earthjustice 的说明文章把儒艮保护、美国国家历史保护法、边野古基地建设、冲绳地方主权和美国军事存在联系起来，适合用来编码“地方生态议题 -> 美国法律程序 -> 国际倡议”的转译路径。
   - https://earthjustice.org/article/fighting-to-protect-the-dugongs-of-japan-s-henoko-bay

5. WWF Japan、日本自然保护协会、Peace Boat、Greenpeace Japan 等组织在边野古和大浦湾议题上有声明、请求或联名行动，可作为日本国内 NGO 与冲绳地方组织连接的样本来源。

## 能抽取的数据关系

- actor_to_actor：冲绳地方团体与日本国内 NGO、海外 NGO、律师组织、国际倡议平台的共同声明或共同诉讼关系。
- actor_to_institution：地方团体向 Marine Mammal Commission、美国法院、IUCN、UN 相关机制等机构发声的关系。
- actor_to_issue：团体将边野古问题表述为儒艮保护、珊瑚礁保护、文化财保护、环境影响评价、人权、地方自治或反军事化的关系。
- event_to_actor：某一封请求信、诉讼、声明、国际会议、署名行动中出现了哪些组织。
- frame_translation：同一地点问题如何从“基地反对”变成“environmental justice / cultural heritage / marine mammal protection / indigenous rights”等框架。

## 推荐字段

- edge_id
- source_id
- event_name
- event_date
- actor_1
- actor_1_type
- actor_1_location
- actor_2
- actor_2_type
- actor_2_location
- relation_type: joint_statement / lawsuit / request_letter / campaign / forum / citation
- issue_tags
- international_forum_or_institution
- evidence_quote_or_summary
- confidence
- review_status

## 可交付物

- `transnational_advocacy_edges.csv`
- `international_actor_registry.csv`
- “地方议题国际化路径图”：Henoko/Oura Bay -> dugong/ecology -> EIA critique -> U.S. court/MMC -> international NGO support
- “跨国倡议网络小报告”：解释冲绳 NGO 不是孤立地方团体，而是会借助国际环保法、美国程序和跨国 NGO 扩大议题能见度

## 难点

最大难点是区分“真实协作关系”和“一次性共同署名关系”。共同声明里的 71 个团体不能直接等同于稳定联盟，否则网络图会虚胖。建议把关系强度分成三档：一次性署名、重复共同发声、共同诉讼或长期协作。

另一个难点是跨国资料偏向英文与环境议题，容易让边野古看起来只是“环保议题”。写作时需要保留它与基地、地方自治、民主程序和生活安全的连接。

## 判断

可作为一期重点模块之一。它的展示效果强，也能直接回应甲方关于“NGO 起了什么作用”的问题：NGO 的作用之一，就是把地方基地争议转译成国际机构能处理的环境、人权和法律议题。
