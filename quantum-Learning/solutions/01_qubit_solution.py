"""
练习 01 参考答案：量子比特基础
"""

from qiskit import QuantumCircuit


def create_single_qubit_circuit():
    """
    创建一个单量子比特电路
    """
    # 创建一个包含 1 个量子比特的量子电路
    qc = QuantumCircuit(1)
    return qc


# 测试
if __name__ == '__main__':
    qc = create_single_qubit_circuit()
    print("电路创建成功！")
    print(f"量子比特数量: {qc.num_qubits}")
    print("\n电路图:")
    print(qc.draw(output='text'))
