# AGENTS.md

This repository supports the Okinawa NGO / civic organization network research project.

All agents should treat this file as the shared operating guide. Tool-specific files such as `CLAUDE.md` may mirror this guide, but this file is the general entry point.

## First Read

1. `docs/phase1_workbench.md` — current control document; must stay under 300 lines.
2. `docs/phase1_scheme_acceptance_audit_v1.md` — authoritative acceptance audit against the original Phase-1 DOCX.
3. `data/metadata/coding_schema_v0.md` — field definitions and evidence levels.
4. `docs/progress_sync_assets_v0.md` — communication assets and current completion notes.
5. `outputs/module_completion_v0/README.md` — existing v0 module deliverables; not the full Phase-1 acceptance status.
6. `CONTEXT.md` — stable domain context.

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

Updated: 2026-07-13.

- Actor registry: 118 organization-level actors. HR-013 added A111 and the user's HR-010 scope correction removed A094, so the net count stayed 118 and remains below the Phase-1 minimum of 120. A087–A093/A095–A101 remain E4 identity-only merges awaiting classification/edge review; A094 evidence is retained as history but must not return to the registry without a new human decision.
- Source log: 247 sources; no `inferred_url` placeholders remain. The HR-013/online-wave crosswalk has 70 source references over 67 URLs; 49 new URLs are S199–S247. Source inclusion does not approve an actor, edge, alliance, funding relation or interpretation. S051 is E0 `rejected_archive_mismatch` and must not support A011.
- Actor-issue candidate/reviewed edges: 222; 101 actors connected, 17 edge-isolated; 59 human-reviewed and 163 candidate rows.
- Actor-place candidate/reviewed edges: 125.
- Funding/support/relation sample edges: 43. F042 is A109→A052 fourth-round legal counsel; F043 is A105→A107 organizational affiliation. Both are explicitly non-funding/non-alliance relations.
- Issue taxonomy: 26 issue categories; HR-011 added anti_war and mobilization after the HR-010 additions.
- Place registry: 20 place/field nodes.
- Evidence notes: 49 formal HR-015 rows; five locator refinements remain explicit.
- Actor-event-venue: 65 formal rows; 61 `human_checked`, 4 `analytical_seed`. AEV0065 is A111's bounded 2024 rally-organizer observation. Nine MMC names are E2 event-only legacy candidates, not actors.
- Legal/policy procedure: 6 cases and 27 roles are HR-014 `human_checked`/accepted. `data/interim/18_legal_policy_actor_roles_v0.csv` separates registry actors from provisional procedural nodes.
- Source archive: 224 `archived`, 2 `manual_archived`, 19 `failed`, 2 `skipped_non_url_reference`. Of S199–S247, 48 archived and S213 remains a 403 failure. Failures may be 403/SSL/transient restrictions and do not negate source content. All 226 preserved artifacts currently match manifest SHA. The archive script refuses silent cache-hash drift, supports `--from-id`/`--to-id`, and allows `--reconcile-cache-hashes` only after manual inspection; raw archive artifacts are Git-binary to preserve bytes.

## Current Deliverables

- Explanatory graph package: `outputs/explanatory_v0/`
  - 5 PNG figures.
  - Main communication figures: place-issue matrix, Henoko/Oura Bay internationalization pathway, actor-issue bridge network.
- Module completion package: `outputs/module_completion_v0/`
  - Covers R2, R3/R4, R5, R11, and R14.
  - R5 now includes the full 2020 OEJP/MMC 71-group participant extraction.
  - `next_module_investigation_tasks_v0.csv` tracks MT tasks and completion status.
- Second progress-sync package: `outputs/formal_comm_v0/`
  - `第二次进度同步_v0.md` — the boss-facing deliverable (Feishu doc), concise, matches the first-sync style; covers research-module-menu progress, seven-week schedule check, and four embedded figure screenshots.
  - `第二次进度同步_v0.md` and `fig/*.png` are the historical client snapshot. `index.html`/`fig/*.html` may be regenerated internally, but publish a new version only after new screenshots and human figure/caption QA; do not silently overwrite the delivered snapshot.
  - This, not `docs/progress_report_v1.md`, is the current boss-facing deliverable.
- Phase-1 online-completion package: `outputs/online_completion_v0/`
  - Field-level findings and search logs for T1-A/D/E; S020 resolved; ONC public project costs and JICA contractor role added.
- Phase-1 visualization supplement: `outputs/phase1_visuals_v1/`
  - Functional ecology, actor-place matrix, and strict E3/E4 support/commission/service layers; generated by `scripts/make_phase1_visuals.py`.
- Phase-1 research report draft: `docs/phase1_research_report_v0.md`
  - Complete v0 draft for internal review; not yet the boss-facing final report.
- Phase-1 acceptance audit: `docs/phase1_scheme_acceptance_audit_v1.md` and `outputs/phase1_acceptance_audit_v0/`
  - The authoritative gap/done_when assessment against the original DOCX.
