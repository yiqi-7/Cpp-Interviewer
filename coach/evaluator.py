"""Six-dimension structured scorer with JSON Schema validation."""
from typing import Optional

from coach.models import EvaluationResult
from coach.prompts import COACH_EVALUATION_PROMPT
from coach.skill_adapter import SkillPromptAdapter


class Evaluator:
    """Six-dimension structured scorer with JSON Schema validation."""

    MAX_RETRIES = 2

    def __init__(self, skill_adapter: SkillPromptAdapter):
        self.skill_adapter = skill_adapter

    def evaluate(
        self,
        question: str,
        user_answer: str,
        key_points: list[str],
    ) -> EvaluationResult:
        """Evaluate user answer with retry on parse failure."""
        for attempt in range(self.MAX_RETRIES + 1):
            raw = self._call_llm(question, user_answer, key_points)
            result = self._parse_evaluation(raw)
            if result is not None:
                return result
        # Fallback on complete failure
        return EvaluationResult(
            rating="okay",
            score_total=0.5,
            correctness=0.5,
            completeness=0.5,
            depth=0.5,
            clarity=0.5,
            code_accuracy=0.5,
            edge_case_awareness=0.5,
            missing_points=[],
            wrong_points=[],
            hallucinated_points=[],
            weakness_tags=[],
            evaluator_confidence=0.3,
        )

    def _call_llm(
        self, question: str, user_answer: str, key_points: list[str]
    ) -> str:
        """Call skill_adapter to get evaluation JSON."""
        return self.skill_adapter.llm.generate(
            self._build_eval_prompt(question, user_answer, key_points),
            system=self.skill_adapter.get_system_prompt(),
            temperature=0.3,
        )

    def _build_eval_prompt(
        self, question: str, user_answer: str, key_points: list[str]
    ) -> str:
        """Build evaluation prompt."""
        return COACH_EVALUATION_PROMPT.format(
            key_points=", ".join(key_points),
            user_answer=user_answer,
            question=question,
        )

    def _parse_evaluation(self, raw: str) -> Optional[EvaluationResult]:
        """Parse JSON from LLM response with strict validation."""
        import json
        import re

        # Extract JSON from markdown code blocks or raw
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return None
        try:
            data = json.loads(match.group())
        except json.JSONDecodeError:
            return None

        # Validate required fields
        required = [
            "rating",
            "score_total",
            "correctness",
            "completeness",
            "depth",
            "clarity",
            "code_accuracy",
            "edge_case_awareness",
            "missing_points",
            "wrong_points",
            "weakness_tags",
            "evaluator_confidence",
            "hallucinated_points",
        ]
        for field in required:
            if field not in data:
                return None

        # Validate types and ranges
        if data["rating"] not in ("good", "okay", "poor"):
            return None
        for key in [
            "score_total",
            "correctness",
            "completeness",
            "depth",
            "clarity",
            "code_accuracy",
            "edge_case_awareness",
            "evaluator_confidence",
        ]:
            if not isinstance(data[key], (int, float)) or not (
                0.0 <= data[key] <= 1.0
            ):
                return None

        return EvaluationResult(
            rating=data["rating"],
            score_total=float(data["score_total"]),
            correctness=float(data["correctness"]),
            completeness=float(data["completeness"]),
            depth=float(data["depth"]),
            clarity=float(data["clarity"]),
            code_accuracy=float(data["code_accuracy"]),
            edge_case_awareness=float(data["edge_case_awareness"]),
            missing_points=data.get("missing_points", []),
            wrong_points=data.get("wrong_points", []),
            hallucinated_points=data.get("hallucinated_points", []),
            weakness_tags=data.get("weakness_tags", []),
            evaluator_confidence=float(data.get("evaluator_confidence", 0.8)),
        )