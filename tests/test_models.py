import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from signal_ledger.models import Observation, Source

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_source_fixture_is_valid() -> None:
    source = Source.model_validate(load("source.json"))
    assert source.id == "source.example"


def test_observation_fixture_is_valid() -> None:
    observation = Observation.model_validate(load("observation.json"))
    assert observation.source_id == "source.example"


def test_observation_rejects_non_sha256_digest() -> None:
    payload = load("observation.json")
    payload["content_digest"] = "md5:bad"
    with pytest.raises(ValidationError):
        Observation.model_validate(payload)


def test_observation_rejects_naive_timestamp() -> None:
    payload = load("observation.json")
    payload["retrieved_at"] = "2026-09-29T09:05:00"
    with pytest.raises(ValidationError):
        Observation.model_validate(payload)
