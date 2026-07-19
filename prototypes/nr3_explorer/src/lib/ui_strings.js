// UI chrome strings (interface copy, not data codes), zh canonical.
// Data taxonomy codes live in labels.js; this table covers fixed UI text only.

export const UI_STRINGS = {
  // nav / topbar
  "nav.overview": { zh: "总览", ja: "総覧", en: "Overview" },
  "nav.actors": { zh: "组织", ja: "組織", en: "Actors" },
  "nav.time": { zh: "时间", ja: "時間", en: "Time" },
  "nav.pathways": { zh: "路径", ja: "経路", en: "Pathways" },
  "nav.evidence": { zh: "证据", ja: "証拠", en: "Evidence" },
  "layer.demo": { zh: "已核", ja: "已核", en: "Reviewed" },
  "layer.research": { zh: "研究", ja: "研究", en: "Research" },
  "layer.hint": {
    zh: "已核视图含已确认与有限确认记录；研究视图追加待审候选与线索",
    ja: "已核ビューは確認済み・限定確認、研究ビューは審査中候補とリードを追加",
    en: "Reviewed view: supported and bounded records. Research view adds candidates and leads",
  },
  "layer.aria": { zh: "已核视图或研究视图", ja: "已核・研究ビュー", en: "Reviewed or research view" },
  "topbar.home": { zh: "回到总览", ja: "総覧へ戻る", en: "Back to overview" },
  "topbar.mainNav": { zh: "主页面", ja: "メインページ", en: "Main pages" },
  "topbar.langAria": { zh: "语言", ja: "言語", en: "Language" },
  "brand.name": { zh: "冲绳研究总图", ja: "沖縄研究総図", en: "Okinawa Research Atlas" },
  "controls.aria": { zh: "画布控制", ja: "キャンバス操作", en: "Canvas controls" },
  "controls.reset": { zh: "复位视图", ja: "ビューをリセット", en: "Reset view" },
  "controls.zoomIn": { zh: "放大", ja: "拡大", en: "Zoom in" },
  "controls.zoomOut": { zh: "缩小", ja: "縮小", en: "Zoom out" },
  "map.aria": { zh: "冲绳行政区研究地图", ja: "沖縄市町村研究マップ", en: "Okinawa municipal research map" },
  "actors.canvasAria": { zh: "组织议题生态图", ja: "組織・課題エコロジー図", en: "Actor–issue ecology canvas" },
  "map.stateAria": { zh: "地图状态", ja: "地図ステート", en: "Map state" },

  // chart titles
  "overview.title": { zh: "全域地点—议题研究地图", ja: "全域の地点・課題研究マップ", en: "Place–Issue Research Map" },
  "actors.title": { zh: "组织—议题生态图", ja: "組織・課題エコロジー図", en: "Actor–Issue Ecology" },
  "time.title": { zh: "事件与谱系时间图", ja: "イベントと系譜の時間図", en: "Events & Genealogy Timeline" },
  "pathways.title": { zh: "问题—行动—场域—产出路径图", ja: "課題—行動—場域—成果の経路図", en: "Issue–Action–Venue–Outcome Pathways" },
  "evidence.title": { zh: "证据覆盖与偏差图", ja: "証拠カバレッジと偏り図", en: "Evidence Coverage & Bias" },

  // map states
  "map.all": { zh: "全域", ja: "全域", en: "All islands" },
  "map.sakishima": { zh: "先岛聚焦", ja: "先島フォーカス", en: "Sakishima focus" },

  // regions
  "region.all": { zh: "全部区域", ja: "全区域", en: "All regions" },
  "region.okinawa": { zh: "冲绳本岛", ja: "沖縄本島", en: "Okinawa Island" },
  "region.miyako": { zh: "宫古群岛", ja: "宮古群島", en: "Miyako Islands" },
  "region.yaeyama": { zh: "八重山群岛", ja: "八重山群島", en: "Yaeyama Islands" },
  "region.other": { zh: "周边岛屿", ja: "周辺島嶼", en: "Surrounding islands" },
  "region.sakishima": { zh: "先岛群岛（宫古 · 八重山）", ja: "先島諸島（宮古・八重山）", en: "Sakishima (Miyako & Yaeyama)" },

  // class groups
  "classGroup.civic": { zh: "公民与地方组织", ja: "市民・地域組織", en: "Civic & local" },
  "classGroup.international": { zh: "国际与倡议组织", ja: "国際・アドボカシー組織", en: "International & advocacy" },
  "classGroup.legal": { zh: "法律与专业组织", ja: "法律・専門組織", en: "Legal & professional" },
  "classGroup.labor": { zh: "劳动与教育组织", ja: "労働・教育組織", en: "Labor & education" },
  "classGroup.service": { zh: "服务与福利组织", ja: "サービス・福祉組織", en: "Service & welfare" },
  "classGroup.public": { zh: "公共与交流机构", ja: "公共・交流機関", en: "Public & exchange" },
  "classGroup.resource": { zh: "企业与资源支持", ja: "企業・リソース支援", en: "Business & resource" },
  "classGroup.unknown": { zh: "尚未归组", ja: "未分類", en: "Ungrouped" },

  // common
  "common.pending": { zh: "待审", ja: "審査中", en: "Pending" },
  "common.close": { zh: "关闭", ja: "閉じる", en: "Close" },

  // overview panel
  "overview.eyebrow": { zh: "当前观察", ja: "現在の観察", en: "Now viewing" },
  "metric.places": { zh: "地点节点", ja: "地点ノード", en: "Place nodes" },
  "metric.actors": { zh: "复核组织", ja: "審査済み組織", en: "Reviewed actors" },
  "metric.triples": { zh: "严格三元组", ja: "厳格な三つ組", en: "Strict triples" },
  "overview.issues": { zh: "主要议题入口", ja: "主要な課題入口", en: "Top issue entries" },
  "overview.issuesSub": { zh: "同源证据", ja: "同一ソース", en: "Same-source" },
  "empty.triples": {
    zh: "当前区域尚无默认层严格三元组",
    ja: "この区域には既定層の厳格三つ組がありません",
    en: "No reviewed same-source triples in this region",
  },
  "overview.pickIssue": { zh: "在组织页查看该议题", ja: "組織ページでこの課題を見る", en: "Open this issue on the Actors page" },
  "overview.episodes": { zh: "相关 episode", ja: "関連エピソード", en: "Related episodes" },
  "overview.episodesSub": { zh: "路径入口", ja: "経路入口", en: "Pathway entries" },
  "overview.pickEpisode": { zh: "在路径页查看", ja: "経路ページで見る", en: "Open in Pathways" },
  "overview.pickEvent": { zh: "在时间页查看该年", ja: "時間ページでその年を見る", en: "Open this year in Time" },
  "compare.title": { zh: "比较", ja: "比較", en: "Compare" },
  "compare.clear": { zh: "退出比较", ja: "比較を終了", en: "Exit compare" },
  "compare.pickRegion": { zh: "对比区域", ja: "比較区域", en: "Compare with" },
  "compare.add": { zh: "加入比较", ja: "比較に追加", en: "Add to compare" },
  "compare.hint": { zh: "再选一个 episode 进行比较", ja: "もう1件選んで比較", en: "Pick one more episode to compare" },
  "section.events": { zh: "事件记录", ja: "イベント記録", en: "Event records" },
  "section.relations": { zh: "与其他组织的关系", ja: "他組織との関係", en: "Relations with other organizations" },
  "section.relationsSub": { zh: "类型化 · 按确认分层", ja: "タイプ別・確認度別", en: "Typed · by confirmation" },
  "section.otherRecords": { zh: "其他记录与研究线索", ja: "その他の記録と研究リード", en: "Other records & research leads" },
  "section.otherRecordsSub": { zh: "非组织关系边", ja: "組織関係辺ではない", en: "Not dyadic relations" },
  "relation.notDyadic": { zh: "非组织关系边", ja: "組織関係辺ではない", en: "Not a dyadic relation" },
  "relation.isLead": { zh: "线索，非资助事实", ja: "リード・資金事実ではない", en: "Lead, not a funding fact" },
  "relation.eventRecord": { zh: "事件参与记录", ja: "イベント参加記録", en: "Event participation record" },
  "relation.caseRole": { zh: "案件角色，非协作边", ja: "事件役割・協力辺ではない", en: "Case role, not a collaboration edge" },
  "relation.confirmed": { zh: "已确认", ja: "確認済み", en: "Confirmed" },
  "relation.missing": { zh: "缺口", ja: "欠落", en: "Missing" },
  "relation.counts": {
    zh: "已确认 {s} · 有限确认 {b} · 待审 {c} · 线索 {l}",
    ja: "確認 {s} ・ 限定 {b} ・ 審査中 {c} ・ リード {l}",
    en: "{s} supported · {b} bounded · {c} pending · {l} leads",
  },
  "empty.relations": {
    zh: "该组织暂无已核组织关系",
    ja: "この組織の已核関係はありません",
    en: "No reviewed relations for this actor",
  },
  "empty.actorEvents": { zh: "默认层暂无事件记录", ja: "既定層にイベント記録なし", en: "No event records in the demo layer" },

  // actors page
  "actors.search": { zh: "搜索组织", ja: "組織を検索", en: "Search actors" },
  "actors.classLabel": { zh: "组织类型", ja: "組織タイプ", en: "Actor class" },
  "actors.issueLabel": { zh: "议题", ja: "課題", en: "Issue" },
  "actors.allClasses": { zh: "全部类型", ja: "すべてのタイプ", en: "All classes" },
  "actors.allIssues": { zh: "全部议题", ja: "すべての課題", en: "All issues" },
  "actors.legendPending": { zh: "待审候选", ja: "審査中の候補", en: "Pending candidates" },
  "actors.noteDemo": { zh: "已核视图 · {n} 条已审关联", ja: "已核 · 審査済み {n} 件", en: "Reviewed · {n} reviewed links" },
  "actors.noteResearch": {
    zh: "研究视图 · 已审 {d} + 待审 {p}",
    ja: "研究 · 審査済み {d} + 審査中 {p}",
    en: "Research · {d} reviewed + {p} pending",
  },
  "actors.emptyTitle": { zh: "没有匹配的复核关联", ja: "一致する審査済み関連がありません", en: "No matching reviewed links" },
  "actors.noMatch": { zh: "无匹配组织", ja: "一致する組織なし", en: "No matching actors" },
  "actors.mode.ecology": { zh: "议题生态", ja: "課題エコロジー", en: "Issue ecology" },
  "actors.mode.relation": { zh: "组织关系", ja: "組織関係", en: "Relations" },
  "actors.relationCanvasAria": { zh: "组织关系图", ja: "組織関係図", en: "Actor relation graph" },
  "actors.relationNote": {
    zh: "已确认 {s} · 有限确认 {b} · 待审 {c}（仅两端均为 registry 组织的关系）",
    ja: "確認 {s} ・ 限定 {b} ・ 審査中 {c}（両端が registry 団体の関係のみ）",
    en: "{s} supported · {b} bounded · {c} pending (dyadic registry-actor relations only)",
  },
  "actors.emptyHint": { zh: "调整组织类型、议题或搜索词", ja: "タイプ・課題・検索語を調整", en: "Try another class, issue, or search term" },
  "actors.panelEmptyTitle": { zh: "选择一个组织", ja: "組織を選択", en: "Select an actor" },
  "actors.panelEmptyHint": {
    zh: "点击画布中的组织节点，查看议题、地点与参与记录。",
    ja: "キャンバス上のノードをクリックすると、課題・地点・参加記録を表示します。",
    en: "Click a node to see its issues, places, and event records.",
  },
  "metric.issues": { zh: "复核议题", ja: "審査済み課題", en: "Reviewed issues" },
  "metric.events": { zh: "事件记录", ja: "イベント記録", en: "Event records" },
  "section.issues": { zh: "议题关联", ja: "課題との関連", en: "Issue links" },
  "section.issuesReviewed": { zh: "人工复核层", ja: "人審レイヤー", en: "Human-reviewed" },
  "section.pendingIssues": { zh: "待审议题关联", ja: "審査中の課題関連", en: "Pending issue links" },
  "section.pendingSub": { zh: "研究视图 · 未人审", ja: "研究・未人審", en: "Research · unreviewed" },
  "section.places": { zh: "公开材料中的地点", ja: "公開資料上の地点", en: "Places in public records" },
  "empty.actorIssues": {
    zh: "该组织在默认层暂无已审议题关联",
    ja: "既定層に審査済み課題関連がありません",
    en: "No reviewed issue links in the demo layer",
  },
  "empty.actorPending": {
    zh: "该组织暂无待审议题关联",
    ja: "審査中の課題関連がありません",
    en: "No pending issue links",
  },
  "empty.actorPlaces": { zh: "默认层暂无地点关联", ja: "既定層に地点関連がありません", en: "No place links in the demo layer" },
  "sources.show": { zh: "查看 {n} 条身份来源", ja: "出所 {n} 件を表示", en: "View {n} identity sources" },
  "sources.hide": { zh: "收起身份来源", ja: "出所を閉じる", en: "Hide identity sources" },
  "sources.unresolved": { zh: "另有 {n} 条旧引用待解析", ja: "旧参照があと {n} 件未解決", en: "{n} legacy refs unresolved" },

  // time page
  "time.summary": {
    zh: "{e} 个事件 · {r} 条参与记录（registry {a}）",
    ja: "{e} イベント · {r} 件の参加記録（registry {a}）",
    en: "{e} events · {r} participation records ({a} registry)",
  },
  "time.pendingSuffix": { zh: " · 待审 {p}", ja: " · 審査中 {p}", en: " · {p} pending" },
  "time.eventUnit": { zh: " 事件", ja: " イベント", en: " events" },
  "time.genealogy": { zh: "组织谱系", ja: "組織系譜", en: "Organizational genealogy" },
  "time.genealogySub": {
    zh: "形成 · 改名 · 分裂 · 合并 · 连续性",
    ja: "形成・改名・分裂・合併・連続性",
    en: "Formation · rename · split · merger · continuity",
  },
  "time.gapTitle": { zh: "谱系锚点 0 条", ja: "系譜アンカー 0 件", en: "0 genealogy anchors" },
  "time.periodEmpty": { zh: "暂无已核事件", ja: "審査済みイベントなし", en: "No reviewed events" },
  "time.gapText": {
    zh: "组织谱系（形成、改名、分裂、合并、连续性）尚未进入数据层，是明确的材料缺口；待后续轮次与地方检索补齐后在这里展开。",
    ja: "組織系譜（形成・改名・分裂・合併・連続性）はまだデータ層に入っていない明確な資料ギャップです。今後のラウンドと現地調査で補完され次第ここに展開します。",
    en: "Organizational genealogy (formation, renames, splits, mergers, continuity) is not in the data layer yet — an explicit material gap. It will appear here once later rounds and local retrieval fill it.",
  },
  "time.pendingHeader": { zh: "待审候选", ja: "審査中の候補", en: "Pending candidates" },
  "time.pendingSub": { zh: "分析种子 · 年份未定", ja: "分析シード・年未定", en: "Analytical seeds · year undecided" },
  "time.eventOnly": {
    zh: "另含 {n} 个事件级参与者（非 registry 组织，不计入组织页）",
    ja: "イベント限定の参加者が他に {n} 名（registry 団体ではなく、組織ページには計上しません）",
    en: "Plus {n} event-only participants (not registry actors; not counted as organizations)",
  },
  "period.p1.focus": {
    zh: "历史背景与组织源流线索（非重点）",
    ja: "歴史背景と組織源流の手がかり（非重点）",
    en: "Historical background & organizational lineage (non-focus)",
  },
  "period.p2.focus": {
    zh: "NPO 法人化后较易公开追踪的组织资料",
    ja: "NPO法人化以降、公開追跡しやすい組織資料",
    en: "Post-NPO-incorporation records, easier to trace publicly",
  },
  "period.p3.focus": {
    zh: "边野古、县民投票、环保倡议、诉讼与全县性政治化",
    ja: "辺野古・県民投票・環境アドボカシー・訴訟と全県的な政治化",
    en: "Henoko, prefectural referendum, environmental advocacy, litigation & prefecture-wide politicization",
  },
  "period.p4.focus": {
    zh: "国际倡议、环境正义、先岛与那国安全化、生活安全与跨国连接",
    ja: "国際アドボカシー・環境正義・先島（与那国）の安保化・生活安全と越境接続",
    en: "International advocacy, environmental justice, Sakishima/Yonaguni securitization, life safety & transnational ties",
  },
  "period.p4.range": { zh: "2020–现在", ja: "2020–現在", en: "2020–present" },

  // pathways
  "path.summary": {
    zh: "{n} 个已核 episode · {m} 类路径",
    ja: "{n} 審査済みエピソード · {m} 経路群",
    en: "{n} reviewed episodes · {m} route families",
  },
  "path.summaryResearch": {
    zh: "已核 {d} ＋ 待审 {p} · {m} 类路径",
    ja: "審査済み {d} ＋ 審査中 {p} · {m} 経路群",
    en: "{d} reviewed + {p} pending · {m} route families",
  },
  "stage.local_problem": { zh: "地方问题", ja: "地方課題", en: "Local problem" },
  "stage.translation_frame": { zh: "转译框架", ja: "翻訳フレーム", en: "Translation frame" },
  "stage.venue_entry": { zh: "场域进入", ja: "場域進入", en: "Venue entry" },
  "stage.intermediate_output": { zh: "中间产出", ja: "中間成果", en: "Intermediate output" },
  "stage.bounded_gain": { zh: "有限结果", ja: "限定的結果", en: "Bounded gain" },
  "stage.underlying_change": { zh: "底层改变", ja: "底層の変化", en: "Underlying change" },
  "chip.context": { zh: "给定背景", ja: "前提背景", en: "Context" },
  "chip.yes": { zh: "观察到", ja: "観察された", en: "Observed" },
  "chip.mixed": { zh: "部分 · 混合", ja: "一部・混合", en: "Partial / mixed" },
  "chip.no": { zh: "未观察到", ja: "観察されず", en: "Not observed" },
  "chip.unknown": { zh: "未知", ja: "不明", en: "Unknown" },
  "path.places": { zh: "相关地点", ja: "関連地点", en: "Related places" },
  "path.actors": { zh: "参与组织", ja: "参加組織", en: "Participating actors" },
  "path.actorsSub": { zh: "{n} 个 registry actor", ja: "{n} の registry アクター", en: "{n} registry actors" },
  "path.sources": { zh: "来源", ja: "ソース", en: "Sources" },
  "path.countUnit": { zh: "{n} 条", ja: "{n} 件", en: "{n}" },
  "path.cases": { zh: "关联案件", ja: "関連案件", en: "Related cases" },

  // evidence page
  "evidence.summary": {
    zh: "{c} 个覆盖单元 · {d} 个维度",
    ja: "{c} カバレッジセル · {d} 次元",
    en: "{c} coverage cells · {d} dimensions",
  },
  "evidence.mechanism": { zh: "可见性机制", ja: "可視性のメカニズム", en: "Visibility mechanism" },
  "evidence.impact": { zh: "对研究问题的影响", ja: "研究課題への影響", en: "Impact on research questions" },
  "evidence.online": { zh: "线上补缺", ja: "オンライン補完", en: "Online gap actions" },
  "evidence.local": { zh: "当地补缺", ja: "現地補完", en: "Local gap actions" },
  "evidence.modules": { zh: "影响模块", ja: "影響モジュール", en: "Affected modules" },
  "evidence.noImplication": {
    zh: "该维度暂无机制解释",
    ja: "この次元の機構説明は未整備",
    en: "No mechanism note for this dimension",
  },
  "evidence.denominator": { zh: "分母 {n}", ja: "分母 {n}", en: "denominator {n}" },
  "evidence.cellUnit": { zh: " 单元", ja: " セル", en: " cells" },
  "dim.D1": { zh: "时间", ja: "時間", en: "Time" },
  "dim.D2": { zh: "地点", ja: "地点", en: "Place" },
  "dim.D3": { zh: "actor 功能·来源层", ja: "アクター機能・ソース層", en: "Actor function & source layer" },
  "dim.D4": { zh: "议题", ja: "課題", en: "Issue" },
  "dim.D5": { zh: "来源类型·归档", ja: "ソース種別・保存", en: "Source type & archive" },
  "dim.D6": { zh: "复核·证据", ja: "審査・証拠", en: "Review & evidence" },

  // drawer
  "drawer.title": { zh: "证据来源", ja: "証拠ソース", en: "Evidence sources" },
  "drawer.loading": { zh: "正在读取证据层…", ja: "証拠レイヤーを読み込み中…", en: "Loading evidence layer…" },
  "drawer.year": { zh: "来源年份", ja: "ソース年", en: "Source year" },
  "drawer.supports": { zh: "支持内容", ja: "支持内容", en: "Supports" },
  "drawer.archive": { zh: "归档状态", ja: "保存状態", en: "Archive status" },
  "drawer.archiveFailed": {
    zh: "（可重试，不等于证据不存在）",
    ja: "（再試行可・証拠がないとは限りません）",
    en: " (retryable; failure ≠ absence of evidence)",
  },
  "drawer.bias": { zh: "偏向提示", ja: "バイアス注意", en: "Bias note" },
  "drawer.noClaim": { zh: "不可支持主张", ja: "主張の根拠に使用不可", en: "Cannot support claims" },
  "drawer.missing": {
    zh: "{id}：当前证据层未收录该 ID。",
    ja: "{id}：この ID は現在の証拠層にありません。",
    en: "{id}: not in the current evidence layer.",
  },

  // loading
  "loading.busy": { zh: "正在加载数据", ja: "データを読み込み中", en: "Loading data" },
  "loading.error": { zh: "数据读取失败", ja: "読み込み失敗", en: "Failed to load data" },
  "loading.errorHint": {
    zh: "请确认数据包可用。",
    ja: "データパッケージを確認してください。",
    en: "Please check the data package.",
  },

  // help popovers
  "help.overview.p1": {
    zh: "地图按 42 个市町村行政区划绘制，颜色只用来区分四个区域。点击陆地选中一个区域，滚轮缩放、拖拽平移。",
    ja: "42の市町村行政区画で描かれた地図です。色は4つの区域を区別するためだけに使います。陸地をクリックして区域を選択、ホイールでズーム、ドラッグでパン。",
    en: "The map shows 42 municipal boundaries; color only separates the four island groups. Click land to select a region; scroll to zoom, drag to pan.",
  },
  "help.overview.p2": {
    zh: "右侧面板列出该区域已人工复核的同源地点—议题三元组；切到研究视图会追加待审候选计数。",
    ja: "右パネルにはその区域の人審済み・同一ソース地点—課題トリプルを表示します。研究ビューに切り替えると審査中の候補数が追加されます。",
    en: "The right panel lists human-reviewed same-source place–issue triples for the region; the research view adds pending candidate counts.",
  },
  "help.actors.p1": {
    zh: "已核视图画的是已人工复核的组织—议题关联；研究视图追加虚线边和虚线圈节点，即待审候选。节点向自己的议题聚拢，大小和位置只是布局结果。",
    ja: "已核ビューは人審済みの組織—課題関連のみを描きます。研究ビューでは破線の辺と破線円のノード（審査中の候補）が加わります。ノードは自分の課題に寄り集まり、大きさと位置はレイアウト上の結果にすぎません。",
    en: "The reviewed view draws only human-reviewed actor–issue links; the research view adds dashed edges and dashed-ring nodes (pending candidates). Nodes cluster toward their issues; size and position are layout artifacts.",
  },
  "help.actors.p2": {
    zh: "点击节点查看组织详情，点击空白处取消选择；滚轮缩放、拖拽平移。",
    ja: "ノードをクリックで組織の詳細、空白をクリックで選択解除。ホイールでズーム、ドラッグでパン。",
    en: "Click a node for details; click empty space to deselect. Scroll to zoom, drag to pan.",
  },
  "help.time.p1": {
    zh: "年份记录的是“某组织在某年做过某事”。点击年份查看当年事件，点击事件中的参与者跳转组织页。",
    ja: "年は「ある組織がある年に行ったこと」の記録です。年をクリックでその年のイベント、参加者をクリックで組織ページへ。",
    en: "Each year records “what an organization did that year”. Click a year for its events; click a participant to open the actor page.",
  },
  "help.time.p2": {
    zh: "四个时段节点来自一期方案的采集策略。组织谱系（形成、改名、分裂、合并）尚未进入数据层，当前显示为缺口，补齐后在这里展开。",
    ja: "4つの期間はフェーズ1計画の収集方針に由来します。組織系譜（形成・改名・分裂・合併）はまだデータ層に入っておらず、現在はギャップ表示です。補完後にここへ展開します。",
    en: "The four periods come from the Phase-1 collection plan. Organizational genealogy (formation, renames, splits, mergers) is not in the data layer yet and shows as an explicit gap; it will appear here when filled.",
  },
  "help.pathways.p1": {
    zh: "按六个阶段读一个案件：地方问题、转译框架、场域进入、中间产出、有限结果、底层改变。状态芯片直接来自数据：“未观察到”指材料中没有该结果的记录。",
    ja: "6段階で案件を読みます：地方課題・翻訳フレーム・場域進入・中間成果・限定的結果・底層の変化。ステータスはデータそのままで、「観察されず」は資料に該当結果の記録がないことを意味します。",
    en: "Read each case in six stages: local problem, translation frame, venue entry, intermediate output, bounded gain, underlying change. Status chips come straight from the data; “Not observed” means the material records no such result.",
  },
  "help.pathways.p2": {
    zh: "左侧按路径族选择案件；研究视图会追加待审 episode。",
    ja: "左の経路群から案件を選びます。研究ビューでは審査中のエピソードが追加されます。",
    en: "Pick a case by route family on the left; the research view adds pending episodes.",
  },
  "help.evidence.p1": {
    zh: "每个单元统计工作样本中某类材料的数量，反映的是文献可见度。各单元有自己的计数单位与分母，只在同一张小图内比较。来源年份、事件年份、主张时期是三种不同的时间。",
    ja: "各セルは作業サンプル内の資料量を数え、文献の可視性を表します。セルごとに単位と分母があり、同じ小図の中だけで比較してください。ソース年・イベント年・主張期間は別々の時間です。",
    en: "Each cell counts material in the working sample — documentary visibility. Every cell has its own unit and denominator; compare only within one mini-chart. Source year, event year, and claim period are different clocks.",
  },
  "help.evidence.p2": {
    zh: "右侧面板给出该维度的机制解释与缺口行动（线上／当地），均来自覆盖审计数据。",
    ja: "右パネルはその次元のメカニズム説明とギャップ対応（オンライン／現地）で、いずれもカバレッジ監査データに基づきます。",
    en: "The right panel gives the dimension's mechanism and gap actions (online/local), all from the coverage-audit data.",
  },
};

export const tu = (key, lang = "zh") =>
  UI_STRINGS[key]?.[lang] || UI_STRINGS[key]?.zh || key;
