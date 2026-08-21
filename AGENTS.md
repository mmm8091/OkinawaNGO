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

## Collaboration Cadence

- The project principal targets roughly 50% participation in interpretive work. AI may handle approved mechanical extraction, normalization, QA and figure generation, but must not replace the principal's question selection, evidence reading or conclusion-strength decisions.
- Before a new broad research wave, provide a compact decision brief: research question, current evidence, competing explanations, expected output and decisions required from the principal.
- Pause after each major module or strong new interpretation for the principal to continue, revise or stop it. Do not accumulate many modules and hand them over only at the end.
- The first five-hour project re-entry sheet has a paused/incomplete return. Do not start another broad research wave until it is completed; read-only clarification and already-approved bounded maintenance remain allowed.

## Current Data Status

Updated: 2026-08-21.

- Actor registry: 122 historical rows and 121 active actors. A072 is a provenance tombstone merged into A071 and must be hidden from current graphs/search; A112–A115 are the HR-027 module-repair additions. The active count clears the Phase-1 minimum of 120. A094 evidence is historical and must not return without a new human decision.
- Source log: 295 sources; no `inferred_url` placeholders remain. NW2-H reused S158/S204 and provisionally added 47 `ai_seeded` proposal-derived URLs as S248–S294; S295 is a separately archived HR-011 locator correction and not an independent identity source. Source inclusion does not approve an actor, edge, alliance, funding relation, election role, causal claim or interpretation. S051 is E0 `rejected_archive_mismatch` and must not support A011.
- Actor-issue table: 294 historical rows. After the principal-confirmed HR-035 Batch 2 merge, the current analytical layer has 283 active edges, 141 human-reviewed and 142 candidate; 116 active actors are connected and 5 are isolated. Eleven rejected/deactivated/excluded rows remain history-only. AI068 and rejected AI178 are excluded from the default Okinawa narrative. AI157 and AI158 remain `needs_second_source` candidates.
- Actor-place table: 135 historical rows; 130 are active, comprising 53 human-reviewed and 77 candidate rows, while 5 are retired. Headquarters/site/event/target/venue semantics remain distinct.
- Funding/support/relation sample edges: 43. F042 is A109→A052 fourth-round legal counsel; F043 is A105→A107 organizational affiliation. Both are explicitly non-funding/non-alliance relations.
- Issue taxonomy: 26 issue categories; HR-011 added anti_war and mobilization after the HR-010 additions.
- Place registry: 21 place/field nodes, including P021 Sakishima Islands.
- Evidence notes: 49 formal HR-015 rows; five locator refinements remain explicit.
- Actor-event-venue: 67 rows; 63 `human_checked`, 4 `analytical_seed`. AEV0065–0067 preserve A111/A108 bounded rally roles and A109's fourth-Kadena litigation role. Nine MMC names are E2 event-only legacy candidates, not actors.
- Legal/policy procedure: 6 cases and 27 roles are HR-014 `human_checked`/accepted. `data/interim/18_legal_policy_actor_roles_v0.csv` separates registry actors from provisional procedural nodes.
- Source archive: 273 `archived`, 2 `manual_archived`, 18 `failed`, 2 `skipped_non_url_reference`. HR-030 is complete and merged. Failures may be 403/SSL/transient restrictions and do not negate source content. The archive script refuses silent cache-hash drift, supports `--from-id`/`--to-id`, and allows `--reconcile-cache-hashes` only after manual inspection; raw archive artifacts are Git-binary to preserve bytes.

## Current Deliverables

- Explanatory graph package: `outputs/explanatory_v0/`
  - 5 PNG figures.
  - Historical exploration package. The old place-issue matrix is retired after the 2026-07-14 method audit found actor-level Cartesian projection; it must not be used as a formal finding. Rebuild MA002 from same-source/same-event actor-place-issue facts.
  - The Henoko/Oura Bay pathway and actor-issue bridge network remain candidate communication assets subject to their human/interpretive gates.
- Module completion package: `outputs/module_completion_v0/`
  - Covers R2, R3/R4, R5, R11, and R14.
  - R5 now includes the full 2020 OEJP/MMC 71-group participant extraction.
  - `next_module_investigation_tasks_v0.csv` tracks MT tasks and completion status.
