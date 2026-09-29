import json
from datetime import UTC, datetime

import pytest

from signal_ledger.demo import run
from signal_ledger.publication import build_publication, load_publication
from signal_ledger.site import REPOSITORY_URL, build_site


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


def test_site_renders_pipeline_output_not_brochure_copy(tmp_path):
    report = run(__import__("pathlib").Path("tests/fixtures/observation.json"))
    publication_dir = tmp_path / "publication"
    build_publication(
        report, publication_dir, generated_at=datetime(2026, 9, 29, tzinfo=UTC)
    )
    site_dir = tmp_path / "site"
    target = build_site(site_dir, publication_dir)
    page = target.read_text(encoding="utf-8")
    ledger = (site_dir / "ledger.html").read_text(encoding="utf-8")

    assert "What changed?" in page
    assert "1 material development in this ledger run." in page
    assert report["event"]["id"] in page
    assert report["claim"]["id"] in ledger
    assert REPOSITORY_URL in page
    assert (site_dir / "methodology.html").exists()
    assert (site_dir / "data" / "manifest.json").exists()


def test_no_material_change_is_publishable(tmp_path):
    report = run(__import__("pathlib").Path("tests/fixtures/observation.json"))
    report["material_change"] = False
    publication_dir = tmp_path / "publication"
    build_publication(report, publication_dir)
    site_dir = tmp_path / "site"
    build_site(site_dir, publication_dir)
    page = (site_dir / "index.html").read_text()
    assert "NO MATERIAL CHANGE" in page
    assert "No material changes; 2 observations were processed." in page
