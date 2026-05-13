[English](#) | [中文](README.md)

# C++ Interview Coach Agent

Your C++ interview learning companion, supporting two work modes:

## Two Modes

### Mode 1: /interview — Interview Q&A Coaching

Simulates an interviewer role, guiding you through topics with follow-up questions.

```
/interview How are virtual functions implemented
/interview What types of smart pointers are there
/interview What is a memory leak
```

**Features:**
- Interviewer perspective: guides thinking, no direct answers
- Three-level depth expansion (Level 1-3)
- Switchable style (concise/detailed)
- High-frequency follow-ups (3-5 per question, basic to advanced)

### Mode 2: /coach — Weakness-Driven Training

Systematic training mode with precise weakness diagnosis.

```
/coach start     # Enter training loop
/coach topic virtual_function  # Train specific topic
/coach weak      # Train weak topics
/coach status    # View mastery dashboard
/coach plan      # Generate today's training plan
```

**Features:**
- Six-dimension precise diagnosis (correctness, completeness, depth, clarity, code_accuracy, edge_case_awareness)
- Weakness-first scheduling (Scheduler candidate_score formula)
- SQLite state persistence (mastery, QA history, review schedule)
- Implicit evaluation mechanism (non-intrusive, minimal feedback)

## Architecture

```
User CLI → Coach Orchestrator → SkillPromptAdapter → SQLite
                      ↓
              ┌──────────────┐
              │ Scheduler    │  Candidate scoring
              │ Evaluator    │  6-dimension scoring
              │ SkillAdapter │  Knowledge engine
              └──────────────┘
```

## Repository Structure

```
Cpp-Interviewer/
├── coach/                    # Coach Agent (Python CLI)
│   ├── cli.py               # CLI entry
│   ├── db.py                # SQLite state layer (6 tables)
│   ├── scheduler.py         # Topic scheduler
│   ├── evaluator.py         # 6-dimension evaluator
│   └── skill_adapter.py     # Knowledge engine adapter
├── skills/
│   ├── coach/SKILL.md       # /coach command entry
│   └── interview/
│       ├── SKILL.md         # /interview mode
│       ├── COACH_SKILL.md   # Coach passive mode
│       └── shared_rules.md  # Common interview rules
├── index/
│   └── knowledge_index.json # Knowledge index (60+ topics)
├── data/
│   └── coach.sqlite         # State storage (generated at runtime)
└── tests/                    # Unit tests
```

## Quick Start

```bash
# View mastery dashboard
python -m coach.cli status

# Train weak topics
python -m coach.cli weak

# Train specific topic
python -m coach.cli topic virtual_function

# Generate today's plan
python -m coach.cli plan
```

## Installation

### Option 1: Clone Repository

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
# Tell your local CLI to install the skill: https://github.com/yiqi-7/Cpp-Interviewer.git
```

### Option 2: Download

Download and extract the repository, then place the folder under `~/.claude/skills/`.

## Notes

- PDF books are managed with Git LFS. You need [Git LFS](https://git-lfs.github.com/) installed when cloning.
- Interview PDFs are encrypted files. The Skill parses content directly; some formatting may be incomplete.
- `/coach reset` and `/coach export` are not yet implemented.

## License

This project is licensed under the [MIT License](LICENSE).

## Discussion Group

Q:828570482