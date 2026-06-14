"""Shared translation logic for 青简译英 (QingJian Translate)."""

from __future__ import annotations

import os
from textwrap import dedent
from typing import Any

DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_TEMPERATURE = 0.3

SYSTEM_PROMPT = dedent(
    """
    You are an expert in Classical Chinese (文言文), historical context, and literary translation.
    Your task is to translate Classical Chinese into high-quality English.

    Output format (strict):
    1) Literal Translation: a close, line-faithful translation.
    2) Polished Translation: idiomatic literary English while preserving meaning.
    3) Notes:
       - Explain difficult words, allusions, grammar inversions, and omitted subjects.
       - If there are ambiguities, provide 1-2 plausible readings.
       - Keep notes concise and useful for learners.

    Requirements:
    - Never hallucinate source text that was not provided.
    - Preserve names, era-specific terms, and titles with transliteration when necessary.
    - If text is not Classical Chinese, politely state this and still provide best-effort translation.
    """
).strip()

MOCK_TRANSLATIONS = {
    "子曰：学而时习之，不亦说乎？": dedent(
        """
        1) Literal Translation:
        The Master said: To learn and from time to time practice it—is this not a joy?

        2) Polished Translation:
        Confucius said, "Is it not a pleasure to study and regularly put what one has learned into practice?"

        3) Notes:
        - 子曰: "The Master said," conventionally referring to Confucius.
        - 时习之: literally "practice it at due times"; 之 points back to what has been learned.
        - 说 (yuè): here means "delight/pleasure," not the modern verb "to speak" (shuō).
        """
    ).strip(),
    "天行健，君子以自强不息。": dedent(
        """
        1) Literal Translation:
        Heaven's movement is strong and vigorous; the noble person therefore strengthens himself without ceasing.

        2) Polished Translation:
        As Heaven moves with tireless vigor, so the gentleman strives constantly for self-renewal.

        3) Notes:
        - 天行健: from the Book of Changes; 健 suggests strength, vitality, and unceasing motion.
        - 君子: an ethically cultivated person, often translated as "gentleman" or "noble person."
        - 以: here indicates drawing a model from the preceding image: "therefore/by this."
        """
    ).strip(),
    "路漫漫其修远兮，吾将上下而求索。": dedent(
        """
        1) Literal Translation:
        The road is long, long, and far-reaching; I shall go high and low in search.

        2) Polished Translation:
        Long and distant is the road ahead; I will search above and below until I find my way.

        3) Notes:
        - 漫漫: describes great length or vastness.
        - 修远: long and distant; 修 can mean "long" in Classical Chinese.
        - 上下而求索: an idiom-like phrase of exhaustive searching, here rendered as "search above and below."
        """
    ).strip(),
}


def normalize_text(text: str | None) -> str:
    """Normalize user input and gracefully handle missing text."""

    return (text or "").strip()


def build_user_prompt(text: str) -> str:
    """Build the user message sent to the model."""

    return f"Please translate the following Classical Chinese text into English:\n\n{normalize_text(text)}"


def has_api_key() -> bool:
    """Return whether an OpenAI API key is configured."""

    return bool(os.getenv("OPENAI_API_KEY"))


def local_mock_translate(text: str) -> str:
    """Return a deterministic offline response for demos and tests."""

    clean_text = normalize_text(text)
    if clean_text in MOCK_TRANSLATIONS:
        return MOCK_TRANSLATIONS[clean_text]

    return dedent(
        f"""
        1) Literal Translation:
        [MOCK] Close English rendering of: {clean_text}

        2) Polished Translation:
        [MOCK] A smoother literary English version of: {clean_text}

        3) Notes:
        - Mock mode is enabled; no API call was made.
        - This fallback keeps the production output shape for offline demos.
        - Set OPENAI_API_KEY and disable mock mode for real translation.
        """
    ).strip()


def translate_text(
    text: str,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    mock: bool = False,
    client: Any | None = None,
) -> str:
    """Translate Classical Chinese text into English.

    The OpenAI SDK is imported lazily so mock mode and unit tests can run in
    offline environments without optional runtime dependencies installed.
    """

    clean_text = normalize_text(text)
    if not clean_text:
        raise ValueError("请先输入文言文内容。")

    if mock:
        return local_mock_translate(clean_text)

    if not has_api_key() and client is None:
        raise RuntimeError("缺少 OPENAI_API_KEY 环境变量。可启用 mock 模式进行离线演示。")

    from openai import OpenAI

    api_client = client or OpenAI()
    response = api_client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(clean_text)},
        ],
        temperature=temperature,
    )
    return response.output_text.strip()
