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
│   └── 工具/                 # 开发工具
│       ├── gdb手册.pdf
│       ├── MySQL必知必会.pdf
│       └── 跟我一起写Makefile.pdf
└── README.md
```

## 书籍筛选说明

以面试官角度筛选，标准为：

| 标准 | 说明 |
|------|------|
| 面试直接相关 | 优先选择面试高频考点覆盖的书籍 |
| 经典权威 | Effective C++、深度探索C++对象模型等公认经典 |
| 实用性强 | gdb、MySQL、Makefile 等工具类面试也会问 |
| 体积合理 | 排除了超过 100MB 的书籍（如深入理解计算机系统 91MB、深入理解Linux网络 177MB） |

### 未收录的书籍及原因

| 书籍 | 原因 |
|------|------|
| 21天学通C++ | 入门级，面试深度不够 |
| 深入理解计算机系统（CSAPP） | 91MB 过大，且内容偏硬件底层 |
| 深入理解Linux网络 | 177MB 过大，内容偏专项 |
| 深入理解FFmpeg | 太专项，与 C++ 面试关联弱 |
| 分布式系统概念与设计 | C++ 实习面试较少涉及 |
| 编码：隐匿在计算机软硬件背后的语言 | 好书但面试直接关联弱 |
| TCP/IP网络编程（C++目录下） | 与系统与网络目录下重复 |

## 在线参考资源

### GitHub 开源仓库

| 仓库 | Stars | 内容 |
|------|-------|------|
| [huihut/interview](https://github.com/huihut/interview) | 37.8k | C/C++ 面试知识总结，涵盖语言、数据结构、算法、系统、网络、设计模式 |
| [leetcode-master](https://github.com/youngyangyang04/leetcode-master) | 61.3k | 代码随想录，200+ 道 LeetCode 题解，以 C++ 为主语言 |
| [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features) | 21.6k | C++11/14/17/20/23 新特性速查手册 |
| [TechCPP](https://github.com/youngyangyang04/TechCPP) | — | C++ 面试 & 学习指南知识点整理 |

### 在线学习 / 刷题平台

| 网站 | 内容 |
|------|------|
| [GeeksforGeeks C++ 面试题](https://www.geeksforgeeks.org/cpp/cpp-interview-questions/) | C++ 面试题合集，分类清晰，英文 |
| [GeeksforGeeks C++ 教程](https://www.geeksforgeeks.org/c-plus-plus/) | C++ 完整教程，从基础到高级 |
| [LeetCode 中国](https://leetcode.cn) | 算法刷题，支持 C++，有面试题讨论区 |
| [CodeTop](https://codetop.cc) | 按公司/岗位筛选高频面试题 |
| [牛客网](https://www.nowcoder.com/search?type=question&query=C%2B%2B) | 国内最大面试题库，有企业真题 |
| [cppreference](https://zh.cppreference.com) | C++ 标准库权威参考 |

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
git clone https://github.com/yiqi-7/-skills.git
# 将 skills/interview/ 复制到 ~/.claude/skills/interview/
```

### 方式二：直接使用

在仓库目录下使用 Claude Code，Skill 会自动识别。

## 注意事项

- PDF 书籍使用 Git LFS 管理，克隆时需要安装 [Git LFS](https://git-lfs.github.com/)
- 八股文 PDF 为加密文件，Skill 通过内容解析读取，部分格式可能不完整
- 建议结合在线资源一起使用，互相补充
