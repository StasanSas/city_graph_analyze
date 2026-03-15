import osmium


class StopRouteHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()

        # id -> (lon, lat, tags)
        self.stops = {}

        # route_id -> route info
        self.routes = {}

    def node(self, n):
        tags = n.tags

        is_stop = (
            tags.get("highway") == "bus_stop"
            or tags.get("railway") == "tram_stop"
            or tags.get("amenity") == "bus_station"
            or tags.get("public_transport") in ["platform", "stop_position"]
        )

        if is_stop:
            self.stops[n.id] = (
                n.location.lon,
                n.location.lat,
                dict(tags),
            )

    def relation(self, r):
        tags = r.tags

        if tags.get("type") != "route":
            return

        route_type = tags.get("route")

        if route_type not in [
            "bus",
            "tram",
            "trolleybus",
            "subway",
            "light_rail",
            "train",
        ]:
            return

        stops = []

        for m in r.members:
            if m.type == "n" and m.role in (
                "stop",
                "platform",
                "stop_entry_only",
                "stop_exit_only",
            ):
                stops.append(m.ref)

        if stops:
            self.routes[r.id] = {
                "type": route_type,
                "name": tags.get("name"),
                "ref": tags.get("ref"),
                "stops": stops,
                "tags": dict(tags),
            }
