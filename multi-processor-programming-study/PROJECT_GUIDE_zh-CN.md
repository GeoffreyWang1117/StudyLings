# 多处理器编程学习项目 - 完整指南

[English Version](PROJECT_SUMMARY.md) | 中文版

🚀 基于《多处理器编程的艺术》的 Rustlings 风格交互式学习项目

---

## 📚 项目概览 | Project Overview

这是一个全面的、渐进式的多处理器编程学习平台，提供 **Java** 和 **C++** 双语言实现（Java 17+，C++20+）。

### 🎉 项目状态：已完成！

**43 个练习文件** | **93+ 个算法** | **20 周学习路径**

### ✅ 完成情况

- ✅ **第一部分**：基础知识（第 1-11 章）- 已完成
- ✅ **第二部分**：实践篇（第 12-19 章）- 已完成
- ✅ **阶段 5**：内存回收与工作窃取 - 已完成
- ✅ **阶段 6**：优先队列、RCU、内存模型 - 已完成
- ✅ **阶段 7**：并行算法 - 已完成

### 📊 项目统计

#### 练习文件
- **Java**：24 个练习文件，包含 55+ 个算法
- **C++**：19 个练习文件，包含 38+ 个算法
- **总计**：43 个练习文件，93+ 个算法

#### 解决方案
- **Java 参考解答**：6 个完整实现
- **C++ 参考解答**：6 个完整实现
- **总计**：12 个完整解决方案文件

#### 文档资源
- 9 个主要文档文件
- 2,500+ 行详细文档
- 硬件需求分析
- 第二版覆盖分析

---

## 🎯 学习路径（20 周） | Learning Path (20 Weeks)

### 第一部分：基础知识（11 周）

#### 第 1-2 周：并发基础
**章节**：第 1 章 - 基础知识

**学习内容**：
- ✅ 线程创建和生命周期
- ✅ 竞态条件的理解和观察
- ✅ 基本的互斥同步（synchronized/mutex）

**练习**：
- `Exercise01_HelloThreads.java/cpp` - 线程创建
- `Exercise02_RaceCondition.java/cpp` - 竞态条件演示
- `Exercise03_Synchronization.java/cpp` - 同步机制

**关键概念**：
- 共享内存并发模型
- 线程安全问题
- 互斥与同步

---

#### 第 3-4 周：互斥算法
**章节**：第 2 章 - 互斥

**学习内容**：
- ✅ Peterson 锁（双线程互斥）
- ✅ Filter 锁（n 线程互斥）
- ✅ 内存可见性与原子性
- ✅ C++ 内存顺序（memory_order）

**练习**：
- `Exercise01_PetersonLock.java/cpp` - Peterson 算法
- `Exercise02_FilterLock.java/cpp` - Filter 算法
- `exercise03_memory_ordering.cpp` - C++ 内存顺序（新增！）

**关键概念**：
- volatile/atomic 变量
- happens-before 关系
- acquire/release 语义
- 内存屏障

**硬件要求**：
- 最低：2 核心
- 推荐：4+ 核心
- 最佳：ARM/RISC-V（弱内存架构更能体现效果）

---

#### 第 5-6 周：并发对象
**章节**：第 3 章 - 并发对象

**学习内容**：
- ✅ 顺序一致性（Sequential Consistency）
- ✅ 线性化（Linearizability）
- ✅ 进展条件（wait-free, lock-free, obstruction-free）

**练习**：
- `Exercise01_SequentialConsistency.java/cpp` - 顺序一致性
- `Exercise02_Linearizability.java` - 线性化
- `Exercise03_ProgressConditions.java` - 进展条件

**关键概念**：
- 正确性条件
- 线性化点
- 无等待、无锁、无阻塞

---

#### 第 7 周：同步原语
**章节**：第 4-5 章 - 基础与同步原语

**学习内容**：
- ✅ 原子寄存器构造
- ✅ Compare-And-Swap (CAS)
- ✅ ABA 问题

**练习**：
- `Exercise01_AtomicRegisters.java` - 原子寄存器
- `Exercise01_CompareAndSwap.java` - CAS 操作

**关键概念**：
- CAS 原子操作
- ABA 问题及解决方案
- 无锁数据结构基础

---

#### 第 8 周：共识
**章节**：第 6 章 - 共识

**学习内容**：
- ✅ 共识问题
- ✅ 共识层级
- ✅ 通用性（Universality）

**练习**：
- `Exercise01_Consensus.java` - 共识与通用构造

**关键概念**：
- 共识数（Consensus Number）
- 等待自由的通用构造
- CAS 的通用性

---

#### 第 9 周：自旋锁
**章节**：第 7 章 - 自旋锁

**学习内容**：
- ✅ TAS Lock（Test-And-Set）
- ✅ TTAS Lock（Test-And-Test-And-Set）
- ✅ Backoff Lock（指数退避）
- ✅ Anderson Lock（队列锁）
- ✅ MCS Lock（可扩展队列锁）

**练习**：
- `Exercise01_SpinLocks.java/cpp` - 5 种自旋锁实现

