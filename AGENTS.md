# AGENTS.md

## Purpose

This repository is the external validation harness for Nexus Game Kit queue payloads. It does not own the Unity package source or its editor control surface.

## Repository layout

- `runner/gamekit_runner/` - Python CLI, local payload validation, JSON-RPC client, command builder, and report writing.
- `runner/config/` - package-source references and validation matrix.
- `payloads/smoke/` - example queue payloads used for local and live smoke checks.
- `tests/` - Python `unittest` coverage for payload validation, command construction, and reporting.
- `.github/workflows/` - harness-test and manually triggered live-host workflows.
- `unity-projects/` - reserved for small Unity runner projects; no runner project baseline is currently checked in.

## Working conventions

- Use a focused review branch and pull request; do not commit directly to `main`.
- Keep this repository separate from the Nexus Game Kit package source; do not copy the package into it.
- Send Unity changes through the Game Kit queue surface rather than mutating Unity project files directly.
- Treat local payload validation as a safety gate before any queue check or submission.
- Keep smoke payloads JSON objects with a non-empty `commands` array. Commands require a non-empty `action`; supplied `params` must be an object.
- Prefer canonical action names from `runner/gamekit_runner/payload.py`. Aliases are accepted locally but produce warnings.
- Use `dry_run` payloads for pull-request validation. `plan`, `dry_run`, and `live` are the recognized modes.
- Write generated reports under ignored output directories such as `artifacts/` or `reports/`; do not commit them.
- Do not commit credentials, Unity license data, package credentials, or publishing credentials. Use the configured secret mechanism for runner authentication.
- Keep publishing of generated prototype output behind explicit manual approval.

## Validation commands

Run from the repository root:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

For a single payload, use `validate-payload`. Queue checks and submissions require a reachable, controlled Game Kit RPC host and should follow successful local validation.

## Change guidance

- Preserve the current standard-library-only Python implementation unless the task requires a dependency change.
- Keep CLI behavior in `runner/gamekit_runner/cli.py`, payload rules in `runner/gamekit_runner/payload.py`, transport concerns in `runner/gamekit_runner/rpc_client.py`, and JSON report serialization in `runner/gamekit_runner/reporter.py`.
- Update or add smoke payload examples only when their command shapes remain locally valid.
- Run the relevant existing unit tests and payload validation after behavior changes.
- The live-host workflow is manually dispatched; preserve its local-validation-before-submission sequence and artifact reporting.
