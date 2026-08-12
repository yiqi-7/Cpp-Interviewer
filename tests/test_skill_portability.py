"""Tests for portable Agent Skills layout."""
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_core_skill_has_required_references():
    """The agent-neutral core skill should point to its progressive references."""
    skill = _read("skills/cpp-interviewer/SKILL.md")

    assert "name: cpp-interviewer" in skill
    assert "references/interview-mode.md" in skill
    assert "references/coach-mode.md" in skill
    assert "references/knowledge-schema.md" in skill
    assert (REPO_ROOT / "skills/cpp-interviewer/agents/openai.yaml").exists()


def test_compatibility_skills_do_not_use_platform_specific_tools():
    """Slash wrappers should not hardcode one agent's tool names or paths."""
    banned = [
        "CLAUDE_SKILL_DIR",
        "~/.claude/skills/coach",
        "AskUserQuestion",
        "WebFetch",
        "WebSearch",
        "Co-" + "Authored-By",
    ]

    for path in ("skills/interview/SKILL.md", "skills/coach/SKILL.md"):
        content = _read(path)
        for token in banned:
            assert token not in content


def test_root_documentation_stays_compact():
    """The repo root should keep one README and avoid duplicate agent docs."""
    for path in ("CLAUDE.md", "GEMINI.md", "README_EN.md"):
        assert not (REPO_ROOT / path).exists()


def test_copilot_shim_and_readme_point_to_core_skill():
    """Instruction-only agents should reuse the same core skill."""
    assert "skills/cpp-interviewer/SKILL.md" in _read(".github/copilot-instructions.md")
    assert "skills/cpp-interviewer/SKILL.md" in _read("README.md")
