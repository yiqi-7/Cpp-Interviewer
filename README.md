<div align="center">

# Cpp-Interviewer

**C++ 面试学习伙伴 — 学 + 练，双模式覆盖**

[中文](#中文) | [English](#english)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code-lightgrey.svg)

</div>

---

<a id="中文"></a>

## 中文

### 简介

模拟面试官角色，帮助你准备 C++ 面试。

- **不是直接给答案**，而是引导你思考、追问细节、指出常见误区
- **无需 PDF 资料**，无需安装 Git LFS，下载后直接使用
- **两种模式**，学练结合

### 两种模式

| 入口 | 作用 | 示例 |
|------|------|------|
| `/interview` | 知识讲解 | `/interview 虚函数是怎么实现的` |
| `/coach` | 面试训练 | `/coach 虚函数`、`/coach weak` |

```
/interview = 教学讲解（学）
/coach = 面试训练（练）
```

### 使用方式

#### 讲解模式（/interview）

```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
```

#### 训练模式（/coach）

```
/coach 虚函数          # 专项训练：虚函数
/coach 智能指针         # 专项训练：智能指针
/coach weak            # 训练薄弱知识点
/coach status          # 查看掌握度仪表盘
/coach plan            # 生成今日训练计划
/coach start           # 进入训练循环
```

`/coach` 会像面试官一样：**出题 → 等你回答 → 评价 → 追问 → 下一题**。

### 核心特性

- **面试官视角**：引导思考，不直接给答案
- **弱项驱动训练**：自动优先训练最薄弱知识点
- **六维度精准诊断**：correctness、completeness、depth、clarity、code_accuracy、edge_case_awareness
- **追问式训练**：根据你的回答持续追问，挖掘薄弱点
- **SQLite 状态持久化**：掌握度、QA 历史自动存储

### 安装方式

#### 方式一：克隆仓库（推荐）

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
cd ~/.claude/skills/Cpp-Interviewer
git checkout coach-agent
```

#### 方式二：下载使用

下载仓库代码后解压，将文件夹放置到 `~/.claude/skills/` 目录下。

### 注意事项

- **无需 PDF 资料即可使用**，默认基于内置知识点索引和模型知识生成回答
- `/coach reset` 和 `/coach export` 尚未实现
- 真实 LLM 接入需要设置 `OPENAI_API_KEY` 环境变量

### 开发者调试方式

```bash
pip install -e .
python -m pytest tests/ -v
python -m coach.cli status
python -m coach.cli topic 虚函数
```

### 开源许可

本项目采用 [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE) 开源。

### 社区

- 交流群：Q 828570482
- 已获 [LINUX DO](https://linux.do/) 社区认可

---

<a id="english"></a>

## English

### Introduction

Simulates an interviewer to help you prepare for C++ interviews.

- **No direct answers** — guides your thinking, asks follow-up questions, highlights pitfalls
- **No PDF required** — works out of the box with built-in knowledge index
- **Two modes** — learn + practice

### Two Modes

| Entry | Purpose | Example |
|-------|---------|---------|
| `/interview` | Teaching | `/interview How are virtual functions implemented` |
| `/coach` | Training | `/coach virtual_function`, `/coach weak` |

```
/interview = teaching (learn)
/coach = interview training (practice)
```

### Usage

#### Teaching Mode (/interview)

```
/interview How are virtual functions implemented
/interview What types of smart pointers are there
/interview What is a memory leak
```

#### Training Mode (/coach)

```
/coach virtual_function    # Train specific topic
/coach smart_pointer       # Train specific topic
/coach weak               # Train weak topics
/coach status             # View mastery dashboard
/coach plan               # Generate today's training plan
/coach start              # Enter training loop
```

`/coach` acts like an interviewer: **ask → wait for your answer → evaluate → follow-up → next question**.

### Core Features

- **Interviewer perspective**: Guides thinking, no direct answers
- **Weakness-driven training**: Automatically prioritizes weakest topics
- **Six-dimension precise diagnosis**: correctness, completeness, depth, clarity, code_accuracy, edge_case_awareness
- **Follow-up based training**: Continues questioning based on your answers to dig out weak points
- **SQLite state persistence**: Mastery, QA history automatically stored

### Installation

#### Option 1: Clone Repository (Recommended)

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
cd ~/.claude/skills/Cpp-Interviewer
git checkout coach-agent
```

#### Option 2: Download

Download and extract the repository, then place the folder under `~/.claude/skills/`.

### Notes

- **Works without PDF resources** — default responses based on built-in knowledge index and model knowledge
- `/coach reset` and `/coach export` are not yet implemented
- Real LLM integration requires setting `OPENAI_API_KEY` environment variable

### Developer / Debug Mode

```bash
pip install -e .
python -m pytest tests/ -v
python -m coach.cli status
python -m coach.cli topic virtual_function
```

### License

This project is licensed under the [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE).

### Community

- Discussion group: Q 828570482
- Recognized by [LINUX DO](https://linux.do/) community