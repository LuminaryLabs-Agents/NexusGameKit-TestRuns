# Nexus Game Kit Test Runs

A Python-based external validation harness for Nexus Game Kit queue payloads. It is separate from the package repository and provides local payload validation, RPC client utilities, JSON reports, smoke payloads, and CI workflows.

![Nexus Game Kit Test Runs workflow](docs/assets/brand/social-card.png)

## Requirements

- Python 3.10 or later
- `PYTHONPATH=runner` when running from a source checkout
- A reachable Nexus Game Kit RPC host only for `health`, `check`, and `submit` commands

## Quick start

Run the local unit tests:

```sh
PYTHONPATH=runner python -m unittest discover -s tests
```

Validate all smoke payloads and write a JSON report:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-directory payloads/smoke --report artifacts/smoke-validation-report.json
```

Validate one payload:

```sh
PYTHONPATH=runner python -m gamekit_runner validate-payload payloads/smoke/smoke-scene-create.json
```

## CLI

The `gamekit_runner` module supports these commands:

- `health` - call the RPC host health method.
- `validate-payload` - validate one local JSON payload without contacting a host.
- `validate-directory` - validate all JSON payloads below a directory.
- `build-actions` - intended to create a payload from command-line action entries; the current CLI parser rejects its action tokens, so use a checked-in or manually authored JSON payload until that source defect is repaired.
- `check` - locally validate a payload, then send it to `queue.check`.
- `submit` - locally validate, queue-check, and submit a payload; `--wait` also waits for and captures queue results when available.

RPC settings can be supplied with `--base-url`, `--token`, and `--timeout`, or through the `NEXUS_RPC_URL` and `NEXUS_TOKEN` environment variables.

## Payloads and reports

Payloads contain a non-empty `commands` array. Commands require an `action`; most actions also require a `target`. Local validation reports errors for malformed commands and warnings for legacy aliases, unknown actions, unusual modes, or missing targets where targets are normally expected.

The smoke examples in `payloads/smoke/` cover scene creation, hierarchy and transform updates, materials, particles, terrain, and a minimal save command. The runner can write individual run reports or validation bundles as JSON to a path supplied with `--report`.

## Repository layout

```text
runner/gamekit_runner/  Python CLI, payload validation, RPC client, and reporting
payloads/smoke/         Example queue payloads for smoke validation
tests/                  Python unit tests
runner/config/          Validation tracks, required RPC methods, and package-source metadata
.github/workflows/      CI and manually triggered live-host smoke workflows
```

## Automation and safety

The `Harness Tests` workflow runs unit tests, validates `payloads/smoke/`, and uploads the validation report. The manually triggered `Live Host Smoke` workflow validates a selected payload locally before submitting it to a configured RPC host and uploads its reports.

Do not commit credentials, Unity license data, or package/publishing credentials. Keep generated prototype publishing behind explicit approval. See [SECURITY.md](SECURITY.md), [RUNBOOK.md](RUNBOOK.md), and [docs/CLOUD_RUNNER.md](docs/CLOUD_RUNNER.md) for operational guidance.

## Documentation

- [Documentation index](docs/README.md)
- [Architecture](docs/architecture.md)
- [CLI reference](docs/cli-reference.md)
- [Payload contract](docs/payload-contract.md)
- [Operations](docs/operations.md)
- [Validation](docs/validation.md)
