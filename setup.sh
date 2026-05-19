#!/bin/bash
# Cpp-Interviewer Skill 安装脚本
# 将 interview 和 coach 技能安装到 ~/.claude/skills/

set -e

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing Cpp-Interviewer skills..."

# 创建目标目录
mkdir -p "$SKILLS_DIR/interview" "$SKILLS_DIR/coach"

# 复制 interview 技能
cp -r "$SCRIPT_DIR/skills/interview/"* "$SKILLS_DIR/interview/"
echo "  ✓ interview skill installed"

# 复制 coach 技能
cp -r "$SCRIPT_DIR/skills/coach/"* "$SKILLS_DIR/coach/"
echo "  ✓ coach skill installed"

# 复制索引文件（如果 interview 目录下没有的话）
if [ ! -f "$SKILLS_DIR/interview/index/knowledge_index.json" ]; then
    mkdir -p "$SKILLS_DIR/interview/index"
    cp "$SCRIPT_DIR/index/knowledge_index.json" "$SKILLS_DIR/interview/index/"
    echo "  ✓ knowledge index installed"
fi

echo ""
echo "Done! Restart Claude Code to use /interview and /coach"
echo ""
echo "Usage:"
echo "  /interview 虚函数       # 知识讲解"
echo "  /coach 虚函数           # 面试训练"
