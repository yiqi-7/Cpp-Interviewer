<div align="center">

# Cpp-Interviewer

**C++ 面试学习伙伴 — 学 + 练，下载后可直接交给 Agent 使用**

[中文](#中文) | [English](#english)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Agent%20Skills-lightgrey.svg)

</div>

---

<a id="中文"></a>

## 中文

### 简介

Cpp-Interviewer 是一个面向主流 Agent 的 C++ 面试 skill 项目，提供学 + 练双模式：

- **`/interview` 直接给精炼答案**：默认简洁模式，不模拟面试、不反问，覆盖 C++、STL、操作系统、网络、数据库等高频考点。
- **`/coach` 模拟面试官追问**：出题 → 等你回答 → 六维度评价 → 记录掌握度 → 继续追问薄弱点。
- **无需 API Key**：直接使用当前 Agent 作为 LLM。
- **无需 PDF/Git LFS**：内置知识索引，clone 后即可安装使用。
- **Agent 中立**：核心 skill 可被 Codex、Claude Code、Cursor、Gemini、Copilot 等 Agent 复用。

知识索引中的 `books/...pdf` 是可选资料路径，书籍需由用户自行提供，仓库不附带这些 PDF。资料缺失时仍可进行基础讲解；Agent 应使用可访问来源或稳定知识，不能声称查阅了未打开的文件。

### 让 Agent 直接安装

把下面这段发给你的本地 Agent 即可：

```text
请安装 Cpp-Interviewer：
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py --agents all
安装后重启当前 Agent，并用 /interview 或 /coach 测试。
```

默认安装到常见 skills 目录：

| Agent | 安装目录 |
|------|----------|
| Codex / ChatGPT | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| 通用 Agent skills 目录 | `~/.agents/skills/` |

只安装到当前 Codex：

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

指定目标或自定义目录：

```bash
python setup.py --agents codex,cursor,claude
python setup.py --skills-dir /path/to/your/agent/skills
```

安装后重启对应 Agent。在支持 slash skill 的环境中输入 `/`，即可看到 `interview` 和 `coach`。不支持 slash skill 的 Agent 可以读取仓库内的 `.github/copilot-instructions.md`，或直接引用 `skills/cpp-interviewer/SKILL.md`。

`python setup.py` 负责复制 skill 文件；它不会把 Python 后端安装到当前解释器。仓库根目录可直接运行 `python -m coach.cli ...`。若要从其他项目目录调用，请在选定的虚拟环境中运行 `python setup.py develop`，随后使用该环境的 Python。只有 skill 文件可用而 CLI 不可用时，仍可对话练习，但不会保存训练状态。

### 兼容性与验证范围

以下区分文件布局兼容与真实 Agent 会话。安装测试使用临时目录，不会安装到开发者的真实 skills 目录；通过它不等于自动触发或回答质量已经验证。

| Agent / 入口 | 交付方式 | 安装布局检查 | 自动触发 | Interview / Coach 真实会话 | 持久化会话 |
|---|---|---|---|---|---|
| Codex | `.codex/skills` | 自动测试覆盖 | 待验证 | 待验证 | 待验证 |
| Claude Code | `.claude/skills` | 自动测试覆盖 | 待验证 | 待验证 | 待验证 |
| Cursor | `.cursor/skills` | 自动测试覆盖 | 待验证 | 待验证 | 待验证 |
| 通用 skills 目录 | `.agents/skills` | 自动测试覆盖 | 由宿主决定，待验证 | 待验证 | 待验证 |
| Gemini / Copilot 等其他环境 | 引用核心文件或 Copilot instructions | 引用路径静态检查 | 待验证 | 待验证 | 待验证 |

验证记录基准日期：2026-11-19。Python 工程测试与 Agent 行为评测分开记录；更新表中状态时附上 Agent / 模型版本、日期和实际记录。可重放用例、评分方式与隔离要求见 [行为评测说明](evals/README.md)。

### 两种模式

| 入口 | 模式 | 核心定位 | 示例 |
|------|------|----------|------|
| `/interview` | 知识讲解（学） | 直接给高密度答案，适合快速复习 | `/interview 虚函数是怎么实现的` |
| `/coach` | 面试训练（练） | 一次一题，追问式训练 | `/coach 虚函数`、`/coach weak` |

#### `/interview` 示例

```text
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
/interview 进程的内存空间结构
```

##### 完整回答示例：进程的内存空间结构

输入：

```text
/interview 进程的内存空间结构
```

典型回答会先说明这是**虚拟地址空间**，再给出常见布局和实现边界：

```text
高地址
┌──────────────────────┐
│ 栈 Stack              │  局部变量、参数、返回地址
│       ↓ 向低地址增长  │
├──────────────────────┤
│ mmap / 共享库区域     │  动态库、文件映射、共享内存
├──────────────────────┤
│ 堆 Heap               │  malloc/new 动态分配
│       ↑ 向高地址增长  │
├──────────────────────┤
│ BSS                   │  未初始化的全局/静态变量
├──────────────────────┤
│ Data                  │  已初始化的全局/静态变量
├──────────────────────┤
│ Rodata                │  字符串常量、只读常量
├──────────────────────┤
│ Text / Code           │  程序机器指令
└──────────────────────┘
低地址
```

- Text 通常可读可执行；Data、BSS 和堆保存进程数据，栈保存调用现场。
- 堆向上增长、栈向下增长是常见实现，不是 C++ 标准保证；实际布局由操作系统、CPU 架构、链接器和 ABI 决定。
- 这是进程看到的虚拟地址空间，不等同于物理内存；ASLR 还会随机化部分区域的实际地址。
- 共享库、线程本地存储、保护页和内核空间可能出现在图示之外；具体区域和顺序应以目标平台的内存映射为准。

这个示例体现 `/interview` 的默认行为：直接解释当前问题，先给可读的整体模型，再补充平台相关边界，不自动切换为模拟面试或追加追问。

#### `/coach` 示例

```text
/coach 虚函数          # 专项训练
/coach weak            # 训练薄弱知识点
/coach due             # 复习到期内容
/coach status          # 查看掌握度
/coach plan            # 生成今日计划
/coach export          # 导出训练数据
/coach reset           # 重置本地训练状态
/coach start           # 进入训练循环
```

`/coach` 会像面试官一样：**出题 → 等你回答 → 评价 → 追问 → 下一题**。

### 状态和路径

训练状态默认保存在 `~/.cpp-interviewer/coach.sqlite`。可用环境变量覆盖：

```bash
export CPP_INTERVIEWER_HOME="$HOME/.cpp-interviewer"
export CPP_INTERVIEWER_DB="$HOME/.cpp-interviewer/coach.sqlite"
export CPP_INTERVIEWER_INDEX="/path/to/knowledge_index.json"
```

Windows PowerShell：

```powershell
$env:CPP_INTERVIEWER_HOME="$HOME\.cpp-interviewer"
$env:CPP_INTERVIEWER_DB="$HOME\.cpp-interviewer\coach.sqlite"
$env:CPP_INTERVIEWER_INDEX="C:\path\to\knowledge_index.json"
```

### 开发者调试

```bash
python -m pytest -q
python -m coach.cli status
python -m coach.cli topic search 虚函数 --json
python -m coach.cli topic-context cpp_vtable --json
python -m coach.cli export --format md --output coach-export.md
python -m coach.cli reset --yes
```

如需安装 `coach` / `cpp-coach` console script，可运行 `python setup.py develop`。

修改 Skill 指令后，除工程测试外还应运行 [行为评测](evals/README.md)，比较相同输入经过核心 Skill 和兼容入口的结果；模型或宿主更新后重跑固定用例，保留失败案例。

### 项目结构

```text
Cpp-Interviewer/
├── skills/
│   ├── cpp-interviewer/      # agent-neutral 核心 skill
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/
│   ├── interview/            # /interview 兼容入口
│   └── coach/                # /coach 兼容入口 + Python 后端
├── .github/copilot-instructions.md
├── setup.py
└── tests/
```

### 导出与重置

`/coach` 的训练状态可以导出或重置：

```bash
python -m coach.cli export --format json --output coach-export.json
python -m coach.cli export --format md --output coach-export.md
python -m coach.cli export --format txt --output coach-export.txt
python -m coach.cli export --format doc --output coach-export.doc
python -m coach.cli reset --yes
```

`reset` 只清空本地训练状态，不删除知识索引。`doc` 导出为 Word 可打开的 HTML 文档。

### Instruction-only Agent 用法

`Gemini`、`Copilot` 等 instruction-only Agent 通常不会自动注册 slash command。可直接让它们读取核心 skill：

```text
请读取 skills/cpp-interviewer/SKILL.md，并按 /interview 模式回答：虚函数是怎么实现的？
```

```text
请读取 skills/cpp-interviewer/SKILL.md，并按 /coach 模式训练我：虚函数
```

## Star History

<a href="https://www.star-history.com/?repos=yiqi-7%2FCpp-Interviewer&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg" />
   <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg" />
   <img alt="Star History Chart" src="./assets/star-history-light.svg" />
 </picture>
</a>

### 开源许可

本项目采用 [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE) 开源。

### 社区

- 已获 [LINUX DO](https://linux.do/) 社区认可

---

<a id="english"></a>

## English

### Introduction

Cpp-Interviewer is an agent-neutral C++ interview skill with two modes:

- **`/interview`**: concise, direct explanations for C++ and CS interview topics.
- **`/coach`**: one-question-at-a-time interview practice with six-dimension evaluation and SQLite mastery tracking.
- **No API key required**: the host agent is the LLM.
- **No PDF or Git LFS required**: it works with the built-in knowledge index after clone.
- **Portable across agents**: Codex, Claude Code, Cursor, Gemini, Copilot, and other tools can reuse the same core skill.

Paths such as `books/...pdf` in the index refer to optional, user-supplied books; these PDFs are not distributed in this repository. Basic explanations still work without them. Use accessible sources or stable knowledge, and never claim to have consulted a file that was not opened.

### Agent-Friendly Install

Give this to your local agent:

```text
Install Cpp-Interviewer:
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py --agents all
Restart the target agent, then test /interview or /coach.
```

Install only to Codex:

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

Choose targets or a custom skills directory:

```bash
python setup.py --agents codex,cursor,claude
python setup.py --skills-dir /path/to/your/agent/skills
```

Common targets:

| Agent | Skills directory |
|-------|------------------|
| Codex / ChatGPT | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| Generic agent skills | `~/.agents/skills/` |

For instruction-only agents, use `.github/copilot-instructions.md` or point the agent at `skills/cpp-interviewer/SKILL.md`.

`python setup.py` copies skill files; it does not install the Python backend into the active interpreter. `python -m coach.cli ...` works from the repository root. To call it from another project directory, run `python setup.py develop` in a chosen virtual environment and use that environment's Python. If only the skill files are available, conversational practice remains available without persistence.

### Compatibility And Verification Scope

Layout compatibility and real agent sessions are separate checks. Installer tests use temporary directories, not the developer's real skills directories; passing them does not establish automatic triggering or answer quality.

| Agent / entry | Delivery | Install layout | Automatic triggering | Real Interview / Coach sessions | Persistence sessions |
|---|---|---|---|---|---|
| Codex | `.codex/skills` | Automated tests | Not verified | Not verified | Not verified |
| Claude Code | `.claude/skills` | Automated tests | Not verified | Not verified | Not verified |
| Cursor | `.cursor/skills` | Automated tests | Not verified | Not verified | Not verified |
| Generic skills directory | `.agents/skills` | Automated tests | Host-dependent; not verified | Not verified | Not verified |
| Other environments, including Gemini / Copilot | Core file or Copilot instructions | Static reference checks | Not verified | Not verified | Not verified |

Verification baseline: November 19, 2026. Keep Python engineering checks separate from agent behavior results. Record agent/model version, date, and actual transcripts when updating this table. See [behavior evals](evals/README.md) for replayable cases, grading, and isolated state.

### Usage

```text
/interview How are virtual functions implemented
/interview What types of smart pointers are there
/interview What is the process memory space layout
/coach virtual_function
/coach weak
/coach status
/coach plan
python -m coach.cli export --format md --output coach-export.md
python -m coach.cli reset --yes
```

### State

Training state defaults to `~/.cpp-interviewer/coach.sqlite`. Override paths with:

```bash
export CPP_INTERVIEWER_HOME="$HOME/.cpp-interviewer"
export CPP_INTERVIEWER_DB="$HOME/.cpp-interviewer/coach.sqlite"
export CPP_INTERVIEWER_INDEX="/path/to/knowledge_index.json"
```

### Developer Mode

```bash
python -m pytest -q
python -m coach.cli status
python -m coach.cli topic search virtual_function --json
python -m coach.cli topic-context cpp_vtable --json
python -m coach.cli export --format md --output coach-export.md
python -m coach.cli reset --yes
```

Run `python setup.py develop` only if you want the `coach` / `cpp-coach` console scripts.

After changing skill instructions, run the [behavior evals](evals/README.md) as well as engineering tests. Compare the same inputs through the core skill and compatibility entries, rerun fixed cases after model or host changes, and retain failed cases.

#### Example answer: process memory space layout

Prompt:

```text
/interview What is the process memory space layout?
```

A useful answer should identify the layout as a **virtual address space** and distinguish common implementation choices from guarantees:

```text
High addresses
┌──────────────────────┐
│ Stack                │  locals, arguments, return state
│       ↓ grows down   │
├──────────────────────┤
│ mmap / shared libs   │  libraries, file mappings, shared memory
├──────────────────────┤
│ Heap                 │  malloc/new allocations
│       ↑ grows up     │
├──────────────────────┤
│ BSS                  │  zero-initialized global/static data
├──────────────────────┤
│ Data                 │  initialized global/static data
├──────────────────────┤
│ Read-only data       │  literals and constants
├──────────────────────┤
│ Text / code          │  executable instructions
└──────────────────────┘
Low addresses
```

The answer should also state that stack/heap growth directions and the exact order are common OS/ABI conventions rather than C++ guarantees, that virtual addresses are different from physical memory, and that ASLR changes runtime addresses.

### Export And Reset

Coach state can be exported as JSON, Markdown, plain text, or a Word-openable `.doc` file:

```bash
python -m coach.cli export --format json --output coach-export.json
python -m coach.cli export --format md --output coach-export.md
python -m coach.cli export --format txt --output coach-export.txt
python -m coach.cli export --format doc --output coach-export.doc
```

Reset clears only local training state and keeps the knowledge index:

```bash
python -m coach.cli reset --yes
```

## Star History

<a href="https://www.star-history.com/?repos=yiqi-7%2FCpp-Interviewer&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="./assets/star-history-dark.svg" />
   <source media="(prefers-color-scheme: light)" srcset="./assets/star-history-light.svg" />
   <img alt="Star History Chart" src="./assets/star-history-light.svg" />
 </picture>
</a>

### License

This project is licensed under the [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE).
