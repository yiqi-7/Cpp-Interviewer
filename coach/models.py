"""数据结构定义。"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EvaluationResult:
    """结构化评价结果，对应 evaluation_detail 表。"""
    rating: str  # "good" | "okay" | "poor"
    score_total: float  # Overall score, e.g., weighted average of dimensions
    correctness: float
    completeness: float
    depth: float
    clarity: float
    code_accuracy: float
    edge_case_awareness: float
    missing_points: list[str] = field(default_factory=list)
    wrong_points: list[str] = field(default_factory=list)
    weakness_tags: list[str] = field(default_factory=list)
    hallucinated_points: list[str] = field(default_factory=list)
    evaluator_confidence: float = 1.0


@dataclass
class TrainingContext:
    """训练上下文，由 Scheduler 传给 SkillPromptAdapter。"""
    topic_id: str
    topic_name: str
    difficulty: int  # 1-3
    weakness_tags: list[str] = field(default_factory=list)
    user_mastery_level: float = 0.0
    session_id: int = 0


@dataclass
class QARecord:
    """问答记录，对应 qa_history 表。"""
    topic_id: str
    question: str
    user_answer: str
    reference_answer: Optional[str] = None
    evaluation: Optional[EvaluationResult] = None


@dataclass
class KnowledgeRecord:
    """知识点掌握度记录，对应 knowledge_record 表。"""
    topic_id: str
    topic_name: str
    domain: str
    status: str = "unvisited"
    mastery_level: float = 0.0
    right_count: int = 0
    wrong_count: int = 0
    consecutive_right: int = 0
    consecutive_wrong: int = 0
    difficulty_level: int = 1
    ease_factor: float = 2.5
    next_review_at: Optional[str] = None
