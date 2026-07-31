# Contributing

## Scope

This repository is the external validation harness for Nexus Game Kit. Keep Unity package source in its package repository; this repository contains the Python runner, payload checks, reports, smoke payloads, and related runner documentation.

## Make a focused change

- Keep runner code under `runner/gamekit_runner/` and its tests under `tests/`.
- Add or update queue payload examples in `payloads/smoke/` using JSON objects with a non-empty `commands` array. When present, each command's `params` value must be an object.
- Prefer canonical action names. The validator accepts local legacy aliases but reports them as warnings.
- Keep generated reports in `artifacts/` or `reports/`; both are ignored by Git.
- Do not add Unity license data, package credentials, prototype-publishing credentials, or other production secrets.

## Validate changes

Run the repository's existing checks before sharing a change:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

The harness-test workflow runs these same checks for pushes and pull requests.

## Live-host work

Validate payloads locally before connecting to a Unity host. Live submission requires a reachable, controlled RPC host and an auth token when the environment is shared. Preserve queue failures in a report artifact. Generated prototype output must not be promoted until payload validation, queue execution, and report capture succeed; publishing also requires explicit manual approval.

## Current status

Implemented: the Python payload harness, runner client utilities, report writer, smoke payloads, and GitHub Actions harness checks.

Planned: `unity-projects/` is reserved for lightweight Unity 2020 and Unity 6 runner projects when the package tracks are ready.

Historical: version `0.1.0` is the initial harness baseline.
