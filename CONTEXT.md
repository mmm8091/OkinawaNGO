# CONTEXT.md

## Project

Okinawa NGO / civic organization network research.

## Phase 1 Goal

Build a verifiable, expandable initial data base for organizations, issues, places, sources, and candidate relationships around Okinawa base politics, environmental framing, life safety, local autonomy, legal procedures, international advocacy, Sakishima / Yonaguni security concerns, and related external NGO / service / funding observation layers.

Phase 1 does not claim to cover all post-1972 Okinawa NGOs or all NPO corporations.

## Core Research Question

How do Okinawa civic organizations / NGOs translate base issues into environmental protection, life safety, local autonomy, human rights, legal procedures, and international advocacy? What public roles do these organizations play around Henoko, Yonaguni, Sakishima, and other key sites?

## Key Terms

- **actor**: A civic organization, NGO, project/network, service organization, sponsor, public institution, or other node included in the registry.
- **source**: A public record used to support an actor, issue, place, or relationship.
- **candidate edge**: A provisional relationship recorded for review; not a final analytic claim.
- **evidence_level**: E0-E4 confidence scheme used to separate confirmed evidence from leads.
- **human review**: Human judgment over explicitly named facts or fields. It does not automatically approve every field in the same row.
- **review_status**: Workflow state of a record. It is separate from evidence strength, the human decision, claim strength, and display eligibility.
- **human_decision**: The principal's accept, revise, defer, or reject decision for a stated review scope.
- **claim_status**: Whether the current material supports a claim fully, supports it with explicit limits, leaves it as a candidate/lead, or does not support it.
- **supported_bounded**: A claim whose core relation or observation is accepted while named fields such as amount, period, recipient scope, or endpoint identity remain incomplete and visible.
- **graph_eligibility**: The semantic form in which a record may be visualized, such as dyadic relation, case role, event participation, aggregate observation, research lead, genealogy anchor, or excluded.
- **reviewed view**: The default frontend layer containing supported and supported-bounded records. It replaces the user-facing term “demo view.”
- **research view**: The frontend layer that adds visibly marked candidates and research leads without changing reviewed-layer wording.
- **event-only participant**: A name supported for participation in a specific event but lacking enough identity/continuity evidence for the actor registry. Event-only names must not be counted as organizations or treated as stable network members.
- **local material collection**: Collection of local/offline/hard-to-access materials such as library database records, organizational reports, activity booklets, or local archives.
- **central fact**: A source-traceable record admitted to the project's authoritative fact layer under the current coding and review rules. It is not automatically an interpretation or general finding.
- **research observation**: A reviewable phenomenon recorded within a named material and selection boundary. It may remain module-specific or provisional and does not become a central fact merely because it is useful.
- **analytic result**: A reproducible comparison, count, sequence, projection, or sensitivity result derived from stated observations, units, denominators, selection rules, and a method version.
- **research claim**: A bounded interpretive statement supported by one or more analytic results and carrying its strength, competing explanations, and prohibited extrapolations.
- **research module**: A question-centered body of observations, evidence, method, results, claims, exhibits, and known gaps. A module's completion and display eligibility are separate judgments.
- **exhibit**: A figure, table, map, timeline, or interactive view used to explain or inspect a research result or claim. Its visual availability does not give it independent evidentiary status.
- **method_status**: Whether an observation, result, or exhibit was produced by a method adequate for its stated use. It is separate from evidence strength, review workflow, claim strength, and frontend implementation.
- **publication snapshot**: An immutable, self-consistent projection of approved research objects for a named audience and research state. It is a publication boundary, not a new source of facts.
- **release profile**: A controlled rule set determining which research objects, fields, and interpretation levels belong in a publication snapshot for a named audience.
- **core publication surface**: An exact file or JSON-pointer projection from the internal exploration builder that has an explicit profile, catalog owner or architecture role, frontend consumer and interpretation limit. A builder manifest proves provenance; the core-surface registry grants publication eligibility.
- **partial bounded surface**: A method-safe fact or navigation subset already visible in the frontend while its full research module still lacks the required adapter, comparison, source drilldown or method card. It must not be reported as a completed integrated module.
- **retired artifact**: A prior figure, table, dataset, or view withdrawn from current evidentiary or explanatory use after a method, data, or scope correction. It remains available only for provenance and audit unless a new review explicitly restores it.

## Main Cautions

- Do not equate co-signing with stable alliance.
- Do not write grant opportunities as awarded grants.
- Do not treat service NGOs as political stance actors unless public evidence supports it.
- Do not over-environmentalize Yonaguni; its stronger frame is frontline/security environment, local autonomy, referendum, Taiwan proximity, and health/life-safety concerns.
- The original Phase-1 DOCX is the acceptance contract. Current internal status and next work are controlled by `docs/phase1_workbench.md` and `docs/phase1_scheme_acceptance_audit_v1.md`; the second progress-sync package is a historical client snapshot, not current acceptance status.
