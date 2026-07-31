# Validation

## Purpose

This repository validates Nexus Game Kit queue payloads from outside the package repository. It provides local payload checks, a Python test suite, JSON reports, and an optional live-host smoke workflow.

## Validation layers

1. **Python unit tests** validate action construction, payload validation, and report writing.
2. **Local payload validation** checks JSON payload structure before any RPC call.
3. **Live-host smoke validation** performs a local validation, asks the host to check and submit one payload, and can wait for queue completion.

## Standard local checks

Run the repository's existing checks with Python 3.10 or later:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

The `Harness Tests` workflow runs these commands on pull requests, pushes to `main`, and manual dispatch. It uploads `artifacts/smoke-validation-report.json` when validation completes.

## Local payload rules

A locally valid payload must be a JSON object with a non-empty `commands` array. Each command must be an object with a non-empty string `action`; supplied `params` values must be objects.

The supported modes are `plan`, `dry_run`, and `live`. An omitted mode defaults to `dry_run`. An unsupported mode produces a warning, while structural violations produce errors and cause the validation command to exit unsuccessfully.

The local validator also reports warnings when an action uses a legacy alias, is not in its local canonical action list, or usually requires a target but has none. Warnings do not make the local validation fail. Local validation checks command shape only; it does not confirm that a live host accepts or successfully executes a payload.

## Live-host smoke workflow

`Live Host Smoke` is manually dispatched. It first runs `validate-payload`, then runs `submit` with queue waiting enabled and writes JSON reports under `artifacts/`. The live submission path performs a host-side queue check before submitting the payload. When a queue identifier is returned, it waits for completion and attempts to collect queue results.

Use a controlled, reachable host and configure authentication outside the repository. Preserve the generated report artifacts for queue or host failures. Do not treat local validation alone as evidence that a payload executed successfully.

## Reports

`validate-payload` and `check` can write a report containing the local validation result. `submit` can additionally record host queue-check, submission, wait, and results responses. `validate-directory` writes a bundle with an overall result, report count, and one local-validation report per JSON payload. The repository ignores `artifacts/` and `reports/` so generated reports are not committed by default.

## Current scope and limits

The smoke payloads exercise scene save/create, hierarchy and transform, material, particle, and terrain command examples. The configured validation matrix records Unity 2020 and Unity 6 package tracks plus required RPC method names; the checked-in Python runner does not show an automated verification of that full matrix. `unity-projects/` is reserved for future small runner projects rather than containing an editor-validation baseline.

The unit suite covers the underlying action builder, but it does not invoke the `build-actions` CLI parser. A direct CLI probe currently fails because `argparse` rejects the intended `--action` tokens. Treat that command as a known defect until a source repair and CLI-level test pass.

## Promotion gate

Generated prototype output must not be promoted until payload validation, queue execution, and report capture have all completed successfully.
