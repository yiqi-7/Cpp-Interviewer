"""SQLite 状态层 - 持久化教练代理的所有状态。"""
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from .config import (
    DEFAULT_DB_PATH,
    LOW_CONFIDENCE_PENALTY,
    MASTERY_DELTA_FACTOR,
    MASTERY_PASS_THRESHOLD,
)
from .models import EvaluationResult, QARecord


def get_connection(db_path: str) -> sqlite3.Connection:
    """创建 SQLite 连接，启用 row factory 和外键约束。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str) -> None:
    """初始化数据库 schema：6 张表 + 5 个索引。"""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. user_state
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
            user_id TEXT PRIMARY KEY,
            total_questions INTEGER DEFAULT 0,
            total_sessions INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now', 'utc')),
            updated_at TEXT DEFAULT (datetime('now', 'utc'))
        )
    """)

    # 2. knowledge_record
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_record (
            user_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT DEFAULT 'unvisited',
            mastery_level REAL DEFAULT 0.0,
            right_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            consecutive_right INTEGER DEFAULT 0,
            consecutive_wrong INTEGER DEFAULT 0,
            difficulty_level INTEGER DEFAULT 1,
            ease_factor REAL DEFAULT 2.5,
            next_review_at TEXT,
            created_at TEXT DEFAULT (datetime('now', 'utc')),
            updated_at TEXT DEFAULT (datetime('now', 'utc')),
            PRIMARY KEY (user_id, topic_id)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_user_topic
        ON knowledge_record(user_id, topic_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_review
        ON knowledge_record(user_id, next_review_at)
    """)

    # 3. qa_history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_history (
            qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id INTEGER,
            topic_id TEXT NOT NULL,
            question TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            reference_answer TEXT,
            weakness_tags TEXT DEFAULT '[]',
            created_at TEXT DEFAULT (datetime('now', 'utc'))
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_qa_user_session
        ON qa_history(user_id, session_id)
    """)

    # 4. evaluation_detail
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_detail (
            detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            qa_id INTEGER NOT NULL,
            rating TEXT NOT NULL,
            score_total REAL NOT NULL,
            correctness REAL NOT NULL,
            completeness REAL NOT NULL,
            depth REAL NOT NULL,
            clarity REAL NOT NULL,
            code_accuracy REAL NOT NULL,
            edge_case_awareness REAL NOT NULL,
            missing_points TEXT DEFAULT '[]',
            wrong_points TEXT DEFAULT '[]',
            weakness_tags TEXT DEFAULT '[]',
            evaluator_confidence REAL DEFAULT 1.0,
            created_at TEXT DEFAULT (datetime('now', 'utc')),
            FOREIGN KEY (qa_id) REFERENCES qa_history(qa_id)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_eval_qa
        ON evaluation_detail(qa_id)
    """)

    # 5. training_session
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_session (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            topic_id TEXT,
            started_at TEXT DEFAULT (datetime('now', 'utc')),
            ended_at TEXT,
            status TEXT DEFAULT 'active'
        )
    """)

    # 6. question_bank
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_bank (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL,
            topic_name TEXT NOT NULL,
            question TEXT NOT NULL,
            reference_answer TEXT,
            difficulty_level INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'utc'))
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_question_topic_difficulty
        ON question_bank(topic_id, difficulty_level)
    """)

    conn.commit()
    conn.close()


class CoachDB:
    """教练数据库封装，提供所有 CRUD 操作。"""

    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = db_path
        init_db(db_path)

    def ensure_user(self, user_id: str) -> None:
        """确保用户存在，不存在则创建。"""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO user_state (user_id)
            VALUES (?)
            """,
            (user_id,),
        )
        conn.commit()
        conn.close()

    def update_knowledge_mastery(
        self,
        user_id: str,
        topic_id: str,
        topic_name: str,
        domain: str,
        score_total: float,
        evaluator_confidence: float,
    ) -> None:
        """根据答题结果更新知识点掌握度。"""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # 获取当前记录
        cursor.execute(
            """
            SELECT mastery_level, right_count, wrong_count,
                   consecutive_right, consecutive_wrong
            FROM knowledge_record
            WHERE user_id = ? AND topic_id = ?
            """,
            (user_id, topic_id),
        )
        row = cursor.fetchone()
        old_mastery = row["mastery_level"] if row else 0.0
        old_right = row["right_count"] if row else 0
        old_wrong = row["wrong_count"] if row else 0
        old_consecutive_right = row["consecutive_right"] if row else 0
        old_consecutive_wrong = row["consecutive_wrong"] if row else 0

        # 计算 delta
        delta = MASTERY_DELTA_FACTOR * (score_total - MASTERY_PASS_THRESHOLD)
        if evaluator_confidence < 0.7:
            delta *= LOW_CONFIDENCE_PENALTY
        new_mastery = max(0.0, min(1.0, old_mastery + delta))

        # 计算新状态
        if new_mastery >= 0.8:
            new_status = "mastered"
        elif new_mastery >= 0.4:
            new_status = "learning"
        else:
            new_status = "weak"

        # 计算新的计数
        if score_total >= MASTERY_PASS_THRESHOLD:
            new_right = old_right + 1
            new_wrong = old_wrong
            new_consecutive_right = old_consecutive_right + 1
            new_consecutive_wrong = 0
        else:
            new_right = old_right
            new_wrong = old_wrong + 1
            new_consecutive_right = 0
            new_consecutive_wrong = old_consecutive_wrong + 1

        # 计算下次复习时间
        next_review = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT OR REPLACE INTO knowledge_record
                (user_id, topic_id, topic_name, domain, mastery_level, status,
                 right_count, wrong_count, consecutive_right, consecutive_wrong,
                 difficulty_level, ease_factor, next_review_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, topic_id, topic_name, domain, new_mastery, new_status,
                new_right, new_wrong, new_consecutive_right, new_consecutive_wrong,
                1, 2.5, next_review,
            ),
        )
        conn.commit()
        conn.close()

    def save_qa(
        self,
        user_id: str,
        session_id: Optional[int],
        topic_id: str,
        question: str,
        user_answer: str,
        reference_answer: Optional[str],
        evaluation: Optional[EvaluationResult],
    ) -> int:
        """保存问答记录和评价详情，返回 qa_id。"""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        weakness_tags = json.dumps([], ensure_ascii=False)
        cursor.execute(
            """
            INSERT INTO qa_history
                (user_id, session_id, topic_id, question, user_answer,
                 reference_answer, weakness_tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, session_id, topic_id, question, user_answer,
                reference_answer, weakness_tags,
            ),
        )
        qa_id = cursor.lastrowid

        if evaluation:
            cursor.execute(
                """
                INSERT INTO evaluation_detail
                    (qa_id, rating, score_total, correctness, completeness,
                     depth, clarity, code_accuracy, edge_case_awareness,
                     missing_points, wrong_points, weakness_tags,
                     evaluator_confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    qa_id,
                    evaluation.rating,
                    evaluation.score_total,
                    evaluation.correctness,
                    evaluation.completeness,
                    evaluation.depth,
                    evaluation.clarity,
                    evaluation.code_accuracy,
                    evaluation.edge_case_awareness,
                    json.dumps(evaluation.missing_points, ensure_ascii=False),
                    json.dumps(evaluation.wrong_points, ensure_ascii=False),
                    json.dumps(evaluation.weakness_tags, ensure_ascii=False),
                    evaluation.evaluator_confidence,
                ),
            )

            # 更新 weakness_tags 回 qa_history
            if evaluation.weakness_tags:
                cursor.execute(
                    """
                    UPDATE qa_history
                    SET weakness_tags = ?
                    WHERE qa_id = ?
                    """,
                    (json.dumps(evaluation.weakness_tags, ensure_ascii=False), qa_id),
                )

        # 更新 user_state 计数
        cursor.execute(
            """
            UPDATE user_state
            SET total_questions = total_questions + 1,
                updated_at = datetime('now', 'utc')
            WHERE user_id = ?
            """,
            (user_id,),
        )

        conn.commit()
        conn.close()
        return qa_id

    def start_session(
        self, user_id: str, topic_id: Optional[str] = None
    ) -> int:
        """开始一个新的训练会话，返回 session_id。"""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO training_session (user_id, topic_id, status)
            VALUES (?, ?, 'active')
            """,
            (user_id, topic_id),
        )
        session_id = cursor.lastrowid

        cursor.execute(
            """
            UPDATE user_state
            SET total_sessions = total_sessions + 1,
                updated_at = datetime('now', 'utc')
            WHERE user_id = ?
            """,
            (user_id,),
        )

        conn.commit()
        conn.close()
        return session_id

    def end_session(self, session_id: int) -> None:
        """结束指定的训练会话。"""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE training_session
            SET ended_at = datetime('now', 'utc'),
                status = 'completed'
            WHERE session_id = ?
            """,
            (session_id,),
        )
        conn.commit()
        conn.close()

    def get_weak_topics(self, user_id: str, limit: int = 10) -> list[dict[str, Any]]:
        """获取用户掌握度最低的知识点。"""
        conn = get_connection(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT topic_id, topic_name, domain, mastery_level, status
            FROM knowledge_record
            WHERE user_id = ? AND mastery_level < 0.6
            ORDER BY mastery_level ASC, consecutive_wrong DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_due_topics(self, user_id: str) -> list[dict[str, Any]]:
        """获取已到复习时间的知识点。"""
        conn = get_connection(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute(
            """
            SELECT topic_id, topic_name, domain, mastery_level, status,
                   next_review_at
            FROM knowledge_record
            WHERE user_id = ?
              AND next_review_at IS NOT NULL
              AND next_review_at <= ?
            ORDER BY next_review_at ASC
            """,
            (user_id, now),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_status_summary(self, user_id: str) -> dict[str, Any]:
        """获取用户状态摘要。"""
        conn = get_connection(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # total 来自 qa_history，mastered/weak/avg_mastery 来自 knowledge_record
        cursor.execute(
            """
            SELECT COUNT(*) as total
            FROM qa_history
            WHERE user_id = ?
            """,
            (user_id,),
        )
        total_row = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN mastery_level >= 0.8 THEN 1 ELSE 0 END) as mastered,
                SUM(CASE WHEN mastery_level < 0.6 THEN 1 ELSE 0 END) as weak,
                AVG(mastery_level) as avg_mastery
            FROM knowledge_record
            WHERE user_id = ?
            """,
            (user_id,),
        )
        mastery_row = cursor.fetchone()
        conn.close()

        return {
            "total": total_row["total"] or 0,
            "mastered": mastery_row["mastered"] or 0,
            "weak": mastery_row["weak"] or 0,
            "avg_mastery": mastery_row["avg_mastery"] or 0.0,
        }
