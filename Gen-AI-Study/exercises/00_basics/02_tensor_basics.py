"""
练习 02: PyTorch 张量基础

PyTorch 张量(Tensor)是深度学习的核心数据结构。
它类似于 NumPy 数组，但可以在 GPU 上运行，并支持自动微分。

在这个练习中，你将学习：
- 创建张量
- 张量与 NumPy 的转换
- 基本张量操作
"""

import torch
import numpy as np


def create_tensors():
    """创建张量的各种方法"""
    # TODO: 从 Python 列表创建张量
    t1 = torch.___([1.0, 2.0, 3.0, 4.0])  # 使用 torch.tensor()

    # TODO: 创建 3x3 的全零张量
    zeros = torch.___(3, 3)  # 使用 torch.zeros()

    # TODO: 创建 2x4 的全一张量
    ones = torch.___(2, 4)  # 使用 torch.ones()

    # TODO: 创建 3x3 的随机张量（均匀分布 0-1）
    rand_tensor = torch.___(3, 3)  # 使用 torch.rand()

    # TODO: 创建 3x3 的随机张量（标准正态分布）
    randn_tensor = torch.___(3, 3)  # 使用 torch.randn()

    return t1, zeros, ones, rand_tensor, randn_tensor


def tensor_numpy_conversion():
    """张量与 NumPy 数组的相互转换"""
    # NumPy 转 PyTorch
    np_array = np.array([1.0, 2.0, 3.0])

    # TODO: 将 NumPy 数组转换为 PyTorch 张量
    tensor_from_np = torch.___(np_array)  # 使用 torch.from_numpy()

    # PyTorch 转 NumPy
    tensor = torch.tensor([4.0, 5.0, 6.0])

    # TODO: 将 PyTorch 张量转换为 NumPy 数组
    np_from_tensor = tensor.___()  # 使用 .numpy() 方法

    return tensor_from_np, np_from_tensor


def tensor_operations():
    """张量的基本运算"""
    a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

    # TODO: 矩阵乘法（注意不是元素级乘法）
    # 使用 @ 运算符或 torch.matmul()
    matmul_result = a ___ b  # 填入矩阵乘法运算符

    # TODO: 计算张量所有元素的和
    sum_result = a.___()  # 使用 .sum()

    # TODO: 计算张量所有元素的均值
    mean_result = a.___()  # 使用 .mean()

    # TODO: 沿着第 0 维（行）求和
    row_sum = a.sum(dim=___)  # 填入维度

    # TODO: 沿着第 1 维（列）求和
    col_sum = a.sum(dim=___)  # 填入维度

    return matmul_result, sum_result, mean_result, row_sum, col_sum


def tensor_shapes():
    """张量形状操作"""
    t = torch.arange(24)  # 0 到 23 的张量

    # TODO: 将张量 reshape 成 2x3x4
    reshaped = t.___(2, 3, 4)  # 使用 .view() 或 .reshape()

    # TODO: 获取张量的形状
    shape = reshaped.___  # 使用 .shape 属性

    # TODO: 获取张量的维度数
    ndim = reshaped.___  # 使用 .dim() 方法

    # TODO: 将形状为 (2, 3, 4) 的张量展平成一维
    flattened = reshaped.___()  # 使用 .flatten()

    return reshaped, shape, ndim, flattened


def main():
    print("测试 create_tensors...")
    t1, zeros, ones, rand_t, randn_t = create_tensors()
    assert torch.equal(t1, torch.tensor([1.0, 2.0, 3.0, 4.0]))
    assert zeros.shape == (3, 3) and torch.all(zeros == 0)
    assert ones.shape == (2, 4) and torch.all(ones == 1)
    assert rand_t.shape == (3, 3)
    assert randn_t.shape == (3, 3)
    print("✓ create_tensors 通过!")

    print("\n测试 tensor_numpy_conversion...")
    tensor_from_np, np_from_tensor = tensor_numpy_conversion()
    assert isinstance(tensor_from_np, torch.Tensor)
    assert isinstance(np_from_tensor, np.ndarray)
    print("✓ tensor_numpy_conversion 通过!")

    print("\n测试 tensor_operations...")
    matmul, sum_r, mean_r, row_sum, col_sum = tensor_operations()
    expected_matmul = torch.tensor([[19.0, 22.0], [43.0, 50.0]])
    assert torch.allclose(matmul, expected_matmul)
    assert torch.allclose(sum_r, torch.tensor(10.0))
    assert torch.allclose(mean_r, torch.tensor(2.5))
    assert torch.allclose(row_sum, torch.tensor([4.0, 6.0]))
    assert torch.allclose(col_sum, torch.tensor([3.0, 7.0]))
    print("✓ tensor_operations 通过!")

    print("\n测试 tensor_shapes...")
    reshaped, shape, ndim, flattened = tensor_shapes()
    assert reshaped.shape == (2, 3, 4)
    assert shape == torch.Size([2, 3, 4])
    assert ndim == 3
    assert flattened.shape == (24,)
    print("✓ tensor_shapes 通过!")

    print("\n🎉 所有测试通过！PyTorch 张量基础掌握完成！")


if __name__ == "__main__":
    main()
