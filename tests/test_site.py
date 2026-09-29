from signal_ledger.site import REPOSITORY_URL, build_site


def test_build_site_is_public_read_only_projection(tmp_path):
    target = build_site(tmp_path)
    page = target.read_text(encoding="utf-8")

    assert target.name == "index.html"
    assert "read-only projection" in page
    assert REPOSITORY_URL in page
    assert "Observation is not truth" in page
    assert "Missing primary evidence cannot silently become verified evidence" in page
    assert "Apache-2.0" in page
    assert "CC BY 4.0" in page
