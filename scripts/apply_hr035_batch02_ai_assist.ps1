param(
    [switch]$ConfirmPrincipal
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$edgePath = Join-Path $root 'outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch02_v1.csv'
$identityPath = Join-Path $root 'outputs/actor_issue_claim_freeze_v1/HR035_actor_identity_companion_batch02_v1.csv'
$bundlePath = Join-Path $root 'outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch02_v1.csv'
$sourceLogPath = Join-Path $root 'data/interim/05_source_log_initial_v0.csv'

$reviewer = if ($ConfirmPrincipal) {
    'project_principal_user'
} else {
    'AI_assist_pending_principal_confirmation'
}
$reviewDate = if ($ConfirmPrincipal) { '2026-07-20' } else { '' }
$notePrefix = if ($ConfirmPrincipal) {
    '项目负责人确认 AI 辅助建议；'
} else {
    'AI辅助建议，待项目负责人确认；'
}

$edgeReviewedFields = 'relation_existence;actor_identity;issue_mapping;source_ref;evidence_level;interpretation_boundary'
$identityReviewedFields = 'actor_identity;canonical_name;actor_class;origin_type;legal_status;source_ref;evidence_level'

$identityDecisions = @{
    A007 = @{
        human_decision = 'revise_identity'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        canonical_name_final = 'ピースボート'
        actor_class_final = 'domestic_japan_ngo'
        origin_type_final = 'japan_domestic'
        legal_status_final = 'nonprofit_form_unresolved'
        approved_identity_formulation = 'S005 的官方页面与站点品牌可确认ピースボート是独立可识别的日本 NGO；本批来源不确认其具体法人形态。'
        identity_interpretation_limit = '“国際交流NGO”是组织自我描述，不等于已核法定法人资格；共同声明参与不生成联盟，也不自动批准其他议题边。'
        review_note = $notePrefix + '名称、独立组织身份、国内 NGO 类型和来源等级成立；将未由 S005 证明的 nongovernmental_nonprofit 法律形态修订为 nonprofit_form_unresolved。'
    }
    A017 = @{
        human_decision = 'accept_identity'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        canonical_name_final = '沖縄対話プロジェクト'
        actor_class_final = 'citizen_network'
        origin_type_final = 'okinawa_local'
        legal_status_final = 'legal_form_unresolved'
        approved_identity_formulation = '官方站点以固定名称、共同代表、规约、企划书、发足记者会和活动日程呈现沖縄対話プロジェクト，可作为冲绳市民对话网络独立识别。'
        identity_interpretation_limit = '项目／网络身份不等于法人资格；参与者、共同代表和活动来宾不得自动拆成 actor 或推导稳定组织关系。'
        review_note = $notePrefix + 'S022 直接闭合名称、组织载体、冲绳市民发起属性和未解决的法律形态。'
    }
    A018 = @{
        human_decision = 'revise_identity'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        canonical_name_final = 'ノーモア沖縄戦 命どぅ宝の会'
        actor_class_final = 'citizen_group'
        origin_type_final = 'okinawa_local'
        legal_status_final = 'legal_form_unresolved_citizen_group'
        approved_identity_formulation = 'S023 点名该会、成立时间、发足集会、五名共同代表及冲绳市民团体属性，足以确认其为独立可识别 actor。'
        identity_interpretation_limit = '地方新闻所称“市民グループ”不证明正式法人形态；S024 是另一项目页面，不承担该会身份确认。'
        review_note = $notePrefix + '身份成立，但 current informal_association 是未被直接证明的法律形态；修订为 legal_form_unresolved_citizen_group，并以 S023 为主要身份依据。'
    }
    A049 = @{
        human_decision = 'revise_identity'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        canonical_name_final = '基地・軍隊を許さない行動する女たちの会'
        actor_class_final = 'citizen_group'
        origin_type_final = 'okinawa_local'
        legal_status_final = 'legal_form_unresolved_citizen_group'
        approved_identity_formulation = 'S039 的学术个案研究直接记载该会名称、1995 年后的成立过程与组织活动，可确认其为冲绳地方女性市民团体。'
        identity_interpretation_limit = '学术二手材料最高按 E3；不能据此确认正式法人形态、全部时期连续性或每位成员的一致立场。'
        review_note = $notePrefix + '身份与组织类型成立；证据等级由 E4 下调为 S039 上限 E3，法律形态由 informal_association 修订为 legal_form_unresolved_citizen_group。'
    }
    A066 = @{
        human_decision = 'revise_identity'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        canonical_name_final = '新外交イニシアティブ（ND）'
        actor_class_final = 'domestic_japan_ngo'
        origin_type_final = 'japan_domestic'
        legal_status_final = 'nonprofit_form_unresolved'
        approved_identity_formulation = 'S032 官方站点以固定名称、组织简介、活动栏目、会员与捐助入口呈现新外交イニシアティブ（ND），可确认其为日本国内政策倡议 NGO／智库。'
        identity_interpretation_limit = '当前归档首页没有直接列示“特定非営利活動法人”资格；智库／政策倡议身份不自动确认任何具体法律、自治或反基地议题边。'
        review_note = $notePrefix + '独立组织身份、名称、国内 NGO 类型和 E4 来源成立；将未由 S032 首页证明的 specified_nonprofit_corporation 修订为 nonprofit_form_unresolved。'
    }
}

$edgeDecisions = @{
    AI016 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'ピースボート—international_advocacy 仅表示其在 2015 年 3 月 25 日作为国内外 31 个 NGO 紧急共同声明的赞同团体之一，参与边野古议题的跨组织公开倡议。'
        review_scope_final = 'event_specific'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S005 是ピースボート官方页面，直接确认其作为赞同团体参与该次边野古紧急共同声明。'
        missing_scope = '当前材料不确认长期 Okinawa project、持续对美传播或其他年份的国际倡议定位。'
        interpretation_limit = '一次共同声明参与不生成稳定联盟、成员关系或全部时期定位，也不证明声明造成政策效果。'
        scope_revision_required = 'yes'
        review_note = $notePrefix + 'S005 足以闭合事件性参与，不足以闭合 HR-019 所述长期项目；建议把 organizational_positioning 收窄为 event_specific。'
    }
    AI040 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '沖縄対話プロジェクト—Taiwan_contingency 表示其官方设立宗旨把防止“台湾有事／南西諸岛有事”和避免冲绳再次成为战场作为对话项目的核心问题框架。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S022 官方页面直接说明项目目的、发起背景、2022–2023 对话计划及台湾、冲绳前线化风险框架。'
        missing_scope = '不确认项目代表全部冲绳市民，也不确认对话已改变政府政策、地区安全环境或冲突风险。'
        interpretation_limit = '记录的是组织公开问题框架与预防性目的；风险判断不得升级为已发生事实或已证政策效果。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '组织自有站点直接支持该精确议题映射及有界组织定位。'
    }
    AI042 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '沖縄対話プロジェクト—peace 表示其以跨越政治立场的市民对话、防止战争及推动和平国际社会为公开项目目的。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S022 官方页面明确写明战争与对话中断的关系、跨境市民对话计划及防止沖縄再成战场的项目目的。'
        missing_scope = '不确认活动已产生和平政策效果、化解国家间冲突或形成稳定跨国组织联盟。'
        interpretation_limit = '项目目的与活动计划不等于效果评估；与台湾、中国、美国市民对话的计划不自动生成组织间关系边。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '官方目的陈述足以确认 peace 组织定位，保留效果边界。'
    }
    AI044 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'ノーモア沖縄戦 命どぅ宝の会—Taiwan_contingency 表示该会在 2021 年成立及 2022 年发足集会语境中，公开反对以“台湾有事”为前提使南西诸岛成为攻击据点。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S023 点名该会并直接转述其成立目的、共同代表和反对台湾有事想定下南西诸岛攻击据点化的公开主张。'
        missing_scope = '不确认 S023 所述成立期之后全部年份的持续活动，也没有组织自有官网材料闭合长期连续性。'
        interpretation_limit = '以第三方新闻直接归因的成立期组织主张为限；不把 S024 的沖縄対話プロジェクト内容转嫁给 A018，不推断政策效果或联盟。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '当前 S024 来源错位；改用 S023 闭合精确 actor—issue 映射。接受的是成立期公开定位，不是无限期连续性。'
    }
    AI119 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        approved_formulation = '基地・軍隊を許さない行動する女たちの会—life_safety 仅表示其从女性人权、军事性暴力与身体／日常生活安全角度提出基地和军队问题。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S039 的学术个案研究把该会的成立、性暴力问题与安全保障的性别化批判直接连接。'
        missing_scope = '不支持一般化“治安”标签，不确认所有时期、所有行动或全部成员对每项生活安全议题立场一致。'
        interpretation_limit = 'life_safety 在此限于女性人权、身体安全与军事性暴力语境；材料不证明个案因果、犯罪趋势或政策效果。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '事实成立但需收窄措辞；按直接来源上限由 E4 下调为 E3。'
    }
    AI121 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        approved_formulation = '基地・軍隊を許さない行動する女たちの会—anti_military 表示该会把反对基地、军队及其结构性／性别化暴力作为可观察的组织定位。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S039 的题名、成立史与个案分析直接围绕该会对基地、军队和军事性暴力的反对。'
        missing_scope = '不确认每次行动、所有成员或全部时期对所有军事政策持完全相同立场。'
        interpretation_limit = '组织名称与学术分析支持有界定位，但不能把一项组织定位扩为全部成员意见、稳定联盟或行动效果。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '精确映射成立；按 S039 最高直接支持把 E4 下调为 E3。'
    }
    AI157 = @{
        human_decision = 'defer_second_source'
        revised_review_status = 'needs_second_source'
        evidence_level_final = 'E4'
        approved_formulation = '暂不批准 ND—legal 事实边；S032 首页只确认政策倡议／外交智库身份，未直接闭合行政法、地方自治法或具体制度论证。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'candidate'
        confirmed_scope = 'S032 官方首页确认 ND 从事信息传播、政策提言和包含沖縄／米军基地主题的政策研究。'
        missing_scope = '缺少可定位的 ND 自有报告或政策文本，直接显示行政法、地方自治法等法律论证。'
        interpretation_limit = '政策研究或基地议题栏目不等于 legal 议题边；不得从组织类型、作者职业或页面链接标题推断法律角色。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '线上仍可补 ND 的具体报告／提言页，故建议 defer_second_source 而非接受或转当地材料。'
    }
    AI158 = @{
        human_decision = 'defer_second_source'
        revised_review_status = 'needs_second_source'
        evidence_level_final = 'E4'
        approved_formulation = '暂不批准 ND—local_autonomy 事实边；S032 首页显示沖縄与地域外交政策研究，但没有直接闭合国—地方权限或地方自治主张。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'candidate'
        confirmed_scope = 'S032 官方首页确认 ND 的政策倡议、外交智库身份与沖縄／基地政策主题。'
        missing_scope = '缺少可定位的 ND 自有政策文本，明确讨论国—地方权限、地方自治或冲绳地方政府权限。'
        interpretation_limit = '“地域外交”“沖縄政策替代”与 local_autonomy 不是同义词；不得把政策研究自动写成代表沖縄整体的自治立场。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '建议补读具体提言或专题页；当前首页不足以冻结精确 local_autonomy 边。'
    }
    AI159 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = '新外交イニシアティブ（ND）—anti_base 仅表示其官方站点持续承载沖縄／米军基地政策研究，并公开提出“不建设边野古新基地”的具体政策替代主张。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S032 官方首页把米军基地列为研究领域，并展示“辺野古問題をどう解決するか―新基地をつくらせないための提言”等组织政策输出。'
        missing_scope = '不确认 ND 反对全部基地、全部安全合作或所有时期的每项基地政策。'
        interpretation_limit = 'anti_base 仅按边野古新基地等具体政策主张解释；政策提言不等于工程停止、政府采纳或代表沖縄社会共识。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '事实可由官网直接支持，但须从笼统反基地标签收窄到具体边野古／新基地政策提言。'
    }
    AI223 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '宮古島地下水研究会—groundwater 表示该会持续从事宫古岛地下水研究、监测、水源保护区域与条例／行政倡议。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S269、S270 为研究会公开材料，S271 为宫古岛市对研究会见解的正式回答，共同闭合研究、风险表达和行政倡议。'
        missing_scope = '不确认研究会提出的所有污染风险已经发生，也不确认污染源、健康因果或政府采纳全部提案。'
        interpretation_limit = '记录的是组织研究／倡议功能和风险主张；行政往返不等于正式合作、共同立场或已证污染事实。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '多项组织侧及行政侧材料直接支持 groundwater 核心定位。'
    }
    AI225 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '宮古島地下水研究会—life_safety 表示其把地下水作为饮用水源与“命之水”进行保护，并将水源安全纳入组织倡议。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S270 的水道水源保护提案与 S271 的市政府正式回应直接显示饮用水源保护和行政沟通。'
        missing_scope = '不确认已发生具体健康损害、疾病因果或研究会风险判断已获行政机关实体认可。'
        interpretation_limit = 'life_safety 仅指饮用水源与生活安全框架；风险表达不升级为已证健康损害或污染源认定。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '事实与既有有界表述一致，保留“未证明健康损害”边界。'
    }
    AI226 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '宮古島地下水研究会—environment 表示其持续开展地下水保全、井泉／水源调查、污染预防及与珊瑚礁生态相连的环境倡议。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S158 的团体概要、S204 的持续活动索引和 S270 的水源保护提案共同支持环境研究／倡议功能。'
        missing_scope = '不确认所有污染主张、生态影响或设施排水因果已经由独立监测或行政机关证实。'
        interpretation_limit = '组织研究与预防性倡议不等于污染事实、损害程度或政策效果；不得生成与行政机关的联盟关系。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '组织设立目的、持续活动与具体水源保护提案形成直接支持。'
    }
    AI232 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        approved_formulation = '全日本港湾労働組合沖縄地方本部—anti_base 表示该地方本部在 2015 年抗议集会中明确反对边野古新基地，并在 2025 年地方分支报告中记录基地议题现场学习与和平行进参与。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S286 直接点名沖縄地方本部并记录反对边野古新基地；S289 是地方分支 2025 年和平行进与基地问题学习报告。'
        missing_scope = '不支持原表所称 2015–2026 连续行动，也不确认其反对沖縄所有基地或全国本部实施相同行动。'
        interpretation_limit = '只归属沖縄地方本部／其具名分支的两个有日期行动；劳组地方行动不转嫁全国本部，共同行进不生成联盟。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '事实成立但时间连续性与“基地ない沖縄”表述超出来源；按最高直接来源由 E4 下调为 E3。'
    }
    AI233 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = '全日本港湾労働組合沖縄地方本部—anti_military 仅表示其在 2024 年反对美国海军军舰使用石垣／那霸民用港，并以罢工等方式介入该次港湾军事利用争议。'
        review_scope_final = 'event_specific'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S287 官方决议记录地方本部对军舰寄港及民用港军事利用的反对和罢工方针；S288 国会记录确认 2024 年石垣罢工及官方转述理由。'
        missing_scope = '不确认该地方本部对所有军队、全部日美演习或所有时期持一般性 anti_military 定位。'
        interpretation_limit = '严格限定 2024 年民用港军事利用／军舰寄港事件；不裁定罢工合法性、效果或更广泛政治立场。'
        scope_revision_required = 'yes'
        review_note = $notePrefix + '直接材料很强，但只闭合具体港湾事件；建议将 organizational_positioning 收窄为 event_specific。'
    }
    AI234 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        approved_formulation = '全日本港湾労働組合沖縄地方本部—peace 表示其在 2015 年反安保法案／新基地抗议及 2025 年 5·15 和平行进中有具名参与。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S286 闭合 2015 年地方本部抗议行动，S289 闭合 2025 年地方分支和平行进参与与基地问题学习。'
        missing_scope = '不支持“2024–2026 连续和平行进”，也不确认其在两个有证年份之外的持续频率或全部分支活动。'
        interpretation_limit = '以两个具日期的地方本部／分支行动为限；活动参与不证明政策效果、联盟或全国本部同等行动。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '删除来源不能支持的 2024–2026 连续性，按 S286/S289 上限由 E4 下调为 E3。'
    }
    AI236 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = '全日本港湾労働組合沖縄地方本部—mobilization 表示现有材料记录其在 2015、2024、2025 年分别采用抗议集会、港湾罢工和和平行进等行动方式。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S286、S288、S289 分别闭合抗议集会、石垣港罢工及 5·15 和平行进等有日期行动。'
        missing_scope = '不确认完整行动清单、年度连续性、动员规模准确性、组织能力强弱或行动效果。'
        interpretation_limit = '这里只编码可观察的重复行动 repertoire；不同事件不得合并为稳定联盟、统一运动组织或因果链。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '三类有日期行动足以支持有界 repertoire，但删除“年度”或完整连续性的暗示。'
    }
    AI237 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '新日本婦人の会沖縄県本部—women 表示其作为全国女性会员组织的新日本婦人の会之沖縄县本部，以女性会员和县本部—支部—班结构开展地方活动。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S280 官方组织介绍确认女性组织及都道府县本部结构；S282、S283 独立点名沖縄県本部的地方行动。'
        missing_scope = '不确认全部沖縄女性由该会代表，也不把中央本部每项声明或其他县本部行动转移给 A115。'
        interpretation_limit = '母体组织结构可支持地方本部身份，不支持分支间行动转嫁、党派隶属或全部成员意见一致。'
        scope_revision_required = 'no'
        review_note = $notePrefix + '全国组织结构与两个地方具名记录共同闭合 women 核心组织属性。'
    }
    AI240 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = '新日本婦人の会沖縄県本部—anti_base 表示其在 2014 年由县本部会员开展反对边野古新基地行动，并在 2018 年由沖縄県本部启动边野古县民投票条例签名动员。'
        review_scope_final = 'organizational_positioning'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S254 中央本部官方谈话明确归因沖縄県本部会员的反新基地行动；S283 精确点名沖縄県本部的边野古县民投票签名行动。'
        missing_scope = '不确认全国本部的全部反基地行动属于 A115，也不支持 2014、2018 以外所有时期或所有基地的一般立场。'
        interpretation_limit = '仅使用明确归因地方本部的材料；共同动员不生成党派隶属、稳定联盟、选举因果或政策效果。'
        scope_revision_required = 'no'
        review_note = $notePrefix + 'S254 虽为中央本部页面但明确点名沖縄県本部会员，S283 再以地方行动独立闭合；保留母体／分支边界。'
    }
}

