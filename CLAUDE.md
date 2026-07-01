# CLAUDE.md

This repository supports the Okinawa NGO / civic organization network research project.

## Project Rules

- Read `docs/phase1_workbench.md` first. It is the current project control document and must stay under 300 lines.
- Do not treat candidate edges as final findings. Initial CSV files contain seed data and candidate relationships for later review.
- Do not describe co-signing or joint statements as stable alliances without additional evidence.
- Do not describe funding, sponsorship, commission, or public-diplomacy relationships as confirmed unless the record is supported by official grants, awards, contracts, financial reports, organization reports, or equivalent primary sources.
- Do not treat service organizations for U.S. military families as anti-base or pro-base actors by default. Code them by observed function.
- For Yonaguni, use the main framing of frontline/security environment, local autonomy, referendum, Taiwan proximity, and health/life-safety concerns. Do not force it into an environmental-obstruction frame.
- Human review and local material collection are tracked in task books, not scattered notes.

## Current Entry Points

- Workbench: `docs/phase1_workbench.md`
- Human review tasks: `docs/human_review_tasks_v0.md`
- Local material collection tasks: `docs/local_retrieval_tasks_v0.md`
- Human decision tasks: `docs/human_decision_tasks_v0.md`
- Coding schema: `data/metadata/coding_schema_v0.md`
- Progress-sync assets: `docs/progress_sync_assets_v0.md`

## Data Status

Current initial data lives under `data/interim/`.

- `01_actor_registry_initial_v0.csv`
- `03_issue_taxonomy_v0.csv`
- `04_place_registry_v0.csv`
- `05_source_log_initial_v0.csv`
- `07_actor_issue_edges_initial_v0.csv`
- `08_actor_place_edges_initial_v0.csv`
- `15_funding_or_support_edges_sample_v0.csv`

Generated progress-sync charts live under `outputs/progress_sync_v0/`.

## Agent Skills

### Issue tracker

Issues are tracked in GitHub Issues for `mmm8091/OkinawaNGO`. External PRs are not treated as a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

This repo uses the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo. Domain documentation is expected at `CONTEXT.md` when created, with ADRs under `docs/adr/`. See `docs/agents/domain.md`.

