import json


def organize_by_car(data):
    lanes = {'E1': [0, 12], 'E2': [12, 24], 'E3': [24, 36], 'E4': [36, 48], 'E5': [48, 60],
             'E6': [60, 72], 'W1': [72, 84], 'W2': [84, 96], 'W3': [96, 108], 'W4': [108, 120],
             'W5': [120, 132], 'W6': [132, 144]}
    for set in data:
        by_car = {'E1': [], 'E2': [], 'E3': [], 'E4': [], 'E5': [], 'E6': [], 'W1': [], 'W2': [],
                    'W3': [], 'W4': [], 'W5': [], 'W6': []}
        pos = set['position']
        id = set['id']
        for i in range(len(id)):
            # recalculate lane change ?
            x, y = pos[i]
            carid = list(id[i].values())[0]
            for key, ranges in lanes.items():
                # sorting by lane
                if ranges[0] < y <= ranges[1]:
                    by_car[key].append((x, y, carid))
                    break
        set['by car'] = by_car
        # print(by_car)

def organize_by_x(data):
    # where each set is a timestamp
    for set in data:

        # where key is lane number, values are list of cars on lane
        for key, values in set['by car'].items():

            # sort each lane in the time stamp by x position
            values.sort(key = lambda x:x[0])


def get_car_leaders(data, by_car_by_timestamp):
    for set in data:
        time = set['timestamp']

        for key, values in set['by car'].items():

            # where car is each car on lane
            for idx, car in enumerate(values):

                car_id = car[2]
                if not car_id in by_car_by_timestamp:
                    by_car_by_timestamp[car_id] = {'leader': []}
                car_leader = by_car_by_timestamp[car_id]['leader']

                if idx == len(values) - 1:
                    leader = None
                else:
                    leader = values[idx + 1][2]

                # no leader written or last leader not the same as this leader
                if car_leader == [] or car_leader[-1][0] != leader:
                    car_leader.append((leader, time))


def create_newfile_dictionary(new_file, by_car_by_timestamp):
    new_file.write(json.dumps(by_car_by_timestamp, indent=4))


def main(data):
    by_car_by_timestamp = {}
    config= {
        'create_new_file': 0
    }

    organize_by_car(data)
    organize_by_x(data, by_car_by_timestamp)

    if config['create_new_file']:
        with open('groundtruth_scene_1_130__cajoles_transformed_by_car.json', 'w') as new_file:
            create_newfile_dictionary(new_file, by_car_by_timestamp)


