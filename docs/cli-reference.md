# CLI reference

`gamekit_runner` is the external validation-harness CLI implemented in `runner/gamekit_runner/cli.py`. It validates queue payloads locally and can call a configured Nexus Game Kit RPC host. The registered `build-actions` command has a known parser defect described below.

## Invocation

The repository workflows invoke the CLI as:

```sh
PYTHONPATH=runner python -m gamekit_runner [global-options] <command> [command-options]
```

Global options must appear before the command.

| Option | Default | Description |
| --- | --- | --- |
| `--base-url URL` | Environment or built-in client default | RPC host URL. The client first uses this option, then `NEXUS_RPC_URL`. |
| `--token TOKEN` | Environment value when available | Authentication token. The client uses `NEXUS_TOKEN` when this option is omitted. |
| `--timeout SECONDS` | `30.0` | Per-request RPC timeout. |

All commands print JSON to standard output. Unhandled input, file, or RPC errors print an error to standard error and exit with code `1`.

## Commands

### `health`

```sh
PYTHONPATH=runner python -m gamekit_runner health
```

Calls the RPC method `nexus.health` and prints its response. This command requires a reachable RPC host.

### `validate-payload`

```sh
PYTHONPATH=runner python -m gamekit_runner validate-payload <payload.json> [--report <report.json>]
```

Validates one JSON payload locally. `--report` writes a JSON run report containing the validation result.

### `validate-directory`

```sh
PYTHONPATH=runner python -m gamekit_runner validate-directory <directory> [--report <report.json>]
```

Recursively validates every `*.json` file under the directory. Its output and optional report contain an overall `ok` value, a file count, and per-file reports.

### `build-actions`

The parser registers this command with `--sequence-id`, `--output`, optional `--mode`, and a remainder intended to contain repeated `--action`, `--target`, and `--param` tokens. In the current `0.1.0` implementation, `argparse` rejects `--action` as an unrecognized argument. Adding a `--` separator does not work because the separator is passed to `command_build_actions()` and rejected as an unknown build token.

Do not rely on this command until the source parser is repaired and covered by a CLI-level test. Use a checked-in smoke payload or manually author JSON according to [the payload contract](payload-contract.md), then run `validate-payload` before queue operations.

The underlying `action_builder.py` module is covered by unit tests and converts parameter values as follows, but that does not make the broken CLI entry point usable:

- `true`, `false`, and `null` become JSON boolean or null values.
- Values beginning with `[` or `{` are parsed as JSON.
- Values containing `.` are parsed as floating-point numbers when possible.
- Other whole-number values are parsed as integers; values that cannot be parsed remain strings.

### `check`

```sh
PYTHONPATH=runner python -m gamekit_runner check <payload.json> [--report <report.json>]
```

Validates the payload locally, then sends it to the RPC method `queue.check`. No RPC call is made when local validation reports an error. With `--report`, the command writes the local validation result and RPC check response.

### `submit`

```sh
PYTHONPATH=runner python -m gamekit_runner submit <payload.json> [--wait] [--wait-timeout SECONDS] [--report <report.json>]
```

Validates the payload locally, calls `queue.check`, then calls `queue.submit`. `--wait` waits for an extracted queue/job identifier; `--wait-timeout` defaults to `120.0` seconds. The client first attempts `queue.wait`; if that call fails, it polls `queue.status` every two seconds. After a successful wait attempt, it also requests `queue.results`; a results-request failure is recorded as a warning in the report rather than terminating the command.

Use submission only with an appropriately controlled host. Repository guidance requires explicit approval before publishing generated prototype output.

## Local validation behavior

A payload must be a JSON object with a non-empty `commands` array. Every command must be an object with a non-empty string `action`; when present, `params` must be an object.

The validator reports warnings, but warnings do not make validation fail:

- A legacy action alias is accepted and normalized to its canonical action.
- An action outside the local canonical-action list is accepted with a warning.
- Most actions without `target` receive a warning. Actions beginning with `scene.save`, `selection.clear`, `playmode.`, `log.clear`, `validation.`, `runtime.`, `scene_state.get`, or `scene_settings.get` do not receive this warning.
- `mode` values outside `plan`, `dry_run`, and `live` receive a warning.

The local canonical actions and legacy aliases are defined in `runner/gamekit_runner/payload.py`. The smoke payloads in `payloads/smoke/` provide current examples of accepted payload structure.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | The command completed without a local validation error or unhandled exception. |
| `2` | Local payload validation found one or more errors. |
| `1` | Argument parsing, file handling, payload construction, or RPC processing raised an exception. |

For `check` and `submit`, a successful process exit means the CLI completed its calls; RPC response schemas and any remote queue-status semantics are not interpreted into additional CLI exit codes.

## Report files

Report paths are created with parent directories as needed. Validation reports contain validation details; `check` and `submit` reports also contain the relevant queue responses. Repository workflows store these JSON artifacts under `artifacts/`, which is ignored by Git.
