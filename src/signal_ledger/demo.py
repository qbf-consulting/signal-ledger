from __future__ import annotations

import json
from pathlib import Path

from .assessment import DimensionAssessment, SignificanceAssessment
from .evidence import assess_claim
from .models import Claim, Observation
from .reconcile import reconcile


def run(fixture: Path) -> dict[str, object]:
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    first = Observation.model_validate(payload)
    second_payload = dict(payload)
    second_payload.update({
        "id": "obs.example.002",
        "canonical_uri": "https://example.org/notices/1?mirror=2",
        "source_id": "source.example",
    })
    second = Observation.model_validate(second_payload)

    event = reconcile((first, second))[0]
    claim = Claim(
        id="claim.example.001",
        statement="The example notice was published.",
        event_id=event.id,
        supporting_observation_ids=(first.id, second.id),
        primary_evidence_observation_ids=(first.id,),
    )
    evidence_state = assess_claim(claim)
    assessment = SignificanceAssessment(
        event_id=event.id,
        dimensions=(
            DimensionAssessment(
                "novelty",
                "material",
                "Fixture marks the first observation of this event.",
                (first.id, second.id),
            ),
            DimensionAssessment(
                "evidence_strength",
                "high",
                "Primary evidence is present and independently corroborated.",
                (first.id, second.id),
            ),
        ),
    )
    return {
        "schema": "signal-ledger.run.v1",
        "observations": [first.id, second.id],
        "event": {
            "id": event.id,
            "state": event.state.value,
            "observation_ids": list(event.observation_ids),
        },
        "claim": {"id": claim.id, "evidence_state": evidence_state.value},
        "significance": [
            {
                "dimension": item.dimension,
                "level": item.level,
                "justification": item.justification,
                "evidence_refs": list(item.evidence_refs),
            }
            for item in assessment.dimensions
        ],
        "material_change": True,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", default="tests/fixtures/observation.json")
    parser.add_argument("--output", default="artifacts/first-run.json")
    args = parser.parse_args()

    report = run(Path(args.fixture))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