- Second progress-sync package (last delivered historical client snapshot): `outputs/formal_comm_v0/`
  - `第二次进度同步_v0.md` — the boss-facing deliverable (Feishu doc), concise, matches the first-sync style; covers research-module-menu progress, seven-week schedule check, and four embedded figure screenshots.
  - `第二次进度同步_v0.md` and `fig/*.png` are the historical client snapshot. `index.html`/`fig/*.html` may be regenerated internally, but publish a new version only after new screenshots and human figure/caption QA; do not silently overwrite the delivered snapshot.
  - This, not `docs/progress_report_v1.md`, is the last delivered boss-facing artifact. `outputs/formal_comm_v2/` is the current third-sync preparation package, not a delivered PDF.
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
- HR-027 return and integration: `docs/human_review_return_HR027_v1.md` and `outputs/hr027_integration_v1/`
  - All four registry decisions are complete and merged as A112–A115. Seventeen event descriptions remain outside central AEV in a human-review candidate queue; no inter-actor relation edge was added. HD-012 separately requests the prior 1990–2022 election-study inputs.
- Third-sync correction ledger: `docs/third_sync_correction_ledger_v1.md`
  - The second sync remains a historical snapshot. The next client communication must explicitly correct its spatial figure, bridge, internationalization and schedule claims.
- Exploration system: `outputs/exploration_system_data_v1/`, `prototypes/nr3_explorer/`, and `docs/nr3_handoff_v1.md`
  - The frontend is regenerated from the HR-035 Batch 2 layer: 141 reviewed/142 research actor-issue edges, with 83 frozen-bounded, 58 accepted-unfrozen, 28 scope-reviewed/fact-pending and 114 fact-pending states. Schema 1.2.0 exposes all 13 episodes in zh/ja/en and five reviewed lifecycle anchors; LC004/LC005 remain last-observed lower bounds, not dissolutions. Actor class, region, place-display-region and time-period semantics come from the data contract rather than React constants.
  - The publication compiler now gates both dedicated exhibits and legacy core-derived surfaces. `data/metadata/research_publication_core_surfaces_v1.json` projects every builder output by exact path/JSON pointer; public releases do not contain the mixed `demo/relations.json`, `research/candidates.json`, unused legacy views or duplicate lifecycle payload. `reviewed`/`client_preview`/`internal` remain physically isolated. Channel verification checks profile/release/manifest hash, and `dist/release.json` records publication/site releases, frontend hash, Git commit and dirty state.
  - Every production build and dev-server generation binds one verified immutable release. Development watches the active `client_preview` channel and restarts Vite when it advances, preventing stale-snapshot hot reloads without mixing parallel requests across releases; missing publication paths return JSON 404 rather than SPA HTML.
  - Publication architecture and existing-asset disposition are authoritative in `docs/research_publication_architecture_v1.md`, `data/metadata/research_publication_catalog_v1.json`, `data/metadata/research_publication_core_surfaces_v1.json`, and `docs/research_publication_asset_audit_v1.md`. The 26 catalog entries comprise eight complete objects, four bounded partial surfaces, five method-ready modules without a public adapter, five valuable packages requiring further research and four retired/prohibited families. Do not claim the historical full-repository suite is green merely from current publication tests.
- Research-wave topic selection: `docs/research_wave_topic_selection_v1.md`, `docs/research_wave_v1_handoff.md`, and `outputs/research_wave_*`
  - H1/H2/H3 first pilots are complete as additive `research_only` packages and were narrowed after cross-audit. H1 supports source dependence of the E3/E4 actor–issue visibility layer, with about 84% of the three-source loss driven by S004; source and actor deletion are unmatched units. H2 compares a nine-actor service-side registry subset with 65 accountability-side candidates (18 human-reviewed anchors/47 candidate-only anchors); direct cross-group organization relations are unencoded in the bounded inputs, while people and recipients are unmeasured/incomplete. H3 supports event-level carrier/contact pathways only; direction, independent adoption, vocabulary growth and durable mobilization are unconfirmed. `outputs/research_wave_topic_selection_v1/frontend_research_modules_v1.json` is a module/asset index, not a row-level frontend contract; status is `module_index_ready_observation_exports_gated`, and all three modules are `not_frontend_ready`. Principal evidence reading is required before a second targeted wave.
