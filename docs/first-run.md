# First workflow run

The `Signal Ledger First Run` workflow is a deterministic, network-independent end-to-end smoke run.

It exercises:

```text
Observation fixtures
  -> reconciliation
  -> Event
  -> Claim
  -> evidence-state assessment
  -> significance dimensions
  -> machine-readable run artifact
```

The run artifact uses schema identifier `signal-ledger.run.v1` and retains observation/evidence references at every derived layer represented in the demo.

The workflow runs when relevant implementation changes reach `main` and can also be manually dispatched. It uploads `signal-ledger-first-run` containing `first-run.json`.

This is a conformance demonstration, not a live-source production collection. Live collectors require separate source-governance and collection-policy work.
