# C++ 面试教练 Agent — 设计文档

> 本项目不是对 Cpp-Interviewer Skill 的简单状态增强，而是在其外层新增 Coach Orchestrator。
> 原 Skill 负责 C++ 面试知识生成，Coach Orchestrator 负责训练流程控制、用户状态管理、答题评价、复习调度和进度可视化。

## 1. 定位

| 组件 | 职责 |
|------|------|
| Cpp-Interviewer Skill | 知识引擎：读取 SKILL.md + knowledge_index.json，生成题目和参考答案 |
| Coach Orchestrator | 主控层：状态管理、诊断引擎、训练调度器、评价器 |

## 2. 架构（四层）

```
用户 CLI (cli.py)
     │
     ▼
Coach Orchestrator
  ├── CLI Handler       — 解析 /coach 命令
  ├── Scheduler        — 选题 + 难度调度
  ├── Evaluator        — 结构化评分（6维度）
  └── SkillPromptAdapter — 读取 SKILL.md 当 Prompt Template，调用 LLM
     │
     ▼
State Repository (SQLite)
  ├── user_state
  ├── knowledge_record
  ├── qa_history
  ├── evaluation_detail
  ├── training_session
  └── question_bank
```

## 3. 数据模型（6张表）

### 3.1 user_state

用户全局状态。

```sql
CREATE TABLE user_state (
    user_id TEXT PRIMARY KEY,
    current_mode TEXT DEFAULT 'coach',
    default_style TEXT DEFAULT 'concise',
    default_depth INTEGER DEFAULT 1,
    last_topic TEXT,
    last_session_id INTEGER,
    created_at TEXT,
    updated_at TEXT
);
```

### 3.2 knowledge_record

知识点掌握度追踪。

```sql
CREATE TABLE knowledge_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    topic_id TEXT,
    topic_name TEXT,
    domain TEXT,

    status TEXT DEFAULT 'unvisited',
    mastery_level REAL DEFAULT 0.0,

    right_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    consecutive_right INTEGER DEFAULT 0,
    consecutive_wrong INTEGER DEFAULT 0,

    last_tested_at TEXT,
    next_review_at TEXT,

    difficulty_level INTEGER DEFAULT 1,
    ease_factor REAL DEFAULT 2.5,

    updated_at TEXT,
    UNIQUE(user_id, topic_id)
);
```

关键字段说明：
- `mastery_level`：掌握度 0.0~1.0
- `consecutive_right/wrong`：连续答对/错次数，用于难度调整
- `next_review_at`：到期复习时间
- `ease_factor`：间隔复习系数（参考 SM-2 算法）

### 3.3 qa_history

问答历史。

```sql
CREATE TABLE qa_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    session_id INTEGER,

    topic_id TEXT,
    question_id INTEGER,
    question TEXT,
    user_answer TEXT,
    reference_answer TEXT,

    final_rating TEXT,
    score_total REAL,

    weakness_summary TEXT,
    created_at TEXT
);
```

### 3.4 evaluation_detail

评分维度详情。

```sql
CREATE TABLE evaluation_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qa_id INTEGER,

    correctness REAL,
    completeness REAL,
    depth REAL,
    clarity REAL,
    code_accuracy REAL,
    edge_case_awareness REAL,

    missing_points TEXT,
    wrong_points TEXT,
    hallucinated_points TEXT,

    weakness_tags TEXT,
    evaluator_confidence REAL,

    created_at TEXT
);
```

字段说明：
- `weakness_tags`：精准标签，如 `["vtable", "vptr", "dynamic_dispatch"]`，供调度器精准选题
- `evaluator_confidence`：评价置信度，低于阈值时减少掌握度更新幅度

### 3.5 training_session

训练会话。

```sql
CREATE TABLE training_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    mode TEXT,
    target_domain TEXT,
    start_time TEXT,
    end_time TEXT,
    total_questions INTEGER DEFAULT 0,
    average_score REAL DEFAULT 0.0,
    summary TEXT
);
```

### 3.6 question_bank

题目缓存。

```sql
CREATE TABLE question_bank (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT,
    difficulty INTEGER,
    question_type TEXT,
    question TEXT,
    reference_answer TEXT,
    key_points TEXT,
    followups TEXT,
    source TEXT,

    skill_version TEXT,
    generator_version TEXT,
    created_from_context TEXT,

    created_at TEXT
);
```

