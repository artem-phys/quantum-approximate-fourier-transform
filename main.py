import json

from qaft import qaft

with open('input.json') as fin:

    # Открытие файла с входными данными в формате json
    input_data = json.load(fin)

    # Чтение входных данных
    num_qubits = input_data['num_qubits']
    approximation_degree = input_data['approximation_degree']
    do_swaps = input_data['do_swaps']
    inverse = input_data['inverse']
    insert_barriers = input_data['insert_barriers']
    qc_output_filename = input_data['qc_output_filename']

    # Подсчёт метрики инфиделити и генерация кода на QASM с помощью основной функции алгоритма
    infidelity, qasm_code = qaft(num_qubits, approximation_degree, do_swaps, inverse, insert_barriers)

# Запись выходных данных в формате json
with open('output.json', 'w') as fout:

    json.dump({'infidelity': infidelity}, fout)

# Запись кода на QASM в файл
with open(qc_output_filename, 'w') as fout2:
    fout2.write(qasm_code)
