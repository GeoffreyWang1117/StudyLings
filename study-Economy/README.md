# Economlings - 经济学交互式学习系统

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个类似 [Rustlings](https://github.com/rust-lang/rustlings) 的交互式学习系统，帮助你通过实践学习主流经济学经典模型和经验公式。

## 特点

- **循序渐进**: 从基础概念到高级模型，由浅入深
- **动手实践**: 通过编程实现经济学模型，加深理解
- **即时反馈**: 自动检查答案，提供详细错误信息
- **进度追踪**: 记录学习进度，随时继续
- **CUDA支持**: 计量经济学和高级模型支持GPU加速（可选）

## 安装

```bash
# 克隆仓库
git clone https://github.com/example/economlings.git
cd economlings

# 安装依赖
pip install -r requirements.txt

# 或者使用 pip 安装（开发模式）
pip install -e .
```

### CUDA 支持（可选）

如果你有 NVIDIA GPU 并想使用 CUDA 加速：

```bash
pip install torch
```

## 使用方法

### 基本命令

```bash
# 启动学习系统，查看当前进度和下一个练习
python -m economlings

# 运行特定练习
python -m economlings run supply_demand1

# 查看所有练习
python -m economlings list

# 查看学习进度
python -m economlings progress

# 获取练习提示
python -m economlings hint supply_demand1

# 监视模式（自动检测文件变化并运行）
python -m economlings watch

# 重置练习进度
python -m economlings reset supply_demand1
python -m economlings reset --all  # 重置所有进度
```

### 学习流程

1. 运行 `python -m economlings` 查看下一个练习
2. 打开练习文件（如 `exercises/01_basics/supply_demand1.py`）
3. 阅读注释中的说明，理解任务
4. 实现标记为 `TODO` 的函数
5. 运行练习文件或使用 `python -m economlings run <练习名>` 检查答案
6. 如果遇到困难，使用 `python -m economlings hint <练习名>` 获取提示
7. 完成后继续下一个练习

## 课程大纲

### 第1章：基础概念 (6个练习)
- `intro1.py` - Python基础与经济学数据类型
- `supply_demand1.py` - 供给与需求基础
- `supply_demand2.py` - 市场均衡计算
- `elasticity1.py` - 价格弹性
- `elasticity2.py` - 交叉弹性与收入弹性
- `marginal1.py` - 边际分析入门

### 第2章：微观经济学 (11个练习)
- 效用函数与边际效用
- 无差异曲线与预算约束
- 消费者最优选择
- 生产函数（柯布-道格拉斯）
- 成本函数与利润最大化
- 垄断定价
- 博弈论与纳什均衡

### 第3章：宏观经济学 (10个练习)
- GDP计算
- 乘数效应
- IS-LM模型
- 总需求-总供给模型
- 菲利普斯曲线
- 索洛增长模型
- 奥肯定律

### 第4章：金融经济学 (8个练习)
- 货币时间价值
- NPV与IRR
- 投资组合理论
- CAPM
- 有效前沿
- Black-Scholes期权定价
- 债券定价

### 第5章：计量经济学 (8个练习) [可选CUDA]
- 线性回归
- OLS估计
- 假设检验
- 时间序列分析
- ARIMA模型
- GARCH模型
- 面板数据分析

### 第6章：高级模型 (4个练习) [CUDA加速]
- DSGE模型入门
- 蒙特卡洛模拟
- 神经网络在经济学中的应用
- 强化学习与经济决策

## 项目结构

```
study-Economy/
├── economlings/           # 核心框架
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py            # 命令行界面
│   ├── runner.py         # 练习运行器
│   ├── checker.py        # 答案检查器
│   ├── progress.py       # 进度追踪
│   └── utils.py          # 工具函数
├── exercises/            # 练习文件
│   ├── 01_basics/
│   ├── 02_microeconomics/
│   ├── 03_macroeconomics/
│   ├── 04_finance/
│   ├── 05_econometrics/
│   └── 06_advanced/
├── tests/                # 测试文件
├── solutions/            # 参考答案（隐藏）
├── requirements.txt
├── setup.py
└── README.md
```

## 练习文件格式

每个练习文件包含：
- 难度标记（★☆☆☆☆ 到 ★★★★★）
- 主题说明
- 详细的任务描述
- 提示（HINT）
- 需要实现的函数（带 `TODO` 注释）
- 自动检查代码

示例：
```python
# EXERCISE: supply_demand1
# DIFFICULTY: ★☆☆☆☆
# TOPIC: 供给与需求基础
#
# 说明：
# 在这个练习中，你需要实现一个简单的供需模型。
#
# HINT: 供给函数的截距为-10，斜率为2

def supply(price: float) -> float:
    """计算给定价格下的供给量。"""
    # TODO: 实现供给函数
    pass

# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
```

## 贡献

欢迎贡献！你可以：
- 报告 Bug
- 提出新功能建议
- 添加新的练习
- 改进文档

## 许可证

MIT License

## 致谢

- 灵感来自 [Rustlings](https://github.com/rust-lang/rustlings)
- 感谢所有贡献者
