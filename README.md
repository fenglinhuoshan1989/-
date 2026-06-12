# 青简译英（文言文→英文翻译助手）

**青简译英** 是一个基于 OpenAI API 的命令行翻译助手，专注把中国文言文翻译成英文，并输出：

1. 直译（Literal Translation）
2. 润色译文（Polished Translation）
3. 注释（词义、典故、语法、省略主语等）

## 1) 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) 配置 API Key

```bash
export OPENAI_API_KEY="你的key"
```

## 3) 单次翻译

```bash
python translator_assistant.py --text "子曰：学而时习之，不亦说乎？"
```

## 4) 交互模式

```bash
python translator_assistant.py --interactive
```

## 可选参数

- `--model`：指定模型（默认 `gpt-5-mini`）
- `--text`：翻译单条文本
- `--interactive`：进入持续对话翻译模式
- `--mock`：离线 mock 演示模式（不调用 API）


## 5) 快速演示（无需 API Key）

如果你要现场演示产品（例如课堂或路演），可以直接运行离线 demo：

```bash
python demo_runner.py
```

这个脚本会展示：
- 一段典型文言文输入
- 三段式输出示例（直译 / 润色 / 注释）

> 注意：`demo_runner.py` 是固定示例，不调用模型；真实翻译请使用 `translator_assistant.py`。


## 6) Web UI（更丰富的界面）

如果你希望更丰富的 UI 界面（按钮、示例、参数滑块、可视化输出），可以运行 Gradio Web 应用：

```bash
python ui_app.py
```

启动后在浏览器打开本地地址（通常是 `http://127.0.0.1:7860`）。

界面能力：
- 多行文言文输入框
- 模型下拉选择
- temperature 滑块
- 一键翻译 / 回车翻译 / 清空
- 内置示例文本


### 离线运行（无依赖/无网络）

```bash
python translator_assistant.py --mock --text "子曰：学而时习之，不亦说乎？"
```
