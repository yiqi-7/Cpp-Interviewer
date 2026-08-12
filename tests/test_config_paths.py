"""Tests for portable path configuration."""
from pathlib import Path

from coach import config


def test_cpp_interviewer_home_controls_default_db_path(monkeypatch, tmp_path):
    """CPP_INTERVIEWER_HOME should define the default SQLite location."""
    monkeypatch.delenv("CPP_INTERVIEWER_DB", raising=False)
    monkeypatch.delenv("COACH_DB_PATH", raising=False)
    monkeypatch.setenv("CPP_INTERVIEWER_HOME", str(tmp_path))

    assert config._default_db_path() == str(tmp_path / "coach.sqlite")


def test_cpp_interviewer_db_takes_precedence(monkeypatch, tmp_path):
    """CPP_INTERVIEWER_DB should override both home and legacy DB env vars."""
    db_path = tmp_path / "custom.sqlite"
    monkeypatch.setenv("CPP_INTERVIEWER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("COACH_DB_PATH", str(tmp_path / "legacy.sqlite"))
    monkeypatch.setenv("CPP_INTERVIEWER_DB", str(db_path))

    assert config._default_db_path() == str(db_path)


def test_cpp_interviewer_index_takes_precedence(monkeypatch, tmp_path):
    """CPP_INTERVIEWER_INDEX should override legacy index env vars."""
    index_path = tmp_path / "knowledge_index.json"
    monkeypatch.setenv("COACH_INDEX_PATH", str(tmp_path / "legacy.json"))
    monkeypatch.setenv("CPP_INTERVIEWER_INDEX", str(index_path))

    assert config._default_index_path() == str(index_path)


def test_default_index_falls_back_to_repo_index(monkeypatch):
    """Without env vars, the repository knowledge index should be preferred."""
    monkeypatch.delenv("CPP_INTERVIEWER_INDEX", raising=False)
    monkeypatch.delenv("COACH_INDEX_PATH", raising=False)

    path = Path(config._default_index_path())

    assert path.name == "knowledge_index.json"
    assert path.parent.name == "index"
    assert path.exists()
