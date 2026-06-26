from __future__ import annotations

import json
from typing import Any

from .payload import resolve_action


def parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        if value.startswith("[") or value.startswith("{"):
            return json.loads(value)
        if "." in value:
            return float(value)
        return int(value)
    except (ValueError, json.JSONDecodeError):
        return value


def parse_param_pairs(pairs: list[str] | None) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise ValueError(f"Parameter must use key=value syntax: {pair}")
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Parameter key cannot be empty: {pair}")
        params[key] = parse_scalar(value.strip())
    return params


def build_command(action: str, target: str | None = None, params: dict[str, Any] | None = None, command_id: str | None = None) -> dict[str, Any]:
    canonical, _ = resolve_action(action)
    command: dict[str, Any] = {"action": canonical}
    if command_id:
        command["id"] = command_id
    if target:
        command["target"] = target
    if params:
        command["params"] = params
    return command
