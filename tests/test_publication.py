import json
from datetime import UTC, datetime

import pytest

from signal_ledger.demo import run
from signal_ledger.publication import build_publication, load_publication


def test_publication_snapshot_round_trip(tmp_path):
    report = run(__import__("pathlib").Path("tests/fixtures/observation.json"))
    publication_dir = tmp_path / "publication"
    built = build_publication(
        report, publication_dir, generated_at=datetime(2026, 9, 29, tzinfo=UTC)
    )
    loaded = load_publication(publication_dir)
    assert built["manifest"] == loaded["manifest"]
    assert loaded["pulse"]["observations"] == 2
    assert loaded["pulse"]["material_developments"] == 1
    assert loaded["manifest"]["content_digest"].startswith("sha256:")


def test_tampered_publication_fails_closed(tmp_path):
    report = run(__import__("pathlib").Path("tests/fixtures/observation.json"))
    publication_dir = tmp_path / "publication"
    build_publication(report, publication_dir)
    pulse = json.loads((publication_dir / "pulse.json").read_text())
    pulse["events"] = 99
    (publication_dir / "pulse.json").write_text(json.dumps(pulse))
    with pytest.raises(ValueError, match="digest mismatch"):
        load_publication(publication_dir)
