$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$reviewer = 'ai_assist_pending_principal'
$reviewDate = '2026-07-20'

function Write-CsvUtf8 {
    param(
        [Parameter(Mandatory = $true)] [object[]] $Rows,
        [Parameter(Mandatory = $true)] [string] $Path
    )
    $Rows | Export-Csv -LiteralPath $Path -NoTypeInformation -Encoding utf8
}

function Escape-MarkdownCell {
    param([AllowNull()] [string] $Text)
    if ($null -eq $Text) {
        return ''
    }
    return (($Text -replace '\r?\n', ' ') -replace '\|', '\|').Trim()
}

function Add-MarkdownTable {
    param(
        [Parameter(Mandatory = $true)] [string[]] $Headers,
        [Parameter(Mandatory = $true)] [object[]] $Rows,
        [Parameter(Mandatory = $true)] [scriptblock] $Selector
    )
    $script:masterLines.Add('| ' + ($Headers -join ' | ') + ' |')
    $script:masterLines.Add('| ' + (($Headers | ForEach-Object { '---' }) -join ' | ') + ' |')
    foreach ($row in $Rows) {
        $values = & $Selector $row
        $escaped = $values | ForEach-Object { Escape-MarkdownCell ([string] $_) }
        $script:masterLines.Add('| ' + ($escaped -join ' | ') + ' |')
    }
}

# HR-010 batch 6: 46 accept, one defer after targeted source checking.
$hr010Path = 'outputs/edge_activation_v1/post_hr013_HR010_batch6_edge_evidence_addendum_v1.csv'
$hr010 = @(Import-Csv -LiteralPath $hr010Path)
foreach ($row in $hr010) {
    if ($row.task_id -eq 'HR010-B6-019') {
        $row.decision = 'defer'
        $row.review_note = 'AI辅助建议：公开主页可分别确认边野古行动与一般地方自治议题，但未找到把“边野古问题”与“地方自治权”直接连接起来的同一条公开材料；详细内容在会员区，暂 defer。'
    }
    else {
        $row.decision = 'accept'
        $row.review_note = 'AI辅助建议：来源直接支持该 actor—issue 映射，按现有 scope 与 explanation_boundary 冻结；不批准联盟、资金、因果或未写明的持续性。'
    }
    $row.reviewer = $reviewer
    $row.review_date = $reviewDate
}
Write-CsvUtf8 -Rows $hr010 -Path $hr010Path

# Lifecycle cases: keep status semantics separate from workflow/review status.
$lifecyclePath = 'outputs/actor_lifecycle_v1/actor_lifecycle_review_queue_v0.csv'
$lifecycle = @(Import-Csv -LiteralPath $lifecyclePath)
$lifecycleRecommendations = @{
    'LCR001' = @{
        decision = 'accept_status'
        note = 'AI辅助建议：确认 dissolved，status_date=2024-11-27；仅以 S182/OTV 对解散日的明确报道为依据，不使用 S051，也不把解散后的行动回填给 A011。'
    }
    'LCR002' = @{
        decision = 'revise_status'
        note = 'AI辅助建议：规范名已应为“ヘリポート基地建設の是非を問う名護市民投票推進協議会”；生命周期改为 reorganized，以 1997-10-18 作为后继 A019 成立/重组边界，不声称这是 A068 精确解散决议日，不合并两个 actor。'
    }
    'LCR003' = @{
        decision = 'revise_status'
        note = 'AI辅助建议：保留 continuity_unverified，但把 last_observed_activity_date 更新为 2023-06-01；该日媒体仍以“南西諸島ピースネット共同代表”标识发言者，只支持至少到该日的组织名义活动，不推断延续至今。'
    }
    'LCR004' = @{
        decision = 'revise_status'
        note = 'AI辅助建议：保留 continuity_unverified，但把 last_observed_activity_date 更新为 2015-06-22；2016年官方资料载录的是2015年请愿，不把文档发布日期当作2016年新活动，也不推断解散或当前活跃。'
    }
}
foreach ($row in $lifecycle) {
    $rec = $lifecycleRecommendations[$row.review_id]
    if ($null -eq $rec) {
        throw "Missing lifecycle recommendation for $($row.review_id)"
    }
    $row.decision = $rec.decision
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate
    $row.review_notes = $rec.note
}
Write-CsvUtf8 -Rows $lifecycle -Path $lifecyclePath