- First post-audit candidate packages and controlled merge:
  - `outputs/phase1_foundation_v1/`: 49 evidence notes and the original 64 AEV rows completed HR-015; the central `09` table now has 65 rows after HR-013 added AEV0065.
  - `outputs/registry_expansion_v1/`: HR-011/012 are merged; A107–A110 are retained, C015 remains deferred, and A052/A053/A010 history/round crosswalks are resolved.
  - `outputs/R08_legal_procedure_v0/`: six cases and 27 roles completed HR-014; third-Kadena counsel remains a provisional procedural collective, not an actor.
  - `outputs/R04_sakishima_frame_corpus_v0/`: 11 formal safe facts, 19 safe source excerpts, two explanatory SVG/HTML figures and brief; HR-016 holds 12 semantic/locator decisions.
  - `outputs/R09_referendum_process_v0/`: 24 formal accepted stages, 25 formal accepted roles, four-case timeline and institutional-gate figure; HR-017 holds 18 reviewed-all items outside the formal layer.
  - `outputs/R10_administrative_collaboration_v0/`: normalized 35 relations, 26 amount observations and 43 function observations with two boundary figures; only 9 relations inherit human review and HR-018 gates the other 26.
  - `outputs/R06_R07_R11_pathways_v1/`: 69 formal actor-event-venue-target/entry-mode observations, 4 separate analytical seeds, six R6 pathway families, three R7 case sequences and 44 R11 entry observations. HR-021 has eight blank downstream decisions; its first seven depend on HR-018 and do not re-review relation facts.
  - `outputs/phase1_source_integration_v1/`: 57 module-source crosswalk rows over 54 unique URLs; 39 new sources were integrated as S160–S198 with `relation_or_claim_approved=no`. HR-022 holds 49 source-metadata/support-boundary decisions with blank decision fields.
  - `outputs/R01_R02_actor_issue_v1/`: full 118-actor × 26-issue layered network, classification ecology, issue co-occurrence and bridge-mechanism figures. Only 59/222 edges are human-reviewed; HR-019 keeps 9 rule, 30 bridge and 65 scope decisions blank.
  - `outputs/R05_coaction_v1/`: complete 2010/2015/2020 lists as 169 event-participation observations, 15 strict repeat registry actors and two explanatory figures. HR-020 holds 14 blank identity/alias/segmentation decisions; repeat co-signing is not an alliance.
  - `outputs/coverage_audit_v1/`: six-dimension, 125-cell visibility-bias audit with Q1–Q3/R1–R11 implications. It is mechanical aggregation, so no HR-023 was created.
  - `outputs/R08_legal_procedure_v1/`: 27 accepted role×case rows across six human-checked cases, 54 role-family cells, two comparison figures and a report insert. It preserves 13 registered-actor roles versus 14 provisional nodes and creates no HR-026.
  - `outputs/edge_activation_v1/`: historical 18-actor/58-edge snapshot plus the current post-HR013 layer: 17 actors, 54 candidate edges and 38 source records. A094 is excluded from current use; HR-010 has 47 blank evidence-addendum rows and HR-024 has 8 blank rows.
  - `outputs/registry_expansion_gate_v1/`: machine evidence gate retained as a pre-human audit snapshot. HR-013 overrides it: A111 added; C010/C034 background-only; C029-C033 rejected; C015 remains in HR-011.
  - `outputs/hr013_online_wave_integration_v1/`: human-decision overlay and 70-row source crosswalk; all source rows retain `relation_or_claim_approved=no`.
- Local retrieval task book v1: `docs/local_retrieval_tasks_v1.md`
  - Splits LR into Tier 1 (online-doable, locked for this round) and Tier 2 (needs local collaborator / in-library databases).
- Source archive: `source_docs/source_archive/`
  - Manifest: `source_docs/source_archive/source_archive_manifest.csv`.
- Inferred URL queue: `data/interim/16_inferred_url_resolution_queue_v0.csv`
  - All 25 placeholders are resolved to verified URLs (year corrections on S020/S027/S030/S037/S040); S020 is a verified 2016 Ryukyu Shimpo URL.

## Current MT Status

- MT-001: extraction done. HR-015 moved nine E2 identity-unverified MMC names out of the actor registry and kept them event-only; independent identity/continuity sources are required before any future actor entry.
- MT-002: basically done; first full source-archive pass has 0 pending real URLs.
- MT-003: done; all 25 placeholders resolved to verified URLs; S020 is no longer a local-retrieval gap.
- MT-007: basically done; `lawsuit_actor_role_table_v0.csv` maps Okinawa Dugong v. Rumsfeld parties (A076 named plaintiff; A002/A019 non-parties; JELF plaintiff; Earthjustice counsel); Turtle Island Restoration Network is now A086 in the registry.
- MT-005: online pass done; named AWWA recipient edges F028–F030 and NOSCO joint donation F036 added; full recipient table still needs Form 990 / internal annual reports.
- MT-006: online public-record pass done; ONC FY2024 project costs and JICA contractor role are sourced in S099/S100. Keep “project cost” wording; do not call these amounts contract payments or movement funding.
- MT-008: basically done; registry-only `actor_relation_events_v1.csv` has 45 rows, 9 events, and 5 action types after withdrawing A077–A085. The central AEV table has 65 rows after HR-013, while preserving the nine event-only participants separately.
- MT-004: online pass done; 2015 Yonaguni referendum context corroborated by mainstream RS/OT/QAB, A015 kept E2 (no non-party source online); org-level identity still needs Yaeyama local retrieval (LR Tier 2).

