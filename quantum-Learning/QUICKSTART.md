# 快速入门指南 ⚡

5分钟开始你的量子编程之旅！

## 第一步：安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/quantum-Learning.git
cd quantum-Learning

# 安装依赖
pip install -r requirements.txt
```

## 第二步：开始第一个练习

```bash
# 启动学习模式
python quantum_rustlings.py watch
```

你会看到类似这样的输出：

```
🚀 Quantum Rustlings - 开始学习！

当前练习: intro01_qubit
文件: exercises/intro/01_qubit.py

✗ intro01_qubit 失败

错误:
  AssertionError: 电路不能为 None

💡 提示:
量子比特是量子计算的基本单位...
```

## 第三步：编辑练习文件

打开 `exercises/intro/01_qubit.py`：

```python
def create_single_qubit_circuit():
    # TODO: 创建一个包含 1 个量子比特的量子电路
    qc = None  # 替换这一行
    return qc
```

修改为：

```python
def create_single_qubit_circuit():
    # TODO: 创建一个包含 1 个量子比特的量子电路
    qc = QuantumCircuit(1)  # ✅ 完成！
    return qc
```

## 第四步：保存并查看结果

保存文件后，watch 模式会自动运行测试：

```
✓ intro01_qubit 通过！
🎉 恭喜！你已完成第一个练习！

当前练习: intro02_superposition
文件: exercises/intro/02_superposition.py
...
```

## 常用命令

```bash
# 查看所有练习和进度
python quantum_rustlings.py list

# 查看当前练习的提示
python quantum_rustlings.py hint

# 验证所有练习
python quantum_rustlings.py verify

# 重置进度
python quantum_rustlings.py reset
```

## 学习建议

### 对于纯新手

1. **从头开始**：不要跳过练习，每个都很重要
2. **阅读说明**：每个文件都有详细的知识点解释
3. **实践为主**：动手写代码比看教程更重要
4. **利用提示**：卡住了就用 `hint` 命令
5. **Google搜索**：遇到不懂的概念就搜索

### 对于有编程基础的学习者

1. **快速过基础**：01-04可能很简单，快速完成
2. **重点在算法**：08-13 是核心，仔细学习
3. **挑战高级题**：19-30 包含前沿内容，值得深入

### 对于量子计算初学者

1. **理解概念**：不要只是完成代码，要理解为什么
2. **运行实验**：修改参数，看看会发生什么
3. **画图可视化**：使用 `qc.draw()` 查看电路
4. **查阅资源**：README 中有推荐的书籍和课程

## 练习结构

每个练习文件包含：

- **文档字符串**：解释目标和知识点
- **TODO 标记**：需要你完成的代码
- **测试函数**：自动验证你的答案
- **说明文字**：额外的背景知识

## 进度跟踪

你的进度保存在 `.progress` 文件中：

```bash
# 查看你的进度
cat .progress
```

## 获取帮助

- **卡住了？** 使用 `hint` 命令
- **发现错误？** 提交 Issue
- **想讨论？** 使用 GitHub Discussions

## 下一步

完成所有练习后：

1. **在真实硬件上运行**：
   - 注册 [IBM Quantum](https://quantum-computing.ibm.com/)
   - 或使用 [AWS Braket](https://aws.amazon.com/braket/)

2. **深入学习**：
   - 阅读研究论文
   - 参加量子计算课程
   - 加入量子计算社区

3. **贡献项目**：
   - 添加新练习
   - 改进文档
   - 分享你的经验

## 常见问题

### Q: 我需要量子力学背景吗？
A: 不需要！这个课程从零开始。

### Q: 需要多久完成？
A: 取决于你的背景，大约 10-30 小时。

### Q: 能在真实量子计算机上运行吗？
A: 可以！完成练习后，可以将代码移植到 IBM Quantum 等平台。

### Q: 练习有参考答案吗？
A: 部分练习在 `solutions/` 目录下有参考答案，但建议先自己尝试。

---

**准备好了吗？开始学习吧！** 🚀

```bash
python quantum_rustlings.py watch
```
