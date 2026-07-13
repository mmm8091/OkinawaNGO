# HR-020：R5 共同行动名称／身份人工复核包

本包只处理线上来源仍无法自动决定的名称切分、日英别名和 registry 对应。事件参与本身已有一手名单支持；待决定的是“这些名称是否代表同一 actor”。

共 14 个问题。`decision`、`human_reviewer`、`review_date`、`decision_note` 均未预填。接受别名只会改变身份连接与重复参与计数，不会把共同署名改写为稳定联盟。

## 决策规则

- `accept`：明确接受题面对应，按影响说明回写 actor/entity key。
- `revise`：给出新的规范名、actor、组织层级或名单切分。
- `reject`：保留不同 event-only names，不建立跨事件或 registry 连接。
- 任何决定都不得仅凭共同署名推定成员关系、资金关系或持续协调。

## 待审项目


### HR020-01｜2020 AOCHR 对应 A054 沖縄人権協会

- 对象：`EV2020_OEJP_MMC_71:P012`
- 事件：`EV2020_OEJP_MMC_71`
- 来源原名：All Okinawa Council for Human Rights (AOCHR)
- 候选 registry actor：`A054`
- 来源：`S006`
- 精确定位：MMC letter pp. 5-7, participant 12
- 人工问题：英文 AOCHR 是否确为 registry A054，而非另一个全冲绳人权团体？
- 若接受：把该参与行连接到 A054；若 A054 另有跨事件行，重复参与计数随之更新。
- 若修订：按人审给出的其他 actor 或规范名连接，并记录修订依据。
- 若拒绝：保留为 event-only name，不进入 registry actor 桥梁。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-02｜2020 Anti-war Network 对应 A008 NGO非戦ネット

- 对象：`EV2020_OEJP_MMC_71:P044`
- 事件：`EV2020_OEJP_MMC_71`
- 来源原名：Anti-war Network
- 候选 registry actor：`A008`
- 来源：`S006;S064;S065;S066;S067`
- 精确定位：MMC letter pp. 5-7, participant 44; A008 existing sources
- 人工问题：通用英文名 Anti-war Network 是否足以对应 A008 NGO非戦ネット？
- 若接受：把参与行连接到 A008；不得恢复 S005 对 A008 的旧误配。
- 若修订：按核实到的正式英文名或另一个主体修订。
- 若拒绝：保留为 event-only name；A008 不获得 2020 参与关系。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-03｜2020 基地撤去和平组织英文名对应 A072

- 对象：`EV2020_OEJP_MMC_71:P068`
- 事件：`EV2020_OEJP_MMC_71`
- 来源原名：The Association for Military Base Free Peaceful Okinawa
- 候选 registry actor：`A072`
- 来源：`S006;S031`
- 精确定位：MMC letter pp. 5-7, participant 68; registry A072 source S031
- 人工问题：The Association for Military Base Free Peaceful Okinawa 是否确为 A072？
- 若接受：把参与行连接到 A072，并仅解释为一次请求参与。
- 若修订：连接到人审核定的其他主体或规范名。
- 若拒绝：保留为 event-only name。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-04｜2020 大阪行动罗马字名对应 A110

- 对象：`EV2020_OEJP_MMC_71:P051`
- 事件：`EV2020_OEJP_MMC_71`
- 来源原名：Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo
- 候选 registry actor：`A110`
- 来源：`S006;S153;S154`
- 精确定位：MMC letter pp. 5-7, participant 51; A110 organization sources
- 人工问题：Henoko ni kichi wo Zettai Tsukurasenai Osaka Kodo 是否为 A110 的罗马字署名？
- 若接受：连接 A110；证明2020请求参与，不证明与其他签署者有稳定联盟。
- 若修订：按人审结果修订为其他主体或规范罗马字别名。
- 若拒绝：保留为 event-only name；A110 不获得该事件关系。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-05｜2020 Stop! Henoko Reclamation Campaign 对应 A106

- 对象：`EV2020_OEJP_MMC_71:P065`
- 事件：`EV2020_OEJP_MMC_71`
- 来源原名：Stop! Henoko Reclamation Campaign
- 候选 registry actor：`A106`
- 来源：`S006;S126;S127`
- 精确定位：MMC letter pp. 5-7, participant 65; A106 organization sources
- 人工问题：Stop! Henoko Reclamation Campaign 是否为 A106 首都圏キャンペーン／連絡会的英文署名？
- 若接受：连接 A106；不解决 A106 当前 canonical variant 的另一个待定问题。
- 若修订：按人审给出的英文名、组织层级或其他 actor 修订。
- 若拒绝：保留为 event-only name。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-06｜2010 名单缺分隔符的两组织切分

