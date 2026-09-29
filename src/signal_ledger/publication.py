from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def _canonical(payload: object) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def build_publication(
    run: dict[str, object],
    output_dir: Path,
    *,
    profile: str = "ai-governance",
    generated_at: datetime | None = None,
) -> dict[str, object]:
    """Transform an assured run artifact into a governed public snapshot."""
    if run.get("schema") != "signal-ledger.run.v1":
        raise ValueError("publication requires signal-ledger.run.v1 input")

    generated = generated_at or datetime.now(UTC)
    event = dict(run["event"])
    claim = dict(run["claim"])
    assessments = list(run["significance"])
    observations = list(run["observations"])
    material = bool(run["material_change"])

    payload = {
        "pulse": {
            "material_change": material,
            "material_developments": 1 if material else 0,
            "observations": len(observations),
            "events": 1,
            "claims": 1,
            "summary": (
                "1 material development in this ledger run."
                if material
                else f"No material changes; {len(observations)} observations were processed."
            ),
        },
        "events": [event],
        "claims": [claim],
        "assessments": [{"event_id": event["id"], "dimensions": assessments}],
        "observations": observations,
    }
    digest = "sha256:" + hashlib.sha256(_canonical(payload)).hexdigest()
    manifest = {
        "schema": "signal-ledger.publication.v1",
        "generated_at": generated.isoformat(),
        "source_run_schema": run["schema"],
        "profile": profile,
        "counts": {
            "observations": len(observations),
            "events": 1,
            "claims": 1,
            "material_developments": 1 if material else 0,
        },
        "content_digest": digest,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    documents = {"manifest": manifest, **payload}
    for name, content in documents.items():
        (output_dir / f"{name}.json").write_text(
            json.dumps(content, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return documents


def load_publication(path: Path) -> dict[str, object]:
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != "signal-ledger.publication.v1":
        raise ValueError("unsupported publication snapshot")
    names = ("pulse", "events", "claims", "assessments", "observations")
    payload = {name: json.loads((path / f"{name}.json").read_text(encoding="utf-8")) for name in names}
    digest = "sha256:" + hashlib.sha256(_canonical(payload)).hexdigest()
    if digest != manifest["content_digest"]:
        raise ValueError("publication content digest mismatch")
    return {"manifest": manifest, **payload}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Build a governed Signal Ledger publication snapshot")
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("publications/latest"))
    parser.add_argument("--profile", default="ai-governance")
    args = parser.parse_args()
    run = json.loads(args.run.read_text(encoding="utf-8"))
    result = build_publication(run, args.output_dir, profile=args.profile)
    print(json.dumps(result["manifest"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
