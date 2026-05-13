"""Tests for Evaluator."""
import pytest

from coach.evaluator import Evaluator
from coach.llm import MockLLMClient
from coach.skill_adapter import SkillPromptAdapter


def test_evaluator_parses_valid_json():
    """Test that evaluator parses valid JSON from LLM response."""
    adapter = SkillPromptAdapter(MockLLMClient())
    ev = Evaluator(adapter)
    result = ev.evaluate(
        "虚函数是怎么实现的？",
        "通过 vtable 实现动态绑定",
        ["vptr", "vtable", "动态绑定"],
    )
    assert result.rating in ("good", "okay", "poor")
    assert 0.0 <= result.score_total <= 1.0
    assert len(result.weakness_tags) >= 0
    assert len(result.hallucinated_points) >= 0  # Must support this


def test_evaluator_rejects_invalid_json():
    """Test fallback on non-JSON LLM response."""

    class BadClient(MockLLMClient):
        def generate(self, prompt, system=None, temperature=0.7):
            return "这不是 JSON"

    adapter = SkillPromptAdapter(BadClient())
    ev = Evaluator(adapter)
    result = ev.evaluate("虚函数？", "不知道", ["vptr"])
    # Should fallback
    assert result.rating == "okay"
    assert result.evaluator_confidence == 0.3


def test_evaluator_rejects_out_of_range():
    """Test rejection of out-of-range score values."""

    class OutOfRangeClient(MockLLMClient):
        def generate(self, prompt, system=None, temperature=0.7):
            return (
                '{"rating":"okay","score_total":1.5,'
                '"correctness":0.7,"completeness":0.6,"depth":0.5,'
                '"clarity":0.7,"code_accuracy":0.8,"edge_case_awareness":0.45,'
                '"missing_points":[],"wrong_points":[],'
                '"weakness_tags":[],"evaluator_confidence":0.8,'
                '"hallucinated_points":[]}'
            )

    adapter = SkillPromptAdapter(OutOfRangeClient())
    ev = Evaluator(adapter)
    result = ev.evaluate("虚函数？", "不知道", ["vptr"])
    # Should fallback since 1.5 > 1.0
    assert result.rating == "okay"


def test_evaluator_rejects_bad_rating():
    """Test rejection of invalid rating value."""

    class BadRatingClient(MockLLMClient):
        def generate(self, prompt, system=None, temperature=0.7):
            return (
                '{"rating":"excellent","score_total":0.7,'
                '"correctness":0.7,"completeness":0.6,"depth":0.5,'
                '"clarity":0.7,"code_accuracy":0.8,"edge_case_awareness":0.45,'
                '"missing_points":[],"wrong_points":[],'
                '"weakness_tags":[],"evaluator_confidence":0.8,'
                '"hallucinated_points":[]}'
            )

    adapter = SkillPromptAdapter(BadRatingClient())
    ev = Evaluator(adapter)
    result = ev.evaluate("虚函数？", "不知道", ["vptr"])
    assert result.rating == "okay"  # fallback


def test_evaluator_calls_skill_adapter_llm():
    """Test that evaluator delegates to skill_adapter.llm."""
    adapter = SkillPromptAdapter(MockLLMClient())
    ev = Evaluator(adapter)
    result = ev.evaluate("虚函数？", "vtable 实现", ["vptr"])
    # If MockLLMClient works, should get valid result
    assert result is not None