"""青简译英 Web UI（Gradio）。"""

from __future__ import annotations

import os
from textwrap import dedent

import gradio as gr
from openai import OpenAI

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


def translate(text: str, model: str, temperature: float) -> str:
    text = (text or "").strip()
    if not text:
        return "请先输入文言文内容。"

    if not os.getenv("OPENAI_API_KEY"):
        return "缺少 OPENAI_API_KEY 环境变量，请先配置后再试。"

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Please translate the following Classical Chinese text into English:\n\n{text}",
            },
        ],
        temperature=temperature,
    )
    return response.output_text.strip()


def build_demo_examples() -> list[list[str]]:
    return [
        ["子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？", "gpt-5-mini", 0.3],
        ["天行健，君子以自强不息。", "gpt-5-mini", 0.2],
        ["路漫漫其修远兮，吾将上下而求索。", "gpt-5-mini", 0.4],
    ]


with gr.Blocks(title="青简译英 · 文言文翻译助手", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 青简译英（QingJian Translate）
        ### 文言文 → 英文翻译助手

        支持输出：**直译（Literal）**、**润色译文（Polished）**、**注释（Notes）**。
        """
    )

    with gr.Row():
        with gr.Column(scale=5):
            input_text = gr.Textbox(
                label="请输入文言文",
                lines=8,
                placeholder="例如：子曰：学而时习之，不亦说乎？",
            )
        with gr.Column(scale=2):
            model = gr.Dropdown(
                label="模型",
                choices=["gpt-5-mini", "gpt-5.4-mini", "gpt-5.4"],
                value="gpt-5-mini",
            )
            temperature = gr.Slider(0, 1, value=0.3, step=0.1, label="创造性（temperature）")
            run_btn = gr.Button("开始翻译", variant="primary")
            clear_btn = gr.Button("清空")

    output = gr.Markdown(label="翻译结果")

    gr.Examples(
        examples=build_demo_examples(),
        inputs=[input_text, model, temperature],
    )

    run_btn.click(translate, inputs=[input_text, model, temperature], outputs=output)
    input_text.submit(translate, inputs=[input_text, model, temperature], outputs=output)
    clear_btn.click(lambda: ("", ""), outputs=[input_text, output])


if __name__ == "__main__":
    app.launch()
