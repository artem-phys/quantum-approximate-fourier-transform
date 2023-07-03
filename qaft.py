import numpy as np

from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit import Aer, execute
from qiskit.quantum_info import process_fidelity
from typing import Optional


def qaft(
        num_qubits: Optional[int] = None,
        approximation_degree: int = 0,
        do_swaps: bool = True,
        inverse: bool = False,
        insert_barriers: bool = False,
):
    """
    :param num_qubits: число кубитов
    :param approximation_degree: степень аппроксимации. Показывает, сколько самых малых поворотов можно отбросить
    :param do_swaps: Флаг, указывающий на необходимость применить гейты SWAP в конце преобразования
    :param inverse: Флаг, указывающий на необходимость реализовать не прямое, а обратное преобразование Фурье
    :param insert_barriers: Флаг, указывающий на необходимость вставить барьеры
    :return: infidelity: Метрика инфиделити - указывает отличие сгенерированного приблжённого преобразования QFT от точного QFT
    :return: qasm_code: Код цепочки сгенерированного приблжённого преобразования QFT в формате OPEN QASM
    """

    # Проверки входных данных
    if num_qubits < 0:
        raise ValueError("Number of qubits cannot be smaller than 0.")

    if approximation_degree < 0:
        raise ValueError("Approximation degree cannot be smaller than 0.")

    if approximation_degree > num_qubits:
        raise ValueError(f"Approximation degree cannot be greater than n = {num_qubits}.")

    if num_qubits == 0:
        return

    # Создание цепочки
    circuit = QuantumCircuit(num_qubits)
    for j in reversed(range(num_qubits)):
        circuit.h(j)
        num_entanglements = max(0, j - max(0, approximation_degree - (num_qubits - j - 1))) # число запутываний

        # Цикл по числу запутываний
        for k in reversed(range(j - num_entanglements, j)):
            # угол поворота для контролируемого вращения
            lam = np.pi * (2.0 ** (k - j))

            # Контролируемое вращение
            circuit.cp(lam, j, k)

        # Вставляем барьеры, если надо
        if insert_barriers:
            circuit.barrier()

    # Применяем свопы, если надо
    if do_swaps:
        for i in range(num_qubits // 2):
            circuit.swap(i, num_qubits-i - 1)

    # Применяем обратное преобразование, если надо
    if inverse:
        circuit = circuit.inverse()

    qasm_code = circuit.decompose().qasm()

    # Симуляция цепочки для получения матрицы унитарного преобразования
    backend = Aer.get_backend('unitary_simulator')
    job = execute(circuit, backend)
    result = job.result()
    u = result.get_unitary(circuit)

    # Точный QFT
    perfect_qft = QFT(num_qubits=num_qubits, approximation_degree=0, do_swaps=do_swaps,
                      inverse=inverse, insert_barriers=insert_barriers)

    backend = Aer.get_backend('unitary_simulator')
    job = execute(perfect_qft, backend)
    result = job.result()
    v = result.get_unitary(perfect_qft)

    # Вычисление инфделити
    infidelity = 1 - process_fidelity(u, v)

    return infidelity, qasm_code