# HR-034: legacy strings are not proof of a row-level human decision.
$hr034Path = 'outputs/review_status_crosswalk_v1/HR034_review_status_crosswalk_v1.csv'
$hr034 = @(Import-Csv -LiteralPath $hr034Path)
foreach ($row in $hr034) {
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate

    if ($row.object_id -eq 'S051') {
        $row.decision = 'reject'
        $row.revised_review_status = 'rejected'
        $row.review_note = 'AI辅助建议：归档内容与目标组织不符，且已是 E0 rejected_archive_mismatch；统一为 rejected，不得支持 A011。'
        continue
    }

    $row.decision = 'revise'
    $row.revised_review_status = 'ai_seeded'

    switch ($row.object_id) {
        'AI068' {
            $row.review_note = 'AI辅助建议：HR-019只批准了默认叙事排除等 scope 处理，actor—issue claim 本身没有逐行人审决定；review_status 仍归 ai_seeded，并继续排除于默认冲绳叙事。'
        }
        'TABLE_R4_QA_SAFE_ONLINE' {
            $row.review_note = 'AI辅助建议：把 qa_safe_online 移至独立 qa_usability_status；法定 review_status 默认 ai_seeded，只有逐行存在 reviewer/decision 的记录才升级。'
        }
        'TABLE_R9_ACCEPTED' {
            $row.review_note = 'AI辅助建议：把 accepted 移至 formal_inclusion_status；法定 review_status 默认 ai_seeded，仅对有明确 HR-017 逐行决定的记录传播 human_checked/human_revised，不能整表批量标人审。'
        }
        'TABLE_HET_ACCEPTED' {
            $row.review_note = 'AI辅助建议：把 accepted 移至 derivation_or_formal_inclusion_status；review_status 由具体上游 R9 行机械继承，不重复做49次语义人审，也不整表标人审。'
        }
        'TABLE_LIFECYCLE_WORKFLOW_STATUS' {
            $row.review_note = 'AI辅助建议：另建 lifecycle_workflow_status 承载工作流字符串；法定 review_status 默认 ai_seeded，LCR 的实体生命周期结论不能直接充当 review_status。'
        }
        default {
            $row.review_note = 'AI辅助建议：旧值只表示可用性/校验状态，缺少逐行 reviewer、decision 与 date；规范为 ai_seeded。来源入库不批准 actor、edge、联盟、资金、金额、因果或解释。'
        }
    }
}
Write-CsvUtf8 -Rows $hr034 -Path $hr034Path

