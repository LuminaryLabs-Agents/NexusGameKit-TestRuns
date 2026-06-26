import json
import tempfile
import unittest
from pathlib import Path

from gamekit_runner.reporter import RunReport, write_report, write_validation_bundle

class ReporterTests(unittest.TestCase):
    def test_write_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            write_report(path, RunReport(name="sample", ok=True))
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(data["ok"])
            self.assertEqual(data["name"], "sample")

    def test_write_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bundle.json"
            write_validation_bundle(path, [{"ok": True}, {"ok": True}])
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(data["ok"])
            self.assertEqual(data["count"], 2)

if __name__ == "__main__":
    unittest.main()
