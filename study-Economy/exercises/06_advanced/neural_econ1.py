# EXERCISE: neural_econ1
# DIFFICULTY: ★★★★★
# TOPIC: 神经网络在经济学中的应用
#
# 说明：
# 神经网络可以捕捉复杂的非线性关系。
#
# 经济学应用：
# 1. 预测宏观经济指标
# 2. 资产价格预测
# 3. 政策效果估计
# 4. 消费者行为建模
#
# 简单前馈神经网络：
# Layer 1: h = σ(W₁x + b₁)
# Layer 2: y = W₂h + b₂
#
# 激活函数：
# - ReLU: max(0, x)
# - Sigmoid: 1 / (1 + e^(-x))
# - Tanh: (e^x - e^(-x)) / (e^x + e^(-x))
#
# 任务：
# 1. 实现基本神经网络操作
# 2. 理解梯度下降
# 3. 应用于经济数据
#
# HINT1: 可以使用PyTorch的CUDA加速
# HINT2: 注意过拟合问题

import numpy as np
from typing import Callable


def relu(x: np.ndarray) -> np.ndarray:
    """
    ReLU激活函数。

    ReLU(x) = max(0, x)

    参数:
        x: 输入数组

    返回:
        激活后的输出
    """
    # TODO: 实现ReLU
    pass


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """
    ReLU导数。

    ReLU'(x) = 1 if x > 0 else 0

    参数:
        x: 输入数组

    返回:
        导数
    """
    # TODO: 实现ReLU导数
    pass


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid激活函数。

    σ(x) = 1 / (1 + e^(-x))

    参数:
        x: 输入数组

    返回:
        激活后的输出
    """
    # TODO: 实现sigmoid
    pass


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """
    Sigmoid导数。

    σ'(x) = σ(x)(1 - σ(x))

    参数:
        x: 输入数组

    返回:
        导数
    """
    # TODO: 实现sigmoid导数
    pass


def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    均方误差损失。

    MSE = (1/n) Σ(yi - ŷi)²

    参数:
        y_true: 真实值
        y_pred: 预测值

    返回:
        MSE损失
    """
    # TODO: 计算MSE
    pass


def mse_gradient(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    MSE损失的梯度。

    ∂MSE/∂ŷ = (2/n)(ŷ - y)

    参数:
        y_true: 真实值
        y_pred: 预测值

    返回:
        梯度
    """
    # TODO: 计算MSE梯度
    pass


def forward_pass(
    x: np.ndarray,
    w1: np.ndarray,
    b1: np.ndarray,
    w2: np.ndarray,
    b2: np.ndarray,
    activation: Callable = relu
) -> tuple[np.ndarray, np.ndarray]:
    """
    两层神经网络前向传播。

    h = activation(W₁x + b₁)
    y = W₂h + b₂

    参数:
        x: 输入 (batch_size × input_dim)
        w1: 第一层权重 (input_dim × hidden_dim)
        b1: 第一层偏置 (hidden_dim,)
        w2: 第二层权重 (hidden_dim × output_dim)
        b2: 第二层偏置 (output_dim,)
        activation: 激活函数

    返回:
        (隐层输出h, 最终输出y)
    """
    # TODO: 前向传播
    pass


def gradient_descent_step(
    params: np.ndarray,
    gradients: np.ndarray,
    learning_rate: float
) -> np.ndarray:
    """
    梯度下降更新步骤。

    θ = θ - α × ∇L

    参数:
        params: 当前参数
        gradients: 梯度
        learning_rate: 学习率

    返回:
        更新后的参数
    """
    # TODO: 梯度下降更新
    pass


def normalize_features(x: np.ndarray) -> tuple[np.ndarray, float, float]:
    """
    特征标准化。

    x_norm = (x - μ) / σ

    参数:
        x: 原始特征

    返回:
        (标准化特征, 均值, 标准差)
    """
    # TODO: 标准化特征
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
