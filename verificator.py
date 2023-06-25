import json

with open('input.json') as fin:
    input_data = json.load(fin)

    num_qubits = input_data['num_qubits']
    approximation_degree = input_data['approximation_degree']
    do_swaps = input_data['do_swaps']
    inverse = input_data['inverse']
    insert_barriers = input_data['insert_barriers']
    qc_output_filename = input_data['qc_output_filename']

with open('output.json') as fout:
    output_data = json.load(fout)
    infidelity = output_data['infidelity']

    if approximation_degree == 0:
        infidelity_min = -1e-8
        infidelity_max = 1e-8
    elif approximation_degree == 1:
        infidelity_min = 1e-8
        infidelity_max = 0.01
    elif 2 < approximation_degree < num_qubits - 1:
        infidelity_min = 1e-8
        infidelity_max = 1 + 1e-8
    elif approximation_degree >= num_qubits - 1:
        infidelity_min = 0.7
        infidelity_max = 1 + 1e-8

    print(f'infidelity: {infidelity}')


    if infidelity_min < infidelity < infidelity_max:
        print('Verification result: PASS')
    else:
        print('Verification result: FAIL')
