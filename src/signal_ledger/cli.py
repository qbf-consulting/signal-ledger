from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .models import Observation, Source
from .storage import ObservationStore


def _read_json(path: str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="signal-ledger")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate_source = subcommands.add_parser("validate-source")
    validate_source.add_argument("file")

    ingest = subcommands.add_parser("ingest-observation")
    ingest.add_argument("file")
    ingest.add_argument("--store", default="data")

    inspect = subcommands.add_parser("inspect-observation")
    inspect.add_argument("observation_id")
    inspect.add_argument("--store", default="data")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.command == "validate-source":
            source = Source.model_validate(_read_json(args.file))
            print(source.model_dump_json(indent=2))
            return 0

        if args.command == "ingest-observation":
            observation = Observation.model_validate(_read_json(args.file))
            path = ObservationStore(args.store).append(observation)
            print(path)
            return 0

        if args.command == "inspect-observation":
            observation = ObservationStore(args.store).get(args.observation_id)
            print(observation.model_dump_json(indent=2))
            return 0

    except (ValidationError, OSError, ValueError) as exc:
        print(f"error: {exc}")
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
