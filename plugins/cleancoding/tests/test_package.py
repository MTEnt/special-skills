from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cleancoding"


class PackageTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        required = (
            ".claude-plugin/plugin.json",
            ".codex-plugin/plugin.json",
            "hooks/hooks.json",
            "hooks/verification_gate.py",
            "skills/cleancoding/SKILL.md",
            "skills/cleancoding/agents/openai.yaml",
            "evals/scenarios.json",
            "evals/rubric.json",
            "evals/run_behavior_suite.py",
            "README.md",
            "CHANGELOG.md",
        )
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_manifests_agree(self) -> None:
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude["name"], "cleancoding")
        self.assertEqual(codex["name"], "cleancoding")
        self.assertEqual(claude["version"], codex["version"])
        self.assertEqual(claude["hooks"], "./hooks/hooks.json")

    def test_skill_is_concise_and_routes_to_references(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(text.encode("utf-8")), 10000)
        for reference in re.findall(r"\]\((references/[a-z-]+\.md)\)", text):
            with self.subTest(reference=reference):
                self.assertTrue((SKILL / reference).is_file())
        self.assertIn("<!-- contract:loop-limit:start -->", text)
        self.assertIn("<!-- contract:handoff-receipt:start -->", text)

    def test_hooks_cover_the_gate_lifecycle(self) -> None:
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(set(config["hooks"]), {"SessionStart", "PostToolUse", "Stop", "SessionEnd"})
        for event in config["hooks"].values():
            for group in event:
                for hook in group["hooks"]:
                    self.assertIn("verification_gate.py", hook["command"])
                    self.assertIn("verification_gate.py", hook["commandWindows"])

    def test_post_tool_use_matcher_skips_read_only_tools(self) -> None:
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        matcher = re.compile(config["hooks"]["PostToolUse"][0]["matcher"])
        for tool in ("Edit", "Write", "MultiEdit", "NotebookEdit", "apply_patch", "Bash", "shell", "exec_command"):
            with self.subTest(tool=tool):
                self.assertTrue(matcher.search(tool))
        for tool in ("Read", "Grep", "Glob", "WebFetch", "Agent"):
            with self.subTest(tool=tool):
                self.assertIsNone(matcher.search(tool))


if __name__ == "__main__":
    unittest.main()
