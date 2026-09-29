import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_required_license_files_exist() -> None:
    for name in ("LICENSE", "LICENSE-CODE", "LICENSE-CONTENT", "NOTICE"):
        assert (ROOT / name).is_file(), name


def test_license_policy_declares_both_qbf_defaults() -> None:
    policy = json.loads((ROOT / "artifact-license-policy.json").read_text(encoding="utf-8"))
    licenses = {entry["license"] for entry in policy["defaults"]}
    assert licenses == {"Apache-2.0", "CC-BY-4.0"}


def test_executable_and_docs_boundaries_are_explicit() -> None:
    policy = json.loads((ROOT / "artifact-license-policy.json").read_text(encoding="utf-8"))
    by_license = {entry["license"]: entry["artifacts"] for entry in policy["defaults"]}
    assert "src/**" in by_license["Apache-2.0"]
    assert "schemas/**" in by_license["Apache-2.0"]
    assert "docs/**" in by_license["CC-BY-4.0"]
    assert "README.md" in by_license["CC-BY-4.0"]
