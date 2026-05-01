# C++ 面试八股文 Skill

一个 Claude Code Skill，模拟面试官角色，帮助你理解和掌握 C++ 面试中的核心知识点。

## 使用方式

```
/interview 虚函数是怎么实现的
/interview 智能指针有哪几种
/interview 什么是内存泄漏
```

## 功能特性

- **面试官视角**：不是直接给答案，而是引导你思考、追问细节、指出常见误区
- **三级深度扩展**：
  - Level 1 — 只讲当前知识点，讲透讲明白
  - Level 2 — 同方向扩展（如 C++ 语言范围内扩展）
  - Level 3 — 跨学科扩展（如 C++ → 操作系统 → 计算机网络）
- **参考资料自动读取**：回答时自动参考仓库中的八股文 PDF 和经典书籍

## 仓库结构

```
.
├── skills/
│   └── interview/
│       └── SKILL.md          # Skill 指令文件
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

## 在线参考资源

### GitHub 开源仓库

| 仓库 | Stars | 内容 |
|------|-------|------|
| [huihut/interview](https://github.com/huihut/interview) | 37.8k | C/C++ 面试知识总结，涵盖语言、数据结构、算法、系统、网络、设计模式 |
| [muluoleiguo/interview](https://github.com/muluoleiguo/interview) | — | C++ 后端面试知识汇总，涵盖语言基础、STL、操作系统、网络、数据库 |
| [yzhu798/CodingInterviewsNotes](https://github.com/yzhu798/CodingInterviewsNotes) | — | C++ 面试笔记，涵盖算法、操作系统、网络、数据库、设计模式 |
| [guaguaupup/cpp_interview](https://github.com/guaguaupup/cpp_interview) | — | C++ 面试题整理，语言基础、STL、内存管理、多线程 |
| [leetcode-master](https://github.com/youngyangyang04/leetcode-master) | 61.3k | 代码随想录，200+ 道 LeetCode 题解，以 C++ 为主语言 |
| [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features) | 21.6k | C++11/14/17/20/23 新特性速查手册 |
| [TechCPP](https://github.com/youngyangyang04/TechCPP) | — | C++ 面试 & 学习指南知识点整理 |

### 面试指南网站

| 网站 | 内容 |
|------|------|
| [interviewguide.cn](https://interviewguide.cn) | 面试指南，覆盖C++、Java、前端、算法、操作系统、网络等，按岗位分类 |
| [小林coding](https://xiaolincoding.com) | 图解计算机网络、操作系统、MySQL、Redis，面试题汇总 |

### 在线学习 / 刷题平台

| 网站 | 内容 |
|------|------|
| [GeeksforGeeks C++ 面试题](https://www.geeksforgeeks.org/cpp/cpp-interview-questions/) | C++ 面试题合集，分类清晰，英文 |
| [GeeksforGeeks C++ 教程](https://www.geeksforgeeks.org/c-plus-plus/) | C++ 完整教程，从基础到高级 |
| [LeetCode 中国](https://leetcode.cn) | 算法刷题，支持 C++，有面试题讨论区 |
| [CodeTop](https://codetop.cc) | 按公司/岗位筛选高频面试题 |
| [牛客网](https://www.nowcoder.com/search?type=question&query=C%2B%2B) | 国内最大面试题库，有企业真题 |
| [cppreference](https://zh.cppreference.com) | C++ 标准库权威参考 |
| [小林coding](https://xiaolincoding.com) | 图解计算机网络、操作系统、MySQL、Redis，面试题汇总 |

### 推荐搜索入口

- [GitHub C++ interview 搜索](https://github.com/search?q=C%2B%2B+interview&type=repositories)
- [GitHub 八股文搜索](https://github.com/search?q=C%2B%2B+%E5%85%AB%E8%82%A1%E6%96%87&type=repositories)
- [知乎 C++ 面试题](https://www.zhihu.com/search?type=content&q=C%2B%2B%E9%9D%A2%E8%AF%95%E9%A2%98)
- [掘金 C++ 面试](https://juejin.cn/search?query=C%2B%2B%E9%9D%A2%E8%AF%95)

### 智能资源选择策略

Skill 会根据问题类型自动选择最合适的数据源：

| 问题类型 | 首选数据源 | 补充数据源 |
|---------|-----------|-----------|
| C++ 语言基础 | 本地八股文 + 小林100道CPP面试题 | huihut/interview、guaguaupup/cpp_interview、muluoleiguo/interview |
| C++ 新特性 | modern-cpp-features | interviewguide.cn、GeeksforGeeks |
| STL 容器/算法原理 | 本地STL源码剖析 | cppreference、huihut/interview |
| 虚函数/多态/对象模型 | 本地深度探索C++对象模型 | huihut/interview、yzhu798/CodingInterviewsNotes |
| 智能指针/内存管理 | 本地八股文 + 小林100道CPP面试题 | huihut/interview、guaguaupup/cpp_interview |
| 数据结构与算法 | 本地八股文算法篇 | leetcode.cn、CodeTop、yzhu798/CodingInterviewsNotes |
| 操作系统 | 小林图解系统 + 八股文计算机基础篇 | huihut/interview、muluoleiguo/interview |
| 计算机网络 | 八股文 + TCP/IP网络编程 | huihut/interview、xiaolincoding.com |
| MySQL 数据库 | 小林图解MySQL + MySQL必知必会 | GeeksforGeeks、yzhu798/CodingInterviewsNotes |
| Redis 缓存 | 小林图解Redis + 小林150道MySQL+Redis面试题 | GeeksforGeeks、yzhu798/CodingInterviewsNotes |
| C++ 后端综合 | muluoleiguo/interview + 本地八股文 | huihut/interview、interviewguide.cn |
| 某公司高频题 | CodeTop + 牛客网 | leetcode.cn、interviewguide.cn |

### 高频考点速查

| 考点 | 推荐资料 |
|------|---------|
| 智能指针（shared_ptr/unique_ptr/weak_ptr） | huihut/interview + cppreference |
| 虚函数与多态 | GeeksforGeeks + huihut/interview |
| STL 容器底层原理 | GeeksforGeeks C++ 教程 |
| 移动语义与右值引用 | modern-cpp-features |
| 内存管理与 RAII | huihut/interview |
| 多线程（thread/mutex/atomic） | cppreference + modern-cpp-features |
| C++11/14/17/20 新特性 | modern-cpp-features |
| 算法与数据结构 | leetcode-master + CodeTop |

## 安装方式

### 方式一：克隆仓库

```bash
git clone https://github.com/yiqi-7/Cpp-Interviewer.git
# 将 skills/interview/ 复制到 ~/.claude/skills/interview/
```

### 方式二：直接使用

在仓库目录下使用 Claude Code，Skill 会自动识别。

## 注意事项

- PDF 书籍使用 Git LFS 管理，克隆时需要安装 [Git LFS](https://git-lfs.github.com/)
- 八股文 PDF 为加密文件，Skill 通过内容解析读取，部分格式可能不完整
- 建议结合在线资源一起使用，互相补充

## 开源许可

本项目采用 [MIT License](LICENSE) 开源。
