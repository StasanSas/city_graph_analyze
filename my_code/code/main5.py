from c_plus_plus_code.graph_solver import *

graph = {
    0: [(1, 1.0), (2, 2.0)],
    1: [(0, 1.0), (3, 4.0)],
    2: [(0, 2.0), (3, 2.0)],
    3: [(1, 4), (2, 2)]
}

try:
    start_node = 0
    end_node = 3
    distance = get_distances(graph, start_node, end_node)

    if distance == -1.0:
        print(f"Путь от {start_node} до {end_node} не найден.")
    else:
        print(f"Минимальная дистанция от {start_node} до {end_node}: {distance}")

except Exception as e:
    print(f"Ошибка при вызове модуля: {e}")