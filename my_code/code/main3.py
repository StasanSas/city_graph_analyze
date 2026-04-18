import networkx as nx

from my_code.code.convertors_graph.cleaner_2chains import Converter2Chains
from my_code.code.convertors_graph.cleaner_one_connected_component import ConverterConnectedComponents
from my_code.code.exper.calculate_length_edges import main
from my_code.code.exper.visualize import find_and_visualize_area
from my_code.code.utilite import read_graphml

#main()

city = "Ekaterinburg"
path_input = f"{city}.graphml"
path_output = f"one_component/{city}.graphml"
cleaner = ConverterConnectedComponents()
cleaner.run(path_input, path_output)

path_input = f"one_component/{city}.graphml"
path_output = f"one_component__and__without_2_chains/{city}.graphml"
cleaner = Converter2Chains()

cleaner.run(path_input, path_output)

graph = read_graphml(path_output)
#graph = nx.read_graphml("C:\\Users\\stanislav.ivanov\\Desktop\\city_graph_analyze\\my_code\\city_pedestrian_graph\\Kostroma.graphml")

#area_file = find_and_visualize_area(
#        graph=graph,
#        center_lat=57.76294207100577,
#        center_lon=40.942512392779435,
#        radius_km=6
#    )
print(3)
