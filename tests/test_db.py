"""Tests for coach.db SQLite state layer."""
import json
import os
import tempfile

import pytest

from coach.config import MASTERY_DELTA_FACTOR, MASTERY_PASS_THRESHOLD, LOW_CONFIDENCE_PENALTY
from coach.db import CoachDB, get_connection, init_db
from coach.models import EvaluationResult


@pytest.fixture
def temp_db():
    """创建临时数据库，初始化后返回 CoachDB 实例，最后清理。"""
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db = CoachDB(path)
    yield db
    os.unlink(path)


class TestEnsureUser:
    def test_creates_new_user(self, temp_db):
        """创建新用户，验证 total=0。"""
        temp_db.ensure_user("user1")
        summary = temp_db.get_status_summary("user1")
        assert summary["total"] == 0
        assert summary["mastered"] == 0
        assert summary["weak"] == 0
        assert summary["avg_mastery"] == 0.0

    def test_ensure_user_idempotent(self, temp_db):
        """重复 ensure_user 不会报错。"""
        temp_db.ensure_user("user1")
        temp_db.ensure_user("user1")
        summary = temp_db.get_status_summary("user1")
        assert summary["total"] == 0


class TestUpdateMastery:
    def test_update_mastery_weak_to_learning(self, temp_db):
        """从 weak 状态更新 mastery，检查 weak_topics 变化。"""
        user_id = "user1"
        topic_id = "cpp/virtual"
        topic_name = "虚函数"
        domain = "C++"

        temp_db.ensure_user(user_id)

        # 初始状态：weak topics 应该为空（因为还没有记录）
        weak_before = temp_db.get_weak_topics(user_id)
        assert len(weak_before) == 0

        # 第一次更新：score=0.5（不 及格），mastery 应该下降
        temp_db.update_knowledge_mastery(
            user_id, topic_id, topic_name, domain,
            score_total=0.5, evaluator_confidence=1.0,
        )

        # 再次检查 weak topics
        weak = temp_db.get_weak_topics(user_id)
        assert len(weak) == 1
        assert weak[0]["topic_id"] == topic_id
        assert weak[0]["status"] == "weak"

        # 第二次更新：score=0.8（及格），mastery 应该上升
        temp_db.update_knowledge_mastery(
            user_id, topic_id, topic_name, domain,
            score_total=0.8, evaluator_confidence=1.0,
        )

        # update_knowledge_mastery 不创建 qa_history，所以 total 仍为 0
        # 但 knowledge_record 中应该有 1 条记录
        summary = temp_db.get_status_summary(user_id)
        assert summary["total"] == 0  # total 来自 qa_history
        assert summary["weak"] == 1  # weak 来自 knowledge_record

    def test_low_confidence_penalty(self, temp_db):
        """低置信度评估应该惩罚 delta。"""
        user_id = "user1"
        topic_id = "cpp/pointer"
        topic_name = "指针"
        domain = "C++"

        temp_db.ensure_user(user_id)

        # 高置信度更新
        temp_db.update_knowledge_mastery(
            user_id, topic_id, topic_name, domain,
            score_total=0.9, evaluator_confidence=1.0,
        )
        row_high = temp_db.get_weak_topics(user_id)
        mastery_high = row_high[0]["mastery_level"] if row_high else 0.0

        # 低置信度更新（惩罚 50%）
        temp_db.update_knowledge_mastery(
            user_id, "cpp/ref", "引用", domain,
            score_total=0.9, evaluator_confidence=0.5,
        )
        row_low = temp_db.get_weak_topics(user_id)
        mastery_low = row_low[0]["mastery_level"] if row_low else 0.0

        # 低置信度的 delta 被惩罚，所以 mastery 应该更低
        assert mastery_low < mastery_high


class TestSaveQA:
    def test_save_qa_and_eval(self, temp_db):
        """保存 QA 记录及其 EvaluationResult。"""
        user_id = "user1"
        temp_db.ensure_user(user_id)

        evaluation = EvaluationResult(
            rating="good",
            score_total=0.85,
            correctness=0.9,
            completeness=0.8,
            depth=0.85,
            clarity=0.9,
            code_accuracy=0.8,
            edge_case_awareness=0.8,
            missing_points=["边界条件"],
            wrong_points=["语法错误"],
            weakness_tags=["指针", "内存管理"],
            evaluator_confidence=0.95,
        )

        qa_id = temp_db.save_qa(
            user_id=user_id,
            session_id=None,
            topic_id="cpp/new",
            question="什么是 new？",
            user_answer="分配内存",
            reference_answer="new 是 C++ 的动态内存分配运算符",
            evaluation=evaluation,
        )

        assert qa_id > 0

        # 验证 user_state 计数
        summary = temp_db.get_status_summary(user_id)
        assert summary["total"] == 1

        # 验证 qa_history 中的 weakness_tags 被正确保存
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT weakness_tags FROM qa_history WHERE qa_id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        tags = json.loads(row["weakness_tags"])
        assert "指针" in tags
        assert "内存管理" in tags

    def test_save_qa_without_eval(self, temp_db):
        """保存 QA 记录时不带 evaluation。"""
        user_id = "user1"
        temp_db.ensure_user(user_id)

        qa_id = temp_db.save_qa(
            user_id=user_id,
            session_id=None,
            topic_id="cpp/class",
            question="什么是类？",
            user_answer="用户自定义类型",
            reference_answer=None,
            evaluation=None,
        )

        assert qa_id > 0


class TestSession:
    def test_start_end_session(self, temp_db):
        """开始和结束训练会话。"""
        user_id = "user1"
        temp_db.ensure_user(user_id)

        session_id = temp_db.start_session(user_id, topic_id="cpp/virtual")
        assert session_id > 0

        summary = temp_db.get_status_summary(user_id)
        assert summary["total"] == 0  # session 不算在 knowledge_record 里

        temp_db.end_session(session_id)

        # 验证 session 状态
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status, ended_at FROM training_session WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        conn.close()

        assert row["status"] == "completed"
        assert row["ended_at"] is not None

    def test_multiple_sessions(self, temp_db):
        """一个用户可以有多个会话。"""
        user_id = "user1"
        temp_db.ensure_user(user_id)

        s1 = temp_db.start_session(user_id)
        s2 = temp_db.start_session(user_id)
        assert s1 != s2

        summary = temp_db.get_status_summary(user_id)
        assert summary["total"] == 0


class TestQueryMethods:
    def test_get_due_topics_empty(self, temp_db):
        """新用户没有 due topics。"""
        temp_db.ensure_user("user1")
        due = temp_db.get_due_topics("user1")
        assert due == []

    def test_get_weak_topics_empty(self, temp_db):
        """新用户没有 weak topics。"""
        temp_db.ensure_user("user1")
        weak = temp_db.get_weak_topics("user1")
        assert weak == []

    def test_get_status_summary_empty_user(self, temp_db):
        """不存在的用户返回零值。"""
        summary = temp_db.get_status_summary("nonexistent")
        assert summary["total"] == 0
        assert summary["mastered"] == 0
        assert summary["weak"] == 0
        assert summary["avg_mastery"] == 0.0
