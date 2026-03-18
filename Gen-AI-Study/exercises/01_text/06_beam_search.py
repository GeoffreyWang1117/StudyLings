"""
练习 11: 束搜索 (Beam Search)

束搜索是序列生成中常用的解码策略，
在贪婪搜索和穷举搜索之间取得平衡。

核心思想：
- 保留 beam_size 个最佳候选序列
- 每步扩展所有候选，选择最佳的 beam_size 个
- 避免贪婪搜索的局部最优

在这个练习中，你将学习：
- 束搜索算法
- 长度归一化
- 多样性解码
"""

import torch
import torch.nn.functional as F
from dataclasses import dataclass
from typing import List


@dataclass
class BeamHypothesis:
    """束搜索假设"""
    tokens: List[int]  # token 序列
    score: float       # 累积 log 概率


def greedy_decode(model_output_fn, max_len, sos_idx, eos_idx):
    """
    贪婪解码 (对比用)

    每步选择概率最高的 token
    """
    tokens = [sos_idx]
    hidden = None

    for _ in range(max_len):
        logits, hidden = model_output_fn(tokens[-1], hidden)
        probs = F.softmax(logits, dim=-1)

        # TODO: 选择概率最高的 token
        next_token = probs.argmax(dim=-1).item()

        tokens.append(next_token)

        if next_token == eos_idx:
            break

    return tokens


def beam_search(model_output_fn, beam_size, max_len, sos_idx, eos_idx, length_penalty=0.6):
    """
    束搜索解码

    Args:
        model_output_fn: 模型输出函数 (token, hidden) -> (logits, new_hidden)
        beam_size: 束宽度
        max_len: 最大长度
        sos_idx: 起始 token
        eos_idx: 结束 token
        length_penalty: 长度惩罚因子 (α in score / len^α)

    Returns:
        best_sequence: 最佳序列
    """
    # 初始化
    hypotheses = [BeamHypothesis(tokens=[sos_idx], score=0.0)]
    completed = []

    hidden_states = {0: None}  # 每个假设的隐藏状态

    for step in range(max_len):
        all_candidates = []

        for idx, hyp in enumerate(hypotheses):
            if hyp.tokens[-1] == eos_idx:
                completed.append(hyp)
                continue

            # 获取模型输出
            last_token = hyp.tokens[-1]
            hidden = hidden_states.get(idx)
            logits, new_hidden = model_output_fn(last_token, hidden)

            # TODO: 计算 log 概率
            log_probs = F.log_softmax(logits, dim=___)  # 填入 -1

            # 获取 top-k 候选
            top_k_log_probs, top_k_indices = torch.topk(log_probs, beam_size)

            for i in range(beam_size):
                new_token = top_k_indices[i].item()
                new_log_prob = top_k_log_probs[i].item()

                # TODO: 计算新的累积分数
                new_score = hyp.score + ___  # 填入 new_log_prob

                new_hyp = BeamHypothesis(
                    tokens=hyp.tokens + [new_token],
                    score=new_score
                )

                all_candidates.append((new_hyp, new_hidden))

        if not all_candidates:
            break

        # TODO: 按分数排序，保留 top beam_size
        all_candidates.sort(key=lambda x: -x[0].score)
        hypotheses = []
        hidden_states = {}

        for i, (hyp, hidden) in enumerate(all_candidates[:beam_size]):
            hypotheses.append(hyp)
            hidden_states[i] = ___  # 填入 hidden

    # 添加未完成的假设
    completed.extend(hypotheses)

    # 长度归一化
    def normalized_score(hyp):
        length = len(hyp.tokens)
        # TODO: 长度归一化分数
        return hyp.score / (length ** ___)  # 填入 length_penalty

    # 选择最佳
    best = max(completed, key=normalized_score)
    return best.tokens