- U.S.-presence multilayer network wave 1: `docs/us_presence_network_research_wave_v1.md`, `docs/us_presence_network_architecture_v1.md`, `docs/us_presence_network_wave1_principal_checkpoint_v1.md`, and `outputs/us_presence_*`
  - The 17 `us_origin` registry rows are frozen as an analytical selection frame: 9 service/charity comparison actors, 6 accountability comparison actors, X013 public-diplomacy program node and X014 funder watchlist node. These are comparison groups, not fixed pro-/anti-U.S. actor labels.
  - Architecture separates money, person–actor–time, service–recipient, affiliation/control, action–institution and official-site layers. The controlled vocabulary has 70 terms and 44 gates; `community_mediation` records a resource/service crossing the base–local-society boundary and does not imply acceptance or legitimation.
  - The actor directory candidate has 121 active actors, 65 formal-page candidates and 56 `not_found`; all 65 page decisions are complete (`accept 54 / revise 4 / defer 5 / reject 2`), while the reviewed overlay is not yet centrally integrated.
  - The service recon has 18 actor/program observations, 29 person roles, 14 typed resource-flow candidates, 16 recipient observations and 12 discourse/service observations (LEG0=3, LEG1=9; LEG2 requires separate bounded-response rows and LEG3 remains zero). The accountability recon has 8 scoped actors, 11 person roles, 9 action/relation observations and 2 resource observations. All remain `research_only` and not frontend-ready.
  - The legacy 43-row relation sample is mapped without fact changes to 8 money, 4 service-recipient, 9 affiliation, 20 action-institution, 1 lead and 1 history-only row. The six group decisions are principal-confirmed (`accept` 5 / `revise` 1); F017/F043 will become `regional_branch` when the rules are later expanded, while the 43-row crosswalk remains unexpanded.
  - The four USN review packets and five-item principal architecture checkpoint are principal-confirmed outside the old central ledger. Their research-return merge is commit `4dccaf1`. The controlled integration design is complete in `docs/us_presence_controlled_integration_design_v1.md` and `outputs/us_presence_controlled_integration_design_v1/`: 37 expected actions, 18 table-delta declarations, 35 mandatory tests and exact ID-to-decision mapping hashes validate as `PASS_DESIGN_ONLY`. The next principal gate is permission to build plan mode and sandbox tests only; central writeback, relation-crosswalk expansion, publication adapter and frontend release remain unauthorized. The pre-return machine contracts still use L1/L2/L3 suffixes as legacy aliases for approved LEG1/LEG2/LEG3 semantics; migrate them mechanically only inside an approved integration plan.
- Post-freeze research compatibility: `outputs/research_wave_postfreeze_compatibility_v1/`
  - Recomputed against HR-035 Batch 2 without rewriting historical pilot packages. H1 still has 271 E3/E4 edges and the same S004 deletion result; H2's current accountability comparison is 77 actors (41 reviewed anchors/36 candidate-only anchors); H3's three target-tag reviewed counts are 3/5/5. These remain `research_only`, `candidate_analysis`, and `not_frontend_ready`.
- Live human-review ledger: `docs/principal_human_review_remaining_v19.md`
  - No pre-USN central online human-decision field is blank. HR-035 Batch 2's 23 decisions are principal-confirmed and centrally merged through the dedicated idempotent merger. Twelve local/new-primary-material items remain; AI157 and AI158 are completed `defer_second_source` decisions and now form online enrichment leads rather than blank human-review items. The USN packets and five-item checkpoint are principal-confirmed and tracked outside the old central ledger. They remain unmerged into central facts and have no central writeback authority; the controlled design is complete, but even plan-mode merger construction requires the next principal approval.
