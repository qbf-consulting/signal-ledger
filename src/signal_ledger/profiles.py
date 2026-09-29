from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class ProfileResult:
    profile_id: str
    relevant: bool
    matched_terms: tuple[str, ...]
    excluded_terms: tuple[str, ...]


def load_profile(path: Path, schema_path: Path = Path("schemas/profile.schema.json")) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(profile)
    return profile


def apply_profile(profile: dict, text: str) -> ProfileResult:
    """Return derived relevance without modifying canonical evidence."""
    normalized = text.casefold()
    included = tuple(
        term for term in profile["relevance"]["include_terms"] if term.casefold() in normalized
    )
    excluded = tuple(
        term for term in profile["relevance"]["exclude_terms"] if term.casefold() in normalized
    )
    return ProfileResult(
        profile_id=profile["id"],
        relevant=bool(included) and not bool(excluded),
        matched_terms=included,
        excluded_terms=excluded,
    )
