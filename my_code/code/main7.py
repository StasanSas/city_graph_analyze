from my_code.code.convertors_graph.convertor_distance_in_times import ConverterDistanceInTimes
from my_code.code.utilite import read_graphml

name = 'Ekaterinburg'
path_input = f'one_component__and__without_2_chains/{name}.graphml'
path_output = f'time_pedestrian_graph/{name}.graphml'
cleaner = ConverterDistanceInTimes()

cleaner.run(path_input, path_output)

graph = read_graphml(path_output)
print(graph)

