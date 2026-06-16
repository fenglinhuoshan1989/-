"""青简译英 Web UI（Gradio）。"""

from __future__ import annotations

import html
import logging

import gradio as gr

from qingjian_core import DEFAULT_MODEL, DEFAULT_TEMPERATURE, translate_text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MODEL_CHOICES = [DEFAULT_MODEL, "gpt-4.5-mini", "gpt-4.5"]


def translate(text: str, model: str, temperature: float, mock: bool) -> str:
    """Translate text with error handling."""
    try:
        logger.debug(f"Web UI translation request: model={model}, mock={mock}")
        result = translate_text(text, model=model, temperature=temperature, mock=mock)
        # Escape HTML special characters in output for safety
        return html.escape(result)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return f"⚠️ **输入错误**: {html.escape(str(e))}"
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        return f"⚠️ **翻译失败**: {html.escape(str(e))}"
    except Exception as e:  # noqa: BLE001
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"⚠️ **系统错误**: {html.escape(str(e))}"


def build_demo_examples() -> list[list[object]]:
    """Build demo examples for the interface."""
    return [
        ["子曰：学而时习之，不亦说乎？", DEFAULT_MODEL, DEFAULT_TEMPERATURE, True],
        ["天行健，君子以自强不息。", DEFAULT_MODEL, 0.2, True],
        ["路漫漫其修远兮，吾将上下而求索。", DEFAULT_MODEL, 0.4, True],
    ]


CUSTOM_CSS = """
#qingjian-hero {
    padding: 28px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #f3ead7 0%, #e3f2e6 54%, #d9e7ff 100%);
    border: 1px solid rgba(78, 65, 38, 0.14);
}
#qingjian-hero h1 { margin-bottom: 4px; }
#qingjian-output { min-height: 360px; }
"""


with gr.Blocks(
    title="青简译英 · 文言文翻译助手",
    theme=gr.themes.Soft(),
    css=CUSTOM_CSS,
) as app:
    gr.Markdown(
        """
        <div id="qingjian-hero">
          <h1>青简译英（QingJian Translate）</h1>
          <p><strong>文言文 → 英文翻译助手</strong></p>
          <p>一键生成 <strong>Literal Translation</strong>、<strong>Polished Translation</strong> 与 <strong>Notes</strong>，适合课堂、读书会和翻译初稿。</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=5):
            input_text = gr.Textbox(
                label="请输入文言文",
                lines=10,
                placeholder="例如：子曰：学而时习之，不亦说乎？",
            )
        with gr.Column(scale=2):
            model = gr.Dropdown(label="模型", choices=MODEL_CHOICES, value=DEFAULT_MODEL)
            temperature = gr.Slider(
                0,
                1,
                value=DEFAULT_TEMPERATURE,
                step=0.1,
                label="创造性（temperature）",
            )
            mock = gr.Checkbox(
                label="离线演示模式（不调用 API）",
                value=True,
            )
            run_btn = gr.Button("开始翻译", variant="primary")
            clear_btn = gr.Button("清空")

    output = gr.Markdown(label="翻译结果", elem_id="qingjian-output")

    gr.Examples(examples=build_demo_examples(), inputs=[input_text, model, temperature, mock])

    run_btn.click(translate, inputs=[input_text, model, temperature, mock], outputs=output)
    input_text.submit(translate, inputs=[input_text, model, temperature, mock], outputs=output)
    clear_btn.click(lambda: ("", ""), outputs=[input_text, output])


if __name__ == "__main__":
    app.launch()
