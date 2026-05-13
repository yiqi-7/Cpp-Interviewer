"""Tests for SkillPromptAdapter."""
import json

import pytest

from coach.llm import MockLLMClient
from coach.skill_adapter import SkillPromptAdapter
from coach.models import TrainingContext


def test_mock_llm_generate_question():
    """Test MockLLMClient generates question properly."""
    client = MockLLMClient()
    result = client.generate("基于以下 context 生成面试题：topic: 虚函数")
    assert "虚函数" in result


def test_mock_llm_evaluate():
    """Test MockLLMClient returns valid JSON evaluation."""
    client = MockLLMClient()
    result = client.generate("你是一个面试官，评估用户回答")
    # Must return valid JSON
    data = json.loads(result)
    assert "rating" in data


def test_skill_adapter_generate_question():
    """Test SkillPromptAdapter.generate_question()."""
    adapter = SkillPromptAdapter(MockLLMClient())
    ctx = TrainingContext(
        topic_id="virtual_function",
        topic_name="虚函数",
        difficulty=2,
        weakness_tags=["vtable"],
        user_mastery_level=0.3,
    )
    question = adapter.generate_question(ctx)
    assert len(question) > 0


def test_skill_adapter_evaluate_answer():
    """Test SkillPromptAdapter.evaluate_answer()."""
    adapter = SkillPromptAdapter(MockLLMClient())
    result = adapter.evaluate_answer(
        "虚函数是怎么实现的？",
        "通过 vtable 实现多态",
        ["vptr", "vtable"],
    )
    assert result.rating in ("good", "okay", "poor")
    assert 0.0 <= result.score_total <= 1.0
    assert len(result.weakness_tags) >= 0
    assert len(result.hallucinated_points) >= 0  # Must support this field


def test_skill_adapter_get_system_prompt():
    """Test SkillPromptAdapter.get_system_prompt()."""
    adapter = SkillPromptAdapter(MockLLMClient())
    prompt = adapter.get_system_prompt()
    assert len(prompt) > 0


def test_skill_adapter_loads_knowledge_index():
    """Test SkillPromptAdapter._load_knowledge_index()."""
    adapter = SkillPromptAdapter(MockLLMClient())
    index = adapter._load_knowledge_index()
    assert isinstance(index, dict)