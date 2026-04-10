from matplotlib import pyplot as plt


def draw_plot_by_x_and_y(x : list[float], y : list[float]):

    plt.plot(x, y)
    plt.xlabel("Размер кластера")
    plt.ylabel("Кол-во кластеров")
    plt.title("Зависимость кол-ва кластеров от размера кластера")
    plt.show()