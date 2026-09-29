# Auditable enrichment providers

Signal Ledger enrichment is a derived layer. Providers may propose candidate claims, topics and relevance explanations, but cannot establish authoritative ledger state.

## First executable provider

`RuleEnricher` is the first non-null provider. It is deliberately deterministic and network-independent. Its purpose is to prove the complete enrichment/provenance contract before adding a model-backed adapter.

Every output records:

- mechanism;
- provider/model identifier;
- rule or prompt version;
- generation timestamp;
- evidence references.

Allowed derived kinds are currently `candidate_claim`, `topic`, and `relevance_explanation`.

The enrichment model rejects kinds representing `evidence_state`, `primary_evidence`, `source_authority`, `regulatory_state`, or `truth`. Those remain governed by deterministic ledger semantics and evidence policy.

## Future LLM adapter

A future LLM provider must implement the same `Enricher` contract and preserve equivalent provenance. It should be optional and provider-neutral. Model output must pass the same allowed-kind validation and cannot mutate source observations, event reconciliation, source authority, or evidence state.

This design allows model-assisted discovery without turning model inference into authority.
