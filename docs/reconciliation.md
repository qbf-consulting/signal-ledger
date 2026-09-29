# Event reconciliation

Event reconciliation is deterministic in v0.2. Observations are grouped only when their normalized titles are identical. This is intentionally conservative: false separation is preferable to an unsupported merge.

An Event is derived state. It retains every contributing observation identifier. Multiple reports therefore increase corroborating evidence without multiplying the number of events.

The reconciliation key is inspectable. Future similarity or AI-assisted clustering must be introduced as candidate derivation, retain provenance, and pass false-merge conformance tests before it can affect canonical event state.