**关键概念**：
- 缓存一致性
- 争用管理
- 队列锁的可扩展性

**硬件要求**：
- 最低：4 核心
- 推荐：8+ 核心
- 最佳：16+ 核心（性能差异显著）

⚠️ **注意**：此练习对硬件敏感度最高！

---

#### 第 10 周：监视器与阻塞同步
**章节**：第 8 章 - 监视器

**学习内容**：
- ✅ 条件变量
- ✅ 有界缓冲区（生产者-消费者）
- ✅ 读写锁
- ✅ 哲学家就餐问题（死锁避免）

**练习**：
- `Exercise01_Monitors.java` - 监视器和阻塞同步

**关键概念**：
- Lock 和 Condition API
- 经典同步问题
- 死锁避免策略

---

#### 第 11 周：并发数据结构（链表、队列、栈）
**章节**：第 9-11 章

**学习内容**：

**链表（第 9 章）**：
- ✅ 粗粒度同步（单锁）
- ✅ 细粒度同步（手递手锁定）
- ✅ 乐观同步（无锁遍历 + 验证）
- ✅ 惰性同步（逻辑删除 + 物理删除）

**队列（第 10 章）**：
- ✅ 有界阻塞队列
- ✅ 无界队列（分离锁）
- ✅ Michael-Scott 无锁队列

**栈（第 11 章）**：
- ✅ 基于锁的栈
- ✅ Treiber 无锁栈
- ✅ 消除退避栈

**练习**：
- `Exercise01_ConcurrentLists.java` - 链表
- `Exercise01_ConcurrentQueues.java/cpp` - 队列
- `Exercise01_ConcurrentStacks.java/cpp` - 栈

**关键概念**：
- 同步策略权衡
- 无锁数据结构
- 消除技术

**硬件要求**：
- 最低：4 核心
- 推荐：8+ 核心（消除退避栈）

---

### 第二部分：实践篇（9 周）

#### 第 12 周：共识与通用构造（复习）
- 深入理解共识层级
- 实现通用构造
- 探索 CAS 的强大能力

---

#### 第 13 周：监视器（复习）
- 经典同步问题
- 条件变量的正确使用
- 死锁避免技术

---

#### 第 14 周：并行计数
**章节**：第 12 章 - 计数、排序与协调

**学习内容**：
- ✅ 缓存行填充计数器（防止伪共享）
- ✅ 条带化计数器（负载分布）
- ✅ 组合计数器（线程本地聚合）
- ✅ 并行数组求和（Fork/Join）

**练习**：
- `Exercise01_ParallelCounting.java/cpp` - 并行计数

**关键概念**：
- 伪共享（False Sharing）
- 缓存行对齐（`alignas(64)` in C++）
- 动态条带化（类似 Java LongAdder）

**硬件要求**：
- 最低：4 核心
- 推荐：8+ 核心
- 最佳：16+ 核心（伪共享效果显著）

---

#### 第 15 周：并发哈希表
**章节**：第 13 章 - 并发哈希

**学习内容**：
- ✅ 条带化哈希表（锁分段）
- ✅ 无锁哈希表（基于 CAS）
- ✅ 布谷鸟哈希（双表位移）

**练习**：
- `Exercise01_ConcurrentHashMap.java` - 并发哈希表

**关键概念**：
- 锁分段技术
- 开放寻址 vs 闭合寻址
- 布谷鸟哈希的位移策略

---

#### 第 16 周：跳表
**章节**：第 14 章 - 跳表与平衡搜索

**学习内容**：
- ✅ 无锁跳表实现
- ✅ 惰性删除与标记
- ✅ 概率性层级生成

**练习**：
- `Exercise01_ConcurrentSkipList.java` - 并发跳表

**关键概念**：
- 概率数据结构
- O(log n) 期望时间复杂度
- 惰性删除模式

---

#### 第 17 周：事务内存
**章节**：第 18 章 - 事务内存

**学习内容**：
- ✅ 软件事务内存（STM）
- ✅ 乐观并发控制
- ✅ 读写集跟踪
- ✅ 自动冲突重试

**练习**：
- `Exercise01_STM.java` - 软件事务内存

**关键概念**：
- ACID 属性
- 版本化并发控制
- 事务组合

---

#### 第 18 周：内存回收与工作窃取 🆕
**阶段 5**：高优先级新增内容

**学习内容**：

**内存回收**：
- ✅ Hazard Pointers 协议
- ✅ 保护指针机制
- ✅ 延迟删除
- ✅ 无锁栈的安全内存回收

**工作窃取**：
- ✅ Chase-Lev 工作窃取双端队列
- ✅ 所有者操作（底部 push/pop，LIFO）
- ✅ 窃取者操作（顶部 steal，FIFO）
- ✅ 动态数组扩容
- ✅ 任务并行基础

**练习**：
- `Exercise01_HazardPointers.java/cpp` - Hazard Pointers
- `Exercise01_WorkStealingDeque.java/cpp` - 工作窃取双端队列

