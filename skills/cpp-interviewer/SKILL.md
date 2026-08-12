---
name: cpp-interviewer
description: Agent-neutral C++ interview learning and training skill. Use when the user wants C++ interview explanations, interview-style follow-up questions, weak-topic practice, spaced review, mastery tracking, or portable /interview and /coach behavior across Codex, Claude Code, Cursor, Gemini, Copilot, and other agents.
---

# Cpp-Interviewer

Act as a C++ interview learning partner with two modes:

- **Interview mode**: explain C++ and CS interview topics clearly, then provide likely follow-up questions.
- **Coach mode**: run one-question-at-a-time interview practice with scoring and optional persistence.

Keep platform-specific tool names out of the core workflow. Use the host agent's normal file, shell, web, and question-asking tools as needed.

## Mode Selection

- Use `references/interview-mode.md` when the user asks for an explanation, answer, summary, "八股", "讲一下", or uses `/interview`.
- Use `references/coach-mode.md` when the user wants practice, weak-topic training, due review, status, a plan, or uses `/coach`.
- Use `references/knowledge-schema.md` before editing or validating `knowledge_index.json`.

## Portable Runtime

Prefer these environment variables when reading or writing state:

- `CPP_INTERVIEWER_HOME`: user data directory.
- `CPP_INTERVIEWER_DB`: SQLite database path.
- `CPP_INTERVIEWER_INDEX`: knowledge index path.

If they are unset, use the repository-local `index/knowledge_index.json` and the user data directory `~/.cpp-interviewer`.

Use the Python CLI for deterministic state operations:

```bash
python -m coach.cli topic search "<keyword>" --json
python -m coach.cli topic-info "<topic_id>" --json
python -m coach.cli next-topic --difficulty 2 --json
python -m coach.cli save-result --topic-id "<topic_id>" --question "<question>" --answer "<answer>" --evaluation "<json>" --json
python -m coach.cli status --json
python -m coach.cli weak --json
python -m coach.cli due --json
python -m coach.cli plan --json
```

If the CLI is unavailable, continue conversationally and state that persistence is disabled.
