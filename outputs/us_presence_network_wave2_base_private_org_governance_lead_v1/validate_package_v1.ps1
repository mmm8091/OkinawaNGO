$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$errors = [System.Collections.Generic.List[string]]::new()

function Add-CheckError([string]$message) {
    $script:errors.Add($message)
}

function Require-File([string]$relativePath) {
    $path = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-CheckError "missing file: $relativePath"
    }
    return $path
}

$leadPath = Require-File 'unexpected_findings_register_v1.csv'
$sourcePath = Require-File 'source_receipts_v1.csv'
$regimePath = Require-File 'regime_governance_matrix_lead_only_v1.csv'
$actorPath = Require-File 'actor_regime_crosswalk_lead_only_v1.csv'
$negativePath = Require-File 'negative_search_log_v1.csv'
$manifestPath = Require-File 'local_artifact_manifest_v1.csv'
$readmePath = Require-File 'README.md'

if ($errors.Count -eq 0) {
    $leads = @(Import-Csv -LiteralPath $leadPath)
    $sources = @(Import-Csv -LiteralPath $sourcePath)
    $regimes = @(Import-Csv -LiteralPath $regimePath)
    $actors = @(Import-Csv -LiteralPath $actorPath)
    $negative = @(Import-Csv -LiteralPath $negativePath)
    $manifest = @(Import-Csv -LiteralPath $manifestPath)

    if ($leads.Count -ne 10) { Add-CheckError "expected 10 lead rows, got $($leads.Count)" }
    if (($leads | Measure-Object -Property recon_step -Maximum).Maximum -gt 3) { Add-CheckError 'recon_step exceeds 3' }
    if (($leads | Where-Object { $_.workflow_status -ne 'lead_only' -or $_.claim_eligibility -ne 'no' -or $_.central_writeback -ne 'no' -or $_.human_review_trigger -ne 'no' -or $_.publication_eligibility -ne 'no' }).Count -gt 0) {
        Add-CheckError 'lead isolation fields are not fixed to lead_only/no/no/no/no'
    }
    if (($leads | Where-Object { $_.record_kind -notin @('origin_observation','followup_observation') }).Count -gt 0) { Add-CheckError 'invalid record_kind' }

    $leadById = @{}
    foreach ($row in $leads) { $leadById[$row.lead_id] = $row }
    foreach ($row in $leads) {
        $step = [int]$row.recon_step
        if ($step -eq 0) {
            if ($row.record_kind -ne 'origin_observation' -or $row.parent_lead_id) { Add-CheckError "invalid origin row: $($row.lead_id)" }
        } else {
            if (-not $row.parent_lead_id -or -not $leadById.ContainsKey($row.parent_lead_id)) {
                Add-CheckError "missing parent for $($row.lead_id)"
            } else {
                $parent = $leadById[$row.parent_lead_id]
                if ($parent.chain_id -ne $row.chain_id) { Add-CheckError "cross-chain parent for $($row.lead_id)" }
                if ([int]$parent.recon_step -ne ($step - 1)) { Add-CheckError "non-sequential parent for $($row.lead_id)" }
            }
        }
    }

    if ($sources.Count -ne 10) { Add-CheckError "expected 10 source receipts, got $($sources.Count)" }
    if (($sources | Where-Object { $_.workflow_status -ne 'lead_only' -or $_.claim_eligibility -ne 'no' }).Count -gt 0) { Add-CheckError 'source receipt isolation fields failed' }
    if ($regimes.Count -ne 2) { Add-CheckError "expected 2 regime rows, got $($regimes.Count)" }
    if ($actors.Count -ne 7) { Add-CheckError "expected 7 actor crosswalk rows, got $($actors.Count)" }
    if ($negative.Count -ne 5) { Add-CheckError "expected 5 negative-search rows, got $($negative.Count)" }

    $mcipac = $regimes | Where-Object regime_id -eq 'BPG-RG01'
    $kadena = $regimes | Where-Object regime_id -eq 'BPG-RG02'
    if (-not $mcipac.facility_price_status.Contains('cost_recovery')) { Add-CheckError 'MCIPAC facility cost-recovery field missing' }
    if (-not $mcipac.organization_legal_position.Contains('not a NAFI')) { Add-CheckError 'MCIPAC non-NAFI field missing' }
    if (-not $mcipac.suspension_or_revocation_terms.Contains('revoke')) { Add-CheckError 'MCIPAC revocation field missing' }
    if (-not $kadena.facility_price_status.Contains('normal fees')) { Add-CheckError 'Kadena normal-fee field missing' }
    if (-not $kadena.debt_and_government_liability_terms.Contains('jointly and severally')) { Add-CheckError 'Kadena private debt field missing' }
    if (-not $kadena.suspension_or_revocation_terms.Contains('withdraw')) { Add-CheckError 'Kadena withdrawal field missing' }

    foreach ($item in $manifest) {
        $artifactPath = Join-Path (Split-Path -Parent (Split-Path -Parent $root)) $item.local_path
        if (-not (Test-Path -LiteralPath $artifactPath -PathType Leaf)) {
            Add-CheckError "missing artifact: $($item.local_path)"
            continue
        }
        $actualLength = (Get-Item -LiteralPath $artifactPath).Length
        $actualHash = (Get-FileHash -LiteralPath $artifactPath -Algorithm SHA256).Hash
        if ([int64]$item.byte_length -ne $actualLength) { Add-CheckError "length mismatch: $($item.artifact_id)" }
        if ($item.sha256.ToUpperInvariant() -ne $actualHash.ToUpperInvariant()) { Add-CheckError "hash mismatch: $($item.artifact_id)" }
        $bytes = [System.IO.File]::ReadAllBytes($artifactPath)
        $prefixLength = [Math]::Min(16, $bytes.Length)
        $prefix = [System.Text.Encoding]::ASCII.GetString($bytes[0..($prefixLength - 1)])
        if (-not $prefix.StartsWith($item.magic_check)) { Add-CheckError "magic mismatch: $($item.artifact_id)" }
    }

    $readme = Get-Content -LiteralPath $readmePath -Raw
    if (-not $readme.Contains('installation_authorization')) { Add-CheckError 'README missing typed authorization design implication' }
    if (-not $readme.Contains('real-estate license')) { Add-CheckError 'README missing facility-license boundary' }
    if (-not $readme.Contains('MCCS')) { Add-CheckError 'README missing MCCS boundary discussion' }
}

