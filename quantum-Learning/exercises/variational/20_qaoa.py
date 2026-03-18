"""
练习 20: QAOA (量子近似优化算法)
==================

目标：实现 QAOA 解决组合优化问题

知识点：
- QAOA 由 Farhi 等人于 2014 年提出
- 用于解决组合优化问题
- 特别适合 NISQ 设备

经典问题：MaxCut
- 给定图 G = (V, E)
- 将节点分成两组，最大化跨组的边数

QAOA 方法：
- 交替应用问题哈密顿量和混合哈密顿量
- 参数 (β, γ) 通过经典优化器调整

任务：使用 QAOA 解决 MaxCut 问题
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np
from scipy.optimize import minimize
import networkx as nx


def create_maxcut_hamiltonian(graph):
    """
    为 MaxCut 问题创建哈密顿量

    H = Σ_{(i,j) ∈ E} (1 - Z_i Z_j) / 2

    参数：
        graph: NetworkX 图

    返回：
        list: [(edge, weight), ...]
    """
    hamiltonian = []
    for edge in graph.edges():
        hamiltonian.append((edge, 1.0))
    return hamiltonian


def apply_problem_unitary(qc, gamma, hamiltonian):
    """
    应用问题酉算子 U(C, γ)

    对于 MaxCut: U(C, γ) = exp(-i γ H_C)
    其中 H_C = Σ (1 - Z_i Z_j) / 2

    参数：
        qc: 量子电路
        gamma: 参数 γ
        hamiltonian: 哈密顿量
    """
    # TODO: 实现问题酉算子
    # 对于每条边 (i, j)，应用 exp(-i γ/2 (1 - Z_i Z_j))
    # 这等价于: RZ(-γ) on both qubits + CNOT + RZ(γ) + CNOT

    for edge, weight in hamiltonian:
        i, j = edge
        # TODO: 实现 ZZ 交互
        # qc.cx(i, j)
        # qc.rz(2 * gamma * weight, j)
        # qc.cx(i, j)
        pass


def apply_mixer_unitary(qc, beta):
    """
    应用混合酉算子 U(B, β)

    U(B, β) = exp(-i β H_B)
    其中 H_B = Σ X_i

    参数：
        qc: 量子电路
        beta: 参数 β
    """
    # TODO: 实现混合酉算子
    # 对所有量子比特应用 RX(2β)

    for i in range(qc.num_qubits):
        # TODO: qc.rx(2 * beta, i)
        pass


def create_qaoa_circuit(graph, params, p=1):
    """
    创建 QAOA 电路

    参数：
        graph: 问题图
        params: 参数 [γ_1, β_1, γ_2, β_2, ..., γ_p, β_p]
        p: QAOA 层数

    返回：
        QuantumCircuit
    """
    n_qubits = len(graph.nodes())
    qc = QuantumCircuit(n_qubits)

    # 初始化：均匀叠加态
    qc.h(range(n_qubits))

    # QAOA 层
    hamiltonian = create_maxcut_hamiltonian(graph)

    for layer in range(p):
        gamma = params[2 * layer]
        beta = params[2 * layer + 1]

        # 问题酉算子
        apply_problem_unitary(qc, gamma, hamiltonian)

        # 混合酉算子
        apply_mixer_unitary(qc, beta)

    return qc


def compute_maxcut_cost(bitstring, graph):
    """
    计算 MaxCut 代价函数

    参数：
        bitstring: 比特串（如 "0110"）
        graph: 图

    返回：
        int: cut 值（跨组的边数）
    """
    cut = 0
    for edge in graph.edges():
        i, j = edge
        if bitstring[i] != bitstring[j]:
            cut += 1
    return cut


def qaoa_objective(params, graph, p):
    """
    QAOA 目标函数

    参数：
        params: QAOA 参数
        graph: 问题图
        p: 层数

    返回：
        float: 期望代价（负的，因为我们要最小化）
    """
    qc = create_qaoa_circuit(graph, params, p)
    qc.measure_all()

    # 运行电路
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts()

    # 计算期望 cut 值
    total_cost = 0
    for bitstring, count in counts.items():
        # Qiskit 的比特顺序是反的
        bitstring = bitstring[::-1]
        cost = compute_maxcut_cost(bitstring, graph)
        total_cost += cost * count

    avg_cost = total_cost / 1000

    # 返回负值（因为我们要最大化 cut，但优化器最小化）
    return -avg_cost


def run_qaoa(graph, p=1):
    """
    运行 QAOA 算法

    参数：
        graph: 要解决的图
        p: QAOA 深度

    返回：
        dict: 结果
    """
    print(f"运行 QAOA (p={p}) 解决 MaxCut...")
    print(f"图: {len(graph.nodes())} 个节点, {len(graph.edges())} 条边\n")

    # 初始化参数
    initial_params = np.random.rand(2 * p) * 2 * np.pi

    # 优化
    result = minimize(
        qaoa_objective,
        initial_params,
        args=(graph, p),
        method='COBYLA',
        options={'maxiter': 100}
    )

    print(f"优化完成！")
    print(f"最优 cut 值: {-result.fun:.2f}")

    # 找到最佳比特串
    qc = create_qaoa_circuit(graph, result.x, p)
    qc.measure_all()

    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts()

    best_bitstring = max(counts.items(), key=lambda x: x[1])[0][::-1]
    best_cut = compute_maxcut_cost(best_bitstring, graph)

    print(f"最佳比特串: {best_bitstring}")
    print(f"Cut 值: {best_cut}")

    return {
        'cut_value': best_cut,
        'bitstring': best_bitstring,
        'params': result.x
    }


def test_qaoa():
    """测试 QAOA"""
    print("测试 QAOA 算法\n")
    print("=" * 60)

    # 创建测试图
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])

    # 运行 QAOA
    result = run_qaoa(G, p=1)

    # 验证（4 个节点的环，最优 cut = 4）
    print(f"\n对于 4-节点环图，理论最优 cut = 4")
    print(f"QAOA 找到的 cut = {result['cut_value']}")

    assert result['cut_value'] >= 3, "QAOA 应该找到接近最优的解"

    print("\n✓ QAOA 成功！")

    return True


def explain_qaoa():
    """解释 QAOA"""
    print("\n" + "=" * 60)
    print("QAOA 算法详解")
    print("=" * 60)

    print("""