# HR-029: freeze current vocabulary conservatively; revised values remain in review notes.
$hr029Path = 'outputs/schema_alias_freeze_v1/HR029_schema_alias_freeze_review_v0.csv'
$hr029 = @(Import-Csv -LiteralPath $hr029Path)
$hr029RevisionNotes = @{
    'HR029-016' = 'AI辅助建议：revise；保留 canonical“辺野古の海を土砂で埋めるな！首都圏連絡会”，把“首都圏キャンペーン”记为 documented_name_variant（站点标题变体），不建第二实体。'
    'HR029-020' = 'AI辅助建议：revise 为 name=Futenma Air Station|type=base_site|parent=P018|aliases=Futenma;MCAS Futenma;普天間飛行場;普天間基地。P018 是宜野湾市，只表示空间父级。'
    'HR029-022' = 'AI辅助建议：revise 为 name=Yonaguni Town|type=municipality|parent=P001|aliases=Yonaguni;Yonaguni Town;与那国町；删除岛屿别名“与那国島”，岛与町不得混同。'
    'HR029-023' = 'AI辅助建议：revise 为 name=Ishigaki City|type=municipality|parent=P001|aliases=Ishigaki;Ishigaki City;石垣市；删除岛屿别名“石垣島”。'
    'HR029-024' = 'AI辅助建议：revise 为 name=Miyakojima City|type=municipality|parent=P001|aliases=Miyako;Miyakojima City;宮古島市；删除岛屿别名“宮古島”。'
    'HR029-026' = 'AI辅助建议：revise 为 no_applicable_venue；umbrella membership 是组织关系，不是发生场所。'
    'HR029-027' = 'AI辅助建议：revise 为 no_applicable_venue；umbrella membership 是组织关系，不是发生场所。'
    'HR029-028' = 'AI辅助建议：revise 为 no_applicable_venue；umbrella membership 是组织关系，不是发生场所。'
    'HR029-029' = 'AI辅助建议：revise 为 no_applicable_venue；umbrella membership 是组织关系，不是发生场所。'
    'HR029-030' = 'AI辅助建议：revise 为 no_applicable_venue；把 public-diplomacy program channel 放在 entry_mode，不创造场所节点，且 NOFO/机会不等于获资助。'
    'HR029-037' = 'AI辅助建议：revise 为 V011（national ministry or agency administrative channel）；JICA 是行政机构渠道，不是国际合作活动场所。'
    'HR029-043' = 'AI辅助建议：revise 为 no_applicable_venue；regional sponsor perimeter 是关系语境，不是冲绳项目现场。'
    'HR029-033' = 'AI辅助建议：revise 为 donation；F025 是具名 KOSC→AWWA 捐助关系，金额未知，不能编码成 aggregate，也不得把 USD 102,000 挂到该边。'
}
foreach ($row in $hr029) {
    $row.human_reviewer = $reviewer
    $row.review_date = $reviewDate
    if ($hr029RevisionNotes.ContainsKey($row.review_item_id)) {
        $row.decision = 'revise'
        $row.review_note = $hr029RevisionNotes[$row.review_item_id]
    }
    else {
        $row.decision = 'accept'
        switch ($row.domain) {
            'actor_field' {
                $row.review_note = 'AI辅助建议：接受 proposed_value；组织类型保持小词表，所有工会及工会联合体统一为 labor_union。'
            }
            'alias' {
                $row.review_note = 'AI辅助建议：接受 proposed_value；该标签仅说明名称关系，不合并 actor，不跨案件轮次回填行动。'
            }
            'place_semantics' {
                $row.review_note = 'AI辅助建议：接受 proposed_value；父级只表示行政/空间层级，不表示组织关系。'
            }
            'venue_reference' {
                $row.review_note = 'AI辅助建议：接受 proposed_value；venue 只表示可观察的制度/活动入口，不证明资金、联盟或政策效果。'
            }
            'relation_type' {
                $row.review_note = 'AI辅助建议：接受 proposed_value；只冻结关系语义，不提升证据等级，也不把共现写成联盟。'
            }
            default {
                $row.review_note = 'AI辅助建议：接受 proposed_value，并保留 required_boundary。'
            }
        }
    }
}
Write-CsvUtf8 -Rows $hr029 -Path $hr029Path

# HR-031: choose the conservative report-strength option in all three cases.
$hr031Path = 'outputs/report_claim_audit_v1/HR031_report_claim_review_v0.csv'
$hr031 = @(Import-Csv -LiteralPath $hr031Path)
$hr031Notes = @{
    'HR-031-01' = 'AI辅助建议选 B：写成“当前公开样本中的分析框架”，不写成已普遍成立的阶段性发现；可在具体人审案例中分别说明可观察转译。'
    'HR-031-02' = 'AI辅助建议选 B：只说当前公开材料呈现地点差异；没有统一抽样与当地材料，不能上升为显著地点依赖。'
    'HR-031-03' = 'AI辅助建议选 B：改成并列的可观察入口/角色；现有材料不支持从生态、法律到国际倡议的连续转换因果链。'
}
foreach ($row in $hr031) {
    $row.decision = 'B'
    $row.reviewer = $reviewer
    $row.review_date = $reviewDate
    $row.review_note = $hr031Notes[$row.review_item_id]
}
Write-CsvUtf8 -Rows $hr031 -Path $hr031Path

