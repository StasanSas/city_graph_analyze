import networkx as nx

from my_code.code.cleaning.abstract_cleaner import CleanerGraph


class Cleaner2Chains(CleanerGraph):
    def __init__(self, *args, **kwargs):
        super(Cleaner2Chains, self).__init__(*args, **kwargs)

    def get_clean_graph(self, graph: nx.Graph) -> nx.Graph:
        """Удаляем изолированные вершины"""
        graph = graph.copy()  # Работаем с копией
        isolated = list(nx.isolates(graph))
        graph.remove_nodes_from(isolated)
        print(f"Удалено изолированных вершин: {len(isolated)}")
        return graph