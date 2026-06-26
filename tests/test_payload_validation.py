import unittest

from gamekit_runner.payload import validate_payload, resolve_action

class PayloadValidationTests(unittest.TestCase):
    def test_canonical_payload_passes(self):
        payload = {
            "version": "1.0",
            "mode": "dry_run",
            "commands": [
                {"action": "scene.create", "target": "Assets/Scenes/Smoke.unity"},
                {"action": "hierarchy.create", "target": "Smoke/Cube", "params": {"type": "Cube"}},
            ],
        }
        report = validate_payload(payload)
        self.assertTrue(report.ok)
        self.assertEqual(report.command_count, 2)

    def test_legacy_alias_warns_but_passes(self):
        payload = {"commands": [{"action": "create_scene", "target": "Assets/Scenes/Smoke.unity"}]}
        report = validate_payload(payload)
        self.assertTrue(report.ok)
        self.assertIn("scene.create", report.canonical_actions)
        self.assertTrue(any(item.level == "warning" for item in report.findings))

    def test_missing_action_fails(self):
        payload = {"commands": [{"target": "Missing/Action"}]}
        report = validate_payload(payload)
        self.assertFalse(report.ok)
        self.assertTrue(any(item.level == "error" for item in report.findings))

    def test_resolve_action(self):
        action, aliased = resolve_action("save_prefab")
        self.assertEqual(action, "prefab.save")
        self.assertTrue(aliased)

if __name__ == "__main__":
    unittest.main()
