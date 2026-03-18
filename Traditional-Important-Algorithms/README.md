# Traditional Important Algorithms

An interactive, rustlings-style exercise repository for learning classic and important algorithms used in programming languages, operating systems, compilers, and distributed systems.

## 📚 What You'll Learn

This repository contains **132 hands-on exercises** covering fourteen major categories of algorithms that are fundamental to computer systems:

### 🧩 1. Garbage Collection & Memory Management (10 exercises)
- Reference Counting
- Mark-Sweep GC
- Copying GC
- Generational GC
- Tricolor Marking
- Incremental GC
- Concurrent GC
- Write Barriers
- Region-based Allocation
- Escape Analysis

### 🧩 2. Memory Models & Safety Mechanisms (6 exercises)
- Stack vs Heap Allocation
- RAII (Resource Acquisition Is Initialization)
- Ownership & Borrowing (Rust's model)
- Smart Pointers (Box, Rc, RefCell)
- Arena Allocators
- Memory Pools

### 🧩 3. Concurrency & Scheduling (10 exercises)
- Round Robin Scheduling
- Priority Scheduling
- Multi-Level Feedback Queue (MLFQ)
- Preemptive Scheduling
- Cooperative Scheduling
- Work Stealing
- Actor Model
- Event Loop
- Coroutine Scheduling
- M:N Threading

### 🧩 4. Operating System Algorithms (9 exercises)
- Paging
- Segmentation
- LRU Cache
- FIFO Page Replacement
- Clock Algorithm
- Buddy System Allocator
- Banker's Algorithm (Deadlock Avoidance)
- Producer-Consumer Problem
- Reader-Writer Locks

### 🧩 5. Compiler & Runtime Mechanisms (7 exercises)
- Lexical Analysis
- Parsing
- Register Allocation (Graph Coloring)
- Constant Folding
- Common Subexpression Elimination (CSE)
- Escape Analysis
- Inline Caching

### 🧩 6. Network & Distributed Systems (10 exercises)
- TCP Congestion Control (AIMD, Slow Start)
- Load Balancing (Round Robin, Least Connections, Consistent Hashing)
- Consistent Hashing
- Raft Consensus Algorithm
- Paxos Consensus Algorithm
- Lease Mechanism
- Heartbeat & Failure Detection
- Vector Clocks
- Gossip Protocol
- Two-Phase Commit

### 🔐 7. Cryptography & Security (10 exercises)
- Symmetric Encryption (AES-like)
- Asymmetric Encryption (RSA)
- Cryptographic Hash Functions (SHA-like)
- Digital Signatures
- Diffie-Hellman Key Exchange
- Message Authentication Code (HMAC)
- Password Hashing (bcrypt/Argon2 concepts)
- Secure Random Number Generation
- JSON Web Tokens (JWT)
- TLS Handshake Protocol

### 💾 8. Database & Storage (12 exercises)
- B-Tree
- B+ Tree
- LSM Tree (Log-Structured Merge Tree)
- Write-Ahead Logging (WAL)
- Multi-Version Concurrency Control (MVCC)
- Transaction Isolation Levels
- Query Optimizer
- Bloom Filter
- Skip List
- Trie / Prefix Tree
- Inverted Index
- Buffer Pool Manager

### 🚦 9. Rate Limiting & Fault Tolerance (10 exercises)
- Token Bucket Algorithm
- Leaky Bucket Algorithm
- Sliding Window Rate Limiter
- Fixed Window Counter
- Circuit Breaker Pattern
- Exponential Backoff Retry
- Bulkhead Isolation
- Timeout Control
- Graceful Degradation
- Adaptive Rate Limiting

### 📝 10. String & Text Processing (10 exercises)
- KMP (Knuth-Morris-Pratt)
- Rabin-Karp Algorithm
- Boyer-Moore String Search
- Aho-Corasick Multi-pattern Matching
- Suffix Array
- Levenshtein Distance (Edit Distance)
- Simple Regex Engine
- Huffman Coding
- LZ77 Compression
- Text Similarity Metrics

### 🌊 11. Stream Processing (10 exercises)
- Sliding Window Aggregation
- Watermark Handling
- Top-K Elements
- Reservoir Sampling
- Streaming Joins
- Checkpoint Mechanism
- Exactly-Once Processing
- Streaming Aggregation
- Event Time vs Processing Time
- Backpressure Handling

### 🕸️ 12. Graph Algorithms (10 exercises)
- Dijkstra's Shortest Path
- Bellman-Ford Algorithm
- Floyd-Warshall All-Pairs Shortest Paths
- Kruskal's Minimum Spanning Tree
- Prim's Minimum Spanning Tree
- Topological Sorting
- Tarjan's Strongly Connected Components
- Maximum Flow (Ford-Fulkerson)
- PageRank
- Graph Coloring

### 🌳 13. Data Structures (10 exercises)
- Red-Black Tree
- AVL Tree
- Binary Heap
- Fibonacci Heap
- Union-Find (Disjoint Set)
- Segment Tree
- Fenwick Tree (Binary Indexed Tree)
- Splay Tree
- Treap
- Persistent Data Structures

### 🤖 14. Machine Learning Fundamentals (8 exercises)
- Gradient Descent & Variants (SGD, Momentum, Adam)
- Linear Regression
- Logistic Regression
- K-Means Clustering
- K-Nearest Neighbors (k-NN)
- Decision Tree
- Neural Network with Backpropagation
- Matrix Factorization for Recommendations

## 🚀 Getting Started

This repository supports **both Rust and Python**! Choose the language you're more comfortable with.

### 🦀 Rust Version

**Prerequisites:**
- Rust 1.70 or higher
- Basic understanding of Rust syntax
- Familiarity with data structures (hashmaps, vectors, etc.)

**Installation:**

1. Clone this repository:
```bash
git clone https://github.com/GeoffreyWang1117/Traditional-Important-Algorithms.git
cd Traditional-Important-Algorithms
```

2. Build the project:
```bash
cargo build
```

3. Run the exercises manager:
```bash
cargo run --bin algorithms
```

### 🐍 Python Version

**Prerequisites:**
- Python 3.8 or higher
- Basic understanding of Python syntax
- Familiarity with data structures (lists, dicts, etc.)

**Installation:**

1. Clone this repository (if not already done):
```bash
git clone https://github.com/GeoffreyWang1117/Traditional-Important-Algorithms.git
cd Traditional-Important-Algorithms
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the exercises manager:
```bash
python3 algorithms.py
```

## 📖 How to Use

### 🦀 Rust Version

#### List All Exercises

```bash
cargo run --bin algorithms list
```

#### Work on an Exercise

1. Open an exercise file, e.g., `exercises/01_gc_and_memory/gc01_reference_counting.rs`
2. Read the documentation and understand what needs to be implemented
3. Fill in the `todo!()` sections
4. Remove the `I AM NOT DONE` comment when you're ready to test
5. Verify your solution:

```bash
cargo run --bin algorithms verify gc01_reference_counting
```

#### Watch Mode

```bash
cargo run --bin algorithms watch gc01_reference_counting
```

#### Get a Hint

```bash
cargo run --bin algorithms hint gc01_reference_counting
```

#### Run All Exercises

```bash
cargo run --bin algorithms run
```

### 🐍 Python Version

#### List All Exercises

```bash
python3 algorithms.py list
```

#### Work on an Exercise

1. Open an exercise file, e.g., `exercises_py/01_gc_and_memory/gc01_reference_counting.py`
2. Read the docstring and understand what needs to be implemented
3. Fill in the `TODO` sections (replace `pass` statements)
4. Remove the `# I AM NOT DONE` comment when you're ready to test
5. Verify your solution:

```bash
python3 algorithms.py verify gc01_reference_counting
```

#### Watch Mode

```bash
python3 algorithms.py watch gc01_reference_counting
```

#### Get a Hint

```bash
python3 algorithms.py hint gc01_reference_counting
```

#### Run All Exercises

```bash
python3 algorithms.py run
```

## 📝 Exercise Format

### 🦀 Rust Format

```rust
// exercise_name.rs
//
// Brief description of the algorithm and what you'll learn
//
// Your task: Clear instructions on what to implement

// I AM NOT DONE  <- Remove this line when you're ready to verify

// Your code here with TODO markers
pub struct MyAlgorithm {
    // ...
}

impl MyAlgorithm {
    pub fn new() -> Self {
        // TODO: Implement this
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_functionality() {
        // Comprehensive tests to verify your implementation
    }
}
```

### 🐍 Python Format

```python
# I AM NOT DONE  <- Remove this line when you're ready to verify

"""
Exercise Name: Description

Your task: Clear instructions on what to implement
"""

class MyAlgorithm:
    def __init__(self):
        # TODO: Implement this
        pass

    def my_method(self):
        # TODO: Implement this
        pass

import unittest

class TestMyAlgorithm(unittest.TestCase):
    def test_basic_functionality(self):
        # Comprehensive tests to verify your implementation
        algo = MyAlgorithm()
        # Test your implementation here

if __name__ == '__main__':
    unittest.main()
```

## 🎯 Learning Path

We recommend following the exercises in order, but you can also jump to topics that interest you:

**🟢 Beginners** (Start here):
- Category 2: Memory Models & Safety
- Category 13: Data Structures
- Category 10: String & Text Processing

**🟡 Intermediate** (Core systems programming):
- Category 1: Garbage Collection & Memory Management
- Category 3: Concurrency & Scheduling
- Category 4: Operating System Algorithms
- Category 8: Database & Storage
- Category 9: Rate Limiting & Fault Tolerance

**🔴 Advanced** (Complex systems):
- Category 5: Compiler & Runtime Mechanisms
- Category 6: Network & Distributed Systems
- Category 11: Stream Processing
- Category 12: Graph Algorithms

**🔐 Security Track**: Category 7 (Cryptography) can be studied after Category 2.

**🤖 ML Track**: Category 14 (Machine Learning) requires understanding of Category 13 (Data Structures) and basic linear algebra.

**💡 Recommended Learning Sequences**:
1. **Full Stack Developer**: 2 → 13 → 8 → 9 → 10 → 7
2. **Systems Programmer**: 2 → 1 → 3 → 4 → 5 → 6
3. **Backend Engineer**: 2 → 8 → 9 → 6 → 11 → 7
4. **Data Engineer**: 13 → 8 → 11 → 12 → 14
5. **Complete Mastery**: Follow categories 1-14 in order

## 🧪 Testing

Each exercise comes with comprehensive tests. Your implementation must pass all tests to be considered complete.

Run tests for a specific exercise:
```bash
rustc --test exercises/01_gc_and_memory/gc01_reference_counting.rs -o /tmp/test && /tmp/test
```

Or use the built-in verifier:
```bash
cargo run --bin algorithms verify gc01_reference_counting
```

## 📚 Additional Resources

### Garbage Collection
- "The Garbage Collection Handbook" by Jones, Hosking, and Moss
- [Memory Management Reference](https://www.memorymanagement.org/)

### Concurrency
- "The Art of Multiprocessor Programming" by Herlihy and Shavit
- [Rust Concurrency Patterns](https://rust-lang.github.io/async-book/)

### Operating Systems
- "Operating Systems: Three Easy Pieces" by Remzi and Andrea Arpaci-Dusseau
- [OSDev Wiki](https://wiki.osdev.org/)

### Compilers
- "Crafting Interpreters" by Robert Nystrom
- "Engineering a Compiler" by Cooper and Torczon

### Distributed Systems
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Distributed Systems" by Maarten van Steen and Andrew S. Tanenbaum
- [Raft Consensus Paper](https://raft.github.io/)
- [The Part-Time Parliament (Paxos)](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)

### Cryptography & Security
- "Applied Cryptography" by Bruce Schneier
- "Cryptography Engineering" by Ferguson, Schneier, and Kohno
- [Crypto101](https://www.crypto101.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Database Systems
- "Database Internals" by Alex Petrov
- "Designing Data-Intensive Applications" by Martin Kleppmann (Chapters 3-4)
- [CMU Database Systems Course](https://15445.courses.cs.cmu.edu/)
- [The Log-Structured Merge-Tree (LSM-Tree)](http://www.cs.umb.edu/~poneil/lsmtree.pdf)

### String Algorithms & Text Processing
- "Algorithms on Strings, Trees, and Sequences" by Dan Gusfield
- "Flexible Pattern Matching in Strings" by Navarro and Raffinot
- [KMP Algorithm Visualization](https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/)

### Stream Processing
- "Streaming Systems" by Akidau, Chernyak, and Lax
- "Kafka: The Definitive Guide" by Narkhede, Shapira, and Palino
- [Apache Flink Documentation](https://flink.apache.org/)
- [The Dataflow Model Paper](https://research.google/pubs/pub43864/)

### Graph Algorithms
- "Introduction to Algorithms" (CLRS) - Graph Algorithms chapters
- "Network Science" by Albert-László Barabási
- [Dijkstra's Algorithm Visualization](https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html)

### Data Structures
- "Introduction to Algorithms" (CLRS)
- "Advanced Data Structures" by Peter Brass
- [VisuAlgo](https://visualgo.net/) - Data structure visualizations

### Machine Learning
- "Hands-On Machine Learning" by Aurélien Géron
- "Pattern Recognition and Machine Learning" by Christopher Bishop
- [Coursera ML Course](https://www.coursera.org/learn/machine-learning) by Andrew Ng
- [Dive into Deep Learning](https://d2l.ai/)

## 🤝 Contributing

Contributions are welcome! If you find bugs, have suggestions, or want to add new exercises:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure:
- New exercises follow the existing format
- Tests are comprehensive
- Documentation is clear

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

Inspired by:
- [Rustlings](https://github.com/rust-lang/rustlings) - The original Rust exercises
- Classic algorithms textbooks and papers
- Real-world implementations in production systems

## 📊 Progress Tracking

You can track your progress at any time:

```bash
cargo run --bin algorithms run
```

This shows:
- ✓ Completed exercises
- ✗ Failed exercises
- ○ Pending exercises

## 💡 Tips

1. **Read the hints**: Use `cargo run --bin algorithms hint <exercise>` when stuck
2. **Understand before implementing**: Read the algorithm description carefully
3. **Test incrementally**: Implement one function at a time and test
4. **Study the tests**: They show exactly what behavior is expected
5. **Research**: These are classic algorithms - there are many resources online
6. **Don't skip exercises**: Later exercises often build on earlier concepts

## 🎓 Learning Outcomes

After completing this repository, you will:

- ✅ Understand how garbage collectors work in modern languages
- ✅ Know the tradeoffs between different memory management strategies
- ✅ Be able to implement concurrent algorithms and schedulers
- ✅ Understand how operating systems manage resources
- ✅ Know how compilers optimize code
- ✅ Have practical experience implementing classic CS algorithms in Rust

## 📧 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the hints: `cargo run --bin algorithms hint <exercise>`
- Review the test cases for expected behavior

---

**Happy Learning! 🎉**

Start your journey with:
```bash
cargo run --bin algorithms list
cargo run --bin algorithms verify gc01_reference_counting
```
