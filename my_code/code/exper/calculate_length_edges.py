import plt

from old_code.Handler import OSMHandler
import matplotlib.pyplot as plt
start_ref = (55.63265, 37.65817)
end_ref = (55.8468, 37.44116)


mode = 'walk'
file = 'C:\\Users/Acer/Desktop/city_graph_analyze/my_code/city_graphs/Ekaterinburg_graph.osm.pbf'
handler = OSMHandler(start_ref, end_ref, mode=mode, file=file)
g = handler.graph.get_graph()
a = g.edges(data=True)
print(list(a))
edge_lengths = [data['weight'] for u, v, data in g.edges(data=True)
                if data['weight'] <= 160]

plt.figure(figsize=(10, 6))
plt.hist(edge_lengths, bins=100, edgecolor='black', alpha=0.7)

# Явно задаём деления на осях
x_ticks = range(0, 161, 5)  # От 0 до 160 с шагом 10
y_ticks = range(0, 25001, 500)  # От 0 до 1000 с шагом 100 (подбери под свои данные)

plt.xticks(x_ticks, rotation=45)  # rotation для наклона, если нужно
plt.yticks(y_ticks)

plt.xlabel('Длина ребра')
plt.ylabel('Частота')
plt.title('Гистограмма длин рёбер графа')
plt.grid(True, alpha=0.3)
plt.show()