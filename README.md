<div align="center">

# Cpp-Interviewer

用本地 AI Agent 复习 C++ 面试知识，或逐题练习并跟踪掌握度。

[中文快速开始](#中文) · [English quick start](#english) · [问题反馈 / Issues](https://github.com/yiqi-7/Cpp-Interviewer/issues)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

<a id="中文"></a>

## 中文

### 快速开始

准备 Git、Python 3.10 或更新版本，以及能加载本地 Skills 的 Agent。项目使用宿主 Agent 的模型，不需要为本项目另配 API Key。

在终端运行以下命令，默认安装到 Codex 的 `~/.codex/skills/`：

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

终端出现 `[OK] codex: ...` 和 `Done! Restart your agent...` 表示安装脚本已完成。重启 Agent，在聊天框试用：

```text
/interview 虚函数表存在哪里？
/coach 虚函数
```

`/interview` 应直接解释虚函数表，并说明布局取决于编译器和 ABI。`/coach` 应先出一道题，等你回答后再评分。自动出现斜杠入口和真实会话表现取决于宿主，验证范围见下文。

### 选择安装位置

从仓库根目录运行 `python setup.py --agents all` 可安装到下表四个目标：

| Agent | 安装目录 |
|------|----------|
| Codex / ChatGPT | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Claude Code | `~/.claude/skills/` |
| 通用 Agent skills 目录 | `~/.agents/skills/` |

可以指定目标，或仅安装到自定义目录：

```bash
python setup.py --agents codex,cursor,claude
python setup.py --skills-dir /path/to/your/agent/skills
```

安装后重启目标 Agent。不支持斜杠入口时，可让 Agent 读取[核心 Skill](skills/cpp-interviewer/SKILL.md)，Copilot 也可以读取[仓库指令](.github/copilot-instructions.md)。

`python setup.py` 负责复制 skill 文件；它不会把 Python 后端安装到当前解释器。仓库根目录可直接运行 `python -m coach.cli ...`。若要从其他项目目录调用，请在选定的虚拟环境中运行 `python setup.py develop`，随后使用该环境的 Python。只有 skill 文件可用而 CLI 不可用时，仍可对话练习，但不会保存训练状态。

### 兼容性与验证范围

以下区分文件布局兼容与真实 Agent 会话。安装测试使用临时目录，不会安装到开发者的真实 skills 目录；通过它不等于自动触发或回答质量已经验证。

知识索引内置在仓库里，无需 Git LFS。`books/...pdf` 是用户可自行提供的可选资料，仓库不附带 PDF。基本讲解可继续；Agent 只能引用实际可访问的资料。

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
| `/interview` | 知识讲解（学） | 直接给高密度答案，适合快速复习 | `/interview 进程的内存空间结构` |
| `/coach` | 面试训练（练） | 一次一题，追问式训练 | `/coach 虚函数`、`/coach weak` |

#### `/interview` 示例

```text
/interview 虚函数表的位置
/interview 进程的内存空间结构
/interview 栈和堆有什么区别
/interview 虚函数是怎么实现的
```

##### 回答示例：虚函数表的位置

```text
C++ 标准没有规定虚函数表（vtable）或虚指针（vptr）的具体布局，它们属于编译器和 ABI 的实现细节。

常见实现中，vtable 通常位于程序映像的只读或重定位后只读数据区，例如 ELF 平台的 .rodata / .data.rel.ro，或 MSVC 的 .rdata。对象中的隐藏 vptr 通常指向相应的表；对象本身仍按存储期位于栈、堆或静态存储区。多继承对象可能包含多个 vptr。

因此，面试中可以概括为：虚函数表通常放在程序的只读数据区域，虚指针通常存放在对象内部；具体布局取决于编译器、ABI 和平台，不能当作 C++ 标准保证。
```

##### 完整回答示例：进程的内存空间结构

输入：

```text
/interview 进程的内存空间结构
```

典型回答会先说明这是**虚拟地址空间**，再给出常见布局和实现边界。下图是示意布局，不代表所有系统的固定顺序：

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

`/coach` 会像面试官一样：**出题 → 等你回答 → 六维度评价 → 追问或进入下一题**。Python 后端可用时，会把评估结果写入本地 SQLite。

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
python -m pip install pytest
python -m pytest -q
python -m coach.cli status
python -m coach.cli topic search 虚函数 --json
python -m coach.cli topic-context cpp_vtable --json
```

首次运行 `status` 时，空数据库会显示 `答题记录数: 0`；`topic-context` 返回含有 `"topic_id":"cpp_vtable"` 的 JSON，说明 CLI 可以读取知识索引。

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

本项目采用 [MIT License](LICENSE) 开源。发现问题时，可在 [Issues](https://github.com/yiqi-7/Cpp-Interviewer/issues) 中附上 Agent、模型、复现步骤和实际表现。提交 PR 前请运行工程测试；涉及 Skill 行为时参考[行为评测说明](evals/README.md)。

### 社区

- 已获 [LINUX DO](https://linux.do/) 社区认可

---

<a id="english"></a>

## English

Cpp-Interviewer is a local agent skill for reviewing C++ interview topics and practicing one question at a time. It uses your host agent's model, so it needs no separate API key.

### Quick Start

You need Git, Python 3.10 or later, and an agent that can load local skills. Run these commands in a terminal to install for Codex:

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
cd Cpp-Interviewer
python setup.py
```

Look for `[OK] codex: ...` and `Done! Restart your agent...` in the output. Restart the agent and try these prompts in the chat:

```text
/interview Where is the virtual function table located?
/coach virtual functions
```

`/interview` should give a direct answer and explain that vtable layout depends on the compiler and ABI. `/coach` should ask one question and wait for your answer before scoring it. Slash command discovery and session behavior depend on the host; see the verification scope below.

### Installation Targets

Choose targets or a custom skills directory:

```bash
python setup.py --agents all
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

For agents without slash commands, point the agent at the [core skill](skills/cpp-interviewer/SKILL.md) or use the [Copilot instructions](.github/copilot-instructions.md) for Copilot.

`python setup.py` copies skill files; it does not install the Python backend into the active interpreter. `python -m coach.cli ...` works from the repository root. To call it from another project directory, run `python setup.py develop` in a chosen virtual environment and use that environment's Python. If only the skill files are available, conversational practice remains available without persistence.

### Compatibility And Verification Scope

Layout compatibility and real agent sessions are separate checks. Installer tests use temporary directories, not the developer's real skills directories; passing them does not establish automatic triggering or answer quality.

The knowledge index is included and does not require Git LFS. Paths such as `books/...pdf` refer to optional user-supplied books. Basic explanations work without these PDFs; the agent should cite only sources it could access.

| Agent / entry | Delivery | Install layout | Automatic triggering | Real Interview / Coach sessions | Persistence sessions |
|---|---|---|---|---|---|
| Codex | `.codex/skills` | Automated tests | Not verified | Not verified | Not verified |
| Claude Code | `.claude/skills` | Automated tests | Not verified | Not verified | Not verified |
| Cursor | `.cursor/skills` | Automated tests | Not verified | Not verified | Not verified |
| Generic skills directory | `.agents/skills` | Automated tests | Host-dependent; not verified | Not verified | Not verified |
| Other environments, including Gemini / Copilot | Core file or Copilot instructions | Static reference checks | Not verified | Not verified | Not verified |

Verification baseline: November 19, 2026. Keep Python engineering checks separate from agent behavior results. Record agent/model version, date, and actual transcripts when updating this table. See [behavior evals](evals/README.md) for replayable cases, grading, and isolated state.

### Usage

`/interview` provides direct explanations. `/coach` asks one question at a time, scores your answer across six dimensions, and tracks mastery in SQLite when the Python backend is available.

```text
/interview How are virtual functions implemented
/interview Where is the virtual function table located?
/interview What is the process memory space layout
/interview What is the difference between stack and heap?
/coach virtual functions
/coach weak
/coach status
/coach plan
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
python -m pip install pytest
python -m pytest -q
python -m coach.cli status
python -m coach.cli topic search vtable --json
python -m coach.cli topic-context cpp_vtable --json
```

On a fresh database, `status` displays `答题记录数: 0` (zero answers). `topic-context` returns JSON containing `"topic_id":"cpp_vtable"`, which confirms the CLI can read the knowledge index.

Run `python setup.py develop` only if you want the `coach` / `cpp-coach` console scripts.

After changing skill instructions, run the [behavior evals](evals/README.md) as well as engineering tests. Compare the same inputs through the core skill and compatibility entries, rerun fixed cases after model or host changes, and retain failed cases.

#### Example answer: virtual function table location

```text
The C++ standard does not specify a virtual table (vtable) or virtual pointer (vptr); their layout is an implementation detail of the compiler and ABI.

In common implementations, a vtable lives in a read-only or relocation-protected read-only section of the program image, such as .rodata or .data.rel.ro on ELF systems, or .rdata with MSVC. An object's hidden vptr usually points to the relevant table. The object itself can still have automatic, dynamic, or static storage duration, and multiple inheritance may require more than one vptr.

So the concise answer is: the vtable is commonly stored in read-only program data, while the vptr is commonly stored inside the object. The exact layout depends on the compiler, ABI, and platform; it is not guaranteed by C++.
```

#### Example answer: process memory space layout

Prompt:

```text
/interview What is the process memory space layout?
```

A useful answer should identify the layout as a **virtual address space** and distinguish common implementation choices from guarantees. This is illustrative; systems do not all use this exact order:

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

This project is licensed under the [MIT License](LICENSE). Report problems in [GitHub Issues](https://github.com/yiqi-7/Cpp-Interviewer/issues) with the agent, model, steps to reproduce, and actual behavior. Run the engineering tests before submitting a PR; for behavior changes, follow the [eval guide](evals/README.md).
