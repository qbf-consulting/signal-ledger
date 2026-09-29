import copy
from pathlib import Path

from signal_ledger.profiles import apply_profile, load_profile

PROFILE_DIR = Path("profiles")


def test_all_shipped_profiles_validate() -> None:
    for path in PROFILE_DIR.glob("*.json"):
        load_profile(path)


def test_profile_application_is_derived_and_does_not_mutate_profile() -> None:
    profile = load_profile(PROFILE_DIR / "digital-trust.json")
    before = copy.deepcopy(profile)
    result = apply_profile(profile, "A trust registry and verifiable credential update")
    assert result.relevant is True
    assert profile == before


def test_exclusion_prevents_relevance() -> None:
    profile = load_profile(PROFILE_DIR / "ai-governance.json")
    result = apply_profile(profile, "AI governance consumer promotion")
    assert result.relevant is False


def test_paper_notes_has_discovery_diversity_lanes() -> None:
    profile = load_profile(PROFILE_DIR / "digital-governance-paper-notes.json")
    assert set(profile["discovery"]["candidate_lanes"]) == {
        "established-interest",
        "adjacent-domain",
        "exploratory",
        "counter-thesis",
    }


def test_profiles_cannot_declare_canonical_evidence_state() -> None:
    for path in PROFILE_DIR.glob("*.json"):
        profile = load_profile(path)
        serialized = str(profile)
        assert "primary_evidence_observation_ids" not in serialized
        assert "evidence_state" not in serialized