- First post-audit candidate packages and controlled merge:
  - `outputs/phase1_foundation_v1/`: 49 evidence notes and the original 64 AEV rows completed HR-015; the central `09` table now has 67 rows after HR-013 and the HR-011 bounded event additions.
  - `outputs/registry_expansion_v1/`: HR-011/012 are merged; A107–A110 are retained, C015 remains deferred, and A052/A053/A010 history/round crosswalks are resolved.
  - `outputs/R08_legal_procedure_v0/`: six cases and 27 roles completed HR-014; third-Kadena counsel remains a provisional procedural collective, not an actor.
  - `outputs/R04_sakishima_frame_corpus_v0/`: 19 human-reviewed/QA-safe frame facts, 24 safe excerpts, 14 layered entities and two explanatory figures. HR-016's 12 online semantic/locator decisions are complete and merged; eight rejected actor candidates remain history-only, while local-expression gaps remain local tasks.
  - `outputs/R09_referendum_process_v0/`: 29 formal accepted stages and 29 formal accepted roles, plus the four-case timeline and institutional-gate figure. HR-017 has 9 online decisions complete and 9 local-retrieval items blank.
  - `outputs/R10_administrative_collaboration_v0/`: a purposive cross-source sample with 35 relations, 28 amount observations and 43 function observations plus two boundary figures; these are within-package counts, not an official annual/department census. The formal layers are 24/10/1 reviewed/revised/local for relations, 21/6/1 for amounts and 29/13/1 for functions. HR-018 online decisions are merged; two original local/internal-record decisions remain deferred.
  - `outputs/R10_completeness_audit_v1/`: verifies the R10 sample boundary against the full 86-page/616-row S002 source universe and the six non-zero S099 program-cost rows. S002 coverage is 10/616; S099's three explicitly public-commissioned rows are represented, without approving relation/payment semantics.
  - `outputs/R10_official_collaboration_universe_v1/`: complete S002 616-row source universe, official resource-type tables, descriptive statistics and two ready-now current SVG/HTML figures generated by `render_r10_official_universe_current.py`. Its 365 machine display labels are not actors; HR-032's 8 canonical/JV/registry crosswalk decisions are complete and merged without creating payment edges.
  - `outputs/R06_R07_R11_pathways_v1/`: 80 formal actor-event-venue-target/entry-mode observations, 4 separate analytical seeds, six R6 pathway families, three R7 cases/nine stages and 53 R11 entry observations. HR-021's 8 downstream decisions are complete and merged; the six SVG/HTML assets are regenerated from the current module CSVs by a render-only script.
  - `outputs/phase1_source_integration_v1/`: 57 module-source crosswalk rows over 54 unique URLs; 39 new sources were integrated as S160–S198 with `relation_or_claim_approved=no`. HR-022's 49 source-metadata/support-boundary decisions are complete and merged.
  - `outputs/R01_R02_actor_issue_v1/`: history audit covers 122 registry rows and 294 actor-issue rows; current figures use 121 active actors and 283 active edges (141 reviewed/142 candidate), with 116 connected and 5 isolated. HR-019, HR-035 Batch 1/2 and HR-010 batch 6 are merged; eleven invalidated rows remain history-only.
  - `outputs/R05_coaction_v1/`: complete 2010/2015/2020 lists as 169 event-participation observations: 64 registry rows, 22 human-reviewed event-only identities and 83 other event-only names; alias pending is zero. HR-020 is complete and merged; repeat co-signing is not an alliance.
  - `outputs/coverage_audit_v1/`: current-layer six-dimension visibility-bias audit over 121 active actors, 283 active actor-issue edges, 130 active actor-place edges and 295 sources; the central 122/294/135 history boundary is retained in the brief. The current generation has 120 category cells, but cell count is not a stable contract. It is mechanical aggregation, so no HR-023 was created.
  - `outputs/R08_legal_procedure_v1/`: 27 accepted role×case rows across six human-checked cases, 54 role-family cells, two comparison figures and a report insert. It preserves 13 registered-actor roles versus 14 provisional nodes and creates no R8-specific HR task; HR-026 is now used by the election-civic candidate layer.
  - `outputs/edge_activation_v1/`: historical 18-actor/58-edge snapshot plus the post-HR013 evidence package. A094 is excluded; HR-024 is merged; HR-010 batch 6 accepted 46 rows as AI249–AI294 and left HR010-B6-019 deferred. A073 remains local/online-exhausted.
  - `outputs/registry_expansion_gate_v1/`: machine evidence gate retained as a pre-human audit snapshot. HR-013 overrides it: A111 added; C010/C034 background-only; C029-C033 rejected; C015 remains in HR-011.
  - `outputs/hr013_online_wave_integration_v1/`: human-decision overlay and 70-row source crosswalk; all source rows retain `relation_or_claim_approved=no`.
