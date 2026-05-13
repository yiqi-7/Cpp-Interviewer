"""默认参数和 Schema 常量。"""

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

# === 数据库路径 ===
DEFAULT_DB_PATH = "data/coach.sqlite"

# === Skill 路径 ===
SKILL_DIR = "skills/interview"
COACH_SKILL_FILE = "skills/interview/COACH_SKILL.md"
SHARED_RULES_FILE = "skills/interview/shared_rules.md"
KNOWLEDGE_INDEX_FILE = "index/knowledge_index.json"