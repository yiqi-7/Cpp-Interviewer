# Cpp-Interviewer Agent Instructions

When the user asks for C++ interview explanations, interview practice, weak-topic review, training plans, or mastery tracking, follow the core skill at `skills/cpp-interviewer/SKILL.md`.

Use `skills/cpp-interviewer/references/interview-mode.md` for explanation tasks and `skills/cpp-interviewer/references/coach-mode.md` for one-question-at-a-time training.

Prefer the portable CLI and environment variables documented in the core skill.

- Export coach data with `python -m coach.cli export --format json|md|txt|doc --output <path>`.
- Reset coach state with `python -m coach.cli reset --yes` only after explicit user confirmation.
- If slash commands are not available, treat "use /interview mode: <topic>" and "use /coach mode: <topic>" as the corresponding modes.
- Do not add co-author trailers to commits unless the user explicitly asks.
