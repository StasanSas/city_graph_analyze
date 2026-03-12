from xml.sax import handler

import networkx as nx
import numpy as np

from old_code.Handler import OSMHandler



g = nx.read_graphml("..\..\city_cleaned_graphs\one_component__and__without_2_chains\Kostroma.graphml")
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

def calculate_length_with_vertex_degrees(g, target_degree, degrees_dict):
    edge_lengths = [data['weight'] for u, v, data in g.edges(data=True)
                    if degrees_dict[u] == target_degree or dict_degree[v] == target_degree]
    edge_lengths = sorted(edge_lengths)
    print(np.mean(edge_lengths))
    print(np.median(edge_lengths))
    l_batch = int(len(edge_lengths) / 10)
    print([float(np.mean(edge_lengths[i:i + l_batch])) for i in range(0, len(edge_lengths), l_batch)])
    print()




dict_degree = calculate_vertex_degrees_compact(g)
print(count_vertices_with_degree(dict_degree, 1))
print(count_vertices_with_degree(dict_degree, 2))
print(count_vertices_with_degree(dict_degree, 3))
print(count_vertices_with_degree(dict_degree, 4))
print(count_vertices_with_degree(dict_degree, 5))
print(count_vertices_with_degree(dict_degree, 6))
print(count_vertices_with_degree(dict_degree, 7))
print(count_vertices_with_degree(dict_degree, 8))
#print(analyze_chains(g))
print("\n")
calculate_length_with_vertex_degrees(g, 1, dict_degree)
calculate_length_with_vertex_degrees(g, 3, dict_degree)
calculate_length_with_vertex_degrees(g, 4, dict_degree)

