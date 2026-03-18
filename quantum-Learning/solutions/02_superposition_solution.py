"""
练习 02 参考答案：量子叠加态
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer


def create_superposition():
    """
    创建一个处于叠加态的量子比特
    """
    qc = QuantumCircuit(1, 1)

    # 应用 Hadamard 门创建叠加态
    qc.h(0)

    # 添加测量
    qc.measure(0, 0)

    return qc


# 测试
if __name__ == '__main__':
    qc = create_superposition()
    print("电路图:")
    print(qc.draw(output='text'))

    # 运行并查看结果
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts()

    print(f"\n测量结果: {counts}")
    print("叠加态创建成功！")
