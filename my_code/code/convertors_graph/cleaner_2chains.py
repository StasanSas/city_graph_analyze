import networkx as nx

from my_code.code.convertors_graph.abstract_cleaner import ConverterGraph


class Converter2Chains(ConverterGraph):


    def get_converted_graph(self, graph: nx.graph, coordinates_data : dict[int, dict[str, float]]) -> nx.graph:
        n = graph.numberOfNodes()

        deg = [graph.degree(u) for u in graph.iterNodes()]
        visited_edges = set()
    
        chains = []
    
        for u in graph.iterNodes():
    
            if deg[u] == 2:
                continue
    
            for v in graph.iterNeighbors(u):
    
                edge = (min(u, v), max(u, v))
                if edge in visited_edges:
                    continue
    
                visited_edges.add(edge)
    
                if deg[v] != 2:
                    continue
    
                path = []
                total_weight = graph.weight(u, v)
    
                prev = u
                cur = v
    
                while deg[cur] == 2:
    
                    path.append(cur)
    
                    neigh = list(graph.iterNeighbors(cur))
                    nxt = neigh[0] if neigh[1] == prev else neigh[1]
    
                    edge = (min(cur, nxt), max(cur, nxt))
                    visited_edges.add(edge)
    
                    total_weight += graph.weight(cur, nxt)
    
                    prev = cur
                    cur = nxt
    
                # cur — вторая граничная вершина
                chains.append((u, cur, path, total_weight))
    
        # применяем изменения
        for u, w, path, weight in chains:
    
            for v in path:
                if graph.hasNode(v):
                    graph.removeNode(v)
    
            if graph.hasNode(u) and graph.hasNode(w):
                if not graph.hasEdge(u, w):
                    graph.addEdge(u, w, weight)
                else:
                    old_w = graph.weight(u, w)
                    if weight < old_w:
                        graph.setWeight(u, w, weight)
    
        return graph