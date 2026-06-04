"""Skill prompt adapter - reads COACH_SKILL.md + shared_rules.md + knowledge_index.json, calls LLM."""
import json
from pathlib import Path
from typing import Optional

from coach.config import (
    COACH_SKILL_FILE,
    DEFAULT_TEMPERATURE,
    KNOWLEDGE_INDEX_FILE,
    SHARED_RULES_FILE,
)
from coach.llm import LLMClient
from coach.models import EvaluationResult, TrainingContext
from coach.prompts import (
    COACH_EVALUATION_PROMPT,
    COACH_QUESTION_PROMPT,
    COACH_REFERENCE_ANSWER_PROMPT,
    COACH_SYSTEM_PROMPT,
)


class SkillPromptAdapter:
    """Reads COACH_SKILL.md + shared_rules.md + knowledge_index.json, calls LLM.

    This adapter only handles: read files + call LLM.
    No scheduling, no scoring logic.
    """

    def __init__(self, llm_client: LLMClient, repo_path: str = "."):
        """Initialize the adapter.

        Args:
            llm_client: LLM client instance for generating responses.
            repo_path: Root path of the repository (default ".").
        """
        self.llm = llm_client
        self.repo_path = Path(repo_path)
        self._knowledge_index: Optional[dict] = None

    def get_system_prompt(self) -> str:
        """Read COACH_SKILL.md + shared_rules.md, concatenate.

        Returns:
            Combined system prompt from COACH_SKILL.md and shared_rules.md.
            Returns empty string if files don't exist.
        """
        coach_skill = self._load_coach_skill()
        shared_rules = self._load_shared_rules()

        parts = []
        if coach_skill:
            parts.append(coach_skill)
        if shared_rules:
            parts.append(shared_rules)

        # Always include the base system prompt
        if parts:
            return "\n\n".join(parts)
        return COACH_SYSTEM_PROMPT

    def _load_knowledge_index(self) -> dict:
        """Load knowledge_index.json.

        Returns:
            Parsed JSON content or empty dict if file doesn't exist.
        """
        if self._knowledge_index is not None:
            return self._knowledge_index

        path = self.repo_path / KNOWLEDGE_INDEX_FILE
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._knowledge_index = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._knowledge_index = {}

        return self._knowledge_index

    def _load_coach_skill(self) -> str:
        """Read COACH_SKILL.md.

        Returns:
            File content or empty string if file doesn't exist.
        """
        path = self.repo_path / COACH_SKILL_FILE
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _load_shared_rules(self) -> str:
        """Read shared_rules.md.

        Returns:
            File content or empty string if file doesn't exist.
        """
        path = self.repo_path / SHARED_RULES_FILE
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def generate_question(
        self, ctx: TrainingContext, related_topics: list[str] = None
    ) -> str:
        """Generate interview question based on TrainingContext.

        Args:
            ctx: Training context containing topic info.
            related_topics: Optional list of related topic names.

        Returns:
            Generated interview question string.
        """
        topic = ctx.topic_name
        difficulty = ctx.difficulty
        weakness_tags = ",".join(ctx.weakness_tags) if ctx.weakness_tags else "无"
        user_mastery = ctx.user_mastery_level

        prompt = COACH_QUESTION_PROMPT.format(
            topic=topic,
            difficulty=difficulty,
            weakness_tags=weakness_tags,
            user_mastery=user_mastery,
        )

        response = self.llm.generate(prompt, temperature=DEFAULT_TEMPERATURE)
        return response.strip()

    def generate_reference_answer(
        self, topic: str, difficulty: int, key_points: list[str]
    ) -> str:
        """Generate reference answer.

        Args:
            topic: Topic name.
            difficulty: Difficulty level (1-3).
            key_points: List of key points to cover.

        Returns:
            Generated reference answer string.
        """
        prompt = COACH_REFERENCE_ANSWER_PROMPT.format(
            topic=topic,
            difficulty=difficulty,
            key_points=", ".join(key_points),
        )

        response = self.llm.generate(prompt, temperature=DEFAULT_TEMPERATURE)
        return response.strip()

    def evaluate_answer(
        self, question: str, user_answer: str, key_points: list[str]
    ) -> EvaluationResult:
        """Evaluate user answer and return structured result.

        Args:
            question: The interview question asked.
            user_answer: User's answer to evaluate.
            key_points: Expected key points for evaluation.

        Returns:
            EvaluationResult with structured evaluation.
        """
        prompt = COACH_EVALUATION_PROMPT.format(
            question=question,
            user_answer=user_answer,
            key_points=", ".join(key_points),
        )

        raw = self.llm.generate(prompt, temperature=DEFAULT_TEMPERATURE)
        return self._parse_evaluation(raw)

    def _parse_evaluation(self, raw: str) -> EvaluationResult:
        """Parse JSON from LLM response.

        Args:
            raw: Raw LLM response string.

        Returns:
            Parsed EvaluationResult object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        # Try to extract JSON from the response
        json_str = raw.strip()

        # Handle markdown code blocks
        if json_str.startswith("```"):
            lines = json_str.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.startswith("```"):
                    in_json = not in_json
                    continue
                if in_json:
                    json_lines.append(line)
            json_str = "\n".join(json_lines)
        else:
            # Try to find JSON object braces
            start = json_str.find("{")
            end = json_str.rfind("}")
            if start != -1 and end != -1:
                json_str = json_str[start : end + 1]

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse evaluation JSON: {e}\nRaw: {raw}")

        return EvaluationResult(
            rating=data.get("rating", "okay"),
            score_total=data.get("score_total", 0.5),
            correctness=data.get("correctness", 0.5),
            completeness=data.get("completeness", 0.5),
            depth=data.get("depth", 0.5),
            clarity=data.get("clarity", 0.5),
            code_accuracy=data.get("code_accuracy", 0.5),
            edge_case_awareness=data.get("edge_case_awareness", 0.5),
            missing_points=data.get("missing_points", []),
            wrong_points=data.get("wrong_points", []),
            weakness_tags=data.get("weakness_tags", []),
            hallucinated_points=data.get("hallucinated_points", []),
            evaluator_confidence=data.get("evaluator_confidence", 1.0),
        )