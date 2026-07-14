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

Updated: 2026-07-14.

- Actor registry: 118 organization-level actors. HR-013 added A111 and the user's HR-010 scope correction removed A094, so the net count stayed 118 and remains below the Phase-1 minimum of 120. A087–A093/A095–A101 remain E4 identity-only merges awaiting classification/edge review; A094 evidence is retained as history but must not return to the registry without a new human decision.
- Source log: 295 sources; no `inferred_url` placeholders remain. NW2-H reused S158/S204 and provisionally added 47 `ai_seeded` proposal-derived URLs as S248–S294; S295 is a separately archived HR-011 locator correction and not an independent identity source. Source inclusion does not approve an actor, edge, alliance, funding relation, election role, causal claim or interpretation. S051 is E0 `rejected_archive_mismatch` and must not support A011.
- Actor-issue candidate/reviewed edges: 222; 101 actors connected, 17 edge-isolated; 59 human-reviewed and 163 candidate rows.
- Actor-place candidate/reviewed edges: 129.
- Funding/support/relation sample edges: 43. F042 is A109→A052 fourth-round legal counsel; F043 is A105→A107 organizational affiliation. Both are explicitly non-funding/non-alliance relations.
- Issue taxonomy: 26 issue categories; HR-011 added anti_war and mobilization after the HR-010 additions.
- Place registry: 20 place/field nodes.
- Evidence notes: 49 formal HR-015 rows; five locator refinements remain explicit.
- Actor-event-venue: 67 rows; 63 `human_checked`, 4 `analytical_seed`. AEV0065–0067 preserve A111/A108 bounded rally roles and A109's fourth-Kadena litigation role. Nine MMC names are E2 event-only legacy candidates, not actors.
- Legal/policy procedure: 6 cases and 27 roles are HR-014 `human_checked`/accepted. `data/interim/18_legal_policy_actor_roles_v0.csv` separates registry actors from provisional procedural nodes.
- Source archive: 265 `archived`, 2 `manual_archived`, 26 `failed`, 2 `skipped_non_url_reference`. Of S248–S294, 40 archived and 7 failed; HR-030 holds 22 blank metadata/archive decisions. Failures may be 403/SSL/transient restrictions and do not negate source content. All 267 preserved artifacts currently match manifest SHA. The archive script refuses silent cache-hash drift, supports `--from-id`/`--to-id`, and allows `--reconcile-cache-hashes` only after manual inspection; raw archive artifacts are Git-binary to preserve bytes.

## Current Deliverables

- Explanatory graph package: `outputs/explanatory_v0/`
  - 5 PNG figures.
  - Historical exploration package. The old place-issue matrix is retired after the 2026-07-14 method audit found actor-level Cartesian projection; it must not be used as a formal finding. Rebuild MA002 from same-source/same-event actor-place-issue facts.
  - The Henoko/Oura Bay pathway and actor-issue bridge network remain candidate communication assets subject to their human/interpretive gates.
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
- Academic/client red-team audit: `docs/phase1_academic_client_redteam_audit_v1.md`
  - The current harsh acceptance and academic-value assessment. It separates the broad client report from the narrow R4+R8+R9 paper and records the retired spatial projection.
- Current formal human assignment: `docs/human_review_assignment_HR027_v1.md`
  - HR-027 is the B01/P0 batch. It has four blank add/defer/reject decisions; HD-012 separately requests the prior 1990–2022 election-study inputs.
- Third-sync correction ledger: `docs/third_sync_correction_ledger_v1.md`
  - The second sync remains a historical snapshot. The next client communication must explicitly correct its spatial figure, bridge, internationalization and schedule claims.
