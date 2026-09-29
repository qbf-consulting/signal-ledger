# Contributing

Signal Ledger is currently under active architectural development.

## Change discipline

- Use an issue to define a coherent, testable proposition before implementation.
- Work on a feature branch and submit changes through a pull request.
- Keep commits modular and independently intelligible.
- Add or update tests for behavior changes.
- Keep documentation synchronized with implemented behavior.
- Do not describe planned capability as already implemented.
- Preserve provenance and authority boundaries when introducing derived data.

## Validation

Before proposing a change:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
```

## Licensing

This repository intentionally has no license at present. Do not assume permission to redistribute repository content beyond rights explicitly granted by the repository owner.
