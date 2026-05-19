"""调度器：根据 candidate_score 公式选择下一个复习主题。"""
from datetime import datetime, timezone
from typing import Optional

from .config import SCHEDULER_WEIGHTS, FREQUENCY_MAP
from .models import TrainingContext


def flatten_knowledge_index(raw_index: dict) -> dict:
    """将 domains 结构展平为 topics 列表。

    支持两种格式：
    1. {"domains": [{"topics": [...]}]} — 原始 knowledge_index.json
    2. {"topics": [...]} — 已展平
    """
    if "topics" in raw_index:
        return raw_index
    topics = []
    for domain in raw_index.get("domains", []):
        for topic in domain.get("topics", []):
            topic_copy = dict(topic)
            topic_copy.setdefault("domain", domain.get("name", ""))
            topics.append(topic_copy)
    return {"topics": topics}


def frequency_to_int(freq) -> int:
    """将面试频率字符串/整数统一转为 1-5 整数。"""
    if isinstance(freq, int):
        return max(1, min(5, freq))
    return FREQUENCY_MAP.get(str(freq).lower(), 3)


class Scheduler:
    """根据候选评分公式选择下一个主题。"""

    def __init__(self, knowledge_index: dict):
        self.index = flatten_knowledge_index(knowledge_index)
        self.recent_question_ids: list[str] = []

    def _is_due(self, next_review_at: Optional[str]) -> bool:
        if not next_review_at:
            return False
        try:
            due_time = datetime.fromisoformat(next_review_at.replace('Z', '+00:00'))
            return due_time <= datetime.now(timezone.utc)
        except (ValueError, TypeError):
            return False

    def score_candidate(
        self,
        topic_id: str,
        mastery_level: float,
        next_review_at: Optional[str],
        interview_frequency,
        difficulty: int,
        target_difficulty: int,
    ) -> float:
        w = SCHEDULER_WEIGHTS
        freq_int = frequency_to_int(interview_frequency)

        weakness_score = 1.0 - mastery_level
        due_review_score = 1.0 if self._is_due(next_review_at) else 0.0
        interview_frequency_score = min(freq_int / 5.0, 1.0)
        difficulty_match_score = max(0.0, 1.0 - abs(difficulty - target_difficulty) / 3.0)
        repetition_penalty = 0.1 if topic_id in self.recent_question_ids else 0.0

        return (
            w["weakness_score"] * weakness_score
            + w["due_review_score"] * due_review_score
            + w["interview_frequency_score"] * interview_frequency_score
            + w["difficulty_match_score"] * difficulty_match_score
            - w["recent_repetition_penalty"] * repetition_penalty
        )

    def get_topic_frequency(self, topic_id: str) -> int:
        """从索引中查询 topic 的面试频率。"""
        for t in self.index.get("topics", []):
            if t.get("id") == topic_id or t.get("topic_id") == topic_id:
                return frequency_to_int(t.get("interview_frequency", 3))
        return 3

    def select_next_topic(
        self,
        weak_topics: list[dict],
        due_topics: list[dict],
        target_difficulty: int = 2,
    ) -> Optional[dict]:
        topic_map = {}
        for t in self.index.get("topics", []):
            tid = t.get("id") or t.get("topic_id", "")
            topic_map[tid] = t

        candidates: list[dict] = []

        for topic in weak_topics + due_topics:
            topic_id = topic["topic_id"]
            freq_info = topic_map.get(topic_id, {})
            interview_frequency = frequency_to_int(freq_info.get("interview_frequency", 3))
            score = self.score_candidate(
                topic_id=topic_id,
                mastery_level=topic["mastery_level"],
                next_review_at=topic.get("next_review_at"),
                interview_frequency=interview_frequency,
                difficulty=topic.get("difficulty_level", 2),
                target_difficulty=target_difficulty,
            )
            candidates.append({"score": score, **topic})

        if not candidates:
            return None

        chosen = max(candidates, key=lambda x: x["score"])
        chosen_topic_id = chosen["topic_id"]

        if chosen_topic_id in self.recent_question_ids:
            self.recent_question_ids.remove(chosen_topic_id)
        self.recent_question_ids.append(chosen_topic_id)
        if len(self.recent_question_ids) > 10:
            self.recent_question_ids = self.recent_question_ids[-10:]

        return {
            "topic_id": chosen["topic_id"],
            "topic_name": chosen.get("topic_name", chosen["topic_id"]),
            "mastery_level": chosen["mastery_level"],
            "difficulty_level": chosen.get("difficulty_level", 2),
            "next_review_at": chosen.get("next_review_at"),
        }