def diverse_beam_search(model_output_fn, beam_size, num_groups, max_len, sos_idx, eos_idx, diversity_penalty=0.5):
    """
    多样性束搜索

    将束分成多个组，组间添加多样性惩罚
    """
    group_size = beam_size // num_groups

    all_results = []

    for g in range(num_groups):
        # 每组独立运行束搜索，但惩罚之前组已选择的 token
        selected_tokens = set()

        hypotheses = [BeamHypothesis(tokens=[sos_idx], score=0.0)]
        hidden_states = {0: None}

        for step in range(max_len):
            all_candidates = []

            for idx, hyp in enumerate(hypotheses):
                if hyp.tokens[-1] == eos_idx:
                    all_results.append(hyp)
                    continue

                last_token = hyp.tokens[-1]
                hidden = hidden_states.get(idx)
                logits, new_hidden = model_output_fn(last_token, hidden)

                log_probs = F.log_softmax(logits, dim=-1)

                # 对之前组选过的 token 添加惩罚
                for prev_token in selected_tokens:
                    if prev_token < log_probs.shape[0]:
                        log_probs[prev_token] -= diversity_penalty

                top_k_log_probs, top_k_indices = torch.topk(log_probs, group_size)

                for i in range(group_size):
                    new_token = top_k_indices[i].item()
                    new_log_prob = top_k_log_probs[i].item()
                    new_score = hyp.score + new_log_prob

                    new_hyp = BeamHypothesis(
                        tokens=hyp.tokens + [new_token],
                        score=new_score
                    )
                    all_candidates.append((new_hyp, new_hidden))

            if not all_candidates:
                break

            all_candidates.sort(key=lambda x: -x[0].score)
            hypotheses = []
            hidden_states = {}

            for i, (hyp, hidden) in enumerate(all_candidates[:group_size]):
                hypotheses.append(hyp)
                hidden_states[i] = hidden
                # 记录这个组选择的 token
                selected_tokens.add(hyp.tokens[-1])

        all_results.extend(hypotheses)

    return all_results


def sample_with_temperature(logits, temperature=1.0, top_k=0, top_p=0.0):
    """
    带温度的采样 (用于对比)

    Args:
        logits: 模型输出
        temperature: 温度参数 (越高越随机)
        top_k: 只从概率最高的 k 个中采样
        top_p: nucleus sampling 阈值
    """
    # 温度缩放
    logits = logits / temperature

    # Top-K 过滤
    if top_k > 0:
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = float('-inf')

    # Top-P (Nucleus) 过滤
    if top_p > 0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices_to_remove.scatter(0, sorted_indices, sorted_indices_to_remove)
        logits[indices_to_remove] = float('-inf')

    # 采样
    probs = F.softmax(logits, dim=-1)
    return torch.multinomial(probs, num_samples=1)


def main():
    torch.manual_seed(42)
    vocab_size = 100

    # 模拟语言模型
    class DummyLM:
        def __init__(self):
            self.hidden_size = 64

        def __call__(self, token, hidden):
            if hidden is None:
                hidden = torch.zeros(self.hidden_size)
            # 模拟下一个 token 的 logits
            logits = torch.randn(vocab_size)
            # 让某些 token 概率更高
            logits[token + 1 if token < vocab_size - 1 else 0] += 2
            hidden = hidden + torch.randn(self.hidden_size) * 0.1
            return logits, hidden

    lm = DummyLM()

    print("测试贪婪解码...")
    greedy_result = greedy_decode(lm, max_len=10, sos_idx=0, eos_idx=99)
    print(f"✓ 贪婪解码结果: {greedy_result[:10]}...")

    print("\n测试束搜索...")
    beam_result = beam_search(lm, beam_size=4, max_len=10, sos_idx=0, eos_idx=99)
    print(f"✓ 束搜索结果: {beam_result[:10]}...")

    print("\n测试多样性束搜索...")
    diverse_results = diverse_beam_search(
        lm, beam_size=8, num_groups=4, max_len=10, sos_idx=0, eos_idx=99
    )
    print(f"✓ 生成了 {len(diverse_results)} 个多样化序列")

    print("\n测试温度采样...")
    logits = torch.randn(vocab_size)

    print("  不同温度的采样结果:")
    for temp in [0.1, 0.5, 1.0, 2.0]:
        samples = [sample_with_temperature(logits.clone(), temperature=temp).item() for _ in range(5)]
        print(f"    T={temp}: {samples}")

    print("\n测试 Top-K 采样...")
    for k in [1, 5, 20]:
        samples = [sample_with_temperature(logits.clone(), top_k=k).item() for _ in range(5)]
        print(f"    K={k}: {samples}")

    print("\n测试 Top-P 采样...")
    for p in [0.1, 0.5, 0.9]:
        samples = [sample_with_temperature(logits.clone(), top_p=p).item() for _ in range(5)]
        print(f"    P={p}: {samples}")

    print("\n🎉 所有测试通过！束搜索掌握完成！")


if __name__ == "__main__":
    main()
