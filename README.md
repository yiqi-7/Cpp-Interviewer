# Cpp-Interviewer

在 AI Agent 里复习 C++ 面试知识，或让它一题一题和你练。

[English](#english) · [反馈问题](https://github.com/yiqi-7/Cpp-Interviewer/issues) · [MIT 许可证](LICENSE)

| 你想做什么 | 在 Agent 中输入 |
| --- | --- |
| 快速搞懂一个考点，直接看解释 | `/interview 虚函数表存在哪里？` |
| 模拟面试，回答后获得评价和追问 | `/coach 虚函数` |

## 快速开始

需要 Git、Python 3.10+ 和支持本地 Skill 的 Agent。下面的命令默认安装到 Codex 的 `~/.codex/skills/`。

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

看到 `[OK] codex` 后重启 Agent，试试上面任一条消息。`/interview` 会直接解释，`/coach` 会先出一道题并等待你的回答。

<details>
<summary>安装到 Claude Code、Cursor 或其他目录</summary>

在仓库根目录运行对应的命令。

```bash
python setup.py --agents claude
python setup.py --agents cursor
python setup.py --skills-dir /path/to/skills
```

没有斜杠命令入口的 Agent 可以读取[核心 Skill](skills/cpp-interviewer/SKILL.md)并按指定模式对话。Copilot 也有[仓库指令](.github/copilot-instructions.md)。

</details>

## 检查训练状态

在仓库根目录运行以下命令。全新数据库会返回 `"total_questions": 0`。

```bash
python -m coach.cli status --json
```

训练记录默认保存在 `~/.cpp-interviewer/coach.sqlite`。Agent 能调用 Python CLI 时才会记录成绩，只有 Skill 文件时也可以对话练习。项目使用宿主 Agent 的模型和内置知识索引，无需为本项目单独配置 API Key 或下载 PDF。

## 示例与开发

- [回答示例](skills/cpp-interviewer/references/answer-examples.md)展示讲解和陪练各自的第一轮表现。
- [Coach 使用说明](skills/coach/SKILL.md)列出薄弱项训练、到期复习和状态查询等入口。
- 安装 `pytest` 后运行 `python -m pytest -q`。工程测试覆盖安装布局和 CLI。实际的 Skill 触发及回答质量依赖宿主与模型，评测方法见[行为评测说明](evals/README.md)。

<details>
<summary>Star History</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg">
  <img src="./assets/star-history-light.svg" alt="Cpp-Interviewer star history">
</picture>

</details>

## English

Cpp-Interviewer adds two C++ interview modes to your AI agent. Try `/interview Where is the vtable stored?` for a direct explanation, or `/coach virtual functions` to get one question and answer it before receiving feedback.

Use the [installation commands](#快速开始) with Git and Python 3.10+, then restart your agent. The default installer target is Codex. Pass `--agents claude` or `--agents cursor` for the other supported installer layouts. For agents without slash commands, point your agent at the [core skill](skills/cpp-interviewer/SKILL.md).

From the repo root, `python -m coach.cli status --json` returns `"total_questions": 0` on a fresh database. Persistence requires CLI access. The host agent supplies the model, and the included index works without downloading PDFs.

[Behavior evals](evals/README.md) · [Issues](https://github.com/yiqi-7/Cpp-Interviewer/issues) · [MIT license](LICENSE)

<details>
<summary>Star History</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg">
  <img src="./assets/star-history-light.svg" alt="Cpp-Interviewer star history">
</picture>

</details>
