# Runbook

## Purpose

This repo validates Nexus Game Kit from outside the package repository.

## Baseline gates

1. Run Python unit tests.
2. Validate payloads in `payloads/smoke`.
3. Save a JSON report under `artifacts`.
4. For live Unity validation, run the manual live-host workflow with a reachable RPC endpoint.

## Failure handling

- Payload validation failures mean the queued command shape is not safe to send.
- RPC connection failures usually mean Unity is not running, the host window is not started, the port is wrong, or the auth token is mismatched.
- Queue failures should be preserved as report artifacts.

## Promotion rule

Do not promote generated prototype output unless payload validation, queue execution, and report capture have completed successfully.
