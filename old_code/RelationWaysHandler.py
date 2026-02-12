import osmium
from django.contrib.gis.geos import LineString, Point
from shapely.ops import linemerge, polygonize, unary_union


class RelationWaysHandler():
     def __init__(self, file_input, file_output, city_name):
         self.file_output = file_output

         self.file_input = file_input
         self.city_name = city_name
         self.ways_ids = []
         self.ways_locations = []
         self.polygon_flag = 0


     def build_polygon(self):
         for obj in osmium.FileProcessor(self.file_input, osmium.osm.RELATION) :
             if 'addr:country' in obj.tags and 'name' in obj.tags:
                 if obj.tags['addr:country'] == 'RU' and obj.tags ['name'] == self.city_name:
                    for m in obj.members:
                         if m.type == 'w':
                            self.ways_ids.append(m.ref)
         for obj in osmium.FileProcessor(self.file_input).with_locations():
             if obj.id in self.ways_ids:
                coords = [( n.lon, n.lat ) for n in obj.nodes ]
                self.ways_locations.append(LineString(coords))
             if len(self.ways_locations)>0:
                self.polygon_flag=1

     def is_polygon(self):
         if self.polygon_flag:
            return True
         return False

     def get_polygon(self):
         merged = linemerge(self.ways_locations)
         borders = polygonize(merged)
         polygon = unary_union(list(borders))
         return polygon

     def is_node_inside_polygon(self, node_lon, node_lat, polygon ) :
         point = Point(node_lon, node_lat)
         return polygon.contains(point)

     def get_output_file(self) :
         self.build_polygon()
         k = 0
         if self.is_polygon():
             polygon = self.get_polygon()
             with osmium.ForwardReferenceWriter(self.file_output, self.file_input, overwrite = True) as writer:
                 for obj in osmium.FileProcessor(self.file_input, osmium.osm.NODE ):
                     n_lon, n_lat = obj.lon, obj.lat
                     if self.is_node_inside_polygon(n_lon, n_lat, polygon):
                        writer.add_node(obj)