**完整解决方案**：
- `solutions/java/HazardPointers_Solution.java`
- `solutions/cpp/hazard_pointers_solution.cpp`
- `solutions/java/WorkStealingDeque_Solution.java`
- `solutions/cpp/work_stealing_deque_solution.cpp`

**关键概念**：
- 内存回收问题（use-after-free）
- 保护协议（set, re-read, verify）
- 非对称双端队列
- 负载均衡

**应用场景**：
- Java ForkJoinPool（使用类似算法）
- .NET Task Parallel Library
- Intel TBB
- Rust Rayon

**重要性**：
- 🔥 **C++ 关键**：无锁结构没有内存回收是不安全的
- 📚 **Java 教育性**：理解 GC 为你做了什么
- 🌉 **跨语言**：理解 C++/Java 互操作性

**硬件要求**：
- 最低：4 核心
- 推荐：8+ 核心
- 最佳：16+ 核心（负载均衡效果显著）

---

#### 第 19 周：优先队列与 RCU 🆕
**阶段 6**：中优先级新增内容

**学习内容**：

**优先队列**：
- ✅ 基于锁的堆优先队列
- ✅ 基于跳表的优先队列（更好的并发性）
- ✅ 放松的优先队列（有界误差，高可扩展性）

**RCU（读-复制-更新）**：
- ✅ 简单 RCU 机制
- ✅ RCU 保护的链表
- ✅ 宽限期概念
- ✅ 与基于锁的方法比较

**练习**：
- `Exercise01_ConcurrentPriorityQueue.java/cpp` - 优先队列
- `Exercise01_RCU.java/cpp` - RCU

**关键概念**：

**优先队列**：
- 根节点争用问题
- 严格顺序 vs 放松语义权衡
- 分段分布

**RCU**：
- 读端：零开销（无锁、无原子操作）
- 写端：复制-更新-等待模式
- 宽限期：等待所有读者完成
- 发布-订阅模型

**应用场景**：
- 任务调度器
- 事件驱动系统
- 图算法（Dijkstra，A*）
- Linux 内核（网络、VFS、调度器中广泛使用）

**硬件要求**：
- 最低：4 核心
- 推荐：8+ 核心
- 最佳：16+ 核心（RCU 读可扩展性显著）

---

#### 第 20 周：并行算法 🆕
**阶段 7**：并行算法

**学习内容**：
- ✅ 并行归并排序（ForkJoinPool / std::async）
- ✅ 并行快速排序（并发分区）
- ✅ 顺序截止优化（10,000 元素）
- ✅ 与内置并行排序比较
- ✅ 大数组性能基准测试

**练习**：
- `Exercise01_ParallelSorting.java/cpp` - 并行排序

**关键概念**：
- 分治并行
- 顺序截止阈值
- 工作窃取调度器（ForkJoinPool）
- 缓存局部性 vs 并行性权衡
- 任务粒度调优

**实现对比**：

1. **并行归并排序**：
   - ✅ 稳定排序（保持相等元素顺序）
   - ✅ 可预测的分割（总在中点）
   - ⚠️ 需要额外内存（临时数组）
   - 使用场景：需要稳定性时

2. **并行快速排序**：
   - ✅ 原地排序（无额外内存）
   - ✅ 良好的缓存局部性
   - ⚠️ 枢轴选择影响平衡
   - 使用场景：内存受限时

**应用场景**：
- 大数据集处理
- 数据库查询优化
- MapReduce 风格计算
- 科学计算

**内置替代方案**：
- **Java**：`Arrays.parallelSort()`（使用类似算法）
- **C++**：`std::execution::par` 策略（C++17）

**硬件要求**：
- 最低：4 核心（基本加速可观察）
- 推荐：8+ 核心（显著加速）
- 最佳：16+ 核心（戏剧性性能提升）
- 数组大小：1000 万+ 元素以获得最佳演示效果

---

## 🏗️ 项目结构 | Project Structure

