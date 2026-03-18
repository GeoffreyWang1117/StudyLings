# 贡献指南

感谢你对 CUDAlings 的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果你发现 bug，请创建一个 issue 并包含:

- 清晰的标题和描述
- 复现步骤
- 预期行为 vs 实际行为
- 系统信息 (OS, CUDA 版本, GPU 型号)
- 相关的错误信息或日志

### 建议新功能

我们欢迎新功能建议！请创建 issue 说明:

- 功能的用途和价值
- 可能的实现方式
- 相关的使用场景

### 贡献练习

这是最有价值的贡献之一！

#### 练习要求

一个好的练习应该:

1. **有明确的学习目标**: 专注于一个特定的 CUDA 概念
2. **循序渐进**: 适合当前难度级别
3. **自包含**: 包含所有必要的代码和说明
4. **有测试**: 能自动验证正确性
5. **有提示**: 提供多级提示帮助学习者

#### 练习模板

```cuda
// 练习 N: 标题
//
// 目标: 简短描述学习目标
//
// 任务:
// 1. 具体任务 1
// 2. 具体任务 2
// 3. ...

#include <stdio.h>
#include <cuda_runtime.h>

// TODO: 实现这个函数
__global__ void my_kernel() {
    // 你的代码在这里
}

int main() {
    // 设置代码...

    // TODO: 调用 kernel

    // 验证代码...
    bool success = true;
    // ... 检查结果 ...

    if (success) {
        printf("TEST_PASSED\n");
        return 0;
    } else {
        printf("TEST_FAILED\n");
        return 1;
    }
}

// I AM NOT DONE
```

#### 添加练习的步骤

1. 在适当的目录创建练习文件
   ```
   exercises/XX_topic/NN_exercise_name.cu
   ```

2. 创建对应的参考答案
   ```
   solutions/XX_topic/NN_exercise_name.cu
   ```

3. 在 `src/exercise_manager.cpp` 中注册练习
   ```cpp
   exercises_.push_back({
       N, "XX_topic", "exercise_name",
       "exercises/XX_topic/NN_exercise_name.cu",
       "练习描述",
       {
           "提示 1: ...",
           "提示 2: ...",
           "提示 3: ..."
       },
       "solutions/XX_topic/NN_exercise_name.cu"
   });
   ```

4. 测试你的练习
   ```bash
   ./cudalings verify N
   ```

### 改进文档

文档改进总是受欢迎的:

- 修正拼写/语法错误
- 改进说明的清晰度
- 添加示例
- 翻译成其他语言

### 代码贡献

#### 设置开发环境

```bash
git clone <repo-url>
cd Cuda-CPP-Study
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make
```

#### 代码风格

- C++ 代码遵循 Google C++ Style Guide
- CUDA 代码遵循 NVIDIA 推荐的最佳实践
- 使用有意义的变量名
- 添加适当的注释

#### 提交 Pull Request

1. Fork 项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

#### PR 要求

- 清晰的标题和描述
- 关联相关的 issue
- 通过所有测试
- 更新相关文档

## 练习主题建议

我们特别欢迎以下主题的练习:

### 已有但需要扩展
- [ ] 更多基础练习
- [ ] 矩阵运算
- [ ] 图像处理
- [ ] 并行算法 (sort, scan, reduce)

### 期待添加
- [ ] Tensor Core 使用
- [ ] Multi-GPU 编程
- [ ] CUDA Graphs
- [ ] 与 cuBLAS/cuFFT 等库集成
- [ ] 深度学习相关的 kernel
- [ ] 分子动力学模拟
- [ ] 光线追踪基础

## 行为准则

- 尊重所有参与者
- 欢迎各种技能水平的贡献者
- 建设性地提供和接受反馈
- 专注于对项目最有利的方面

## 问题？

如果有任何疑问，请:

- 查看现有的 issues 和 PRs
- 创建新的 issue 提问
- 参与讨论

感谢你帮助改进 CUDAlings！ 🙏
