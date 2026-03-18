"""
练习 03: 自动微分 (Autograd)

自动微分是深度学习训练的核心。PyTorch 的 autograd 包能够自动计算梯度。

在这个练习中，你将学习：
- requires_grad 参数的作用
- 计算图的构建
- 梯度的计算和访问
- 梯度的清零
"""

import torch


def basic_gradient():
    """计算简单函数的梯度"""
    # TODO: 创建一个张量，设置 requires_grad=True 以追踪计算
    x = torch.tensor([2.0, 3.0], requires_grad=___)  # 填入 True

    # 计算 y = x^2 + 2x + 1
    y = x ** 2 + 2 * x + 1

    # TODO: 计算 y 对 x 的梯度
    # 首先需要对 y 求和（因为 backward 需要标量）
    loss = y.sum()
    loss.___()  # 调用 backward() 方法

    # TODO: 获取 x 的梯度
    # 对于 y = x^2 + 2x + 1, dy/dx = 2x + 2
    # 当 x = [2.0, 3.0] 时，梯度应该是 [6.0, 8.0]
    grad = x.___  # 使用 .grad 属性

    return grad


def gradient_with_operations():
    """理解复杂运算的梯度"""
    # 创建需要梯度的张量
    w = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
    x = torch.tensor([[1.0], [1.0]])  # 不需要梯度

    # 前向传播: y = w @ x
    y = w @ x

    # 计算损失 (简单求和)
    loss = y.sum()

    # TODO: 反向传播
    ___.backward()  # 对哪个变量调用 backward？

    # TODO: 获取 w 的梯度
    w_grad = ___.grad  # 从哪里获取梯度？

    return w_grad


def gradient_accumulation():
    """理解梯度累积"""
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

    # 第一次前向和反向传播
    y1 = (x ** 2).sum()
    y1.backward()
    grad_after_first = x.grad.clone()

    # TODO: 在第二次反向传播前，需要清零梯度
    # 否则梯度会累积
    x.grad.___()  # 使用 zero_() 方法

    # 第二次前向和反向传播
    y2 = (x ** 2).sum()
    y2.backward()
    grad_after_second = x.grad.clone()

    return grad_after_first, grad_after_second


def no_grad_context():
    """使用 no_grad 上下文管理器"""
    x = torch.tensor([1.0, 2.0], requires_grad=True)

    # 正常计算（追踪梯度）
    y_with_grad = x ** 2

    # TODO: 在不追踪梯度的情况下计算
    # 使用 torch.no_grad() 上下文管理器
    with torch.___():  # 填入 no_grad()
        y_without_grad = x ** 2

    # 检查是否需要梯度
    requires_grad_with = y_with_grad.requires_grad
    requires_grad_without = y_without_grad.requires_grad

    return requires_grad_with, requires_grad_without


def detach_tensor():
    """分离张量以停止梯度追踪"""
    x = torch.tensor([1.0, 2.0], requires_grad=True)
    y = x ** 2

    # TODO: 创建一个与 y 共享数据但不追踪梯度的新张量
    y_detached = y.___()  # 使用 detach() 方法

    return y.requires_grad, y_detached.requires_grad


def main():
    print("测试 basic_gradient...")
    grad = basic_gradient()
    expected = torch.tensor([6.0, 8.0])
    assert torch.allclose(grad, expected), f"期望 {expected}，得到 {grad}"
    print("✓ basic_gradient 通过!")

    print("\n测试 gradient_with_operations...")
    w_grad = gradient_with_operations()
    expected = torch.tensor([[1.0, 1.0], [1.0, 1.0]])
    assert torch.allclose(w_grad, expected), f"期望 {expected}，得到 {w_grad}"
    print("✓ gradient_with_operations 通过!")

    print("\n测试 gradient_accumulation...")
    grad1, grad2 = gradient_accumulation()
    # 两次的梯度应该相同（因为清零了）
    assert torch.allclose(grad1, grad2), "梯度应该相同，说明清零成功"
    print("✓ gradient_accumulation 通过!")

    print("\n测试 no_grad_context...")
    with_grad, without_grad = no_grad_context()
    assert with_grad == True, "有梯度追踪的结果应该 requires_grad=True"
    assert without_grad == False, "no_grad 上下文中的结果应该 requires_grad=False"
    print("✓ no_grad_context 通过!")

    print("\n测试 detach_tensor...")
    original_grad, detached_grad = detach_tensor()
    assert original_grad == True
    assert detached_grad == False
    print("✓ detach_tensor 通过!")

    print("\n🎉 所有测试通过！自动微分掌握完成！")


if __name__ == "__main__":
    main()
