from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class SourceClass(str, Enum):
    PRIMARY = "primary"
    OFFICIAL = "official"
    RESEARCH = "research"
    JOURNALISM = "journalism"
    ANALYSIS = "analysis"
    COMMUNITY = "community"
    OTHER = "other"


class SourceStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    RETIRED = "retired"


class CollectionMethod(str, Enum):
    RSS = "rss"
    ATOM = "atom"
    API = "api"
    HTML = "html"
    MANUAL = "manual"
    FILE = "file"


StableId = Annotated[str, Field(pattern=r"^[a-z][a-z0-9._-]{2,127}$")]


class Source(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: StableId
    name: str = Field(min_length=1, max_length=200)
    canonical_uri: HttpUrl
    source_class: SourceClass
    authority_domains: tuple[str, ...] = ()
    jurisdiction: str | None = Field(default=None, max_length=120)
    collection_method: CollectionMethod
    cadence: str | None = Field(default=None, max_length=80)
    status: SourceStatus = SourceStatus.ACTIVE
    scope_notes: str | None = Field(default=None, max_length=1000)

    @field_validator("authority_domains")
    @classmethod
    def domains_must_be_nonempty(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value.strip() for value in values):
            raise ValueError("authority_domains must not contain empty values")
        return values


class Observation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: StableId
    source_id: StableId
    canonical_uri: HttpUrl
    title: str = Field(min_length=1, max_length=500)
    summary: str | None = Field(default=None, max_length=5000)
    language: str = Field(default="en", pattern=r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")
    published_at: datetime | None = None
    retrieved_at: datetime
    content_digest: str
    collection_method: CollectionMethod
    collector: str = Field(min_length=1, max_length=120)
    source_version: str | None = Field(default=None, max_length=120)

    @field_validator("published_at", "retrieved_at")
    @classmethod
    def timestamps_must_be_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("timestamps must include a timezone")
        return value

    @field_validator("content_digest")
    @classmethod
    def digest_must_be_sha256(cls, value: str) -> str:
        if not SHA256_RE.match(value):
            raise ValueError("content_digest must use sha256:<64 lowercase hex characters>")
        return value


class EventState(str, Enum):
    NEW = "new"
    CHANGED = "changed"
    CONFIRMED = "confirmed"
    SUPERSEDED = "superseded"


class EntityRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: StableId
    name: str = Field(min_length=1, max_length=200)
    kind: str = Field(min_length=1, max_length=80)


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: StableId
    reconciliation_key: str = Field(min_length=1, max_length=500)
    title: str = Field(min_length=1, max_length=500)
    observation_ids: tuple[StableId, ...] = Field(min_length=1)
    entities: tuple[EntityRef, ...] = ()
    state: EventState = EventState.NEW

    @field_validator("observation_ids")
    @classmethod
    def observations_must_be_unique(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if len(values) != len(set(values)):
            raise ValueError("observation_ids must be unique")
        return values


class EvidenceState(str, Enum):
    INDETERMINATE = "indeterminate"
    PARTIALLY_VERIFIED = "partially_verified"
    VERIFIED = "verified"
    CONTRADICTORY = "contradictory"
    SUPERSEDED = "superseded"


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: StableId
    statement: str = Field(min_length=1, max_length=5000)
    event_id: StableId
    supporting_observation_ids: tuple[StableId, ...] = ()
    challenging_observation_ids: tuple[StableId, ...] = ()
    primary_evidence_observation_ids: tuple[StableId, ...] = ()
    state: EvidenceState = EvidenceState.INDETERMINATE
