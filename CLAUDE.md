# C++ 面试教练 Agent

> 你的 C++ 面试学习伙伴 — 弱项驱动训练、精准诊断、系统化复习

## Agent Skills 结构

核心 skill 是 agent-neutral 的 `skills/cpp-interviewer/SKILL.md`：

- `skills/cpp-interviewer/references/interview-mode.md`：讲解模式
- `skills/cpp-interviewer/references/coach-mode.md`：训练模式
- `skills/cpp-interviewer/references/knowledge-schema.md`：知识索引 schema

`skills/interview/SKILL.md` 和 `skills/coach/SKILL.md` 是 slash command 兼容入口。后续优化核心行为时优先修改 `skills/cpp-interviewer/`，入口文件只保留轻量转发规则。

## 快速开始

```bash
# 训练薄弱知识点
python -m coach.cli weak

# 指定专题训练
python -m coach.cli topic 虚函数

# 查看掌握度
python -m coach.cli status

# 生成今日计划
python -m coach.cli plan

# 搜索知识点
python -m coach.cli topic search 虚函数 --json
```

## 命令

| 命令 | 功能 |
|------|------|
| `/coach start` | 进入训练模式，探测水平后循环训练 |
| `/coach topic <topic>` | 指定专题训练，如 `/coach topic 虚函数` |
| `/coach weak` | 从薄弱知识点列表依次训练 |
| `/coach due` | 只训练到期需要复习的知识点 |
| `/coach status` | 查看掌握度仪表盘 |
| `/coach plan` | 生成今日训练计划 |

## 可移植路径

状态和索引路径优先使用：

| 环境变量 | 用途 |
|---------|------|
| `CPP_INTERVIEWER_HOME` | 用户数据目录，默认 `~/.cpp-interviewer` |
| `CPP_INTERVIEWER_DB` | SQLite 数据库路径 |
| `CPP_INTERVIEWER_INDEX` | `knowledge_index.json` 路径 |

## 核心特性

### 弱项驱动训练

根据 Scheduler candidate_score 公式自动优先训练最薄弱的知识点：

```
candidate_score =
  0.40 × weakness_score      # 薄弱度
+ 0.25 × due_review_score   # 到期复习
+ 0.20 × interview_frequency_score  # 面试频率
+ 0.10 × difficulty_match_score     # 难度匹配
- 0.05 × recent_repetition_penalty   # 重复惩罚
```

### 六维度精准诊断

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
- LLM：当前 agent 自身（Claude Code / Cursor 等），无需 API Key

## 项目结构

```
Cpp-Interviewer/
├── skills/
│   ├── cpp-interviewer/     # agent-neutral 核心 skill
│   ├── coach/
│   │   ├── SKILL.md         # /coach 命令入口
│   │   ├── coach/           # Python 持久化后端
│   │   └── index/
│   └── interview/
│       ├── SKILL.md         # /interview 模式
│       ├── COACH_SKILL.md   # coach 被动模式
│       └── shared_rules.md  # 公共面试规则
└── setup.py                 # 多 Agent 安装入口
```

## 使用限制

- `/coach reset` 和 `/coach export` 尚未实现
