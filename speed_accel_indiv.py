import math
import matplotlib.pyplot as plt
import statistics as st

# BRAKE_BOUNDARY = -3
# ACCEL_BOUNDARY = 2.25
FEET_PER_MILE = 5280
SECONDS_PER_HR = 3600


# computes the speed and acceleration of vehicles at every time point
# input
# output
def compute_speed_accel(data):
    for data_set in data:
        timestamp = data_set['timestamp']
        y_pos = data_set['y_position']
        x_pos = data_set['x_position']
        speed = [(0,0,0)]
        accel = [(0,0,0), (0,0,0)]

        for i in range(1, len(timestamp)):
            x1, x2, y1, y2 = x_pos[i-1], x_pos[i], y_pos[i-1], y_pos[i]

            # in miles
            y_dist = (y2-y1)/FEET_PER_MILE
            x_dist = (x2-x1)/FEET_PER_MILE
            delta_dist = math.sqrt((x_dist)**2+(y_dist)**2)

            delta_time = (timestamp[i]-timestamp[i-1])  # in seconds


            y_speed_cur = y_dist/delta_time*SECONDS_PER_HR
            x_speed_cur = x_dist/delta_time*SECONDS_PER_HR
            cur_speed = delta_dist/delta_time*SECONDS_PER_HR  # mph

            speed.append((x_speed_cur, y_speed_cur, cur_speed))  # converts to mph

            if i == 1:
                continue


            delta_speed = cur_speed - speed[i-1][2]
            delta_speed_y = y_speed_cur - speed[i-1][1]
            delta_speed_x = x_speed_cur - speed[i-1][0]

            cur_accel = delta_speed*(FEET_PER_MILE/SECONDS_PER_HR)/delta_time  # accel per sec: fpsps
            y_accel_cur = delta_speed_y*(FEET_PER_MILE/SECONDS_PER_HR)/delta_time
            x_accel_cur = delta_speed_x*(FEET_PER_MILE/SECONDS_PER_HR)/delta_time

            accel.append((x_accel_cur, y_accel_cur, cur_accel))

        data_set['speed'], data_set['accel'] = speed, accel


def print_speed_accel(data):
    speed = []
    accel = []
    ttl = 0
    for set in data:
        ttl+=1

        # just concatenate the lists
        for i in range(1, len(set['speed'])):
            speed.append(set['speed'][i][2])
            if i == 1: continue
            accel.append(set['accel'][i][2])

    print(f"across {ttl} trajectories, there was:\n- an average speed of {st.mean(speed):.2f}"
          f" miles per hour\n - maximum: {max(speed):.2f}\n - minimum: {min(speed):.2f}\n - "
          f"standard deviation: {st.stdev(speed):.2f}")
    print(f"- an average acceleration of {st.mean(accel):.2f} feet per second squared\n"
          f" - maximum: {max(accel):.2f}\n - minimum: {min(accel):.2f}\n - standard deviation: "
          f"{st.stdev(accel):.2f}")

    print("graphed information of distributions of speed and acceleration: ")
    graph_speed_accel(speed, accel)


def graph_speed_accel(speed, accel):
    figure, axis = plt.subplots(nrows=1, ncols=2)
    axis[0].hist(speed)
    axis[0].set_ylabel("# of trajectories")
    axis[0].set_xlabel("speed (mph)")
    axis[0].set_title("distribution of speeds")

    axis[1].hist(accel)
    axis[1].set_ylabel("# of trajectories")
    axis[1].set_xlabel("acceleration (f/s^2)")
    axis[1].set_title("distribution of accelerations")

    plt.show()


