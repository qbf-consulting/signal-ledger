import json
from pathlib import Path

from signal_ledger.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_validate_ingest_inspect(tmp_path: Path, capsys) -> None:
    assert main(["validate-source", str(FIXTURES / "source.json")]) == 0
    assert "source.example" in capsys.readouterr().out

    assert main([
        "ingest-observation",
        str(FIXTURES / "observation.json"),
        "--store",
        str(tmp_path),
    ]) == 0
    capsys.readouterr()

    assert main([
        "inspect-observation",
        "obs.example.001",
        "--store",
        str(tmp_path),
    ]) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["content_digest"].startswith("sha256:")
