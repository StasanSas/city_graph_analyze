import numpy as np

from old_code.Handler import OSMHandler

def add_in_chain(chain, value, direction):
    if direction == 1:
        chain.append(value)
    else:
        chain.insert(0, value)
    return chain

def find_chains_simple(graph):
    """
    Находит максимальные пути, где все внутренние вершины имеют степень 2.
    Концы пути могут иметь любую степень.
    """
    visited = set()
    chains = []

    for node in graph.nodes():
        if node in visited:
            continue

        if graph.degree(node) == 2:
            chain = [node]
            visited.add(node)
            neighbors_start = list(graph.neighbors(node))
            for d in [(1, neighbors_start[0]), (-1, neighbors_start[1])]: # 1 = вперед, -1 = назад
                direction = d[0]
                current_neighbor = d[1]
                while True:
                    if graph.degree(current_neighbor) == 2:
                        add_in_chain(chain, current_neighbor, direction)

                        visited.add(current_neighbor)
                        next_neighbor = [n for n in graph.neighbors(current_neighbor)
                                 if n not in visited]
                        if len(next_neighbor) != 1:
                            print(len(next_neighbor))
                            break
                        current_neighbor = next_neighbor[0]
                    else:
                        add_in_chain(chain, current_neighbor, direction)
                        break
            if len(chain) >= 4:
                chains.append(len(chain) - 3)
    return chains

def analyze_chains(graph):
    """
    Полный анализ цепочек в графе
    """
    chains = find_chains_simple(graph)

    if not chains:
        print("В графе нет цепочек (путей из вершин степени 2)")
        return None

    # Статистика
    lengths = chains

    analysis = {
        'total_chains': sum(chains),
        #'chain_lengths': lengths,
        'mean_length': np.mean(lengths),
        'median_length': np.median(lengths),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'std_length': np.std(lengths),
        'chains': chains
    }

    return analysis

start_ref = (55.63265, 37.65817)
end_ref = (55.8468, 37.44116)



mode = 'walk'
file = '/my_code/city_graphs/Moscow_graph.osm.pbf'
handler = OSMHandler(start_ref, end_ref, mode=mode, file=file)
g = handler.graph.get_graph()
def calculate_vertex_degrees_compact(graph):
    return dict(graph.degree())

def count_vertices_with_degree(degrees_dict, target_degree):
    """
    Считает количество вершин с заданной степенью.
    """
    count = 0
    for vertex, degree in degrees_dict.items():
        if degree == target_degree:
            count += 1
    return count
dict_degree = calculate_vertex_degrees_compact(g)
print(count_vertices_with_degree(dict_degree, 1))
print(count_vertices_with_degree(dict_degree, 2))
print(count_vertices_with_degree(dict_degree, 3))
print(count_vertices_with_degree(dict_degree, 4))
#print(analyze_chains(g))
handler.handle()
