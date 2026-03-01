import networkit as nk
import networkx as nx


def nx_to_nk(nx_graph):
    n_nodes = len(nx_graph.nodes())

    nk_graph = nk.Graph(n_nodes, weighted=True, directed=False)

    for u, v, data in nx_graph.edges(data=True):
        if "weight" not in data:
            raise ValueError(f"Ребро ({u}, {v}) не имеет веса")
        weight = float(data["weight"])
        nk_graph.addEdge(int(u), int(v), weight)

    return nk_graph



def nx_to_nk_with_extra(nx_graph):
    n_nodes = len(nx_graph.nodes())
    nk_g = nk.Graph(n_nodes, weighted=True, directed=nx_graph.is_directed())

    extra = {}
    for n, d in nx_graph.nodes(data=True):
        extra[int(n)] = d

    for u, v, d in nx_graph.edges(data=True):
        if "weight" not in d:
            raise ValueError(f"Edge {(u,v)} no weight")
        weight = float(d["weight"])
        nk_g.addEdge(int(u), int(v), weight)

    return nk_g, extra

def nk_to_nx(nk_g, extra=None):
    extra = extra or {}
    nx_g = nx.Graph()

    for u in nk_g.iterNodes():
        nx_g.add_node(str(u), **extra.get(u, {}))

    for u, v in nk_g.iterEdges():
        w = nk_g.weight(u, v)
        nx_g.add_edge(str(u), str(v), weight=w)

    return nx_g