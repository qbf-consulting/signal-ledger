from __future__ import annotations

from .models import Claim, EvidenceState


def assess_claim(claim: Claim) -> EvidenceState:
    if claim.challenging_observation_ids:
        return EvidenceState.CONTRADICTORY
    if not claim.primary_evidence_observation_ids:
        return EvidenceState.INDETERMINATE
    if set(claim.primary_evidence_observation_ids) <= set(claim.supporting_observation_ids):
        return EvidenceState.VERIFIED
    return EvidenceState.PARTIALLY_VERIFIED
