"""Tests for coach.db SQLite state layer."""
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone

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

        # 验证 qa_history 中的 final_rating 和 score_total 被正确保存
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT final_rating, score_total, weakness_summary FROM qa_history WHERE id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        assert row["final_rating"] == "good"
        assert row["score_total"] == 0.85

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

        session_id = temp_db.start_session(user_id, mode="topic", target_domain="C++")
        assert session_id > 0

        summary = temp_db.get_status_summary(user_id)
        assert summary["total"] == 0  # session 不算在 knowledge_record 里

        temp_db.end_session(session_id, total_questions=5, average_score=0.85, summary="Good work")

        # 验证 session 状态
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT mode, target_domain, total_questions, average_score, summary, end_time FROM training_session WHERE id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        conn.close()

        assert row["mode"] == "topic"
        assert row["target_domain"] == "C++"
        assert row["total_questions"] == 5
        assert row["average_score"] == 0.85
        assert row["summary"] == "Good work"
        assert row["end_time"] is not None

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


class TestSchemaValidation:
    """Phase 1.5: Schema validation tests to verify design doc alignment."""

    def test_user_state_has_required_fields(self, temp_db):
        """user_state 表必须有 current_mode, default_style, default_depth, last_topic, last_session_id"""
        temp_db.ensure_user("test_user")
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(user_state)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        required = {"current_mode", "default_style", "default_depth", "last_topic", "last_session_id"}
        assert required.issubset(columns), f"Missing columns: {required - columns}"
        # Check defaults
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_state WHERE user_id = ?", ("test_user",))
        row = cursor.fetchone()
        conn.close()
        assert row["current_mode"] == "coach"
        assert row["default_style"] == "concise"
        assert row["default_depth"] == 1

    def test_qa_history_has_required_fields(self, temp_db):
        """qa_history 表必须有 question_id, final_rating, score_total, weakness_summary"""
        temp_db.ensure_user("test_user")
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(qa_history)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        required = {"question_id", "final_rating", "score_total", "weakness_summary"}
        assert required.issubset(columns), f"Missing columns: {required - columns}"

    def test_evaluation_detail_has_hallucinated_points(self, temp_db):
        """evaluation_detail 表必须有 hallucinated_points 字段"""
        temp_db.ensure_user("test_user")
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(evaluation_detail)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        assert "hallucinated_points" in columns

    def test_training_session_has_required_fields(self, temp_db):
        """training_session 表必须有 mode, target_domain, average_score, summary"""
        temp_db.ensure_user("test_user")
        session_id = temp_db.start_session("test_user", mode="topic", target_domain="C++")
        temp_db.end_session(session_id, total_questions=5, average_score=0.85, summary="Good session")

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(training_session)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        required = {"mode", "target_domain", "average_score", "summary"}
        assert required.issubset(columns), f"Missing columns: {required - columns}"

        # Verify the session data
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM training_session WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        assert row["mode"] == "topic"
        assert row["target_domain"] == "C++"
        assert row["total_questions"] == 5
        assert row["average_score"] == 0.85
        assert row["summary"] == "Good session"

    def test_question_bank_has_required_fields(self, temp_db):
        """question_bank 表必须有 key_points, followups, skill_version, created_from_context"""
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(question_bank)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        required = {"key_points", "followups", "skill_version", "created_from_context"}
        assert required.issubset(columns), f"Missing columns: {required - columns}"

    def test_question_bank_difficulty_column_named_difficulty(self, temp_db):
        """question_bank 的难度列应命名为 difficulty 而非 difficulty_level"""
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(question_bank)")
        columns = {row["name"] for row in cursor.fetchall()}
        conn.close()

        assert "difficulty" in columns
        assert "difficulty_level" not in columns


