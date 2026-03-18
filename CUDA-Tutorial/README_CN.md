# JAXlings 🔥

**交互式 JAX 学习练习，带自动评判系统** - 灵感来自 Rustlings！

JAXlings 是一个全面的教程系统，通过动手编码练习，从入门到高级教授 JAX。

## 🎯 什么是 JAXlings？

JAXlings 通过修复小练习来帮助你学习 JAX。每个练习都旨在教你 JAX 中的特定概念，从基本数组操作到高级主题，如自定义梯度和注意力机制。

## ✨ 特性

- **25+ 练习**涵盖从基础到高级的 JAX 主题
- **自动评判** - 对你的解决方案即时反馈
- **观察模式** - 保存时自动重新运行练习
- **渐进难度** - 从入门到高级主题
- **实际示例** - 神经网络、优化器、CNN、注意力机制
- **全面覆盖**：
  - JAX 数组和操作简介
  - 数组操作（索引、重塑、广播）
  - 使用 `grad` 进行自动微分
  - JIT 编译以提高性能
  - 使用 `vmap` 进行向量化
  - 神经网络构建模块
  - 优化器（SGD、Adam、RMSprop）
  - 高级主题（CNN、批归一化、注意力）

## 🚀 开始使用

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/jaxlings.git
cd jaxlings

# 安装依赖
pip install -r requirements.txt

# 或以开发模式安装
pip install -e .
```

### 快速开始

```bash
# 运行下一个待完成的练习
python jaxlings.py verify

# 或使用安装的命令
jaxlings verify
```

## 📚 如何使用

### 基本命令

```bash
# 验证下一个练习
jaxlings verify

# 观察模式 - 文件更改时自动运行
jaxlings watch

# 运行特定练习
jaxlings run intro01_hello_jax

# 列出所有练习
jaxlings list

# 获取当前练习的提示
jaxlings hint

# 获取特定练习的提示
jaxlings hint arrays01_indexing

# 重置所有进度
jaxlings reset
```

### 工作流程

1. **从第一个练习开始：**
   ```bash
   jaxlings verify
   ```

2. **在编辑器中打开练习文件**（将显示路径）

3. **阅读说明**并修复代码

4. **删除 `# I AM NOT DONE` 注释**，当你认为完成时

5. **再次运行练习：**
   ```bash
   jaxlings verify
   ```

6. **使用观察模式**获得自动反馈：
   ```bash
   jaxlings watch
   ```

## 📖 练习结构

练习分为 5 个类别：

### 01. 入门（3个练习）
- `intro01_hello_jax` - JAX 入门
- `intro02_arrays` - 创建 JAX 数组
- `intro03_operations` - 基本数组操作

### 02. 数组（4个练习）
- `arrays01_indexing` - 数组索引和切片
- `arrays02_reshaping` - 重塑和转置
- `arrays03_broadcasting` - 广播规则
- `arrays04_advanced_indexing` - 使用 `.at[]` 进行函数式更新

### 03. 变换（5个练习）
- `transform01_grad` - 自动微分
- `transform02_value_and_grad` - 计算值和梯度
- `transform03_jit` - JIT 编译以提高速度
- `transform04_vmap` - 自动向量化
- `transform05_combining` - 组合变换

### 04. 神经网络（5个练习）
- `nn01_linear_layer` - 构建线性层
- `nn02_activation` - 激活函数
- `nn03_loss_functions` - 损失函数
- `nn04_simple_mlp` - 多层感知器
- `nn05_training_loop` - 训练循环和优化

### 05. 高级（5个练习）
- `advanced01_custom_grad` - 使用 `custom_vjp` 自定义梯度
- `advanced02_optimizer` - 实现优化器
- `advanced03_cnn` - 卷积神经网络
- `advanced04_batch_norm` - 批归一化
- `advanced05_attention` - 注意力机制

## 🎓 学习路径

**初学者**（入门 + 数组）
→ **中级**（变换）
→ **高级**（神经网络 + 高级）

每个练习都建立在之前的概念上，所以我们建议按顺序学习！

## 💡 提示

- **阅读提示！**卡住时使用 `jaxlings hint`
- **本地运行测试** - 每个练习文件都可以用 `python exercises/.../exercise.py` 运行
- **使用观察模式** - `jaxlings watch` 提供即时反馈
- **阅读 JAX 文档** - https://jax.readthedocs.io/
- **不要跳过练习** - 每一个都教授重要概念

## 🎯 你将学到什么

完成 JAXlings 后，你将掌握：

- ✅ JAX 数组操作和 NumPy 兼容性
- ✅ 自动微分和梯度计算
- ✅ JIT 编译以优化性能
- ✅ 使用 vmap 进行高效批处理的向量化
- ✅ 从头开始构建神经网络
- ✅ 实现现代优化器
- ✅ 创建 CNN 和注意力机制
- ✅ JAX 开发的最佳实践

## 🚀 下一步

完成 JAXlings 后，查看：

- [Flax](https://github.com/google/flax) - JAX 的神经网络库
- [Optax](https://github.com/deepmind/optax) - 梯度处理和优化库
- [Haiku](https://github.com/deepmind/dm-haiku) - DeepMind 的神经网络库

---

**快乐学习！🎉**

如果你觉得 JAXlings 有帮助，请给它一个星标 ⭐！
