[English](#) | [中文](README.md)

# C++ Interview Skill

Simulates an interviewer to help you understand and master core C++ interview topics.

## Usage

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

## Features

- **Interviewer perspective**: Guides your thinking, asks follow-up questions, and highlights common pitfalls instead of giving direct answers
- **Three-level depth expansion**:
  - Level 1 - Explain the current topic thoroughly
  - Level 2 - Expand within the same domain (e.g., more C++ topics)
  - Level 3 - Cross-domain expansion (includes Level 2 + OS, networking, etc.)
- **Selectable answer style**: Concise mode (quick review) / Detailed mode (deep learning), switchable anytime
- **Progressive difficulty follow-ups**: 3-5 high-frequency interview follow-up questions after each answer, sorted from basic to advanced
- **Knowledge index system**: Quickly locate knowledge sources via `index/knowledge_index.json`; new books or URLs are automatically indexed
- **Auto-read reference materials**: Automatically references the PDFs and classic books in the repository

## Repository Structure

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

## Knowledge Index System

`index/knowledge_index.json` contains a structured index of 60+ interview topics, covering:

| Domain | Topics | Examples |
|--------|--------|----------|
| C++ Language | 15 | Pointers & references, smart pointers, vtable, move semantics... |
| STL | 4 | vector internals, map/unordered_map, iterator invalidation... |
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

**To add new books or URLs, just update the index file - no need to modify SKILL.md.**

## Online Reference Resources

### GitHub Repositories

| Repository | Stars | Content |
|-----------|-------|---------|
| [huihut/interview](https://github.com/huihut/interview) | 37.8k | C/C++ interview knowledge summary: language, DS, algorithms, systems, networking, design patterns |
| [muluoleiguo/interview](https://github.com/muluoleiguo/interview) | — | C++ backend interview knowledge: language basics, STL, OS, networking, databases |
| [yzhu798/CodingInterviewsNotes](https://github.com/yzhu798/CodingInterviewsNotes) | — | C++ interview notes: algorithms, OS, networking, databases, design patterns |
| [guaguaupup/cpp_interview](https://github.com/guaguaupup/cpp_interview) | — | C++ interview questions: language basics, STL, memory management, multithreading |
| [leetcode-master](https://github.com/youngyangyang04/leetcode-master) | 61.3k | Code Caprice, 200+ LeetCode solutions, primarily in C++ |
| [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features) | 21.6k | C++11/14/17/20/23 feature cheat sheet |
| [TechCPP](https://github.com/youngyangyang04/TechCPP) | — | C++ interview & study guide knowledge summary |

### Interview Guide Websites

| Website | Content |
|---------|---------|
| [interviewguide.cn](https://interviewguide.cn) | Interview guide covering C++, Java, frontend, algorithms, OS, networking, categorized by role |
| [小林coding](https://xiaolincoding.com) | Visual guides for networking, OS, MySQL, Redis with interview question summaries |

### Online Learning / Practice Platforms

| Website | Content |
|---------|---------|
| [GeeksforGeeks C++ Interview](https://www.geeksforgeeks.org/cpp/cpp-interview-questions/) | C++ interview questions, well-categorized, English |
| [GeeksforGeeks C++ Tutorial](https://www.geeksforgeeks.org/c-plus-plus/) | Complete C++ tutorial from basics to advanced |
| [LeetCode](https://leetcode.cn) | Algorithm practice, supports C++, has interview discussion forums |
| [CodeTop](https://codetop.cc) | Filter high-frequency interview questions by company/role |
| [牛客网](https://www.nowcoder.com/search?type=question&query=C%2B%2B) | China's largest interview question bank with real company questions |
| [cppreference](https://zh.cppreference.com) | Authoritative C++ standard library reference |

### Recommended Search Entry Points

- [GitHub C++ interview search](https://github.com/search?q=C%2B%2B+interview&type=repositories)
- [GitHub 八股文 search](https://github.com/search?q=C%2B%2B+%E5%85%AB%E8%82%A1%E6%96%87&type=repositories)
- [Zhihu C++ interview questions](https://www.zhihu.com/search?type=content&q=C%2B%2B%E9%9D%A2%E8%AF%95%E9%A2%98)
- [Juejin C++ interviews](https://juejin.cn/search?query=C%2B%2B%E9%9D%A2%E8%AF%95)

### Smart Resource Selection Strategy

The Skill automatically selects the best data source based on question type:

| Question Type | Primary Source | Supplementary Source |
|--------------|---------------|---------------------|
| C++ Language Basics | Local guides + Xiaolin 100 CPP questions | huihut/interview, guaguaupup/cpp_interview, muluoleiguo/interview |
| Modern C++ | modern-cpp-features | interviewguide.cn, GeeksforGeeks |
| STL Containers/Algorithms | Local STL Source Analysis | cppreference, huihut/interview |
| Virtual Functions/Polymorphism | Local Deep into C++ Object Model | huihut/interview, yzhu798/CodingInterviewsNotes |
| Smart Pointers/Memory | Local guides + Xiaolin 100 CPP questions | huihut/interview, guaguaupup/cpp_interview |
| Data Structures & Algorithms | Local algorithm guides | leetcode.cn, CodeTop, yzhu798/CodingInterviewsNotes |
| Operating Systems | Xiaolin Visual System + CS guides | huihut/interview, muluoleiguo/interview |
| Computer Networking | Guides + TCP/IP Programming | huihut/interview, xiaolincoding.com |
| MySQL | Xiaolin Visual MySQL + MySQL Crash Course | GeeksforGeeks, yzhu798/CodingInterviewsNotes |
| Redis | Xiaolin Visual Redis + Xiaolin 150 MySQL+Redis | GeeksforGeeks, yzhu798/CodingInterviewsNotes |
| C++ Backend Comprehensive | muluoleiguo/interview + local guides | huihut/interview, interviewguide.cn |
| Company-specific Questions | CodeTop + 牛客网 | leetcode.cn, interviewguide.cn |

### High-Frequency Topic Quick Reference

| Topic | Recommended Resources |
|-------|----------------------|
| Smart pointers (shared_ptr/unique_ptr/weak_ptr) | huihut/interview + cppreference |
| Virtual functions & polymorphism | GeeksforGeeks + huihut/interview |
| STL container internals | GeeksforGeeks C++ Tutorial |
| Move semantics & rvalue references | modern-cpp-features |
| Memory management & RAII | huihut/interview |
| Multithreading (thread/mutex/atomic) | cppreference + modern-cpp-features |
| C++11/14/17/20 features | modern-cpp-features |
| Algorithms & Data Structures | leetcode-master + CodeTop |

## Installation

### Option 1: Clone Repository

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
# Tell your local CLI to install the skill: https://github.com/yiqi-7/Cpp-Interviewer.git
```

### Option 2: Download

Download and extract the repository, then place the folder under `~/.claude/skills/`.

## Notes

- PDF books are managed with Git LFS. You need [Git LFS](https://git-lfs.github.com/) installed when cloning.
- Interview PDFs are encrypted files. The Skill parses content directly; some formatting may be incomplete.
- Recommended to use alongside online resources for comprehensive coverage.

## License

This project is licensed under the [MIT License](LICENSE).
