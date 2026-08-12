#!/usr/bin/env python3
"""Cpp-Interviewer Skill 安装脚本 — 跨平台，支持 Windows / Linux / macOS"""

import os
import shutil
import sys
from pathlib import Path


MANAGED_INTERVIEW_ENTRIES = ["SKILL.md", "COACH_SKILL.md", "shared_rules.md", "index"]
MANAGED_COACH_ENTRIES = ["SKILL.md", "coach", "index"]
MANAGED_CORE_ENTRIES = ["SKILL.md", "agents", "references", "index"]
DEFAULT_AGENTS = ["codex"]
ALL_AGENT_TARGETS = ["codex", "cursor", "claude", "agents"]
AGENT_SKILL_DIRS = {
    "agents": ".agents/skills",
    "codex": ".codex/skills",
    "chatgpt": ".codex/skills",
    "claude": ".claude/skills",
    "claude-code": ".claude/skills",
    "cursor": ".cursor/skills",
}
SETUPTOOLS_COMMANDS = {
    "bdist_wheel",
    "build",
    "build_ext",
    "build_py",
    "develop",
    "dist_info",
    "egg_info",
    "editable_wheel",
    "install",
    "sdist",
}


def run_setuptools_setup() -> None:
    from setuptools import find_packages, setup

    setup(
        package_dir={"": "skills/coach"},
        packages=find_packages(where="skills/coach", include=["coach", "coach.*"]),
        include_package_data=True,
    )


def print_help() -> None:
    print("Usage: python setup.py [--agents codex,claude,cursor,agents|all] [--skills-dir PATH] [--help]")
    print()
    print("Install Cpp-Interviewer skills into mainstream agent skill directories.")
    print("Default agent target: codex. Use --agents all for common local agent homes.")
    print("Use --skills-dir PATH for an agent with a custom skills directory.")
    print("Set CPP_INTERVIEWER_HOME to choose the data directory.")
    print("Existing local metadata such as .git directories is preserved.")


def replace_managed_entries(src_dir: Path, dst_dir: Path, entries: list[str]) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        target = dst_dir / entry
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        source = src_dir / entry
        if source.is_dir():
            shutil.copytree(source, target)
        elif source.exists():
            shutil.copy2(source, target)


def _parse_agents(value: str) -> list[str]:
    agents = [item.strip().lower() for item in value.split(",") if item.strip()]
    if "all" in agents:
        return list(ALL_AGENT_TARGETS)
    unknown = [agent for agent in agents if agent not in AGENT_SKILL_DIRS]
    if unknown:
        raise ValueError(f"Unsupported agent target: {unknown[0]}")
    return agents or list(DEFAULT_AGENTS)


def parse_args(argv: list[str]) -> tuple[list[str], list[Path], bool]:
    agents = list(DEFAULT_AGENTS)
    custom_skill_dirs: list[Path] = []
    agents_explicit = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            return agents, custom_skill_dirs, True
        if arg == "--agents":
            if i + 1 >= len(argv):
                raise ValueError("--agents requires a comma-separated value")
            agents = _parse_agents(argv[i + 1])
            agents_explicit = True
            i += 2
            continue
        if arg.startswith("--agents="):
            agents = _parse_agents(arg.split("=", 1)[1])
            agents_explicit = True
            i += 1
            continue
        if arg == "--skills-dir":
            if i + 1 >= len(argv):
                raise ValueError("--skills-dir requires a path")
            custom_skill_dirs.append(Path(argv[i + 1]).expanduser())
            i += 2
            continue
        if arg.startswith("--skills-dir="):
            custom_skill_dirs.append(Path(arg.split("=", 1)[1]).expanduser())
            i += 1
            continue
        raise ValueError(f"Unknown argument: {arg}")
    if custom_skill_dirs and not agents_explicit:
        agents = []
    return agents, custom_skill_dirs, False


def _skill_dir_for_agent(agent: str) -> Path:
    return Path.home() / AGENT_SKILL_DIRS[agent]


def _data_dir() -> Path:
    env = os.environ.get("CPP_INTERVIEWER_HOME")
    if env:
        return Path(env)
    return Path.home() / ".cpp-interviewer"


def install_to_skills_dir(script_dir: Path, skills_dir: Path) -> None:
    src_core = script_dir / "skills" / "cpp-interviewer"
    src_interview = script_dir / "skills" / "interview"
    src_coach = script_dir / "skills" / "coach"
    src_coach_pkg = script_dir / "skills" / "coach" / "coach"
    src_index = script_dir / "skills" / "coach" / "index" / "knowledge_index.json"

    dst_core = skills_dir / "cpp-interviewer"
    dst_interview = skills_dir / "interview"
    dst_coach = skills_dir / "coach"

    replace_managed_entries(src_core, dst_core, MANAGED_CORE_ENTRIES)
    core_index = dst_core / "index" / "knowledge_index.json"
    core_index.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_index, core_index)

    replace_managed_entries(src_interview, dst_interview, MANAGED_INTERVIEW_ENTRIES)
    interview_index = dst_interview / "index" / "knowledge_index.json"
    interview_index.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_index, interview_index)

    replace_managed_entries(src_coach, dst_coach, ["SKILL.md"])
    dst_coach_pkg = dst_coach / "coach"
    if dst_coach_pkg.exists():
        shutil.rmtree(dst_coach_pkg)
    shutil.copytree(src_coach_pkg, dst_coach_pkg)

    coach_index = dst_coach / "index" / "knowledge_index.json"
    coach_index.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_index, coach_index)

    main_py = dst_coach_pkg / "__main__.py"
    if not main_py.exists():
        main_py.write_text('from coach.cli import main\nraise SystemExit(main())\n', encoding="utf-8")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        agents, custom_skill_dirs, help_requested = parse_args(argv)
    except ValueError as exc:
        print(str(exc))
        print_help()
        return 1
    if help_requested:
        print_help()
        return 0

    script_dir = Path(__file__).resolve().parent
    data_dir = _data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Installing Cpp-Interviewer skills...")
    print(f"  Source: {script_dir}")
    if agents:
        print(f"  Agents: {', '.join(agents)}")
    if custom_skill_dirs:
        print(f"  Custom skill dirs: {', '.join(str(path) for path in custom_skill_dirs)}")
    print()

    for agent in agents:
        skills_dir = _skill_dir_for_agent(agent)
        install_to_skills_dir(script_dir, skills_dir)
        print(f"  [OK] {agent}: {skills_dir}")
    for skills_dir in custom_skill_dirs:
        install_to_skills_dir(script_dir, skills_dir)
        print(f"  [OK] custom: {skills_dir}")

    print()
    print("Done! Restart your agent, then use interview / coach where slash skills are supported.")
    print()
    print("Usage:")
    print("  /interview 虚函数       # knowledge explanation")
    print("  /coach 虚函数           # interview training (with persistence)")
    print()
    print("SQLite database will be created at:")
    print(f"  {data_dir / 'coach.sqlite'}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in SETUPTOOLS_COMMANDS:
        run_setuptools_setup()
        raise SystemExit(0)
    raise SystemExit(main())
