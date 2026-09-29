"""Render consumer-facing operational Signal Ledger output."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from .operational import load_operational_publication

REPOSITORY_URL = "https://github.com/qbf-consulting/signal-ledger"


def _shell(title: str, body: str) -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Signal Ledger</title><style>
:root{{color-scheme:light dark;font-family:ui-sans-serif,system-ui,sans-serif}}body{{margin:0;line-height:1.55}}main{{max-width:1080px;margin:auto;padding:2.5rem 1.4rem}}
nav{{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:3rem}}a{{color:inherit}}h1{{font-size:clamp(2.6rem,7vw,5.4rem);letter-spacing:-.055em;line-height:.95}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:1rem}}.card{{border:1px solid color-mix(in srgb,currentColor 22%,transparent);border-radius:12px;padding:1.2rem;margin:1rem 0}}
.meta,.muted{{opacity:.72;font-size:.92rem}}.tag{{display:inline-block;border:1px solid currentColor;border-radius:999px;padding:.1rem .55rem;margin-right:.4rem;font-size:.78rem}}
footer{{margin-top:4rem;padding-top:1.5rem;border-top:1px solid color-mix(in srgb,currentColor 22%,transparent)}}</style></head><body><main>
<nav><strong>Signal Ledger</strong><a href="index.html">Pulse</a><a href="evidence.html">Evidence</a><a href="methodology.html">Methodology</a></nav>{body}
<footer><p>Evidence-backed public intelligence from governed sources. <a href="{REPOSITORY_URL}">Inspect the implementation and governance.</a></p></footer></main></body></html>"""


def build_site(output_dir: Path, publication_dir: Path = Path("publications/operational")) -> Path:
    pub = load_operational_publication(publication_dir)
    manifest, signals, collection = pub["manifest"], pub["signals"], pub["collection"]
    output_dir.mkdir(parents=True, exist_ok=True)
    cards = []
    for signal in signals:
        cards.append(f"""<article class="card"><div><span class="tag">{html.escape(signal["domain"])}</span><span class="tag">{html.escape(signal["evidence_state"])}</span></div>
<h2>{html.escape(signal["headline"])}</h2><p>{html.escape(signal["summary"])}</p><h3>Why it may matter</h3><p>{html.escape(signal["why_it_matters"])}</p>
<p class="meta">Source: {html.escape(signal["source"]["name"])} · {html.escape(signal["source"]["class"])} · {html.escape(signal["uncertainty"])}</p>
<p><a href="{html.escape(signal["evidence"]["uri"])}">Read source ↗</a></p></article>""")
    if not cards:
        cards.append('<div class="card"><h2>No publishable signals in this run</h2><p>Collection completed, but nothing matched the current governed publication profiles. Signal Ledger does not manufacture a development when the evidence does not support one.</p></div>')
    body = f"""<p class="muted">AI governance + digital trust · updated {html.escape(manifest["generated_at"])}</p>
<h1>What should you know?</h1><p>Material and potentially relevant changes from governed public sources, with the evidence and uncertainty behind each judgment.</p>
<div class="grid"><div class="card"><strong>{manifest["published_signals"]}</strong><br>signals</div><div class="card"><strong>{manifest["collected_items"]}</strong><br>items observed</div>
<div class="card"><strong>{manifest["successful_sources"]}/{manifest["source_count"]}</strong><br>sources reached</div></div>{''.join(cards)}"""
    evidence_rows = "".join(f'<div class="card"><strong>{html.escape(x["source_id"])}</strong><p>Status: {html.escape(x["status"])}</p><p>{html.escape(x.get("error","Items collected: "+str(x.get("items",0))))}</p></div>' for x in collection)
    evidence = f"""<h1>Evidence</h1><p>Collection evidence for the current publication run. Source failures are retained rather than silently discarded.</p>{evidence_rows}
<p class="meta">Publication digest: {html.escape(manifest["content_digest"])}</p>"""
    methodology = """<h1>Methodology</h1><p>Signal Ledger observes governed public sources, applies deterministic domain relevance, and publishes consumer Signals without treating source publication as proof of every proposition.</p>
<div class="card"><h2>Authority is scoped</h2><p>An official source is authoritative for its own publication and status. That does not automatically verify broader claims in the material.</p></div>
<div class="card"><h2>Single-source signals remain qualified</h2><p>The operational MVP labels official-source matches partially verified and community-source matches indeterminate until corroboration/evidence rules are expanded.</p></div>
<div class="card"><h2>No LLM required</h2><p>Collection, relevance and publication are deterministic. Optional enrichment remains bounded and cannot establish truth or source authority.</p></div>"""
    for name,title,content in (("index.html","Pulse",body),("evidence.html","Evidence",evidence),("methodology.html","Methodology",methodology)):
        (output_dir/name).write_text(_shell(title,content),encoding="utf-8")
    data=output_dir/"data";data.mkdir(exist_ok=True)
    for name in ("manifest","signals","collection"):
        (data/f"{name}.json").write_text(json.dumps(pub[name],indent=2,sort_keys=True)+"\n")
    return output_dir/"index.html"


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("--publication-dir",type=Path,default=Path("publications/operational"));parser.add_argument("--output-dir",type=Path,default=Path("_site"));args=parser.parse_args()
    print(build_site(args.output_dir,args.publication_dir))


if __name__=="__main__": main()
