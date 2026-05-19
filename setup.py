#!/usr/bin/env python3
"""Cpp-Interviewer Skill 安装脚本 — 跨平台，支持 Windows / Linux / macOS"""

import shutil
import sys
from pathlib import Path


def main():
    skills_dir = Path.home() / ".claude" / "skills"
    script_dir = Path(__file__).resolve().parent

    src_interview = script_dir / "skills" / "interview"
    src_coach = script_dir / "skills" / "coach"
    src_coach_pkg = script_dir / "coach"
    src_index = script_dir / "index" / "knowledge_index.json"

    dst_interview = skills_dir / "interview"
    dst_coach = skills_dir / "coach"

    print("Installing Cpp-Interviewer skills...")
    print(f"  Source: {script_dir}")
    print(f"  Target: {skills_dir}")
    print()

    # ── interview skill ──
    if dst_interview.exists():
        shutil.rmtree(dst_interview)
    shutil.copytree(src_interview, dst_interview)
    print("  [OK] interview")

    # 确保索引在 interview/index/ 下
    index_dst = dst_interview / "index" / "knowledge_index.json"
    if not index_dst.exists():
        index_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_index, index_dst)
        print("  [OK] interview/index/knowledge_index.json")

    # ── coach skill ──
    if dst_coach.exists():
        shutil.rmtree(dst_coach)
    shutil.copytree(src_coach, dst_coach)
    print("  [OK] coach (SKILL.md)")

    # 复制 coach Python 包到 coach/coach/
    dst_coach_pkg = dst_coach / "coach"
    if dst_coach_pkg.exists():
        shutil.rmtree(dst_coach_pkg)
    shutil.copytree(src_coach_pkg, dst_coach_pkg)
    print("  [OK] coach/coach/ (Python package)")

    # 复制知识索引到 coach/index/
    coach_index = dst_coach / "index" / "knowledge_index.json"
    coach_index.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_index, coach_index)
    print("  [OK] coach/index/knowledge_index.json")

    # 复制 __main__.py 以便 python -m coach.cli 工作
    main_py = dst_coach_pkg / "__main__.py"
    if not main_py.exists():
        main_py.write_text('from coach.cli import main\nraise SystemExit(main())\n', encoding='utf-8')
        print("  [OK] coach/coach/__main__.py")

    print()
    print("Done! Restart Claude Code, then type / to see interview and coach.")
    print()
    print("Usage:")
    print("  /interview 虚函数       # knowledge explanation")
    print("  /coach 虚函数           # interview training (with persistence)")
    print()
    print("SQLite database will be created at:")
    print(f"  {Path.home() / '.claude' / 'coach' / 'data' / 'coach.sqlite'}")


if __name__ == "__main__":
    main()
