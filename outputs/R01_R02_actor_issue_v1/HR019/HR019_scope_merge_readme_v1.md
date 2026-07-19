# HR-019 scope review merge

- All 76 selected actor-issue edges now carry a principal-reviewed scope classification.
- Scope review does not automatically elevate an AI-seeded factual edge to `human_checked`.
- Seven `remain_unclear` mappings are deactivated; their prior source references are preserved in `invalidated_source_ref` rather than left as apparent support.
- Thirty bridge interpretations are stored in a separate analytical layer. They do not create actor relations, alliances or influence scores.
