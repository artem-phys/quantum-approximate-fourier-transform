import json

from qaft import qaft

with open('input.json') as fin:
    input_data = json.load(fin)

    num_qubits = input_data['num_qubits']
    approximation_degree = input_data['approximation_degree']
    do_swaps = input_data['do_swaps']
    inverse = input_data['inverse']
    insert_barriers = input_data['insert_barriers']

    infidelity = qaft(num_qubits, approximation_degree, do_swaps, inverse, insert_barriers)

with open('output.json', 'w') as fout:
    json.dump({'infidelity': infidelity}, fout)
