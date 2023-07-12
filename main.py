import pandas as pd
import numpy as np
import os
import datetime

################ Defining Function ################

def calculate_final_xaxis_dist(data):

    # Initiate a counter
    final_distances_xaxis = {}

    # Group the data by track number
    grouped_data = data.groupby('Track no')

    # Loop through the tracks
    for track, track_data in grouped_data:

        # Calculate the distance between consecutive points
        dx = track_data['X'].iloc[26] - track_data['X'].iloc[0]

        final_distances_xaxis[track] = dx
        #print(dx)

    return final_distances_xaxis

def calc_tactic_index(data):

    # Extract the second column values
    second_column = [value for key, value in data.items()]

    forward_sum = sum(1 for x in second_column if x > 0)
    backward_sum = sum(1 for x in second_column if x < 0)

    # Calculate the tactic index
    tactic_index = (backward_sum - forward_sum)/(forward_sum + backward_sum)

    return tactic_index

def instant_velocity_cells(data):
    print('Average displacement of positive and negative steps of cells that have a positive xf-xi value\n')
    # Initiate a counter
    final_distances_xaxis = {}

    # Group the data by track number
    grouped_data = data.groupby('Track no')

    # Loop through the tracks
    for track, track_data in grouped_data:

        # Calculate the distance between consecutive points
        dx = track_data['X'].iloc[26] - track_data['X'].iloc[0]
        final_distances_xaxis[track] = dx

        if final_distances_xaxis[track] > 0:
            step_delta = np.diff(track_data['X'])
            #print(f"{track} is a positive cell with a step delta of {step_delta}")
            #defining variables to calculate average step distance (for both positive and negative.)
            total_positive_step_dist = 0
            total_negative_step_dist = 0
            average_positive_step_vel = 0
            average_negative_step_vel = 0
            no_of_positive_steps = 0
            no_of_negative_steps = 0

            # Counting the no of steps
            for step in step_delta:

                if step > 0:
                    #print(f'+ve step with a distance of {step} and the location of the step is {id(step_delta)}')
                    no_of_positive_steps += 1
                    total_positive_step_dist = total_positive_step_dist + step
                elif step < 0:
                    #print(f'-ve step with a distance of {step} and the location of the step is {id(step_delta)}')
                    no_of_negative_steps += 1
                    total_negative_step_dist = total_negative_step_dist + step
            average_positive_step_displacement = total_positive_step_dist / no_of_positive_steps
            average_negative_step_displacement = total_negative_step_dist / no_of_negative_steps
            print(f'track: {track},\n avg +ve step displacement = {average_positive_step_displacement}\n avg -ve step displacement = {average_negative_step_displacement}')
            output_file.write(f'track: {track},\n avg +ve step displacement = {average_positive_step_displacement}\n avg -ve step displacement = {average_negative_step_displacement} \n')
        elif final_distances_xaxis[track] < 0:
            # print(f"track {track} is a negative cell.")
            pass
        else:
            # print(f'track {track} is a cell zero final distance')
            pass
    return average_positive_step_displacement, average_negative_step_displacement


################ Code Begins Here ################

input_folder_path = './input_files/'  # Replace with the path to your folder

## to output files

# Get the current timestamp
current_time = datetime.datetime.now()

# Format the timestamp as part of the file name
file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.txt")

# Create the file path
output_file_path = './output_files/' + file_name  # Replace with the desired directory path


# Iterate over files in the folder and write to output folder
with open(output_file_path, 'w') as output_file:

    for filename in os.listdir(input_folder_path):

        file_path = os.path.join(input_folder_path, filename)

        if os.path.isfile(file_path) and filename.endswith('.csv'):
            # Process the file
            print(f'\n Processing file: {file_path}\n')
            output_file.write(f'\n Processing file: {file_path} \n \n .')
            # Add your code to handle the file here
            current_tracking_file = str(file_path)
            print(current_tracking_file)
            # Load the tracked data from a CSV file
            tracked_data = pd.read_csv(current_tracking_file)

            # Calculate the final distances for each track number
            final_distances_xaxis = calculate_final_xaxis_dist(tracked_data)
            # Calculate the Tactic index for 12 hour period
            final_ti = calc_tactic_index(final_distances_xaxis)

            # Print the final x distances for each track number
            print('Xf-Xi values for all tracks \n')
            output_file.write('Xf-Xi values for all tracks \n')
            for track, tactic_index in final_distances_xaxis.items():
                print(f'Track {track} - X_f-X_i: {tactic_index}')
                output_file.write(f'Track {track} - X_f-X_i: {tactic_index} \n')

            # Print the tactic index for each track number
            print(f'\nTactic index = {final_ti}\n')
            output_file.write(f'\nTactic index = {final_ti}\n')

            average_positive_step_displacement, average_negative_step_displacement = instant_velocity_cells(tracked_data)
