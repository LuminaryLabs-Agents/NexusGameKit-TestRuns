import unittest

from gamekit_runner.action_builder import build_command, parse_param_pairs

class ActionBuilderTests(unittest.TestCase):
    def test_param_parsing(self):
        params = parse_param_pairs(["count=3", "name=Smoke"])
        self.assertEqual(params["count"], 3)
        self.assertEqual(params["name"], "Smoke")

    def test_build_command_resolves_alias(self):
        command = build_command("create_empty", "World/Root", {"name": "Root"})
        self.assertEqual(command["action"], "hierarchy.create")
        self.assertEqual(command["target"], "World/Root")

if __name__ == "__main__":
    unittest.main()
