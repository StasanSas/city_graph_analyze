from typing import Any

from datetime import datetime, timezone


class DataArrival:
    def __init__(self, id_node : int, arrival_time : datetime):
        self.id_node = id_node
        self.arrival_time = arrival_time

    def __hash__(self) -> int:
        return hash((self.id_node, self.arrival_time))

    def __eq__(self, other) -> bool:
        if not isinstance(other, DataArrival):
            return False
        return (self.id_node, self.arrival_time) == (other.id_node, other.arrival_time)

    def __repr__(self):
        return f" {self.id_node} | {self.arrival_time.time()} "


class TransportRoute:
    def __init__(self, id, name, d : dict[DataArrival, DataArrival]):
        self.id = id
        
        self.my_stops = set()
        self.init_stops(d)
        
        self.next_stops = d
        
        self.d_datetime_for_stop_by_id_stop = {}
        self.init_d_datetime(d)
        
        
    def init_stops(self, d : dict[DataArrival, DataArrival]):
        for stop_start, stop_end in d.items():
            self.my_stops.add(stop_start.id_node)
            self.my_stops.add(stop_end.id_node)
            
    def init_d_datetime(self, d : dict[DataArrival, DataArrival]):
        node_ids = set()
        for stop_start in d.keys():
            if stop_start.id_node not in self.d_datetime_for_stop_by_id_stop:
                self.d_datetime_for_stop_by_id_stop[stop_start.id_node] = [stop_start.arrival_time]
            else:
                self.d_datetime_for_stop_by_id_stop[stop_start.id_node].append(stop_start.arrival_time)
            node_ids.add(stop_start.id_node)
        for id in node_ids:
            self.d_datetime_for_stop_by_id_stop[id] = sorted(self.d_datetime_for_stop_by_id_stop[id])



    def is_stop_in_route(self, v) -> bool:
        return v in self.my_stops

    def get_nearest_datetime_for_stop(self, currentDataStateStop : DataArrival) -> DataArrival | None:
        l = self.d_datetime_for_stop_by_id_stop[currentDataStateStop.id_node]
        for time in l:
            if time < currentDataStateStop.arrival_time:
                continue
            return time
        return None

    def get_next_stop_data(self, current_stop_data : DataArrival) -> DataArrival:
        if current_stop_data not in self.next_stops:
            raise ValueError(f"Stop state {current_stop_data} is not start state")
        return self.next_stops[current_stop_data]


class TransportRoutes:
    def __init__(self, routes: list[TransportRoute]):
        self.all_nodes_stop = set()
        self.d_route_by_rote_id = {}
        self.init_d_route_by_route_id(routes)

        self.d_rote_by_node = {}
        self.init_d_rote_by_node(routes)

    def init_d_route_by_route_id(self, routes):
        for route in routes:
            self.d_route_by_rote_id[route.id] = route

    def init_d_rote_by_node(self, routes):
        for route in routes:
            for id_node in route.my_stops:
                if id_node not in self.d_rote_by_node:
                    self.d_rote_by_node[id_node] = []
                self.d_rote_by_node[id_node].append(route.id)
                self.all_nodes_stop.add(id_node)



    def is_stop(self, v) -> bool:
        return v in self.all_nodes_stop

    def get_nearest_routes_for_stop(self, currentDataStateStop : DataArrival) -> list[DataArrival]:
        result = []
        for route_id in self.d_rote_by_node[currentDataStateStop.id_node]:
            route = self.d_route_by_rote_id[route_id]
            nearest_arrival_for_current_route = route.get_nearest_datetime_for_stop(currentDataStateStop)
            if nearest_arrival_for_current_route is None:
                continue
            next_stop_for_current_route = route.get_next_stop_data(
                DataArrival(
                    currentDataStateStop.id_node,
                    nearest_arrival_for_current_route
                )
            )
            result.append(next_stop_for_current_route)
        return result



if __name__ == "__main__":
    d_1 = {}
    s_1__24_00 = DataArrival(1, datetime(2025, 12, 31, 23, 24, 0, tzinfo=timezone.utc))
    s_2__25_00 = DataArrival(2, datetime(2025, 12, 31, 23, 25, 0, tzinfo=timezone.utc))
    d_1[s_1__24_00] = s_2__25_00

    s_3__25_30 = DataArrival(3, datetime(2025, 12, 31, 23, 25, 30, tzinfo=timezone.utc))
    d_1[s_2__25_00] = s_3__25_30

    s_1__27_00 = DataArrival(1, datetime(2025, 12, 31, 23, 27, 00, tzinfo=timezone.utc))
    d_1[s_3__25_30] = s_1__27_00

    s_2__25_00_new = DataArrival(2, datetime(2025, 12, 31, 23, 28, 0, tzinfo=timezone.utc))
    d_1[s_1__27_00] = s_2__25_00_new

    d_2 = {}
    s_4__26_00 = DataArrival(4, datetime(2025, 12, 31, 23, 26, 00, tzinfo=timezone.utc))
    d_2[s_2__25_00] = s_4__26_00

    s_5__26_30 = DataArrival(5, datetime(2025, 12, 31, 23, 26, 30, tzinfo=timezone.utc))
    d_2[s_4__26_00] = s_5__26_30

    s_2__28_00 = DataArrival(2, datetime(2025, 12, 31, 23, 28, 00, tzinfo=timezone.utc))
    d_2[s_2__28_00] = s_2__28_00

    s_4__26_00 = DataArrival(4, datetime(2025, 12, 31, 23, 29, 00, tzinfo=timezone.utc))
    d_1[s_1__27_00] = s_4__26_00
    
    route_1 = TransportRoute(1, d_1)
    route_2 = TransportRoute(2, d_2)
    
    routes = TransportRoutes([route_1, route_2])

    print(routes.is_stop(10))
    print(routes.is_stop(1))
    print(routes.is_stop(1))
    print(routes.get_nearest_routes_for_stop(
        DataArrival(2, datetime(2025, 12, 31, 23, 26, 0, tzinfo=timezone.utc)))
    )

    print(routes.get_nearest_routes_for_stop(
        DataArrival(1, datetime(2025, 12, 31, 23, 23, 0, tzinfo=timezone.utc)))
    )

    print(routes.get_nearest_routes_for_stop(
        DataArrival(1, datetime(2025, 12, 31, 23, 25, 0, tzinfo=timezone.utc)))
    )
    
    