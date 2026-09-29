import json
from pathlib import Path

import pytest

from signal_ledger.models import Observation
from signal_ledger.storage import ObservationExistsError, ObservationStore


FIXTURE = Path(__file__).parent / "fixtures" / "observation.json"


def observation() -> Observation:
    return Observation.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))


def test_append_and_get_preserves_provenance(tmp_path: Path) -> None:
    store = ObservationStore(tmp_path)
    original = observation()

    path = store.append(original)
    restored = store.get(original.id)

    assert path.exists()
    assert restored == original
    assert restored.content_digest == original.content_digest
    assert restored.collector == "fixture-collector"
    assert restored.source_version == "etag-example"


def test_append_rejects_duplicate_identifier(tmp_path: Path) -> None:
    store = ObservationStore(tmp_path)
    original = observation()
    store.append(original)

    with pytest.raises(ObservationExistsError):
        store.append(original)
