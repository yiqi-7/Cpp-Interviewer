"""调度器：根据 candidate_score 公式选择下一个复习主题。"""
from typing import Optional

from coach.config import SCHEDULER_WEIGHTS
from coach.models import TrainingContext


class Scheduler:
    """根据候选评分公式选择下一个主题。"""

    def __init__(self, knowledge_index: dict):
        """
        Args:
            knowledge_index: 知识库索引，格式为
                {"topics": [{"topic_id": "...", "interview_frequency": int}, ...]}
        """
        self.index = knowledge_index
        self.recent_question_ids: list[str] = []

    def score_candidate(
        self,
        topic_id: str,
        mastery_level: float,
        next_review_at: Optional[str],  # None or ISO date string
        interview_frequency: int,  # 1-5
        difficulty: int,  # 1-3
        target_difficulty: int,  # 1-3
    ) -> float:
        """
        使用 candidate_score 公式计算候选主题得分。

        公式：
            candidate_score =
                0.40 * weakness_score
              + 0.25 * due_review_score
              + 0.20 * interview_frequency_score
              + 0.10 * difficulty_match_score
              - 0.05 * recent_repetition_penalty
        """
        w = SCHEDULER_WEIGHTS

        weakness_score = 1.0 - mastery_level
        due_review_score = 1.0 if next_review_at else 0.0
        interview_frequency_score = min(interview_frequency / 5.0, 1.0)
        difficulty_match_score = max(0.0, 1.0 - abs(difficulty - target_difficulty) / 3.0)
        repetition_penalty = 0.1 if topic_id in self.recent_question_ids else 0.0

        return (
            w["weakness_score"] * weakness_score
            + w["due_review_score"] * due_review_score
            + w["interview_frequency_score"] * interview_frequency_score
            + w["difficulty_match_score"] * difficulty_match_score
            - w["recent_repetition_penalty"] * repetition_penalty
        )

    def select_next_topic(
        self,
        weak_topics: list[dict],  # [{"topic_id", "topic_name", "mastery_level", "difficulty_level", "next_review_at"}]
        due_topics: list[dict],
        target_difficulty: int = 2,
    ) -> Optional[dict]:
        """
        从弱主题和待复习主题中选择得分最高的主题。

        Args:
            weak_topics: 需要加强的薄弱主题列表
            due_topics: 已到复习时间的待复习主题列表
            target_difficulty: 目标难度等级 (1-3)

        Returns:
            得分最高的主题字典；若候选列表为空则返回 None
        """
        # 构建候选列表，并从 knowledge_index 中查询 interview_frequency
        topic_map = {t["topic_id"]: t for t in self.index.get("topics", [])}
        candidates: list[dict] = []

        for topic in weak_topics:
            topic_id = topic["topic_id"]
            freq_info = topic_map.get(topic_id, {})
            interview_frequency = freq_info.get("interview_frequency", 3)
            score = self.score_candidate(
                topic_id=topic_id,
                mastery_level=topic["mastery_level"],
                next_review_at=topic.get("next_review_at"),
                interview_frequency=interview_frequency,
                difficulty=topic["difficulty_level"],
                target_difficulty=target_difficulty,
            )
            candidates.append({"score": score, **topic})

        for topic in due_topics:
            topic_id = topic["topic_id"]
            freq_info = topic_map.get(topic_id, {})
            interview_frequency = freq_info.get("interview_frequency", 3)
            score = self.score_candidate(
                topic_id=topic_id,
                mastery_level=topic["mastery_level"],
                next_review_at=topic.get("next_review_at"),
                interview_frequency=interview_frequency,
                difficulty=topic["difficulty_level"],
                target_difficulty=target_difficulty,
            )
            candidates.append({"score": score, **topic})

        if not candidates:
            return None

        chosen = max(candidates, key=lambda x: x["score"])
        chosen_topic_id = chosen["topic_id"]

        # 维护最近问题列表，最多保留 10 条
        if chosen_topic_id in self.recent_question_ids:
            self.recent_question_ids.remove(chosen_topic_id)
        self.recent_question_ids.append(chosen_topic_id)
        if len(self.recent_question_ids) > 10:
            self.recent_question_ids = self.recent_question_ids[-10:]

        # 返回时去掉内部 score 字段
        return {
            "topic_id": chosen["topic_id"],
            "topic_name": chosen["topic_name"],
            "mastery_level": chosen["mastery_level"],
            "difficulty_level": chosen["difficulty_level"],
            "next_review_at": chosen.get("next_review_at"),
        }