- First post-audit candidate packages and controlled merge:
  - `outputs/phase1_foundation_v1/`: 49 evidence notes and the original 64 AEV rows completed HR-015; the central `09` table now has 67 rows after HR-013 and the HR-011 bounded event additions.
  - `outputs/registry_expansion_v1/`: HR-011/012 are merged; A107–A110 are retained, C015 remains deferred, and A052/A053/A010 history/round crosswalks are resolved.
  - `outputs/R08_legal_procedure_v0/`: six cases and 27 roles completed HR-014; third-Kadena counsel remains a provisional procedural collective, not an actor.
  - `outputs/R04_sakishima_frame_corpus_v0/`: 11 formal safe facts, 19 safe source excerpts, two explanatory SVG/HTML figures and brief; HR-016 holds 12 semantic/locator decisions.
  - `outputs/R09_referendum_process_v0/`: 24 formal accepted stages, 25 formal accepted roles, four-case timeline and institutional-gate figure; HR-017 holds 18 reviewed-all items outside the formal layer.
  - `outputs/R10_administrative_collaboration_v0/`: a purposive cross-source sample with 35 relations, 26 amount observations and 43 function observations plus two boundary figures; these are within-package counts, not an official annual/department census. Only 9 relations inherit human review and HR-018 gates the other 26.
  - `outputs/R10_completeness_audit_v1/`: verifies the R10 sample boundary against the full 86-page/616-row S002 source universe and the six non-zero S099 program-cost rows. S002 coverage is 10/616; S099's three explicitly public-commissioned rows are represented, without approving relation/payment semantics.
  - `outputs/R10_official_collaboration_universe_v1/`: complete S002 616-row source universe, official resource-type tables, descriptive statistics and two ready-now figures. Its 365 machine display labels are not actors; HR-032 gates only future canonical/JV/registry crosswalk.
  - `outputs/R06_R07_R11_pathways_v1/`: 71 formal actor-event-venue-target/entry-mode observations, 4 separate analytical seeds, six R6 pathway families, three R7 case sequences and 44 R11 entry observations. HR-021 has eight blank downstream decisions; its first seven depend on HR-018 and do not re-review relation facts.
  - `outputs/phase1_source_integration_v1/`: 57 module-source crosswalk rows over 54 unique URLs; 39 new sources were integrated as S160–S198 with `relation_or_claim_approved=no`. HR-022 holds 49 source-metadata/support-boundary decisions with blank decision fields.
  - `outputs/R01_R02_actor_issue_v1/`: full 118-actor × 26-issue layered network, classification ecology, issue co-occurrence and bridge-mechanism figures. Only 59/222 edges are human-reviewed; HR-019 keeps 9 rule, 30 bridge and 65 scope decisions blank.
  - `outputs/R05_coaction_v1/`: complete 2010/2015/2020 lists as 169 event-participation observations, 15 strict repeat registry actors and two explanatory figures. HR-020 holds 14 blank identity/alias/segmentation decisions; repeat co-signing is not an alliance.
  - `outputs/coverage_audit_v1/`: six-dimension, 125-cell visibility-bias audit with Q1–Q3/R1–R11 implications. It is mechanical aggregation, so no HR-023 was created.
  - `outputs/R08_legal_procedure_v1/`: 27 accepted role×case rows across six human-checked cases, 54 role-family cells, two comparison figures and a report insert. It preserves 13 registered-actor roles versus 14 provisional nodes and creates no R8-specific HR task; HR-026 is now used by the election-civic candidate layer.
  - `outputs/edge_activation_v1/`: historical 18-actor/58-edge snapshot plus the current post-HR013 layer: 17 actors, 54 candidate edges and 38 source records. A094 is excluded from current use; HR-010 has 47 blank evidence-addendum rows and HR-024 has 8 blank rows.
  - `outputs/registry_expansion_gate_v1/`: machine evidence gate retained as a pre-human audit snapshot. HR-013 overrides it: A111 added; C010/C034 background-only; C029-C033 rejected; C015 remains in HR-011.
  - `outputs/hr013_online_wave_integration_v1/`: human-decision overlay and 70-row source crosswalk; all source rows retain `relation_or_claim_approved=no`.
