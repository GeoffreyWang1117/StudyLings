# CUDAlings 架构设计

## 项目概览

CUDAlings 是一个交互式 CUDA C++ 学习系统，模仿 Rustlings 的设计理念，通过渐进式练习帮助学习者掌握 GPU 编程。

## 目录结构

```
Cuda-CPP-Study/
├── src/                      # 核心运行时系统 (C++)
│   ├── main.cpp             # 程序入口
│   ├── exercise_manager.*   # 练习管理器
│   ├── runner.*             # 练习执行器
│   └── progress.*           # 进度追踪
├── exercises/               # 练习文件
│   ├── 01_intro/           # 基础入门
│   ├── 02_kernels/         # Kernel 函数
│   ├── 03_threads/         # 线程管理
│   ├── 04_memory/          # 内存管理
│   ├── 05_shared_memory/   # 共享内存
│   ├── 06_sync/            # 同步机制
│   ├── 07_optimization/    # 性能优化
│   ├── 08_streams/         # CUDA 流
│   └── 09_advanced/        # 高级特性
├── solutions/              # 参考答案
│   └── (镜像 exercises 结构)
├── docs/                   # 文档
│   ├── GETTING_STARTED.md
│   ├── EXERCISE_GUIDE.md
│   ├── CONTRIBUTING.md
│   └── ARCHITECTURE.md
├── scripts/                # 工具脚本
│   ├── install.sh
│   └── check_gpu.sh
├── CMakeLists.txt         # 构建配置
└── README.md              # 项目说明
```

## 核心组件

### 1. Exercise Manager (练习管理器)

**职责**:
- 加载和管理所有练习
- 提供练习查询接口
- 跟踪练习完成状态

**关键类**:
```cpp
class ExerciseManager {
    std::vector<Exercise> exercises_;  // 所有练习
    Exercise* get_exercise(int num);   // 获取特定练习
    Exercise* get_next_incomplete();   // 获取下一个未完成练习
};

struct Exercise {
    int number;                        // 练习编号
    std::string topic;                 // 主题
    std::string file_path;             // 文件路径
    std::vector<std::string> hints;    // 提示
};
```

### 2. Runner (执行器)

**职责**:
- 编译 CUDA 练习
- 运行测试
- 提供反馈

**工作流程**:
```
1. 用户修改练习文件
2. Runner 调用 nvcc 编译
3. 执行生成的程序
4. 检查输出和退出码
5. 提供反馈（成功/失败/提示）
```

**关键方法**:
```cpp
class Runner {
    bool compile_exercise(const Exercise&);  // 编译
    bool run_tests(const Exercise&);         // 运行测试
    void verify(int exercise_num);           // 验证
    void watch_mode();                       // 监视模式
};
```

### 3. Progress Tracker (进度追踪)

**职责**:
- 保存完成的练习
- 加载进度状态
- 显示学习统计

**数据存储**:
- 位置: `~/.cudalings/progress.txt`
- 格式: 每行一个练习编号

```cpp
class ProgressTracker {
    std::set<int> completed_exercises_;
    bool load();                      // 从文件加载
    bool save();                      // 保存到文件
    void mark_completed(int num);     // 标记完成
};
```

## 练习设计

### 练习文件格式

每个练习文件包含:

1. **头部说明**: 练习目标和任务
2. **TODO 标记**: 需要学习者完成的部分
3. **测试代码**: 自动验证功能
4. **完成标记**: `I AM NOT DONE` 注释

### 练习验证机制

验证流程:
```
1. 检查文件是否存在
2. 使用 nvcc 编译
3. 执行程序
4. 检查:
   - 退出码 == 0
   - 输出包含 "TEST_PASSED"
   - 没有 "TEST_FAILED" 或 "ERROR"
5. 返回结果
```

### 提示系统

三级提示设计:
- **Level 1**: 指向问题方向
- **Level 2**: 给出具体思路
- **Level 3**: 提供代码片段

## 编译系统

### CMake 配置

```cmake
# 检测 CUDA
find_package(CUDA)

# 编译主程序 (C++)
add_executable(cudalings ${SOURCES})

# 不编译练习文件（由运行时编译）
```

### 运行时编译

练习由 Runner 在运行时编译:
```bash
nvcc -o /tmp/test_N exercise.cu -arch=sm_60 -std=c++14
```

优势:
- 即时反馈
- 无需重新构建整个项目
- 支持不同 GPU 架构

## 用户交互流程

### 典型学习会话

```
1. ./cudalings list
   └─> 显示所有练习和进度

2. ./cudalings run
   └─> 显示下一个未完成练习的描述

3. 用户编辑练习文件
   └─> 实现 TODO 部分

4. ./cudalings verify
   └─> 编译和测试
   └─> 提供反馈

5. (如果失败) ./cudalings hint
   └─> 显示提示

6. (重复 3-5 直到成功)

7. 自动进入下一个练习
```

### 监视模式

```
./cudalings watch
  └─> 监控文件变化
      └─> 自动编译和测试
          └─> 即时反馈
```

实现:
```cpp
while (true) {
    check_file_modifications();
    if (changed) {
        verify(exercise);
    }
    sleep(2s);
}
```

## 扩展点

### 添加新练习

1. 创建练习文件: `exercises/XX_topic/NN_name.cu`
2. 创建答案: `solutions/XX_topic/NN_name.cu`
3. 注册到 ExerciseManager:
   ```cpp
   exercises_.push_back({
       N, "topic", "name",
       "path", "description",
       {"hint1", "hint2"},
       "solution_path"
   });
   ```

### 添加新功能

可能的扩展:
- 性能基准测试
- 代码质量检查
- 可视化工具
- Web 界面
- 协作功能

## 技术栈

- **语言**: C++14 (主程序), CUDA C++ (练习)
- **构建**: CMake 3.18+
- **依赖**:
  - CUDA Toolkit 11.0+
  - C++ 标准库
  - 文件系统库 (C++17 或 Boost)

## 设计原则

### 1. 简单性
- 最小化依赖
- 清晰的代码结构
- 易于理解和修改

### 2. 渐进性
- 练习由浅入深
- 每个练习聚焦一个概念
- 循序渐进的难度曲线

### 3. 即时反馈
- 快速编译
- 清晰的错误信息
- 监视模式

### 4. 自包含
- 每个练习独立完整
- 包含所有必要的代码
- 不依赖外部资源

### 5. 可扩展性
- 易于添加新练习
- 模块化设计
- 清晰的接口

## 性能考虑

### 编译优化
- 只编译修改的文件
- 缓存编译结果（未来优化）
- 并行编译多个练习（未来优化）

### 文件监视
- 使用文件修改时间而非内容哈希
- 可配置的轮询间隔
- 避免不必要的重编译

## 安全性

### 代码执行
- 编译错误被捕获和显示
- 运行时错误不会崩溃主程序
- 超时保护（未来添加）

### 文件操作
- 检查文件存在性
- 使用临时目录存放可执行文件
- 正确的错误处理

## 未来改进

### 短期
- [ ] 添加更多练习
- [ ] 改进错误消息
- [ ] 添加性能测试
- [ ] 支持更多 GPU 架构

### 中期
- [ ] Web 界面
- [ ] 进度同步（云端）
- [ ] 社区练习库
- [ ] 性能分析集成

### 长期
- [ ] AI 辅助提示
- [ ] 自动难度调整
- [ ] 多语言支持
- [ ] 认证系统

## 总结

CUDAlings 通过精心设计的架构，提供了一个高效、友好的 CUDA 学习平台。模块化的设计使得系统易于维护和扩展，而渐进式的练习体系确保了良好的学习体验。
