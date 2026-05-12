<div align="center">

# Cpp-Interviewer

**C++ 面试八股讲解 Skill**

**C++ Interview Preparation Skill**

[中文](#中文) | [English](#english)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code-lightgrey.svg)

</div>

---

<a id="中文"></a>

## 中文

### 简介

模拟面试官角色，帮助你理解和掌握 C++ 面试中的核心知识点。不是直接给答案，而是引导你思考、追问细节、指出常见误区。

### 使用方式

**面试提问：**
```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
```

**添加参考资料（书籍 / 网址）：**
```
/interview 添加书籍 F:\books\深入理解计算机系统.pdf
/interview 添加网址 https://some-interview-site.com
```

添加后，Skill 会自动解析内容、建立知识点索引，后续提问时自动匹配检索。

### 功能特性

- **面试官视角**：不是直接给答案，而是引导你思考、追问细节、指出常见误区
- **三级深度扩展**：
    - Level 1 — 只讲当前知识点，讲透讲明白
    - Level 2 — 同方向扩展（如 C++ 语言范围内扩展）
    - Level 3 — 跨学科扩展（包含 Level 2 全部内容 + 横向扩展到操作系统、计算机网络等）
- **回答风格可选**：简洁模式（快速复习）/ 详细模式（深入学习），随时可切换
- **难度递进追问**：每个问题结束后给出 3-5 个高频面试追问，从基础到深入排列
- **知识点索引系统**：通过 `index/knowledge_index.json` 快速定位知识来源，新增书籍或网址自动建立索引
- **参考资料自动读取**：回答时自动参考仓库中的八股文 PDF 和经典书籍

### 仓库结构

```
.
├── skills/
│   └── interview/
│       └── SKILL.md          # Skill 指令文件
├── index/
│   └── knowledge_index.json  # 知识点索引（60+ 知识点，快速定位资料来源）
├── books/
│   ├── 八股文/                # 面试核心八股文
│   │   ├── C++篇.pdf
│   │   ├── 计算机基础篇.pdf
│   │   ├── 算法篇.pdf
│   │   ├── 面经篇.pdf
│   │   └── 概述.pdf
│   ├── C++/                  # C++ 经典书籍
│   │   ├── c++知识点全概括.pdf
│   │   ├── Effective C++.pdf
│   │   ├── STL源码剖析.pdf
│   │   └── 深度探索C++对象模型.pdf
│   ├── 系统与网络/            # 操作系统、网络、底层
│   │   ├── Linux高性能服务器编程.pdf
│   │   ├── TCP IP网络编程.pdf
│   │   ├── 深入理解Linux进程与内存.pdf
│   │   └── 程序员的自我修养—链接、装载与库.pdf
│   ├── 工具/                 # 开发工具
│   │   ├── gdb手册.pdf
│   │   ├── MySQL必知必会.pdf
│   │   └── 跟我一起写Makefile.pdf
│   └── 小林coding/           # 小林coding 图解 + 面试题
│       ├── 面试题/
│       │   ├── 100道+CPP面试题.pdf
│       │   ├── 150道MySQL+Redis面试题.pdf
│       │   ├── 150道计算机网络+操作系统+数据结构与算法面试题.pdf
│       │   └── 30道Linux命令+Git面试题.pdf
│       └── 图解系列/
│           ├── 图解MySQL.pdf
│           ├── 图解Redis.pdf
│           └── 图解系统.pdf
└── README.md
```

### 知识点索引系统

`index/knowledge_index.json` 包含 60+ 个面试知识点的结构化索引，覆盖：

| 领域 | 知识点数 | 示例 |
|------|---------|------|
| C++ 语言 | 15 | 指针与引用、智能指针、虚函数表、移动语义... |
| STL | 4 | vector底层、map/unordered\_map、迭代器失效... |
| C++ 新特性 | 3 | C++11/14/17/20、多线程并发 |
| 算法与数据结构 | 8 | 排序、动态规划、二叉树、链表、图... |
| 操作系统 | 6 | 进程与线程、虚拟内存、死锁、IO模型... |
| 计算机网络 | 5 | TCP、UDP、HTTP/HTTPS、DNS、IP... |
| 数据库 | 2 | MySQL、Redis |
| 链接装载库 | 2 | 静态库/动态库、编译链接流程 |
| 工具 | 4 | GDB、Makefile、Git、Linux命令 |
| 设计模式 | 5 | 单例、工厂、观察者、策略、RAII |

每个知识点包含：
- `keywords`：用于匹配用户问题的关键词
- `sources`：指向具体书籍路径和在线资源
- `related_topics`：关联知识点（用于深度扩展）
- `interview_frequency`：面试频率评级

**新增书籍或网址时，只需更新索引文件即可，无需修改 SKILL.md。**

### 在线参考资源

#### GitHub 开源仓库

| 仓库 | Stars | 内容 |
|------|-------|------|
| [huihut/interview](https://github.com/huihut/interview) | 37.8k | C/C++ 面试知识总结，涵盖语言、数据结构、算法、系统、网络、设计模式 |
| [muluoleiguo/interview](https://github.com/muluoleiguo/interview) | — | C++ 后端面试知识汇总，涵盖语言基础、STL、操作系统、网络、数据库 |
| [yzhu798/CodingInterviewsNotes](https://github.com/yzhu798/CodingInterviewsNotes) | — | C++ 面试笔记，涵盖算法、操作系统、网络、数据库、设计模式 |
| [guaguaupup/cpp_interview](https://github.com/guaguaupup/cpp_interview) | — | C++ 面试题整理，语言基础、STL、内存管理、多线程 |
| [leetcode-master](https://github.com/youngyangyang04/leetcode-master) | 61.3k | 代码随想录，200+ 道 LeetCode 题解，以 C++ 为主语言 |
| [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features) | 21.6k | C++11/14/17/20/23 新特性速查手册 |
| [TechCPP](https://github.com/youngyangyang04/TechCPP) | — | C++ 面试 & 学习指南知识点整理 |

#### 面试指南网站

| 网站 | 内容 |
|------|------|
| [interviewguide.cn](https://interviewguide.cn) | 面试指南，覆盖C++、Java、前端、算法、操作系统、网络等，按岗位分类 |
| [小林coding](https://xiaolincoding.com) | 图解计算机网络、操作系统、MySQL、Redis，面试题汇总 |

#### 在线学习 / 刷题平台

| 网站 | 内容 |
|------|------|
| [GeeksforGeeks C++ 面试题](https://www.geeksforgeeks.org/cpp/cpp-interview-questions/) | C++ 面试题合集，分类清晰，英文 |
| [GeeksforGeeks C++ 教程](https://www.geeksforgeeks.org/c-plus-plus/) | C++ 完整教程，从基础到高级 |
| [LeetCode 中国](https://leetcode.cn) | 算法刷题，支持 C++，有面试题讨论区 |
| [CodeTop](https://codetop.cc) | 按公司/岗位筛选高频面试题 |
| [牛客网](https://www.nowcoder.com/search?type=question&query=C%2B%2B) | 国内最大面试题库，有企业真题 |
| [cppreference](https://zh.cppreference.com) | C++ 标准库权威参考 |

#### 智能资源选择策略

Skill 会根据问题类型自动选择最合适的数据源：

| 问题类型 | 首选数据源 | 补充数据源 |
|---------|-----------|-----------|
| C++ 语言基础 | 本地八股文 + 小林100道CPP面试题 | huihut/interview、guaguaupup/cpp\_interview、muluoleiguo/interview |
| C++ 新特性 | modern-cpp-features | interviewguide.cn、GeeksforGeeks |
| STL 容器/算法原理 | 本地STL源码剖析 | cppreference、huihut/interview |
| 虚函数/多态/对象模型 | 本地深度探索C++对象模型 | huihut/interview、yzhu798/CodingInterviewsNotes |
| 智能指针/内存管理 | 本地八股文 + 小林100道CPP面试题 | huihut/interview、guaguaupup/cpp\_interview |
| 数据结构与算法 | 本地八股文算法篇 | leetcode.cn、CodeTop、yzhu798/CodingInterviewsNotes |
| 操作系统 | 小林图解系统 + 八股文计算机基础篇 | huihut/interview、muluoleiguo/interview |
| 计算机网络 | 八股文 + TCP/IP网络编程 | huihut/interview、xiaolincoding.com |
| MySQL 数据库 | 小林图解MySQL + MySQL必知必会 | GeeksforGeeks、yzhu798/CodingInterviewsNotes |
| Redis 缓存 | 小林图解Redis + 小林150道MySQL+Redis面试题 | GeeksforGeeks、yzhu798/CodingInterviewsNotes |

#### 高频考点速查

| 考点 | 推荐资料 |
|------|---------|
| 智能指针（shared\_ptr/unique\_ptr/weak\_ptr） | huihut/interview + cppreference |
| 虚函数与多态 | GeeksforGeeks + huihut/interview |
| STL 容器底层原理 | GeeksforGeeks C++ 教程 |
| 移动语义与右值引用 | modern-cpp-features |
| 内存管理与 RAII | huihut/interview |
| 多线程（thread/mutex/atomic） | cppreference + modern-cpp-features |
| C++11/14/17/20 新特性 | modern-cpp-features |
| 算法与数据结构 | leetcode-master + CodeTop |

### 安装方式

#### 方式一：克隆仓库（推荐）

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
```

#### 方式二：下载使用

下载仓库代码后解压，将文件夹放置到 `~/.claude/skills/` 目录下。

### 注意事项

- PDF 书籍使用 Git LFS 管理，克隆时需要安装 [Git LFS](https://git-lfs.github.com/)
- 八股文 PDF 为加密文件，Skill 通过内容解析读取，部分格式可能不完整
- 建议结合在线资源一起使用，互相补充

### 开源许可

本项目采用 [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE) 开源。

### 社区

- 交流群：Q 828570482
- 已获 [LINUX DO](https://linux.do/) 社区认可

---

<a id="english"></a>

## English

### Introduction

Simulates an interviewer to help you understand and master core C++ interview topics. Instead of giving direct answers, it guides your thinking, asks follow-up questions, and highlights common pitfalls.

### Usage

**Ask interview questions:**
```
/interview How are virtual functions implemented
/interview What types of smart pointers are there
/interview What is a memory leak
```

**Add reference materials (books / URLs):**
```
/interview Add book F:\books\CSAPP.pdf
/interview Add URL https://some-interview-site.com
```

After adding, the Skill automatically parses content, builds a knowledge index, and matches relevant sources for future questions.

### Features

- **Interviewer perspective**: Guides your thinking, asks follow-up questions, and highlights common pitfalls instead of giving direct answers
- **Three-level depth expansion**:
    - Level 1 — Explain the current topic thoroughly
    - Level 2 — Expand within the same domain (e.g., more C++ topics)
    - Level 3 — Cross-domain expansion (includes Level 2 + OS, networking, etc.)
- **Selectable answer style**: Concise mode (quick review) / Detailed mode (deep learning), switchable anytime
- **Progressive difficulty follow-ups**: 3-5 high-frequency interview follow-up questions after each answer, sorted from basic to advanced
- **Knowledge index system**: Quickly locate knowledge sources via `index/knowledge_index.json`; new books or URLs are automatically indexed
- **Auto-read reference materials**: Automatically references the PDFs and classic books in the repository

### Repository Structure

```
.
├── skills/
│   └── interview/
│       └── SKILL.md          # Skill instruction file
├── index/
│   └── knowledge_index.json  # Knowledge index (60+ topics, fast source lookup)
├── books/
│   ├── 八股文/                # Core interview guides
│   │   ├── C++篇.pdf
│   │   ├── 计算机基础篇.pdf
│   │   ├── 算法篇.pdf
│   │   ├── 面经篇.pdf
│   │   └── 概述.pdf
│   ├── C++/                  # Classic C++ books
│   │   ├── c++知识点全概括.pdf
│   │   ├── Effective C++.pdf
│   │   ├── STL源码剖析.pdf
│   │   └── 深度探索C++对象模型.pdf
│   ├── 系统与网络/            # OS, networking, low-level
│   │   ├── Linux高性能服务器编程.pdf
│   │   ├── TCP IP网络编程.pdf
│   │   ├── 深入理解Linux进程与内存.pdf
│   │   └── 程序员的自我修养—链接、装载与库.pdf
│   ├── 工具/                 # Dev tools
│   │   ├── gdb手册.pdf
│   │   ├── MySQL必知必会.pdf
│   │   └── 跟我一起写Makefile.pdf
│   └── 小林coding/           # Xiaolin coding diagrams + interview questions
│       ├── 面试题/
│       │   ├── 100道+CPP面试题.pdf
│       │   ├── 150道MySQL+Redis面试题.pdf
│       │   ├── 150道计算机网络+操作系统+数据结构与算法面试题.pdf
│       │   └── 30道Linux命令+Git面试题.pdf
│       └── 图解系列/
│           ├── 图解MySQL.pdf
│           ├── 图解Redis.pdf
│           └── 图解系统.pdf
└── README.md
```

### Knowledge Index System

`index/knowledge_index.json` contains a structured index of 60+ interview topics, covering:

| Domain | Topics | Examples |
|--------|--------|----------|
| C++ Language | 15 | Pointers & references, smart pointers, vtable, move semantics... |
| STL | 4 | vector internals, map/unordered\_map, iterator invalidation... |
| Modern C++ | 3 | C++11/14/17/20, multithreading & concurrency |
| Algorithms & DS | 8 | Sorting, DP, binary trees, linked lists, graphs... |
| Operating Systems | 6 | Processes & threads, virtual memory, deadlock, IO models... |
| Networking | 5 | TCP, UDP, HTTP/HTTPS, DNS, IP... |
| Databases | 2 | MySQL, Redis |
| Linking & Loading | 2 | Static/dynamic libraries, compilation & linking pipeline |
| Tools | 4 | GDB, Makefile, Git, Linux commands |
| Design Patterns | 5 | Singleton, Factory, Observer, Strategy, RAII |

Each topic includes:
- `keywords`: For matching user questions
- `sources`: Pointers to specific book paths and online resources
- `related_topics`: Linked topics (for depth expansion)
- `interview_frequency`: Interview frequency rating

**To add new books or URLs, just update the index file — no need to modify SKILL.md.**

### Online Reference Resources

#### GitHub Repositories

| Repository | Stars | Content |
|-----------|-------|---------|
| [huihut/interview](https://github.com/huihut/interview) | 37.8k | C/C++ interview knowledge summary: language, DS, algorithms, systems, networking, design patterns |
| [muluoleiguo/interview](https://github.com/muluoleiguo/interview) | — | C++ backend interview knowledge: language basics, STL, OS, networking, databases |
| [yzhu798/CodingInterviewsNotes](https://github.com/yzhu798/CodingInterviewsNotes) | — | C++ interview notes: algorithms, OS, networking, databases, design patterns |
| [guaguaupup/cpp_interview](https://github.com/guaguaupup/cpp_interview) | — | C++ interview questions: language basics, STL, memory management, multithreading |
| [leetcode-master](https://github.com/youngyangyang04/leetcode-master) | 61.3k | Code Caprice, 200+ LeetCode solutions, primarily in C++ |
| [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features) | 21.6k | C++11/14/17/20/23 feature cheat sheet |
| [TechCPP](https://github.com/youngyangyang04/TechCPP) | — | C++ interview & study guide knowledge summary |

#### Interview Guide Websites

| Website | Content |
|---------|---------|
| [interviewguide.cn](https://interviewguide.cn) | Interview guide covering C++, Java, frontend, algorithms, OS, networking, categorized by role |
| [小林coding](https://xiaolincoding.com) | Visual guides for networking, OS, MySQL, Redis with interview question summaries |

#### Online Learning / Practice Platforms

| Website | Content |
|---------|---------|
| [GeeksforGeeks C++ Interview](https://www.geeksforgeeks.org/cpp/cpp-interview-questions/) | C++ interview questions, well-categorized, English |
| [GeeksforGeeks C++ Tutorial](https://www.geeksforgeeks.org/c-plus-plus/) | Complete C++ tutorial from basics to advanced |
| [LeetCode](https://leetcode.cn) | Algorithm practice, supports C++, has interview discussion forums |
| [CodeTop](https://codetop.cc) | Filter high-frequency interview questions by company/role |
| [牛客网](https://www.nowcoder.com/search?type=question&query=C%2B%2B) | China's largest interview question bank with real company questions |
| [cppreference](https://zh.cppreference.com) | Authoritative C++ standard library reference |

#### Smart Resource Selection Strategy

The Skill automatically selects the best data source based on question type:

| Question Type | Primary Source | Supplementary Source |
|--------------|---------------|---------------------|
| C++ Language Basics | Local guides + Xiaolin 100 CPP questions | huihut/interview, guaguaupup/cpp\_interview, muluoleiguo/interview |
| Modern C++ | modern-cpp-features | interviewguide.cn, GeeksforGeeks |
| STL Containers/Algorithms | Local STL Source Analysis | cppreference, huihut/interview |
| Virtual Functions/Polymorphism | Local Deep into C++ Object Model | huihut/interview, yzhu798/CodingInterviewsNotes |
| Smart Pointers/Memory | Local guides + Xiaolin 100 CPP questions | huihut/interview, guaguaupup/cpp\_interview |
| Data Structures & Algorithms | Local algorithm guides | leetcode.cn, CodeTop, yzhu798/CodingInterviewsNotes |
| Operating Systems | Xiaolin Visual System + CS guides | huihut/interview, muluoleiguo/interview |
| Computer Networking | Guides + TCP/IP Programming | huihut/interview, xiaolincoding.com |
| MySQL | Xiaolin Visual MySQL + MySQL Crash Course | GeeksforGeeks, yzhu798/CodingInterviewsNotes |
| Redis | Xiaolin Visual Redis + Xiaolin 150 MySQL+Redis | GeeksforGeeks, yzhu798/CodingInterviewsNotes |

#### High-Frequency Topic Quick Reference

| Topic | Recommended Resources |
|-------|----------------------|
| Smart pointers (shared\_ptr/unique\_ptr/weak\_ptr) | huihut/interview + cppreference |
| Virtual functions & polymorphism | GeeksforGeeks + huihut/interview |
| STL container internals | GeeksforGeeks C++ Tutorial |
| Move semantics & rvalue references | modern-cpp-features |
| Memory management & RAII | huihut/interview |
| Multithreading (thread/mutex/atomic) | cppreference + modern-cpp-features |
| C++11/14/17/20 features | modern-cpp-features |
| Algorithms & Data Structures | leetcode-master + CodeTop |

### Installation

#### Option 1: Clone Repository (Recommended)

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git ~/.claude/skills/Cpp-Interviewer
```

#### Option 2: Download

Download and extract the repository, then place the folder under `~/.claude/skills/`.

### Notes

- PDF books are managed with Git LFS. You need [Git LFS](https://git-lfs.github.com/) installed when cloning.
- Interview PDFs are encrypted files. The Skill parses content directly; some formatting may be incomplete.
- Recommended to use alongside online resources for comprehensive coverage.

### License

This project is licensed under the [MIT License](https://github.com/yiqi-7/Cpp-Interviewer/blob/main/LICENSE).

### Community

- Discussion group: Q 828570482
- Recognized by [LINUX DO](https://linux.do/) community
