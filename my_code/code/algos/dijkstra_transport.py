from datetime import time

import networkit as nk

from my_code.code.algos.transport_routes.transport_routes import TransportRoutes, DataArrival


class DijkstraWithTransport():
    def __init__(self, g : nk.Graph, start_time : time, transportRoutes : TransportRoutes = TransportRoutes([])):
        # g ПЕШЕХОДНЫЙ граф с рёбрами, содержащими информацию о ВРЕМЕНИ движения между вершинами
        # start_time время отправления пешехода из своей начальной точки
        # можно было добавить как аргумент в run, но мы делаем на основе этого времени предобработку transportRoutes
        # TransportRoutes  - структура, необходимая для обработки маршрутов общественного транспорта
        # Её нужно создавать с умом, чтобы была связана с графом g.
        pass