```
multi-processor-programming-study/
├── README.md                           # 项目主说明文件
├── PROJECT_SUMMARY.md                  # 英文项目总结
├── PROJECT_GUIDE_zh-CN.md             # 中文完整指南（本文件）
├── EXERCISES_OVERVIEW.md               # 练习概览（43 个练习详解）
│
├── exercises/                          # 练习目录
│   ├── java/                          # Java 练习（24 个文件）
│   │   ├── pom.xml                    # Maven 配置
│   │   └── src/main/java/com/multiprocessor/
│   │       ├── basics/                # 第 1 章：基础
│   │       ├── mutual_exclusion/      # 第 2 章：互斥
│   │       ├── concurrent_objects/    # 第 3 章：并发对象
│   │       ├── foundations/           # 第 4 章：基础
│   │       ├── synchronization/       # 第 5 章：同步原语
│   │       ├── consensus/             # 第 6 章：共识
│   │       ├── spin_locks/            # 第 7 章：自旋锁
│   │       ├── monitors/              # 第 8 章：监视器
│   │       ├── linked_lists/          # 第 9 章：链表
│   │       ├── queues/                # 第 10 章：队列
│   │       ├── stacks/                # 第 11 章：栈
│   │       └── part2/                 # 第二部分
│   │           ├── counting/          # 第 12 章：计数
│   │           ├── hashing/           # 第 13 章：哈希
│   │           ├── skiplists/         # 第 14 章：跳表
│   │           ├── transactional_memory/  # 第 18 章：事务内存
│   │           ├── memory_reclamation/    # 内存回收 🆕
│   │           ├── work_stealing/         # 工作窃取 🆕
│   │           ├── priority_queues/       # 优先队列 🆕
│   │           ├── rcu/                   # RCU 🆕
│   │           └── parallel_algorithms/   # 并行算法 🆕
│   │
│   └── cpp/                           # C++ 练习（19 个文件）
│       ├── CMakeLists.txt             # CMake 配置
│       ├── 01_basics/                 # 第 1 章：基础
│       ├── 02_mutual_exclusion/       # 第 2 章：互斥
│       ├── 03_concurrent_objects/     # 第 3 章：并发对象
│       ├── 07_spin_locks/             # 第 7 章：自旋锁
│       ├── 10_queues/                 # 第 10 章：队列
│       ├── 11_stacks/                 # 第 11 章：栈
│       └── part2/                     # 第二部分
│           ├── counting/              # 计数
│           ├── memory_reclamation/    # 内存回收 🆕
│           ├── work_stealing/         # 工作窃取 🆕
│           ├── priority_queues/       # 优先队列 🆕
│           ├── rcu/                   # RCU 🆕
│           └── parallel_algorithms/   # 并行算法 🆕
│
├── solutions/                          # 参考解答（12 个文件）
│   ├── java/                          # Java 解答
│   │   ├── Exercise01_HelloThreads_Solution.java
│   │   ├── Exercise02_RaceCondition_Solution.java
│   │   ├── Exercise01_PetersonLock_Solution.java
│   │   ├── HazardPointers_Solution.java        🆕
│   │   └── WorkStealingDeque_Solution.java     🆕
│   │
│   └── cpp/                           # C++ 解答
│       ├── exercise01_hello_threads_solution.cpp
│       ├── exercise01_peterson_lock_solution.cpp
│       ├── lock_free_stack_solution.cpp
│       ├── hazard_pointers_solution.cpp        🆕
│       └── work_stealing_deque_solution.cpp    🆕
│
└── docs/                               # 文档目录
    ├── getting_started.md             # 入门指南
    ├── learning_path.md               # 学习路径
    ├── concepts.md                    # 核心概念深入解析
    ├── CPU_REQUIREMENTS.md            # CPU 硬件需求分析
    └── SECOND_EDITION_TOPICS.md       # 第二版覆盖分析
```

---

## 💻 硬件需求 | Hardware Requirements

不同练习对硬件的要求不同，以充分观察并发编程现象：

### 基本分类

#### 最低配置（2-4 核心）
**学习价值**：~60%
- ✅ 正确性理解
- ✅ 基本概念学习
- ❌ 性能差异不明显
- ❌ 可扩展性无法体现

**推荐练习**：
- 第 1-6 章（基础和正确性）
- 第 8 章（监视器）

---

#### 推荐配置（8 核心）
**学习价值**：~85%
- ✅ 大多数练习有意义
- ✅ 基本的争用和可扩展性可观察
- ✅ 性能差异开始显现
- ⚠️ 高级优化效果不够显著

**推荐练习**：
- 所有基础章节
- 第 7 章（自旋锁）- 部分效果
- 第 11 章（消除退避）- 部分效果
- 第 12 章（并行计数）- 部分效果

---

#### 最佳配置（16+ 核心）
**学习价值**：~95%
- ✅ 所有练习达到完整教育价值
- ✅ 性能差异显著
- ✅ 可扩展性问题明显
- ✅ 高级算法的复杂性得到证明

**推荐练习**：
- 所有练习！
- 第 7 章（自旋锁）- 完整效果
- 第 11 章（消除退避）- 完整效果
- 第 12 章（并行计数）- 完整效果

---

### 硬件敏感度最高的练习

#### 🔥 极高敏感度（16+ 核心必需）

1. **第 7 章：自旋锁**
   - MCS Lock 的可扩展性
   - Anderson Lock 的数组队列
   - Backoff 的指数退避
   - **硬件要求**：16+ 核心高度推荐

2. **第 11 章：消除退避栈**
   - 消除技术的效果
   - 高争用场景
   - **硬件要求**：16+ 核心高度推荐

3. **第 12 章：并行计数**
   - 伪共享的观察
   - 条带化效果
   - **硬件要求**：16+ 核心以获得戏剧性效果

4. **阶段 5：工作窃取**
   - 负载均衡效果
   - 窃取行为观察
   - **硬件要求**：16+ 核心以观察完整效果

---

#### ⚠️ 高敏感度（8+ 核心推荐）

5. **第 10 章：无锁队列**
   - Michael-Scott 队列性能
   - ABA 问题演示
   - **硬件要求**：8+ 核心

6. **第 13 章：并发哈希表**
   - 锁分段效果
   - 布谷鸟哈希位移
   - **硬件要求**：8+ 核心

