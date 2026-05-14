<div align="center">

# Cpp-Interviewer

**C++ 面试学习伙伴 — 弱项驱动训练、精准诊断、系统化复习**

**C++ Interview Preparation — Weakness-Driven Training & Systematic Review**

[中文](#中文) | [English](#english)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code-lightgrey.svg)
![Branch](https://img.shields.io/badge/branch-coach--agent-orange.svg)

</div>

---

<a id="中文"></a>

## 中文

### 简介

模拟面试官角色，帮助你理解和掌握 C++ 面试中的核心知识点。不是直接给答案，而是引导你思考、追问细节、指出常见误区。

**coach-agent 分支新增：** 系统化训练模式 `C++ 面试教练 Agent`，支持弱项驱动训练、六维度精准诊断、SQLite 状态持久化。

### 两种模式

#### 模式一：/interview — 面试八股讲解

```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
```

#### 模式二：/coach — 弱项驱动训练（新增）

```
/coach start     # 进入训练循环
/coach topic 虚函数  # 指定专题训练
/coach weak      # 训练薄弱知识点
/coach status     # 查看掌握度仪表盘
/coach plan       # 生成今日训练计划
```

### 核心特性

- **面试官视角**：引导思考、追问细节、指出误区，而非直接给答案
- **弱项驱动训练**：Scheduler candidate_score 公式自动优先训练最薄弱知识点
- **六维度精准诊断**：correctness、completeness、depth、clarity、code_accuracy、edge_case_awareness
- **三级深度扩展**：
    - Level 1 — 只讲当前知识点，讲透讲明白
    - Level 2 — 同方向扩展（如 C++ 语言范围内扩展）
    - Level 3 — 跨学科扩展（包含 Level 2 全部内容 + 横向扩展到操作系统、计算机网络等）
- **回答风格可选**：简洁模式（快速复习）/ 详细模式（深入学习），随时可切换
- **难度递进追问**：每个问题结束后给出 3-5 个高频面试追问，从基础到深入排列
- **知识点索引系统**：通过 `index/knowledge_index.json` 快速定位知识来源
- **SQLite 状态持久化**：掌握度、QA 历史、复习计划自动存储

### 技术架构

```
用户 CLI → Coach Orchestrator → SkillPromptAdapter → SQLite
                      ↓
              ┌──────────────┐
              │ Scheduler    │  candidate_score 公式
              │ Evaluator    │  六维度评分
              │ SkillAdapter │  知识引擎
              └──────────────┘
```

### 仓库结构

```
.
├── bin/                      # 可选 launcher 脚本
│   ├── coach                # Linux/macOS
│   └── coach.bat            # Windows
├── coach/                    # 教练 Agent（Python CLI）
│   ├── cli.py               # CLI 入口
│   ├── db.py                # SQLite 状态层（6 表）
│   ├── scheduler.py         # 选题调度器
│   ├── evaluator.py         # 六维度评价器
│   ├── skill_adapter.py     # 知识引擎适配器
│   └── prompts.py           # Prompt 模板
├── skills/
│   ├── coach/SKILL.md       # /coach 命令入口
│   └── interview/
│       ├── SKILL.md         # /interview 模式
│       ├── COACH_SKILL.md   # coach 被动模式
│       └── shared_rules.md  # 公共面试规则
├── index/
│   └── knowledge_index.json # 知识点索引（60+ 知识点）
├── data/
│   └── coach.sqlite         # 状态存储（运行时生成）
└── tests/                    # 单元测试
```

### 快速开始

### 推荐方式一：Claude Code Skill（直接对话）

安装 Skill 后，在 Claude Code 中直接输入：

```text
/coach status              # 查看掌握度仪表盘
/coach topic 虚函数         # 指定专题训练
/coach weak                # 训练薄弱知识点
/coach due                 # 训练到期复习的知识点
/coach plan                # 生成今日训练计划
/coach start               # 进入完整训练循环
```

### 推荐方式二：终端命令（pip 安装）

```bash
pip install -e .
coach status              # 查看掌握度仪表盘
coach topic 虚函数         # 指定专题训练
coach weak                # 训练薄弱知识点
coach due                 # 训练到期复习的知识点
coach plan                # 生成今日训练计划
```

不安装也可使用 launcher 脚本：

```bash
./bin/coach status
./bin/coach topic 虚函数
```

### 开发调试方式

```bash
python -m coach.cli status
python -m coach.cli topic 虚函数
```

### /interview 模式

```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
```

### 安装方式

#### 方式一：克隆仓库（推荐）

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
cd ~/.claude/skills/Cpp-Interviewer
git checkout coach-agent   # 切换到 coach-agent 分支
```

#### 方式二：下载使用

下载仓库代码后解压，将文件夹放置到 `~/.claude/skills/` 目录下。

### 注意事项

- 本项目**无需 PDF 资料即可使用**，默认基于内置知识点索引和模型知识生成回答。
- `books/` 目录为可选资料库，未下载或解析失败时不影响核心功能。
- `/coach reset` 和 `/coach export` 尚未实现
- 真实 LLM 接入需要设置 `OPENAI_API_KEY` 环境变量

### 可选：启用本地 PDF 资料库

如需使用完整本地资料库，需额外安装 Git LFS：

```bash
git lfs install
git lfs pull
```

部分 PDF 可能存在加密或格式兼容问题；解析失败时系统会自动跳过并使用其他来源补充。

### 开源许可

本项目采用 [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE) 开源。

### 社区

- 交流群：Q 828570482
- 已获 [LINUX DO](https://linux.do/) 社区认可

---

<a id="english"></a>

## English

### Introduction

Simulates an interviewer to help you understand and master core C++ interview topics. Instead of giving direct answers, it guides your thinking, asks follow-up questions, and highlights common pitfalls.

**coach-agent branch adds:** Systematic training mode `C++ Interview Coach Agent` with weakness-driven training, six-dimension precise diagnosis, and SQLite state persistence.

### Two Modes

#### Mode 1: /interview — Interview Q&A Coaching

```
/interview How are virtual functions implemented
/interview What types of smart pointers are there
/interview What is a memory leak
```

#### Mode 2: /coach — Weakness-Driven Training (New)

```
/coach start     # Enter training loop
/coach topic virtual_function  # Train specific topic
/coach weak      # Train weak topics
/coach status    # View mastery dashboard
/coach plan      # Generate today's training plan
```

### Core Features

- **Interviewer perspective**: Guides thinking, asks follow-up questions, highlights pitfalls — no direct answers
- **Weakness-driven training**: Scheduler candidate_score formula automatically prioritizes weakest topics
- **Six-dimension precise diagnosis**: correctness, completeness, depth, clarity, code_accuracy, edge_case_awareness
- **Three-level depth expansion**:
    - Level 1 — Explain the current topic thoroughly
    - Level 2 — Expand within the same domain (e.g., more C++ topics)
    - Level 3 — Cross-domain expansion (includes Level 2 + OS, networking, etc.)
- **Selectable answer style**: Concise mode (quick review) / Detailed mode (deep learning), switchable anytime
- **Progressive difficulty follow-ups**: 3-5 high-frequency interview follow-up questions after each answer, sorted from basic to advanced
- **Knowledge index system**: Quickly locate knowledge sources via `index/knowledge_index.json`
- **SQLite state persistence**: Mastery, QA history, and review schedule automatically stored

### Architecture

```
User CLI → Coach Orchestrator → SkillPromptAdapter → SQLite
                      ↓
              ┌──────────────┐
              │ Scheduler    │  candidate_score formula
              │ Evaluator    │  6-dimension scoring
              │ SkillAdapter │  Knowledge engine
              └──────────────┘
```

### Repository Structure

```
.
├── bin/                      # Optional launcher scripts
│   ├── coach                # Linux/macOS
│   └── coach.bat            # Windows
├── coach/                    # Coach Agent (Python CLI)
│   ├── cli.py               # CLI entry
│   ├── db.py                # SQLite state layer (6 tables)
│   ├── scheduler.py         # Topic scheduler
│   ├── evaluator.py         # 6-dimension evaluator
│   ├── skill_adapter.py     # Knowledge engine adapter
│   └── prompts.py           # Prompt templates
├── skills/
│   ├── coach/SKILL.md       # /coach command entry
│   └── interview/
│       ├── SKILL.md         # /interview mode
│       ├── COACH_SKILL.md   # Coach passive mode
│       └── shared_rules.md  # Common interview rules
├── index/
│   └── knowledge_index.json # Knowledge index (60+ topics)
├── data/
│   └── coach.sqlite         # State storage (generated at runtime)
└── tests/                    # Unit tests
```

### Quick Start

### Recommended Option 1: Claude Code Skill (Direct Conversation)

After installing the Skill, directly input in Claude Code:

```text
/coach status              # View mastery dashboard
/coach topic virtual_function  # Train specific topic
/coach weak                # Train weak topics
/coach due                 # Train due review topics
/coach plan                # Generate today's training plan
/coach start               # Enter full training loop
```

### Recommended Option 2: Terminal Command (pip install)

```bash
pip install -e .
coach status              # View mastery dashboard
coach topic virtual_function  # Train specific topic
coach weak                # Train weak topics
coach due                 # Train due review topics
coach plan                # Generate today's training plan
```

Without pip install, you can also use the launcher script:

```bash
./bin/coach status
./bin/coach topic virtual_function
```

### Development/Debug Mode

```bash
python -m coach.cli status
python -m coach.cli topic virtual_function
```

### /interview Mode

```
/interview How are virtual functions implemented
/interview What types of smart pointers are there
```

### Installation

#### Option 1: Clone Repository (Recommended)

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
cd ~/.claude/skills/Cpp-Interviewer
git checkout coach-agent   # Switch to coach-agent branch
```

#### Option 2: Download

Download and extract the repository, then place the folder under `~/.claude/skills/`.

### Notes

- This project **works without PDF resources**; default responses are based on the built-in knowledge index and model knowledge.
- `books/` is an optional resource library; missing or failed parsing does not affect core functionality.
- `/coach reset` and `/coach export` are not yet implemented.
- Real LLM integration requires setting `OPENAI_API_KEY` environment variable.

### Optional: Enable Local PDF Resource Library

To use the full local resource library, install Git LFS additionally:

```bash
git lfs install
git lfs pull
```

Some PDFs may have encryption or compatibility issues; failed parsing will be skipped and supplemented from other sources.

### License

This project is licensed under the [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE).

### Community

- Discussion group: Q 828570482
- Recognized by [LINUX DO](https://linux.do/) community