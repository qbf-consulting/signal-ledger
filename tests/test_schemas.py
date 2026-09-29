import json
from pathlib import Path

from signal_ledger.schema import load_schema, validate

ROOT = Path(__file__).parents[1]


def fixture(name: str) -> dict:
    return json.loads((ROOT / "tests" / "fixtures" / name).read_text(encoding="utf-8"))


def test_source_schema_accepts_fixture() -> None:
    validate(fixture("source.json"), load_schema(ROOT / "schemas" / "source.schema.json"))


def test_observation_schema_accepts_fixture() -> None:
    validate(
        fixture("observation.json"),
        load_schema(ROOT / "schemas" / "observation.schema.json"),
    )
