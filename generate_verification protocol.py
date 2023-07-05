import itertools

from qaft import qaft

num_qubits_list = [5]
approximation_degree_list = [0, 1, 4]
do_swaps_list = [False, True]
inverse_list = [False, True]
insert_barriers_list = [False]

parameters_lists = [
   num_qubits_list,
   approximation_degree_list,
   do_swaps_list,
    inverse_list,
    insert_barriers_list
]

# Добавляем только те тесты, где степень аппроксимации меньше числа кубитов
tests = [parameter_set for parameter_set in itertools.product(*parameters_lists) if parameter_set[0] >= parameter_set[1]]

for test_entry in tests:

    # Параметры запуска
    num_qubits, approximation_degree, do_swaps, inverse, insert_barriers = test_entry

    print(f"""Значение метрики инфиделити для запуска алгоритма для следующих параметров: 
            Количество кубитов {test_entry[0]} 
            Степень аппроксимации {test_entry[1]}
            Гейты SWAP {'присутствуют' if test_entry[2] else 'отсутствуют'}     
            {'Прямое' if test_entry[3] else 'Обратное'} преобразование
            Барьеры {'присутствуют' if test_entry[4] else 'отсутствуют'}
            """)
    print()
    # Требования к показателю
    print('Требования к показателю')




    if approximation_degree == 0:
        print("[-ε, ε]")
        print()
    elif approximation_degree == 1:
        print("[ε, 0.3]")
        print()
    elif 2 < approximation_degree < num_qubits - 1:
        print("[ε, 1]")
        print()
    elif approximation_degree >= num_qubits - 1:
        print("[0.5, 1+ε]")
        print()

    # Измеренное значение
    infidelity, qasm_code = qaft(num_qubits, approximation_degree, do_swaps, inverse, insert_barriers)
    print(f'Измеренное значение {infidelity}')
    print()
    print()