# One-pass principal review document.
$docPath = 'docs/principal_human_review_master_return_2026-07-20_v1.md'
$lines = [System.Collections.Generic.List[string]]::new()
$script:masterLines = $lines
$lines.Add('# 剩余在线人工复核总审核包（145条）')
$lines.Add('')
$lines.Add('- 生成日期：2026-07-20')
$lines.Add('- 状态：`AI辅助建议，待项目负责人逐条或整包确认`')
$lines.Add('- reviewer 标记：`ai_assist_pending_principal`（不是人审完成标记）')
$lines.Add('- 合并状态：未运行任何中央数据 merge；本文件和五张任务表只是待审返回包。')
$lines.Add('')
$lines.Add('## 一次性审核方式')
$lines.Add('')
$lines.Add('如果你接受全部建议，回复“确认全部145条”即可；如果只修改个别项，列出 ID 和新决定，例如 `HR029-033 改为 reject`。确认后再由下一线程把 reviewer 改成项目负责人、写正式 return 文档并执行相应 merge/重建。')
$lines.Add('')
$lines.Add('## 范围与计数')
$lines.Add('')
$lines.Add('| 任务 | 条数 | AI建议分布 |')
$lines.Add('| --- | ---: | --- |')
$lines.Add('| HR-010 batch 6 actor–issue 证据补充 | 47 | accept 46；defer 1 |')
$lines.Add('| LCR001–004 组织生命周期 | 4 | accept_status 1；revise_status 3 |')
$lines.Add('| HR-034 旧 review_status 交叉核查 | 50 | revise 49；reject 1 |')
$lines.Add('| HR-029 schema / alias freeze | 41 | accept 28；revise 13 |')
$lines.Add('| HR-031 报告主张强度 | 3 | B 3 |')
$lines.Add('| 合计 | 145 | 全部已填写为待确认建议 |')
$lines.Add('')
$lines.Add('本轮不包含12条必须依赖当地/馆藏/内部材料的任务：HR-017 本地项9条、HR-018 已标 `deferred_local_or_internal_record` 的2条、HR-024/A073 的1条。也不把尚未正式发出的后续 HR-035 批次虚构为现有任务。')
$lines.Add('')
$lines.Add('## 调查后需要你特别看的判断')
$lines.Add('')
$lines.Add('1. **HR010-B6-019**：自治劳主页能分别看到边野古行动和一般地方自治议题，但没有找到把两者直接连接起来的同一条公开材料，因此建议 `defer`，而不是凭主题邻近接受。')
$lines.Add('2. **LCR001 / A011**：[OTV 报道](https://www.otv.co.jp/okitive/news/post/00012171/index.html)明确记载组织于2024-11-27解散，建议接受 `dissolved`。')
$lines.Add('3. **LCR002 / A068**：[冲绳县官方年表 S192](https://www.pref.okinawa.jp/kititaisaku/DP-08-13.pdf)可确认1997年公投推进组织及后继反对直升机场基地组织的程序边界，但不能把后继组织当成同一 actor，也不能把后继成立日伪装成精确解散决议日。')
$lines.Add('4. **LCR003 / A065**：[冲绳时报2023-06-01报道](https://www.okinawatimes.co.jp/articles/-/1162100)仍使用“南西諸島ピースネット共同代表”这一组织身份，所以把最后可见活动更新到该日，但仍保持 `continuity_unverified`。')
$lines.Add('5. **LCR004 / A069**：[2015-02-12联合请求书](https://img03.ti-da.net/usr/h/e/n/henoko/2015-02-12%E8%BE%BA%E9%87%8E%E5%8F%A4%E5%9F%BA%E5%9C%B0%E5%BB%BA%E8%A8%AD%E3%81%AB%E4%BF%82%E3%82%8B%E5%9F%8B%E7%AB%8B%E5%9C%9F%E7%A0%82%E3%81%AE%E6%8E%A1%E5%8F%96%E5%80%99%E8%A3%9C%E5%9C%B0%E3%81%AE%E4%B8%AD%E6%AD%A2%E3%82%92%E6%B1%82%E3%82%81%E3%82%8B%E8%A6%81%E8%AB%8B%E6%9B%B8.pdf)和[冲绳县委员会资料](https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/017/050/45kaihouh28.pdf)支持至少到2015-06-22的组织名义活动；2016年文档只是载录2015年请愿。')
$lines.Add('6. **HR034**：`verified`、`human_verified`、`accepted`、`qa_safe_online` 等旧字符串不等于有 reviewer/decision/date 的逐行人审；因此除已知错档 S051 外，一律先归 `ai_seeded`，再由明确的人审记录逐行升级。')
$lines.Add('7. **HR029**：保持较小组织类型词表，工会联合体也统一为 `labor_union`；岛屿与市町别名分离；membership、NOFO 和 sponsor perimeter 不再硬塞进 venue。')
$lines.Add('8. **HR031**：三条都选保守的 B，不把当前样本升级成普遍机制、显著地点效应或连续转换因果链。')
$lines.Add('')

