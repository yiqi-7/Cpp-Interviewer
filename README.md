# Cpp-Interviewer

在本地 AI Agent 里复习 C++ 面试知识，或一题一题练习。使用宿主 Agent 的模型，无需另配 API Key 或下载 PDF。

[开始使用](#快速开始) · [English](#english) · [问题反馈](https://github.com/yiqi-7/Cpp-Interviewer/issues) · [MIT](LICENSE)

**技术栈：** Python 3.10+（安装与本地训练 CLI）· SQLite（训练记录）· Markdown（Agent 指令与知识库）。

## 快速开始

需要 Git、Python 3.10+ 和能读取本地文件的 Agent。

**1. 在终端安装 Skill。** 以下命令默认安装到 Codex。

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

看到 `[OK] codex: ...` 后，Skill 已复制到 `~/.codex/skills/`。使用 Claude Code 或 Cursor 时，将最后一条命令改为 `python setup.py --agents claude` 或 `python setup.py --agents cursor`。

**2. 重启 Agent，打开刚克隆的仓库，先试试陪练：**

`/coach 虚函数`

成功时，Agent 会先问一道虚函数题并等待你回答；你回答后，它会给出评价并继续训练。想直接看讲解时，可改用 `/interview 虚函数表存在哪里？`。

**没有斜杠入口？** 仍在这个仓库的 Agent 会话里，把下面这句话当普通消息发出去：

> 请读取 `skills/cpp-interviewer/SKILL.md`，按 coach 模式训练我：虚函数。先问一道题，等我回答后再评价。

## 继续使用

- [Coach 指南](skills/cpp-interviewer/references/coach-mode.md) · [回答示例](skills/cpp-interviewer/references/answer-examples.md)
- [自定义安装参数](setup.py) · [Copilot 指令](.github/copilot-instructions.md)

训练记录默认保存在 `~/.cpp-interviewer/coach.sqlite`。Agent 无法调用 Python CLI 时，可以继续练习，但不会保存成绩。

<details>
<summary>可选：检查本地训练后端</summary>

在仓库根目录运行：

```bash
python -m coach.cli status --json
```

全新数据库的输出包含 `"total_questions": 0`。这说明 CLI 能读取训练状态，不代表 Agent 已加载 Skill 或已完成一次练习。

在其他项目目录调用后端时，见[运行与路径说明](skills/cpp-interviewer/SKILL.md#portable-runtime)。

</details>

贡献前安装 `pytest` 并运行 `python -m pytest -q`。安装与 CLI 测试之外，Skill 触发与回答质量另有[行为评测指南](evals/README.md)。

<details>
<summary>Star History</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg">
  <img src="./assets/star-history-light.svg" alt="Cpp-Interviewer star history">
</picture>

</details>

## English

Review C++ topics with `/interview`, or practice one question at a time with `/coach`. The host agent supplies the model; no separate API key or PDF download is required.

**Stack:** Python 3.10+ (installer and local training CLI) · SQLite (practice history) · Markdown (agent instructions and knowledge base).

Follow the [quick start](#快速开始) with Git and Python 3.10+. The installer defaults to Codex; add `--agents claude` or `--agents cursor` for those hosts. Look for `[OK]`, then restart your agent and open the cloned repo. Start with `/coach virtual functions`: it should ask one question and wait for your answer before giving feedback. For a direct explanation, try `/interview Where is the vtable stored?`.

No slash entry? Send this as a regular message in the repo's agent session:

> Read `skills/cpp-interviewer/SKILL.md` and use coach mode to practice virtual functions. Ask one question, wait for my answer, then give feedback.

[Runtime and paths](skills/cpp-interviewer/SKILL.md#portable-runtime) · [Behavior evals](evals/README.md) · [Issues](https://github.com/yiqi-7/Cpp-Interviewer/issues) · [MIT](LICENSE)

<details>
<summary>Star History</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg">
  <img src="./assets/star-history-light.svg" alt="Cpp-Interviewer star history">
</picture>

</details>
