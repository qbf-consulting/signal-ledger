from signal_ledger.evidence import assess_claim
from signal_ledger.models import Claim, EvidenceState


def claim(**changes) -> Claim:
    payload = {
        "id": "claim.example",
        "statement": "A material change occurred.",
        "event_id": "event.example",
        "supporting_observation_ids": (),
        "challenging_observation_ids": (),
        "primary_evidence_observation_ids": (),
    }
    payload.update(changes)
    return Claim(**payload)


def test_missing_primary_evidence_is_indeterminate() -> None:
    assert assess_claim(claim(supporting_observation_ids=("obs.one",))) == EvidenceState.INDETERMINATE


def test_conflicting_evidence_is_contradictory() -> None:
    item = claim(
        supporting_observation_ids=("obs.one",),
        challenging_observation_ids=("obs.two",),
        primary_evidence_observation_ids=("obs.one",),
    )
    assert assess_claim(item) == EvidenceState.CONTRADICTORY


def test_primary_support_can_verify() -> None:
    item = claim(
        supporting_observation_ids=("obs.one",),
        primary_evidence_observation_ids=("obs.one",),
    )
    assert assess_claim(item) == EvidenceState.VERIFIED
