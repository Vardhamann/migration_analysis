import numpy as np
import os
import datetime
import plotly.figure_factory as ff
import pandas as pd


input_folder_path = './input_files/'  # Replace with the path to your folder
output_folder_path = './output_plots/'  # Replace with the path to your output folder

# Get the current time as a datetime object
current_time = datetime.datetime.now()

# Format the current time as a string
current_time_str = current_time.strftime("%Y-%m-%d_%H-%M")

# Create a directory with the current time as the folder name
folder_name = os.path.join(output_folder_path, current_time_str)

def make_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")
    return None

def plot_function(positive_cell_steps, negative_cell_steps):
    group_labels = ['Positive cells', 'Negative cells']
    colors = ['purple', 'red']

    # Create distplot with curve_type set to 'normal'
    fig = ff.create_distplot([positive_cell_steps, negative_cell_steps], group_labels, bin_size=2,
                             curve_type='normal', # override default 'kde'
                             colors=colors, show_rug =False)

    # Add title
    fig.update_layout(title_text='Distribution of step size of positive and negative cells',
                      xaxis_title="Step size in pixels",
                      yaxis_title="",
                      legend_title="Legend"
                      )
    fig.show()
    return None

def step_displacement_counter(tracked_data):
    positive_cell_steps = []  # Initialize an empty list to store positive step deltas
    negative_cell_steps = []  # Initialize an empty list to store negative step deltas

    for track, track_data in tracked_data.groupby('Track no'):
        final_x_axis_displacement = track_data['X'].iloc[26] - track_data['X'].iloc[0]  # Use -1 instead of 26 for the last element
        step_delta = np.diff(track_data['X'][:26])

        if final_x_axis_displacement > 0:
            positive_cell_steps.append(step_delta)  # Use positive_cell_steps instead of positive_cell_steps
        elif final_x_axis_displacement < 0:
            negative_cell_steps.append(step_delta)

    # Convert the lists to arrays if needed
    positive_cell_steps = np.vstack(positive_cell_steps) if positive_cell_steps else None
    negative_cell_steps = np.vstack(negative_cell_steps) if negative_cell_steps else None
    return positive_cell_steps, negative_cell_steps

positive_cell_steps_all = []
negative_cell_steps_all = []
for filename in os.listdir(input_folder_path):
    file_path = os.path.join(input_folder_path, filename)
    if os.path.isfile(file_path) and filename.endswith('.csv'):
        tracked_data = pd.read_csv(file_path)
        positive_cell_steps, negative_cell_steps = step_displacement_counter(tracked_data)
        positive_cell_steps_all.append(positive_cell_steps)
        negative_cell_steps_all.append(negative_cell_steps)

# Convert the lists to NumPy arrays after the loop
positive_cell_steps_all = np.vstack(positive_cell_steps_all)
negative_cell_steps_all = np.vstack(negative_cell_steps_all)

positive_counts = positive_cell_steps_all.flatten()
negative_counts = negative_cell_steps_all.flatten()
plot_function(positive_counts, negative_counts)