7. **阶段 5：Hazard Pointers**
   - 回收开销观察
   - 高线程流失率
   - **硬件要求**：8+ 核心

8. **阶段 6：优先队列**
   - 根节点争用
   - 放松语义的可扩展性
   - **硬件要求**：8+ 核心

9. **阶段 6：RCU**
   - 读可扩展性
   - 读密集型工作负载（90%+ 读）
   - **硬件要求**：8+ 核心，16+ 最佳

10. **阶段 7：并行排序**
    - 加速比观察
    - 任务并行效果
    - **硬件要求**：8+ 核心

---

#### ✅ 低敏感度（2-4 核心足够）

- 第 1 章：基础
- 第 2 章：互斥算法
- 第 3 章：并发对象
- 第 4 章：基础
- 第 5 章：同步原语
- 第 6 章：共识
- 第 8 章：监视器
- 第 9 章：链表

---

### 特殊硬件考虑

#### ARM/RISC-V（弱内存架构）
**推荐练习**：
- 第 2 章：Peterson Lock（内存顺序效果明显）
- C++ 内存顺序练习（`exercise03_memory_ordering.cpp`）
- **教育价值**：异常高
- **原因**：x86 强内存模型隐藏许多 bug

#### x86（强内存模型）
- 大多数内存顺序 bug 被隐藏
- 使用 ThreadSanitizer 检测问题
- 仍能学习概念，但效果不如弱内存架构

---

### 云平台选项（硬件不足时）

如果您的硬件有限，可以使用云实例：

#### AWS EC2
- **c5.4xlarge**：16 核心，适合高敏感度练习
- **c5.2xlarge**：8 核心，适合大多数练习
- **费用**：按小时计费

#### Azure
- **F16s v2**：16 核心
- **F8s v2**：8 核心

#### Google Cloud Platform (GCP)
- **c2-standard-16**：16 核心
- **c2-standard-8**：8 核心

#### GitHub Actions
- **免费**：2 核心
- 适合基本测试和 CI/CD

---

## 🚀 快速开始 | Getting Started

### 前置条件

#### Java 练习
- Java 17 或更高版本（推荐 OpenJDK）
- Maven 3.6+ 或 Gradle 7.0+

#### C++ 练习
- C++20 兼容编译器
  - GCC 10+ 或
  - Clang 12+ 或
  - MSVC 2019+
- CMake 3.20+

---

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd multi-processor-programming-study

# Java 构建
cd exercises/java
mvn clean install

# C++ 构建
cd exercises/cpp
mkdir build && cd build
cmake ..
make
```

---

### 运行练习

#### Java

```bash
cd exercises/java

# 运行所有测试
mvn test

# 运行特定练习
mvn exec:java -Dexec.mainClass="com.multiprocessor.basics.Exercise01_HelloThreads"

# 运行特定测试
mvn test -Dtest=Exercise01Test
```

#### C++

```bash
cd exercises/cpp/build

# 运行所有测试
ctest

# 运行特定练习
./01_basics/exercise01_hello_threads

# 运行自旋锁练习
./07_spin_locks/exercise01_spin_locks
```

---

## 📖 如何使用 | How to Use

### 学习流程

1. **从基础开始**
   - 从第 1 模块开始，选择您喜欢的语言（Java 或 C++）
   - 建议两种语言都尝试以获得完整理解

2. **阅读练习说明**
   - 每个文件包含详细的说明和 TODO 标记
   - 理解概念后再开始编码

3. **实现解决方案**
   - 填写标记为 TODO 或 FIXME 的代码
   - 不要急于查看解答

4. **运行测试**
   - 使用测试框架验证您的实现
   - 所有测试应该通过

5. **对比参考解答**
   - 完成后，检查 solutions/ 目录
   - 理解不同的实现方式

6. **进入下一个练习**
   - 按顺序进行以获得最佳学习效果
   - 不要跳过基础练习

---

### 练习格式

每个练习文件包含：
- **概念说明**：您将学到什么
- **TODO 标记**：需要编写代码的位置
- **测试**：自动验证正确性
- **提示**：如果卡住了，参考注释

#### 示例

```java
// 练习：实现一个带有竞态条件演示的简单计数器
// TODO: 实现 increment() 方法
// 提示：思考多个线程访问时会发生什么

public class Counter {
    private int count = 0;

    public void increment() {
        // TODO: 实现此方法
        // count++;  // 这是线程安全的吗？
    }

