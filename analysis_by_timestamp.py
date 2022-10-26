def organize_by_car(data):
    for set in data:
        by_car = []
        pos = set['position']
        id = set['id']
        for i in range(len(id)):
            # recalculate lane change ?
            x, y = pos[i]
            carid = list(id[i].values())[0]
            by_car.append((x, y, carid))
        set['by car'] = by_car

def organize_by_x(data):
    for set in data:
        set['by car'].sort(key = lambda x : x[0])

def main(data):
    organize_by_car(data)
    organize_by_x(data)