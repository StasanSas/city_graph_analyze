from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Point:
    lon: float
    lat: float

@dataclass_json
@dataclass
class Stop:
    name: str
    lat: float
    lon: float


@dataclass_json
@dataclass
class RouteCoordinates:
    name: str
    stops: List[Stop]


@dataclass_json
@dataclass
class StopTime:
    stop_name: str
    time: List[str]

@dataclass_json
@dataclass
class SubRouteTimes:
    name: str
    time_stops: List[StopTime]


@dataclass_json
@dataclass
class SubRouteTimesNormalized:
    points: List[Point]
    times_list: List[List[str]] # каждый массив соответствует одному проезду автобуса/трамвая/троллейбуса/маршрутки
    # длина каждого массива в массиве = длине points

@dataclass_json
@dataclass
class RouteTimes:
    name: str
    data_sub_route: List[SubRouteTimes]

class Route:
    def __init__(self, name):
        self.name = name
        self.data_stop = [] # [(Stop, [time])]
        self.all_coords = [] # [(lat, lon)]