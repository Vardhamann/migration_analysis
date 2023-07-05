import pandas as pd
import numpy as np

def calculate_tactic_index(data):

    # Initiate a counter
    tactic_indices = {}

    # Group the data by track number
    grouped_data = data.groupby('Track n°')

    # Loop through the tracks
    for track, track_data in grouped_data:
        #print(track_data['X'].iloc[0])
        # Calculate the distance between consecutive points
        dx = track_data['X'].iloc[-1] - track_data['X'].iloc[0]
        distances = (dx)
        print(dx)
        # Calculate the sum of forward distances and backward distances
        forward_sum = np.sum(distances[distances > 0])
        backward_sum = np.sum(distances[distances < 0])
        # print(forward_sum)
        # print(backward_sum)
        # Calculate the tactic index
        tactic_index = (forward_sum - backward_sum)/(forward_sum + backward_sum)

        # Store the tactic index for the current track number
        tactic_indices[track] = tactic_index
        #print(tactic_index)
    return tactic_indices

# Load the tracked data from a CSV file
tracked_data = pd.read_csv('./tracked_data.csv')

# Calculate the tactic index for each track number
tactic_indices = calculate_tactic_index(tracked_data)

# Print the tactic index for each track number
for track, tactic_index in tactic_indices.items():
    print(f'Track {track} - Tactic Index: {tactic_index}')
