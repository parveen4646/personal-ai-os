# Memory Service design

A memory contains user-scoped text, a typed classification, importance from 0 to 1, and JSON metadata. The initial API supports explicit creation and retrieval so clients can be built now.

Future work:

- Extract candidates from conversations with an LLM and require explicit retention rules.
- Store versioned embedding vectors using pgvector.
- Retrieve by user, type, recency, importance, and semantic similarity.
- Add provenance, expiry, conflict resolution, and access controls.

The service is the source of truth for long-term memory; agents should call its API rather than write directly to its database.
