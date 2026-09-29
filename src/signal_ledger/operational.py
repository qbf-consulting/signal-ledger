from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .profiles import apply_profile, load_profile

USER_AGENT = "Signal-Ledger/0.1 (+https://github.com/qbf-consulting/signal-ledger)"


@dataclass(frozen=True)
class CollectedItem:
    source_id: str
    source_name: str
    source_class: str
    authority_scope: str
    title: str
    summary: str
    uri: str
    published_at: str | None
    retrieved_at: str
    digest: str


def _text(node: ET.Element, names: tuple[str, ...]) -> str:
    for child in list(node):
        local = child.tag.rsplit("}", 1)[-1].lower()
        if local in names and child.text:
            return re.sub(r"<[^>]+>", " ", child.text).strip()
    return ""


def _link(node: ET.Element) -> str:
    for child in list(node):
        if child.tag.rsplit("}", 1)[-1].lower() == "link":
            return child.attrib.get("href") or (child.text or "").strip()
    return ""


def parse_feed(data: bytes, source: dict, retrieved_at: datetime, limit: int = 10) -> list[CollectedItem]:
    root = ET.fromstring(data)
    entries = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1].lower() in {"item", "entry"}]
    result = []
    for entry in entries[:limit]:
        title = _text(entry, ("title",))
        uri = _link(entry) or _text(entry, ("guid", "id"))
        summary = _text(entry, ("description", "summary", "content"))
        published = _text(entry, ("pubdate", "published", "updated")) or None
        if not title or not uri:
            continue
        digest = "sha256:" + hashlib.sha256((title + "\n" + summary + "\n" + uri).encode()).hexdigest()
        result.append(CollectedItem(
            source_id=source["id"], source_name=source["name"], source_class=source["source_class"],
            authority_scope=source["authority_scope"], title=title, summary=summary[:2000], uri=uri,
            published_at=published, retrieved_at=retrieved_at.isoformat(), digest=digest,
        ))
    return result


def collect(source: dict, timeout: int = 20) -> tuple[list[CollectedItem], dict]:
    retrieved = datetime.now(UTC)
    request = urllib.request.Request(source["feed_url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            items = parse_feed(response.read(), source, retrieved)
        return items, {"source_id": source["id"], "status": "ok", "items": len(items)}
    except (urllib.error.URLError, TimeoutError, OSError, ET.ParseError) as exc:
        return [], {"source_id": source["id"], "status": "failed", "error": f"{type(exc).__name__}: {exc}"}


def _why(domain: str, source_class: str, matched: tuple[str, ...]) -> str:
    basis = ", ".join(matched[:4])
    if domain == "ai-governance":
        return f"Potentially relevant to AI governance because the source material matched: {basis}."
    return f"Potentially relevant to digital trust because the source material matched: {basis}."


def build_operational_publication(registry: Path, output_dir: Path, max_signals: int = 20) -> dict:
    config = json.loads(registry.read_text())
    profiles = {
        name: load_profile(Path("profiles") / f"{name}.json")
        for name in ("ai-governance", "digital-trust")
    }
    items: list[CollectedItem] = []
    collection = []
    for source in config["sources"]:
        found, evidence = collect(source)
        items.extend(found)
        collection.append(evidence)

    signals = []
    seen = set()
    for item in items:
        text = f"{item.title} {item.summary}"
        for domain, profile in profiles.items():
            result = apply_profile(profile, text)
            if not result.relevant:
                continue
            key = (item.uri, domain)
            if key in seen:
                continue
            seen.add(key)
            evidence_state = "partially_verified" if item.source_class in {"official", "primary"} else "indeterminate"
            signals.append({
                "id": "signal." + hashlib.sha256((item.uri + domain).encode()).hexdigest()[:16],
                "headline": item.title,
                "summary": item.summary or "The source did not provide a summary; inspect the primary item for detail.",
                "why_it_matters": _why(domain, item.source_class, result.matched_terms),
                "domain": domain,
                "status": "new",
                "evidence_state": evidence_state,
                "source": {"id": item.source_id, "name": item.source_name, "class": item.source_class,
                           "authority_scope": item.authority_scope},
                "evidence": {"uri": item.uri, "digest": item.digest, "retrieved_at": item.retrieved_at,
                             "published_at": item.published_at},
                "matched_terms": list(result.matched_terms),
                "uncertainty": "Single-source observation; publication status is observed, broader claims are not independently verified.",
            })
    signals = signals[:max_signals]
    generated = datetime.now(UTC).isoformat()
    payload = {"signals": signals, "collection": collection}
    digest = "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    manifest = {
        "schema": "signal-ledger.operational-publication.v1", "generated_at": generated,
        "content_digest": digest, "source_count": len(config["sources"]),
        "successful_sources": sum(x["status"] == "ok" for x in collection),
        "failed_sources": sum(x["status"] == "failed" for x in collection),
        "collected_items": len(items), "published_signals": len(signals),
        "domains": ["ai-governance", "digital-trust"],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in {"manifest": manifest, **payload}.items():
        (output_dir / f"{name}.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    return {"manifest": manifest, **payload}


def load_operational_publication(path: Path) -> dict:
    manifest = json.loads((path / "manifest.json").read_text())
    if manifest.get("schema") != "signal-ledger.operational-publication.v1":
        raise ValueError("unsupported operational publication")
    payload = {name: json.loads((path / f"{name}.json").read_text()) for name in ("signals", "collection")}
    digest = "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if digest != manifest["content_digest"]:
        raise ValueError("operational publication content digest mismatch")
    return {"manifest": manifest, **payload}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=Path("sources/pilot.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("publications/operational"))
    args = parser.parse_args()
    result = build_operational_publication(args.sources, args.output_dir)
    print(json.dumps(result["manifest"], indent=2))


if __name__ == "__main__":
    main()
