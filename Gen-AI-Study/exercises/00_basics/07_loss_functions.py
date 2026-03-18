"""
练习 07: 损失函数 (Loss Functions)

损失函数衡量模型预测与真实值之间的差距。
不同任务需要不同的损失函数。

常见损失函数：
- MSE Loss: 回归任务
- Cross Entropy Loss: 分类任务
- BCE Loss: 二分类任务
- KL Divergence: 概率分布匹配

在这个练习中，你将学习：
- 各种损失函数的数学原理
- 手动实现常见损失函数
- 理解何时使用哪种损失函数
"""

import torch
import torch.nn.functional as F
import math


def mse_loss(pred, target):
    """
    均方误差损失 (Mean Squared Error)

    MSE = (1/n) * Σ(pred_i - target_i)^2

    用于回归任务
    """
    # TODO: 计算 MSE
    diff = pred - target
    mse = (diff ** ___).mean()  # 填入 2
    return mse


def mae_loss(pred, target):
    """
    平均绝对误差 (Mean Absolute Error / L1 Loss)

    MAE = (1/n) * Σ|pred_i - target_i|

    对异常值更鲁棒
    """
    # TODO: 计算 MAE
    mae = torch.___(pred - target).mean()  # 使用 abs
    return mae


def cross_entropy_loss(logits, targets):
    """
    交叉熵损失 (Cross Entropy Loss)

    CE = -Σ target_i * log(softmax(logits)_i)

    对于 one-hot 目标，等价于 -log(softmax(logits)[correct_class])

    Args:
        logits: 未归一化的预测 (batch, num_classes)
        targets: 类别索引 (batch,)
    """
    # TODO: 计算 log_softmax
    # log_softmax 比 log(softmax) 数值更稳定
    log_probs = F.log_softmax(logits, dim=___)  # 填入维度 -1 或 1

    # TODO: 收集正确类别的 log 概率
    # 使用 gather 或索引
    batch_size = logits.shape[0]
    ce = -log_probs[torch.arange(batch_size), targets].mean()

    return ce


def binary_cross_entropy_loss(pred, target):
    """
    二元交叉熵损失 (Binary Cross Entropy)

    BCE = -[target * log(pred) + (1-target) * log(1-pred)]

    pred 应该是经过 sigmoid 的概率值
    """
    eps = 1e-7  # 防止 log(0)

    # TODO: 计算 BCE
    bce = -(target * torch.log(pred + eps) +
            (1 - ___) * torch.log(1 - pred + eps))  # 填入 target

    return bce.mean()


def bce_with_logits_loss(logits, target):
    """
    带 Logits 的 BCE（数值更稳定）

    使用 log-sum-exp 技巧
    """
    # TODO: 计算带 logits 的 BCE
    # max(logits, 0) - logits * target + log(1 + exp(-|logits|))
    bce = torch.clamp(logits, min=0) - logits * target + torch.log(
        1 + torch.exp(-torch.___(logits))  # 使用 abs
    )

    return bce.mean()


def kl_divergence(p, q):
    """
    KL 散度 (Kullback-Leibler Divergence)

    KL(P||Q) = Σ P(x) * log(P(x) / Q(x))

    衡量两个概率分布的差异
    P: 真实分布
    Q: 近似分布
    """
    eps = 1e-7

    # TODO: 计算 KL 散度
    kl = (p * torch.log((p + eps) / (___ + eps))).sum(dim=-1)  # 填入 q

    return kl.mean()


def focal_loss(logits, targets, gamma=2.0, alpha=0.25):
    """
    Focal Loss (用于类别不平衡)

    FL = -α * (1-p)^γ * log(p)

    γ (gamma): 聚焦参数，降低易分类样本的权重
    α (alpha): 类别权重
    """
    probs = F.softmax(logits, dim=-1)
    batch_size = logits.shape[0]

    # 获取正确类别的概率
    p = probs[torch.arange(batch_size), targets]

    # TODO: 计算 focal loss
    # FL = -α * (1-p)^γ * log(p)
    focal_weight = (1 - p) ** ___  # 填入 gamma
    fl = -alpha * focal_weight * torch.log(p + 1e-7)

    return fl.mean()


