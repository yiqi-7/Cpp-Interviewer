[English](README_EN.md) | [中文](README.md)

# Cpp-Interviewer

Agent-neutral C++ interview learning and practice skills. Clone it, run the installer, restart your agent, and use `/interview` or `/coach`.

## Quick Install

Give this to your local agent:

```text
Install Cpp-Interviewer:
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py --agents all
Restart the target agent, then test /interview or /coach.
```

Default install:

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

Install to selected agents or a custom skills directory:

```bash
python setup.py --agents codex,cursor,claude
python setup.py --skills-dir /path/to/your/agent/skills
```

Common targets:

| Agent | Skills directory |
|-------|------------------|
| Codex / ChatGPT | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| Generic agent skills | `~/.agents/skills/` |

Instruction-only agents can use `.github/copilot-instructions.md`, `GEMINI.md`, or point directly at `skills/cpp-interviewer/SKILL.md`.

## Modes

| Entry | Purpose | Example |
|-------|---------|---------|
| `/interview` | Concise explanations | `/interview How are virtual functions implemented` |
| `/coach` | One-question-at-a-time practice | `/coach virtual_function`, `/coach weak` |

`/interview` gives direct interview-ready explanations. `/coach` asks a question, waits for your answer, evaluates it, stores mastery when possible, and asks the next question.

## State

No API key, PDF files, or Git LFS setup is required. Training state defaults to `~/.cpp-interviewer/coach.sqlite`.

Override paths with:

```bash
export CPP_INTERVIEWER_HOME="$HOME/.cpp-interviewer"
export CPP_INTERVIEWER_DB="$HOME/.cpp-interviewer/coach.sqlite"
export CPP_INTERVIEWER_INDEX="/path/to/knowledge_index.json"
```

## Developer Mode

```bash
python -m pytest -q
python -m coach.cli status
python -m coach.cli topic search virtual_function --json
python -m coach.cli topic-context cpp_vtable --json
```

Run `python setup.py develop` only if you want the `coach` / `cpp-coach` console scripts.

## Repository Structure

```text
.
├── skills/
│   ├── cpp-interviewer/      # agent-neutral core skill
│   ├── interview/            # /interview compatibility entry
│   └── coach/                # /coach entry + Python backend
├── .github/copilot-instructions.md
├── GEMINI.md
├── setup.py
└── tests/
```

## License

This project is licensed under the [MIT License](LICENSE).
