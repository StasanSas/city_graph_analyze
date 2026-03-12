
def get_center(components_id, coordinates_data):
    x, y = 0, 0
    for component in components_id:
        coords = coordinates_data[component]
        x += coords['x_coord']
        y += coords['y_coord']
    return x / len(components_id), y / len(components_id)