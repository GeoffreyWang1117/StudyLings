"""
练习 20: 采样策略 (Sampling Strategies)

采样策略决定了文本生成的多样性和质量。
不同的策略适用于不同的场景。

常用策略：
1. Greedy: 总是选择概率最高的 token（确定性）
2. Temperature: 调整概率分布的锐度
3. Top-k: 只从概率最高的 k 个 token 中采样
4. Top-p (Nucleus): 从累积概率达到 p 的最小集合中采样

在这个练习中，你将学习：
- 各种采样策略的实现
- 不同策略的效果对比
- 如何组合使用不同策略
"""

import torch
import torch.nn.functional as F


def greedy_sampling(logits):
    """
    贪婪采样：选择概率最高的 token

    Args:
        logits: 模型输出，形状 (batch_size, vocab_size)

    Returns:
        选中的 token ID，形状 (batch_size,)
    """
    # TODO: 返回概率最高的 token
    return logits.___(dim=-1)  # 使用 argmax


def temperature_sampling(logits, temperature=1.0):
    """
    温度采样：通过温度参数调整分布

    temperature < 1: 分布更尖锐，更确定性
    temperature = 1: 原始分布
    temperature > 1: 分布更平坦，更随机

    Args:
        logits: (batch_size, vocab_size)
        temperature: 温度参数

    Returns:
        采样的 token ID
    """
    # TODO: 用温度缩放 logits
    scaled_logits = logits / ___  # 填入 temperature

    # TODO: 计算概率分布
    probs = F.___(scaled_logits, dim=-1)  # 使用 softmax

    # TODO: 从分布中采样
    return torch.___(probs, num_samples=1).squeeze(-1)  # 使用 multinomial


def top_k_sampling(logits, k=50, temperature=1.0):
    """
    Top-k 采样：只从概率最高的 k 个 token 中采样

    Args:
        logits: (batch_size, vocab_size)
        k: 保留的 token 数量
        temperature: 温度参数

    Returns:
        采样的 token ID
    """
    # 温度缩放
    logits = logits / temperature

    # TODO: 获取 top-k 的值和索引
    top_k_values, top_k_indices = torch.___(logits, k=k, dim=-1)  # 使用 topk

    # 对 top-k 的值计算概率
    probs = F.softmax(top_k_values, dim=-1)

    # TODO: 从 top-k 中采样
    sampled_indices = torch.multinomial(probs, num_samples=1)

    # 映射回原始词表索引
    # TODO: 使用 gather 获取实际的 token ID
    token_ids = top_k_indices.___(dim=-1, index=sampled_indices)  # 使用 gather

    return token_ids.squeeze(-1)


def top_p_sampling(logits, p=0.9, temperature=1.0):
    """
    Top-p (Nucleus) 采样：从累积概率达到 p 的最小集合中采样

    相比 Top-k，Top-p 更自适应：
    - 当分布尖锐时，只保留少数 token
    - 当分布平坦时，保留更多 token

    Args:
        logits: (batch_size, vocab_size)
        p: 累积概率阈值
        temperature: 温度参数

    Returns:
        采样的 token ID
    """
    # 温度缩放
    logits = logits / temperature

    # 对 logits 排序
    sorted_logits, sorted_indices = torch.sort(logits, dim=-1, descending=True)
    sorted_probs = F.softmax(sorted_logits, dim=-1)

    # TODO: 计算累积概率
    cumulative_probs = torch.___(sorted_probs, dim=-1)  # 使用 cumsum

    # TODO: 找到累积概率超过 p 的位置
    # 创建掩码：True 表示该位置的累积概率已超过 p（应被移除）
    sorted_indices_to_remove = cumulative_probs ___ p  # 填入比较运算符（>）

    # 保留第一个超过阈值的 token（否则可能什么都不剩）
    sorted_indices_to_remove[..., 0] = False

    # 将要移除的位置设为负无穷
    sorted_logits = sorted_logits.masked_fill(sorted_indices_to_remove, float('-inf'))

    # 重新计算概率
    probs = F.softmax(sorted_logits, dim=-1)

    # 采样
    sampled_indices = torch.multinomial(probs, num_samples=1)

    # 映射回原始索引
    token_ids = sorted_indices.gather(dim=-1, index=sampled_indices)

    return token_ids.squeeze(-1)


