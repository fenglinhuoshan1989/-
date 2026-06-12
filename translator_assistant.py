"""青简译英 (QingJian Translate): Classical Chinese (文言文) -> English assistant.

Usage:
  1) Set OPENAI_API_KEY
  2) python translator_assistant.py --text "子曰：学而时习之，不亦说乎？"
  3) python translator_assistant.py --interactive
"""

from __future__ import annotations

import argparse
import os
import sys
from textwrap import dedent


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


def build_user_prompt(text: str) -> str:
    return f"Please translate the following Classical Chinese text into English:\n\n{text.strip()}"


def local_mock_translate(text: str) -> str:
    return f"""1) Literal Translation:
[MOCK] {text}

2) Polished Translation:
[MOCK] A polished English rendering of: {text}

3) Notes:
- Mock mode is enabled; no API call was made.
- Set OPENAI_API_KEY and disable --mock for real translation.
""".strip()


def translate_text(client, model: str, text: str, mock: bool = False) -> str:
    if mock:
        return local_mock_translate(text)

    from openai import OpenAI  # lazy import so mock mode works without dependency

    if client is None:
        client = OpenAI()

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text)},
        ],
        temperature=0.3,
    )
    return response.output_text.strip()


def interactive_loop(client, model: str, mock: bool = False) -> None:
    print("青简译英已启动。输入 q 退出。")
    while True:
        try:
            text = input("\n请输入文言文：\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            return

        if not text:
            print("请输入非空文本。")
            continue
        if text.lower() in {"q", "quit", "exit"}:
            print("再见！")
            return

        try:
            result = translate_text(client, model, text, mock=mock)
        except Exception as exc:  # noqa: BLE001
            print(f"翻译失败：{exc}")
            continue

        print("\n=== 翻译结果 ===")
        print(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classical Chinese -> English translation assistant")
    parser.add_argument("--text", type=str, help="Single text to translate")
    parser.add_argument("--model", type=str, default="gpt-5-mini", help="OpenAI model name")
    parser.add_argument("--interactive", action="store_true", help="Start interactive translation mode")
    parser.add_argument("--mock", action="store_true", help="Use built-in mock translation without API")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.mock and not os.getenv("OPENAI_API_KEY"):
        print("缺少 OPENAI_API_KEY 环境变量。可加 --mock 进行离线演示。", file=sys.stderr)
        return 1

    if not args.text and not args.interactive:
        print("请使用 --text 或 --interactive。", file=sys.stderr)
        return 1

    client = None

    if args.interactive:
        interactive_loop(client, args.model, mock=args.mock)
        return 0

    result = translate_text(client, args.model, args.text, mock=args.mock)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
