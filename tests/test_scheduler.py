"""调度器测试。"""
import pytest
from coach.scheduler import Scheduler


def test_weak_topic_high_score():
    """薄弱主题（mastery=0.1）得分应高于熟练主题（mastery=0.8）。"""
    scheduler = Scheduler(
        {"topics": [{"topic_id": "virtual_function", "interview_frequency": 5}]}
    )
    score_weak = scheduler.score_candidate(
        "virtual_function",
        mastery_level=0.1,
        next_review_at=None,
        interview_frequency=5,
        difficulty=1,
        target_difficulty=2,
    )
    score_strong = scheduler.score_candidate(
        "virtual_function",
        mastery_level=0.8,
        next_review_at=None,
        interview_frequency=5,
        difficulty=1,
        target_difficulty=2,
    )
    assert score_weak > score_strong


def test_due_topic_boosts_score():
    """有 next_review_at 时 due_review_score = 1.0，得分应更高。"""
    scheduler = Scheduler({"topics": []})
    with_due = scheduler.score_candidate(
        "topic",
        mastery_level=0.5,
        next_review_at="2026-01-01T00:00:00+00:00",
        interview_frequency=3,
        difficulty=2,
        target_difficulty=2,
    )
    without_due = scheduler.score_candidate(
        "topic",
        mastery_level=0.5,
        next_review_at=None,
        interview_frequency=3,
        difficulty=2,
        target_difficulty=2,
    )
    assert with_due > without_due


def test_frequency_mapping():
    """interview_frequency=5 映射到 1.0，frequency=1 映射到 0.2。"""
    scheduler = Scheduler({"topics": []})
    score_high = scheduler.score_candidate(
        "t", 0.5, None, 5, 2, 2
    )
    score_low = scheduler.score_candidate(
        "t", 0.5, None, 1, 2, 2
    )
    assert score_high > score_low


def test_difficulty_match_score():
    """难度完全匹配时 difficulty_match_score = 1.0，偏离时相应降低。"""
    scheduler = Scheduler({"topics": []})
    # difficulty=2, target=2 → exact match, score = 1.0
    exact = scheduler.score_candidate(
        "t", 0.5, None, 3, 2, 2
    )
    # difficulty=1, target=3 → |1-3|/3 = 0.67 → 1-0.67 = 0.33
    off = scheduler.score_candidate(
        "t", 0.5, None, 3, 1, 3
    )
    assert exact > off


def test_recent_repetition_penalty():
    """recent_question_ids 中的 topic_id 受到重复惩罚。"""
    scheduler = Scheduler({"topics": []})
    scheduler.recent_question_ids.append("topic")
    with_penalty = scheduler.score_candidate(
        "topic",
        mastery_level=0.2,
        next_review_at=None,
        interview_frequency=5,
        difficulty=2,
        target_difficulty=2,
    )
    scheduler.recent_question_ids.clear()
    without_penalty = scheduler.score_candidate(
        "topic",
        mastery_level=0.2,
        next_review_at=None,
        interview_frequency=5,
        difficulty=2,
        target_difficulty=2,
    )
    assert with_penalty < without_penalty


def test_select_next_topic_prefers_weaker():
    """select_next_topic 返回得分最高的主题。"""
    scheduler = Scheduler(
        {
            "topics": [
                {"topic_id": "vf", "interview_frequency": 5},
                {"topic_id": "sp", "interview_frequency": 3},
            ]
        }
    )
    weak = [
        {"topic_id": "vf", "topic_name": "Virtual Function", "mastery_level": 0.1, "difficulty_level": 1},
        {"topic_id": "sp", "topic_name": "Smart Pointer", "mastery_level": 0.5, "difficulty_level": 1},
    ]
    chosen = scheduler.select_next_topic(weak, [], target_difficulty=2)
    assert chosen is not None
    assert chosen["topic_id"] == "vf"


def test_select_next_topic_with_due_and_weak():
    """due_topics 和 weak_topics 同时存在时，选择得分更高的。"""
    scheduler = Scheduler(
        {
            "topics": [
                {"topic_id": "vf", "interview_frequency": 5},
                {"topic_id": "sp", "interview_frequency": 3},
            ]
        }
    )
    weak = [
        {"topic_id": "sp", "topic_name": "Smart Pointer", "mastery_level": 0.5, "difficulty_level": 2},
    ]
    due = [
        {
            "topic_id": "vf",
            "topic_name": "Virtual Function",
            "mastery_level": 0.1,
            "difficulty_level": 2,
            "next_review_at": "2026-01-01T00:00:00+00:00",
        },
    ]
    chosen = scheduler.select_next_topic(weak, due, target_difficulty=2)
    assert chosen is not None
    # vf 有 due_review boost + low mastery，应该被选中
    assert chosen["topic_id"] == "vf"


def test_select_next_topic_empty_returns_none():
    """当候选列表为空时返回 None。"""
    scheduler = Scheduler({"topics": []})
    result = scheduler.select_next_topic([], [], target_difficulty=2)
    assert result is None


def test_select_next_topic_adds_to_recent():
    """选择的主题应被加入 recent_question_ids。"""
    scheduler = Scheduler(
        {"topics": [{"topic_id": "vf", "interview_frequency": 5}]}
    )
    weak = [
        {"topic_id": "vf", "topic_name": "Virtual Function", "mastery_level": 0.1, "difficulty_level": 1},
    ]
    scheduler.select_next_topic(weak, [], target_difficulty=2)
    assert "vf" in scheduler.recent_question_ids


def test_select_next_topic_respects_max_recent():
    """recent_question_ids 最多保留 10 条。"""
    scheduler = Scheduler(
        {"topics": [{"topic_id": f"t{i}", "interview_frequency": 3} for i in range(15)]}
    )
    for i in range(15):
        scheduler.select_next_topic(
            [{"topic_id": f"t{i}", "topic_name": f"Topic {i}", "mastery_level": 0.1, "difficulty_level": 1}],
            [],
            target_difficulty=2,
        )
    assert len(scheduler.recent_question_ids) == 10