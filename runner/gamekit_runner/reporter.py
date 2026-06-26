from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

@dataclass
class RunReport:
    name: str
    ok: bool
    validation: dict[str, Any] | None = None
    health: dict[str, Any] | None = None
    queue_check: dict[str, Any] | None = None
    queue_submit: dict[str, Any] | None = None
    queue_wait: dict[str, Any] | None = None
    queue_results: dict[str, Any] | None = None
    artifacts: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "validation": self.validation,
            "health": self.health,
            "queue_check": self.queue_check,
            "queue_submit": self.queue_submit,
            "queue_wait": self.queue_wait,
            "queue_results": self.queue_results,
            "artifacts": self.artifacts,
            "notes": self.notes,
        }


def write_json(path: str | Path, value: dict[str, Any]) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def write_report(path: str | Path, report: RunReport) -> Path:
    return write_json(path, report.to_dict())


def write_validation_bundle(path: str | Path, reports: list[dict[str, Any]]) -> Path:
    ok = all(report.get("ok") for report in reports)
    bundle = {"ok": ok, "count": len(reports), "reports": reports}
    return write_json(path, bundle)
