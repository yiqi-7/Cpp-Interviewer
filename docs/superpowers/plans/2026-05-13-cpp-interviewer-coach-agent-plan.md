# C++ 面试教练 Agent — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建 C++ 面试教练 Agent（MVP 闭环：/coach start → 出题 → 评价 → 写入 SQLite → 下一题）

**Architecture:** 四层架构（CLI → Coach Orchestrator → SkillPromptAdapter → SQLite State Repository），Skill 降级为知识引擎，被动接收参数输出内容；主控层负责状态、评价、调度。

**Tech Stack:** Python 3.10+, SQLite, LLM API (OpenAI compatible)

---

## 文件结构

```
Cpp-Interviewer/
├── skills/interview/
│   ├── SKILL.md              # 已有，保持不动
│   ├── COACH_SKILL.md        # 新增，coach 被动模式
│   └── shared_rules.md        # 新增，公共面试规则
├── index/knowledge_index.json # 已有，保持不动
├── coach/
│   ├── __init__.py
│   ├── config.py             # 默认参数、Schema 常量
│   ├── models.py             # 数据类（EvaluationResult, TrainingContext 等）
│   ├── db.py                 # SQLite 初始化 + CRUD
│   ├── skill_adapter.py      # SkillPromptAdapter：读取 SKILL.md + index，调 LLM
│   ├── scheduler.py          # 选题公式计算
│   ├── evaluator.py          # 六维度评分 + JSON Schema 校验
│   ├── prompts.py            # Evaluator 出题/评价 prompt
│   └── cli.py                # CLI 命令入口
├── tests/
│   ├── __init__.py
│   ├── test_db.py
│   ├── test_scheduler.py
│   ├── test_evaluator.py
│   └── test_skill_adapter.py
└── data/coach.sqlite          # 运行时生成
```

---

## Task 1: 项目骨架 + config.py

**Files:**
- Create: `coach/__init__.py`
- Create: `coach/config.py`
- Create: `tests/__init__.py`

---

## Task 2: 数据模型 models.py

**Files:**
- Create: `coach/models.py`

---

## Task 3: SQLite 状态层 db.py

**Files:**
- Create: `coach/db.py`
- Create: `tests/test_db.py`

---

## Task 4: SkillPromptAdapter + MockLLMClient

**Files:**
- Create: `coach/skill_adapter.py`
- Create: `coach/prompts.py`
- Create: `tests/test_skill_adapter.py`

---

## Task 5: Scheduler 选题逻辑

**Files:**
- Create: `coach/scheduler.py`
- Create: `tests/test_scheduler.py`

---

## Task 6: Evaluator 六维度评分 + JSON Schema 校验

**Files:**
- Create: `coach/evaluator.py`
- Create: `tests/test_evaluator.py`

---

## Task 7: CLI MVP 闭环

**Files:**
- Create: `coach/cli.py`
- Modify: `coach/skill_adapter.py`（添加 generate_evaluation_prompt 方法）

---

## Task 8: 补全 Skill 文件

**Files:**
- Create: `skills/interview/COACH_SKILL.md`
- Create: `skills/interview/shared_rules.md`

---

## Task 9: 接真实 LLM（OpenAI Compatible）

**Files:**
- Modify: `coach/skill_adapter.py`（新增 OpenAICompatibleClient）

---

## Task 10: 修复 SKILL.md YAML 格式

**Files:**
- Modify: `skills/interview/SKILL.md`

---

## 快速验证命令

```bash
# 运行所有测试
python -m pytest tests/ -v

# 手动跑 CLI
python -m coach.cli start
python -m coach.cli status
python -m coach.cli weak
```

---

**Plan complete.**