$lines.Add('## HR-010 batch 6：actor–issue 证据补充（47条）')
$lines.Add('')
Add-MarkdownTable -Headers @('ID', 'actor', 'issue', 'claim', 'sources', 'AI建议', '理由/边界') -Rows $hr010 -Selector {
    param($row)
    @($row.task_id, "$($row.actor_id) $($row.actor_name)", "$($row.issue_id) $($row.issue_label)", $row.claim, $row.source_keys, $row.decision, "$($row.review_note) 原边界：$($row.explanation_boundary)")
}
$lines.Add('')

$lines.Add('## LCR001–004：组织生命周期（4条）')
$lines.Add('')
Add-MarkdownTable -Headers @('ID', 'actor', '当前候选', '候选日期/最后活动', 'AI建议', '理由与修订值') -Rows $lifecycle -Selector {
    param($row)
    @($row.review_id, "$($row.actor_id) $($row.canonical_name)", $row.current_candidate_status, "status=$($row.status_date_candidate); last=$($row.last_observed_activity_date)", $row.decision, $row.review_notes)
}
$lines.Add('')

$lines.Add('## HR-034：旧 review_status 交叉核查（50条）')
$lines.Add('')
Add-MarkdownTable -Headers @('ID', '对象', '旧值', '影响行数', 'AI建议', '新 review_status', '理由/边界') -Rows $hr034 -Selector {
    param($row)
    @($row.review_item_id, "$($row.object_id) $($row.object_label)", $row.current_value, $row.affected_row_count, $row.decision, $row.revised_review_status, "$($row.review_note) 必守边界：$($row.required_boundary)")
}
$lines.Add('')

$lines.Add('## HR-029：schema / alias freeze（41条）')
$lines.Add('')
Add-MarkdownTable -Headers @('ID', 'domain', '对象/字段', '当前值', '原 proposed_value', 'AI建议', '理由或修订值') -Rows $hr029 -Selector {
    param($row)
    @($row.review_item_id, $row.domain, "$($row.object_id) $($row.object_name) / $($row.field_name)", $row.current_value, $row.proposed_value, $row.decision, "$($row.review_note) 必守边界：$($row.required_boundary)")
}
$lines.Add('')
$lines.Add('注意：HR-029 是当前快照上的语义决定。项目负责人确认并完成 HR-010/LCR/HR-034 的中央合并后，应重建 freeze 包，再机械对照这些决定；不能把当前快照直接当作最终 frozen schema。')
$lines.Add('')

$lines.Add('## HR-031：报告主张强度（3条）')
$lines.Add('')
Add-MarkdownTable -Headers @('ID', 'claims', '问题', '选项', 'AI建议', '理由') -Rows $hr031 -Selector {
    param($row)
    @($row.review_item_id, $row.claim_ids, $row.review_question, $row.decision_options, $row.decision, $row.review_note)
}
$lines.Add('')

$lines.Add('## 确认后的合并纪律')
$lines.Add('')
$lines.Add('1. 先把你确认的决定写入正式 human-return 文档，把 `ai_assist_pending_principal` 替换为项目负责人标记；未确认项保持待审。')
$lines.Add('2. 只运行与已确认任务对应的 merge / reconstruction；不要运行 AGENTS.md 列出的 pre-human 或历史 builder。')
$lines.Add('3. HR-010、LCR、HR-034 合并后重建 HR-029 freeze 快照并核对行数、ID 和 proposed_value 漂移，再冻结 schema。')
$lines.Add('4. HR-031 只控制报告措辞强度，不反向提升数据层证据等级。')
$lines.Add('5. 12条本地材料任务继续留在 ledger，不因本包“全确认”而自动关闭。')

Set-Content -LiteralPath $docPath -Value $lines -Encoding utf8

[pscustomobject]@{
    HR010 = $hr010.Count
    Lifecycle = $lifecycle.Count
    HR034 = $hr034.Count
    HR029 = $hr029.Count
    HR031 = $hr031.Count
    Total = $hr010.Count + $lifecycle.Count + $hr034.Count + $hr029.Count + $hr031.Count
    Document = $docPath
} | Format-List
