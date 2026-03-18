"""
练习 07: 量子隐形传态
==================

目标：实现量子隐形传态协议

知识点：
- 量子隐形传态是利用纠缠和经典通信来传输量子态
- 不违反相对论（需要经典通信，不能超光速）
- 不违反量子不可克隆定理（原态被破坏）

协议步骤：
1. Alice 和 Bob 共享一个贝尔对
2. Alice 对她的量子比特和待传输的量子比特进行贝尔测量
3. Alice 将测量结果（2个经典比特）发送给 Bob
4. Bob 根据 Alice 的测量结果应用相应的纠正操作

应用：
- 量子网络
- 量子中继
- 分布式量子计算

任务：实现完整的量子隐形传态电路
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, state_fidelity
import numpy as np


def create_teleportation_circuit(input_state='0'):
    """
    创建量子隐形传态电路

    参数：
        input_state: 要传输的量子态 ('0', '1', '+', '-', 或自定义)

    返回：
        QuantumCircuit: 隐形传态电路
    """
    # 创建量子寄存器
    # q[0]: Alice 的输入量子比特（要传输的态）
    # q[1]: Alice 的贝尔对量子比特
    # q[2]: Bob 的贝尔对量子比特
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(2, 'c')  # 存储 Alice 的测量结果
    qc = QuantumCircuit(qr, cr)

    # 步骤0: 准备要传输的量子态
    if input_state == '1':
        qc.x(0)
    elif input_state == '+':
        qc.h(0)
    elif input_state == '-':
        qc.x(0)
        qc.h(0)
    # 如果是 '0'，不需要任何操作

    qc.barrier()

    # 步骤1: 创建 Alice 和 Bob 之间的贝尔对（在 q[1] 和 q[2] 上）
    # TODO: 在 q[1] 和 q[2] 上创建贝尔态


    qc.barrier()

    # 步骤2: Alice 进行贝尔测量（q[0] 和 q[1]）
    # TODO: CNOT from q[0] to q[1]

    # TODO: H gate on q[0]

    qc.barrier()

    # 步骤3: Alice 测量她的两个量子比特
    qc.measure([0, 1], [0, 1])

    qc.barrier()

    # 步骤4: Bob 根据测量结果应用纠正操作
    # TODO: 如果 c[1] == 1，对 q[2] 应用 X 门
    # 提示：qc.x(2).c_if(cr[1], 1)

    # TODO: 如果 c[0] == 1，对 q[2] 应用 Z 门


    return qc


def test_teleportation():
    """测试量子隐形传态"""

    test_states = {
        '|0⟩': '0',
        '|1⟩': '1',
        '|+⟩': '+',
        '|-⟩': '-'
    }

    print("测试量子隐形传态\n")
    print("=" * 50)

    for name, state_prep in test_states.items():
        print(f"\n传输状态: {name}")

        qc = create_teleportation_circuit(state_prep)

        # 显示电路（仅第一次）
        if name == '|0⟩':
            print("\n电路结构:")
            print(qc.draw(output='text'))

        # 使用有状态模拟器来验证
        # 我们需要在测量之前获取状态
        qc_no_measure = QuantumCircuit(3)

        # 准备初始态
        if state_prep == '1':
            qc_no_measure.x(0)
        elif state_prep == '+':
            qc_no_measure.h(0)
        elif state_prep == '-':
            qc_no_measure.x(0)
            qc_no_measure.h(0)

        # 保存初始态用于比较
        initial_state = Statevector.from_instruction(qc_no_measure)
        initial_qubit_state = [initial_state.data[0], initial_state.data[1]]

        print(f"初始态（q[0]）: {initial_qubit_state}")

        # 运行完整的传态电路
        simulator = Aer.get_backend('aer_simulator')
        qc_test = create_teleportation_circuit(state_prep)

        # 添加额外的测量来检查 Bob 的量子比特
        qc_final = qc_test.copy()
        qc_final.measure(2, 0)  # 重用经典寄存器

        job = simulator.run(qc_final, shots=100)
        counts = job.result().get_counts()

        # 检查结果
        if state_prep == '0':
            expected = '000'  # Bob 的量子比特应该是 0
            assert counts.get(expected, 0) > 90, f"传输 |0⟩ 失败，结果: {counts}"
        elif state_prep == '1':
            expected = '001'  # Bob 的量子比特应该是 1
            assert counts.get(expected, 0) > 90, f"传输 |1⟩ 失败，结果: {counts}"

        print(f"✓ {name} 传输成功！")

    return True


def demonstrate_teleportation():
    """演示量子隐形传态的工作原理"""
    print("\n" + "=" * 50)
    print("量子隐形传态原理演示")
    print("=" * 50)

    print("""
量子隐形传态协议：

1. 初始状态：
   - Alice 有量子比特 q[0]，处于状态 |ψ⟩ = α|0⟩ + β|1⟩
   - Alice 和 Bob 共享贝尔对：q[1] 和 q[2]

2. Alice 的操作：
   - 对 q[0] 和 q[1] 进行 CNOT 和 H 操作（贝尔测量）
   - 测量 q[0] 和 q[1]，得到2个经典比特

3. Bob 的操作：
   - 根据 Alice 的测量结果应用纠正：
     * 如果第2位是1，应用 X 门
     * 如果第1位是1，应用 Z 门
   - Bob 的量子比特现在处于 |ψ⟩ 态

关键点：
- 需要经典通信（Alice 告诉 Bob 测量结果）
- Alice 的原始态被破坏（满足不可克隆定理）
- Bob 获得的是原始态的完美副本
    """)

    return True


if __name__ == '__main__':
    try:
        test_teleportation()
        demonstrate_teleportation()

        print("\n🎉 恭喜！你已掌握量子隐形传态！")
        print("\n关键要点:")
        print("- 量子隐形传态利用纠缠传输量子信息")
        print("- 需要经典通信，因此不违反相对论")
        print("- 原始态被破坏，不违反量子不可克隆定理")
        print("- 这是量子网络和量子互联网的基础")
        print("\n历史：")
        print("1993年由Bennett等人提出，1997年首次实验实现")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
