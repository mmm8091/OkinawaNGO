# US presence multilayer network architecture v1

Date: 2026-08-19

Status: `research_only / architecture_proposal / not_frontend_ready / no_central_writeback`

## Purpose

This package specifies the data contracts and gates for studying how observable NGO/civic actions and
relations constrain, hold accountable, mitigate, reproduce, mediate across the base–local-society
boundary, or attempt to legitimate U.S. military
presence in Okinawa. It does not classify organizations as pro-U.S. or anti-U.S., and it contains no
new factual extraction.

## Files

- `proposed_table_contracts_v1.csv`: table grain, keys, required fields, evidence gates, graph rules,
  time semantics, and prohibited inferences.
- `coding_vocabulary_v1.csv`: controlled vocabulary for function, evidence basis, endpoint types,
  relation types, time, and network eligibility.
- `validation_rules_v1.csv`: machine and human validation gates.
- `vertical_slice_register_v1.csv`: independently acceptable tracer-bullet work packages.
- `../../docs/us_presence_network_architecture_v1.md`: rationale, compatibility map, analytical
  boundaries, and recommended execution order.

## Governing boundary

The existing central tables and frontend remain unchanged. Existing central and research-only rows may
be referenced by `provenance_input_ids`, but this architecture does not upgrade their review status,
create actors, create person identities, create funding edges, or approve interpretations.

## Central design decisions

1. Function is coded on a dated action, role, or relation observation, never as an essential actor
   stance.
2. Money, people, service recipients, affiliation/control, and action/institution remain separate
   network layers.
3. `community_mediation` records a reviewed resource/service/referral interface crossing the
   base–local-society boundary. It is distinct from `garrison_reproduction` and does not itself establish
   political acceptance, legitimation, dependency, influence, or continuity.
4. A donation, service, or community-mediation observation is not legitimation evidence by itself.
5. Unobserved cross-group relations become a reportable negative result only after a frozen selection
   frame, symmetric search, explicit source-family coverage, and separate measurement of organization,
   person, and recipient interfaces.
6. Network metrics remain ineligible until one relation family has reviewed endpoints, direction,
   time, a declared denominator, a missingness report, and sensitivity checks.

## Package counts

- 10 proposed table contracts;
- 70 controlled-vocabulary rows;
- 44 validation rules;
- 10 tracer-bullet slices.

## Suggested first run

Execute `US-VS00` and `US-VS01` first. They answer the client-facing directory question and retype
existing observations without new factual claims. Then run one garrison-reproduction tracer
(`US-VS02`) and one accountability tracer (`US-VS03`) as a paired comparison. Pause for principal
review before expanding the wave.
