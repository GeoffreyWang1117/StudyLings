# 快速开始指南

## 安装 CUDA Toolkit

### Ubuntu/Debian

```bash
# 添加 NVIDIA 包仓库
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"

# 安装 CUDA
sudo apt update
sudo apt install cuda
```

### 设置环境变量

将以下内容添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

然后重新加载配置:

```bash
source ~/.bashrc
```

### 验证安装

```bash
nvcc --version
nvidia-smi
```

## 构建 CUDAlings

```bash
# 克隆仓库
git clone <your-repo-url>
cd Cuda-CPP-Study

# 创建构建目录
mkdir build && cd build

# 配置和构建
cmake ..
make

# 运行
./cudalings
```

## 你的第一个练习

```bash
# 查看所有练习
./cudalings list

# 运行第一个练习
./cudalings run

# 编辑练习文件
# 打开 exercises/01_intro/01_hello_cuda.cu

# 验证你的解决方案
./cudalings verify

# 需要帮助？
./cudalings hint
```

## 推荐的学习流程

1. **阅读练习描述**: 每个练习文件都有详细的说明
2. **理解任务**: 确保明白要实现什么
3. **编写代码**: 填写 TODO 部分
4. **验证**: 使用 `cudalings verify` 测试
5. **迭代**: 如果失败，查看错误信息并修正
6. **获取提示**: 如果卡住了，使用 `cudalings hint`
7. **继续前进**: 完成后自动进入下一个练习

## 监视模式

最便捷的学习方式是使用监视模式:

```bash
./cudalings watch
```

这会自动检测文件变化并立即验证你的代码，提供即时反馈！

## 常见问题

### Q: 编译错误 "nvcc: command not found"

A: 确保 CUDA Toolkit 已安装并且 PATH 设置正确。

### Q: 运行时错误 "no CUDA-capable device is detected"

A: 这意味着你的系统没有 NVIDIA GPU 或驱动未正确安装。

### Q: 如何跳过某个练习？

A: 虽然不推荐，但你可以手动标记为完成:

```bash
echo "N" >> ~/.cudalings/progress.txt  # N 是练习编号
```

### Q: 如何重置进度？

A: 删除进度文件:

```bash
rm ~/.cudalings/progress.txt
```

## 学习资源

- [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [CUDA Toolkit Documentation](https://docs.nvidia.com/cuda/)

## 获取帮助

如果遇到问题:

1. 查看练习的提示
2. 阅读 CUDA 官方文档
3. 查看参考答案（最后的手段）
4. 在项目 issue 中提问

祝学习愉快！ 🚀
