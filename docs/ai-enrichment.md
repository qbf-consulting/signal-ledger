# Optional AI enrichment

AI enrichment is an optional derived layer, not an authority layer.

Permitted uses include candidate event clustering, claim extraction, entity-resolution suggestions, translation, topic tagging, relevance explanation, and contradiction-candidate discovery.

Every non-null enrichment provider must persist derivation provenance: mechanism, model identifier where applicable, prompt/rule version, generation timestamp, and evidence references.

AI output cannot directly establish truth, regulatory status, source authority, publication state, or final assurance state. The default `NullEnricher` proves that the deterministic core has no AI-provider dependency.
