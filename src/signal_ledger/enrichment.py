from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


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


class Enricher(Protocol):
    def enrich(self, text: str, evidence_refs: tuple[str, ...]) -> tuple[Enrichment, ...]: ...


class NullEnricher:
    """Default deterministic provider: produces no derived content."""

    def enrich(self, text: str, evidence_refs: tuple[str, ...]) -> tuple[Enrichment, ...]:
        return ()
