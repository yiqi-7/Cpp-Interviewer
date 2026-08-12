"""CLI 入口：python -m coach.cli <command> [args] [--json]"""
import html
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
            print(f"答题记录数: {summary['total_questions']}")
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

    def cmd_topic(self, topic: str, json_output=False):
        self.cmd_topic_info(topic, json_output)

    def cmd_topic_search(self, keyword: str, json_output=False):
        needle = keyword.strip().lower()
        matches = []
        if needle:
            for topic in self.scheduler.index.get("topics", []):
                topic_id = topic.get("id") or topic.get("topic_id", "")
                topic_name = topic.get("name") or topic.get("topic_name", topic_id)
                keywords = topic.get("keywords", [])
                haystack = [topic_id.lower(), topic_name.lower()]
                haystack.extend(str(k).lower() for k in keywords)
                if any(needle in item for item in haystack):
                    matches.append(
                        {
                            "topic_id": topic_id,
                            "topic_name": topic_name,
                            "domain": topic.get("domain", ""),
                            "keywords": keywords,
                            "interview_frequency": topic.get("interview_frequency", "medium"),
                            "related_topics": topic.get("related_topics", []),
                        }
                    )

        result = {"query": keyword, "matches": matches}
        if json_output:
            _print_json(result)
        else:
            if not matches:
                print("没有匹配到知识点")
                return 0
            for item in matches:
                print(f"{item['topic_id']}\t{item['topic_name']}")
        return 0

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
            return 1

        try:
            eval_data = json.loads(eval_json_str)
        except json.JSONDecodeError:
            if json_output:
                _print_json({"error": "invalid --evaluation JSON"})
            else:
                print("无效的 --evaluation JSON")
            return 1

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
        return 0

    def cmd_next_topic(self, args, json_output=False):
        parsed = _parse_named_args(args)
        try:
            target_diff = int(parsed.get("difficulty", "2"))
        except ValueError:
            if json_output:
                _print_json({"error": "invalid --difficulty"})
            else:
                print("无效的 --difficulty")
            return 1
        if target_diff not in (1, 2, 3):
            if json_output:
                _print_json({"error": "--difficulty must be 1, 2, or 3"})
            else:
                print("--difficulty 必须是 1、2 或 3")
            return 1

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
        return 0

    def cmd_reset(self, args, json_output=False):
        parsed = _parse_named_args(args)
        confirmed = "yes" in parsed
        if not confirmed:
            result = {"ok": False, "error": "requires --yes"}
            if json_output:
                _print_json(result)
            else:
                print("重置会清空本地训练记录。确认执行请加 --yes")
            return 1

        deleted = self.db.reset_user_state("default")
        result = {"ok": True, "deleted": deleted}
        if json_output:
            _print_json(result)
        else:
            total = sum(deleted.values())
            print(f"已重置训练状态，共清理 {total} 条记录")
        return 0

    def cmd_export(self, args, json_output=False):
        parsed = _parse_named_args(args)
        fmt_value = parsed.get("format", "json")
        output = parsed.get("output")

        if fmt_value is True or fmt_value == "":
            result = {"ok": False, "error": "missing --format value"}
            if json_output:
                _print_json(result)
            else:
                print("缺少 --format 的取值。可选: json, md, txt, doc")
            return 1
        if output is True or output == "":
            result = {"ok": False, "error": "missing --output value"}
            if json_output:
                _print_json(result)
            else:
                print("缺少 --output 的文件路径")
            return 1

        fmt = str(fmt_value).lower()
        if fmt not in _EXPORT_FORMATS:
            result = {"ok": False, "error": f"unsupported export format: {fmt}"}
            if json_output:
                _print_json(result)
            else:
                print("不支持的导出格式。可选: json, md, txt, doc")
            return 1

        data = self.db.export_user_data("default")
        rendered = _render_export(data, fmt)
        if output:
            output_path = Path(output).expanduser()
        else:
            output_path = None

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
            result = {"ok": True, "format": fmt, "output": str(output_path)}
            if json_output:
                _print_json(result)
            else:
                print(f"已导出: {output_path}")
        else:
            if json_output and fmt == "json":
                print(rendered)
            elif json_output:
                _print_json({"ok": True, "format": fmt, "content": rendered})
            else:
                print(rendered)
        return 0

    def cmd_topic_context(self, args, json_output=False):
        """Return keywords + related_topics + name + domain for a topic.

        Usage: topic-context <topic_id_or_keyword> [--json]
        """
        if not args:
            if json_output:
                _print_json({"error": "missing topic id or keyword"})
            else:
                print("用法: topic-context <topic_id_or_keyword>")
            return 1

        query = args[0].lower()
        match = None
        for t in self.scheduler.index.get("topics", []):
            tid = (t.get("id") or t.get("topic_id", "")).lower()
            tname = t.get("name", "").lower()
            kw_list = [k.lower() for k in t.get("keywords", [])]
            if query == tid or query in tname or any(query in k for k in kw_list):
                match = t
                break

        if match is None:
            if json_output:
                _print_json({"error": f"topic not found: {args[0]}"})
            else:
                print(f"未找到 topic: {args[0]}")
            return 1

        related_ids = match.get("related_topics", []) or []
        related_names = []
        for rid in related_ids:
            for t in self.scheduler.index.get("topics", []):
                if (t.get("id") or t.get("topic_id", "")) == rid:
                    related_names.append(t.get("name", rid))
                    break

        result = {
            "topic_id": match.get("id") or match.get("topic_id", ""),
            "topic_name": match.get("name", ""),
            "domain": match.get("domain", ""),
            "keywords": match.get("keywords", []),
            "related_topics": related_ids,
            "related_topic_names": related_names,
            "interview_frequency": match.get("interview_frequency", "medium"),
            "sources": match.get("sources", []),
        }

        if json_output:
            _print_json(result)
        else:
            print(f"Topic: {result['topic_name']} ({result['topic_id']})")
            print(f"Domain: {result['domain']}")
            print(f"Keywords: {', '.join(result['keywords'])}")
            print(f"Related: {', '.join(result['related_topic_names'])}")
            print(f"Frequency: {result['interview_frequency']}")
        return 0


