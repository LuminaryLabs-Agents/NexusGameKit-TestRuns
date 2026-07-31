# Payload Contract

## Scope and status

This document records the implemented payload behavior of the external runner in this repository. It is a local safety check before a payload is sent to the queue surface; passing local validation does not establish live-host acceptance or execution success.

The repository history records this harness as the initial `0.1.0` baseline.

## Payload shape

A payload is a JSON object with a required, non-empty `commands` array.

```json
{
  "version": "1.0",
  "sequence_id": "example-sequence",
  "mode": "dry_run",
  "autoSaveAfterEachAction": false,
  "commands": [
    {
      "id": "example-command",
      "action": "scene.create",
      "target": "Assets/Scenes/Example.unity",
      "params": {}
    }
  ]
}
```

| Field | Local behavior |
| --- | --- |
| `commands` | Required. Must be a non-empty array. Each item must be an object with a non-blank string `action`. |
| `mode` | Optional; defaults to `dry_run` during validation. `plan`, `dry_run`, and `live` are the recognized values. Other values produce a warning, not an error. |
| `version` | Emitted as `1.0` by the payload builder. The local validator does not require or validate it. |
| `sequence_id` | Emitted by the payload builder. The local validator does not require or validate it. |
| `autoSaveAfterEachAction` | Emitted as `false` by the payload builder. The local validator does not validate it. |

## Command shape

A command uses the following fields:

| Field | Local behavior |
| --- | --- |
| `action` | Required non-blank string. Canonical actions are preferred. A known legacy alias resolves to its canonical action and produces a warning. An action outside the local canonical list also produces a warning. |
| `target` | Usually expected. The validator warns when it is missing or falsy, except for the action groups listed below. It does not validate target type or path syntax. |
| `params` | Optional. When supplied with a non-null value, it must be an object. |
| `id` | Used by smoke examples. The local validator does not require it, validate its type, or enforce uniqueness. |

Targets are optional locally for `scene.save`, `selection.clear`, and actions beginning with `playmode.`, `log.clear`, `validation.`, `runtime.`, `scene_state.get`, or `scene_settings.get`.

## Actions

Canonical actions are grouped below for readability. The local canonical list is implemented in `runner/gamekit_runner/payload.py`.

| Group | Actions |
| --- | --- |
| Scene and hierarchy | `scene.create`, `scene.open`, `scene.save`, `scene.delete`; `hierarchy.create`, `hierarchy.update`, `hierarchy.reparent`, `hierarchy.delete`; `transform.update`; `selection.set`, `selection.clear` |
| Scene view and capture | `scene_view.set_state`, `scene_view.frame`, `scene_view.capture_camera`, `scene_view.capture_window`; `editor.screenshot`, `hierarchy.capture` |
| Components and play mode | `component.create`, `component.update`, `component.delete`, `inspector.update`; `playmode.enter`, `playmode.exit`, `playmode.pause`, `playmode.step`, `playmode.wait_for_state`, `playmode.capture`; `log.clear`, `script.create` |
| Assets and prefabs | `asset.create`, `asset.clone`, `asset.rename`, `asset.move`, `asset.delete`, `asset.import_model`, `asset.import_model_many`; `model.configure`; `prefab.save`, `prefab.instantiate`, `prefab.create_variant`, `prefab.unpack`, `prefab.apply_overrides` |
| Materials | `material.create`, `material.clone`, `material.set_color`, `material.set_float`, `material.set_vector`, `material.set_texture`, `material.bulk_set`, `material.copy_properties`, `material.assign_to_renderer`, `material.assign_to_renderer_slot`, `material.assign_shared_to_many`, `material.get`, `material.list_properties`, `material.setup` |
| Environment and content | `render_settings.update`, `volume_profile.update_asset`, `scene_settings.get`; `particle.configure`; `terrain.create`, `terrain.apply_noise`, `terrain.stamp`, `terrain.smooth` |
| Validation and state | `validation.validate_scene`, `runtime.get_hierarchy`, `scene_state.get` |

Supported legacy aliases include `create_scene`, `open_scene`, `save_scene`, `create_empty`, `create_primitive`, `destroy`, `reparent`, `set_position`, `set_rotation`, `set_scale`, `set_scene_view`, `frame_selection`, `capture_scene`, `select_many`, `save_prefab`, `instantiate_prefab`, `import_model`, `import_model_many`, `rename_asset`, `configure_model`, `setup_materials`, `create_terrain`, `terrain_apply_noise`, `terrain_stamp`, and `terrain_smooth`.

## Validation outcome

Local validation fails only when it finds an error, including a missing or empty `commands` array, a non-object command, a missing or blank `action`, or a non-object non-null `params` value. Warnings do not make validation fail.

The validation report includes `ok`, the payload path when available, command count, canonicalized action names, and findings with a level, message, and JSON-style path.

## Queue use

The runner can submit a locally valid payload only after a queue check. The queue surface is invoked through `queue.check` and `queue.submit`; queue status, results, and waiting are supported by the client. Preserve queue failures in report artifacts as directed by `RUNBOOK.md`.

## Unknowns

- The authoritative Unity package schemas and alias definitions are referenced in `runner/config/gamekit-package-sources.json` but are not present in this repository checkout; their requirements are not documented here.
- Host-side validation rules, action-specific `params` schemas, result schemas, and execution semantics are not established by the local harness.
- The live queue's treatment of unknown actions, optional targets, versions, sequence IDs, command IDs, and autosave settings is not established by this repository.
