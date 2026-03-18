# Getting Started

Welcome to the Multi-Processor Programming Study project! This guide will help you get up and running.

## Prerequisites

### For Java Exercises

**Required:**
- Java 17 or later (OpenJDK recommended)
  - Check: `java -version`
- Maven 3.6+ or Gradle 7.0+
  - Check: `mvn -version` or `gradle -version`

**Installation:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openjdk-17-jdk maven
```

**macOS:**
```bash
brew install openjdk@17 maven
```

**Windows:**
- Download OpenJDK from https://adoptium.net/
- Download Maven from https://maven.apache.org/download.cgi

### For C++ Exercises

**Required:**
- C++20 compliant compiler:
  - GCC 10+ (Linux)
  - Clang 12+ (macOS/Linux)
  - MSVC 2019+ (Windows)
- CMake 3.20+
  - Check: `cmake --version`

**Installation:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install build-essential cmake
```

**macOS:**
```bash
brew install cmake
# Xcode Command Line Tools (includes clang)
xcode-select --install
```

**Windows:**
- Install Visual Studio 2019 or later with C++ support
- Download CMake from https://cmake.org/download/

## Quick Start

### Java

1. **Navigate to the Java exercises:**
```bash
cd exercises/java
```

2. **Build the project:**
```bash
mvn clean install
```

3. **Run the exercise runner:**
```bash
mvn exec:java -Dexec.args="list"
```

4. **Work on an exercise:**
   - Open an exercise file (e.g., `src/main/java/com/multiprocessor/basics/Exercise01_HelloThreads.java`)
   - Read the instructions and TODOs
   - Implement the missing code
   - Run the tests:
```bash
mvn test -Dtest=Exercise01_HelloThreadsTest
```

5. **Run a specific exercise:**
```bash
# Compile and run
mvn compile exec:java -Dexec.mainClass="com.multiprocessor.basics.Exercise01_HelloThreads"
```

### C++

1. **Navigate to the C++ exercises:**
```bash
cd exercises/cpp
```

2. **Build the project:**
```bash
mkdir build
cd build
cmake ..
make
```

Or on Windows with Visual Studio:
```bash
mkdir build
cd build
cmake .. -G "Visual Studio 16 2019"
cmake --build . --config Release
```

3. **Work on an exercise:**
   - Open an exercise file (e.g., `01_basics/exercise01_hello_threads.cpp`)
   - Read the instructions and TODOs
   - Implement the missing code
   - Rebuild:
```bash
make  # or cmake --build .
```

4. **Run a specific exercise:**
```bash
./01_basics/exercise01_hello_threads
```

5. **Run tests:**
```bash
ctest
# Or run specific test
./01_basics/basics_tests
```

## IDE Setup

### IntelliJ IDEA (Java)

1. Open IntelliJ IDEA
2. File → Open → Select `exercises/java` folder
3. IDEA will automatically detect the Maven project
4. Right-click on an exercise file → Run

### Visual Studio Code (Java & C++)

**For Java:**
1. Install "Extension Pack for Java"
2. Open `exercises/java` folder
3. VSCode will detect Maven automatically

**For C++:**
1. Install "C/C++" and "CMake Tools" extensions
2. Open `exercises/cpp` folder
3. Select a kit when prompted (your compiler)
4. Build using CMake extension

### CLion (C++)

1. Open CLion
2. File → Open → Select `exercises/cpp` folder
3. CLion will automatically configure CMake
4. Right-click on an exercise file → Run

## Working on Exercises

### Typical Workflow

1. **Read the exercise description**
   - Every exercise starts with a concept explanation
   - Understand what you're trying to learn

2. **Locate TODO markers**
   - Search for `TODO` comments
   - These mark places where you need to add code

3. **Implement the solution**
   - Follow the hints provided
   - Don't be afraid to experiment

4. **Run tests**
   - Tests verify your implementation
   - Read failure messages carefully

5. **Fix issues**
   - If tests fail, re-read the concept explanation
   - Check the hints
   - Try running the main() function to see output

6. **Move to next exercise**
   - Complete exercises in order
   - Each builds on previous concepts

### Example: Exercise 01 (Java)

```bash
cd exercises/java
mvn clean install

# Edit the file
vim src/main/java/com/multiprocessor/basics/Exercise01_HelloThreads.java

# Run tests
mvn test -Dtest=Exercise01_HelloThreadsTest

# If tests pass, move to next exercise
```

### Example: Exercise 01 (C++)

```bash
cd exercises/cpp
mkdir build && cd build
cmake ..

# Edit the file
vim ../01_basics/exercise01_hello_threads.cpp

# Rebuild and run
make
./01_basics/exercise01_hello_threads

# Run tests
./01_basics/basics_tests
```

## Understanding Test Output

### Passing Test (Java)
```
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

### Failing Test (Java)
```
Tests run: 4, Failures: 1, Errors: 0, Skipped: 0

testCreateThread(Exercise01_HelloThreadsTest)
  Expected: not null
  but was: null
```
This tells you:
- Which test failed
- What was expected
- What was actually returned

### Passing Test (C++)
```
[==========] Running 4 tests from 1 test suite.
[----------] 4 tests from Exercise01Test
[ RUN      ] Exercise01Test.CreateThread
[       OK ] Exercise01Test.CreateThread (0 ms)
[==========] 4 tests from 1 test suite ran. (5 ms total)
[  PASSED  ] 4 tests.
```

### Failing Test (C++)
```
[ RUN      ] Exercise01Test.CreateThread
/path/to/test.cpp:15: Failure
Expected: (thread != nullptr)
  Actual: false
[  FAILED  ] Exercise01Test.CreateThread (1 ms)
```

## Common Issues

### Java

**Issue: "Cannot find symbol"**
- **Cause**: Missing import or typo
- **Fix**: Add proper import statements

**Issue: "java.lang.NullPointerException"**
- **Cause**: Forgot to initialize something
- **Fix**: Check TODO comments for initialization

**Issue: Tests timeout**
- **Cause**: Deadlock or infinite loop
- **Fix**: Review synchronization logic

### C++

**Issue: "error: 'thread' is not a member of 'std'"**
- **Cause**: Missing include or old C++ standard
- **Fix**: Add `#include <thread>` and ensure C++20

**Issue: "undefined reference to 'pthread_create'"**
- **Cause**: Not linking pthread library
- **Fix**: Already handled in CMakeLists.txt

**Issue: Segmentation fault**
- **Cause**: Accessing uninitialized memory or data race
- **Fix**: Use debugger (gdb/lldb) to find the issue

## Tips for Success

1. **Read the book**: "The Art of Multiprocessor Programming" provides deep understanding
2. **Start simple**: Don't try to optimize before getting correctness
3. **Use print statements**: Add debug output to understand execution
4. **Be patient**: Concurrent programming is tricky, take your time
5. **Experiment**: Try changing things to see what breaks
6. **Ask questions**: If stuck, re-read the concept explanation

## Next Steps

1. Complete Module 01 (Basics)
2. Review the [Learning Path](learning_path.md)
3. Check [Concepts](concepts.md) for detailed explanations
4. Look at [Hints](hints.md) if you get stuck

## Getting Help

If you encounter issues:

1. **Re-read the exercise description**: Often the answer is there
2. **Check the hints**: Look for HINT comments in the code
3. **Run the main() function**: See the actual output
4. **Compare with test expectations**: What's different?
5. **Review the concepts**: Check docs/concepts.md

Remember: The goal is to learn, not just to pass tests. Understanding why something works is more important than just making it work.

Happy learning! 🎓
