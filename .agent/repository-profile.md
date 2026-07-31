# Repository Profile

## Purpose

This repository is an external validation harness for Nexus Game Kit queue payloads. It is separate from the package repository and owns local payload validation, runner utilities, report generation, smoke examples, and harness workflows.

## Current Implementation

- `runner/gamekit_runner/` is a Python 3.10+ CLI package.
  - Validates JSON payload structure and normalizes known legacy action aliases.
  - Contains tested action-builder helpers, while the current `build-actions` CLI entry point is blocked by an argument-parser defect.
  - Calls a JSON-RPC host for health, queue checking, submission, waiting, and results.
  - Writes JSON run reports and validation bundles.
- `payloads/smoke/` contains dry-run examples covering scene, hierarchy/transform, material, particle, terrain, and asset-template actions.
- `tests/` uses the standard-library `unittest` framework for action construction, payload validation, and report writing.
- `.github/workflows/harness-tests.yml` runs unit tests and validates smoke payloads on pull requests and pushes to `main`; it uploads the validation report as an artifact.
- `.github/workflows/live-host-smoke.yml` is manually dispatched, validates a selected payload locally, then submits it to a configured live host and uploads reports.

## Repository Shape

```text
runner/gamekit_runner/  Python CLI, payload validation, RPC client, reporting
runner/config/          Package-source and validation-matrix configuration
payloads/smoke/         Example queue payloads
 tests/                 Unit tests
.github/workflows/      Harness and manually triggered live-host workflows
docs/                   Cloud-runner guidance
unity-projects/         Reserved location for future small runner projects
```

## Conventions and Safety

- Local payload errors block execution; warnings include legacy aliases, unrecognized local action names, and actions that usually need a target.
- Payload modes supported by the local validator are `plan`, `dry_run`, and `live`; generated payloads default to `dry_run`.
- Generated reports belong under ignored artifact/report locations rather than source control.
- Keep credentials and license data out of the repository. Live-host and generated-prototype publishing workflows require controlled access; publishing requires explicit approval.
- The runner is intended to interact through the Game Kit queue surface, rather than directly mutating Unity project files.

## Planned / Reserved Work

`unity-projects/` is reserved for small runner projects. Its README states that Unity 2020 and Unity 6 runner projects are to be added when the corresponding package tracks are ready for editor validation.

## Historical Note

`HISTORY.md` records version `0.1.0` as the initial harness baseline.
