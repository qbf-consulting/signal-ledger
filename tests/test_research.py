from signal_ledger.research import ResearchCandidate


def test_research_candidate_handoff_preserves_provenance() -> None:
    candidate = ResearchCandidate(
        observation_id="obs.paper.one",
        canonical_uri="https://example.org/paper",
        title="Example governance paper",
        discovery_channel="exploration-sample",
        evidence_refs=("obs.paper.one",),
    )
    exported = candidate.export()
    assert exported["schema"] == "signal-ledger.research-candidate.v1"
    assert exported["evidence_refs"] == ["obs.paper.one"]
    assert exported["discovery_channel"] == "exploration-sample"
