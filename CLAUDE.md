# CLAUDE.md

This repository supports the Okinawa NGO / civic organization network research project.

For general multi-agent instructions, read `AGENTS.md` first. This file mirrors the same project rules for Claude-specific sessions.

## Project Rules

- Read `docs/phase1_workbench.md` first. It is the current project control document and must stay under 300 lines.
- Do not treat candidate edges as final findings. Initial CSV files contain seed data and candidate relationships for later review.
- Do not describe co-signing or joint statements as stable alliances without additional evidence.
- Do not describe funding, sponsorship, commission, or public-diplomacy relationships as confirmed unless the record is supported by official grants, awards, contracts, financial reports, organization reports, or equivalent primary sources.
- Do not treat service organizations for U.S. military families as anti-base or pro-base actors by default. Code them by observed function.
- For Yonaguni, use the main framing of frontline/security environment, local autonomy, referendum, Taiwan proximity, and health/life-safety concerns. Do not force it into an environmental-obstruction frame.
- Human review and local material collection are tracked in task books, not scattered notes.

## Current Entry Points

- General agent guide: `AGENTS.md`
- Workbench: `docs/phase1_workbench.md`
- Progress report: `docs/progress_report_v1.md`
- Human review tasks: `docs/human_review_tasks_v0.md`
- Local material collection tasks: `docs/local_retrieval_tasks_v1.md` (v1 supersedes v0; v0 kept as detailed catalog)
- Human decision tasks: `docs/human_decision_tasks_v0.md`
- Coding schema: `data/metadata/coding_schema_v0.md`
- Progress-sync assets: `docs/progress_sync_assets_v0.md`
- Module completion package: `outputs/module_completion_v0/README.md`
- Second progress-sync (boss-facing): `outputs/formal_comm_v0/第二次进度同步_v0.md` (figure sources regen: `python scripts\make_formal_comm_package.py`)
- Inferred URL queue: `data/interim/16_inferred_url_resolution_queue_v0.csv`

## Data Status

Current initial data lives under `data/interim/`. Updated 2026-07-02.

- `01_actor_registry_initial_v0.csv` — 103 actors (MT-001 added A077–A085 E2 signatory-only; MT-007 added A086 Turtle Island Restoration Network)
- `02_actor_aliases_initial_v0.csv` — 14 aliases
- `03_issue_taxonomy_v0.csv` — 19 issues
- `04_place_registry_v0.csv` — 20 places
- `05_source_log_initial_v0.csv` — 96 sources, currently 93 real URLs, 1 `inferred_url` placeholder (S020), and 2 non-URL references
- `07_actor_issue_edges_initial_v0.csv` — 180 edges
- `08_actor_place_edges_initial_v0.csv` — 124 edges
- `15_funding_or_support_edges_sample_v0.csv` — 33 edges (MT-005 AWWA recipients F028–F030; MT-006 ONC admin edges F031–F033)

Generated progress-sync charts live under `outputs/progress_sync_v0/` and `outputs/progress_sync_v1/`.

Current explanatory deliverables live under `outputs/explanatory_v0/`.

Current module deliverables live under `outputs/module_completion_v0/`.

Source archive status:

- 90 `archived`
- 2 `manual_archived`
- 1 `failed` (S096 MOFA page returns HTTP 403 to the bot; public URL, not bot-archivable)
- 1 `skipped_inferred_url` (S020)
- 2 `skipped_non_url_reference`
- (occasional transient SSL failures on other hosts recover on re-run)

Current MT status:

- MT-001: Tier A 9 actors (A077–A085) added at E2 signatory-only and wired into the 2020 MMC co-action event; Tier B deferred, Tier C signatory-only.
- MT-002: first full source-archive pass is basically done.
- MT-003: basically done; 24 of 25 placeholders resolved to verified URLs (year fixes on S027/S030/S037/S040); only S020 (Miyako groundwater) remains as a local-retrieval gap.
- MT-007: basically done; `lawsuit_actor_role_table_v0.csv` maps the Okinawa Dugong v. Rumsfeld parties — A076 confirmed named plaintiff, A002/A019 non-parties, JELF plaintiff, Earthjustice counsel; Turtle Island Restoration Network is the only named plaintiff still outside the registry.
- MT-005: in progress; named AWWA recipient edges added (F028–F030: Yomitan Quegoen, Uruma Social Welfare, Boy Scouts Far East; E3, DVIDS-sourced); full annual recipient table still needs Form 990 / annual reports. See `MT005_awwa_recipient_note.md`.
- MT-006: basically done; ONC placed in the international-cooperation/multicultural admin layer (MOFA NGO consultant F031, prefecture/city commissions F032–F033, JICA festival F011), separate from the anti-base movement; F019 (ONC–base-affairs) downgraded. See `MT006_onc_admin_chain_note.md`.
- MT-008: basically done; `actor_relation_events_v1.csv` (54 rows, 9 events) adds event_id/action_type/relation_strength as an event-aware side table. See `MT008_edge_enrichment_note.md`.

## Agent Skills

### Issue tracker

Issues are tracked in GitHub Issues for `mmm8091/OkinawaNGO`. External PRs are not treated as a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

This repo uses the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo. Domain documentation is expected at `CONTEXT.md` when created, with ADRs under `docs/adr/`. See `docs/agents/domain.md`.
