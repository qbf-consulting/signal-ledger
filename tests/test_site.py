from datetime import UTC, datetime
from pathlib import Path

from signal_ledger.demo import run
from signal_ledger.publication import build_publication
from signal_ledger.site import REPOSITORY_URL, build_site


def test_build_site_is_public_read_only_projection(tmp_path):
    report = run(Path("tests/fixtures/observation.json"))
    publication_dir = tmp_path / "publication"
    build_publication(
        report, publication_dir, generated_at=datetime(2026, 9, 29, tzinfo=UTC)
    )
    target = build_site(tmp_path / "site", publication_dir)
    page = target.read_text(encoding="utf-8")

    assert target.name == "index.html"
    assert "read-only projection" in page
    assert REPOSITORY_URL in page
    assert "What changed?" in page
    assert report["event"]["id"] in page
