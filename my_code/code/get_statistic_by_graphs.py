import os

from my_code.code.rusian_cityes import read_cities_file
from old_code.Modes.WalkMode import WalkMode

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cities = read_cities_file('rusian_city.txt')
    current_directory = 'city_graphs'
    for city in cities:
        filename = f"{city['name'].replace(' ', '_')}_graph.osm.pbf"
        filepath = os.path.join(current_directory, filename)
        creator_graph = WalkMode(filepath)
        graph = creator_graph.get_graph().graph
        print(city['name'] + ": \nвершины - " + str(len(graph.nodes.keys())) + "\nрёбра - " + str(len(graph.edges.keys())))


