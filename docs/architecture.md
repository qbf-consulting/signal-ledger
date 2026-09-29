# Architecture

## Purpose

Signal Ledger is an evidence-backed change intelligence system. The initial implementation deliberately begins below the level of events, claims, significance, or editorial presentation.

The v0.1 architecture establishes one durable proposition:

> An observation records what a governed source presented, when Signal Ledger retrieved it, and how that observation can be traced. It does not establish that the observed statement is true.

## Layering

```text
Source Registry
      |
      v
Observation
      |
      v
Append-only evidence substrate

Future layers:
Observation -> Claim -> Event -> Evidence State -> Assessment -> Publication
```

Each future layer must preserve references to the evidence from which it was derived. Derived judgments must not silently acquire the authority of their source material.

## Current invariants

1. **Stable identifiers** — sources and observations have explicit identifiers.
2. **Append-only observation identity** — an existing observation identifier cannot be overwritten through the storage API.
3. **Provenance retention** — retrieval time, collection method, collector identity, source version, and content digest survive persistence.
4. **Strict models** — unknown fields are rejected.
5. **No implicit truth claim** — persistence means “observed”, not “verified”.
6. **No AI dependency** — the core evidence layer is deterministic and locally testable.

## Deliberately deferred

Event reconciliation, claim extraction, contradiction resolution, significance assessment, topic/radar profiles, UI publication, and bounded AI enrichment are separate implementation propositions.
