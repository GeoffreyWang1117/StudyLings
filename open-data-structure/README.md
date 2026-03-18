# Open Data Structures - Python Learning System 🐍

Welcome to **ODS-Python**, an interactive learning system inspired by Rustlings, designed to teach you data structures from the book *"Open Data Structures"* through hands-on Python exercises.

## 🎯 Features

- **Progressive Learning Path**: Exercises organized from basic to advanced
- **Interactive Feedback**: Automatic testing with helpful hints
- **Comprehensive Coverage**: All major data structures from ODS
- **Real-world Applications**: Practical scenarios for each data structure
- **Watch Mode**: Auto-run tests as you save your solutions

## 📚 Covered Data Structures

1. **Arrays & Lists**
   - Array-Based Lists
   - Linked Lists (Singly, Doubly, Circular)
   - Skip Lists

2. **Stacks & Queues**
   - Array-Based Stack
   - Linked Stack
   - Queue & Deque implementations

3. **Hash Tables**
   - Chaining
   - Open Addressing
   - Applications

4. **Trees**
   - Binary Search Trees
   - AVL Trees
   - Red-Black Trees
   - B-Trees
   - Treaps

5. **Heaps**
   - Binary Heaps
   - Priority Queues

6. **Graphs**
   - Adjacency List
   - Adjacency Matrix
   - Graph Algorithms (BFS, DFS, Dijkstra, etc.)

7. **Sorting Algorithms**
   - Merge Sort
   - Quick Sort
   - Heap Sort
   - Counting Sort

8. **Advanced Data Structures**
   - Trie (Prefix Tree)
   - Union-Find (Disjoint Set)
   - Segment Tree
   - Fenwick Tree (Binary Indexed Tree)
   - Bloom Filter
   - KMP String Matching
   - Interval Tree
   - Splay Tree

9. **Specialized Structures**
   - Suffix Array (string indexing)
   - K-D Tree (spatial search)
   - Rope (text editor)
   - Merkle Tree (blockchain/verification)
   - Aho-Corasick (multi-pattern matching)
   - Count-Min Sketch (stream analytics)
   - Radix Tree (IP routing)
   - Cartesian Tree (range queries)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd open-data-structure

# Install dependencies
pip install -r requirements.txt
```

### Running the Exercises

```bash
# Run in interactive mode
python main.py

# Run in watch mode (auto-run on file changes)
python main.py watch

# Run a specific exercise
python main.py run <exercise-name>

# Verify all completed exercises
python main.py verify

# Get a hint for current exercise
python main.py hint

# List all exercises
python main.py list
```

## 📖 How It Works

1. Each exercise is a Python file with incomplete code
2. Your task is to implement the missing parts (marked with `# TODO`)
3. Run the exercise to see if your solution passes the tests
4. Use hints if you get stuck
5. Move on to the next exercise once tests pass

## 🎓 Learning Path

Exercises are organized in order of increasing difficulty:

```
intro → arrays → lists → stacks → queues → hash_tables →
trees → heaps → graphs → sorting → advanced
```

## 💡 Example

```python
# exercises/01_arrays/01_array_stack.py

class ArrayStack:
    """
    Implement a stack using a Python list (array-based).
    """
    def __init__(self):
        # TODO: Initialize your stack
        pass

    def push(self, item):
        # TODO: Add item to top of stack
        pass

    def pop(self):
        # TODO: Remove and return top item
        pass
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new exercises
- Improve existing ones
- Fix bugs
- Enhance documentation

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Inspired by [Rustlings](https://github.com/rust-lang/rustlings)
- Based on *"Open Data Structures"* by Pat Morin
- Built for learners who want hands-on practice with data structures

## 📧 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing exercises for examples
- Use the built-in hint system

Happy learning! 🎉
