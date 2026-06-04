"""默认参数和 Schema 常量。"""
import os
from pathlib import Path


# === LLM 配置 ===
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7

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


def _default_db_path() -> str:
    """三层 fallback 确定 DB 路径。"""
    env = os.environ.get("COACH_DB_PATH")
    if env:
        return env
    user_path = Path.home() / ".claude" / "coach" / "data" / "coach.sqlite"
    return str(user_path)


def _default_index_path() -> str:
    """三层 fallback 确定知识索引路径。"""
    env = os.environ.get("COACH_INDEX_PATH")
    if env:
        return env
    # skill 安装目录
    skill_index = Path.home() / ".claude" / "skills" / "coach" / "index" / "knowledge_index.json"
    if skill_index.exists():
        return str(skill_index)
    return "index/knowledge_index.json"


DEFAULT_DB_PATH = _default_db_path()
KNOWLEDGE_INDEX_FILE = _default_index_path()

# === Skill 路径（兼容旧代码） ===
SKILL_DIR = "skills/interview"
COACH_SKILL_FILE = "skills/interview/COACH_SKILL.md"
SHARED_RULES_FILE = "skills/interview/shared_rules.md"
