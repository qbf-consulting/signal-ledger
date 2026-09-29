"""Build the deterministic public GitHub Pages projection."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

REPOSITORY_URL = "https://github.com/qbf-consulting/signal-ledger"


def _card(title: str, body: str) -> str:
    return f'<article class="card"><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></article>'


def build_site(output_dir: Path) -> Path:
    """Render a static, repository-derived public projection."""
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = json.loads(Path("profiles/ai-governance.json").read_text(encoding="utf-8"))
    dimensions = ", ".join(profile["significance_dimensions"])

    cards = "".join(
        [
            _card("Observation", "A source exposed an artifact at a recorded time. Observation is not truth."),
            _card("Event", "Related observations are reconciled deterministically without treating report count as importance."),
            _card("Evidence", "Claims retain supporting, challenging, and primary-evidence references plus explicit uncertainty."),
            _card("Assessment", "Significance is decomposed into inspectable dimensions rather than collapsed into an opaque score."),
        ]
    )
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Signal Ledger</title>
<meta name="description" content="Evidence-backed change intelligence with inspectable provenance, uncertainty, and assessment.">
<style>
:root {{ color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; }}
body {{ margin: 0; line-height: 1.6; }}
main {{ max-width: 980px; margin: auto; padding: 4rem 1.5rem; }}
header {{ max-width: 760px; margin-bottom: 3rem; }}
h1 {{ font-size: clamp(2.8rem, 8vw, 5.8rem); line-height: .92; letter-spacing: -.06em; margin: 0 0 1.5rem; }}
.lede {{ font-size: 1.25rem; }}
.badge {{ display: inline-block; border: 1px solid currentColor; border-radius: 999px; padding: .2rem .65rem; margin-bottom: 1.2rem; font-size: .82rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); gap: 1rem; margin: 2rem 0 3rem; }}
.card {{ border: 1px solid color-mix(in srgb, currentColor 24%, transparent); border-radius: 12px; padding: 1.25rem; }}
.card h3 {{ margin-top: 0; }}
section {{ margin: 3rem 0; }}
code {{ font-family: ui-monospace, monospace; }}
a {{ color: inherit; }}
footer {{ margin-top: 5rem; border-top: 1px solid color-mix(in srgb, currentColor 24%, transparent); padding-top: 1.5rem; font-size: .9rem; }}
</style>
</head>
<body>
<main>
<header>
<div class="badge">QBF Consulting · architectural prototype</div>
<h1>Signal<br>Ledger</h1>
<p class="lede">Evidence-backed change intelligence that keeps observation, claim, evidence and judgment distinct.</p>
<p>This site is a <strong>read-only projection</strong> of version-controlled Signal Ledger artifacts. The canonical source of truth is the <a href="{REPOSITORY_URL}">public GitHub repository</a>.</p>
</header>
<section>
<h2>From signal to inspectable judgment</h2>
<div class="grid">{cards}</div>
</section>
<section>
<h2>Implemented baseline</h2>
<p>The executable prototype covers governed observations and provenance, deterministic reconciliation, claims and evidence states, decomposed significance assessment, change detection, Research Radar interoperability, and bounded optional AI enrichment.</p>
<p>The current AI-governance profile evaluates: <strong>{html.escape(dimensions)}</strong>.</p>
</section>
<section>
<h2>Assurance posture</h2>
<p>Missing primary evidence cannot silently become verified evidence. Contradictory evidence remains explicit. AI-derived material carries derivation provenance and cannot establish source authority, truth, or final assurance state.</p>
<p>The repository CI tests Python 3.11–3.13, while a separate end-to-end workflow exercises the complete deterministic demonstration and emits a machine-readable run artifact.</p>
</section>
<section>
<h2>Reproduce it</h2>
<pre><code>python -m pip install -e ".[dev]"
ruff check .
pytest
python -m signal_ledger.demo --output artifacts/first-run.json
python -m signal_ledger.site --output-dir _site</code></pre>
</section>
<footer>
<p>Signal Ledger is maintained by QBF Consulting LLP. Code and machine-readable artifacts: Apache-2.0. Documentation and specification content: CC BY 4.0. See the repository for authoritative licensing and provenance.</p>
</footer>
</main>
</body>
</html>
"""
    target = output_dir / "index.html"
    target.write_text(document, encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Signal Ledger public projection")
    parser.add_argument("--output-dir", type=Path, default=Path("_site"))
    args = parser.parse_args()
    target = build_site(args.output_dir)
    print(target)


if __name__ == "__main__":
    main()
