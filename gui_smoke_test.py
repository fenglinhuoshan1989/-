"""Headless-friendly GUI smoke test and demo for 青简译英.

This script validates the desktop GUI wiring without requiring a visible display.
It also prints a self-contained demo translation example so reviewers can see
what the GUI will show in offline mode.
"""

from __future__ import annotations

import logging
import os
import sys
import tkinter as tk

from desktop_gui import EXAMPLES, MODEL_CHOICES, QingJianDesktopApp
from qingjian_core import DEFAULT_MODEL, DEFAULT_TEMPERATURE, translate_text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEMO_TEXT = "学而不思则罔，思而不学则殆。"


def has_display() -> bool:
    """Return whether this process appears able to open a Tk window."""

    if sys.platform.startswith("win") or sys.platform == "darwin":
        return True
    return bool(os.environ.get("DISPLAY"))


def run_headless_demo() -> str:
    """Run a deterministic offline demo that mirrors the GUI translation path."""

    logger.debug("Running headless demo")
    return translate_text(
        DEMO_TEXT,
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        mock=True,
    )


def run_optional_window_smoke() -> str:
    """Instantiate the Tkinter GUI when a display is available; otherwise skip."""

    if not has_display():
        return "SKIP: no graphical display detected; headless smoke demo only."

    try:
        root = tk.Tk()
        root.withdraw()
        app = QingJianDesktopApp(root)
        root.update_idletasks()
        title = root.title()
        root.destroy()
        return f"OK: desktop GUI initialized with title: {title}; app={app.__class__.__name__}"
    except Exception as e:  # noqa: BLE001
        logger.error(f"GUI initialization failed: {e}", exc_info=True)
        return f"ERROR: desktop GUI failed to initialize: {e}"


def main() -> int:
    """Main entry point."""
    print("=== 青简译英 GUI Smoke Test ===")
    print(f"GUI class: {QingJianDesktopApp.__name__}")
    print(f"Default model choices: {', '.join(MODEL_CHOICES)}")
    print(f"Built-in GUI examples: {len(EXAMPLES)}")
    print(run_optional_window_smoke())
    print("\n[界面演示输入]")
    print(DEMO_TEXT)
    print("\n[界面演示输出]")
    try:
        print(run_headless_demo())
    except Exception as e:  # noqa: BLE001
        logger.error(f"Demo failed: {e}", exc_info=True)
        print(f"Demo error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