def combined_sampling(logits, temperature=1.0, top_k=50, top_p=0.9):
    """
    组合采样：结合温度、top-k 和 top-p

    Args:
        logits: (batch_size, vocab_size)
        temperature: 温度参数
        top_k: Top-k 值（设为 0 禁用）
        top_p: Top-p 值（设为 1.0 禁用）

    Returns:
        采样的 token ID
    """
    # TODO: 温度缩放
    logits = logits / ___  # 填入 temperature

    # 应用 Top-k
    if top_k > 0:
        # 只保留 top-k，其他设为负无穷
        top_k_values, _ = torch.topk(logits, k=top_k, dim=-1)
        min_top_k = top_k_values[..., -1, None]  # 第 k 大的值
        logits = logits.masked_fill(logits < min_top_k, float('-inf'))

    # 应用 Top-p
    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, dim=-1, descending=True)
        sorted_probs = F.softmax(sorted_logits, dim=-1)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

        # 移除累积概率超过 p 的 token
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 0] = False

        # 将移除的索引映射回原始顺序
        indices_to_remove = sorted_indices_to_remove.scatter(
            dim=-1, index=sorted_indices, src=sorted_indices_to_remove
        )
        logits = logits.masked_fill(indices_to_remove, float('-inf'))

    # TODO: 计算概率并采样
    probs = F.softmax(logits, dim=-1)
    return torch.___(probs, num_samples=1).squeeze(-1)  # 使用 multinomial


def repetition_penalty(logits, generated_tokens, penalty=1.2):
    """
    重复惩罚：降低已生成 token 的概率

    Args:
        logits: 当前 logits
        generated_tokens: 已生成的 token 列表
        penalty: 惩罚因子（> 1 减少重复，< 1 增加重复）

    Returns:
        修改后的 logits
    """
    # TODO: 对已生成的 token 应用惩罚
    for token in generated_tokens:
        if logits[0, token] > 0:
            logits[0, token] = logits[0, token] / ___  # 填入 penalty
        else:
            logits[0, token] = logits[0, token] * ___  # 填入 penalty

    return logits


def main():
    # 创建测试 logits
    vocab_size = 100
    logits = torch.randn(1, vocab_size)

    print("测试 greedy_sampling...")
    token = greedy_sampling(logits)
    assert token == logits.argmax(dim=-1)
    print("✓ greedy_sampling 通过!")

    print("\n测试 temperature_sampling...")
    # 低温度应该更接近 greedy
    samples_low_temp = [temperature_sampling(logits.clone(), temperature=0.1).item()
                        for _ in range(100)]
    most_common = max(set(samples_low_temp), key=samples_low_temp.count)
    assert most_common == logits.argmax().item()
    print("✓ temperature_sampling 通过!")

    print("\n测试 top_k_sampling...")
    token = top_k_sampling(logits, k=10)
    # 结果应该在 top-10 中
    top_10 = torch.topk(logits, k=10, dim=-1).indices[0]
    assert token.item() in top_10.tolist()
    print("✓ top_k_sampling 通过!")

    print("\n测试 top_p_sampling...")
    token = top_p_sampling(logits, p=0.9)
    assert 0 <= token.item() < vocab_size
    print("✓ top_p_sampling 通过!")

    print("\n测试 combined_sampling...")
    token = combined_sampling(logits, temperature=0.8, top_k=50, top_p=0.9)
    assert 0 <= token.item() < vocab_size
    print("✓ combined_sampling 通过!")

    print("\n测试不同温度的效果...")
    print("  (采样 1000 次，统计 top-1 token 出现的比例)")
    for temp in [0.1, 0.5, 1.0, 2.0]:
        samples = [temperature_sampling(logits.clone(), temperature=temp).item()
                   for _ in range(1000)]
        top_token = logits.argmax().item()
        top_ratio = samples.count(top_token) / 1000
        print(f"  温度 {temp}: top-1 出现比例 {top_ratio:.1%}")

    print("\n测试 repetition_penalty...")
    logits_test = torch.tensor([[1.0, 2.0, 3.0, 4.0, 5.0]])
    generated = [4, 3]  # 已生成的 token
    penalized = repetition_penalty(logits_test.clone(), generated, penalty=1.5)
    # 已生成的 token 的 logits 应该变小
    assert penalized[0, 4] < logits_test[0, 4]
    assert penalized[0, 3] < logits_test[0, 3]
    print("✓ repetition_penalty 通过!")

    print("\n🎉 所有测试通过！采样策略掌握完成！")


if __name__ == "__main__":
    main()
