from signal_ledger.enrichment import NullEnricher


def test_core_operates_without_ai_provider() -> None:
    assert NullEnricher().enrich("input", ("obs.one",)) == ()
