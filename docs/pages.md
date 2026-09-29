# GitHub Pages projection

Signal Ledger publishes a generated static site through GitHub Pages.

## Authority boundary

The Pages site is a **read-only projection**. Repository-controlled code, schemas, profiles, documentation, and workflow evidence remain canonical. The rendered site must not create, mutate, or independently assert ledger state.

## Build locally

```bash
python -m pip install -e ".[dev]"
python -m signal_ledger.site --output-dir _site
```

Open `_site/index.html` locally.

## Deployment

`.github/workflows/pages.yml` runs tests, builds and validates the projection, uploads the Pages artifact, and deploys it to the `github-pages` environment. The build job has read-only repository permission. Only the deployment job receives `pages: write` and `id-token: write`.

A failed test or projection validation prevents deployment.
