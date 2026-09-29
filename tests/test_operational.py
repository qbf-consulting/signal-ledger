import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from signal_ledger.operational import build_operational_publication, parse_feed
from signal_ledger.site import build_site

SOURCE = {"id":"test","name":"Test Standards Body","source_class":"official","authority_scope":"Own publications."}


def test_parse_real_feed_shape():
    data=Path("tests/fixtures/feed.xml").read_bytes()
    items=parse_feed(data,SOURCE,datetime(2026,9,29,tzinfo=UTC))
    assert items[0].title.startswith("New verifiable credential")
    assert items[0].uri=="https://example.org/spec"


def test_operational_publication_drives_consumer_site(tmp_path):
    registry=tmp_path/"sources.json"
    registry.write_text(json.dumps({"sources":[{**SOURCE,"feed_url":"https://example.org/feed","canonical_uri":"https://example.org","domains":["digital-trust"]}]}))
    item=parse_feed(Path("tests/fixtures/feed.xml").read_bytes(),SOURCE,datetime(2026,9,29,tzinfo=UTC))
    with patch("signal_ledger.operational.collect",return_value=(item,[{"source_id":"test","status":"ok","items":1}])):
        pub=build_operational_publication(registry,tmp_path/"pub")
    assert pub["manifest"]["published_signals"]>=1
    target=build_site(tmp_path/"site",tmp_path/"pub")
    page=target.read_text()
    assert "What should you know?" in page
    assert "New verifiable credential trust registry specification published" in page
    assert "Why it may matter" in page
    assert "Read source" in page
