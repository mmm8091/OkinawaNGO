param(
    [switch]$ConfirmPrincipal
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$taskPath = Join-Path $root 'outputs/actor_issue_claim_freeze_v1/HR035_actor_issue_fact_review_batch01_v1.csv'
$bundlePath = Join-Path $root 'outputs/actor_issue_claim_freeze_v1/HR035_source_bundle_batch01_v1.csv'
$sourceLogPath = Join-Path $root 'data/interim/05_source_log_initial_v0.csv'

$sourceIdsByEdge = [ordered]@{
    AI021 = @('S009', 'S128')
    AI025 = @('S018', 'S019')
    AI027 = @('S018', 'S019')
    AI048 = @('S061', 'S128', 'S142')
    AI049 = @('S006', 'S007')
    AI050 = @('S061', 'S128', 'S006', 'S007')
    AI106 = @('S128', 'S129')
    AI126 = @('S185', 'S025')
    AI127 = @('S185', 'S025')
    AI129 = @('S026')
    AI132 = @('S027')
    AI164 = @('S192', 'S042')
    AI178 = @('S047')
    AI231 = @('S273', 'S274')
    AI241 = @('S283')
}

$commonReviewedFields = 'relation_existence;actor_identity;issue_mapping;source_ref;evidence_level;interpretation_boundary'
$reviewer = if ($ConfirmPrincipal) { 'project_principal_user' } else { 'AI_assist_pending_principal_confirmation' }
$reviewDate = if ($ConfirmPrincipal) { '2026-07-20' } else { '' }
$pendingPrefix = if ($ConfirmPrincipal) { '项目负责人确认 AI 辅助建议；' } else { 'AI辅助建议，待项目负责人确认；' }

$decisions = @{
    AI021 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'Earthjustice 的 international_advocacy 边只表示其作为冲绳儒艮案原告方 counsel，将边野古／儒艮争议带入美国联邦司法程序。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = '第九巡回法院判决列明 Earthjustice 律师代表原告上诉人；S009 记录其跨境法律倡议。'
        missing_scope = '不确认 Earthjustice 是具名原告，也不确认其全部国际倡议或全部冲绳活动。'
        interpretation_limit = 'counsel 与 plaintiff 严格分开；案件代理不生成稳定联盟，不证明胜诉、停工或项目改变。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '补入 S128 官方判决的 counsel 列示；S009 保留为组织侧法律／国际渠道说明。'
    }
    AI025 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E3'
        approved_formulation = '石垣市住民投票を求める会是石垣陆自部署住民投票条例签名、直接请求及议会处理过程中的具名请求／推动组织。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S018、S019 点名该会、代表、签名提交和住民投票条例程序。'
        missing_scope = '不确认该会代表全市多数、实际投票结果、诉讼原告身份或无限期组织定位。'
        interpretation_limit = 'requester／campaign body 不等于诉讼 plaintiff；不推断政策因果或稳定联盟。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '事实成立；最高直接支持为地方新闻 E3，故不沿用当前 E4。'
    }
    AI027 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E3'
        approved_formulation = 'A011—anti_military 仅标记该会介入石垣陆自部署这一具体军事设施争议，并以住民投票直接请求推进市民表决。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S018、S019 明确住民投票对象为平得大俣地区陆上自卫队部署，并点名 A011 的请求／推动角色。'
        missing_scope = '未证明 A011 对所有基地、自卫队或安全政策持一般性、长期反军事立场。'
        interpretation_limit = 'anti_military 在此是特定部署争议对象标签；与 AI025 属同一程序链，不重复计为独立行动。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '接受的是具体部署争议介入，不是一般反军事组织定位；证据等级按 S018 的 E3 冻结。'
    }
    AI048 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'JELF 的 legal 边按案件分列：冲绳儒艮案为具名组织原告／上诉人；泡濑公金支出诉讼仅为 supporter／正式材料承载者。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S061、S128 支持儒艮案 plaintiff／appellant；S142 及 HR-014 角色表支持泡濑 supporter／host。'
        missing_scope = '不确认 JELF 在泡濑案是具名 plaintiff 或 counsel，也不把律师组织身份自动转移到其他案件。'
        interpretation_limit = '逐案固定角色；原告、律师、supporter／host 严格分开；不推断稳定联盟或统一胜败。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '原 S006/S007 只支撑 2020 MMC 事件，不能承担 legal 边；改用 S061、S128、S142。'
    }
    AI049 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E4'
        approved_formulation = 'JELF—biodiversity 仅表示其作为 2020 年 OEJP／MMC 冲绳儒艮请求与公民社会报告的公开参与者。'
        review_scope_final = 'event_specific'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S006 的 71 团体请求／报告名单及 S007 的事件叙述闭合 JELF 在该次生物多样性／儒艮语境中的参与。'
        missing_scope = '不支持 JELF 的一般、长期 biodiversity 组织定位，也不证明其参与所有相关活动。'
        interpretation_limit = '一次共同请求／报告参与不生成稳定联盟、成员关系、持续协调或影响效果。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '仅接受 2020 MMC 事件边界；S006 为行动发起方的一手事件记录。'
    }
    AI050 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'JELF—dugong 包含两条分开的具名事实：冲绳儒艮案组织原告／上诉人角色，以及 2020 年 MMC 儒艮请求／报告参与。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S061、S128 支持诉讼 plaintiff／appellant；S006、S007 支持 2020 MMC 事件参与。'
        missing_scope = '不确认两次行动之间存在持续协调、同一联盟或其他年份的连续活动。'
        interpretation_limit = '诉讼与共同请求分开记录；共同出现不等于稳定联盟，案件结果不等于工程停止。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '原来源只覆盖 MMC 事件；补入 S061、S128 才能支撑已批的主要诉讼角色。'
    }
    AI106 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'Center for Biological Diversity 的 legal 边严格表示其在冲绳儒艮案中的具名组织原告／上诉人角色。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S128、S129 第九巡回法院判决 caption 均列 CBD 为 Plaintiffs-Appellants。'
        missing_scope = 'S004 共同声明不支持该法律角色；不确认 CBD 在其他冲绳案件中的角色。'
        interpretation_limit = '具名原告／上诉人不等于 counsel；2017 年发回和 2020 年终局不得概括为停工或项目改变。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '已目视核验 S128 判决首页 caption；以 S128、S129 替换错位的 S004。'
    }
    AI126 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = '「辺野古」県民投票の会—Henoko 仅表示该会在 2018–2019 年推动以边野古填海／基地建设为问题对象的县民投票。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S185 点名该会代表、副代表和请求代表身份并明确条例题目；S025 确认投票问题与结果；LC001 记录 2019-03-26 解散。'
        missing_scope = '不确认解散后的组织连续性、后续个人行动归属或所有签名者的组织成员身份。'
        interpretation_limit = '仅限 2018–2019 程序期；投票结果不证明组织造成结果，解散后行动不得归给 A051。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + 'S025 只证明投票本身，补入 S185 闭合精确 actor—程序映射；生命周期边界继承 LC001。'
    }
    AI127 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = 'A051—local_autonomy 仅表示该会通过条例制定直接请求与县民投票程序表达对边野古问题的地方直接民主／自治诉求。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S185 闭合 A051 与条例制定请求代表／县议会听证角色，S025 闭合正式投票；LC001 记录解散。'
        missing_scope = '不支持 A051 对所有地方自治议题的长期定位，也不证明其代表全体冲绳居民。'
        interpretation_limit = '仅限 2018–2019 直接请求／投票程序；不从程序参与推断政策因果、联盟或解散后连续性。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '原 S025 无法单独识别 A051，补入 S185；地方自治含义限定为该次制度程序。'
    }
    AI129 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E3'
        approved_formulation = '嘉手納基地爆音差止訴訟原告団—life_safety 表示嘉手纳噪音诉讼中睡眠、健康风险、人格权与日常生活损害主张。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S026 报道第三次诉讼的居民原告、噪音损害、睡眠妨害、部分健康风险认定及损害赔偿。'
        missing_scope = '不证明各轮原告成员相同，也不证明飞行停止、噪音消除或全部健康因果。'
        interpretation_limit = '限定各轮诉讼；部分损害／风险认定和赔偿不得写成运行禁令或全面健康因果。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '事实成立，但 S026 是新闻而非法院原文，证据等级由 E4 下调为 E3。'
    }
    AI132 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E3'
        approved_formulation = '普天間基地爆音訴訟団—life_safety 表示普天间噪音诉讼中人格权、夜间早晨噪音和居民日常生活损害主张。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S027 报道第二次诉讼的周边居民原告、人格权侵害主张、损害赔偿与差止请求被驳回。'
        missing_scope = '不证明各轮原告成员相同，也不证明飞行停止、噪音消除或其他轮次全部事实。'
        interpretation_limit = '限定各轮诉讼；部分赔偿不等于禁令、运行停止或全部诉求获支持。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '事实成立，但 S027 是新闻而非法院原文，证据等级由 E4 下调为 E3。'
    }
    AI164 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E3'
        approved_formulation = 'A068—anti_base 仅表示「ヘリポート基地建設の是非を問う名護市民投票推進協議会」在 1997 年海上直升机基地争议中组织条例直接请求、签名和市民投票推动，并处于反对基地建设的事件语境。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S192 闭合事件期组织名、代表、证明、签名、直接请求、条例和投票程序；S042 闭合公投与反对票多数。'
        missing_scope = '官方材料不足以把 A068 写成 1997 年后持续组织；A068→A019 的发展性改组／后继关系仍须单列谱系事实，不直接合并。'
        interpretation_limit = '活动期限定 1997 年；公投结果不等于组织造成结果，后继组织的后续行动不回填给 A068。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '以正式全称冻结 actor 单位并补入 S192；程序角色为 E4，但精确反基地立场与谱系边界只能保守到 E3。'
    }
    AI178 = @{
        human_decision = 'reject'
        revised_review_status = 'rejected'
        evidence_level_final = 'E4'
        approved_formulation = '不建立 A075—anti_base 事实边；沖縄防衛局应在工程实施者、行政程序 actor 或争议对象层编码。'
        review_scope_final = 'excluded_wrong_polarity'
        claim_status = 'unsupported'
        confirmed_scope = 'S047 只确认沖縄防衛局承载普天间替代设施建设环境影响评价等实施／行政角色。'
        missing_scope = '没有证据表明沖縄防衛局持反基地立场。'
        interpretation_limit = '争议对象、工程实施者或行政端点不等于反对该工程；可迁入程序／target 层，但不得进入无 polarity／role 的立场网络。'
        scope_revision_required = 'yes'
        review_note = $pendingPrefix + '该映射本身制造错误政治立场；HR-019 scope 若保留 implementer_or_target 语义，应迁出 actor–issue 立场边。'
    }
    AI231 = @{
        human_decision = 'revise'
        revised_review_status = 'human_revised'
        evidence_level_final = 'E4'
        approved_formulation = '宜野湾ちゅら水会—legal 当前可冻结到 2022 年 PFAS 血液检查请愿、委员会参考人陈述及相关市议会程序。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S273 点名该会参考人并记录请愿内容；S274 官方意见书点名该会采样及市议会制度输出。'
        missing_scope = '现有 S273/S274 不支持 2025–2026 公害调停申请、审查及程序性驳回；该阶段须另行登记、归档来源后再冻结。'
        interpretation_limit = '只表示 petition／formal-procedure user，不是一般法律组织；不推断 PFAS 因果、污染源、实体胜败或程序效果。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '不否定后续调停事实，但本批现有中央来源只闭合 2022 请愿，故缩窄已证时间范围。'
    }
    AI241 = @{
        human_decision = 'accept'
        revised_review_status = 'human_checked'
        evidence_level_final = 'E3'
        approved_formulation = '新日本婦人の会沖縄県本部—referendum 仅表示冲绳县本部在 2018 年启动边野古县民投票条例签名动员。'
        review_scope_final = 'institutional_or_case_role'
        claim_status = 'supported_bounded'
        confirmed_scope = 'S283 精确点名沖縄県本部、行动日期、边野古县民投票条例对象及签名动员。'
        missing_scope = '不确认全国本部实施该行动，也不支持 2018–2019 以外的持续县民投票角色。'
        interpretation_limit = '分支行动不转移给全国组织；共同动员不生成党派隶属、稳定联盟或政策效果。'
        scope_revision_required = 'no'
        review_note = $pendingPrefix + '事件事实成立；S283 为党报新闻，按 E3 冻结并保留分支／母体边界。'
    }
}

