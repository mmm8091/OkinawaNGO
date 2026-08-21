# U.S.-presence accountability reconnaissance v1

Date: 2026-08-19

Status: `research_only / 9 principal decisions complete / no central writeback / not frontend-ready`

This package extends the U.S.-origin accountability/public-diplomacy side of the current database. Nine field-level decisions are complete, but no approved change has yet been merged into central actor, person, relation or source tables.

## Counts

- scoped U.S.-origin actors: 8 (six accountability actors plus one public-diplomacy program and one funder watchlist);
- new official-source proposals: 7;
- typed resource observations: 2;
- public person-role observations: 11;
- action/relation observations or existing-role crosswalks: 9;
- bounded searches: 6;
- principal review items: 9.

## Reading order

1. `accountability_actor_scope_v1.csv`
2. `resource_observations_v1.csv`
3. `person_role_observations_v1.csv`
4. `action_relation_observations_v1.csv`
5. `official_source_proposals_v1.csv`
6. `bounded_search_log_v1.csv`
7. `human_review_queue_v1.csv`
8. `../../docs/us_presence_accountability_recon_brief_v1.md`

## Strongest new candidate facts

1. Earthjustice's official FY2021 Form 990 lists `1272 OKINAWA DUGONG` at USD 276,345.50 under court-awarded attorney fees and costs. A separate Judgment Fund record shows USD 280,000; the two amounts are not merged and do not create a simple OSD→Earthjustice money edge.
2. Official Veterans For Peace records identify chapter 1003 Ryukyu/Okinawa and named people. The original USAA005 A019 endpoint has been withdrawn; the corrected coalition target remains event-only/off-graph. Hideki Yoshikawa's same-date OEJP/SDCC person bridge is approved without creating an organization alliance.
3. Friends of the Earth U.S. now has two discrete Okinawa event observations, 2015 and 2019. Pacific Environment remains bounded mainly to the 2015 Okinawa event; neither supports a continuous project claim.

## Hard boundaries

- A case-level fee/cost amount is not a donor or funding-source identification.
- A funding opportunity is not an award.
- Shared event participation is not an alliance.
- Named coalition work is not membership or funding.
- A bounded negative search is not evidence of real-world absence.
- New source URLs stay in this proposal package until source-log/archive review.

The formal review record is `docs/human_review_return_USN_accountability_v1.md`; the package `manifest.json` remains the immutable pre-human generation receipt, so its queue/README hashes refer to dispatched bytes.
