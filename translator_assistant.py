"""青简译英 (QingJian Translate): Classical Chinese (文言文) -> English CLI."""

from __future__ import annotations

import argparse
import logging
import sys

from qingjian_core import DEFAULT_MODEL, DEFAULT_TEMPERATURE, translate_text

logger = logging.getLogger(__name__)


def interactive_loop(model: str, temperature: float, mock: bool = False) -> None:
    """Run interactive translation loop."""
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
        except ValueError as e:
            print(f"输入错误: {e}")
            logger.debug(f"Validation error: {e}", exc_info=True)
            continue
        except RuntimeError as e:
            print(f"翻译失败: {e}")
            logger.error(f"Translation error: {e}", exc_info=True)
            continue
        except Exception as e:  # noqa: BLE001
            print(f"未知错误: {e}")
            logger.error(f"Unexpected error: {e}", exc_info=True)
            continue

        print("\n=== 翻译结果 ===")
        print(result)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="青简译英：文言文 -> 英文翻译助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python translator_assistant.py --text "子曰：学而时习之，不亦说乎？"
  python translator_assistant.py --interactive
  python translator_assistant.py --mock --text "天行健"
        """,
    )
    parser.add_argument("--text", type=str, help="Single text to translate")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help=f"OpenAI model name (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Sampling temperature for API-backed translation (default: {DEFAULT_TEMPERATURE})",
    )
    parser.add_argument("--interactive", action="store_true", help="Start interactive translation mode")
    parser.add_argument("--mock", action="store_true", help="Use built-in mock translation without API")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not args.text and not args.interactive:
        print("请使用 --text 或 --interactive。", file=sys.stderr)
        print("Use --help 查看更多选项。", file=sys.stderr)
        return 1

    if args.interactive:
        interactive_loop(args.model, args.temperature, mock=args.mock)
        return 0

    try:
        result = translate_text(args.text, model=args.model, temperature=args.temperature, mock=args.mock)
    except ValueError as e:
        print(f"输入错误: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"翻译失败: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"未知错误: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