def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":")))


_EXPORT_FORMATS = {"json", "md", "txt", "doc"}


def _render_export(data, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)
    if fmt == "md":
        return _render_markdown_export(data)
    if fmt == "txt":
        return _render_text_export(data)
    if fmt == "doc":
        return _render_doc_export(data)
    raise ValueError(f"unsupported export format: {fmt}")


def _render_markdown_export(data) -> str:
    lines = [
        "# Cpp-Interviewer Coach Export",
        "",
        f"- User: `{data['user_id']}`",
        f"- Exported at: `{data['exported_at']}`",
        f"- Topics: {data['summary']['total']}",
        f"- Questions: {data['summary']['total_questions']}",
        f"- Average mastery: {data['summary']['avg_mastery']:.1%}",
        "",
        "## Knowledge Records",
        "",
    ]
    if data["knowledge_records"]:
        lines.append("| Topic | Status | Mastery | Right/Wrong | Next Review |")
        lines.append("|---|---|---:|---:|---|")
        for item in data["knowledge_records"]:
            lines.append(
                "| {topic_name} (`{topic_id}`) | {status} | {mastery:.1%} | {right}/{wrong} | {next_review} |".format(
                    topic_name=item["topic_name"],
                    topic_id=item["topic_id"],
                    status=item["status"],
                    mastery=item["mastery_level"] or 0.0,
                    right=item["right_count"] or 0,
                    wrong=item["wrong_count"] or 0,
                    next_review=item["next_review_at"] or "",
                )
            )
    else:
        lines.append("No knowledge records.")

    lines.extend(["", "## QA History", ""])
    if data["qa_history"]:
        for qa in data["qa_history"]:
            lines.extend(
                [
                    f"### {qa['topic_id']} - {qa['created_at']}",
                    "",
                    f"- Question: {qa['question']}",
                    f"- Answer: {qa['user_answer']}",
                    f"- Rating: {qa.get('final_rating') or ''}",
                    f"- Score: {qa.get('score_total') if qa.get('score_total') is not None else ''}",
                ]
            )
            for detail in qa.get("evaluation_detail", []):
                lines.append(f"- Missing: {', '.join(detail.get('missing_points') or [])}")
                lines.append(f"- Weakness: {', '.join(detail.get('weakness_tags') or [])}")
            lines.append("")
    else:
        lines.append("No QA history.")

    return "\n".join(lines).rstrip() + "\n"


