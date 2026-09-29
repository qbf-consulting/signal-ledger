from pathlib import Path

from signal_ledger.demo import run


def test_end_to_end_demo() -> None:
    report = run(Path("tests/fixtures/observation.json"))
    assert report["schema"] == "signal-ledger.run.v1"
    assert report["event"]["state"] == "confirmed"
    assert report["claim"]["evidence_state"] == "verified"
    assert report["material_change"] is True
    assert len(report["observations"]) == 2
