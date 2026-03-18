"""
练习 01: NumPy 基础

NumPy 是科学计算的基础库，也是深度学习的基石。
在这个练习中，你将学习：
- 创建数组
- 数组运算
- 数组形状操作

提示：NumPy 数组操作是向量化的，比 Python 循环快得多
"""

import numpy as np


def create_arrays():
    """创建基本数组"""
    # TODO: 创建一个包含 [1, 2, 3, 4, 5] 的一维数组
    arr1 = np.___([1, 2, 3, 4, 5])  # 使用 np.array()

    # TODO: 创建一个 3x3 的全零数组
    zeros = np.___((___, ___))  # 使用 np.zeros()，填入形状

    # TODO: 创建一个 2x4 的全一数组
    ones = np.___((___, ___))  # 使用 np.ones()，填入形状

    # TODO: 创建一个 0 到 9 的数组（共10个数）
    range_arr = np.___(10)  # 使用 np.arange()

    return arr1, zeros, ones, range_arr


def array_operations():
    """数组运算"""
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])

    # TODO: 计算 a 和 b 的元素级加法
    add_result = a ___ b  # 填入运算符

    # TODO: 计算 a 和 b 的元素级乘法
    mul_result = a ___ b  # 填入运算符

    # TODO: 计算 a 的每个元素的平方
    square_result = a ___ ___  # 使用 ** 运算符，填入指数

    return add_result, mul_result, square_result


def array_shapes():
    """数组形状操作"""
    arr = np.arange(12)

    # TODO: 将一维数组 reshape 成 3x4 的二维数组
    reshaped = arr.reshape((___, ___))  # 填入目标形状

    # TODO: 获取数组的形状
    shape = reshaped.___  # 使用 shape 属性

    # TODO: 将 3x4 数组转置成 4x3 数组
    transposed = reshaped.___  # 使用转置属性或方法

    return reshaped, shape, transposed


def main():
    print("测试 create_arrays...")
    arr1, zeros, ones, range_arr = create_arrays()
    assert np.array_equal(arr1, np.array([1, 2, 3, 4, 5]))
    assert zeros.shape == (3, 3) and np.all(zeros == 0)
    assert ones.shape == (2, 4) and np.all(ones == 1)
    assert np.array_equal(range_arr, np.arange(10))
    print("✓ create_arrays 通过!")

    print("\n测试 array_operations...")
    add_result, mul_result, square_result = array_operations()
    assert np.array_equal(add_result, np.array([6, 8, 10, 12]))
    assert np.array_equal(mul_result, np.array([5, 12, 21, 32]))
    assert np.array_equal(square_result, np.array([1, 4, 9, 16]))
    print("✓ array_operations 通过!")

    print("\n测试 array_shapes...")
    reshaped, shape, transposed = array_shapes()
    assert reshaped.shape == (3, 4)
    assert shape == (3, 4)
    assert transposed.shape == (4, 3)
    print("✓ array_shapes 通过!")

    print("\n🎉 所有测试通过！NumPy 基础掌握完成！")


if __name__ == "__main__":
    main()
