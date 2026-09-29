from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .models import Event, EventState, Observation


def normalize_key(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def reconcile(observations: Iterable[Observation]) -> list[Event]:
    groups: dict[str, list[Observation]] = {}
    for observation in observations:
        groups.setdefault(normalize_key(observation.title), []).append(observation)

    events = []
    for key, members in sorted(groups.items()):
        digest = hashlib.sha256(key.encode()).hexdigest()[:20]
        events.append(Event(
            id=f"event.{digest}",
            reconciliation_key=key,
            title=members[0].title,
            observation_ids=tuple(sorted(item.id for item in members)),
            state=EventState.CONFIRMED if len(members) > 1 else EventState.NEW,
        ))
    return events
