import folium

def parse_data(text: str):
    segments = []
    current = []

    for line in text.splitlines():
        line = line.strip()

        if not line or line == "city" or line == "1":
            continue

        if line == "END":
            if current:
                segments.append(current)
                current = []
            continue
        if line == "!":
            continue
        lon, lat   = map(float, line.split())
        current.append((lat, lon))

    return segments


def visualize(segments):
    # центр карты
    first_point = segments[0][0]
    m = folium.Map(location=first_point, zoom_start=12)

    for seg in segments:
        folium.PolyLine(seg).add_to(m)

    return m



# --- использование ---
text = None

with open('C:\\Users\\stanislav.ivanov\\Desktop\\city_graph_analyze\\my_code\\city_polygons\\Ekaterinburg.poly', 'r') as f:
    text = f.read()

segments = parse_data(text)
m = visualize(segments)

m.save("map.html")