- Second post-audit online wave:
  - `outputs/R03_spatial_dossier_v1/`: 135 historical actor-place rows, of which 130 are active (53 reviewed/77 candidate) and 5 retired. HR-025 is complete; the active Sakishima dossier has 13 rows (Yonaguni 6/Ishigaki 3/Miyako 4), and AP123 is P007 Camp Foster.
  - `outputs/R09_election_civic_interface_v1/`: 19 human-reviewed actor-event observations across the 2014/2018/2022 gubernatorial elections: 18 confirm occurrence and one is announcement-only. No vote, turnout, outcome or policy causality is inferred.
  - `outputs/registry_value_gate_v2/`: five module-value candidates were gated; four HR-027 rows are now `add` and merged as A112–A115, while 八重山大地会 remains deferred for a continuity gap.
  - `outputs/R05_R07_heterogeneous_repertoire_v1/`: 148 existing formal observations reduce to 39 unique case/event×action×venue units across 15 action families and 9 venue groups. It adds no facts, so HR-028 is zero.
  - `outputs/schema_alias_freeze_v1/`: the final dependency-ordered regeneration preserved all 41 principal-confirmed HR-029 decisions, and the central actor/alias/place/venue/relation/action vocabulary merge is complete. P004 Futenma locality/issue and P010 MCAS Futenma installation remain separate; all 18 `R10_VENUE` placeholders are resolved or explicitly no-applicable-venue. The five formerly gated report figures still need final rerender/QA.
  - `outputs/next_wave_source_proposal_audit_v1/` and `outputs/next_wave_source_integration_v1/`: 50 proposal rows normalize to 49 URLs; two reuse S158/S204 and 47 provisionally enter as S248–S294. All claim approvals remain `no`; HR-030's 22 metadata/archive decisions are complete and merged.
  - `outputs/report_assembly_v1/` and `outputs/report_claim_audit_v1/`: 73 report resources remain the assembly inventory. HR-029's data gate and HR-031's three interpretive decisions are closed; HR-031 chose conservative B for sample-framework wording, visible place differences and parallel internationalization entries. Five figures still require final post-freeze rerender/QA before their manifest status changes. Plans are not contract artifacts: MA017–MA023 still track the report DOCX/PDF, paper, PPTX, Sakishima dossier DOCX, public-data bundle, final codebook/lint and missing prior-election-study input.
  - `outputs/report_assembly_v1/`: report assembly blueprint for 36 logical figures, 26 tables and 11 briefs; 22 figures are ready now, 5 require freeze, 9 are superseded. The recommended formal report is 32 pages; this package does not generate DOCX/PDF.
  - `outputs/human_review_orchestration_v1/`: historical pre-merge orchestration snapshot; use `docs/principal_human_review_remaining_v19.md` for the live 12-local-item human-decision ledger.
  - `outputs/R03_strict_place_issue_v1/`: 306 active same-source actor-place-issue triples; 299 are E3/E4, 81 dual-human-reviewed, and 97 have formal event attachment. The retired Cartesian projection is only a sensitivity upper bound.
  - `outputs/R02_actor_issue_robustness_v1/`: reviewed-only and S003/S004/S006 leave-out analysis. S004 materially shapes the international perimeter: ecology-to-international bridges fall 8→4 without it, while A001/A002/A009/A046 survive the combined three-source removal.
  - `outputs/translation_episode_comparison_v1/`: 13 analytical episodes across R8/R9 and four HR-027 event candidates. `data/metadata/episode_display_trilingual_v1.csv` adds the reviewed 13×7×3 display overlay without changing fact status. It separates venue entry/intermediate output from substantive project change; TE10–TE13 are not central event facts yet.
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
- Registry growth remains module/value-driven. HR-027 raised the registry history from 118 to 122; A072's duplicate resolution leaves 121 active actors. The current actor-issue graph has 5 active isolated actors; HR-019/024/025, HR-035 Batch 1/2 and HR-010 are merged. Do not reinsert A077–A085, A094, rejected AI178 or the A072 tombstone without a new human decision. MMC Tier B enters only as a separate mainland-solidarity layer when analytically justified; Tier C stays event-only.
- Existing `R14 coverage` outputs are a foundation coverage audit under the final DOCX numbering; final R14 is organizational genealogy and is an expansion module.
- Authoritative acceptance audit: `docs/phase1_scheme_acceptance_audit_v1.md`. Online/local sequencing remains in `docs/phase1_online_completion_plan_v0.md`; the current sub-agent execution briefs are in `docs/phase1_next_wave_execution_v2.md`.
- If delivered today, the conservative client verdict remains reject-and-rectify: the 120 minimum, first same-source place-issue layer and current online HR freeze are repaired, but 142 active actor-issue edges remain candidates and all final DOCX/PDF, paper, PPTX, Sakishima dossier, public-data bundle and final codebook/lint remain incomplete.
- Academic work now has 13 translation episodes plus reviewed-only and source-cluster sensitivity. Next add non-entry negative cases, identity-uncertainty sensitivity, and event-level review for HR-027 episodes; do not infer process from issue co-occurrence.

## Useful Commands

