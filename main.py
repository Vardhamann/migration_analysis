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


input_folder_path = './input_files/'  # Replace with the path to your folder
output_folder_path = './output_files/'  # Replace with the path to your output folder

current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.txt")
output_file_path = os.path.join(output_folder_path, file_name)

with open(output_file_path, 'w') as output_file:
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)

        if os.path.isfile(file_path) and filename.endswith('.csv'):
            print(f'\nProcessing file: {file_path}\n')
            output_file.write(f'\nProcessing file: {file_path}\n\n')

            tracked_data = pd.read_csv(file_path)
            final_distances_xaxis = calculate_final_xaxis_dist(tracked_data)
            final_ti = calc_tactic_index(final_distances_xaxis)

            print('Xf-Xi values for all tracks\n')
            output_file.write('Xf-Xi values for all tracks\n')
            for track, tactic_index in final_distances_xaxis.items():
                print(f'Track {track} - X_f-X_i: {tactic_index}')
                output_file.write(f'Track {track} - X_f-X_i: {tactic_index}\n')

            print(f'\nTactic index = {final_ti}\n')
            output_file.write(f'\nTactic index = {final_ti}\n')

            grouped_data = tracked_data.groupby('Track no')
            for track, track_data in grouped_data:
                dx = track_data['X'].iloc[26] - track_data['X'].iloc[0]
                if dx > 0:
                    step_delta = np.diff(track_data['X'])
                    avg_positive_step_displacement, avg_negative_step_displacement = average_step_displacement(step_delta)
                    print(f'track: {track},\n avg +ve step displacement = {avg_positive_step_displacement}\n avg -ve step displacement = {avg_negative_step_displacement}')
                    output_file.write(f'track: {track},\n avg +ve step displacement = {avg_positive_step_displacement}\n avg -ve step displacement = {avg_negative_step_displacement}\n')
