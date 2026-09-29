import json
from pathlib import Path

from signal_ledger.models import Observation
from signal_ledger.reconcile import reconcile

FIXTURE = Path(__file__).parent / "fixtures" / "observation.json"


def make(identifier: str, title: str) -> Observation:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["id"] = identifier
    payload["title"] = title
    payload["canonical_uri"] = f"https://example.org/{identifier}"
    return Observation.model_validate(payload)


def test_five_observations_of_same_event_reconcile_to_one_event() -> None:
    observations = [make(f"obs.example.00{i}", "Example notice") for i in range(1, 6)]
    events = reconcile(observations)
    assert len(events) == 1
    assert len(events[0].observation_ids) == 5
    assert events[0].state.value == "confirmed"


def test_distinct_titles_do_not_collapse() -> None:
    events = reconcile([make("obs.one", "Model Alpha released"), make("obs.two", "Law Beta adopted")])
    assert len(events) == 2
