"""青简译英桌面 GUI（Tkinter）。

这是一个无需额外 GUI 依赖的桌面界面。默认启用离线演示模式，便于
没有 API Key 或未安装 OpenAI SDK 时预览完整翻译流程。
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk

from qingjian_core import DEFAULT_MODEL, DEFAULT_TEMPERATURE, translate_text

EXAMPLES = (
    "子曰：学而时习之，不亦说乎？",
    "天行健，君子以自强不息。",
    "路漫漫其修远兮，吾将上下而求索。",
)
MODEL_CHOICES = (DEFAULT_MODEL, "gpt-5.4-mini", "gpt-5.4")


class QingJianDesktopApp:
    """Tkinter desktop application for QingJian Translate."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("青简译英 · 文言文翻译助手")
        self.root.geometry("980x720")
        self.root.minsize(860, 620)

        self.model_var = tk.StringVar(value=DEFAULT_MODEL)
        self.temperature_var = tk.DoubleVar(value=DEFAULT_TEMPERATURE)
        self.mock_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="就绪：默认使用离线演示模式。")

        self._configure_style()
        self._build_layout()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Hero.TFrame", background="#f3ead7")
        style.configure("HeroTitle.TLabel", background="#f3ead7", foreground="#243426", font=("Arial", 22, "bold"))
        style.configure("HeroSubtitle.TLabel", background="#f3ead7", foreground="#44513f", font=("Arial", 12))
        style.configure("Primary.TButton", font=("Arial", 11, "bold"), padding=8)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=6)

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        hero = ttk.Frame(container, style="Hero.TFrame", padding=18)
        hero.pack(fill=tk.X, pady=(0, 14))
        ttk.Label(hero, text="青简译英（QingJian Translate）", style="HeroTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(
            hero,
            text="文言文 → 英文：一键生成直译、润色译文和学习注释。",
            style="HeroSubtitle.TLabel",
        ).pack(anchor=tk.W, pady=(6, 0))

        main = ttk.Frame(container)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(1, weight=1)

        ttk.Label(main, text="请输入文言文").grid(row=0, column=0, sticky=tk.W, pady=(0, 6))
        ttk.Label(main, text="翻译结果").grid(row=0, column=1, sticky=tk.W, padx=(12, 0), pady=(0, 6))

        self.input_text = tk.Text(main, height=16, wrap=tk.WORD, font=("Arial", 12), padx=10, pady=10)
        self.input_text.grid(row=1, column=0, sticky=tk.NSEW)
        self.input_text.insert("1.0", EXAMPLES[0])

        self.output_text = tk.Text(main, height=16, wrap=tk.WORD, font=("Arial", 11), padx=10, pady=10)
        self.output_text.grid(row=1, column=1, sticky=tk.NSEW, padx=(12, 0))
        self.output_text.configure(state=tk.DISABLED)

        controls = ttk.Frame(container)
        controls.pack(fill=tk.X, pady=(14, 8))
        controls.columnconfigure(6, weight=1)

        ttk.Label(controls, text="模型").grid(row=0, column=0, sticky=tk.W)
        ttk.Combobox(
            controls,
            textvariable=self.model_var,
            values=MODEL_CHOICES,
            width=18,
            state="readonly",
        ).grid(row=0, column=1, padx=(6, 18), sticky=tk.W)

        ttk.Label(controls, text="temperature").grid(row=0, column=2, sticky=tk.W)
        ttk.Scale(
            controls,
            from_=0,
            to=1,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL,
            length=150,
        ).grid(row=0, column=3, padx=(6, 18), sticky=tk.W)

        ttk.Checkbutton(controls, text="离线演示模式", variable=self.mock_var).grid(row=0, column=4, padx=(0, 18))

        self.translate_button = ttk.Button(controls, text="开始翻译", style="Primary.TButton", command=self.translate_async)
        self.translate_button.grid(row=0, column=5, padx=(0, 8))
        ttk.Button(controls, text="清空", command=self.clear).grid(row=0, column=6, sticky=tk.W)

        examples = ttk.Frame(container)
        examples.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(examples, text="示例：").pack(side=tk.LEFT)
        for example in EXAMPLES:
            ttk.Button(examples, text=example, command=lambda value=example: self.load_example(value)).pack(
                side=tk.LEFT,
                padx=(6, 0),
            )

        status = ttk.Label(container, textvariable=self.status_var, anchor=tk.W)
        status.pack(fill=tk.X)

    def load_example(self, value: str) -> None:
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", value)
        self.status_var.set("已载入示例文本。")

    def clear(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self._set_output("")
        self.status_var.set("已清空。")

    def translate_async(self) -> None:
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("缺少输入", "请先输入文言文内容。")
            return

        self.translate_button.configure(state=tk.DISABLED)
        self.status_var.set("翻译中……")
        worker = threading.Thread(target=self._translate_worker, args=(text,), daemon=True)
        worker.start()

    def _translate_worker(self, text: str) -> None:
        try:
            result = translate_text(
                text,
                model=self.model_var.get(),
                temperature=self.temperature_var.get(),
                mock=self.mock_var.get(),
            )
        except Exception as exc:  # noqa: BLE001
            result = f"⚠️ 翻译失败：{exc}"

        self.root.after(0, self._finish_translation, result)

    def _finish_translation(self, result: str) -> None:
        self._set_output(result)
        self.translate_button.configure(state=tk.NORMAL)
        self.status_var.set("完成。")

    def _set_output(self, text: str) -> None:
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.configure(state=tk.DISABLED)


def main() -> None:
    root = tk.Tk()
    QingJianDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