    public int getCount() {
        return count;
    }
}
```

---

## 🌟 核心算法列表 | Core Algorithms

### 第一部分：基础算法（30+ 个）

#### 互斥算法
- Peterson Lock（两线程互斥）
- Filter Lock（n 线程互斥）

#### 自旋锁（5 个）
- TAS Lock
- TTAS Lock
- Backoff Lock
- Anderson Lock
- MCS Lock

#### 链表（4 个实现）
- Coarse-Grained List
- Fine-Grained List
- Optimistic List
- Lazy List

#### 队列（3 个实现）
- Bounded Blocking Queue
- Unbounded Queue
- Michael-Scott Lock-Free Queue

#### 栈（3 个实现）
- Lock-Based Stack
- Treiber Stack（无锁）
- Elimination Backoff Stack

---

### 第二部分：高级算法（63+ 个）

#### 计数与归约
- Combining Counter
- Striped Counter
- Cache-Line Padded Counter
- Parallel Array Sum

#### 哈希表（3 个实现）
- Striped Hash Map
- Lock-Free Hash Map
- Cuckoo Hash Map

#### 跳表
- Lock-Free Skip List

#### 同步模式
- Universal Consensus
- Bounded Buffer
- Readers-Writers Lock
- Dining Philosophers
- Barrier

#### 高级技术
- Software Transactional Memory
- Hazard Pointers 🆕
- Work-Stealing Deque 🆕
- Priority Queues（3 个实现）🆕
- RCU 🆕
- Parallel Sorting（2 个实现）🆕

---

## 🔑 关键概念 | Key Concepts

### 正确性条件
- **顺序一致性（Sequential Consistency）**：存在全局操作序列
- **线性化（Linearizability）**：存在线性化点，像原子操作
- **无阻塞性（Non-blocking）**：系统总能进展

### 进展条件
- **Wait-Free（无等待）**：每个线程在有限步骤内完成
- **Lock-Free（无锁）**：至少一个线程在有限步骤内完成
- **Obstruction-Free（无障碍）**：单独运行时能完成
- **Blocking（阻塞）**：可能无限等待

### 同步技术
- **锁（Locks）**：互斥访问
- **原子操作（Atomic Operations）**：CAS, TAS, FAA
- **内存模型（Memory Models）**：happens-before, synchronizes-with

### 性能优化
- **缓存行对齐**：防止伪共享
- **指数退避**：减少争用
- **条带化**：分布负载
- **消除**：配对操作

---

## 📚 文档资源 | Documentation Resources

### 主要文档

1. **[EXERCISES_OVERVIEW.md](EXERCISES_OVERVIEW.md)**
   - 所有 43 个练习的完整目录
   - 每个练习的详细说明
   - 关键概念和硬件要求

2. **[docs/learning_path.md](docs/learning_path.md)**
   - 20 周结构化学习路径
   - 每周学习目标
   - 推荐阅读材料

3. **[docs/concepts.md](docs/concepts.md)**
   - 核心概念深入解析
   - 正确性条件详解
   - 进展条件比较

4. **[docs/CPU_REQUIREMENTS.md](docs/CPU_REQUIREMENTS.md)**
   - 详细的硬件需求分析
   - 每个练习的核心数要求
   - 云平台选项

5. **[docs/SECOND_EDITION_TOPICS.md](docs/SECOND_EDITION_TOPICS.md)**
   - 第二版新增主题分析
   - 实现优先级
   - 阶段 5、6、7 详情

6. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - 英文项目总结
   - 完整算法目录
   - 项目指标

7. **[docs/getting_started.md](docs/getting_started.md)**
   - 安装和设置指南
   - 故障排除
   - 常见问题

---

## 🎓 学习建议 | Learning Tips

### 基于您的硬件

#### 如果您有 2-4 核心
- 专注于第 1-6、8 章（正确性和基础）
- 跳过性能比较部分
- 使用云实例进行高核心实验
- 您仍能获得 ~60% 的教育价值

#### 如果您有 8 核心
- 所有章节都有价值
- 可以观察基本的争用和可扩展性
- 适合大多数学习目标
- 您能获得 ~85% 的教育价值

#### 如果您有 16+ 核心
- 所有练习达到完整教育价值
- 性能差异显著
- 高级算法的复杂性得到证明
- 您能获得 ~95% 的教育价值
- 强烈推荐认真学习

---

### 基于您的语言

#### Java 开发者
- 完成所有 24 个 Java 练习
- 欣赏垃圾回收为您做了什么
- 专注于算法理解，而非手动内存管理
- Hazard Pointers 练习帮助理解 GC 的价值

#### C++ 开发者
- 完成所有 19 个 C++ 练习
- 内存回收练习**至关重要**
- 专注于生产就绪的安全无锁代码
- 理解 C++ 内存模型的细微差别

#### 双语言学习者
- 最佳学习体验
- 理解内存模型差异
- 跨语言并发编程技能
- 深刻理解高级和低级抽象

---

### 学习节奏

#### 快速通道（10-12 周）
- 仅 Java 或仅 C++
- 专注于核心练习
- 跳过一些性能比较

#### 标准通道（20 周）
- 双语言学习
- 完成所有练习
- 深入理解概念

#### 深入通道（30+ 周）
- 双语言学习
- 实现变体算法
- 阅读原始论文
- 贡献到开源项目

---

## 🎯 学习成果 | Learning Outcomes

完成本项目后，您将能够：

### 理解核心概念
- ✅ 线程安全和竞态条件
- ✅ 互斥和同步
- ✅ 原子操作和 CAS
- ✅ 内存模型和内存顺序
- ✅ 正确性条件（线性化、顺序一致性）
- ✅ 进展条件（无等待、无锁、阻塞）

### 实现经典算法
- ✅ Peterson Lock、Filter Lock
- ✅ 各种自旋锁（TAS, TTAS, MCS, Anderson）
- ✅ Treiber Stack（无锁栈）
- ✅ Michael-Scott Queue（无锁队列）
- ✅ 各种同步策略的链表

### 掌握高级技术
- ✅ 软件事务内存（STM）
- ✅ Hazard Pointers（内存回收）
- ✅ 工作窃取（Chase-Lev 算法）
- ✅ RCU（读-复制-更新）
- ✅ 并发优先队列
- ✅ 并行算法

### 优化性能
- ✅ 识别和避免伪共享
- ✅ 使用缓存行对齐
- ✅ 实现指数退避
- ✅ 应用条带化技术
- ✅ 使用消除优化

### 编写生产代码
- ✅ 安全的无锁数据结构（C++）
- ✅ 高性能并发代码
- ✅ 正确使用 Java 并发 API
- ✅ 正确使用 C++ 内存模型
- ✅ 避免常见陷阱（ABA、内存泄漏）

---

## 🔧 开发工具 | Development Tools

### 推荐工具

#### Java
- **IDE**：IntelliJ IDEA, Eclipse, VS Code
- **构建工具**：Maven, Gradle
- **测试框架**：JUnit 5
- **性能分析**：JProfiler, VisualVM
- **并发调试**：Java Flight Recorder

#### C++
- **IDE**：CLion, VS Code, Visual Studio
- **构建工具**：CMake
- **测试框架**：Google Test
- **性能分析**：perf, Valgrind
- **并发调试**：ThreadSanitizer, Helgrind

---

### 调试并发问题

#### ThreadSanitizer（推荐！）
```bash
# C++ with ThreadSanitizer
cmake -DCMAKE_CXX_FLAGS="-fsanitize=thread -g" ..
make
./exercise