- Second post-audit online wave:
  - `outputs/R03_spatial_dossier_v1/`: 129/129 actor-place edges receive candidate semantics; 41 blank HR-025 decisions; full matrix and separate Yonaguni/Ishigaki/Miyako dossiers. Henoko has 42 target edges versus 3 presence edges; AP123 exposes a Camp Schwab/Foster cross-key conflict.
  - `outputs/R09_election_civic_interface_v1/`: 19 candidate actor-event observations across the 2014/2018/2022 gubernatorial elections and 21 source proposals. All 19 remain in blank HR-026; no vote, turnout, outcome or policy causality is inferred.
  - `outputs/registry_value_gate_v2/`: five module-value candidates were gated; four enter blank HR-027 (宮古島地下水研究会, 宜野湾ちゅら水会, 全日本港湾労働組合沖縄地方本部, 新日本婦人の会沖縄県本部), while 八重山大地会 is deferred for a continuity gap. No A number or central actor edge was added.
  - `outputs/R05_R07_heterogeneous_repertoire_v1/`: 148 existing formal observations reduce to 39 unique case/event×action×venue units across 15 action families and 9 venue groups. It adds no facts, so HR-028 is zero.
  - `outputs/schema_alias_freeze_v1/`: 467 freeze candidates and 34 blank HR-029 decisions; proposed vocabulary consolidation is actor_class 25→24, legal_status 44→33, relation 28→25 and action 14→12. Central schema remains unchanged.
  - `outputs/next_wave_source_proposal_audit_v1/` and `outputs/next_wave_source_integration_v1/`: 50 proposal rows normalize to 49 URLs; two reuse S158/S204 and 47 provisionally enter as S248–S294. All claim approvals remain `no`; HR-030 has 22 blank metadata/archive rows.
  - `outputs/report_assembly_v1/` and `outputs/report_claim_audit_v1/`: 73 current report resources are classified as ready/freeze/superseded; the assembly plan targets a 32-page report and 20-page PPT. All 27 non-superseded report figures have a figure→data→source-crosswalk→script→human-gate traceability row (14 ready, 13 pending gate). The claim audit covers 78 claims and 32 numeric groups; HR-031 holds three blank interpretive-strength decisions. Plans are not contract artifacts: MA017–MA023 separately track the report DOCX/PDF, paper, PPTX, Sakishima dossier DOCX, public-data bundle, final codebook/lint and missing prior-election-study input.
  - `outputs/report_assembly_v1/`: report assembly blueprint for 36 logical figures, 26 tables and 11 briefs; 14 figures are ready now, 13 require freeze, 9 are superseded. The recommended formal report is 32 pages; this package does not generate DOCX/PDF.
  - `outputs/human_review_orchestration_v1/`: HR-016–032 dependency graph, 13 recommended batches and a 378-row inventory (370 blank decisions plus 8 ancillary rows). It organizes review work and never pre-fills a human decision.
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
- MT-008: basically done; registry-only `actor_relation_events_v1.csv` has 45 rows, 9 events, and 5 action types after withdrawing A077–A085. The central AEV table has 67 rows after HR-013 and bounded HR-011 additions, while preserving the nine event-only participants separately.
- MT-004: online pass done; 2015 Yonaguni referendum context corroborated by mainstream RS/OT/QAB, A015 kept E2 (no non-party source online); org-level identity still needs Yaeyama local retrieval (LR Tier 2).

## Current Phase-1 Direction (2026-07-14)

