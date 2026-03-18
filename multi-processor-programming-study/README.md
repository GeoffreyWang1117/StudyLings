# Multi-Processor Programming Study

[English](#) | [中文完整指南](PROJECT_GUIDE_zh-CN.md) | [Documentation Index](DOCUMENTATION_INDEX.md)

🚀 A Rustlings-style interactive learning project for mastering concurrent and parallel programming based on "The Art of Multiprocessor Programming".

## 📚 Overview

This project provides hands-on exercises in both **Java** and **C++** (modern standards: Java 17+, C++20+) to help you learn multiprocessor programming concepts progressively. Each exercise is designed to teach specific concepts from "The Art of Multiprocessor Programming" through practical implementation.

### 🎉 Project Status: Complete!

**43 exercise files** | **93+ algorithms** | **20-week learning path**

✅ **Part 1**: Foundations (Chapters 1-11) - Complete
✅ **Part 2**: Practice (Chapters 12-19) - Complete
✅ **Phase 5**: Memory Reclamation & Work Stealing - Complete
✅ **Phase 6**: Priority Queues, RCU, Memory Model - Complete
✅ **Phase 7**: Parallel Algorithms - Complete

**What's Inside**:
- 24 Java exercise files (55+ algorithms)
- 19 C++ exercise files (38+ algorithms)
- 12 complete solution files
- Comprehensive testing frameworks
- Detailed documentation and learning guides

## 🎯 Learning Path

The exercises are organized into modules that follow the book's structure:

### Part 1: Foundations
1. **Basics** - Introduction to concurrent programming concepts
2. **Mutual Exclusion** - Peterson's algorithm, filters, memory ordering
3. **Concurrent Objects** - Linearizability, sequential consistency
4. **Foundations** - Register constructions, atomic snapshots
5. **Synchronization Primitives** - Compare-and-swap, load-linked/store-conditional
6. **Consensus** - Consensus protocols, universality
7. **Spin Locks** - TAS, TTAS, backoff, queue locks (MCS, Anderson)
8. **Monitors & Blocking** - Condition variables, semaphores
9. **Linked Lists** - Coarse-grained, fine-grained, optimistic, lazy synchronization
10. **Concurrent Queues** - Bounded/unbounded queues, ABA problem
11. **Concurrent Stacks** - Lock-free stacks, elimination

### Part 2: Practice (Advanced Topics)
12. **Parallel Counting** - Scalable counters, false sharing prevention
13. **Concurrent Hashing** - Striped, cuckoo, lock-free hash maps
14. **Skip Lists** - Lock-free probabilistic search structures
15. **Transactional Memory** - Software STM with optimistic concurrency
16. **Memory Reclamation** - Hazard pointers for lock-free structures
17. **Work Stealing** - Chase-Lev deque, task parallelism
18. **Priority Queues** - Lock-based, skiplist-based, relaxed queues
19. **Read-Copy-Update (RCU)** - Read-heavy optimization pattern
20. **Parallel Algorithms** - Parallel sorting (merge sort, quick sort)

## 🏗️ Project Structure

```
multi-processor-programming-study/
├── README.md
├── exercises/
│   ├── java/               # Java exercises
│   │   ├── 01_basics/
│   │   ├── 02_mutual_exclusion/
│   │   ├── 03_concurrent_objects/
│   │   └── ...
│   └── cpp/                # C++ exercises
│       ├── 01_basics/
│       ├── 02_mutual_exclusion/
│       ├── 03_concurrent_objects/
│       └── ...
├── solutions/              # Reference solutions (for self-checking)
│   ├── java/
│   └── cpp/
├── runner/                 # Exercise validation tools
│   ├── java/
│   └── cpp/
└── docs/                   # Additional learning materials
    ├── getting_started.md         # Installation and setup guide
    ├── learning_path.md           # 17-week structured learning path
    ├── concepts.md                # Deep dive into core concepts
    ├── CPU_REQUIREMENTS.md        # Hardware requirements analysis
    └── SECOND_EDITION_TOPICS.md   # Second edition coverage analysis
```

## 🚀 Getting Started

### Prerequisites

**For Java exercises:**
- Java 17 or later (OpenJDK recommended)
- Maven 3.6+ or Gradle 7.0+

**For C++ exercises:**
- C++20 compliant compiler (GCC 10+, Clang 12+, or MSVC 2019+)
- CMake 3.20+

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd multi-processor-programming-study

# For Java
cd exercises/java
mvn clean install

# For C++
cd exercises/cpp
mkdir build && cd build
cmake ..
make
```

### Running Exercises

**Java:**
```bash
cd exercises/java
mvn exec:java -Dexec.mainClass="ExerciseRunner"
# Or run specific exercise
mvn test -Dtest=Exercise01Test
```

**C++:**
```bash
cd exercises/cpp/build
./exercise_runner
# Or run specific exercise
./01_basics/exercise01
```

## 📖 How to Use

1. **Start with the basics**: Begin with module 01 in your preferred language
2. **Read the exercise description**: Each file contains instructions and TODO markers
3. **Implement the solution**: Fill in the missing code marked with TODO or FIXME
4. **Run tests**: Use the exercise runner to validate your solution
5. **Compare with solutions**: After solving, check the solutions/ directory for reference implementations
6. **Move to next exercise**: Progress through modules sequentially for best learning

## 🎓 Exercise Format

Each exercise file contains:
- **Concept explanation**: Brief description of what you'll learn
- **TODO markers**: Places where you need to write code
- **Tests**: Automated tests to verify correctness
- **Hints**: Comments to guide you (if you're stuck)

Example:
```java
// Exercise: Implement a simple counter with race condition demonstration
// TODO: Implement increment() method
// HINT: Think about what happens when multiple threads access this

public class Counter {
    private int count = 0;

    public void increment() {
        // TODO: Implement this method
    }

    public int getCount() {
        return count;
    }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs or issues
- Suggest new exercises
- Improve documentation
- Add test cases

## 📄 License

This project is for educational purposes. Please refer to "The Art of Multiprocessor Programming" for theoretical foundations.

## 🙏 Acknowledgments

- Based on "The Art of Multiprocessor Programming" by Maurice Herlihy and Nir Shavit
- Inspired by Rustlings project structure

## 💻 Hardware Requirements

Different exercises have varying hardware requirements to fully observe concurrent programming phenomena:

- **Minimum (2-4 cores)**: Basic learning, correctness understanding
- **Recommended (8 cores)**: Most exercises show interesting behavior
- **Optimal (16+ cores)**: Full educational value, dramatic performance differences

**Most hardware-sensitive exercises:**
- Chapter 7: Spin Locks (16+ cores ideal)
- Chapter 11: Elimination Backoff (16+ cores highly recommended)
- Chapter 12: Parallel Counting (16+ cores for dramatic effects)

For detailed analysis of hardware requirements per exercise, see [docs/CPU_REQUIREMENTS.md](docs/CPU_REQUIREMENTS.md).

For students with limited hardware:
- Focus on correctness and fundamental concepts
- Use cloud instances (AWS, Azure, GCP) for high-core-count experiments
- GitHub Actions provides free 2-core runners for basic testing

## 📚 Additional Resources

### English Documentation
- **[Exercise Overview](EXERCISES_OVERVIEW.md)**: Complete catalog of all 43 exercises
- **[Algorithm Mapping](ALGORITHM_EXERCISE_MAPPING.md)**: Algorithm-to-exercise mapping (93+ algorithms)
- **[Project Summary](PROJECT_SUMMARY.md)**: Comprehensive project documentation
- **[Learning Path](docs/learning_path.md)**: 20-week structured progression
- **[CPU Requirements](docs/CPU_REQUIREMENTS.md)**: Detailed hardware requirements analysis
- **[Second Edition Topics](docs/SECOND_EDITION_TOPICS.md)**: Coverage of second edition content
- **[Concepts Guide](docs/concepts.md)**: Deep dive into core concepts

### 中文文档 (Chinese Documentation)
- **[完整中文指南](PROJECT_GUIDE_zh-CN.md)**: 包含所有内容的完整中文学习指南
- **[文档索引](DOCUMENTATION_INDEX.md)**: 中英文文档索引和导航

## 📞 Support

If you encounter issues or have questions:
1. Check the docs/ directory for additional help
2. Review the EXERCISES_OVERVIEW.md for complete exercise catalog
3. Compare your implementation with solutions/
4. Check CPU_REQUIREMENTS.md if exercises don't show expected behavior

Happy concurrent programming! 🎉
