"""
练习 27: 量子生成对抗网络 (QGAN)
==================

目标：实现量子版本的 GAN

知识点：
- QGAN 将经典 GAN 的概念扩展到量子领域
- 组件：
  * Generator（生成器）：参数化量子电路
  * Discriminator（判别器）：可以是量子或经典
- 应用：
  * 生成量子态
  * 量子数据增强
  * 学习量子系统

前沿进展（2023-2025）：
- 混合量子-经典 GAN
- 用于量子数据的生成模型
- 量子优势的新方向

任务：实现简化的 QGAN
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, state_fidelity
import numpy as np
from scipy.optimize import minimize


def create_generator(params, n_qubits=2):
    """
    创建生成器电路

    目标：生成特定的量子态分布

    参数：
        params: 生成器参数
        n_qubits: 量子比特数

    返回：
        QuantumCircuit: 生成器电路
    """
    qc = QuantumCircuit(n_qubits)

    # TODO: 实现参数化生成器
    # 使用旋转门和纠缠门
    # 例如：
    # qc.ry(params[0], 0)
    # qc.ry(params[1], 1)
    # qc.cx(0, 1)
    # qc.ry(params[2], 0)
    # qc.ry(params[3], 1)

    return qc


def create_target_state(n_qubits=2):
    """
    创建目标量子态（"真实数据"）

    这里我们使用贝尔态作为目标

    参数：
        n_qubits: 量子比特数

    返回：
        Statevector: 目标态
    """
    qc = QuantumCircuit(n_qubits)

    # 创建贝尔态 |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc.h(0)
    qc.cx(0, 1)

    target = Statevector.from_instruction(qc)

    return target


def discriminator_loss(generated_state, target_state):
    """
    计算判别器损失

    使用保真度（Fidelity）作为度量
    保真度越高，生成的态越接近目标态

    参数：
        generated_state: 生成的量子态
        target_state: 目标态

    返回：
        float: 损失值（1 - 保真度）
    """
    fidelity = state_fidelity(generated_state, target_state)

    # 损失 = 1 - 保真度（最小化损失 = 最大化保真度）
    loss = 1 - fidelity

    return loss


def generator_objective(params, target_state, n_qubits):
    """
    生成器目标函数

    参数：
        params: 生成器参数
        target_state: 目标态
        n_qubits: 量子比特数

    返回：
        float: 损失值
    """
    # TODO: 创建生成器并生成态
    gen_circuit = create_generator(params, n_qubits)
    generated_state = Statevector.from_instruction(gen_circuit)

    # TODO: 计算损失
    loss = discriminator_loss(generated_state, target_state)

    return loss


def train_qgan(n_qubits=2, n_params=4, max_iter=100):
    """
    训练 QGAN

    参数：
        n_qubits: 量子比特数
        n_params: 参数数量
        max_iter: 最大迭代次数

    返回：
        dict: 训练结果
    """
    print("开始训练 QGAN...")
    print(f"量子比特数: {n_qubits}")
    print(f"参数数量: {n_params}\n")

    # 创建目标态
    target_state = create_target_state(n_qubits)
    print(f"目标态（贝尔态）: {target_state.data}\n")

    # 初始化生成器参数
    initial_params = np.random.rand(n_params) * 2 * np.pi

    # TODO: 训练生成器
    result = minimize(
        generator_objective,
        initial_params,
        args=(target_state, n_qubits),
        method='COBYLA',
        options={'maxiter': max_iter}
    )

    print(f"训练完成！")
    print(f"迭代次数: {result.nfev}")
    print(f"最终损失: {result.fun:.6f}")
    print(f"最终保真度: {1 - result.fun:.6f}")

    # 生成最终态
    final_circuit = create_generator(result.x, n_qubits)
    final_state = Statevector.from_instruction(final_circuit)

    print(f"\n生成的态: {final_state.data}")
    print(f"目标态:   {target_state.data}")

    return {
        'params': result.x,
        'loss': result.fun,
        'fidelity': 1 - result.fun,
        'generated_state': final_state,
        'target_state': target_state
    }


def test_qgan():
    """测试 QGAN"""
    print("测试量子生成对抗网络\n")
    print("=" * 60)

    result = train_qgan(n_qubits=2, n_params=4, max_iter=100)

    # 验证：保真度应该接近 1
    assert result['fidelity'] > 0.95, \
        f"保真度应该 > 0.95，实际: {result['fidelity']:.4f}"

    print("\n✓ QGAN 训练成功！")
    print(f"  生成器成功学习了目标量子态")

    return True


def explain_qgan():
    """解释 QGAN"""
    print("\n" + "=" * 60)
    print("量子生成对抗网络（QGAN）")
    print("=" * 60)

    print("""
经典 GAN vs 量子 GAN：

经典 GAN：
  - 生成器：神经网络
  - 判别器：神经网络
  - 数据：经典数据（图像、文本等）

量子 GAN：
  - 生成器：参数化量子电路
  - 判别器：量子或经典
  - 数据：量子态

QGAN 的优势：
  ✓ 可以生成难以经典描述的量子态
  ✓ 潜在的量子优势
  ✓ 用于量子机器学习

应用场景：
  1. 量子态学习
     - 学习未知量子过程产生的态
     - 量子系统建模

  2. 量子数据增强
     - 生成训练用的量子数据
     - 提高量子机器学习性能

  3. 量子化学
     - 生成分子的量子态
     - 加速量子模拟

前沿研究（2024-2025）：
  🔬 混合 QGAN：结合量子和经典组件
  🔬 纠缠 GAN：利用纠缠提升性能
  🔬 QGAN 用于量子误差缓解
  🔬 可证明的量子优势

挑战：
  ⚠ 训练稳定性
  ⚠ 梯度消失问题
  ⚠ 需要大量量子资源

这是量子机器学习最前沿的方向之一！
    """)


if __name__ == '__main__':
    try:
        test_qgan()
        explain_qgan()

        print("\n🎉 恭喜！你已进入量子机器学习前沿！")
        print("\n关键要点:")
        print("- QGAN 是量子+AI的结合")
        print("- 可以生成复杂的量子态")
        print("- 2024-2025年的研究热点")
        print("- 潜在的量子优势应用")
        print("\n你已经站在量子计算研究的最前沿！")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
