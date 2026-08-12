"""默认参数和 Schema 常量。"""
import os
from pathlib import Path


# === 调度器权重 ===
SCHEDULER_WEIGHTS = {
    "weakness_score": 0.40,
    "due_review_score": 0.25,
    "interview_frequency_score": 0.20,
    "difficulty_match_score": 0.10,
    "recent_repetition_penalty": 0.05,
}

# === 及格线 ===
MASTERY_PASS_THRESHOLD = 0.6

# === 掌握度更新系数 ===
MASTERY_DELTA_FACTOR = 0.12
LOW_CONFIDENCE_PENALTY = 0.5

# === 面试频率映射 ===
FREQUENCY_MAP = {
    "very_high": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "very_low": 1,
}


def _user_data_dir() -> Path:
    """Return the agent-neutral user data directory."""
    env = os.environ.get("CPP_INTERVIEWER_HOME")
    if env:
        return Path(env)
    return Path.home() / ".cpp-interviewer"


def _default_db_path() -> str:
    """Resolve the SQLite DB path using portable environment variables first."""
    env = os.environ.get("CPP_INTERVIEWER_DB") or os.environ.get("COACH_DB_PATH")
    if env:
        return env
    return str(_user_data_dir() / "coach.sqlite")


def _default_index_path() -> str:
    """Resolve knowledge_index.json without assuming a specific agent."""
    env = os.environ.get("CPP_INTERVIEWER_INDEX") or os.environ.get("COACH_INDEX_PATH")
    if env:
        return env

    repo_root = Path(__file__).resolve().parent.parent
    candidates = [
        repo_root / "index" / "knowledge_index.json",
        repo_root / "skills" / "cpp-interviewer" / "index" / "knowledge_index.json",
    ]

    for agent_dir in (".codex", ".claude", ".cursor"):
        candidates.extend(
            [
                Path.home() / agent_dir / "skills" / "cpp-interviewer" / "index" / "knowledge_index.json",
                Path.home() / agent_dir / "skills" / "coach" / "index" / "knowledge_index.json",
            ]
        )

    for path in candidates:
        if path.exists():
            return str(path)
    return str(repo_root / "index" / "knowledge_index.json")


DEFAULT_DB_PATH = _default_db_path()
KNOWLEDGE_INDEX_FILE = _default_index_path()
