# Cpp-Interviewer Skill 安装脚本 (Windows)
# 将 interview 和 coach 技能安装到 ~/.claude/skills/

$ErrorActionPreference = "Stop"
$SkillsDir = "$env:USERPROFILE\.claude\skills"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Installing Cpp-Interviewer skills..." -ForegroundColor Cyan

# 创建目标目录
New-Item -ItemType Directory -Force -Path "$SkillsDir\interview" | Out-Null
New-Item -ItemType Directory -Force -Path "$SkillsDir\coach" | Out-Null

# 复制 interview 技能
Copy-Item -Recurse -Force "$ScriptDir\skills\interview\*" "$SkillsDir\interview\"
Write-Host "  ✓ interview skill installed" -ForegroundColor Green

# 复制 coach 技能
Copy-Item -Recurse -Force "$ScriptDir\skills\coach\*" "$SkillsDir\coach\"
Write-Host "  ✓ coach skill installed" -ForegroundColor Green

# 复制索引文件
if (-not (Test-Path "$SkillsDir\interview\index\knowledge_index.json")) {
    New-Item -ItemType Directory -Force -Path "$SkillsDir\interview\index" | Out-Null
    Copy-Item -Force "$ScriptDir\index\knowledge_index.json" "$SkillsDir\interview\index\"
    Write-Host "  ✓ knowledge index installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done! Restart Claude Code to use /interview and /coach" -ForegroundColor Yellow
Write-Host ""
Write-Host "Usage:"
Write-Host "  /interview 虚函数       # 知识讲解"
Write-Host "  /coach 虚函数           # 面试训练"