$identityRows = Import-Csv -LiteralPath $identityPath
foreach ($row in $identityRows) {
    if (-not $identityDecisions.ContainsKey($row.actor_id)) {
        throw "No identity decision prepared for $($row.actor_id)"
    }
    $decision = $identityDecisions[$row.actor_id]
    foreach ($field in @(
        'human_decision',
        'revised_review_status',
        'evidence_level_final',
        'canonical_name_final',
        'actor_class_final',
        'origin_type_final',
        'legal_status_final',
        'approved_identity_formulation',
        'identity_interpretation_limit',
        'review_note'
    )) {
        $row.$field = $decision[$field]
    }
    $row.reviewed_fields = $identityReviewedFields
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate
}
$identityRows | Export-Csv -LiteralPath $identityPath -NoTypeInformation -Encoding utf8 -UseQuotes AsNeeded

$edgeRows = Import-Csv -LiteralPath $edgePath
foreach ($row in $edgeRows) {
    if (-not $edgeDecisions.ContainsKey($row.edge_id)) {
        throw "No edge decision prepared for $($row.edge_id)"
    }
    $decision = $edgeDecisions[$row.edge_id]
    foreach ($field in @(
        'human_decision',
        'revised_review_status',
        'evidence_level_final',
        'approved_formulation',
        'review_scope_final',
        'claim_status',
        'confirmed_scope',
        'missing_scope',
        'interpretation_limit',
        'scope_revision_required',
        'review_note'
    )) {
        $row.$field = $decision[$field]
    }
    $row.reviewed_fields = $edgeReviewedFields
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate
}