# computes the number of acceleration and brake events per trajectory and adds it in data set
# in the form of (avg acceleration of event, start time, end time)
def compute_accel_events(data, variable, BRAKE_BOUNDARY, ACCEL_BOUNDARY):
    ttl_evnt = 0
    if variable == 'x':
        idx_accel = 0
        num_accel_name = '# x_accel'
        num_brake_name = '# x_brake'
    if variable == 'y':
        idx_accel = 1
        num_accel_name = '# y_accel'
        num_brake_name = '# y_brake'
    if variable == 'ttl':
        idx_accel = 2
        num_accel_name = '# accel'
        num_brake_name = '# brake'

    for data_set in data:
        accel = data_set['accel']
        data_set[num_accel_name], data_set[num_brake_name] = [], []
        b, a, event = False, False, False
        start_time, start_idx, running_sum, running_count = 0, 0, 0, 0
        index = 0
        while index < len(accel):
            pt = accel[index][idx_accel]

            # event ends or prog ends...
            if event and (((a and pt < ACCEL_BOUNDARY) or (b and pt > BRAKE_BOUNDARY)) or index == len(accel)-1):
                end_idx = index
                ttl_evnt+=1

                # checks if new event is beginning. if it jumps from -3 to 2.25 in one time stamp
                if (a and pt <= BRAKE_BOUNDARY) or (b and pt >= ACCEL_BOUNDARY):
                    # event ends, but new event immediately begins, so we set index back for next
                    # iteration to start at current index and begin event.
                    index -= 1

                # start time, end time, avg acceleration
                cur = (running_sum/running_count, start_time, data_set['timestamp'][end_idx])
                if running_sum < 0:
                    data_set[num_brake_name].append(cur)
                    b = False
                else:
                    data_set[num_accel_name].append(cur)
                    a = False
                event = False
                running_sum, running_count = 0,0

            # event begins
            elif not event and pt >= ACCEL_BOUNDARY or pt <= BRAKE_BOUNDARY:
                event = True
                start_idx = index
                start_time = data_set['timestamp'][start_idx]
                running_sum += pt
                running_count += 1
                if pt >= ACCEL_BOUNDARY:
                    a = True
                else:
                    b = True

            # event is occurring
            elif event and index!=len(accel)-1:
                # make sure it doesn't jump from -3 to 2.25 in one time stamp
                running_sum += pt
                running_count += 1

            index += 1
    print("total events:", ttl_evnt)


# computes percentage of total trajectory spent in acceleration and brake events
def compute_accel_percentage(data):
    for data_set in data:
        total_time = data_set['timestamp'][-1]-data_set['timestamp'][0]
        time_accel, time_brake = 0, 0
        if data_set['# accel']:
            for itm in data_set['# accel']:
                time_accel += itm[1]-itm[0]
        if data_set['# brake']:
            for itm in data_set['# brake']:
                time_brake += itm[1] - itm[0]
        data_set['% accel'] = time_accel / total_time
        data_set['% brake'] = time_brake / total_time


# finds lane changes and puts it in 'lane_changes' key in form [lane_name, start time in lane, end time in lane]
def find_lane_changes(data):
    lanes = {'E1': [0, 12], 'E2': [12, 24], 'E3': [24, 36], 'E4': [36, 48], 'E5': [48, 60],
             'E6': [60, 72], 'W1': [72, 84], 'W2': [84, 96], 'W3': [96, 108], 'W4': [108, 120],
             'W5': [120, 132], 'W6': [132, 144]}

    for data_set in data:
        y_pos = data_set['y_position']
        data_set['lane_changes'] = []
        prev, cur = None, None
        start_time, stop_time = data_set['timestamp'][0], None
        for i, y in enumerate(y_pos):

            # finds which lane the car is in
            for lane, rnge in lanes.items():
                if rnge[0] < y <= rnge[1]:
                    cur = lane
                    if not prev:
                        prev = cur
                    break

            # lane change occurs
            if prev != cur:
                stop_time = data_set['timestamp'][i]
                data_set['lane_changes'].append([prev, start_time, stop_time])
                start_time = stop_time
                prev = cur

        # add the last lane in
        if not data_set['lane_changes'] or data_set['lane_changes'][-1][0] != cur:
            data_set['lane_changes'].append([cur, start_time, data_set['timestamp'][-1]])


