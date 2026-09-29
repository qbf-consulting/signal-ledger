# Signal Ledger

Signal Ledger is an evidence-backed change intelligence system that preserves the distinction between what a source said, what event the observations describe, what claims can be supported, and what judgments are derived from that evidence.

It is reusable QBF infrastructure: domain profiles can define sources, significance dimensions, and downstream views without changing the underlying evidence substrate.

## Current status

**v0.4 architectural prototype — executable end-to-end baseline**

Implemented capabilities include:

- governed source and observation records with explicit provenance;
- append-oriented observation persistence and SHA-256 content digests;
- deterministic, conservative observation-to-event reconciliation;
- explicit event and entity models;
- claims with supporting, challenging, and primary-evidence references;
- evidence states including indeterminate, partially verified, verified, contradictory, and superseded;
- decomposed, evidence-linked significance assessments rather than an opaque importance score;
- change detection across significance assessments;
- a Digital Governance Paper Notes research-candidate interoperability profile;
- a provider-neutral, optional AI-enrichment interface with derivation provenance;
- JSON Schemas and machine-readable profiles;
- CLI validation, ingestion, and inspection operations;
- unit and conformance tests across Python 3.11, 3.12, and 3.13;
- an end-to-end GitHub Actions assurance run that emits a machine-readable evidence artifact.

An observation means:

> Signal Ledger observed that a configured source exposed this artifact at this time, using this collection path.

It does **not** mean that propositions in the source are verified or true. Events, claims, evidence states, and significance assessments are separate derived layers with their own evidence requirements.

## Architecture

```text
Governed Source
      |
      v
Observation + provenance
      |
      v
Deterministic reconciliation
      |
      v
Event
      |
      v
Claim
      |
      v
Evidence state
      |
      v
Significance assessment
      |
      v
Change-oriented output

Optional overlays:
- domain/research profiles
- auditable AI enrichment
```

See [Architecture](docs/architecture.md), [Provenance](docs/provenance.md), [Reconciliation](docs/reconciliation.md), [Evidence states](docs/evidence-states.md), [Significance model](docs/significance-model.md), and [AI enrichment](docs/ai-enrichment.md).

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

The deterministic demonstration exercises observations -> reconciliation -> claims/evidence -> significance -> run artifact without network or AI dependencies.

```bash
python -m signal_ledger.demo --output artifacts/first-run.json
```

See [First workflow run](docs/first-run.md).

## Research Radar interoperability

Signal Ledger does not replace the Digital Governance Paper Notes Radar. The research profile defines a provenance-preserving candidate handoff so the two approaches can be evaluated comparatively before any production workflow changes. See [Research Radar interoperability](docs/research-radar-interoperability.md).

## Repository discipline

Changes proceed through issue -> feature branch -> pull request, with tests and documentation updated alongside behavior. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licensing

Signal Ledger follows the QBF Consulting mixed-license convention. Executable and machine-readable artifacts are licensed under **Apache-2.0**; specifications, documentation, governance prose, diagrams, and narrative examples are licensed under **CC BY 4.0**. See [LICENSE](LICENSE), [LICENSE-CODE](LICENSE-CODE), [LICENSE-CONTENT](LICENSE-CONTENT), [NOTICE](NOTICE), and the machine-readable [artifact license policy](artifact-license-policy.json). Artifact-specific and inherited provenance notices take precedence.

## Security and contact

Report security concerns using the private process in [SECURITY.md](SECURITY.md). General contact: ask@qbfconsulting.digital.
