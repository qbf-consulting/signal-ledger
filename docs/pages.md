# Publication and GitHub Pages

Signal Ledger distinguishes execution from publication.

```text
observations -> events -> claims/evidence -> assessment
                    |
                    v
              assured run artifact
                    |
                    v
             publication gate
                    |
                    v
       signal-ledger.publication.v1
                    |
                    v
        Pulse / Ledger / Methodology
```

## Publication contract

A Pages deployment consumes only a validated publication snapshot. The snapshot contains:

- `manifest.json` — schema, generation time, profile, counts and content digest;
- `pulse.json` — material-change summary and run-derived counts;
- `events.json`;
- `claims.json`;
- `assessments.json`;
- `observations.json`.

The digest covers the publication payload. The renderer fails closed if the payload no longer matches the manifest.

Collection is not publication. Interpretation is not publication. The publication builder is the explicit boundary between working ledger state and public output.

## Public views

**Pulse** is the homepage and answers *what changed?*

**Ledger** exposes the event, claim/evidence state and significance assessment behind the Pulse.

**Methodology** explains the evidence and authority boundaries and exposes publication provenance.

The machine-readable snapshot is also copied under `/data/` in the Pages artifact.

## Current limitation

The current Pages workflow uses the deterministic conformance run as its publication input. This closes the architectural publication gap, but it is not yet a live-source intelligence feed. The next pilot should replace that input with a governed real-source collection run without changing the publication contract.

## Reproduce

```bash
python -m signal_ledger.demo --output artifacts/run.json
python -m signal_ledger.publication --run artifacts/run.json --output-dir publications/latest
python -m signal_ledger.site --publication-dir publications/latest --output-dir _site
```
