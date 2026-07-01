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

- `01_actor_registry_initial_v0.csv` — 102 actors (MT-001 added A077–A085, E2 signatory-only)
- `02_actor_aliases_initial_v0.csv` — 14 aliases
- `03_issue_taxonomy_v0.csv` — 19 issues
- `04_place_registry_v0.csv` — 20 places
- `05_source_log_initial_v0.csv` — 92 sources, currently 89 real URLs, 1 `inferred_url` placeholder (S020), and 2 non-URL references
- `07_actor_issue_edges_initial_v0.csv` — 180 edges
- `08_actor_place_edges_initial_v0.csv` — 124 edges
- `15_funding_or_support_edges_sample_v0.csv` — 27 edges

Generated progress-sync charts live under `outputs/progress_sync_v0/` and `outputs/progress_sync_v1/`.

Current explanatory deliverables live under `outputs/explanatory_v0/`.

Current module deliverables live under `outputs/module_completion_v0/`.

Source archive status:

- 85 `archived`
- 2 `manual_archived`
- 2 `failed` (transient SSL; recover on re-run)
- 1 `skipped_inferred_url` (S020)
- 2 `skipped_non_url_reference`

Current MT status:

- MT-001: Tier A 9 actors (A077–A085) added at E2 signatory-only and wired into the 2020 MMC co-action event; Tier B deferred, Tier C signatory-only.
- MT-002: first full source-archive pass is basically done.
- MT-003: basically done; 24 of 25 placeholders resolved to verified URLs (year fixes on S027/S030/S037/S040); only S020 (Miyako groundwater) remains as a local-retrieval gap.

## Agent Skills

### Issue tracker

Issues are tracked in GitHub Issues for `mmm8091/OkinawaNGO`. External PRs are not treated as a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

This repo uses the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo. Domain documentation is expected at `CONTEXT.md` when created, with ADRs under `docs/adr/`. See `docs/agents/domain.md`.