关键字段说明：
- `skill_version`：生成题目时引用的 Skill 版本，便于后续淘汰旧题
- `created_from_context`：生成的上下文（topic/difficulty/user_level），便于复盘

## 4. Skill 文件结构

```
skills/interview/
├── SKILL.md           # 保留 /interview 单次问答模式
├── COACH_SKILL.md      # 新增，被 Coach Agent 调用（被动模式）
└── shared_rules.md     # 公共 C++ 面试官规则（两模式共用）
```

注意：`/coach` 模式下 Skill 不主动询问风格/深度，只接收参数输出内容。

## 5. Evaluator 结构化输出

Evaluator 输出必须通过 JSON Schema 校验。如果解析失败，自动触发一次修复重试。

```json
{
  "rating": "good|okay|poor",
  "score_total": 0.0,
  "correctness": 0.0,
  "completeness": 0.0,
  "depth": 0.0,
  "clarity": 0.0,
  "code_accuracy": 0.0,
  "edge_case_awareness": 0.0,
  "missing_points": [],
  "wrong_points": [],
  "weakness_tags": [],
  "evaluator_confidence": 0.0
}
```

六维度评分说明：

| 维度 | 含义 |
|------|------|
| correctness | 概念是否正确 |
| completeness | 是否覆盖关键点 |
| depth | 是否讲到底层机制 |
| clarity | 表达是否像面试回答 |
| code_accuracy | 代码是否正确 |
| edge_case_awareness | 是否知道边界情况 |

## 6. Scheduler 选题公式

```
candidate_score =
  0.40 * weakness_score
+ 0.25 * due_review_score
+ 0.20 * interview_frequency_score
+ 0.10 * difficulty_match_score
- 0.05 * recent_repetition_penalty
```

| 因子 | 作用 |
|------|------|
| weakness_score | 优先训练薄弱知识点（基于 mastery_level） |
| due_review_score | 到期复习优先（基于 next_review_at） |
| interview_frequency_score | 高频面试点优先（来自 knowledge_index.json） |
| difficulty_match_score | 匹配用户当前难度 |
| recent_repetition_penalty | 避免连续刷同一题 |

## 7. 掌握度更新策略

保守更新，避免单次误判大幅波动：

```python
delta = 0.12 * (score_total - 0.6)

if evaluator_confidence < 0.7:
    delta *= 0.5

mastery_level = clamp(old_mastery + delta, 0.0, 1.0)
```

- `0.6` 为及格线
- 高于 0.6 才提高掌握度，低于才降低
- 评价信心低时减少更新幅度

## 8. 隐式评价机制

- 训练过程**不打断用户**
- 每题**极简反馈**：`评价：基本正确，但底层细节不足。下一题继续追问 vtable。`
- 详细评价通过 `/coach review` 查看
- 所有评价写入数据库，用户可随时查询

## 9. CLI 命令

| 命令 | 功能 |
|------|------|
| `/coach start` | 进入训练模式 |
| `/coach topic <topic>` | 指定专题训练 |
| `/coach weak` | 自动训练薄弱点 |
| `/coach due` | 只训练到期复习的知识点 |
| `/coach status` | 查看掌握度仪表盘 |
| `/coach review` | 查看最近评价详情 |
| `/coach plan` | 生成今日训练计划 |
| `/coach reset` | 重置状态 |
| `/coach export` | 导出训练记录 |

## 10. 目录结构

```
Cpp-Interviewer/
├── skills/
│   └── interview/
│       ├── SKILL.md           # 保留 /interview 模式
│       ├── COACH_SKILL.md     # 新增，coach 被动模式
│       └── shared_rules.md    # 公共面试规则
├── index/
│   └── knowledge_index.json   # 现有，不动
├── coach/
│   ├── __init__.py
│   ├── config.py             # 默认参数
│   ├── models.py             # 数据结构
│   ├── db.py                 # SQLite 读写
│   ├── llm.py                # LLMClient / MockLLMClient / OpenAICompatibleClient
│   ├── skill_adapter.py      # SkillPromptAdapter
│   ├── scheduler.py          # 选题 + 难度调度
│   ├── evaluator.py          # 结构化评分
│   └── cli.py                # CLI 入口
├── tests/
│   ├── test_db.py
│   ├── test_scheduler.py
│   ├── test_evaluator.py
│   └── test_skill_adapter.py
└── data/
    └── coach.sqlite           # 状态存储
```