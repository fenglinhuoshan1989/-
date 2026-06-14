"""Unit tests for QingJian shared translation logic."""

from __future__ import annotations

import unittest

from qingjian_core import build_user_prompt, local_mock_translate, normalize_text, translate_text


class QingJianCoreTest(unittest.TestCase):
    def test_normalize_text_handles_none_and_whitespace(self) -> None:
        self.assertEqual(normalize_text(None), "")
        self.assertEqual(normalize_text("  子曰  "), "子曰")

    def test_build_user_prompt_includes_clean_text(self) -> None:
        prompt = build_user_prompt("  天行健  ")
        self.assertTrue(prompt.endswith("天行健"))

    def test_known_mock_translation_uses_realistic_demo_text(self) -> None:
        result = local_mock_translate("子曰：学而时习之，不亦说乎？")
        self.assertIn("The Master said", result)
        self.assertIn("Polished Translation", result)
        self.assertIn("Notes", result)

    def test_translate_text_rejects_empty_input(self) -> None:
        with self.assertRaises(ValueError):
            translate_text("", mock=True)

    def test_translate_text_mock_does_not_require_api(self) -> None:
        result = translate_text("未知文言示例", mock=True)
        self.assertIn("[MOCK]", result)


if __name__ == "__main__":
    unittest.main()
