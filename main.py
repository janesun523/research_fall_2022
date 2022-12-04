import json

FILE_BY_CAR = "groundtruth_scene_1_130__cajoles.json"
FILE_BY_TIMESTAMP = "groundtruth_scene_1_130__cajoles_transformed.json"

import speed_accel_indiv
import analysis_by_timestamp

def main():
    with open(FILE_BY_CAR) as f:
        data_by_car = json.load(f)
    with open(FILE_BY_TIMESTAMP) as f:
        data_by_timestamp = json.load(f)

    # analyze speed and acceleration information for individual trajectories
    # per bound
    print("-3 to 2.25")
    speed_accel_indiv.main(data_by_car, -3, 2.25)
    #
    # print("-2.5 to 2")
    # speed_accel_indiv.main(data_by_car, -2.5, 2)
    #
    # print("-1.5 to 1")
    # speed_accel_indiv.main(data_by_car, -1.5, 1)

    # analyze interactions between cars
    analysis_by_timestamp.main(data_by_timestamp)

main()