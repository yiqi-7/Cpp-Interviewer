[English](README_EN.md) | [中文](#)

# C++ 面试教练 Agent

你的 C++ 面试学习伙伴，支持两种工作模式：

## 两种模式

### 模式一：/interview — 面试八股讲解

模拟面试官角色，针对问题进行引导式教学。

```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
```

**特性：**
- 面试官视角：引导思考，不直接给答案
- 三级深度扩展（Level 1-3）
- 风格可切换（简洁/详细）
- 高频追问（每题 3-5 个，从基础到深入）

### 模式二：/coach — 弱项驱动训练

系统化训练模式，精准诊断薄弱点。

```
/coach start     # 进入训练循环
/coach topic 虚函数  # 指定专题训练
/coach weak      # 训练薄弱知识点
/coach status     # 查看掌握度仪表盘
/coach plan       # 生成今日训练计划
```

**特性：**
- 六维度精准诊断（correctness, completeness, depth, clarity, code_accuracy, edge_case_awareness）
- 弱项优先调度（Scheduler candidate_score 公式）
- SQLite 状态持久化（掌握度、QA 历史、复习计划）
- 隐式评价机制（不打断训练，极简反馈）

## 技术架构

```
用户 CLI → Coach Orchestrator → SkillPromptAdapter → SQLite
                      ↓
              ┌──────────────┐
              │ Scheduler    │  选题公式
              │ Evaluator    │  六维度评分
              │ SkillAdapter │  知识引擎
              └──────────────┘
```

## 仓库结构

```
Cpp-Interviewer/
├── coach/                    # 教练 Agent（Python CLI）
│   ├── cli.py               # CLI 入口
│   ├── db.py                # SQLite 状态层（6 表）
│   ├── scheduler.py         # 选题调度器
│   ├── evaluator.py         # 六维度评价器
│   └── skill_adapter.py     # 知识引擎适配器
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

## 快速开始

```bash
# 查看掌握度
python -m coach.cli status

# 开始训练薄弱点
python -m coach.cli weak

# 指定专题训练
python -m coach.cli topic 虚函数

# 生成今日计划
python -m coach.cli plan
```

## 安装方式

### 方式一：克隆仓库

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
# 告诉本地 CLI 安装 skill：https://github.com/yiqi-7/Cpp-Interviewer.git
```

### 方式二：下载使用

下载仓库代码后解压，将文件夹放置到 `~/.claude/skills/` 目录下。

## 注意事项

- PDF 书籍使用 Git LFS 管理，克隆时需要安装 [Git LFS](https://git-lfs.github.com/)
- 八股文 PDF 为加密文件，Skill 通过内容解析读取，部分格式可能不完整
- `/coach reset` 和 `/coach export` 尚未实现

## 开源许可

本项目采用 [MIT License](LICENSE) 开源。

## 交流群

Q:828570482