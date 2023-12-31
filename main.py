import pandas as pd
import numpy as np
import os
import datetime
import math
from scipy import stats

# function definitions

def average_step_displacement(x):
    step_delta = np.diff(x)
    positive_steps = [step for step in step_delta if step > 0] #count number of positive steps
    negative_steps = [step for step in step_delta if step < 0] #count number of negative steps
    avg_positive = sum(positive_steps) / len(positive_steps) if positive_steps else 0
    avg_negative = sum(negative_steps) / len(negative_steps) if negative_steps else 0
    num_positive = len(positive_steps)
    num_negative = len(negative_steps)
    return avg_positive, avg_negative, num_positive, num_negative


def calculate_velocity(x, y, time):
    x_diplacement = x.iloc[26] - x.iloc[0]
    y_diplacement = y.iloc[26] - y.iloc[0]
    x_sign = math.copysign(1, x_diplacement)
    y_sign = math.copysign(1, y_diplacement)
    velocity_x = x_diplacement / time
    velocity_y = y_diplacement / time
    velocity = math.sqrt(velocity_x ** 2 + velocity_y ** 2)
    velocity_direction = (velocity, x_sign, y_sign)
    return velocity_direction

def calculate_speed(x, y, time):
    total_distance = np.sum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
    return total_distance / time

def calculate_x_axis_velocity(x, time):
    velocity = (x.iloc[26] - x.iloc[0])/time
    return velocity

def calculate_x_axis_speed(x, time):
    distance = np.sum(np.sqrt(np.diff(x) ** 2))
    speed = distance /time
    return speed

def calculate_track_length_distance(x, y):
    distance = np.sum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
    return np.sum(distance)

def calculate_track_length_displacement(x, y):
    distance = np.sqrt((x.iloc[26]-x.iloc[0]) ** 2 + (y.iloc[26]-y.iloc[0]) ** 2)
    return np.sum(distance)

def calculate_track_length_distance_x(x):
    distance = np.sqrt(np.diff(x) ** 2)
    return np.sum(distance)

def calculate_track_length_displacement_x(x):
    displacement = x.iloc[26]-x.iloc[0]
    return displacement

def calculate_persistence(vel,speed):
    persistence = vel/speed
    return persistence


