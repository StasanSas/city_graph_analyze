from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Point:
    x: float
    y: float

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
    points: List[Point]


@dataclass_json
@dataclass
class RouteTime:
    stops: List[str]
    time: List[str]

@dataclass_json
@dataclass
class RouteTimes:
    data_times: List[RouteTime]

class Route:
    def __init__(self, name):
        self.name = name
        self.data_stop = [] # [(Stop, [time])]
        self.all_coords = [] # [(lat, lon)]