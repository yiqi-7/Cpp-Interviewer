"""Tests for CLI entrypoint."""
import sys
import os
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Ensure coach module is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from coach.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_main_status_entrypoint(capsys, tmp_path):
    """Test coach status can be called via main(['status'])."""
    # Mock the CoachCLI to avoid actual DB operations
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_status.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["status"])

        assert result == 0
        mock_instance.cmd_status.assert_called_once()


def test_main_topic_entrypoint(capsys, tmp_path):
    """Test coach topic can be called via main(['topic', '虚函数'])."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_topic.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["topic", "虚函数"])

        assert result == 0
        mock_instance.cmd_topic.assert_called_once_with("虚函数")


def test_main_topic_entrypoint_passes_json_flag(capsys, tmp_path):
    """Test coach topic forwards --json to cmd_topic."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_topic.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["topic", "虚函数", "--json"])

        assert result == 0
        mock_instance.cmd_topic.assert_called_once_with("虚函数", True)


def test_main_topic_search_entrypoint_passes_json_flag():
    """Test coach topic search forwards --json to cmd_topic_search."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_topic_search.return_value = 0
        MockCLI.return_value = mock_instance

        result = main(["topic", "search", "虚函数", "--json"])

        assert result == 0
        mock_instance.cmd_topic_search.assert_called_once_with("虚函数", True)


def test_main_topic_context_entrypoint_passes_json_flag():
    """Test coach topic-context forwards --json to cmd_topic_context."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_topic_context.return_value = 0
        MockCLI.return_value = mock_instance

        result = main(["topic-context", "cpp_vtable", "--json"])

        assert result == 0
        mock_instance.cmd_topic_context.assert_called_once_with(["cpp_vtable"], True)


def test_repo_root_python_module_entrypoint_works(tmp_path):
    """A freshly cloned repo should support python -m coach.cli from its root."""
    env = {**os.environ, "CPP_INTERVIEWER_HOME": str(tmp_path)}
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, "-m", "coach.cli", "topic-context", "cpp_vtable", "--json"],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert '"topic_id":"cpp_vtable"' in result.stdout


def test_main_unknown_command_returns_nonzero():
    """Test unknown command returns 1."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        MockCLI.return_value = mock_instance

        result = main(["unknown_command"])

        assert result == 1


def test_main_no_args_shows_help(capsys):
    """Test main([]) shows usage and returns 0."""
    result = main([])

    assert result == 0
    captured = capsys.readouterr()
    assert "用法:" in captured.out
    assert "coach start" in captured.out


def test_main_weak_entrypoint(capsys, tmp_path):
    """Test coach weak can be called via main(['weak'])."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_weak.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["weak"])

        assert result == 0
        mock_instance.cmd_weak.assert_called_once()


def test_main_plan_entrypoint(capsys, tmp_path):
    """Test coach plan can be called via main(['plan'])."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_plan.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["plan"])

        assert result == 0
        mock_instance.cmd_plan.assert_called_once()


def test_main_due_entrypoint(capsys, tmp_path):
    """Test coach due can be called via main(['due'])."""
    with patch("coach.cli.CoachCLI") as MockCLI:
        mock_instance = MagicMock()
        mock_instance.cmd_due.return_value = None
        MockCLI.return_value = mock_instance

        result = main(["due"])

        assert result == 0
        mock_instance.cmd_due.assert_called_once()


def test_main_next_topic_invalid_difficulty_returns_json_error(capsys):
    """Invalid next-topic difficulty should not crash in JSON mode."""
    result = main(["next-topic", "--difficulty", "abc", "--json"])

    assert result == 1
    captured = capsys.readouterr()
    assert '"error":"invalid --difficulty"' in captured.out


def test_main_next_topic_rejects_out_of_range_difficulty(capsys):
    """next-topic difficulty must stay in the documented 1-3 range."""
    result = main(["next-topic", "--difficulty", "4", "--json"])

    assert result == 1
    captured = capsys.readouterr()
    assert '"error":"--difficulty must be 1, 2, or 3"' in captured.out


def test_main_save_result_missing_topic_returns_nonzero(capsys):
    """save-result should return nonzero when required args are missing."""
    result = main(["save-result", "--json"])

    assert result == 1
    captured = capsys.readouterr()
    assert '"error":"missing --topic-id"' in captured.out


def test_main_save_result_invalid_json_returns_nonzero(capsys):
    """save-result should return nonzero when evaluation JSON is invalid."""
    result = main(["save-result", "--topic-id", "x", "--evaluation", "{bad", "--json"])

    assert result == 1
    captured = capsys.readouterr()
    assert '"error":"invalid --evaluation JSON"' in captured.out