$sourceRows = Import-Csv -LiteralPath $sourceLogPath
$sourceIndex = @{}
foreach ($source in $sourceRows) {
    $sourceIndex[$source.source_id] = $source
}

function Get-ArchiveMetadata {
    param([string]$SourceId)
    $metadataPath = Join-Path $root "source_docs/source_archive/$SourceId/metadata.json"
    if (-not (Test-Path -LiteralPath $metadataPath)) {
        throw "Missing archive metadata for $SourceId"
    }
    return Get-Content -Raw -LiteralPath $metadataPath | ConvertFrom-Json
}

$taskRows = Import-Csv -LiteralPath $taskPath
foreach ($row in $taskRows) {
    if (-not $decisions.ContainsKey($row.edge_id)) {
        throw "No decision prepared for $($row.edge_id)"
    }
    $decision = $decisions[$row.edge_id]
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
    $row.reviewed_fields = $commonReviewedFields
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate

    $ids = $sourceIdsByEdge[$row.edge_id]
    $sources = @($ids | ForEach-Object {
        if (-not $sourceIndex.ContainsKey($_)) {
            throw "Unknown source id $_ for $($row.edge_id)"
        }
        $sourceIndex[$_]
    })
    $metadata = @($ids | ForEach-Object { Get-ArchiveMetadata -SourceId $_ })
    $row.source_ref = $ids -join ';'
    $row.source_titles = (($sources | ForEach-Object { "$($_.source_id) $($_.title)" }) -join ' || ')
    $row.source_urls = (($sources | ForEach-Object { $_.url }) -join ' || ')
    $row.source_archive_paths = (($metadata | ForEach-Object { $_.local_path }) -join ' || ')
    $row.source_archive_statuses = (($metadata | ForEach-Object { "$($_.source_id):$($_.archive_status)" }) -join ' || ')
}

