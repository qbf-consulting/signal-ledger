# Public-readiness gate

Date: 2026-09-29

This gate records repository-local checks performed before changing Signal Ledger from private to public visibility.

## Gate results

| Check | Result | Evidence |
| --- | --- | --- |
| Default branch | PASS | `main` is the only remaining branch at audit start. |
| Open work residue | PASS | No open issues or pull requests at audit start. |
| Commit-history scope | PASS | History is compact and consists of the initial README plus expected issue/PR implementation tranches. |
| Credential-pattern scan | PASS | Default-branch searches found no password, secret, token, API-key, private-key, GitHub-token, or OpenAI-key patterns. |
| Personal/internal residue | PASS | No localhost, TODO/FIXME, private/internal markers, or personal Gmail address patterns were found by the audit searches. |
| Fixtures | PASS | Test fixtures use synthetic identifiers and `example.org` URIs. |
| Workflow permissions | PASS | Current workflows explicitly request `contents: read` only. |
| Generated/local-sensitive files | PASS after remediation | `.env*`, generated `artifacts/`, and common private-key extensions are excluded. |
| Documentation accuracy | PASS after remediation | README reflects implemented event, claim, evidence, significance, interoperability, and enrichment layers. |
| Security disclosure | PASS after remediation | SECURITY.md provides durable private-reporting guidance suitable for a public repository. |
| Licensing | PASS | QBF mixed licensing is declared in human- and machine-readable form and covered by tests. |
| End-to-end assurance | PASS | The Signal Ledger First Run workflow is a PR assurance gate and emits a validated machine-readable artifact. |

## Visibility-transition boundary

This gate covers repository content and connector-visible GitHub metadata. GitHub repository/organization settings that are not exposed through the available repository interface must be verified after the visibility change, especially branch/ruleset enforcement, Actions permissions, secret scanning/security features, and Pages deployment settings.

## Post-publication verification

After changing visibility to public:

1. confirm the repository reports `public`;
2. confirm the protect-main/ruleset posture still applies;
3. confirm Actions default permissions remain least-privilege;
4. enable and verify appropriate GitHub security/secret-scanning features;
5. configure GitHub Pages to deploy from Actions;
6. execute the Pages deployment and inspect the rendered site;
7. verify public links, licensing, security guidance, and workflow status from an unauthenticated view.

A public Pages projection must remain a read-only view of ledger state; it must not become an independent source of truth.
