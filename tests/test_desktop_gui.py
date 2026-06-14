"""Tests for desktop GUI configuration and demo path."""

from __future__ import annotations

import unittest

from desktop_gui import EXAMPLES, MODEL_CHOICES, QingJianDesktopApp
from gui_smoke_test import DEMO_TEXT, run_headless_demo
from qingjian_core import DEFAULT_MODEL


class DesktopGuiTest(unittest.TestCase):
    def test_gui_has_examples_and_default_model(self) -> None:
        self.assertGreaterEqual(len(EXAMPLES), 3)
        self.assertIn(DEFAULT_MODEL, MODEL_CHOICES)

    def test_gui_class_is_available_for_launch(self) -> None:
        self.assertEqual(QingJianDesktopApp.__name__, "QingJianDesktopApp")

    def test_headless_demo_uses_gui_demo_text(self) -> None:
        result = run_headless_demo()
        self.assertIn(DEMO_TEXT, result)
        self.assertIn("Polished Translation", result)


if __name__ == "__main__":
    unittest.main()
