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

#### 训练模式交互示例

**专项训练 `/coach 虚函数`**

```
你：/coach 虚函数

教练：专项训练：vtable
      掌握度：2.4%
      难度：基础

      第 1 题：
      什么是虚函数表（vtable）？每个包含虚函数的类和它的对象分别与 vtable 是什么关系？

你：虚函数表是一个函数指针数组，编译器为每个含虚函数的类生成一张表。类共享一张 vtable，对象通过 vptr 指向它。

教练：评价：概念基本正确，但遗漏了 vptr 的存储位置和继承场景下的表合并规则。
      薄弱点：vptr 布局、多重继承
      掌握度更新：2.4% → 12%

      第 2 题：
      多重继承下，一个对象会有几个 vptr？编译器如何决定调用哪个虚函数？
```

**薄弱训练 `/coach weak`**

```
你：/coach weak

教练：当前薄弱点：vtable（掌握度 12%）
      开始训练...

      第 1 题：
      虚析构函数的作用是什么？如果基类析构函数不是虚函数，delete 派生类指针会发生什么？
```

**掌握度仪表盘 `/coach status`**

```
你：/coach status

教练：📊 掌握度仪表盘
      ──────────────────────────
      总知识点：15    已掌握：2
      薄弱：8       平均掌握度：23%
      ──────────────────────────
      ▓▓▓░░░░░░░  虚函数       35%
      ▓▓░░░░░░░░  智能指针     20%
      ▓░░░░░░░░░  vtable       12%
      ░░░░░░░░░░  内存管理      5%
      ...
```

**今日计划 `/coach plan`**

```
你：/coach plan

教练：📋 今日训练计划
      ──────────────────────────
      复习（到期）：
        1. vtable — 上次训练 3 天前，建议复习
      新增（薄弱）：
        2. 内存管理 — 掌握度 5%
        3. 多线程锁 — 掌握度 8%
      ──────────────────────────
      输入 /coach 开始按计划训练
```

**进入训练循环 `/coach start`**

```
你：/coach start

教练：你想训练哪个方向？
      - 直接说知识点名称（如"虚函数"、"智能指针"）
      - weak：训练薄弱知识点
      - due：复习到期内容

你：虚函数

教练：专项训练：虚函数
      掌握度：35%
      难度：中等

      第 1 题：
      虚函数的动态绑定在编译期和运行期分别做了什么？如果不用虚函数，还有什么方式实现多态？
```

### 核心特性

- **面试官视角**：引导思考，不直接给答案
- **弱项驱动训练**：自动优先训练最薄弱知识点
- **六维度精准诊断**：correctness、completeness、depth、clarity、code_accuracy、edge_case_awareness
- **追问式训练**：根据你的回答持续追问，挖掘薄弱点
- **SQLite 状态持久化**：掌握度、QA 历史自动存储

### 安装方式

#### 方式一：克隆 + 自动安装（推荐）

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

安装后重启 Claude Code，输入 `/` 即可看到 `interview` 和 `coach`。

#### 方式二：手动安装

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
```

将 `skills/interview/` 和 `skills/coach/` 两个文件夹复制到 `~/.claude/skills/` 下：

```
~/.claude/skills/
├── interview/
│   ├── SKILL.md
│   └── index/knowledge_index.json
└── coach/
    ├── SKILL.md
    ├── coach/                # Python 持久化后端
    │   ├── cli.py
    │   ├── db.py
    │   ├── scheduler.py
    │   └── ...
    └── index/knowledge_index.json
```

### 注意事项

- **无需 PDF 资料即可使用**，默认基于内置知识点索引和模型知识生成回答
- `/coach reset` 和 `/coach export` 尚未实现
- 真实 LLM 接入需要设置 `OPENAI_API_KEY` 环境变量

### 开发者调试方式

```bash
# 从 skills/coach/ 目录运行
cd skills/coach
python -m coach.cli status
python -m coach.cli topic 虚函数

# 或者使用安装脚本
python setup.py
```
## Star History

<a href="https://www.star-history.com/?repos=yiqi-7%2FCpp-Interviewer&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&legend=top-left" />
 </picture>
</a>

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

#### Training Mode Interaction Examples

**Specific Topic `/coach virtual_function`**

```
You: /coach virtual_function

