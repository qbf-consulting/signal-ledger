from __future__ import annotations

import json
from pathlib import Path

from .models import Observation


class ObservationExistsError(FileExistsError):
    """Raised when append-only storage already contains an observation identifier."""


class ObservationStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)

    def _path(self, observation_id: str) -> Path:
        return self.root / "observations" / f"{observation_id}.json"

    def append(self, observation: Observation) -> Path:
        path = self._path(observation.id)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = observation.model_dump(mode="json")
        serialized = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

        try:
            with path.open("x", encoding="utf-8") as handle:
                handle.write(serialized)
        except FileExistsError as exc:
            raise ObservationExistsError(
                f"observation '{observation.id}' already exists; storage is append-only"
            ) from exc

        return path

    def get(self, observation_id: str) -> Observation:
        path = self._path(observation_id)
        with path.open("r", encoding="utf-8") as handle:
            return Observation.model_validate(json.load(handle))
