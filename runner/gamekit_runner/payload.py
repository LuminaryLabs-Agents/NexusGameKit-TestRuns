from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

CANONICAL_ACTIONS = {
    "scene.create", "scene.open", "scene.save", "scene.delete",
    "hierarchy.create", "hierarchy.update", "hierarchy.reparent", "hierarchy.delete",
    "transform.update", "selection.set", "selection.clear",
    "scene_view.set_state", "scene_view.frame", "scene_view.capture_camera", "scene_view.capture_window",
    "editor.screenshot", "hierarchy.capture",
    "component.create", "component.update", "component.delete", "inspector.update",
    "playmode.enter", "playmode.exit", "playmode.pause", "playmode.step", "playmode.wait_for_state", "playmode.capture",
    "log.clear", "script.create",
    "asset.create", "asset.clone", "asset.rename", "asset.move", "asset.delete", "asset.import_model", "asset.import_model_many",
    "model.configure", "prefab.save", "prefab.instantiate", "prefab.create_variant", "prefab.unpack", "prefab.apply_overrides",
    "material.create", "material.clone", "material.set_color", "material.set_float", "material.set_vector", "material.set_texture",
    "material.bulk_set", "material.copy_properties", "material.assign_to_renderer", "material.assign_to_renderer_slot",
    "material.assign_shared_to_many", "material.get", "material.list_properties", "material.setup",
    "render_settings.update", "volume_profile.update_asset", "scene_settings.get",
    "particle.configure", "terrain.create", "terrain.apply_noise", "terrain.stamp", "terrain.smooth",
    "validation.validate_scene", "runtime.get_hierarchy", "scene_state.get",
}

ALIASES = {
    "create_scene": "scene.create",
    "open_scene": "scene.open",
    "save_scene": "scene.save",
    "create_empty": "hierarchy.create",
    "create_primitive": "hierarchy.create",
    "destroy": "hierarchy.delete",
    "reparent": "hierarchy.reparent",
    "set_position": "transform.update",
    "set_rotation": "transform.update",
    "set_scale": "transform.update",
    "set_scene_view": "scene_view.set_state",
    "frame_selection": "scene_view.frame",
    "capture_scene": "scene_view.capture_camera",
    "select_many": "selection.set",
    "save_prefab": "prefab.save",
    "instantiate_prefab": "prefab.instantiate",
    "import_model": "asset.import_model",
    "import_model_many": "asset.import_model_many",
    "rename_asset": "asset.rename",
    "configure_model": "model.configure",
    "setup_materials": "material.setup",
    "create_terrain": "terrain.create",
    "terrain_apply_noise": "terrain.apply_noise",
    "terrain_stamp": "terrain.stamp",
    "terrain_smooth": "terrain.smooth",
}

TARGET_OPTIONAL_PREFIXES = (
    "scene.save",
    "selection.clear",
    "playmode.",
    "log.clear",
    "validation.",
    "runtime.",
    "scene_state.get",
    "scene_settings.get",
)

@dataclass
class ValidationFinding:
    level: str
    message: str
    path: str = "$"

@dataclass
class ValidationReport:
    ok: bool
    payload_path: str | None = None
    command_count: int = 0
    findings: list[ValidationFinding] = field(default_factory=list)
    canonical_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "payload_path": self.payload_path,
            "command_count": self.command_count,
            "canonical_actions": self.canonical_actions,
            "findings": [finding.__dict__ for finding in self.findings],
        }


def load_payload(path: str | Path) -> dict[str, Any]:
    payload_path = Path(path)
    with payload_path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Payload root must be an object: {payload_path}")
    return value


def resolve_action(action: str) -> tuple[str, bool]:
    canonical = ALIASES.get(action, action)
    return canonical, canonical != action


def action_needs_target(action: str) -> bool:
    return not any(action.startswith(prefix) for prefix in TARGET_OPTIONAL_PREFIXES)


def validate_payload(payload: dict[str, Any], payload_path: str | None = None) -> ValidationReport:
    findings: list[ValidationFinding] = []
    canonical_actions: list[str] = []

    commands = payload.get("commands")
    if not isinstance(commands, list) or not commands:
        findings.append(ValidationFinding("error", "Payload must contain a non-empty commands array", "$.commands"))
        return ValidationReport(False, payload_path, 0, findings, canonical_actions)

    mode = payload.get("mode", "dry_run")
    if mode not in {"plan", "dry_run", "live"}:
        findings.append(ValidationFinding("warning", "mode should be one of plan, dry_run, or live", "$.mode"))

    for index, command in enumerate(commands):
        path = f"$.commands[{index}]"
        if not isinstance(command, dict):
            findings.append(ValidationFinding("error", "Command must be an object", path))
            continue
        action = command.get("action")
        if not isinstance(action, str) or not action.strip():
            findings.append(ValidationFinding("error", "Command must include action", f"{path}.action"))
            continue
        canonical, used_alias = resolve_action(action.strip())
        canonical_actions.append(canonical)
        if used_alias:
            findings.append(ValidationFinding("warning", f"Legacy action alias {action!r} resolves to {canonical!r}", f"{path}.action"))
        if canonical not in CANONICAL_ACTIONS:
            findings.append(ValidationFinding("warning", f"Action {canonical!r} is not in the local canonical action list", f"{path}.action"))
        if action_needs_target(canonical) and not command.get("target"):
            findings.append(ValidationFinding("warning", f"Action {canonical!r} usually needs a target", f"{path}.target"))
        params = command.get("params", {})
        if params is not None and not isinstance(params, dict):
            findings.append(ValidationFinding("error", "params must be an object when supplied", f"{path}.params"))

    ok = not any(finding.level == "error" for finding in findings)
    return ValidationReport(ok, payload_path, len(commands), findings, canonical_actions)


def validate_payload_file(path: str | Path) -> ValidationReport:
    payload = load_payload(path)
    return validate_payload(payload, str(path))


def build_payload(sequence_id: str, mode: str, commands: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "version": "1.0",
        "sequence_id": sequence_id,
        "mode": mode,
        "autoSaveAfterEachAction": False,
        "commands": commands,
    }
