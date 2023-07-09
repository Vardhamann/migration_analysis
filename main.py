import pandas as pd
import numpy as np

def calculate_final_xaxis_dist(data):

    # Initiate a counter
    final_distances_xaxis = {}

    # Group the data by track number
    grouped_data = data.groupby('Track n°')

    # Loop through the tracks
    for track, track_data in grouped_data:

        # Calculate the distance between consecutive points
        dx = track_data['X'].iloc[23] - track_data['X'].iloc[0]

        final_distances_xaxis[track] = dx
        #print(dx)

    return final_distances_xaxis

def calc_tactic_index(data):

    # Extract the second column values
    second_column = [value for key, value in data.items()]

    forward_sum = sum(1 for x in second_column if x > 0)
    backward_sum = sum(1 for x in second_column if x < 0)

    # Calculate the tactic index
    tactic_index = (forward_sum - backward_sum)/(forward_sum + backward_sum)

    return tactic_index

# Load the tracked data from a CSV file
tracked_data = pd.read_csv('./tracked_data.csv')

# Calculate the final distances for each track number
final_distances_xaxis = calculate_final_xaxis_dist(tracked_data)
# Calculate the Tactic index for 12 hour period
final_ti = calc_tactic_index(final_distances_xaxis)

# Print the final x distances for each track number
for track, tactic_index in final_distances_xaxis.items():
    print(f'Track {track} - X_f-X_i: {tactic_index}')

# Print the tactic index for each track number
print(f'Tactic index = {final_ti}')