```powershell
python scripts\archive_sources.py
python scripts\archive_sources.py --retry-failed
python scripts\archive_sources.py --from-id 197 --to-id 198 --retry-failed
python scripts\archive_sources.py --from-id 213 --to-id 213 --retry-failed
python scripts\archive_sources.py --reconcile-cache-hashes
python scripts\normalize_actor_issue_tags.py
python scripts\merge_hr016_hr017_modules_v1.py
python scripts\merge_hr020_hr026_v1.py
python scripts\merge_hr018_hr021.py
python scripts\merge_hr018_main_relation_sample_v1.py
python scripts\merge_hr032_partner_crosswalk_v1.py
python scripts\render_r10_current.py
python scripts\render_r10_official_universe_current.py
python scripts\render_r06_r07_r11_current.py
python scripts\make_r08_legal_procedure_v1.py
python scripts\validate_registry_expansion_gate_v1.py
python scripts\integrate_hr013_online_wave.py
python scripts\make_r03_spatial_dossier_v1.py
python scripts\make_registry_value_gate_v2.py
python scripts\make_r05_r07_heterogeneous_repertoire_v1.py
python scripts\make_schema_alias_freeze_v1.py
python scripts\audit_next_wave_source_proposals_v1.py
python scripts\integrate_next_wave_sources_v1.py
python scripts\merge_hr035_batch02_v1.py
python scripts\make_r01_r02_actor_issue.py
python scripts\make_strict_place_issue_v1.py
python scripts\make_coverage_audit_v1.py
python scripts\make_research_wave_postfreeze_compatibility_v1.py
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
python scripts\make_human_review_orchestration_v1.py
python scripts\make_review_status_crosswalk_v1.py
python scripts\make_hr035_batch02_v1.py
python scripts\merge_confirmed_remaining_online_reviews_v1.py --stage upstream
python scripts\merge_confirmed_remaining_online_reviews_v1.py --stage freeze
python scripts\build_exploration_system_data_v1.py
python scripts\build_publication_snapshot_v1.py --profile client_preview
python scripts\build_publication_snapshot_v1.py --verify-only
python scripts\validate_phase1_data.py
```

After source-log or archive changes, rerun the archive script first, then regenerate explanatory and module packages.

The `merge_*` commands above are post-review reconstruction commands. Run them only while the corresponding completed human-return files remain present, and run `render_r06_r07_r11_current.py` after `merge_hr018_hr021.py`.

The following are pre-human-review or historical builders and must not be run against the current merged layer: `make_r04_sakishima_formal.py`, `make_r04_hr016_packet.py`, `make_r05_coaction_v1.py`, `make_r09_referendum_process.py`, `make_r09_election_civic_interface_v1.py`, `make_r10_admin_collaboration.py`, `make_r10_official_collaboration_universe_v1.py`, `make_edge_activation_v1.py`, `make_phase1_visuals.py`, `make_r06_r07_r11_pathways.py`, `make_review_status_crosswalk_v1.py`, and `make_schema_alias_freeze_v1.py`. The last two scripts are now pre-central-freeze provenance builders; rerunning them after HR-034/029 can fail or recreate obsolete blank review candidates. Preserve existing outputs and use the confirmed return/freeze manifests for current work.

Do not rerun `scripts/audit_report_claims_v1.py` until HR-031 and its hard-coded historical counts have been updated; use `scripts/reconcile_rca063_post_hr018.py` only for the bounded RCA063 release. `scripts/make_third_progress_sync_v2.py` is the historical six-figure builder and must not overwrite the present third-sync preparation package; use `scripts/render_formal_comm_v2_r5_current.py` for the current R5 figure 6.

## Communication Guidance

- The old `docs/progress_report_v1.md` is an internal draft, not a deliverable.
- Next boss-facing communication should use explanatory outputs, not only statistics.
- Safe current message: all returned online reviews through HR-035 Batch 2 are integrated. The registry has 122 history rows/121 active actors and actor–issue has 294 history/283 active edges (141 reviewed/142 candidate). The place-issue replacement has 306 active same-source triples (81 dual-reviewed). No assigned online human decision remains blank; twelve local/new-primary-material items remain. The exploration frontend now includes the complete 13×7×3 episode display layer and five bounded lifecycle anchors, and is built from a verified public publication snapshot rather than directly from research outputs. Nine method-ready modules still lack a complete adapter (four have bounded partial surfaces and five have no public module surface); final contract artifacts still do not exist.
- Keep all claims conservative: "publicly visible event participation", "candidate relation", "source-backed role", or "needs local retrieval" are preferred to over-strong network claims.
