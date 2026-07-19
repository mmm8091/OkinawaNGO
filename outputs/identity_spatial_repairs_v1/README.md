# Identity and spatial blocking repairs v1

Principal-approved HR-019/HR-025 identity, scope and place-key decisions were applied to the central tables by `scripts/merge_identity_spatial_repairs_v1.py`.

Important boundaries:

- A072 is a provenance tombstone (`merged_duplicate_of=A071`), not an active actor.
- A068 was renamed, but lifecycle/genealogy candidates remain undecided.
- AP049 uses P021 Sakishima as a whole and remains source-ID-integration pending; it must not fan out to three island municipalities.
- AP048/AP118 and duplicate A072 issue edges remain in the tables as rejected/retired provenance rows and must not enter figures.
- New review-report URLs were not silently inserted into the central source log.
