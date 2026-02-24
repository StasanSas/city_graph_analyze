import networkit as nk

def nx_to_nk(nx_graph):
    n_nodes = len(nx_graph.nodes())

    nk_graph = nk.Graph(n_nodes, weighted=True, directed=False)

    for u, v, data in nx_graph.edges(data=True):
        if "weight" not in data:
            raise ValueError(f"Ребро ({u}, {v}) не имеет веса")
        weight = float(data["weight"])
        nk_graph.addEdge(int(u), int(v), weight)

    return nk_graph