## Current Phase-1 Direction (2026-07-13)

- Finish all reasonable online work before assigning local collaborators.
- Complete the valuable Phase-1 visualizations and a research-report v0 first; use their explicit evidence gaps to generate local tasks.
- Local assignment starts only after Tier 1 is complete or logged as `online_exhausted`, figures have data/scripts/briefs, and the report draft identifies exact missing fields.
- The original Phase-1 DOCX is the acceptance contract: 120–180 verifiable actors, all R1–R11 at differentiated depth, five specified core figures, a 25–35 page report, an 8k–12k paper, and a 15–20 page PPT.
- Registry growth remains module/value-driven and must eventually recover from 118 to at least 120 with organization-level evidence. The post-HR013 edge-activation pass leaves 17 current isolates; 16 have 54 candidate edges awaiting HR-010/HR-024, while A073 remains online-exhausted. HR-013's general-public-interest candidates are no longer available for number-filling. Prioritize 宮古島地下水研究会 and other thin-layer candidates with continuity plus a direct Phase-1 issue connection. The registry may exceed 180 if actor/place/channel/role layers remain unsaturated. Do not reinsert legacy A077–A085 or A094 to meet the number without a new human decision. MMC Tier B enters only as a separate mainland-solidarity layer when analytically justified; Tier C stays event-only.
- Existing `R14 coverage` outputs are a foundation coverage audit under the final DOCX numbering; final R14 is organizational genealogy and is an expansion module.
- Authoritative acceptance audit: `docs/phase1_scheme_acceptance_audit_v1.md`. Online/local sequencing remains in `docs/phase1_online_completion_plan_v0.md`; the current sub-agent execution briefs are in `docs/phase1_next_wave_execution_v2.md`.

## Useful Commands

```powershell
python scripts\archive_sources.py
python scripts\archive_sources.py --retry-failed
python scripts\archive_sources.py --from-id 197 --to-id 198 --retry-failed
python scripts\archive_sources.py --from-id 213 --to-id 213 --retry-failed
python scripts\archive_sources.py --reconcile-cache-hashes
python scripts\normalize_actor_issue_tags.py
python scripts\make_r04_sakishima_formal.py
python scripts\make_r04_hr016_packet.py
python scripts\make_r09_referendum_process.py
python scripts\make_r10_admin_collaboration.py
python scripts\make_r06_r07_r11_pathways.py
python scripts\make_r08_legal_procedure_v1.py
python scripts\make_edge_activation_v1.py
python scripts\validate_registry_expansion_gate_v1.py
python scripts\integrate_hr013_online_wave.py
python scripts\make_r01_r02_actor_issue.py
python scripts\make_r05_coaction_v1.py
python scripts\make_coverage_audit_v1.py
python scripts\make_phase1_source_merge_proposal.py
python scripts\integrate_phase1_module_sources.py
python scripts\merge_hr011_hr012.py
python scripts\merge_hr014.py
python scripts\merge_hr015.py
python scripts\finalize_hr011_hr015_main.py
python scripts\make_explanatory_graph_package.py
python scripts\make_module_completion_package.py
python scripts\make_relation_events.py
python scripts\make_event_repertoire_fig.py
python scripts\make_formal_comm_package.py
python scripts\make_phase1_visuals.py
python scripts\validate_phase1_data.py
```

After source-log or archive changes, rerun the archive script first, then regenerate explanatory and module packages.

## Communication Guidance

- The old `docs/progress_report_v1.md` is an internal draft, not a deliverable.
- Next boss-facing communication should use explanatory outputs, not only statistics.
- Safe current message: HR-011–015 are integrated; R1/R2, R4/R5/R9/R10, R6/R7/R8/R11 and the six-dimension coverage audit have online explanatory packages. HR-016–022 and HR-024 preserve unresolved human decisions. The registry remains 118 after replacing A094 with A111, so Phase-1 still misses the 120 minimum; the largest online gaps are R3 spatial semantics/dossiers, the R9 election side, heterogeneous R5/R7 actions, schema/alias freeze, and the final report/paper/PPT deliverables.
- Keep all claims conservative: "publicly visible event participation", "candidate relation", "source-backed role", or "needs local retrieval" are preferred to over-strong network claims.