def _render_text_export(data) -> str:
    lines = [
        "Cpp-Interviewer Coach Export",
        "=" * 30,
        f"User: {data['user_id']}",
        f"Exported at: {data['exported_at']}",
        f"Topics: {data['summary']['total']}",
        f"Questions: {data['summary']['total_questions']}",
        f"Average mastery: {data['summary']['avg_mastery']:.1%}",
        "",
        "Knowledge Records",
        "-" * 17,
    ]
    if data["knowledge_records"]:
        for item in data["knowledge_records"]:
            lines.append(
                "{topic_name} ({topic_id}) | {status} | mastery {mastery:.1%} | right/wrong {right}/{wrong}".format(
                    topic_name=item["topic_name"],
                    topic_id=item["topic_id"],
                    status=item["status"],
                    mastery=item["mastery_level"] or 0.0,
                    right=item["right_count"] or 0,
                    wrong=item["wrong_count"] or 0,
                )
            )
    else:
        lines.append("No knowledge records.")

    lines.extend(["", "QA History", "-" * 10])
    if data["qa_history"]:
        for qa in data["qa_history"]:
            lines.append(f"[{qa['created_at']}] {qa['topic_id']}")
            lines.append(f"Q: {qa['question']}")
            lines.append(f"A: {qa['user_answer']}")
            if qa.get("final_rating"):
                lines.append(f"Rating: {qa['final_rating']} ({qa.get('score_total')})")
            lines.append("")
    else:
        lines.append("No QA history.")

    return "\n".join(lines).rstrip() + "\n"


def _render_doc_export(data) -> str:
    md = _render_markdown_export(data)
    paragraphs = []
    for line in md.splitlines():
        escaped = html.escape(line)
        if line.startswith("# "):
            paragraphs.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            paragraphs.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            paragraphs.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("|"):
            paragraphs.append(f"<pre>{escaped}</pre>")
        elif line:
            paragraphs.append(f"<p>{escaped}</p>")
        else:
            paragraphs.append("<br>")
    body = "\n".join(paragraphs)
    return (
        "<html><head><meta charset=\"utf-8\"><title>Cpp-Interviewer Coach Export</title>"
        "</head><body>"
        f"{body}"
        "</body></html>\n"
    )


def _parse_named_args(args):
    result = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args) and not args[i + 1].startswith("--"):
            key = args[i][2:]
            result[key] = args[i + 1]
            i += 2
        elif args[i].startswith("--"):
            result[args[i][2:]] = True
            i += 1
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
        print("命令: coach start, topic <id>, topic search <keyword>, topic-info <id>, topic-context <id>, status, weak, due, plan, save-result ..., next-topic, reset, export")
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
        "reset": lambda: cli.cmd_reset(rest, use_json),
        "export": lambda: cli.cmd_export(rest, use_json),
    }

    if cmd in dispatch:
        result = dispatch[cmd]()
        if isinstance(result, int):
            return result
    elif cmd == "topic-info":
        if not rest:
            if use_json:
                _print_json({"error": "missing topic id"})
            else:
                print("用法: topic-info <topic_id>")
            return 1
        cli.cmd_topic_info(rest[0], use_json)
    elif cmd == "topic-context":
        if not rest:
            if use_json:
                _print_json({"error": "missing topic id or keyword"})
            else:
                print("用法: topic-context <topic_id_or_keyword>")
            return 1
        return cli.cmd_topic_context(rest, use_json)
    elif cmd == "topic":
        if not rest:
            if use_json:
                _print_json({"error": "missing topic"})
            else:
                print("用法: topic <topic>")
            return 1
        if rest[0] == "search":
            if len(rest) < 2:
                if use_json:
                    _print_json({"error": "missing keyword"})
                else:
                    print("用法: topic search <keyword>")
                return 1
            return cli.cmd_topic_search(rest[1], use_json)
        if use_json:
            cli.cmd_topic(rest[0], use_json)
        else:
            cli.cmd_topic(rest[0])
    elif cmd == "save-result":
        return cli.cmd_save_result(rest, use_json)
    elif cmd == "next-topic":
        return cli.cmd_next_topic(rest, use_json)
    else:
        if use_json:
            _print_json({"error": f"未知命令: {cmd}"})
        else:
            print(f"未知命令: {cmd}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
