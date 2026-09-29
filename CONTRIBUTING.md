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

Contributions are accepted under the license applicable to the artifact class being modified: **Apache-2.0** for executable and machine-readable artifacts, and **CC BY 4.0** for specifications and documentation. Contributors must preserve third-party provenance and any more-specific artifact-level license. See [LICENSE](LICENSE) and [artifact-license-policy.json](artifact-license-policy.json).