def smooth_l1_loss(pred, target, beta=1.0):
    """
    Smooth L1 Loss (Huber Loss)

    当误差较小时用 L2，较大时用 L1
    避免 L2 对异常值过于敏感

    loss = 0.5 * x^2 / beta,  if |x| < beta
    loss = |x| - 0.5 * beta,  otherwise
    """
    diff = pred - target
    abs_diff = torch.abs(diff)

    # TODO: 计算 smooth L1
    loss = torch.where(
        abs_diff < beta,
        0.5 * diff ** 2 / ___,  # 填入 beta
        abs_diff - 0.5 * beta
    )

    return loss.mean()


def contrastive_loss(anchor, positive, negative, margin=1.0):
    """
    对比损失 (用于相似度学习)

    loss = max(0, margin - ||anchor - negative|| + ||anchor - positive||)

    让正样本靠近，负样本远离
    """
    # 计算距离
    pos_dist = torch.norm(anchor - positive, dim=-1)
    neg_dist = torch.norm(anchor - negative, dim=-1)

    # TODO: 计算对比损失
    loss = torch.clamp(margin - neg_dist + ___, min=0)  # 填入 pos_dist

    return loss.mean()


def main():
    torch.manual_seed(42)

    print("测试 MSE Loss...")
    pred = torch.tensor([1.0, 2.0, 3.0])
    target = torch.tensor([1.5, 2.5, 3.5])
    mse = mse_loss(pred, target)
    expected_mse = F.mse_loss(pred, target)
    assert torch.allclose(mse, expected_mse)
    print(f"✓ MSE = {mse:.4f}")

    print("\n测试 MAE Loss...")
    mae = mae_loss(pred, target)
    expected_mae = F.l1_loss(pred, target)
    assert torch.allclose(mae, expected_mae)
    print(f"✓ MAE = {mae:.4f}")

    print("\n测试 Cross Entropy Loss...")
    logits = torch.randn(4, 10)
    targets = torch.randint(0, 10, (4,))
    ce = cross_entropy_loss(logits, targets)
    expected_ce = F.cross_entropy(logits, targets)
    assert torch.allclose(ce, expected_ce, atol=1e-5)
    print(f"✓ CE = {ce:.4f}")

    print("\n测试 Binary Cross Entropy Loss...")
    pred_probs = torch.sigmoid(torch.randn(10))
    binary_targets = torch.randint(0, 2, (10,)).float()
    bce = binary_cross_entropy_loss(pred_probs, binary_targets)
    expected_bce = F.binary_cross_entropy(pred_probs, binary_targets)
    assert torch.allclose(bce, expected_bce, atol=1e-5)
    print(f"✓ BCE = {bce:.4f}")

    print("\n测试 BCE with Logits...")
    logits_binary = torch.randn(10)
    bce_logits = bce_with_logits_loss(logits_binary, binary_targets)
    expected_bce_logits = F.binary_cross_entropy_with_logits(logits_binary, binary_targets)
    assert torch.allclose(bce_logits, expected_bce_logits, atol=1e-5)
    print(f"✓ BCE Logits = {bce_logits:.4f}")

    print("\n测试 KL Divergence...")
    p = F.softmax(torch.randn(4, 10), dim=-1)
    q = F.softmax(torch.randn(4, 10), dim=-1)
    kl = kl_divergence(p, q)
    expected_kl = F.kl_div(q.log(), p, reduction='batchmean')
    print(f"✓ KL = {kl:.4f}")

    print("\n测试 Focal Loss...")
    fl = focal_loss(logits, targets)
    print(f"✓ Focal Loss = {fl:.4f}")

    print("\n测试 Smooth L1 Loss...")
    sl1 = smooth_l1_loss(pred, target)
    expected_sl1 = F.smooth_l1_loss(pred, target)
    assert torch.allclose(sl1, expected_sl1, atol=1e-5)
    print(f"✓ Smooth L1 = {sl1:.4f}")

    print("\n测试 Contrastive Loss...")
    anchor = torch.randn(4, 128)
    positive = anchor + 0.1 * torch.randn(4, 128)  # 相似
    negative = torch.randn(4, 128)  # 不相似
    cl = contrastive_loss(anchor, positive, negative)
    print(f"✓ Contrastive Loss = {cl:.4f}")

    print("\n🎉 所有测试通过！损失函数掌握完成！")


if __name__ == "__main__":
    main()