$taskRows | Export-Csv -LiteralPath $taskPath -NoTypeInformation -Encoding utf8 -UseQuotes AsNeeded

$reviewItemByEdge = @{}
foreach ($row in $taskRows) {
    $reviewItemByEdge[$row.edge_id] = $row.review_item_id
}

$bundleRows = foreach ($edgeId in $sourceIdsByEdge.Keys) {
    foreach ($sourceId in $sourceIdsByEdge[$edgeId]) {
        $source = $sourceIndex[$sourceId]
        $metadata = Get-ArchiveMetadata -SourceId $sourceId
        [pscustomobject][ordered]@{
            review_item_id = $reviewItemByEdge[$edgeId]
            edge_id = $edgeId
            source_id = $sourceId
            source_title = $source.title
            source_url = $source.url
            source_type = $source.source_type
            source_year = $source.year
            source_evidence_level = $source.evidence_level
            source_review_status = $source.review_status
            what_it_supports = $source.what_it_supports
            support_scope = $source.support_scope
            locator = $source.locator
            archive_status = $metadata.archive_status
            local_path = $metadata.local_path
        }
    }
}

$bundleRows | Export-Csv -LiteralPath $bundlePath -NoTypeInformation -Encoding utf8 -UseQuotes AsNeeded

Write-Output "Updated $($taskRows.Count) HR-035 task rows and $($bundleRows.Count) source-bundle rows."
