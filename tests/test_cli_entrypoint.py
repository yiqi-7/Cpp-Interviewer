"""Tests for CLI entrypoint."""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Ensure coach module is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from coach.cli import main


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