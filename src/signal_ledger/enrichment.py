from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Protocol

ALLOWED_DERIVED_KINDS = frozenset({"candidate_claim", "topic", "relevance_explanation"})
PROHIBITED_AUTHORITY_KINDS = frozenset(
    {"evidence_state", "primary_evidence", "source_authority", "regulatory_state", "truth"}
)


@dataclass(frozen=True)
class DerivationProvenance:
    mechanism: str
    model: str | None
    prompt_version: str | None
    generated_at: datetime
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class Enrichment:
    kind: str
    value: str
    provenance: DerivationProvenance

    def __post_init__(self) -> None:
        if self.kind not in ALLOWED_DERIVED_KINDS:
            raise ValueError(f"enrichment kind cannot establish authoritative state: {self.kind}")

    def export(self) -> dict[str, object]:
        payload = asdict(self)
        payload["provenance"]["generated_at"] = self.provenance.generated_at.isoformat()
        payload["provenance"]["evidence_refs"] = list(self.provenance.evidence_refs)
        return payload


class Enricher(Protocol):
    def enrich(self, text: str, evidence_refs: tuple[str, ...]) -> tuple[Enrichment, ...]: ...


class NullEnricher:
    """Default deterministic provider: produces no derived content."""

    def enrich(self, text: str, evidence_refs: tuple[str, ...]) -> tuple[Enrichment, ...]:
        return ()


class RuleEnricher:
    """Versioned deterministic provider that proves the auditable enrichment contract."""

    VERSION = "rules-v1"
    TOPICS = {
        "digital-trust": ("trust registry", "verifiable credential", "digital identity", "delegation"),
        "ai-governance": ("ai governance", "ai regulation", "artificial intelligence"),
        "research": ("paper", "study", "research"),
    }

    def enrich(self, text: str, evidence_refs: tuple[str, ...]) -> tuple[Enrichment, ...]:
        normalized = text.casefold()
        now = datetime.now(timezone.utc)
        provenance = DerivationProvenance(
            mechanism="deterministic-rule",
            model="signal-ledger-rule-enricher",
            prompt_version=self.VERSION,
            generated_at=now,
            evidence_refs=evidence_refs,
        )
        derived = []
        for topic, terms in self.TOPICS.items():
            matches = tuple(term for term in terms if term in normalized)
            if matches:
                derived.append(Enrichment("topic", topic, provenance))
                derived.append(
                    Enrichment(
                        "relevance_explanation",
                        f"Matched {topic} terms: {', '.join(matches)}",
                        provenance,
                    )
                )
        return tuple(derived)
