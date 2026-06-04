"""CLI 入口：python -m coach.cli <command> [args] [--json]"""
import json
import sys
from pathlib import Path

from .config import DEFAULT_DB_PATH, KNOWLEDGE_INDEX_FILE
from .db import CoachDB
from .scheduler import Scheduler
from .models import EvaluationResult


class CoachCLI:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.db = CoachDB(str(self.repo_path / DEFAULT_DB_PATH))
        self.db.ensure_user("default")
        self.scheduler = self._load_scheduler()

    def _load_scheduler(self):
        index_path = self.repo_path / KNOWLEDGE_INDEX_FILE
        if not index_path.exists():
            from .config import _default_index_path
            index_path = Path(_default_index_path())
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return Scheduler(raw)
        return Scheduler({"topics": []})

    def cmd_status(self, json_output=False):
        summary = self.db.get_status_summary("default")
        if json_output:
            _print_json(summary)
        else:
            print(f"总知识点数: {summary['total']}")
            print(f"已掌握: {summary['mastered']}")
            print(f"薄弱: {summary['weak']}")
            print(f"平均掌握度: {summary['avg_mastery']:.1%}")

    def cmd_weak(self, json_output=False):
        weak = self.db.get_weak_topics("default", limit=10)
        if json_output:
            _print_json({"topics": weak})
        else:
            if not weak:
                print("当前没有薄弱知识点记录")
                return
            for t in weak:
                print(f"  {t['topic_name']} — 掌握度 {t['mastery_level']:.1%} ({t['status']})")

    def cmd_due(self, json_output=False):
        due = self.db.get_due_topics("default")
        if json_output:
            _print_json({"topics": due})
        else:
            if not due:
                print("没有到期复习的知识点")
                return
            for t in due:
                print(f"  {t['topic_name']} — 掌握度 {t['mastery_level']:.1%}")

    def cmd_plan(self, json_output=False):
        weak = self.db.get_weak_topics("default", limit=3)
        due = self.db.get_due_topics("default")
        if json_output:
            _print_json({"weak": weak, "due": due[:2]})
        else:
            print("今日训练计划：")
            for i, t in enumerate(weak, 1):
                print(f"  {i}. {t['topic_name']} (薄弱, 掌握度 {t['mastery_level']:.1%})")
            for i, t in enumerate(due[:2], len(weak) + 1):
                print(f"  {i}. {t['topic_name']} (到期复习)")

    def cmd_topic_info(self, topic: str, json_output=False):
        from .db import get_connection
        conn = get_connection(self.db.db_path)
        conn.row_factory = None
        cursor = conn.cursor()
        cursor.execute(
            "SELECT topic_id, topic_name, mastery_level, status, "
            "right_count, wrong_count, difficulty_level, next_review_at "
            "FROM knowledge_record WHERE user_id=? AND topic_id=?",
            ("default", topic),
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            result = {
                "topic_id": row[0], "topic_name": row[1],
                "mastery_level": row[2], "status": row[3],
                "right_count": row[4], "wrong_count": row[5],
                "difficulty_level": row[6], "next_review_at": row[7],
            }
        else:
            topic_name = topic
            for t in self.scheduler.index.get("topics", []):
                tid = t.get("id") or t.get("topic_id", "")
                if tid == topic:
                    topic_name = t.get("name", topic)
                    break
            result = {
                "topic_id": topic, "topic_name": topic_name,
                "mastery_level": 0.0, "status": "unvisited",
                "right_count": 0, "wrong_count": 0,
                "difficulty_level": 2, "next_review_at": None,
            }

        if json_output:
            _print_json(result)
        else:
            print(f"知识点: {result['topic_name']}")
            print(f"掌握度: {result['mastery_level']:.1%}")
            print(f"状态: {result['status']}")
            print(f"答对/答错: {result['right_count']}/{result['wrong_count']}")

    def cmd_save_result(self, args, json_output=False):
        parsed = _parse_named_args(args)
        topic_id = parsed.get("topic-id", "")
        question = parsed.get("question", "")
        answer = parsed.get("answer", "")
        eval_json_str = parsed.get("evaluation", "{}")

        if not topic_id:
            if json_output:
                _print_json({"error": "missing --topic-id"})
            else:
                print("缺少 --topic-id")
            return

        try:
            eval_data = json.loads(eval_json_str)
        except json.JSONDecodeError:
            if json_output:
                _print_json({"error": "invalid --evaluation JSON"})
            else:
                print("无效的 --evaluation JSON")
            return

        topic_name = topic_id
        for t in self.scheduler.index.get("topics", []):
            tid = t.get("id") or t.get("topic_id", "")
            if tid == topic_id:
                topic_name = t.get("name", topic_id)
                break

        eval_result = EvaluationResult(
            rating=eval_data.get("rating", "okay"),
            score_total=eval_data.get("score_total", 0.5),
            correctness=eval_data.get("correctness", 0.5),
            completeness=eval_data.get("completeness", 0.5),
            depth=eval_data.get("depth", 0.5),
            clarity=eval_data.get("clarity", 0.5),
            code_accuracy=eval_data.get("code_accuracy", 0.5),
            edge_case_awareness=eval_data.get("edge_case_awareness", 0.5),
            missing_points=eval_data.get("missing_points", []),
            wrong_points=eval_data.get("wrong_points", []),
            weakness_tags=eval_data.get("weakness_tags", []),
            hallucinated_points=eval_data.get("hallucinated_points", []),
            evaluator_confidence=eval_data.get("evaluator_confidence", 1.0),
        )

        self.db.update_knowledge_mastery(
            "default", topic_id, topic_name, "C++",
            eval_result.score_total, eval_result.evaluator_confidence,
        )

        qa_id = self.db.save_qa(
            "default", None, topic_id, question, answer, None, eval_result,
        )

        from .db import get_connection
        conn = get_connection(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT mastery_level FROM knowledge_record "
            "WHERE user_id=? AND topic_id=?", ("default", topic_id)
        )
        row = cursor.fetchone()
        conn.close()
        new_mastery = row[0] if row else 0.0

        result = {"ok": True, "qa_id": qa_id, "new_mastery": round(new_mastery, 3)}
        if json_output:
            _print_json(result)
        else:
            print(f"已保存 (qa_id={qa_id}), 新掌握度: {new_mastery:.1%}")

    def cmd_next_topic(self, args, json_output=False):
        parsed = _parse_named_args(args)
        target_diff = int(parsed.get("difficulty", "2"))

        weak = self.db.get_weak_topics("default", limit=10)
        due = self.db.get_due_topics("default")

        chosen = self.scheduler.select_next_topic(weak, due, target_diff)
        if not chosen:
            topics = self.scheduler.index.get("topics", [])
            if topics:
                import random
                t = random.choice(topics)
                chosen = {
                    "topic_id": t.get("id") or t.get("topic_id", ""),
                    "topic_name": t.get("name", ""),
                    "mastery_level": 0.0,
                    "difficulty_level": target_diff,
                    "next_review_at": None,
                    "reason": "random",
                }
            else:
                chosen = {"error": "no topics available"}

        if json_output:
            _print_json(chosen)
        else:
            if "error" in chosen:
                print(chosen["error"])
            else:
                print(f"推荐: {chosen['topic_name']} (掌握度 {chosen['mastery_level']:.1%})")

    def cmd_reset(self, json_output=False):
        if json_output:
            _print_json({"ok": False, "error": "not implemented"})
        else:
            print("重置功能待实现")

    def cmd_export(self, json_output=False):
        if json_output:
            _print_json({"ok": False, "error": "not implemented"})
        else:
            print("导出功能待实现")


def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":")))


