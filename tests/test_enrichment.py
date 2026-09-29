from datetime import UTC, datetime

import pytest

from signal_ledger.enrichment import DerivationProvenance, Enrichment, NullEnricher, RuleEnricher


def provenance() -> DerivationProvenance:
    return DerivationProvenance(
        mechanism="test",
        model=None,
        prompt_version="v1",
        generated_at=datetime.now(UTC),
        evidence_refs=("obs.one",),
    )


def test_real_provider_produces_auditable_derived_output() -> None:
    items = RuleEnricher().enrich(
        "A trust registry update changes digital identity delegation.",
        ("obs.one",),
    )
    assert items
    assert {item.kind for item in items} == {"topic", "relevance_explanation"}
    assert all(item.provenance.evidence_refs == ("obs.one",) for item in items)
    assert all(item.provenance.prompt_version == "rules-v1" for item in items)


@pytest.mark.parametrize(
    "kind",
    ["evidence_state", "primary_evidence", "source_authority", "regulatory_state", "truth"],
)
def test_enrichment_cannot_claim_authoritative_state(kind: str) -> None:
    with pytest.raises(ValueError):
        Enrichment(kind, "verified", provenance())


def test_enrichment_export_preserves_derivation_provenance() -> None:
    item = RuleEnricher().enrich("AI governance research paper", ("obs.one",))[0]
    exported = item.export()
    assert exported["provenance"]["mechanism"] == "deterministic-rule"
    assert exported["provenance"]["evidence_refs"] == ["obs.one"]


def test_null_provider_remains_supported() -> None:
    assert NullEnricher().enrich("anything", ("obs.one",)) == ()
