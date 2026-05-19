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
    src_index = script_dir / "index" / "knowledge_index.json"

    dst_interview = skills_dir / "interview"
    dst_coach = skills_dir / "coach"

    print("Installing Cpp-Interviewer skills...")
    print(f"  Source: {script_dir}")
    print(f"  Target: {skills_dir}")
    print()

    # interview
    if dst_interview.exists():
        shutil.rmtree(dst_interview)
    shutil.copytree(src_interview, dst_interview)
    print("  [OK] interview")

    # 确保索引文件在 interview/index/ 下
    index_dst = dst_interview / "index" / "knowledge_index.json"
    if not index_dst.exists():
        index_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_index, index_dst)
        print("  [OK] knowledge_index.json")

    # coach
    if dst_coach.exists():
        shutil.rmtree(dst_coach)
    shutil.copytree(src_coach, dst_coach)
    print("  [OK] coach")

    print()
    print("Done! Restart Claude Code, then type / to see interview and coach.")
    print()
    print("Usage:")
    print("  /interview 虚函数       # knowledge explanation")
    print("  /coach 虚函数           # interview training")


if __name__ == "__main__":
    main()
