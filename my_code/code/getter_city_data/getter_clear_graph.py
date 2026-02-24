import os
import networkx as nx

from old_code.Modes.WalkMode import WalkMode


def prepare_graph_for_graphml(graph: nx.Graph) -> nx.Graph:
    """
        Конвертирует граф в формат:
        node id -> int
        node attrs -> x_coord, y_coord
        edge attrs -> weight
        """

    new_graph = nx.Graph()

    node_map = {}

    # --- 1. создаём новые id узлов ---
    for i, node in enumerate(graph.nodes()):
        node_map[node] = str(i)

        if isinstance(node, tuple) and len(node) == 2:
            lat, lon = node
        else:
            raise ValueError(
                f"Узел {node!r} не содержит координаты (ожидался tuple(lon, lat))"
            )

        new_graph.add_node(
            str(i),
            x_coord=float(lon),
            y_coord=float(lat),
        )

    # --- 2. копируем рёбра ---
    for u, v, data in graph.edges(data=True):
        if "weight" not in data:
            raise ValueError(
                f"У ребра ({u!r}, {v!r}) отсутствует атрибут 'weight'"
            )
        new_graph.add_edge(
            node_map[u],
            node_map[v],
            weight=float(data["weight"])
        )

    return new_graph


def save_clear_graph(input_dir, output_dir, file):
    path = os.path.join(input_dir, file)

    tag_finder = WalkMode(file=path)
    graph = tag_finder.get_graph().get_graph()

    graph = prepare_graph_for_graphml(graph)

    name = file.split("_")[0]
    out_path = os.path.join(output_dir, name + ".graphml")

    nx.write_graphml(
        graph,
        out_path,
        encoding="utf-8",
        prettyprint=True
    )


def save_clear_files():
    output_dir = "../../city_clear_graph"
    os.makedirs(output_dir, exist_ok=True)

    input_dir = "../../city_graphs"

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pbf"):
            save_clear_graph(input_dir, output_dir, file_name)


if __name__ == "__main__":
    # save_clear_files()
    output_dir = "../../city_clear_graph"
    input_dir = "../../city_graphs"
    save_clear_graph(input_dir, output_dir, 'Kostroma_graph.osm.pbf')