class TestJSONRoundTrip:
    """Test that JSON fields are stored and retrieved correctly."""

    def test_weakness_tags_json_roundtrip(self, temp_db):
        """weakness_tags 在 evaluation_detail 中正确序列化和反序列化"""
        temp_db.ensure_user("test_user")
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
            weakness_tags=["vtable", "vptr", "dynamic_dispatch"],
            hallucinated_points=[],
            evaluator_confidence=0.95,
        )

        qa_id = temp_db.save_qa(
            user_id="test_user",
            session_id=None,
            topic_id="cpp/virtual",
            question="什么是虚函数？",
            user_answer="虚函数是可以在子类中重写的函数",
            reference_answer="虚函数是 C++ 多态的基础",
            evaluation=evaluation,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT weakness_tags FROM evaluation_detail WHERE qa_id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        tags = json.loads(row["weakness_tags"])
        assert tags == ["vtable", "vptr", "dynamic_dispatch"]

    def test_missing_points_json_roundtrip(self, temp_db):
        """missing_points 正确序列化和反序列化"""
        temp_db.ensure_user("test_user")
        evaluation = EvaluationResult(
            rating="okay",
            score_total=0.7,
            correctness=0.7,
            completeness=0.6,
            depth=0.7,
            clarity=0.8,
            code_accuracy=0.7,
            edge_case_awareness=0.6,
            missing_points=["内存泄漏", "智能指针"],
            wrong_points=[],
            weakness_tags=["内存管理"],
            hallucinated_points=[],
            evaluator_confidence=0.9,
        )

        qa_id = temp_db.save_qa(
            user_id="test_user",
            session_id=None,
            topic_id="cpp/smart_ptr",
            question="什么是智能指针？",
            user_answer="智能指针是自动管理内存的指针",
            reference_answer="智能指针是 C++11 引入的自动内存管理工具",
            evaluation=evaluation,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT missing_points FROM evaluation_detail WHERE qa_id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        missing = json.loads(row["missing_points"])
        assert missing == ["内存泄漏", "智能指针"]

    def test_wrong_points_json_roundtrip(self, temp_db):
        """wrong_points 正确序列化和反序列化"""
        temp_db.ensure_user("test_user")
        evaluation = EvaluationResult(
            rating="poor",
            score_total=0.4,
            correctness=0.5,
            completeness=0.4,
            depth=0.4,
            clarity=0.6,
            code_accuracy=0.5,
            edge_case_awareness=0.4,
            missing_points=["未提及移动语义"],
            wrong_points=["认为引用是对象", "混淆指针和引用"],
            weakness_tags=["引用", "指针"],
            hallucinated_points=["声称引用占用额外内存"],
            evaluator_confidence=0.85,
        )

        qa_id = temp_db.save_qa(
            user_id="test_user",
            session_id=None,
            topic_id="cpp/reference",
            question="什么是引用？",
            user_answer="引用是一个别名",
            reference_answer="引用是对象的别名",
            evaluation=evaluation,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT wrong_points FROM evaluation_detail WHERE qa_id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        wrong = json.loads(row["wrong_points"])
        assert wrong == ["认为引用是对象", "混淆指针和引用"]

    def test_hallucinated_points_json_roundtrip(self, temp_db):
        """hallucinated_points 正确序列化和反序列化"""
        temp_db.ensure_user("test_user")
        evaluation = EvaluationResult(
            rating="poor",
            score_total=0.35,
            correctness=0.4,
            completeness=0.3,
            depth=0.3,
            clarity=0.5,
            code_accuracy=0.4,
            edge_case_awareness=0.3,
            missing_points=["未提及虚析构函数"],
            wrong_points=["错误理解了多态机制"],
            weakness_tags=["多态", "虚函数"],
            hallucinated_points=["声称虚函数表在栈上", "声称 vptr 在编译时确定"],
            evaluator_confidence=0.8,
        )

        qa_id = temp_db.save_qa(
            user_id="test_user",
            session_id=None,
            topic_id="cpp/polymorphism",
            question="解释 C++ 多态",
            user_answer="多态是多种形式",
            reference_answer="多态是同一接口不同实现",
            evaluation=evaluation,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hallucinated_points FROM evaluation_detail WHERE qa_id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        hallucinated = json.loads(row["hallucinated_points"])
        assert hallucinated == ["声称虚函数表在栈上", "声称 vptr 在编译时确定"]


class TestDueTopicQuery:
    """Test get_due_topics with expired next_review_at."""

    def test_get_due_topics_with_expired_review(self, temp_db):
        """验证 get_due_topics 能正确返回已过期的复习项"""
        temp_db.ensure_user("test_user")

        # 手动插入一个已过期的 knowledge_record
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        expired_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        cursor.execute(
            """
            INSERT INTO knowledge_record
                (user_id, topic_id, topic_name, domain, mastery_level, status, next_review_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("test_user", "cpp/expired", "过期知识点", "C++", 0.5, "learning", expired_time),
        )
        conn.commit()
        conn.close()

        due = temp_db.get_due_topics("test_user")
        assert len(due) == 1
        assert due[0]["topic_id"] == "cpp/expired"

    def test_get_due_topics_uses_isoformat(self, temp_db):
        """验证 next_review_at 比较使用 isoformat"""
        temp_db.ensure_user("test_user")

        # 插入一个当前时间-1秒的记录（刚刚过期）
        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        just_expired = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        cursor.execute(
            """
            INSERT INTO knowledge_record
                (user_id, topic_id, topic_name, domain, mastery_level, status, next_review_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("test_user", "cpp/just_expired", "刚过期知识点", "C++", 0.5, "learning", just_expired),
        )
        conn.commit()
        conn.close()

        due = temp_db.get_due_topics("test_user")
        assert len(due) == 1
        assert due[0]["topic_id"] == "cpp/just_expired"

    def test_knowledge_record_on_conflict_preserves_fields(self, temp_db):
        """验证 ON CONFLICT 更新不会重置原有字段"""
        temp_db.ensure_user("test_user")
        topic_id = "cpp/test_topic"
        topic_name = "测试主题"
        domain = "C++"

        # 第一次插入
        temp_db.update_knowledge_mastery(
            "test_user", topic_id, topic_name, domain,
            score_total=0.5, evaluator_confidence=1.0,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT mastery_level, right_count, wrong_count FROM knowledge_record WHERE user_id = ? AND topic_id = ?",
            ("test_user", topic_id),
        )
        row = cursor.fetchone()
        first_mastery = row["mastery_level"]
        first_right = row["right_count"]
        first_wrong = row["wrong_count"]
        conn.close()

        # 第二次更新（不改变 topic_name 等字段）
        temp_db.update_knowledge_mastery(
            "test_user", topic_id, topic_name, domain,
            score_total=0.8, evaluator_confidence=1.0,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT mastery_level, right_count, wrong_count, topic_name, domain FROM knowledge_record WHERE user_id = ? AND topic_id = ?",
            ("test_user", topic_id),
        )
        row = cursor.fetchone()
        conn.close()

        # topic_name 和 domain 应该保持不变
        assert row["topic_name"] == topic_name
        assert row["domain"] == domain
        # mastery 应该更新
        assert row["mastery_level"] > first_mastery


class TestQARecordFieldPopulation:
    """Test that qa_history final_rating, score_total, weakness_summary are populated."""

    def test_qa_history_final_rating_populated(self, temp_db):
        """qa_history 的 final_rating 字段被正确填充"""
        temp_db.ensure_user("test_user")
        evaluation = EvaluationResult(
            rating="good",
            score_total=0.85,
            correctness=0.9,
            completeness=0.8,
            depth=0.85,
            clarity=0.9,
            code_accuracy=0.8,
            edge_case_awareness=0.8,
            missing_points=[],
            wrong_points=[],
            weakness_tags=["vtable"],
            hallucinated_points=[],
            evaluator_confidence=0.95,
        )

        qa_id = temp_db.save_qa(
            user_id="test_user",
            session_id=None,
            topic_id="cpp/virtual",
            question="什么是虚函数？",
            user_answer="虚函数是可以在子类中重写的函数",
            reference_answer="虚函数是 C++ 多态的基础",
            evaluation=evaluation,
        )

        conn = get_connection(temp_db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT final_rating, score_total FROM qa_history WHERE id = ?",
            (qa_id,),
        )
        row = cursor.fetchone()
        conn.close()

        assert row["final_rating"] == "good"
        assert row["score_total"] == evaluation.score_total
