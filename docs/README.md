# Documentation

## Purpose

This repository is an external validation harness for Nexus Game Kit queue payloads. It is separate from the package repository and does not own the Unity Editor control surface or package source.

The harness provides:

- Local JSON payload validation.
- A Python command-line runner for validation, queue checks, and queue submission.
- JSON report writing.
- Smoke payload examples.
- GitHub Actions workflows for local harness checks and manually dispatched live-host smoke runs.

## Start here

- [Quickstart](../QUICKSTART.md) - concise local-validation starting point.
- [Runbook](../RUNBOOK.md) - baseline gates, failure handling, and promotion rule.
- [Cloud Runner](CLOUD_RUNNER.md) - cloud-runner responsibilities and non-goals.
- [Security](../SECURITY.md) - credential and RPC-host safety rules.
- [Smoke Payloads](../payloads/smoke/README.md) - queue payload examples.
- [Architecture](architecture.md) - ownership, components, and execution boundary.
- [CLI reference](cli-reference.md) - commands, options, exit codes, and reports.
- [Payload contract](payload-contract.md) - local validation shape and limitations.
- [Operations](operations.md) - local and controlled-host workflows.
- [Validation](validation.md) - automated and manual verification gates.
- [Visual identity](visual-identity.md) - repository asset pack and usage rules.

## Repository layout

```text
runner/gamekit_runner/  Python CLI, payload validation, RPC client, and reporting
runner/config/          Validation matrix and package-source metadata
payloads/smoke/         Checked-in smoke payload examples
tests/                  Python unit tests
.github/workflows/      Harness and manually dispatched live-host workflows
unity-projects/         Reserved location for small Unity runner projects
```

## Local validation

The project requires Python 3.10 or later and has no declared runtime dependencies. The checked-in workflow uses Python 3.11.

Validate the smoke payloads:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

Validate one payload:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-payload payloads/smoke/smoke-scene-create.json
```

Validation requires a non-empty `commands` array. Commands must provide an action; supplied `params` values must be JSON objects. The validator recognizes canonical actions and selected legacy aliases, and reports warnings for aliases, unrecognized actions, questionable modes, and usually-required targets.

## Runner commands

`gamekit_runner` exposes these subcommands:

- `health` - call the host health method.
- `validate-payload` - validate one JSON payload locally.
- `validate-directory` - validate every JSON payload below a directory.
- `build-actions` - intended action-payload construction; currently blocked by the parser limitation documented in the CLI reference.
- `check` - locally validate a payload, then request a remote queue check.
- `submit` - locally validate, queue-check, and submit a payload; it can also wait for results.

Remote commands accept optional base URL, token, and timeout arguments. Use them only with a local or controlled RPC host, following [Security](../SECURITY.md).

## Payloads and reports

Payloads are JSON objects containing queue commands. Builder-generated payloads use version `1.0`, a `sequence_id`, a mode (`plan`, `dry_run`, or `live`), `autoSaveAfterEachAction`, and `commands`.

The smoke directory contains examples covering scene creation, hierarchy and transform operations, materials, particles, terrain, and a minimal save action. Reports are written as JSON when a command receives `--report`; generated `artifacts/` and `reports/` directories are ignored by Git.

## Automation

`harness-tests.yml` runs Python unit tests, validates `payloads/smoke`, and uploads the validation report on pull requests, pushes to `main`, and manual dispatch.

`live-host-smoke.yml` is manually dispatched. It validates a selected payload locally, submits it to the configured RPC host, and uploads reports even if the live run fails.

## Current status

Version `0.1.0` is the initial harness baseline. The `unity-projects/` directory is reserved for small runner projects; its documentation states that Unity 2020 and Unity 6 runner projects should be added when their package tracks are ready.
