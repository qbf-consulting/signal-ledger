from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ResearchCandidate:
    observation_id: str
    canonical_uri: str
    title: str
    discovery_channel: str
    evidence_refs: tuple[str, ...]

    def export(self) -> dict[str, object]:
        return {
            "schema": "signal-ledger.research-candidate.v1",
            "observation_id": self.observation_id,
            "canonical_uri": self.canonical_uri,
            "title": self.title,
            "discovery_channel": self.discovery_channel,
            "evidence_refs": list(self.evidence_refs),
        }
