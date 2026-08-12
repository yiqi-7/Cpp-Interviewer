"""Tests for the Cpp-Interviewer skill installer."""
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run_setup(args, home, extra_env=None):
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "setup.py"), *args],
        cwd=REPO_ROOT,
        env={**os.environ, "USERPROFILE": str(home), "HOME": str(home), **(extra_env or {})},
        text=True,
        capture_output=True,
    )


def test_setup_help_does_not_install(tmp_path):
    """--help should describe usage without modifying agent skill dirs."""
    result = run_setup(["--help"], tmp_path)

    assert result.returncode == 0
    assert "Usage:" in result.stdout
    assert not (tmp_path / ".codex").exists()
    assert not (tmp_path / ".claude").exists()


def test_setup_preserves_existing_hidden_and_local_files(tmp_path):
    """Installer should not delete local metadata in an existing skill dir."""
    coach_dir = tmp_path / ".codex" / "skills" / "coach"
    git_dir = coach_dir / ".git" / "objects"
    git_dir.mkdir(parents=True)
    keep_file = coach_dir / "_topics.tmp"
    object_file = git_dir / "object"
    keep_file.write_text("local cache", encoding="utf-8")
    object_file.write_text("git metadata", encoding="utf-8")

    result = run_setup([], tmp_path)

    assert result.returncode == 0, result.stderr
    assert keep_file.read_text(encoding="utf-8") == "local cache"
    assert object_file.read_text(encoding="utf-8") == "git metadata"
    assert (coach_dir / "SKILL.md").exists()
    assert (coach_dir / "coach" / "cli.py").exists()


def test_setup_installs_to_requested_agent_targets(tmp_path):
    """Installer should support mainstream agent skill directories."""
    result = run_setup(["--agents", "codex,cursor"], tmp_path)

    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".codex" / "skills" / "cpp-interviewer" / "SKILL.md").exists()
    assert (tmp_path / ".cursor" / "skills" / "cpp-interviewer" / "SKILL.md").exists()
    assert (tmp_path / ".codex" / "skills" / "interview" / "SKILL.md").exists()
    assert (tmp_path / ".codex" / "skills" / "coach" / "SKILL.md").exists()


def test_setup_all_installs_known_mainstream_targets(tmp_path):
    """--agents all should give users a one-command mainstream install path."""
    result = run_setup(["--agents", "all"], tmp_path)

    assert result.returncode == 0, result.stderr
    for folder in (".codex", ".cursor", ".claude", ".agents"):
        assert (tmp_path / folder / "skills" / "cpp-interviewer" / "SKILL.md").exists()
        assert (tmp_path / folder / "skills" / "interview" / "SKILL.md").exists()
        assert (tmp_path / folder / "skills" / "coach" / "SKILL.md").exists()


def test_setup_installs_to_custom_skills_dir(tmp_path):
    """--skills-dir should support agents with custom skill locations."""
    custom_dir = tmp_path / "custom-agent" / "skills"

    result = run_setup(["--skills-dir", str(custom_dir)], tmp_path)

    assert result.returncode == 0, result.stderr
    assert (custom_dir / "cpp-interviewer" / "SKILL.md").exists()
    assert (custom_dir / "interview" / "SKILL.md").exists()
    assert (custom_dir / "coach" / "SKILL.md").exists()


def test_setup_honors_cpp_interviewer_home(tmp_path):
    """CPP_INTERVIEWER_HOME should override the default user-data directory."""
    data_home = tmp_path / "portable-data"

    result = run_setup([], tmp_path, {"CPP_INTERVIEWER_HOME": str(data_home)})

    assert result.returncode == 0, result.stderr
    assert data_home.exists()
    assert "SQLite database will be created at:" in result.stdout
    assert str(data_home / "coach.sqlite") in result.stdout


def test_editable_develop_install_works_in_venv(tmp_path):
    """The coach backend should be installable after clone without global side effects."""
    venv_dir = tmp_path / "venv"
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv_dir)],
        check=True,
        text=True,
        capture_output=True,
        timeout=120,
    )
    python_bin = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

    result = subprocess.run(
        [str(python_bin), "setup.py", "develop"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    import_result = subprocess.run(
        [str(python_bin), "-c", "import coach.cli; print(coach.cli.main(['status', '--json']))"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=120,
    )

    assert import_result.returncode == 0, import_result.stdout + import_result.stderr
    assert '"total"' in import_result.stdout
