"""Unit tests for QingJian shared translation logic."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from qingjian_core import (
    build_user_prompt,
    local_mock_translate,
    normalize_text,
    translate_text,
    validate_input,
)


class QingJianCoreTest(unittest.TestCase):
    """Tests for core translation logic."""

    def test_normalize_text_handles_none_and_whitespace(self) -> None:
        """Test text normalization."""
        self.assertEqual(normalize_text(None), "")
        self.assertEqual(normalize_text("  子曰  "), "子曰")

    def test_build_user_prompt_includes_clean_text(self) -> None:
        """Test user prompt construction."""
        prompt = build_user_prompt("  天行健  ")
        self.assertTrue(prompt.endswith("天行健"))
        self.assertIn("Classical Chinese", prompt)

    def test_validate_input_rejects_empty_text(self) -> None:
        """Test input validation rejects empty input."""
        with self.assertRaises(ValueError) as ctx:
            validate_input("")
        self.assertIn("请先输入", str(ctx.exception))

    def test_validate_input_rejects_long_text(self) -> None:
        """Test input validation rejects overly long input."""
        long_text = "文" * 3000  # Exceed 2000 character limit
        with self.assertRaises(ValueError) as ctx:
            validate_input(long_text)
        self.assertIn("过长", str(ctx.exception))

    def test_known_mock_translation_uses_realistic_demo_text(self) -> None:
        """Test mock translation returns realistic output."""
        result = local_mock_translate("子曰：学而时习之，不亦说乎？")
        self.assertIn("The Master said", result)
        self.assertIn("Polished Translation", result)
        self.assertIn("Notes", result)

    def test_translate_text_rejects_empty_input(self) -> None:
        """Test translate_text rejects empty input."""
        with self.assertRaises(ValueError):
            translate_text("", mock=True)

    def test_translate_text_mock_does_not_require_api(self) -> None:
        """Test mock mode works without API."""
        result = translate_text("未知文言示例", mock=True)
        self.assertIn("[MOCK]", result)
        self.assertIn("Close English rendering", result)

    def test_translate_text_respects_max_length(self) -> None:
        """Test translate_text enforces input length limit."""
        long_text = "文" * 2500
        with self.assertRaises(ValueError):
            translate_text(long_text, mock=True)


class QingJianAPITest(unittest.TestCase):
    """Tests for API integration."""

    @patch("qingjian_core.OpenAI")
    def test_translate_with_api_success(self, mock_openai_class: MagicMock) -> None:
        """Test successful API translation."""
        # Setup mock client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Mock the response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test translation result"
        mock_client.chat.completions.create.return_value = mock_response

        # Test translation
        result = translate_text("子曰", mock=False, client=mock_client)

        # Verify
        self.assertEqual(result, "Test translation result")
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        self.assertIn("model", call_args.kwargs)
        self.assertIn("messages", call_args.kwargs)
        self.assertIn("temperature", call_args.kwargs)

    @patch("qingjian_core.OpenAI")
    def test_translate_handles_api_timeout(self, mock_openai_class: MagicMock) -> None:
        """Test timeout retry logic."""
        from openai import APITimeoutError

        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Simulate timeout on first call, success on second
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Recovered result"
        mock_client.chat.completions.create.side_effect = [
            APITimeoutError("Timeout"),
            mock_response,
        ]

        # Should retry and succeed
        result = translate_text("子曰", mock=False, client=mock_client)
        self.assertEqual(result, "Recovered result")
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)

    @patch("qingjian_core.OpenAI")
    def test_translate_fails_after_max_retries(self, mock_openai_class: MagicMock) -> None:
        """Test exhausted retries raise error."""
        from openai import APIConnectionError

        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Always fail
        mock_client.chat.completions.create.side_effect = APIConnectionError("Connection failed")

        # Should fail after retries
        with self.assertRaises(RuntimeError) as ctx:
            translate_text("子曰", mock=False, client=mock_client)
        self.assertIn("重试", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
