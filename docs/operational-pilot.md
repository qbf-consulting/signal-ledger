# Operational pilot

The operational pilot is the first end-to-end public intelligence path:

```text
governed public feeds
  -> collection evidence
  -> normalized feed items
  -> deterministic profile relevance
  -> consumer Signals
  -> digest-protected operational publication
  -> Pulse / Evidence / Methodology
```

The source registry is `sources/pilot.json`. Sources are intentionally bounded and primarily official or standards/community publishers. Authority is scoped: a publisher is authoritative for its own publication/status, not automatically for every proposition in an item.

The workflow runs every six hours and may also be dispatched manually. Network failures are recorded in the publication rather than silently omitted.

## MVP evidence semantics

A single official/primary-source match is published as `partially_verified`: the publication itself is observed, but broader propositions have not been independently corroborated. Community-source matches are `indeterminate`.

This is deliberately conservative. Future reconciliation can combine observations into events and promote evidence state only when deterministic evidence rules justify it.

## Consumer Signal

A Signal contains a human-readable headline, source summary, domain, why-it-may-matter explanation, evidence state, authority scope, source URI, digest, retrieval time, matched terms and explicit uncertainty.

Internal ledger identifiers are not the primary consumer interface.