- 对象：`EV2010_WWF_67:P060;EV2010_WWF_67:P061`
- 事件：`EV2010_WWF_67`
- 来源原名：憲法ひろば・杉並;福岡地区合同労働組合
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;R5S004`
- 精确定位：S003 raw.html line 438; WBSJ mirror 賛同団体 paragraph
- 人工问题：标称67团体但逗号切分仅66项；“憲法ひろば・杉並福岡地区合同労働組合”是否应切成两个组织？
- 若接受：保留两行，2010结构化总数与来源声明67一致。
- 若修订：按人审提供的正确边界或正式名修订两行。
- 若拒绝：合并为一个 source-literal 名称；结构化可辨名称降为66，并保留来源自称67的差异。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-07｜二見以北十区组织的日英跨事件对应

- 对象：`EV2010_WWF_67:P010;EV2020_OEJP_MMC_71:P019`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：ヘリ基地いらない二見以北十区の会;No Heliport Base Association of 10 Districts North of Futamai
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 19
- 人工问题：2010“ヘリ基地いらない二見以北十区の会”与2020英文名是否为同一组织？
- 若接受：合并为一个 event-only bridge，进入2010/2020重复参与表。
- 若修订：按核实到的正式名、英文别名或组织沿革修订。
- 若拒绝：两行保持独立 event-only names。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-08｜北限儒艮组织的日英跨事件对应

- 对象：`EV2010_WWF_67:P013;EV2020_OEJP_MMC_71:P009`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：北限のジュゴンを見守る会;Protect Northernmost Dugong Team Zan
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 9
- 人工问题：2010“北限のジュゴンを見守る会”与2020 Protect Northernmost Dugong Team Zan 是否同一组织？
- 若接受：合并为一个 event-only bridge，进入2010/2020重复参与表。
- 若修订：按人审给出的组织名或沿革关系修订。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-09｜環瀬戸内海会議的日英跨事件对应

- 对象：`EV2010_WWF_67:P022;EV2020_OEJP_MMC_71:P035`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：環瀬戸内海会議;Pan-Seto Inland Sea Congress
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 35
- 人工问题：Pan-Seto Inland Sea Congress 是否为環瀬戸内海会議的英文名？
- 若接受：合并为2010/2020 event-only bridge。
- 若修订：按核实到的正式英文名或继承关系修订。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-10｜海洋生物保护组织的日英跨事件对应

- 对象：`EV2010_WWF_67:P032;EV2020_OEJP_MMC_71:P029`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：海の生き物を守る会;Association for Conservation of Marine Communities
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 29
- 人工问题：Association for Conservation of Marine Communities 是否对应2010“海の生き物を守る会”？
- 若接受：合并为2010/2020 event-only bridge。
- 若修订：按人审确认的其他日文名修订。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-11｜みん宿ヤポネシア的日英跨事件对应

- 对象：`EV2010_WWF_67:P042;EV2020_OEJP_MMC_71:P016`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：みん宿ヤポネシア;Minshuku Yaponesia
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 16
- 人工问题：Minshuku Yaponesia 是否就是2010“みん宿ヤポネシア”？
- 若接受：合并为2010/2020 event-only bridge；仍不自动认定为 NGO。
- 若修订：修订其实体类型、正式名或组织／场所边界。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-12｜じゅごんの里的日英跨事件对应

- 对象：`EV2010_WWF_67:P066;EV2020_OEJP_MMC_71:P003`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：じゅごんの里;Dugong no Sato
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 3
- 人工问题：Dugong no Sato 是否就是2010“じゅごんの里”？
- 若接受：合并为2010/2020 event-only bridge。
- 若修订：按正式名或组织持续性证据修订。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-13｜命どぅ宝名称的日英跨事件对应

- 对象：`EV2010_WWF_67:P055;EV2020_OEJP_MMC_71:P020`
- 事件：`EV2010_WWF_67;EV2020_OEJP_MMC_71`
- 来源原名：沖縄について考え・連帯する「命どぅ宝」の会;Nuchi du Takara o keisyosurukai
- 候选 registry actor：`无／跨事件 event-only 对应`
- 来源：`S003;S006`
- 精确定位：S003 signatory paragraph; MMC letter participant 20
- 人工问题：Nuchi du Takara o keisyosurukai 是否对应2010“沖縄について考え・連帯する『命どぅ宝』の会”？
- 若接受：合并为2010/2020 event-only bridge。
- 若修订：按人审确认的日文原名或不同组织关系修订。
- 若拒绝：两行保持独立。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：


### HR020-14｜“自然の権利”基金与 JELF 的实体边界

- 对象：`EV2010_WWF_67:P017`
- 事件：`EV2010_WWF_67`
- 来源原名：「自然の権利」基金
- 候选 registry actor：`A020`
- 来源：`S003`
- 精确定位：S003 signatory paragraph and JUCON contact line 441-442
- 人工问题：2010名单将 JELF 与“自然の権利”基金分别列名；基金应作为独立 event-only 名、JELF 下属项目，还是 A020 别名？
- 若接受：按人审指定边界连接；若并入 A020，必须注明同一事件双列名问题并避免重复计数。
- 若修订：记录为项目／组织层级关系，但不作为同一 actor。
- 若拒绝：维持独立 event-only name；不把联系地址关系写成组织同一。

决定（留空）：[ ] accept　[ ] revise　[ ] reject

复核人：__________　日期：__________

决定说明：



## 回写要求

人审完成后，应同时重跑参与表、二部边、重复桥梁、重叠表、两图和解释性 brief，并保留原始 `source_name`。