def analyze_tracks(tracked_data, output_file):
    positive_avg_positive_step_displacements = []
    positive_avg_negative_step_displacements = []
    negative_avg_positive_step_displacements = []
    negative_avg_negative_step_displacements = []
    avg_positive_velocities = []
    avg_negative_velocities = []
    avg_positive_speeds = []
    avg_negative_speeds = []
    avg_positive_track_lengths_displacement = []
    avg_negative_track_lengths_displacement = []
    avg_positive_track_lengths_distance = []
    avg_negative_track_lengths_distance = []
    avg_positive_persistances_x_axis = []
    avg_negative_persistances_x_axis = []
    positive_cell_count = 0
    negative_cell_count = 0

    output_file.write('Individual Track Values:\n\n')

    for track, track_data in tracked_data.groupby('Track no'):
        #print(track)
        x = track_data['X']
        y = track_data['Y']
        final_x_axis_displacement = track_data['X'].iloc[26] - track_data['X'].iloc[0] # to evaluate which cells are positive vs negative
        #print(final_x_axis_displacement)

        avg_positive_step_displacement, avg_negative_step_displacement, num_positive_steps, num_negative_steps = average_step_displacement(x)

        # Calculate total Velocity and Speed
        velocity = calculate_velocity(x, y, 13)  # Assuming 13 units of time
        speed = calculate_speed(x, y, 13)  # Assuming 13 units of time

        # Calculate X-axis Velocity and Speed
        x_axis_velocity = calculate_x_axis_velocity(x, 13)  # Assuming 13 units of time
        x_axis_speed = calculate_x_axis_speed(x, 13)  # Assuming 13 units of time

        track_length_distance = calculate_track_length_distance(x, y)
        track_length_displacement = calculate_track_length_displacement(x, y)
        track_length_distance_x = calculate_track_length_distance_x(x)
        track_length_displacement_x = calculate_track_length_displacement_x(x)

        # Calculate Persistence
        persistence_xy = calculate_persistence(velocity[0], speed)
        persistence_x = calculate_persistence(x_axis_velocity, x_axis_speed)

        # output_file.write(f'Track: {track}\n')
        # output_file.write(f'  Xf-Xi: {final_x_axis_displacement}\n')
        # output_file.write(f'  Average +ve Step Displacement: {avg_positive_step_displacement}\n')
        # output_file.write(f'  Average -ve Step Displacement: {avg_negative_step_displacement}\n')
        # output_file.write(f'  Number of +ve Steps: {num_positive_steps}\n')
        # output_file.write(f'  Number of -ve Steps: {num_negative_steps}\n')
        # output_file.write(f'  Velocity: {velocity}\n')
        # output_file.write(f'  Speed: {speed}\n')
        # output_file.write(f'  X-axis Velocity: {x_axis_velocity}\n')
        # output_file.write(f'  X-axis Speed: {x_axis_speed}\n')
        # output_file.write(f'  Persistence (X&Y): {persistence_xy}\n')
        # output_file.write(f'  Persistence (X): {persistence_x}\n')
        # output_file.write(f'  Track Length(distance): {track_length_distance}\n')
        # output_file.write(f'  Track Length(displacement): {track_length_displacement}\n')
        # output_file.write(f'  Track Length(distance) X axis: {track_length_distance_x}\n')
        # output_file.write(f'  Track Length(displacement) X axis: {track_length_displacement_x}\n\n')

        # Categorize the values based on displacement sign
        if final_x_axis_displacement > 0:
            positive_avg_positive_step_displacements.append(avg_positive_step_displacement)
            positive_avg_negative_step_displacements.append(avg_negative_step_displacement)
            avg_positive_track_lengths_displacement.append(track_length_displacement_x)
            avg_positive_track_lengths_distance.append(track_length_distance_x)
            avg_positive_persistances_x_axis.append(persistence_x)
            avg_positive_velocities.append(x_axis_velocity)
            avg_positive_speeds.append(x_axis_speed)
            positive_cell_count += 1
        elif final_x_axis_displacement < 0:
            negative_avg_positive_step_displacements.append(avg_positive_step_displacement)
            negative_avg_negative_step_displacements.append(avg_negative_step_displacement)
            avg_negative_track_lengths_displacement.append(track_length_displacement_x)
            avg_negative_track_lengths_distance.append(track_length_distance_x)
            avg_negative_persistances_x_axis.append(persistence_x)
            avg_negative_velocities.append(x_axis_velocity)
            avg_negative_speeds.append(x_axis_speed)
            negative_cell_count += 1

    positive_avg_positive_step_displacement = np.mean(positive_avg_positive_step_displacements)
    positive_avg_negative_step_displacement = np.mean(positive_avg_negative_step_displacements)
    negative_avg_positive_step_displacement = np.mean(negative_avg_positive_step_displacements)
    negative_avg_negative_step_displacement = np.mean(negative_avg_negative_step_displacements)
    avg_positive_velocity = np.mean(avg_positive_velocities)
    avg_negative_velocity = np.mean(avg_negative_velocities)
    avg_positive_speed = np.mean(avg_positive_speeds)
    avg_negative_speed = np.mean(avg_negative_speeds)
    avg_positive_track_length_displacement = np.mean(avg_positive_track_lengths_displacement)
    avg_negative_track_length_displacement = np.mean(avg_negative_track_lengths_displacement)
    avg_positive_track_length_distance = np.mean(avg_positive_track_lengths_distance)
    avg_negative_track_length_distance = np.mean(avg_negative_track_lengths_distance)
    avg_positive_persistance_x_axis = np.mean(avg_positive_persistances_x_axis)
    avg_negative_persistance_x_axis = np.mean(avg_negative_persistances_x_axis)
    final_tactic_index = (negative_cell_count - positive_cell_count) / (negative_cell_count + positive_cell_count)

    output_file.write('Average Values:\n\n')
    output_file.write(f'Number of Positive Cells: {positive_cell_count}\n')
    output_file.write(f'Number of Negative Cells: {negative_cell_count}\n')
    output_file.write(f'Tactic index = {final_tactic_index}\n\n')
    output_file.write(f'Positive cells\n')
    output_file.write(f'Average +ve Step Displacement: {positive_avg_positive_step_displacement}\n')
    output_file.write(f'Average -ve Step Displacement: {positive_avg_negative_step_displacement}\n')
    output_file.write(f'Average X axis Velocity: {avg_positive_velocity}\n')
    output_file.write(f'Average X axis Speed: {avg_positive_speed}\n')
    output_file.write(f'Average persistence in x axis: {avg_positive_persistance_x_axis} \n')
    output_file.write(f'Average Track Length X axis (displacement): {avg_positive_track_length_displacement}\n')
    output_file.write(f'Average Track Length X axis (distance): {avg_positive_track_length_distance}\n\n')
    output_file.write(f'Negative cells\n')
    output_file.write(f'Average +ve Step Displacement: {negative_avg_positive_step_displacement}\n')
    output_file.write(f'Average -ve Step Displacement: {negative_avg_negative_step_displacement}\n')
    output_file.write(f'Average X axis Velocity: {avg_negative_velocity}\n')
    output_file.write(f'Average X axis Speed: {avg_negative_speed}\n')
    output_file.write(f'Average persistence in x axis: {avg_negative_persistance_x_axis} \n')
    output_file.write(f'Average Track Length X axis (displacement): {avg_negative_track_length_displacement}\n')
    output_file.write(f'Average Track Length X axis (distance): {avg_negative_track_length_distance}\n\n')


    t_statistic, p_value = stats.ttest_ind(avg_positive_velocities, avg_negative_velocities)
    output_file.write(f'T-test comparing velocities of the two populations:\n')
    output_file.write(f'T value: {t_statistic}, P value {p_value}\n\n')

    t_statistic, p_value = stats.ttest_ind(positive_avg_positive_step_displacements, negative_avg_positive_step_displacements)
    output_file.write(f'T-test comparing the positive steps of the two populations:\n')
    output_file.write(f'T value: {t_statistic}, P value {p_value}\n\n')

    t_statistic, p_value = stats.ttest_ind(positive_avg_negative_step_displacements, negative_avg_negative_step_displacements)
    output_file.write(f'T-test comparing the negative steps of the two populations:\n')
    output_file.write(f'T value: {t_statistic}, P value {p_value}\n\n')


