# Provenance

## Evidence boundary

Signal Ledger distinguishes source material from statements derived by the system.

An **Observation** is evidence that a configured source exposed a particular artifact at a retrieval time. It is not, by itself, evidence that every proposition contained in that artifact is true.

## Required provenance fields

Every observation records:

- source identifier;
- canonical artifact URI;
- retrieval timestamp;
- collection method;
- collector identifier;
- SHA-256 content digest;
- optional published timestamp;
- optional source version marker such as an ETag or upstream revision.

## Digest semantics

`content_digest` uses the form:

```text
sha256:<64 lowercase hexadecimal characters>
```

Collectors are responsible for defining the exact bytes or canonical representation that were hashed. Collector-specific canonicalization rules must be documented before production collection is introduced.

## Mutation

The v0.1 store is append-only by observation identifier. Correction or supersession semantics are intentionally deferred. Future implementations must represent correction as additional state/evidence rather than silently rewriting historical observation records.