# Java with ThreadSanitizer (experimental)
java -XX:+UseG1GC -Xmx4g YourClass
```

#### Valgrind Helgrind
```bash
valgrind --tool=helgrind ./exercise
```

#### Java Flight Recorder
```bash
java -XX:+UnlockCommercialFeatures \
     -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=recording.jfr \
     YourClass
```

---

## 📊 项目指标 | Project Metrics

### 开发时间线

#### 阶段 1-4（初始开发）
- 第 1 部分：基础练习（第 1-11 章）
- Java 和 C++ 实现
- 基本文档
- **时间**：约 40 小时

#### 阶段 5（高优先级新增）
- Hazard Pointers（Java & C++）
- Work-Stealing Deque（Java & C++）
- 完整解决方案
- **时间**：约 5.5 小时

#### 阶段 6（中优先级新增）
- Priority Queues（Java & C++）
- RCU（Java & C++）
- Enhanced Memory Model（C++）
- **时间**：约 6.5 小时

#### 阶段 7（并行算法）
- Parallel Sorting（Java & C++）
- 综合项目文档
- **时间**：约 2.5 小时

**总开发时间**：约 54.5 小时

---

### 代码统计

#### Java
- **练习文件**：24 个
- **代码行数**：约 8,000 行
- **测试用例**：100+ 个
- **算法实现**：55+ 个

#### C++
- **练习文件**：19 个
- **代码行数**：约 6,000 行
- **测试用例**：80+ 个
- **算法实现**：38+ 个

#### 文档
- **文档文件**：10 个
- **文档行数**：约 5,000 行
- **语言**：英文 + 中文

---

## 💡 常见问题 | FAQ

### Q1：我应该先学 Java 还是 C++？
**A**：取决于您的背景：
- 如果熟悉 Java，先学 Java 练习
- 如果熟悉 C++，先学 C++ 练习
- 建议最终两种语言都学习以获得完整理解

### Q2：我只有 4 核 CPU，能学习吗？
**A**：可以！
- 您仍能学习 ~60% 的内容
- 专注于正确性和基础概念
- 使用云实例进行高核心实验
- 所有基础练习（第 1-6、8 章）效果很好

### Q3：练习的顺序重要吗？
**A**：是的，强烈建议按顺序学习：
- 后面的练习建立在前面的概念上
- 跳过基础可能导致困惑
- 至少按部分（Part 1 然后 Part 2）顺序学习

### Q4：需要多长时间完成？
**A**：取决于您的节奏：
- **快速通道**：10-12 周（单语言，核心练习）
- **标准通道**：20 周（双语言，所有练习）
- **深入通道**：30+ 周（包括扩展和变体）

### Q5：练习难度如何？
**A**：渐进式：
- **第 1-2 周**：简单（基础概念）
- **第 3-11 周**：中等（经典算法）
- **第 12-20 周**：困难（高级技术）

### Q6：需要阅读《多处理器编程的艺术》吗？
**A**：强烈推荐但非必需：
- 练习包含足够的说明
- 书籍提供理论深度
- 练习提供实践经验
- 两者结合效果最佳

### Q7：Hazard Pointers 在 Java 中有用吗？
**A**：有教育价值：
- 理解 GC 为您做了什么
- 理解 C++ 的挑战
- 跨语言并发理解
- 与 C++ 开发者更好的协作

### Q8：我应该实现变体算法吗？
**A**：推荐用于深入学习：
- 完成所有基础练习后
- 尝试实现您自己的变体
- 比较性能差异
- 贡献到开源项目

---

## 🤝 贡献 | Contributing

欢迎贡献！您可以：

### 报告问题
- 发现 bug
- 练习中的错误
- 文档问题
- 硬件特定问题

### 建议新练习
- 缺失的算法
- 额外的变体
- 真实世界的应用

### 改进文档
- 更清晰的说明
- 更多示例
- 翻译

### 添加测试用例
- 边缘情况
- 性能测试
- 压力测试

---

## 📄 许可证 | License

本项目用于教育目的。理论基础请参考《多处理器编程的艺术》。

---

## 🙏 致谢 | Acknowledgments

- 基于 Maurice Herlihy 和 Nir Shavit 的《多处理器编程的艺术》
- 受 Rustlings 项目结构启发
- 感谢所有贡献者和学习者

---

## 📞 支持 | Support

如果遇到问题或有疑问：

1. **检查文档**
   - [EXERCISES_OVERVIEW.md](EXERCISES_OVERVIEW.md) - 练习概览
   - [docs/learning_path.md](docs/learning_path.md) - 学习路径
   - [docs/CPU_REQUIREMENTS.md](docs/CPU_REQUIREMENTS.md) - 硬件需求
   - [docs/getting_started.md](docs/getting_started.md) - 入门指南

2. **对比解决方案**
   - 检查 solutions/ 目录
   - 理解参考实现

3. **硬件问题**
   - 查看 CPU_REQUIREMENTS.md
   - 考虑使用云实例

4. **练习不显示预期行为**
   - 检查核心数要求
   - 验证编译器优化设置
   - 使用 ThreadSanitizer

---

## 🎉 开始学习！

现在您已经了解了项目的完整情况，准备好开始您的多处理器编程学习之旅了吗？

### 下一步

1. **安装环境**
   ```bash
   # Java
   cd exercises/java
   mvn clean install

   # C++
   cd exercises/cpp
   mkdir build && cd build
   cmake .. && make
   ```

2. **开始第一个练习**
   ```bash
   # Java
   cd exercises/java/src/main/java/com/multiprocessor/basics
   # 打开 Exercise01_HelloThreads.java

   # C++
   cd exercises/cpp/01_basics
   # 打开 exercise01_hello_threads.cpp
   ```

3. **参考学习路径**
   - 打开 [docs/learning_path.md](docs/learning_path.md)
   - 按照 20 周计划学习

4. **遇到问题时**
   - 查看 [docs/getting_started.md](docs/getting_started.md)
   - 检查 [EXERCISES_OVERVIEW.md](EXERCISES_OVERVIEW.md)

---

## 📈 学习进度追踪

### 第一部分：基础知识（11 周）
- [ ] 第 1 周：并发基础
- [ ] 第 2 周：并发基础（续）
- [ ] 第 3 周：互斥算法
- [ ] 第 4 周：互斥算法（续）+ 内存顺序
- [ ] 第 5 周：并发对象
- [ ] 第 6 周：并发对象（续）
- [ ] 第 7 周：同步原语
- [ ] 第 8 周：共识
- [ ] 第 9 周：自旋锁 ⚠️ 需要 8+ 核心
- [ ] 第 10 周：监视器与阻塞同步
- [ ] 第 11 周：并发数据结构

### 第二部分：实践篇（9 周）
- [ ] 第 12 周：共识（复习）
- [ ] 第 13 周：监视器（复习）
- [ ] 第 14 周：并行计数 ⚠️ 需要 8+ 核心
- [ ] 第 15 周：并发哈希表
- [ ] 第 16 周：跳表
- [ ] 第 17 周：事务内存
- [ ] 第 18 周：内存回收与工作窃取 🆕 ⚠️ 需要 8+ 核心
- [ ] 第 19 周：优先队列与 RCU 🆕 ⚠️ 需要 8+ 核心
- [ ] 第 20 周：并行算法 🆕 ⚠️ 需要 8+ 核心

---

## 🌟 总结

这是一个全面、深入、实践导向的多处理器编程学习项目：

- ✅ **43 个练习**，从简单到高级
- ✅ **93+ 个算法**，涵盖经典和现代技术
- ✅ **双语言**，Java 和 C++ 完整实现
- ✅ **20 周路径**，结构化渐进学习
- ✅ **完整文档**，中英双语详细指南
- ✅ **硬件分析**，针对不同配置的建议
- ✅ **参考解答**，12 个完整解决方案

无论您是学生、专业开发者，还是并发编程爱好者，这个项目都能帮助您：
- 深入理解并发编程理论
- 掌握经典和现代算法
- 编写生产级并发代码
- 避免常见陷阱和问题

**祝您学习愉快！🚀**

---

**最后更新**：2025-11-21
**版本**：1.0（完整版，阶段 5-6-7 完成）
**语言**：中文（简体）

[返回顶部](#多处理器编程学习项目---完整指南)
