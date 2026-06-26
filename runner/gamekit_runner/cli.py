from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .action_builder import build_command, parse_param_pairs
from .payload import build_payload, load_payload, validate_payload, validate_payload_file
from .reporter import RunReport, write_report, write_validation_bundle
from .rpc_client import GameKitRpcClient, RpcError


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def command_health(args: argparse.Namespace) -> int:
    client = GameKitRpcClient(args.base_url, args.token, args.timeout)
    result = client.health()
    _print_json(result)
    return 0


def command_validate_payload(args: argparse.Namespace) -> int:
    report = validate_payload_file(args.payload)
    result = report.to_dict()
    if args.report:
        write_report(args.report, RunReport(name=str(args.payload), ok=report.ok, validation=result))
    _print_json(result)
    return 0 if report.ok else 2


def command_validate_directory(args: argparse.Namespace) -> int:
    root = Path(args.directory)
    reports: list[dict[str, Any]] = []
    for payload_path in sorted(root.rglob("*.json")):
        report = validate_payload_file(payload_path).to_dict()
        reports.append(report)
    if args.report:
        write_validation_bundle(args.report, reports)
    bundle = {"ok": all(item.get("ok") for item in reports), "count": len(reports), "reports": reports}
    _print_json(bundle)
    return 0 if bundle["ok"] else 2


def command_build_actions(args: argparse.Namespace) -> int:
    commands = []
    current_action: str | None = None
    current_target: str | None = None
    current_params: list[str] = []

    def flush() -> None:
        nonlocal current_action, current_target, current_params
        if current_action is None:
            return
        commands.append(build_command(current_action, current_target, parse_param_pairs(current_params)))
        current_action = None
        current_target = None
        current_params = []

    index = 0
    tokens = args.items
    while index < len(tokens):
        token = tokens[index]
        if token == "--action":
            flush()
            index += 1
            current_action = tokens[index]
        elif token == "--target":
            index += 1
            current_target = tokens[index]
        elif token == "--param":
            index += 1
            current_params.append(tokens[index])
        else:
            raise ValueError(f"Unknown build token: {token}")
        index += 1
    flush()

    payload = build_payload(args.sequence_id, args.mode, commands)
    report = validate_payload(payload).to_dict()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _print_json({"output": str(output), "validation": report})
    return 0 if report["ok"] else 2


def command_check(args: argparse.Namespace) -> int:
    payload = load_payload(args.payload)
    local = validate_payload(payload, str(args.payload)).to_dict()
    if not local["ok"]:
        _print_json(local)
        return 2
    client = GameKitRpcClient(args.base_url, args.token, args.timeout)
    result = client.queue_check(payload)
    if args.report:
        write_report(args.report, RunReport(name=str(args.payload), ok=True, validation=local, queue_check=result))
    _print_json(result)
    return 0


def extract_queue_id(value: dict[str, Any]) -> str | None:
    text = json.dumps(value)
    for key in ["queue_id", "queueId", "job_id", "jobId", "id"]:
        if key in value and isinstance(value[key], str):
            return value[key]
    if isinstance(value.get("result"), dict):
        return extract_queue_id(value["result"])
    return None


def command_submit(args: argparse.Namespace) -> int:
    payload = load_payload(args.payload)
    local = validate_payload(payload, str(args.payload)).to_dict()
    if not local["ok"]:
        _print_json(local)
        return 2
    client = GameKitRpcClient(args.base_url, args.token, args.timeout)
    check = client.queue_check(payload)
    submit = client.queue_submit(payload)
    queue_wait = None
    queue_results = None
    queue_id = extract_queue_id(submit)
    if args.wait and queue_id:
        queue_wait = client.queue_wait(queue_id, args.wait_timeout)
        try:
            queue_results = client.queue_results(queue_id)
        except RpcError as exc:
            queue_results = {"warning": str(exc)}
    report = RunReport(str(args.payload), True, local, queue_check=check, queue_submit=submit, queue_wait=queue_wait, queue_results=queue_results)
    if args.report:
        write_report(args.report, report)
    _print_json(report.to_dict())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gamekit_runner")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--token", default=None)
    parser.add_argument("--timeout", type=float, default=30.0)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("health")
    p.set_defaults(func=command_health)

    p = sub.add_parser("validate-payload")
    p.add_argument("payload")
    p.add_argument("--report")
    p.set_defaults(func=command_validate_payload)

    p = sub.add_parser("validate-directory")
    p.add_argument("directory")
    p.add_argument("--report")
    p.set_defaults(func=command_validate_directory)

    p = sub.add_parser("build-actions")
    p.add_argument("--sequence-id", required=True)
    p.add_argument("--mode", default="dry_run", choices=["plan", "dry_run", "live"])
    p.add_argument("--output", required=True)
    p.add_argument("items", nargs=argparse.REMAINDER)
    p.set_defaults(func=command_build_actions)

    p = sub.add_parser("check")
    p.add_argument("payload")
    p.add_argument("--report")
    p.set_defaults(func=command_check)

    p = sub.add_parser("submit")
    p.add_argument("payload")
    p.add_argument("--wait", action="store_true")
    p.add_argument("--wait-timeout", type=float, default=120.0)
    p.add_argument("--report")
    p.set_defaults(func=command_submit)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
