import pandas as pd
import numpy as np
import os
import datetime


def calculate_final_xaxis_dist(data):
    return data.groupby('Track no')['X'].apply(lambda x: x.iloc[26] - x.iloc[0]).to_dict()


def calc_tactic_index(data):
    second_column = list(data.values())
    forward_sum = sum(1 for x in second_column if x > 0)
    backward_sum = sum(1 for x in second_column if x < 0)
    return (backward_sum - forward_sum) / (forward_sum + backward_sum)


def average_step_displacement(step_delta):
    positive_steps = [step for step in step_delta if step > 0]
    negative_steps = [step for step in step_delta if step < 0]
    avg_positive = sum(positive_steps) / len(positive_steps)
    avg_negative = sum(negative_steps) / len(negative_steps)
    return avg_positive, avg_negative


def calculate_velocity(displacement, time):
    return displacement / time


def calculate_track_length(x, y):
    distance = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    return np.sum(distance)


def analyze_tracks(tracked_data, output_file):
    for track, track_data in tracked_data.groupby('Track no'):
        dx = track_data['X'].iloc[26] - track_data['X'].iloc[0]
        if dx > 0:
            step_delta = np.diff(track_data['X'])
            avg_positive_step_displacement, avg_negative_step_displacement = average_step_displacement(step_delta)

            velocity_change = np.diff(track_data['X'])
            velocity = calculate_velocity(dx, 12)  # Assuming 12 units of time

            x = track_data['X']
            y = track_data['Y']

            track_length = calculate_track_length(x, y)

            output_file.write(f'Track: {track}\n')
            output_file.write(f'Avg +ve step displacement = {avg_positive_step_displacement}\n')
            output_file.write(f'Avg -ve step displacement = {avg_negative_step_displacement}\n')
            output_file.write(f'Velocity: {velocity}\n')
            output_file.write(f'Velocity Change: {velocity_change}\n')
            output_file.write(f'Track Length: {track_length}\n\n')


input_folder_path = './input_files/'  # Replace with the path to your folder
output_folder_path = './output_files/'  # Replace with the path to your output folder

current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.txt")
output_file_path = os.path.join(output_folder_path, file_name)

with open(output_file_path, 'w') as output_file:
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)

        if os.path.isfile(file_path) and filename.endswith('.csv'):
            output_file.write(f'\nProcessing file: {file_path}\n\n')

            tracked_data = pd.read_csv(file_path)
            final_distances_xaxis = calculate_final_xaxis_dist(tracked_data)
            final_ti = calc_tactic_index(final_distances_xaxis)

            output_file.write('Xf-Xi values for all tracks\n')
            for track, tactic_index in final_distances_xaxis.items():
                output_file.write(f'Track {track} - X_f-X_i: {tactic_index}\n')

            output_file.write(f'\nTactic index = {final_ti}\n\n')

            analyze_tracks(tracked_data, output_file)
