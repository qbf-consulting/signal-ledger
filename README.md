# Signal Ledger

Signal Ledger is an evidence-backed change intelligence system for collecting governed source observations with explicit provenance and machine-verifiable structure.

The project is being built as reusable QBF infrastructure: domain-specific profiles can later define what sources are observed, what constitutes significance, and how changes are presented without coupling those judgments to the evidence substrate.

## Current status

**v0.1 bootstrap — observation and provenance baseline**

The current implementation provides:

- governed source records;
- strict observation records;
- canonical provenance fields;
- SHA-256 content digests;
- append-only persistence by observation identifier;
- JSON Schemas for sources and observations;
- a small CLI for validation, ingestion, and inspection;
- unit, conformance, storage, and CLI tests;
- CI across supported Python runtimes.

At this stage, an observation means:

> Signal Ledger observed that a configured source exposed this artifact at this time, using this collection path.

It does **not** mean that the propositions in the source are verified or true.

## Architecture

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

The future layers are intentionally not implemented in v0.1. See [Architecture](docs/architecture.md) and [Provenance](docs/provenance.md).

## Quick start

Requires Python 3.11 or later.

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
```

Validate a source:

```bash
signal-ledger validate-source tests/fixtures/source.json
```

Ingest an observation:

```bash
signal-ledger ingest-observation tests/fixtures/observation.json --store ./data
```

Inspect it:

```bash
signal-ledger inspect-observation obs.example.001 --store ./data
```

## End-to-end demonstration

A deterministic workflow exercises observations -> reconciliation -> claims/evidence -> significance -> run artifact without network or AI dependencies.

Run locally:

```bash
python -m signal_ledger.demo --output artifacts/first-run.json
```

See [First workflow run](docs/first-run.md).

## Repository discipline

Changes are expected to proceed through issue -> feature branch -> pull request, with tests and documentation updated alongside behavior. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licensing

This repository intentionally has no license at present. Do not assume permission to redistribute repository content beyond rights explicitly granted by QBF Consulting LLP.

## Contact

Security concerns should follow [SECURITY.md](SECURITY.md). General contact: ask@qbfconsulting.digital.
