"""青简译英 (QingJian Translate): Classical Chinese (文言文) -> English CLI."""

from __future__ import annotations

import argparse
import sys

from qingjian_core import DEFAULT_MODEL, DEFAULT_TEMPERATURE, translate_text


def interactive_loop(model: str, temperature: float, mock: bool = False) -> None:
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
            result = translate_text(text, model=model, temperature=temperature, mock=mock)
        except Exception as exc:  # noqa: BLE001
            print(f"翻译失败：{exc}")
            continue

        print("\n=== 翻译结果 ===")
        print(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="青简译英：文言文 -> 英文翻译助手")
    parser.add_argument("--text", type=str, help="Single text to translate")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help="Sampling temperature for API-backed translation",
    )
    parser.add_argument("--interactive", action="store_true", help="Start interactive translation mode")
    parser.add_argument("--mock", action="store_true", help="Use built-in mock translation without API")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.text and not args.interactive:
        print("请使用 --text 或 --interactive。", file=sys.stderr)
        return 1

    if args.interactive:
        interactive_loop(args.model, args.temperature, mock=args.mock)
        return 0

    try:
        result = translate_text(args.text, model=args.model, temperature=args.temperature, mock=args.mock)
    except Exception as exc:  # noqa: BLE001
        print(f"翻译失败：{exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
