---
name: coach
description: C++ 面试教练 Agent — 弱项驱动训练、精准诊断、系统化复习
argument-hint: "[start] 或 [topic <专题>] 或 [weak] 或 [due] 或 [status] 或 [plan]"
---

# C++ 面试教练 Agent

你的 C++ 面试学习伙伴，基于弱项驱动训练和精准诊断，高效提升面试水平。

## 命令

| 命令 | 功能 |
|------|------|
| `/coach start` | 进入训练模式，探测水平后循环训练 |
| `/coach topic <topic>` | 指定专题训练，如 `/coach topic 虚函数` |
| `/coach weak` | 从薄弱知识点列表依次训练 |
| `/coach due` | 只训练到期需要复习的知识点 |
| `/coach status` | 查看掌握度仪表盘 |
| `/coach plan` | 生成今日训练计划 |

## 工作原理

```
用户输入 /coach 命令
       │
       ▼
Coach Orchestrator (Python CLI)
  ├── 加载用户历史状态（SQLite）
  ├── Scheduler 按 candidate_score 公式选题
  ├── SkillPromptAdapter 生成题目（读 COACH_SKILL.md）
  ├── 用户回答
  ├── Evaluator 六维度评分
  ├── 更新掌握度 + 写入历史
  └── 输出极简反馈
```

### 调度器公式

```
candidate_score =
  0.40 × weakness_score
+ 0.25 × due_review_score
+ 0.20 × interview_frequency_score
+ 0.10 × difficulty_match_score
- 0.05 × recent_repetition_penalty
```

### 六维度评价

| 维度 | 含义 |
|------|------|
| correctness | 概念是否正确 |
| completeness | 是否覆盖关键点 |
| depth | 是否讲到底层机制 |
| clarity | 表达是否清晰 |
| code_accuracy | 代码是否正确 |
| edge_case_awareness | 是否知道边界情况 |

## 使用方式

在 Claude Code 对话中直接输入 `/coach <command>`，例如：

- `/coach start` — 开始训练
- `/coach topic 虚函数` — 训练虚函数专题
- `/coach weak` — 训练薄弱知识点
- `/coach status` — 查看掌握度

## 技术栈

- Python 3.10+
- SQLite（状态持久化）
- LLM：MockLLMClient（默认）/ OpenAI Compatible API（可选，需要设置 OPENAI_API_KEY）

## 当前限制

- `/coach reset` 和 `/coach export` 尚未实现