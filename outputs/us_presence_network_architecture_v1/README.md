# US presence multilayer network architecture v1

Date: 2026-08-19

Status: `research_only / principal_checkpoint_confirmed / not_frontend_ready / no_central_writeback`

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
- `principal_checkpoint_return_v1.json`: machine-readable five-item principal decision record.
- `../../docs/human_review_return_USN_architecture_checkpoint_v1.md`: formal decision return and boundaries.

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

## Current next action

US-VS00/01 review inputs and the five-item checkpoint are complete. First prepare a controlled
integration design, expected field-level diff and idempotent test plan; do not write central tables.
The pre-return CSV contracts retain L1/L2/L3 suffixes as legacy aliases for approved
LEG1/LEG2/LEG3 semantics. Migrate those codes mechanically before integration, preserving all
non-target fields and package row counts. After integration design review, run USN-04/05/06 one
bounded research-only slice at a time.
