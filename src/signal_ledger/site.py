"""Render a governed publication snapshot as the public Pages surface."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from .publication import load_publication

REPOSITORY_URL = "https://github.com/qbf-consulting/signal-ledger"


def _shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Signal Ledger</title>
<style>
:root {{ color-scheme:light dark; font-family:ui-sans-serif,system-ui,sans-serif }}
body {{ margin:0; line-height:1.55 }} main {{ max-width:1050px; margin:auto; padding:2.5rem 1.4rem }}
nav {{ display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:3rem }} a {{ color:inherit }}
h1 {{ font-size:clamp(2.5rem,7vw,5rem); letter-spacing:-.055em; line-height:.95 }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:1rem }}
.card {{ border:1px solid color-mix(in srgb,currentColor 22%,transparent); border-radius:12px; padding:1.15rem }}
.metric {{ font-size:2rem; font-weight:700 }} .muted {{ opacity:.72 }} code {{ font-family:ui-monospace,monospace }}
footer {{ margin-top:4rem; padding-top:1.5rem; border-top:1px solid color-mix(in srgb,currentColor 22%,transparent) }}
</style></head><body><main>
<nav><strong>Signal Ledger</strong><a href="index.html">Pulse</a><a href="ledger.html">Ledger</a><a href="methodology.html">Methodology</a></nav>
{body}
<footer><p>This is a read-only projection of a governed publication snapshot. <a href="{REPOSITORY_URL}">Canonical repository</a>.</p></footer>
</main></body></html>"""


def build_site(output_dir: Path, publication_dir: Path = Path("publications/latest")) -> Path:
    publication = load_publication(publication_dir)
    manifest = publication["manifest"]
    pulse = publication["pulse"]
    event = publication["events"][0]
    claim = publication["claims"][0]
    assessment = publication["assessments"][0]

    output_dir.mkdir(parents=True, exist_ok=True)
    status = "MATERIAL CHANGE" if pulse["material_change"] else "NO MATERIAL CHANGE"
    pulse_body = f"""<p class="muted">Evidence-backed situational awareness · profile: {html.escape(manifest["profile"])}</p>
<h1>What changed?</h1><h2>{status}</h2><p>{html.escape(pulse["summary"])}</p>
<div class="grid">
<div class="card"><div class="metric">{pulse["observations"]}</div>observations</div>
<div class="card"><div class="metric">{pulse["events"]}</div>events</div>
<div class="card"><div class="metric">{pulse["claims"]}</div>claims</div>
<div class="card"><div class="metric">{pulse["material_developments"]}</div>material developments</div>
</div>
<h2>Current material signal</h2>
<div class="card"><strong>{html.escape(event["state"].upper())}</strong>
<p>Event <code>{html.escape(event["id"])}</code></p>
<p>Claim <code>{html.escape(claim["id"])}</code>: evidence state <strong>{html.escape(claim["evidence_state"])}</strong>.</p>
<p><a href="ledger.html">Inspect evidence and assessment →</a></p></div>
<p class="muted">Snapshot {html.escape(manifest["content_digest"])} · generated {html.escape(manifest["generated_at"])}</p>"""

    dims = "".join(
        f'<div class="card"><strong>{html.escape(d["dimension"])}</strong><p>{html.escape(d["level"])}</p>'
        f'<p>{html.escape(d["justification"])}</p><p class="muted">Evidence: {html.escape(", ".join(d["evidence_refs"]))}</p></div>'
        for d in assessment["dimensions"]
    )
    ledger_body = f"""<h1>Ledger</h1><p>Inspectable output from the published ledger snapshot.</p>
<h2>Event</h2><div class="card"><code>{html.escape(event["id"])}</code><p>State: {html.escape(event["state"])}</p>
<p>Observations: {html.escape(", ".join(event["observation_ids"]))}</p></div>
<h2>Claim</h2><div class="card"><code>{html.escape(claim["id"])}</code><p>Evidence state: <strong>{html.escape(claim["evidence_state"])}</strong></p></div>
<h2>Significance assessment</h2><div class="grid">{dims}</div>"""

    method_body = f"""<h1>Methodology</h1>
<p>Signal Ledger separates observation, reconciliation, claims, evidence state, significance and publication.</p>
<div class="grid">
<div class="card"><h3>Observation ≠ truth</h3><p>A record says what a governed source exposed and when it was retrieved.</p></div>
<div class="card"><h3>Interpretation ≠ publication</h3><p>Only a validated publication snapshot is eligible for this public projection.</p></div>
<div class="card"><h3>AI ≠ authority</h3><p>Enrichment may derive candidates and explanations but cannot establish truth, source authority or final evidence state.</p></div>
</div>
<h2>Publication evidence</h2><p>Schema: <code>{html.escape(manifest["schema"])}</code></p>
<p>Source run: <code>{html.escape(manifest["source_run_schema"])}</code></p>
<p>Digest: <code>{html.escape(manifest["content_digest"])}</code></p>
<p>For normative implementation details, tests and licensing, use the <a href="{REPOSITORY_URL}">repository</a>.</p>"""

    for name, title, body in (
        ("index.html", "Pulse", pulse_body),
        ("ledger.html", "Ledger", ledger_body),
        ("methodology.html", "Methodology", method_body),
    ):
        (output_dir / name).write_text(_shell(title, body), encoding="utf-8")

    data_dir = output_dir / "data"
    data_dir.mkdir(exist_ok=True)
    for name in ("manifest", "pulse", "events", "claims", "assessments", "observations"):
        (data_dir / f"{name}.json").write_text(
            json.dumps(publication[name], indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return output_dir / "index.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Signal Ledger public snapshot")
    parser.add_argument("--publication-dir", type=Path, default=Path("publications/latest"))
    parser.add_argument("--output-dir", type=Path, default=Path("_site"))
    args = parser.parse_args()
    print(build_site(args.output_dir, args.publication_dir))


if __name__ == "__main__":
    main()
