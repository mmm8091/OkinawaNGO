# AGENTS.md

This repository supports the Okinawa NGO / civic organization network research project.

All agents should treat this file as the shared operating guide. Tool-specific files such as `CLAUDE.md` may mirror this guide, but this file is the general entry point.

## First Read

1. `docs/phase1_workbench.md` — current control document; must stay under 300 lines.
2. `data/metadata/coding_schema_v0.md` — field definitions and evidence levels.
3. `docs/progress_sync_assets_v0.md` — communication assets and current completion notes.
4. `outputs/module_completion_v0/README.md` — current R-module deliverables and MT task status.
5. `CONTEXT.md` — stable domain context.

## Hard Rules

- Do not treat candidate edges as final findings.
- Do not describe co-signing, joint statements, request letters, or shared event participation as stable alliances without additional evidence.
- Do not describe funding, sponsorship, commission, grant, public diplomacy, or institutional support as confirmed unless supported by official grants, awards, contracts, financial reports, organization reports, or equivalent primary records.
- Do not write grant opportunity / NOFO as awarded funding or a recipient relationship.
- Do not treat service organizations for U.S. military families as anti-base or pro-base actors by default. Code them by observed function.
- For Yonaguni, use the main framing of frontline/security environment, local autonomy, referendum, Taiwan proximity, and health/life-safety concerns. Do not force it into an environmental-obstruction frame.
- Human review, local retrieval, and human decision tasks belong in task books and logs, not scattered notes.
- Sensitive relationships require human review; do not do AI writing as AI review.

## Current Data Status

Updated: 2026-07-01.

- Actor registry: 93 actors.
- Source log: 92 sources, currently 76 real URLs, 14 `inferred_url` placeholders, and 2 non-URL references.
- Actor-issue candidate edges: 180.
- Actor-place candidate edges: 124.
- Funding/support sample edges: 27.
- Issue taxonomy: 19 issue categories.
- Place registry: 20 place/field nodes.
- Source archive: 74 `archived`, 2 `manual_archived`, 14 `skipped_inferred_url`, 2 `skipped_non_url_reference`, 0 `pending_archive`.

## Current Deliverables

- Explanatory graph package: `outputs/explanatory_v0/`
  - 5 PNG figures.
  - Main communication figures: place-issue matrix, Henoko/Oura Bay internationalization pathway, actor-issue bridge network.
- Module completion package: `outputs/module_completion_v0/`
  - Covers R2, R3/R4, R5, R11, and R14.
  - R5 now includes the full 2020 OEJP/MMC 71-group participant extraction.
  - `next_module_investigation_tasks_v0.csv` tracks MT tasks and completion status.
- Source archive: `source_docs/source_archive/`
  - Manifest: `source_docs/source_archive/source_archive_manifest.csv`.
- Inferred URL queue: `data/interim/16_inferred_url_resolution_queue_v0.csv`
  - 11 of 25 initial placeholders have been resolved and archived.
  - 14 remain unresolved or require correction/local retrieval.

## Current MT Status

- MT-001: basically done for extraction; still needs registry review of 2020 MMC extension candidates.
- MT-002: basically done; first full source-archive pass has 0 pending real URLs.
- MT-003: in progress; finish resolving 14 remaining `inferred_url` placeholders.
- MT-004: pending; Yonaguni A014/A015 local evidence pack.
- MT-005: pending; AWWA / spouse clubs charity recipient evidence.
- MT-006: pending; ONC / JICA / MOFA relationship chain.
- MT-007: pending; dugong lawsuit plaintiff mapping.
- MT-008: pending; add event/action/relation-strength fields to relation data.

## Useful Commands

```powershell
python scripts\archive_sources.py
python scripts\make_explanatory_graph_package.py
python scripts\make_module_completion_package.py
```

After source-log or archive changes, rerun the archive script first, then regenerate explanatory and module packages.

## Communication Guidance

- The old `docs/progress_report_v1.md` is an internal draft, not a deliverable.
- Next boss-facing communication should use explanatory outputs, not only statistics.
- Safe current message: R2, R3/R4, R5, R11, and R14 now have interpretable v0 deliverables; MT-001 extraction, MT-002 archive, and MT-003 first URL-resolution pass are the most concrete progress items.
- Keep all claims conservative: "publicly visible event participation", "candidate relation", "source-backed role", or "needs local retrieval" are preferred to over-strong network claims.

