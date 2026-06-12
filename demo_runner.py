"""青简译英演示脚本（无需 API Key）。

该脚本用于现场演示产品输出格式和讲解流程。
"""

from textwrap import dedent

DEMO_SOURCE = "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？"

DEMO_OUTPUT = dedent(
    """
    1) Literal Translation:
    The Master said: To learn and from time to time practice what one has learned—is this not a joy?
    To have friends come from afar—is this not a delight?

    2) Polished Translation:
    Confucius said, "To study and regularly review what you have studied—what greater pleasure is there?
    And when friends arrive from distant places—what greater happiness is there?"

    3) Notes:
    - 子曰: literally "The Master said," conventionally referring to Confucius.
    - 说 (yuè): in Classical usage, "delight/joy" (not modern "to speak").
    - 朋: often rendered "friends," but can imply fellow learners.
    """
).strip()


def main() -> None:
    print("=== 青简译英 Demo ===")
    print("\n[输入文言文]")
    print(DEMO_SOURCE)
    print("\n[示例输出]")
    print(DEMO_OUTPUT)
    print("\n提示：这是离线演示文本，用于路演/课堂；真实翻译请运行 translator_assistant.py。")


if __name__ == "__main__":
    main()
