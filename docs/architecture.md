# Architecture

## Purpose and boundary

This repository is an external validation harness for Nexus Game Kit queue payloads. It is separate from the publishable package repository and does not own the Unity Editor control surface or package source. Its responsibilities are local payload validation, optional interaction with a controlled RPC host, and JSON report capture.

## Implemented shape

```text
payloads/smoke/ or CLI action input
            |
            v
runner/gamekit_runner/
  - action_builder: command construction and scalar parsing
  - payload: local validation, aliases, and payload construction
  - cli: command orchestration
  - rpc_client: optional JSON-RPC calls to a host
  - reporter: JSON report serialization
            |
            +--> local validation output
            +--> optional queue check / submission / result retrieval
            +--> caller-selected JSON report path
```

### Core components

- `runner/gamekit_runner/payload.py` owns the local payload rules. A valid payload requires a non-empty `commands` array; each command must be an object with a non-empty `action`; supplied `params` values must be objects. It also maintains local canonical action names and legacy aliases. Unknown actions, unsupported modes, aliases, and usually-missing targets produce warnings rather than validation errors.
- `runner/gamekit_runner/action_builder.py` converts command-line action input into commands, resolving aliases and parsing scalar parameter values.
- `runner/gamekit_runner/cli.py` exposes local validation, payload-directory validation, health checks, queue checks, and submission commands. It also registers action-payload construction, but the current parser does not successfully pass its option-like tokens to the builder. Queue-facing commands perform local validation before contacting a host.
- `runner/gamekit_runner/rpc_client.py` provides JSON-RPC transport. Submission performs a queue check, then submits the payload; optional waiting retrieves the queue result when available and otherwise polls queue status.
- `runner/gamekit_runner/reporter.py` serializes individual run reports and validation bundles as JSON.

## Inputs, configuration, and outputs

- `payloads/smoke/` contains example dry-run payloads covering scene, hierarchy and transform, material, particle, and terrain actions.
- `runner/config/validation-matrix.json` declares the supported Unity tracks, the smoke-payload directory, and required RPC method names. The current Python implementation does not load this file directly.
- `runner/config/gamekit-package-sources.json` records package-track and contract-path references for the separate package repository. The current Python implementation does not load this file directly.
- Reports are written only when the relevant CLI `--report` option is supplied. The repository ignores `artifacts/` and `reports/`, and the workflows use `artifacts/` for generated reports.

## Automation and safety boundaries

The `Harness Tests` workflow runs the Python unit tests, validates `payloads/smoke/`, and uploads the resulting validation report. The `Live Host Smoke` workflow is manually dispatched; it validates a selected payload locally, then submits it to an RPC host and uploads reports even if the live step fails.

Repository policy keeps sensitive data out of version control and requires explicit approval before publishing generated prototype output. The documented cloud-runner boundary is to consume the package as a dependency, avoid copying package source here, and avoid direct Unity-project mutation outside the Game Kit queue surface.

## Planned and historical notes

`unity-projects/` is reserved for small runner projects. Its README states that Unity 2020 and Unity 6 runner projects are to be added when their package tracks are ready for editor validation; no such project is currently checked in.

Version `0.1.0` is recorded as the initial harness baseline.

## Not asserted by this repository

This repository does not define the authoritative remote action, queue, capability, or alias schemas. Its local validation is a harness-side check and does not prove that a target host accepts or executes a payload.