def print_lane_changes(data):
    ttl, ttl_lc, num_changes = 0,0,0
    lanes = {'E1': 0, 'E2': 0, 'E3': 0, 'E4': 0, 'E5': 0, 'E6': 0, 'W1': 0, 'W2': 0,
                      'W3': 0, 'W4': 0, 'W5': 0, 'W6': 0}
    for set in data:
        ttl += 1
        if len(set['lane_changes']) > 1:
            ttl_lc += 1
            num_changes += len(set['lane_changes']) - 1
        for chng in set['lane_changes']:
            lanes[chng[0]] += 1

    print(f'there were {ttl_lc} trajectories with lane changes, with an average of '
          f'{num_changes/ttl_lc:.2f} lane changes. ')
    print(f'across all {ttl} trajectories, the average number of lanes each car occupied was '
          f'{(num_changes+ttl)/ttl:.2f}. ')

    names = list(lanes.keys())
    values = list(lanes.values())

    plt.bar(range(len(lanes)), values, tick_label=names)
    plt.ylabel("# of trajectories")
    plt.xlabel("lane of highway")
    plt.title("distribution of lane locations")
    plt.show()


# calculates the conditional probability of P(B|A)
def intersection_conditional(data):
    # N(A + B) / N(A) = P(B | A): num acceleration and lane change / num lane change = prob accel given lane chng
    # A = lane change
    # B = acceleration of x
    summed_conditional_A_given_B = 0
    summed_occurrences_A_given_B = 0
    summed_conditional_B_given_A = 0
    summed_occurrences_B_given_A = 0

    for set in data:

        event_As = set['lane_changes'][:-1] # last one isn't really a lane change
        event_Bs = set['# x_accel']
        num_A_and_B = 0
        num_A = len(event_As)
        num_B = len(event_Bs)

        if num_A == 0 and num_B == 0:
            # neither event a or b... doesn't count for anything
            continue
        elif num_A == 0:
            # event b happened... acceleration but no lane change
            summed_conditional_A_given_B += 0
            summed_occurrences_A_given_B += 1
        elif num_B == 0:
            # event a happened... lane change but no accel
            summed_conditional_B_given_A += 0
            summed_occurrences_B_given_A += 1
        else:
            # there is both lane change and acceleration
            idx_B = 0
            for event_A in event_As:
                lane_change_moment = event_A[2]

                # if accel event within 1 sec before the lane change: count
                # lane change moment is too far past event B at idxB
                while idx_B < num_B and lane_change_moment - event_Bs[idx_B][2] > 1:
                    idx_B += 1
                if idx_B >= num_B:
                    break
                    # lane change in middle of acceleration event
                    # can one accel event be related to TWO lane changes?
                if event_Bs[idx_B][1] - 1 <= lane_change_moment <= event_Bs[idx_B][2] + 1:
                    num_A_and_B += 1

            summed_conditional_B_given_A += num_A_and_B/num_A
            summed_conditional_A_given_B += num_A_and_B/num_B
            summed_occurrences_A_given_B+=1
            summed_occurrences_B_given_A+=1

    print(f'P(B|A): {summed_conditional_B_given_A/summed_occurrences_B_given_A*100:.2f}%') #should be 0.33
    print(f'P(A|B): {summed_conditional_A_given_B/summed_occurrences_A_given_B*100:.2f}%')


def time_interval(data):
    time_differences = {}
    for set in data:
        for i in range(1, len(set['timestamp'])):
            diff = set['timestamp'][i]-set['timestamp'][i-1]
            time_differences[diff] = time_differences.get(diff, 0) + 1
    print(time_differences)


def main(data, BRAKE_BOUNDARY, ACCEL_BOUNDARY):
    config = {
        'print': False
    }

    compute_speed_accel(data)
    compute_accel_events(data, 'x', BRAKE_BOUNDARY, ACCEL_BOUNDARY)
    # percent_accel_brake_times(data)
    find_lane_changes(data)
    intersection_conditional(data)
    # time_interval(data)


    if config['print']:
        print_speed_accel(data)
        print_lane_changes(data)
