"""CLI 入口：python -m coach.cli <command> [args]"""
import sys
from pathlib import Path

from .config import DEFAULT_DB_PATH
from .db import CoachDB
from .llm import MockLLMClient
from .skill_adapter import SkillPromptAdapter
from .scheduler import Scheduler
from .evaluator import Evaluator
from .models import TrainingContext


class CoachCLI:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.db = CoachDB(str(self.repo_path / DEFAULT_DB_PATH))
        self.db.ensure_user("default")

        # Initialize components with MockLLMClient
        self.llm = MockLLMClient()
        self.skill_adapter = SkillPromptAdapter(self.llm, repo_path=str(self.repo_path))
        self.evaluator = Evaluator(self.skill_adapter)
        self.scheduler = self._load_scheduler()

        self.current_session_id = None

    def _load_scheduler(self):
        import json
        index_path = self.repo_path / "index" / "knowledge_index.json"
        if index_path.exists():
            with open(index_path, "r", encoding="utf-8") as f:
                index = json.load(f)
        else:
            index = {"topics": []}
        return Scheduler(index)

    def cmd_start(self):
        """进入训练模式：探测水平 -> 生成计划 -> 循环训练"""
        self.current_session_id = self.db.start_session("default", "coach")
        print("进入训练模式（输入 '退出' 结束）")
        print("-" * 40)

        # 先问一个引导问题探测水平
        ctx = TrainingContext(
            topic_id="start", topic_name="引导问题", difficulty=1,
            session_id=self.current_session_id
        )
        question = self.skill_adapter.generate_question(ctx)
        print(f"\n引导问题: {question}")
        user_answer = input("你的回答: ").strip()
        if user_answer == "退出":
            return

        # 根据回答简单评估，跳过深入实现，专注于训练循环
        self._train_loop()

    def cmd_topic(self, topic: str):
        """指定专题训练"""
        self.current_session_id = self.db.start_session("default", "coach", target_domain=topic)
        weak = [{"topic_id": topic, "topic_name": topic, "mastery_level": 0.0, "difficulty_level": 2}]
        self._train_loop_with_topics(weak)

    def cmd_weak(self):
        """训练薄弱点"""
        self.current_session_id = self.db.start_session("default", "coach")
        weak = self.db.get_weak_topics("default", limit=5)
        if not weak:
            print("当前没有薄弱知识点记录，先用 /coach start 开始训练")
            return
        self._train_loop_with_topics(weak)

    def cmd_due(self):
        """训练到期复习点"""
        self.current_session_id = self.db.start_session("default", "coach")
        due = self.db.get_due_topics("default")
        if not due:
            print("没有到期复习的知识点")
            return
        self._train_loop_with_topics(due)

    def cmd_status(self):
        """查看掌握度仪表盘"""
        summary = self.db.get_status_summary("default")
        print(f"总知识点数: {summary['total']}")
        print(f"已掌握: {summary['mastered']}")
        print(f"薄弱: {summary['weak']}")
        print(f"平均掌握度: {summary['avg_mastery']:.1%}")

    def cmd_plan(self):
        """生成今日训练计划"""
        weak = self.db.get_weak_topics("default", limit=5)
        due = self.db.get_due_topics("default")
        print("今日训练计划：")
        for i, t in enumerate(weak[:3], 1):
            print(f"  {i}. {t['topic_name']} (掌握度 {t['mastery_level']:.1%})")
        for i, t in enumerate(due[:2], len(weak[:3]) + 1):
            print(f"  {i}. {t['topic_name']} (到期复习)")

    def cmd_reset(self):
        print("重置功能待实现（MVP 跳过）")

    def cmd_export(self):
        print("导出功能待实现（MVP 跳过）")

    def _train_loop_with_topics(self, topics: list[dict]):
        """针对给定 topics 进行训练循环"""
        for t in topics:
            ctx = TrainingContext(
                topic_id=t["topic_id"],
                topic_name=t.get("topic_name", t["topic_id"]),
                difficulty=t.get("difficulty_level", 2),
                user_mastery_level=t.get("mastery_level", 0.0),
                session_id=self.current_session_id
            )
            related = []
            question = self.skill_adapter.generate_question(ctx, related)
            print(f"\n题目: {question}")
            user_answer = input("你的回答: ").strip()
            if not user_answer or user_answer == "退出":
                break

            # 评价
            key_points = ["基本概念", "实现原理", "常见应用"]
            eval_result = self.evaluator.evaluate(question, user_answer, key_points)

            # 极简反馈
            rating_text = {"good": "正确 ✓", "okay": "基本可以，细节不足", "poor": "需要加强"}
            print(f"评价：{rating_text.get(eval_result.rating, '')}")
            if eval_result.weakness_tags:
                print(f"薄弱点: {', '.join(eval_result.weakness_tags)}")

            # 更新状态
            self.db.update_knowledge_mastery(
                "default", t["topic_id"], t.get("topic_name", t["topic_id"]), "C++",
                eval_result.score_total, eval_result.evaluator_confidence
            )
            ref_answer = self.skill_adapter.generate_reference_answer(
                t["topic_id"], ctx.difficulty, key_points
            )
            self.db.save_qa(
                "default", self.current_session_id,
                t["topic_id"], question, user_answer, ref_answer, eval_result
            )
            print()

    def _train_loop(self):
        """自由训练循环：用户输入 topic，Agent 出题训练"""
        while True:
            topic_name = input("\n输入要训练的 topic（或 '退出'）: ").strip()
            if not topic_name or topic_name == "退出":
                break
            ctx = TrainingContext(
                topic_id=topic_name, topic_name=topic_name,
                difficulty=2, session_id=self.current_session_id
            )
            question = self.skill_adapter.generate_question(ctx)
            print(f"题目: {question}")
            user_answer = input("你的回答: ").strip()
            if not user_answer or user_answer == "退出":
                break
            key_points = ["基本概念", "实现原理", "常见应用"]
            eval_result = self.evaluator.evaluate(question, user_answer, key_points)
            print(f"评价: {eval_result.rating} ({eval_result.score_total:.2f})")
            self.db.update_knowledge_mastery(
                "default", topic_name, topic_name, "C++",
                eval_result.score_total, eval_result.evaluator_confidence
            )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Supports both console_scripts and python -m coach.cli."""
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) < 1:
        print("用法: coach start|topic <专题>|weak|due|status|plan|reset|export")
        print("提示: 使用 /coach status 等命令在 Claude Code 中直接训练")
        return 0

    repo_path = Path(__file__).parent.parent
    cli = CoachCLI(repo_path=str(repo_path))

    cmd = argv[0]
    if cmd == "start":
        cli.cmd_start()
    elif cmd == "topic":
        cli.cmd_topic(argv[1] if len(argv) > 1 else "")
    elif cmd == "weak":
        cli.cmd_weak()
    elif cmd == "due":
        cli.cmd_due()
    elif cmd == "status":
        cli.cmd_status()
    elif cmd == "plan":
        cli.cmd_plan()
    elif cmd == "reset":
        cli.cmd_reset()
    elif cmd == "export":
        cli.cmd_export()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: start, topic <专题>, weak, due, status, plan, reset, export")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())