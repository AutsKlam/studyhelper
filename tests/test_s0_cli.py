from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTENT_FIELDS = {
    "topic",
    "evidence",
    "notes_mapping",
    "gaps",
    "next_action",
    "self_check",
}


def run_ask(fixture: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "evibrief",
            "ask",
            "--fixture",
            fixture,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


class S0CliTest(unittest.TestCase):
    def test_success_contract(self) -> None:
        result = run_ask("fixtures/s0_question.txt")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), CONTENT_FIELDS | {"run"})
        self.assertGreaterEqual(len(payload["evidence"]), 1)
        self.assertGreaterEqual(len(payload["notes_mapping"]), 1)

        evidence = payload["evidence"][0]
        self.assertEqual(
            set(evidence),
            {"claim", "snippet", "source_type", "locator", "date"},
        )
        self.assertEqual(evidence["source_type"], "local")

        notes_mapping = payload["notes_mapping"][0]
        self.assertEqual(set(notes_mapping), {"note", "relation", "locator"})
        self.assertIn(notes_mapping["relation"], {"supports", "contradicts", "missing"})
        self.assertEqual(payload["run"]["prompt_version"], "s0-placeholder")
        self.assertEqual(payload["run"]["materials_version"], "s0-fixture-v1")

    def test_empty_fixture_fails_readably(self) -> None:
        result = run_ask("fixtures/s0_empty.txt")

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"]["code"], "EMPTY_QUESTION")
        self.assertTrue(payload["error"]["message"])

    def test_missing_fixture_fails_readably(self) -> None:
        result = run_ask("fixtures/does-not-exist.txt")

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"]["code"], "FIXTURE_NOT_FOUND")
        self.assertTrue(payload["error"]["message"])

    def test_outside_fixtures_directory_is_rejected(self) -> None:
        result = run_ask("PLAN.md")

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"]["code"], "FIXTURE_NOT_FOUND")
        self.assertTrue(payload["error"]["message"])


if __name__ == "__main__":
    unittest.main()
