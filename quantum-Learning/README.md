# Quantum Rustlings 🚀

> 从零基础到2025年前沿的量子编程学习之旅

一个类似 [Rustlings](https://github.com/rust-lang/rustlings) 的交互式量子计算学习系统，使用 Python 和 Quantum Circuit Model（量子电路模型）。

## ✨ 特性

- 📚 **渐进式学习**：从量子比特基础到最前沿的量子LDPC码
- 🎯 **实践导向**：30个精心设计的练习题
- 🔄 **即时反馈**：自动测试和提示系统
- 🎨 **友好界面**：彩色终端输出和清晰的错误信息
- 🔬 **前沿内容**：涵盖2024-2025年最新研究进展

## 📋 学习路径

### Level 1: 量子基础 (01-04)
- **01_qubit**: 量子比特基础
- **02_superposition**: 量子叠加态
- **03_measurement**: 量子测量
- **04_gates**: 基本量子门

### Level 2: 量子纠缠与协议 (05-07)
- **05_bell_state**: 贝尔态（量子纠缠）
- **06_ghz_state**: GHZ态（多量子比特纠缠）
- **07_teleportation**: 量子隐形传态

### Level 3: 经典量子算法 (08-13)
- **08_deutsch**: Deutsch算法（第一个量子优势）
- **09_deutsch_jozsa**: Deutsch-Jozsa算法
- **10_bernstein_vazirani**: Bernstein-Vazirani算法
- **11_grover**: Grover搜索算法（二次加速）
- **12_qft**: 量子傅立叶变换
- **13_shor**: Shor因数分解算法

### Level 4: 量子纠错 (14-18)
- **14_bit_flip**: 比特翻转码
- **15_phase_flip**: 相位翻转码
- **16_shor_code**: Shor 9量子比特码
- **17_syndrome**: Syndrome测量
- **18_surface_code_intro**: 表面码入门

### Level 5: 变分量子算法 (19-22)
- **19_vqe**: VQE（变分量子本征求解器）
- **20_qaoa**: QAOA（量子近似优化算法）
- **21_qml**: 量子机器学习基础
- **22_qnn**: 量子神经网络

### Level 6: NISQ时代应用 (23-25)
- **23_simulation**: 量子模拟
- **24_chemistry**: 量子化学应用
- **25_optimization**: 量子优化问题

### Level 7: 前沿主题 (26-30) 🔥
- **26_fault_tolerant**: 容错量子计算
- **27_qgan**: 量子生成对抗网络（2023-2024热点）
- **28_qnn_advanced**: 高级量子神经网络
- **29_quantum_advantage**: 量子优势实验
- **30_ldpc_codes**: 量子LDPC码（2024-2025最前沿）

## 🚀 快速开始

### 安装依赖

```bash
# 安装 Python 3.8+
# 安装 Qiskit 和其他依赖
pip install qiskit qiskit-aer scipy numpy matplotlib toml
```

### 开始学习

```bash
# 克隆仓库
git clone https://github.com/yourusername/quantum-Learning.git
cd quantum-Learning

# 开始学习！
python quantum_rustlings.py watch
```

### 其他命令

```bash
# 列出所有练习和进度
python quantum_rustlings.py list

# 验证所有练习
python quantum_rustlings.py verify

# 查看当前练习的提示
python quantum_rustlings.py hint

# 重置学习进度
python quantum_rustlings.py reset
```

## 📖 使用方法

1. **开始学习模式**：运行 `python quantum_rustlings.py watch`
2. **阅读题目**：每个练习文件都包含详细的说明和知识点
3. **完成代码**：找到 `TODO` 标记，填写你的代码
4. **运行测试**：保存文件后会自动测试（watch模式）
5. **查看提示**：如果卡住了，使用 `hint` 命令
6. **进入下一题**：测试通过后自动进入下一个练习

### 示例：完成第一个练习

```python
# exercises/intro/01_qubit.py

def create_single_qubit_circuit():
    """创建一个单量子比特电路"""
    # TODO: 创建一个包含 1 个量子比特的量子电路
    qc = QuantumCircuit(1)  # 填写这里
    return qc
```

运行测试：
```bash
python exercises/intro/01_qubit.py
```

或使用 watch 模式：
```bash
python quantum_rustlings.py watch
```

## 🎯 学习目标

完成所有练习后，你将能够：

- ✅ 理解量子计算的基本概念（叠加、纠缠、测量）
- ✅ 掌握主要的量子算法（Grover、Shor、VQE等）
- ✅ 了解量子纠错的原理和方法
- ✅ 使用变分算法解决实际问题
- ✅ 跟上2024-2025年的最新研究进展
- ✅ 在真实量子硬件上运行程序

## 🔧 技术栈

- **Python 3.8+**
- **Qiskit**：IBM的开源量子计算框架
- **Qiskit Aer**：高性能量子电路模拟器
- **NumPy**：数值计算
- **SciPy**：科学计算和优化
- **Matplotlib**：可视化

## 📚 推荐资源

### 书籍
- *Quantum Computation and Quantum Information* - Nielsen & Chuang
- *Programming Quantum Computers* - Johnston, Harrigan & Gimeno-Segovia
- *Learn Quantum Computing with Python and Q#* - Kaiser & Granade

### 在线课程
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)
- [Qiskit Textbook](https://qiskit.org/textbook/)
- [Quantum Computing for the Very Curious](https://quantum.country/)

### 论文 (2024-2025 前沿)
- Quantum LDPC Codes (Panteleev & Kalachev, 2022)
- Quantum Advantage Experiments (Google AI, 2023)
- Variational Quantum Algorithms (McClean et al., 2024)

## 🤝 贡献

欢迎贡献！如果你想添加新的练习或改进现有内容：

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-exercise`)
3. 提交你的改动 (`git commit -m 'Add some amazing exercise'`)
4. 推送到分支 (`git push origin feature/amazing-exercise`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 灵感来自 [Rustlings](https://github.com/rust-lang/rustlings)
- 使用 [Qiskit](https://qiskit.org/) 量子计算框架
- 参考了多个优秀的量子计算教程和课程

## 🌟 Star History

如果这个项目对你有帮助，请给它一个星标！⭐

## 📞 联系方式

- Issues: [GitHub Issues](https://github.com/yourusername/quantum-Learning/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/quantum-Learning/discussions)

---

**开始你的量子编程之旅吧！🚀**

记住：
> "如果你认为你理解了量子力学，那你就还没有理解量子力学。" - Richard Feynman

但不用担心，通过实践，你会逐渐建立直觉！💪
