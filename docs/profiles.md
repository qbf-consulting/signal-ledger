# Governed profiles

Profiles are policy overlays over canonical Signal Ledger evidence. They answer domain-specific questions such as *is this relevant to digital trust?* or *which significance dimensions should this research profile inspect?*

They do not modify observations, reconcile events, designate primary evidence, or set evidence states.

Every shipped profile validates against `schemas/profile.schema.json` and declares:

- purpose;
- preferred source classes and authority expectations;
- inclusion and exclusion terms;
- significance dimensions;
- optional discovery channels and candidate lanes;
- output semantics.

## Shipped profiles

- **AI Governance** — regulation, standards, governance and deployment accountability.
- **Digital Trust** — identity, credentials, trust registries, delegation and assurance.
- **Digital Governance Paper Notes** — research discovery and editorial handoff.

The Paper Notes profile deliberately includes four candidate lanes: established-interest, adjacent-domain, exploratory and counter-thesis. This makes discovery diversity explicit and testable rather than relying solely on prior topics or known authors.

Profile relevance is derived judgment. A positive profile match does not increase source authority or evidence strength.
