# C++ 面试教练 Agent

> 你的 C++ 面试学习伙伴 — 弱项驱动训练、精准诊断、系统化复习

## 命令

### `/coach start`
进入训练模式。先出一道引导题探测你的水平，然后你可以自由输入 topic 进行训练。

### `/coach topic <topic>`
指定专题训练。例如：`/coach topic 虚函数`

### `/coach weak`
从你的薄弱知识点列表依次训练（优先训练 mastery_level 最低的 topic）。

### `/coach due`
只训练到期需要复习的知识点（根据 next_review_at 筛选）。

### `/coach status`
查看你的掌握度仪表盘：总知识点数、已掌握数、薄弱数、平均掌握度。

### `/coach plan`
生成今日训练计划，列出最需要加强的薄弱点。

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

### 掌握度更新

```
delta = 0.12 × (score_total - 0.6)
（低于 0.6 及格线时降低，高于时提高；低置信度评价时减少更新幅度）
```

## 技术栈

- Python 3.10+
- SQLite（状态持久化）
- LLM：MockLLMClient（默认）/ OpenAI Compatible API（可选）

## 使用限制

- `/coach reset` 和 `/coach export` 尚未实现
- 真实 LLM 接入需要设置 `OPENAI_API_KEY` 环境变量

## 文件结构

```
coach/
├── config.py      # 配置常量
├── models.py      # 数据类
├── db.py           # SQLite 状态层
├── llm.py          # LLMClient / MockLLMClient / OpenAICompatibleClient
├── skill_adapter.py # SkillPromptAdapter
├── scheduler.py    # 选题调度器
├── evaluator.py    # 六维度评价器
└── cli.py          # CLI 入口
```