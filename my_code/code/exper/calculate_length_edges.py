import numpy as np
import plt

from my_code.code.utilite import read_graphml
from old_code.Handler import OSMHandler
import matplotlib.pyplot as plt

def main():
    g = read_graphml('one_component__and__without_2_chains/Kostroma.graphml')
    a = g.edges(data=True)
    edge_lengths = [data['weight'] for u, v, data in g.edges(data=True)
                    if data['weight'] <= 200]
    print(np.mean(edge_lengths))
    print(np.median(edge_lengths))
    plt.figure(figsize=(10, 6))
    plt.hist(edge_lengths, bins=100, edgecolor='black', alpha=0.7)

    # Явно задаём деления на осях
    x_ticks = range(0, 161, 5)  # От 0 до 160 с шагом 10
    y_ticks = range(0, 1001, 100)  # От 0 до 1000 с шагом 100 (подбери под свои данные)

    plt.xticks(x_ticks, rotation=45)  # rotation для наклона, если нужно
    plt.yticks(y_ticks)

    plt.xlabel('Длина ребра')
    plt.ylabel('Частота')
    plt.title('Гистограмма длин рёбер графа')
    plt.grid(True, alpha=0.3)
    plt.show()
