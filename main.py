import json

FILE = "groundtruth_scene_1_130__cajoles.json"

import speed_accel_indiv
import analysis_by_timestamp

def main():
    with open(FILE) as f:
        data = json.load(f)

    # analyze speed and acceleration information for individual trajectories
    # per bound
    print("-3 to 2.25")
    speed_accel_indiv.main(data, -3, 2.25)
    print()

    print("-2.5 to 2")
    speed_accel_indiv.main(data, -2.5, 2)
    print()

    print("-1.5 to 1")
    speed_accel_indiv.main(data, -1.5, 1)
    print()

    # analyze interactions between cars


main()