- Finish all reasonable online work before assigning local collaborators.
- Complete the valuable Phase-1 visualizations and a research-report v0 first; use their explicit evidence gaps to generate local tasks.
- Local assignment starts only after Tier 1 is complete or logged as `online_exhausted`, figures have data/scripts/briefs, and the report draft identifies exact missing fields.
- The original Phase-1 DOCX is the acceptance contract: 120–180 verifiable actors, all R1–R11 at differentiated depth, five specified core figures, a 25–35 page report, an 8k–12k paper, and a 15–20 page PPT.
- Registry growth remains module/value-driven and must eventually recover from 118 to at least 120 with organization-level evidence. HR-027 now holds four value-gated candidates; accepting at least two would reach the minimum, but the reason must be module repair rather than number filling. The post-HR013 edge-activation pass leaves 17 current isolates; 16 have 54 candidate edges awaiting HR-010/HR-024, while A073 remains online-exhausted. Do not reinsert legacy A077–A085 or A094 without a new human decision. MMC Tier B enters only as a separate mainland-solidarity layer when analytically justified; Tier C stays event-only.
- Existing `R14 coverage` outputs are a foundation coverage audit under the final DOCX numbering; final R14 is organizational genealogy and is an expansion module.
- Authoritative acceptance audit: `docs/phase1_scheme_acceptance_audit_v1.md`. Online/local sequencing remains in `docs/phase1_online_completion_plan_v0.md`; the current sub-agent execution briefs are in `docs/phase1_next_wave_execution_v2.md`.
- If delivered today, the conservative client verdict is reject-and-rectify: registry is 118, the formal same-source/event place-issue figure is missing, and final DOCX/PDF, paper, PPTX, Sakishima dossier, public-data bundle and frozen codebook do not yet exist.
- Academic work now follows a separate line: operationalize 12–18 translation episodes around R4+R8+R9, add negative cases and reviewed-only/source-cluster/identity-uncertainty robustness checks, and do not infer process from issue co-occurrence.

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
python scripts\make_r10_official_collaboration_universe_v1.py
python scripts\make_r06_r07_r11_pathways.py
python scripts\make_r08_legal_procedure_v1.py
python scripts\make_edge_activation_v1.py
python scripts\validate_registry_expansion_gate_v1.py
python scripts\integrate_hr013_online_wave.py
python scripts\make_r03_spatial_dossier_v1.py
python scripts\make_r09_election_civic_interface_v1.py
python scripts\make_registry_value_gate_v2.py
python scripts\make_r05_r07_heterogeneous_repertoire_v1.py
python scripts\make_schema_alias_freeze_v1.py
python scripts\audit_next_wave_source_proposals_v1.py
python scripts\integrate_next_wave_sources_v1.py
python scripts\make_r01_r02_actor_issue.py
python scripts\make_r05_coaction_v1.py
python scripts\make_coverage_audit_v1.py
python scripts\make_phase1_source_merge_proposal.py
python scripts\integrate_phase1_module_sources.py
python scripts\merge_hr011_hr012.py
python scripts\merge_hr014.py
python scripts\merge_hr015.py
python scripts\finalize_hr011_hr015_main.py
# Historical exploration packages only; regenerated spatial output is visibly retired.
python scripts\make_explanatory_graph_package.py
python scripts\make_module_completion_package.py
python scripts\make_relation_events.py
python scripts\make_event_repertoire_fig.py
# Historical second-sync reproduction only; never overwrite the delivered snapshot for a new sync.
python scripts\make_formal_comm_package.py
python scripts\make_report_traceability_crosswalk_v1.py
python scripts\audit_report_claims_v1.py
python scripts\make_human_review_orchestration_v1.py
python scripts\make_phase1_visuals.py
python scripts\validate_phase1_data.py
```

After source-log or archive changes, rerun the archive script first, then regenerate explanatory and module packages.

## Communication Guidance

- The old `docs/progress_report_v1.md` is an internal draft, not a deliverable.
- Next boss-facing communication should use explanatory outputs, not only statistics.
- Safe current message: HR-011–015 are integrated; R1–R11 now all have differentiated online explanatory layers, including R3 spatial dossiers, R9 election candidates, heterogeneous R5/R7 actions and the complete 616-row R10 official-source universe. The registry remains 118 after replacing A094 with A111; four value-gated candidates are formally assigned in HR-027, and no candidate has been auto-added. The old place-issue matrix is retired; its same-source/event replacement is still missing. HR-016–022 and HR-024–027/029–032 preserve unresolved human decisions; HR-028 is zero. The main remaining work is the publication-critical human freeze, corrected core figures, translation-episode/robustness analysis and final contract artifacts.
- Keep all claims conservative: "publicly visible event participation", "candidate relation", "source-backed role", or "needs local retrieval" are preferred to over-strong network claims.
