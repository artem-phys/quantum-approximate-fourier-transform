import numpy as np

from qiskit.circuit import QuantumCircuit
from typing import Optional


def qaft(
        num_qubits: Optional[int] = None,
        approximation_degree: int = 0,
        do_swaps: bool = True,
        inverse: bool = False,
        insert_barriers: bool = False,
):

    if num_qubits < 0:
        raise ValueError("Number of qubits cannot be smaller than 0.")

    if approximation_degree < 0:
        raise ValueError("Approximation degree cannot be smaller than 0.")

    if approximation_degree > num_qubits:
        raise ValueError(f"Approximation degree cannot be greater than n = {num_qubits}.")

    if num_qubits == 0:
        return

    circuit = QuantumCircuit(num_qubits)
    for j in reversed(range(num_qubits)):
        circuit.h(j)
        num_entanglements = max(0, j - max(0, approximation_degree - (num_qubits - j - 1)))
        for k in reversed(range(j - num_entanglements, j)):
            # Use negative exponents so that the angle safely underflows to zero, rather than
            # using a temporary variable that overflows to infinity in the worst case.
            lam = np.pi * (2.0 ** (k - j))
            circuit.cp(lam, j, k)

        if insert_barriers:
            circuit.barrier()

    if do_swaps:
        for i in range(num_qubits // 2):
            circuit.swap(i, num_qubits - i - 1)

    if inverse:
        circuit = circuit.inverse()

    qasm_result = circuit.decompose().qasm()

    return qasm_result

