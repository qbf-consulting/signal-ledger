import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from signal_ledger.operational import build_operational_publication, parse_feed
from signal_ledger.site import REPOSITORY_URL, build_site


def test_build_site_is_consumer_projection(tmp_path):
    source = {
        "id": "test",
        "name": "Test Standards Body",
        "source_class": "official",
        "authority_scope": "Own publications.",
    }
    registry = tmp_path / "sources.json"
    registry.write_text(json.dumps({"sources": [{**source, "feed_url": "https://example.org/feed"}]}))
    items = parse_feed(
        Path("tests/fixtures/feed.xml").read_bytes(),
        source,
        datetime(2026, 9, 29, tzinfo=UTC),
    )
    evidence = {"source_id": "test", "status": "ok", "items": 1}
    with patch("signal_ledger.operational.collect", return_value=(items, evidence)):
        build_operational_publication(registry, tmp_path / "publication")
    target = build_site(tmp_path / "site", tmp_path / "publication")
    page = target.read_text(encoding="utf-8")
    assert target.name == "index.html"
    assert "What should you know?" in page
    assert REPOSITORY_URL in page
    assert "New verifiable credential trust registry specification published" in page
