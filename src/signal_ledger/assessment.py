from __future__ import annotations

from dataclasses import dataclass

DIMENSIONS = (
    "novelty",
    "ecosystem_impact",
    "governance_impact",
    "deployment_impact",
    "research_significance",
    "reversibility",
    "evidence_strength",
    "geographic_scope",
)


@dataclass(frozen=True)
class DimensionAssessment:
    dimension: str
    level: str
    justification: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class SignificanceAssessment:
    event_id: str
    dimensions: tuple[DimensionAssessment, ...]

    def material_dimensions(self) -> tuple[DimensionAssessment, ...]:
        return tuple(item for item in self.dimensions if item.level in {"material", "high"})


def changed(before: SignificanceAssessment, after: SignificanceAssessment) -> tuple[str, ...]:
    prior = {item.dimension: item.level for item in before.dimensions}
    return tuple(
        item.dimension
        for item in after.dimensions
        if prior.get(item.dimension) != item.level
    )
