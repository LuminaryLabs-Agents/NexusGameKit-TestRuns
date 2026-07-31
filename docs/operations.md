# Operations

## Scope and current status

This repository provides an external Python validation harness for Nexus Game Kit queue payloads. It does not own the Unity package or its editor control surface.

Implemented baseline:

- Local JSON payload validation and action construction.
- JSON-RPC client operations for health, queue checking, submission, waiting, status, and results.
- JSON report writing.
- Smoke payload examples in `payloads/smoke/`.
- A pull-request/push workflow for local harness checks and a manually started live-host smoke workflow.

Historical note: version `0.1.0` is the initial harness baseline.

## Prerequisites

- Python 3.10 or later. The checked-in CI workflows use Python 3.11.
- Run commands from the repository root with `PYTHONPATH=runner`.
- A reachable, controlled RPC host is required only for remote commands.

Do not store credentials, Unity license data, private package credentials, or publishing credentials in this repository.

## Local validation

Run the existing test suite:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
```

Validate all smoke payloads and write a report:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

Validate one payload:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-payload payloads/smoke/smoke-scene-create.json --report artifacts/local-validation.json
```

The validator requires a non-empty `commands` array. Missing command actions and non-object `params` are errors. Unknown actions, legacy action aliases, unsupported `mode` values, and missing usually-required targets produce warnings rather than local validation failure. Supported modes are `plan`, `dry_run`, and `live`; a missing mode is treated as `dry_run` by the local validator.

Generated reports can be placed under `artifacts/`; that directory is ignored by Git.

## Creating a payload

Use the checked-in smoke payloads as the current executable examples, or manually author JSON according to [the payload contract](payload-contract.md). Always run `validate-payload` before remote operations.

The CLI registers a `build-actions` command, but the current `0.1.0` argument parser rejects its intended `--action` tokens. This was reproduced with and without an option separator. Do not present that command as operational until its source parser and CLI-level coverage are repaired.

## Remote operations

Provide the RPC location through `NEXUS_RPC_URL` or `--base-url`. Provide the optional token through `NEXUS_TOKEN` or `--token`; when present, the client sends it in the `X-Nexus-Token` request header.

Check host availability before queue work:

```sh
PYTHONPATH=runner python -m gamekit_runner health
```

Validate a payload against the remote queue without submitting it:

```sh
PYTHONPATH=runner python -m gamekit_runner check payloads/smoke/smoke-scene-create.json --report artifacts/queue-check.json
```

Submit only after local validation and queue checking are appropriate for the target environment:

```sh
PYTHONPATH=runner python -m gamekit_runner submit payloads/smoke/smoke-scene-create.json --wait --report artifacts/queue-run.json
```

`submit` performs local validation, calls `queue.check`, then calls `queue.submit`. With `--wait`, it attempts `queue.wait`; if that call fails, it polls `queue.status` until a response contains `completed`, `failed`, `cancelled`, or `rejected`, or the wait timeout expires. When a queue identifier is available, it also requests `queue.results`.

Use dry-run payloads for pull-request validation. Live operations and generated prototype publishing require explicit approval.

## CI workflows

- `.github/workflows/harness-tests.yml` runs on pull requests, pushes to `main`, and manual dispatch. It runs unit tests, validates `payloads/smoke/`, and uploads `artifacts/smoke-validation-report.json`.
- `.github/workflows/live-host-smoke.yml` runs only by manual dispatch. It locally validates the selected payload, runs `submit --wait`, and uploads JSON reports even when the live operation fails.

## Failure handling

- Local validation failures mean the payload is not safe to send in its current shape.
- RPC connection failures can indicate that the host is unavailable, the configured RPC location is incorrect, or authentication does not match the host.
- Preserve queue-operation reports as artifacts for investigation.
- Do not promote generated prototype output until payload validation, queue execution, and report capture have completed successfully.

## Reference configuration

`runner/config/validation-matrix.json` records planned Unity tracks, smoke payload directories, and required RPC method names. `runner/config/gamekit-package-sources.json` records package-source and contract-path references. These files are not consumed by the inspected Python runner modules.

`unity-projects/` is reserved for small runner projects; its README states that Unity 2020 and Unity 6 runner projects are to be added when their package tracks are ready.