def calculate_tactic_index_over_time(tracked_data):
    tactic_index_overtime = []
    for i in range(1, 27, 1):
        positive_cell_count = 0
        negative_cell_count = 0
        for track, track_data in tracked_data.groupby('Track no'):
            instant_x_axis_displacement = track_data['X'].iloc[i] - track_data['X'].iloc[0]
            # Categorize the values based on displacement sign
            if instant_x_axis_displacement > 0:
                positive_cell_count += 1
            elif instant_x_axis_displacement < 0:
                negative_cell_count += 1
        print(positive_cell_count, negative_cell_count)
        tactic_index_inst = (negative_cell_count - positive_cell_count) / (negative_cell_count + positive_cell_count)
        tactic_index_overtime.append(tactic_index_inst)
    #print(tactic_index_overtime)

    return tactic_index_overtime


input_folder_path = './input_files_modified/'  # Replace with the path to your folder
output_folder_path = './output_files/'  # Replace with the path to your output folder

current_time = datetime.datetime.now()
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S_iter2.txt")
output_file_path = os.path.join(output_folder_path, file_name)

with open(output_file_path, 'w') as output_file:
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)

        if os.path.isfile(file_path) and filename.endswith('.csv'):
            output_file.write(f'\nProcessing file: {file_path}\n\n')
            print(f'\nProcessing file: {file_path}\n\n')
            tracked_data = pd.read_csv(file_path)
            analyze_tracks(tracked_data, output_file)

            ## add one more loop to have tracks only
            tactic_index_values = calculate_tactic_index_over_time(tracked_data)
            output_file.write(f'Tactic Index Over Time:\n {tactic_index_values}\n\n')
            # for i, tactic_index in enumerate(tactic_index_values):
            #     output_file.write(f'Time Step {i+1}: {tactic_index}\n')
