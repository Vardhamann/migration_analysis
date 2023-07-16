import pandas as pd
import numpy as np
import os
import datetime


def average_step_displacement(step_delta):
    positive_steps = [step for step in step_delta if step > 0]
    negative_steps = [step for step in step_delta if step < 0]
    avg_positive = sum(positive_steps) / len(positive_steps) if positive_steps else 0
    avg_negative = sum(negative_steps) / len(negative_steps) if negative_steps else 0
    num_positive = len(positive_steps)
    num_negative = len(negative_steps)
    return avg_positive, avg_negative, num_positive, num_negative


def calculate_velocity(displacement, time):
    return displacement / time


def calculate_track_length(x, y):
    distance = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
    return np.sum(distance)


def analyze_tracks(tracked_data, output_file):
    positive_avg_positive_step_displacements = []
    positive_avg_negative_step_displacements = []
    negative_avg_positive_step_displacements = []
    negative_avg_negative_step_displacements = []
    avg_positive_velocities = []
    avg_negative_velocities = []
    avg_positive_velocity_changes = []
    avg_negative_velocity_changes = []
    avg_positive_track_lengths = []
    avg_negative_track_lengths = []
    positive_cell_count = 0
    negative_cell_count = 0

    output_file.write('Individual Track Values:\n\n')

    for track, track_data in tracked_data.groupby('Track no'):
        final_x_axis_displacement = track_data['X'].iloc[26] - track_data['X'].iloc[0]
        step_delta = np.diff(track_data['X'])
        avg_positive_step_displacement, avg_negative_step_displacement, num_positive_steps, num_negative_steps = average_step_displacement(step_delta)

        velocity_change = np.diff(track_data['X'])
        velocity = calculate_velocity(final_x_axis_displacement, 12)  # Assuming 12 units of time

        x = track_data['X']
        y = track_data['Y']

        track_length = calculate_track_length(x, y)

        output_file.write(f'Track: {track}\n')
        output_file.write(f'  Xf-Xi: {final_x_axis_displacement}\n')
        output_file.write(f'  Average +ve Step Displacement: {avg_positive_step_displacement}\n')
        output_file.write(f'  Average -ve Step Displacement: {avg_negative_step_displacement}\n')
        output_file.write(f'  Number of +ve Steps: {num_positive_steps}\n')
        output_file.write(f'  Number of -ve Steps: {num_negative_steps}\n')
        output_file.write(f'  Velocity: {velocity}\n')
        output_file.write(f'  Velocity Change: {velocity_change}\n')
        output_file.write(f'  Track Length: {track_length}\n\n')

        # Categorize the values based on displacement sign
        if final_x_axis_displacement > 0:
            positive_avg_positive_step_displacements.append(avg_positive_step_displacement)
            positive_avg_negative_step_displacements.append(avg_negative_step_displacement)
            avg_positive_velocities.append(velocity)
            avg_positive_velocity_changes.extend(velocity_change)
            avg_positive_track_lengths.append(track_length)
            positive_cell_count += 1
        elif final_x_axis_displacement < 0:
            negative_avg_positive_step_displacements.append(avg_positive_step_displacement)
            negative_avg_negative_step_displacements.append(avg_negative_step_displacement)
            avg_negative_velocities.append(velocity)
            avg_negative_velocity_changes.extend(velocity_change)
            avg_negative_track_lengths.append(track_length)
            negative_cell_count += 1

    positive_avg_positive_step_displacement = np.mean(positive_avg_positive_step_displacements)
    positive_avg_negative_step_displacement = np.mean(positive_avg_negative_step_displacements)
    negative_avg_positive_step_displacement = np.mean(negative_avg_positive_step_displacements)
    negative_avg_negative_step_displacement = np.mean(negative_avg_negative_step_displacements)
    avg_positive_velocity = np.mean(avg_positive_velocities)
    avg_negative_velocity = np.mean(avg_negative_velocities)
    avg_positive_velocity_change = np.mean(avg_positive_velocity_changes)
    avg_negative_velocity_change = np.mean(avg_negative_velocity_changes)
    avg_positive_track_length = np.mean(avg_positive_track_lengths)
    avg_negative_track_length = np.mean(avg_negative_track_lengths)
    final_tactic_index = (negative_cell_count - positive_cell_count)/(negative_cell_count + positive_cell_count)

    output_file.write('Average Values:\n\n')
    output_file.write(f'Number of Positive Cells: {positive_cell_count}\n')
    output_file.write(f'Number of Negative Cells: {negative_cell_count}\n')
    output_file.write(f'Tactic index = {final_tactic_index}\n\n')
    output_file.write(f'Average +ve Step Displacement (Positive DX): {positive_avg_positive_step_displacement}\n')
    output_file.write(f'Average -ve Step Displacement (Positive DX): {positive_avg_negative_step_displacement}\n')
    output_file.write(f'Average +ve Step Displacement (Negative DX): {negative_avg_positive_step_displacement}\n')
    output_file.write(f'Average -ve Step Displacement (Negative DX): {negative_avg_negative_step_displacement}\n')
    output_file.write(f'Average +ve Velocity: {avg_positive_velocity}\n')
    output_file.write(f'Average -ve Velocity: {avg_negative_velocity}\n')
    output_file.write(f'Average +ve Velocity Change: {avg_positive_velocity_change}\n')
    output_file.write(f'Average -ve Velocity Change: {avg_negative_velocity_change}\n')
    output_file.write(f'Average +ve Track Length: {avg_positive_track_length}\n')
    output_file.write(f'Average -ve Track Length: {avg_negative_track_length}\n')


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
            analyze_tracks(tracked_data, output_file)