$result = [ordered]@{
    package = 'us_presence_network_wave2_base_private_org_governance_lead_v1'
    validated_at = (Get-Date).ToString('yyyy-MM-ddTHH:mm:ssK')
    status = if ($errors.Count -eq 0) { 'PASS' } else { 'FAIL' }
    counts = [ordered]@{
        unexpected_findings = if ($null -ne $leads) { $leads.Count } else { 0 }
        source_receipts = if ($null -ne $sources) { $sources.Count } else { 0 }
        governance_regimes = if ($null -ne $regimes) { $regimes.Count } else { 0 }
        actor_crosswalk_rows = if ($null -ne $actors) { $actors.Count } else { 0 }
        negative_searches = if ($null -ne $negative) { $negative.Count } else { 0 }
        local_artifacts = if ($null -ne $manifest) { $manifest.Count } else { 0 }
    }
    errors = @($errors)
}

$json = $result | ConvertTo-Json -Depth 5
$jsonLines = ($json -replace "`r`n", "`n").Split("`n") | ForEach-Object { $_.TrimEnd() }
$jsonLf = ($jsonLines -join "`n").TrimEnd("`r", "`n") + "`n"
[System.IO.File]::WriteAllText((Join-Path $root 'validation_report_v1.json'), $jsonLf, [System.Text.UTF8Encoding]::new($false))
$json

if ($errors.Count -gt 0) { exit 1 }