Coach: Training: vtable
       Mastery: 2.4%
       Difficulty: Basic

       Q1:
       What is a vtable? What's the relationship between a class with virtual functions, its objects, and the vtable?

You: A vtable is an array of function pointers. The compiler generates one per class with virtual functions. Objects point to it via vptr.

Coach: Evaluation: Core concept correct, but missed vptr storage layout and inheritance table merging rules.
       Weakness: vptr layout, multiple inheritance
       Mastery update: 2.4% → 12%

       Q2:
       Under multiple inheritance, how many vptrs does an object have? How does the compiler resolve virtual function calls?
```

**Weak Topics `/coach weak`**

```
You: /coach weak

Coach: Current weakness: vtable (mastery 12%)
       Starting training...

       Q1:
       What's the purpose of a virtual destructor? What happens if you delete a derived class pointer through a non-virtual base destructor?
```

**Mastery Dashboard `/coach status`**

```
You: /coach status

Coach: 📊 Mastery Dashboard
       ──────────────────────────
       Total: 15    Mastered: 2
       Weak: 8      Avg Mastery: 23%
       ──────────────────────────
       ▓▓▓░░░░░░░  Virtual Functions   35%
       ▓▓░░░░░░░░  Smart Pointers      20%
       ▓░░░░░░░░░  vtable              12%
       ░░░░░░░░░░  Memory Mgmt          5%
       ...
```

**Training Plan `/coach plan`**

```
You: /coach plan

Coach: 📋 Today's Training Plan
       ──────────────────────────
       Review (due):
         1. vtable — last trained 3 days ago, recommended review
       New (weak):
         2. Memory Management — mastery 5%
         3. Thread Locks — mastery 8%
       ──────────────────────────
       Type /coach to start training
```

**Training Loop `/coach start`**

```
You: /coach start

Coach: What topic would you like to train?
       - Type a topic name (e.g. "virtual_function", "smart_pointer")
       - weak: train weak topics
       - due: review due content

You: virtual_function

Coach: Training: Virtual Functions
       Mastery: 35%
       Difficulty: Intermediate

       Q1:
       What happens at compile time vs runtime for dynamic binding of virtual functions? Besides virtual functions, what other ways can achieve polymorphism?
```

### Core Features

- **Interviewer perspective**: Guides thinking, no direct answers
- **Weakness-driven training**: Automatically prioritizes weakest topics
- **Six-dimension precise diagnosis**: correctness, completeness, depth, clarity, code_accuracy, edge_case_awareness
- **Follow-up based training**: Continues questioning based on your answers to dig out weak points
- **SQLite state persistence**: Mastery, QA history automatically stored

### Installation

#### Option 1: Clone + Auto Install (Recommended)

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

After installation, restart Claude Code. Type `/` to see `interview` and `coach`.

#### Option 2: Manual Install

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
```

Copy `skills/interview/` and `skills/coach/` to `~/.claude/skills/`:

```
~/.claude/skills/
├── interview/
│   ├── SKILL.md
│   └── index/knowledge_index.json
└── coach/
    ├── SKILL.md
    ├── coach/                # Python 持久化后端
    │   ├── cli.py
    │   ├── db.py
    │   ├── scheduler.py
    │   └── ...
    └── index/knowledge_index.json
```

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
## Star History

<a href="https://www.star-history.com/?repos=yiqi-7%2FCpp-Interviewer&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=yiqi-7/Cpp-Interviewer&type=date&legend=top-left" />
 </picture>
</a>

### License

This project is licensed under the [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE).

### Community

- Discussion group: Q 828570482
- Recognized by [LINUX DO](https://linux.do/) community
### 参考资料

本项目不包含参考资料 PDF，以下资源可自行获取：

- **C++ 基础**：《Effective C++》、《STL 源码剖析》、《深度探索 C++ 对象模型》
- **面试题**：[小林 Coding](https://www.xiaolincoding.com/) 面试系列
- **系统与网络**：《Linux 高性能服务器编程》、《TCP/IP 网络编程》