def _parse_named_args(args):
    result = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            key = args[i][2:]
            result[key] = args[i + 1]
            i += 2
        else:
            i += 1
    return result


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    use_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]

    if len(argv) < 1:
        print("用法: coach <command> [args] [--json]")
        print("命令: status, weak, due, plan, topic-info <id>, save-result ..., next-topic, reset, export")
        return 0

    repo_path = Path(__file__).parent.parent
    cli = CoachCLI(repo_path=str(repo_path))

    cmd = argv[0]
    rest = argv[1:]

    dispatch = {
        "status": lambda: cli.cmd_status(use_json),
        "weak": lambda: cli.cmd_weak(use_json),
        "due": lambda: cli.cmd_due(use_json),
        "plan": lambda: cli.cmd_plan(use_json),
        "reset": lambda: cli.cmd_reset(use_json),
        "export": lambda: cli.cmd_export(use_json),
    }

    if cmd in dispatch:
        dispatch[cmd]()
    elif cmd == "topic-info":
        if not rest:
            if use_json:
                _print_json({"error": "missing topic id"})
            else:
                print("用法: topic-info <topic_id>")
            return 1
        cli.cmd_topic_info(rest[0], use_json)
    elif cmd == "save-result":
        cli.cmd_save_result(rest, use_json)
    elif cmd == "next-topic":
        cli.cmd_next_topic(rest, use_json)
    else:
        if use_json:
            _print_json({"error": f"未知命令: {cmd}"})
        else:
            print(f"未知命令: {cmd}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
