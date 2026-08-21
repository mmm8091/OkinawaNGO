# U.S.-presence service/charity reconnaissance v1

Status: `research_only` / 13 principal decisions complete / not merged into central tables / not frontend-ready.

Observed on: 2026-08-19. Research period: 2012–2026. This package is an additive reconnaissance layer over the H2 nine-actor service core. It does not modify the registry, source log, relation sample, human-review ledger, publication snapshots or `outputs/formal_comm_v3/`.

## What this pass adds

- Rechecks all 9 H2 service-core actors against current organization, IRS-derived and military/installation records.
- Screens the current MCIPAC/MCCS private-organization page. The page displays 81 entries in a combined Okinawa/Camp Fuji/MCAS Iwakuni universe; **81 is not an Okinawa actor count**.
- Surfaces 4 high-priority missing candidates: Marine Thrift Shop Okinawa, Marine Gift Shop, Neighborhood Pantry–Camp Butler and North Island Okinawa Spouses Club.
- Separates people (29 role candidates), resource flows (14), recipient observations (16) and relationship/legitimacy language (12).
- Proposes 38 sources for later archival and human review. Source proposals do not approve claims or relations.

## Evidence channels

1. **Official/installation records** establish authorization, office presence, program availability and military-reported events. They do not independently establish recipient experience.
2. **IRS-derived filings** establish filing-period legal status, officers, totals and reported grant categories. This package uses ProPublica as an interface; central merge requires inspection of the underlying filing image/XML.
3. **Organization records** establish self-description, named boards, recipient lists and organizer language. They remain interested-party sources.
4. **Military public-affairs stories** can support dated reported transfers or quoted language, but are not neutral evaluations of community effects.

## Resource-flow contract

- `currency` contains only the ISO-style code `USD`; qualifications belong in `amount_semantics`.
- `amount_semantics` distinguishes `exact_reported`, `minimum_reported`, `equivalent_valuation`, `aggregate_reported` and `pledge_commitment`.
- `transaction_chain_id` and `flow_step_no` are populated only when a source identifies an intermediary step. RF006 records Marine Thrift Shop → Lions Clubs as step 1; the unnamed downstream institutions are not synthesized.
- Every other flow leaves the chain ID and step blank and explains in `transaction_chain_note` whether it is direct, aggregate or otherwise not decomposable.
- RF001 is a deferred anomalous filing observation: the USD 2,580 label appears in an individual-assistance table without organization-recipient fields. It is not a precise KOSC→AWWA flow. F025 remains a separate historical bounded relation.

## LEG0–LEG3 interpretation gate

- **LEG0 — service/resource fact:** a service exists, a transfer is reported, or a program has a named service population. This package has3 explicit LEG0 observations plus the separate flow and recipient tables.
- **LEG1 — source narrative:** an organization, officer or military story uses terms such as `goodwill`, `friendship`, `bond`, `bridge`, `unity` or `community partnership`. This package has9 LEG1 observations.
- **LEG2 — bounded response:** a recipient, local institution or independent source records acceptance, relay, resistance or reinterpretation. Candidate rows must be created separately with a precise response subject and locator.
- **LEG3 — effect:** repeatable attitude, behavior or institutional effects are supported by a baseline, comparison or explicit research design. **No LEG3 evidence is established in this package.**

Charity is therefore not coded as pro-base or as legitimation. The analytical proposition is narrower: recurring services and transfers may provide material infrastructure and a vocabulary through which the U.S. presence is represented as socially useful; whether that representation is received, contested or ignored remains an empirical question.

## Files

| File | Rows | Purpose |
|---|---:|---|
| `service_actor_universe_v1.csv` | 18 | Existing core, missing candidates and scope leads |
| `person_role_candidates_v1.csv` | 29 | Time-bounded officer/staff candidates |
| `resource_flow_candidates_v1.csv` | 14 | Amount/date/purpose typed flow candidates |
| `service_recipient_candidates_v1.csv` | 16 | Named and aggregate recipient observations |
| `legitimation_claim_observations_v1.csv` | 12 | LEG0 service and LEG1 narrative observations; original row labels await mechanical migration |
| `source_proposals_v1.csv` | 38 | Unmerged source proposals |
| `negative_search_log_v1.csv` | 11 | Targeted searches with unresolved outcomes |
| `coverage_gaps_v1.csv` | 10 | Evidence gaps and next retrieval routes |
| `human_review_queue_v1.csv` | 13 | Principal decision queue; 13/13 decisions complete |
| `manifest.json` | — | Immutable pre-human generation receipt; queue/README hashes refer to dispatched bytes |

The principal-facing task book is `docs/human_review_assignment_USN_service_ecology_v1.md`; research support and the formal return are `docs/human_review_research_USN_service_ecology_v1.md` and `docs/human_review_return_USN_service_ecology_v1.md`.

## Safe use

- Use actor rows to plan expansion, not to change the central registry.
- Use flow rows as candidate facts. Aggregate scholarship/service populations never become organization edges.
- Read `amount` together with `currency` and `amount_semantics`; never move `minimum` or `equivalent` qualifiers into the currency field.
- Keep membership, donation, sponsorship, program support and beneficiary observations as different relation types.
- Keep filing-period roles distinct from present-day roles.
- Do not infer ACGO dissolution from filing cessation or roster absence.
- Do not infer that every MCIPAC roster entry is Okinawa-based.
- Human review is complete, but controlled integration and publication-adapter gates remain incomplete; do not expose this package directly in the client frontend.
