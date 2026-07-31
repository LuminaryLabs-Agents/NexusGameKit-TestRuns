# Repository Memory

## Purpose

`NexusGameKit-TestRuns` is an external validation harness for Nexus Game Kit queue payloads. It is separate from the package repository: this repository owns payload validation, runner utilities, reports, smoke examples, and automation; the package repository owns the Unity Editor control surface.

## Architecture

- `runner/gamekit_runner/` is a dependency-free Python 3.10+ package and CLI.
  - `payload.py` loads payload JSON, resolves legacy action aliases, and performs local structural checks.
  - `action_builder.py` creates canonical commands and parses CLI parameter values.
  - `rpc_client.py` sends JSON-RPC health and queue requests to a configured host.
  - `reporter.py` writes formatted JSON reports and validation bundles.
- `payloads/smoke/` contains dry-run examples covering scene, hierarchy/transform, material, particle, and terrain actions.
- `tests/` uses the standard-library `unittest` framework for action building, validation, and report writing.
- `runner/config/` records package-track metadata and the required RPC-method matrix.
- `.github/workflows/` runs unit tests plus smoke-payload validation for pushes to `main` and pull requests; a separate manually dispatched workflow validates and submits one payload to a live host and uploads reports.

## Conventions

- Payloads are JSON objects with a non-empty `commands` array. Commands require an `action`; `params`, when supplied, must be an object.
- Prefer canonical dotted action names. Legacy aliases are accepted locally but reported as warnings.
- Use `plan`, `dry_run`, or `live` for payload mode. Unsupported modes and actions outside the local canonical list warn rather than fail; structural errors fail validation.
- Validate locally before RPC queue checks or submission. Persist optional reports as JSON; generated artifacts belong under ignored artifact/report directories.
- Keep this repository independent of package source. Do not copy Unity package code here or mutate Unity projects except through the Game Kit queue surface.
- Do not commit credentials, license data, or publishing credentials. Treat publishing generated prototype output as requiring explicit manual approval.

## Implemented CLI Surface

`python -m gamekit_runner` provides health checking, individual or directory payload validation, remote queue checking, and queue submission with optional waiting/results capture. The registered `build-actions` command is not currently usable because `argparse` rejects its intended option-like action tokens; preserve this limitation until source repair and CLI-level coverage prove otherwise.

## Plans and History

- `unity-projects/` is reserved for small runner projects; Unity 2020 and Unity 6 runner-project baselines are planned when their package tracks are ready.
- Version `0.1.0` is the initial harness baseline.

## Unknowns

- This checkout contains no package contract/schema files, so compatibility between the local canonical-action list and the package contract is not verified here.
- No checked-in Unity runner project or recorded live-host execution result is present in this checkout.