# AI044 originally cited S024, which belongs to A017's project and is therefore
# an actor/source mismatch. Replace it with S023, the archived local report that
# directly names A018 and states its Taiwan-contingency framing.
$sourceRows = Import-Csv -LiteralPath $sourceLogPath
$s023 = $sourceRows | Where-Object source_id -eq 'S023' | Select-Object -First 1
if (-not $s023) {
    throw 'S023 is missing from the source log'
}
$s023MetadataPath = Join-Path $root 'source_docs/source_archive/S023/metadata.json'
$s023Metadata = Get-Content -Raw -LiteralPath $s023MetadataPath | ConvertFrom-Json
$ai044 = $edgeRows | Where-Object edge_id -eq 'AI044' | Select-Object -First 1
$ai044.source_ref = 'S023'
$ai044.source_titles = "S023 $($s023.title)"
$ai044.source_urls = $s023.url
$ai044.source_archive_paths = $s023Metadata.local_path
$ai044.source_archive_statuses = "S023:$($s023Metadata.archive_status)"

$edgeRows | Export-Csv -LiteralPath $edgePath -NoTypeInformation -Encoding utf8 -UseQuotes AsNeeded

$bundleRows = @(Import-Csv -LiteralPath $bundlePath)
$bundleRows = @($bundleRows | Where-Object {
    -not ($_.review_item_id -eq 'HR035-B02-AI044' -and $_.item_type -eq 'edge_fact')
})
$bundleRows += [pscustomobject][ordered]@{
    review_item_id = 'HR035-B02-AI044'
    item_type = 'edge_fact'
    edge_id = 'AI044'
    actor_id = 'A018'
    source_id = 'S023'
    source_title = $s023.title
    source_url = $s023.url
    source_type = $s023.source_type
    source_year = $s023.year
    source_evidence_level = $s023.evidence_level
    source_review_status = $s023.review_status
    what_it_supports = $s023.what_it_supports
    support_scope = $s023.support_scope
    locator = $s023.locator
    archive_status = $s023Metadata.archive_status
    local_path = $s023Metadata.local_path
}
$bundleRows | Sort-Object review_item_id, item_type, source_id |
    Export-Csv -LiteralPath $bundlePath -NoTypeInformation -Encoding utf8 -UseQuotes AsNeeded

$identityCounts = $identityRows | Group-Object human_decision | Sort-Object Name
$edgeCounts = $edgeRows | Group-Object human_decision | Sort-Object Name

Write-Output "Updated $($identityRows.Count) identity rows and $($edgeRows.Count) edge rows."
Write-Output ("Identity decisions: " + (($identityCounts | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ', '))
Write-Output ("Edge decisions: " + (($edgeCounts | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ', '))
Write-Output "Reviewer marker: $reviewer"
