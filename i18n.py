"""Internationalization (i18n) system for QingJian Translate."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class I18n:
    """Multi-language translation system."""

    # Supported languages
    SUPPORTED_LANGUAGES = ["zh_CN", "en_US"]

    def __init__(self, language: str = "zh_CN"):
        """Initialize i18n with specified language.

        Args:
            language: Language code (e.g., 'zh_CN', 'en_US')
        """
        if language not in self.SUPPORTED_LANGUAGES:
            logger.warning(
                f"Unsupported language '{language}', falling back to 'en_US'"
            )
            language = "en_US"

        self.language = language
        self.translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()

    def _load_translations(self) -> None:
        """Load translation files from locales directory."""
        from config import LOCALES_DIR

        lang_file = LOCALES_DIR / f"{self.language}.json"

        if not lang_file.exists():
            logger.warning(f"Translation file not found: {lang_file}")
            return

        try:
            with open(lang_file, encoding="utf-8") as f:
                self.translations[self.language] = json.load(f)
                logger.debug(f"Loaded {len(self.translations[self.language])} translations for {self.language}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse translation file {lang_file}: {e}")
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")

    def t(self, key: str, **kwargs) -> str:
        """Get translated text.

        Args:
            key: Translation key (e.g., 'input.prompt')
            **kwargs: Format parameters

        Returns:
            Translated text, or key if translation not found
        """
        text = self.translations.get(self.language, {}).get(key, key)

        try:
            return text.format(**kwargs) if kwargs else text
        except KeyError as e:
            logger.warning(f"Missing format parameter in translation '{key}': {e}")
            return text

    def get_language(self) -> str:
        """Get current language code."""
        return self.language

    def set_language(self, language: str) -> None:
        """Change language at runtime."""
        if language in self.SUPPORTED_LANGUAGES:
            self.language = language
            self._load_translations()
        else:
            logger.warning(f"Cannot set unsupported language: {language}")


# Global i18n instance
_i18n_instance: Optional[I18n] = None


def get_i18n() -> I18n:
    """Get or create global i18n instance."""
    global _i18n_instance

    if _i18n_instance is None:
        from config import DEFAULT_LANGUAGE

        _i18n_instance = I18n(language=DEFAULT_LANGUAGE)

    return _i18n_instance
