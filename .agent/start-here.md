# Start Here

## Purpose

This repository is the external validation harness for Nexus Game Kit. It is separate from the publishable package repository: the package owns the Unity Editor control surface; this repository owns payload validation, RPC runner utilities, reports, and smoke examples.

## What exists now

- Python CLI and library: `runner/gamekit_runner/`
- Local JSON payload validation and action construction
- JSON-RPC client support for health, queue checking, submission, waiting, and result retrieval
- Smoke payloads: `payloads/smoke/`
- CI validation of unit tests and smoke payloads: `.github/workflows/harness-tests.yml`
- Manually dispatched live-host smoke workflow: `.github/workflows/live-host-smoke.yml`

The tracked package metadata requires Python 3.10 or newer. The local validation configuration names Unity 2020.3 and Unity 6000.x as target tracks and lists the RPC methods expected by the harness.

## First local checks

From the repository root, the CI-equivalent local checks are:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

`artifacts/` is ignored by Git. Local validation checks payload structure; it does not execute commands in Unity.

## Working with payloads

Payloads are JSON objects with a non-empty `commands` array. Commands require an `action`; supplied `params` values must be objects. Supported modes are `plan`, `dry_run`, and `live`.

Prefer canonical dotted action names such as `scene.create` and `hierarchy.create`. The runner accepts certain legacy aliases but reports them as warnings. Unknown actions and missing targets for actions that usually need one also produce warnings, while malformed commands produce errors.

The underlying action-builder helpers are tested, but the current `build-actions` CLI entry point is blocked by an argument-parser defect. Use checked-in or manually authored JSON payloads and validate them locally instead.

Use `validate-payload` or `validate-directory` before contacting a host. For a reachable controlled host, `check` sends `queue.check`; `submit` performs a queue check, submits the payload, and can wait for results. Write reports with `--report` so queue failures are retained as artifacts.

## Boundaries and safety

- Do not copy the Unity package source into this repository.
- Do not store runner credentials, Unity license data, package credentials, or publishing credentials in Git.
- Prefer dry-run payloads for pull requests.
- Treat publishing generated prototype output as an explicitly approved action.
- Do not promote prototype output until local payload validation, queue execution, and report capture have succeeded.

## Current limits and planned work

`unity-projects/` is reserved for small runner projects. Its README describes Unity 2020 and Unity 6 runner projects as future additions when their package tracks are ready; no such runner projects are checked in here.

The recorded history is an initial `0.1.0` harness baseline.

## Verify before live execution

- Confirm the selected package revision and target Unity track against the consuming environment.
- Confirm that a controlled RPC host is reachable and has the required authentication configuration.
- Confirm the live host's action and queue contracts match the local validation assumptions before relying on a successful local check.