QAOA 的核心思想：

  经典退火 vs 量子退火 vs QAOA：

    经典退火：
      - 逐步降低温度
      - 可能困在局部最优

    量子退火：
      - 利用量子隧穿
      - 需要专用硬件（D-Wave）

    QAOA：
      - 离散门操作
      - 可在通用量子计算机上运行
      - 结合了量子和经典

算法流程：

  1. 初始化：|s⟩ = |+⟩^⊗n

  2. p 层迭代：
     对于 ℓ = 1 to p:
       - 应用 U(C, γ_ℓ) = exp(-i γ_ℓ H_C)
       - 应用 U(B, β_ℓ) = exp(-i β_ℓ H_B)

  3. 测量并计算代价

  4. 经典优化器更新 (γ, β)

  5. 重复直到收敛

为什么有效？

  绝热演化的离散化：
    - 从易解问题 H_B 开始
    - 慢慢演化到难问题 H_C
    - QAOA 是离散的近似版本

  p → ∞：QAOA → 绝热算法
  p = 1：启发式，但在 NISQ 上可行

应用：

  ✓ MaxCut
  ✓ 图着色
  ✓ 旅行商问题（TSP）
  ✓ 投资组合优化
  ✓ 车辆路径问题

性能：

  理论：
    - p=1: 期望近似比 > 0.6924
    - p → ∞: 可达最优解

  实践：
    - 小问题（n < 20）：接近最优
    - 大问题：启发式，但有希望

挑战（2024-2025）：

  ⚠ 最优参数难找
  ⚠ 需要大量测量
  ⚠ 贫瘠高原问题
  ⚠ 与经典算法竞争

前沿方向：

  🔬 递归 QAOA（RQAOA）
  🔬 自适应参数
  🔬 暖启动（Warm-start QAOA）
  🔬 多角度QAOA（ma-QAOA）

实际应用案例：

  - JPMorgan Chase: 投资组合优化
  - Volkswagen: 交通流优化
  - Airbus: 飞机装载优化

QAOA 是 NISQ 时代最有前景的算法之一！
    """)


if __name__ == '__main__':
    try:
        test_qaoa()
        explain_qaoa()

        print("\n🎉 恭喜！你已掌握 QAOA！")
        print("\n关键要点:")
        print("- QAOA 适合 NISQ 设备")
        print("- 解决组合优化问题")
        print("- 量子+经典混合算法")
        print("- 有实际商业应用")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
