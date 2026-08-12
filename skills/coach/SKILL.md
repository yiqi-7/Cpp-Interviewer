---
name: coach
description: C++ 面试训练入口。Use when the user invokes /coach or wants one-question-at-a-time practice, weak-topic training, due review, training plan, status dashboard, answer evaluation, and SQLite mastery tracking.
---

# Coach

This is a compatibility entry for `/coach`. Follow the agent-neutral core skill in `../cpp-interviewer/SKILL.md`, then use `../cpp-interviewer/references/coach-mode.md`.

## Runtime

Use the portable CLI when available:

```bash
python -m coach.cli topic search "<keyword>" --json
python -m coach.cli topic-info "<topic_id>" --json
python -m coach.cli topic-context "<topic_id_or_keyword>" --json
python -m coach.cli next-topic --difficulty 2 --json
python -m coach.cli save-result --topic-id "<topic_id>" --question "<question>" --answer "<answer>" --evaluation "<json>" --json
python -m coach.cli status --json
python -m coach.cli weak --json
python -m coach.cli due --json
python -m coach.cli plan --json
python -m coach.cli reset --yes --json
python -m coach.cli export --format md --output coach-export.md --json
```

Prefer `CPP_INTERVIEWER_HOME`, `CPP_INTERVIEWER_DB`, and `CPP_INTERVIEWER_INDEX` for state and index locations. If the CLI is unavailable, continue without persistence and say so briefly.

For `/coach export`, let the user choose `md`, `doc`, `txt`, or `json`. If they only ask to export, ask once for the format; if they do not give a path, use `coach-export.<format>`. Use `doc` for a Word-openable document.

For `/coach reset`, ask for explicit confirmation before running the reset command. Reset clears local training state only and keeps the knowledge index.

## Discipline

Ask one question at a time, wait for the user's answer, evaluate on six dimensions, save when possible, then ask one follow-up or next question. Do not give long teaching content unless the user asks.

## User Command

$ARGUMENTS
