"""CLI integration tests."""

from __future__ import annotations

import subprocess
import sys
import unittest


class CLIIntegrationTest(unittest.TestCase):
    """End-to-end CLI tests."""

    def test_cli_help(self) -> None:
        """Test CLI help message."""
        result = subprocess.run(
            [sys.executable, "translator_assistant.py", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--text", result.stdout)
        self.assertIn("--interactive", result.stdout)
        self.assertIn("--mock", result.stdout)

    def test_cli_mock_translation(self) -> None:
        """Test CLI with mock mode."""
        result = subprocess.run(
            [
                sys.executable,
                "translator_assistant.py",
                "--mock",
                "--text",
                "子曰：学而时习之，不亦说乎？",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Literal Translation", result.stdout)
        self.assertIn("Polished Translation", result.stdout)
        self.assertIn("Notes", result.stdout)

    def test_cli_rejects_empty_input(self) -> None:
        """Test CLI rejects empty input."""
        result = subprocess.run(
            [
                sys.executable,
                "translator_assistant.py",
                "--mock",
                "--text",
                "",
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr or "请先输入" in result.stdout)

    def test_cli_requires_text_or_interactive(self) -> None:
        """Test CLI requires --text or --interactive."""
        result = subprocess.run(
            [sys.executable, "translator_assistant.py"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--text", result.stderr)


if __name__ == "__main__":
    unittest.main()
