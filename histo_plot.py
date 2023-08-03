import numpy as np
import os
import plotly.express as px
import pandas as pd

input_folder_path = './input_files_modified/'  # Replace with the path to your folder

def plot_step_distance_histogram(df, file_identifier):
    color_map = {'Positive': 'green', 'Negative': 'red', 'No movement': 'blue'}
    fig = px.histogram(df, x="Step Distance", color="Cell Type",
                       histfunc='count',
                       color_discrete_map=color_map,  # Set colors for each category
                       marginal="box",
                       hover_data=df.columns, opacity=0.4)

    fig.update_layout(
        title_text=f'Step Distance Histogram by Cell Type (Experiment {file_identifier})',
        xaxis_title="Step Distance in pixels",
        yaxis_title="Frequency (Count)",
        legend_title="Cell Type",
        barmode='overlay'
    )

    fig.show()

def calculate_cell_type(x_values):
    final_x_axis_displacement = x_values.iloc[-1] - x_values.iloc[0]
    return 'Positive' if final_x_axis_displacement > 0 else ('Negative' if final_x_axis_displacement < 0 else 'No movement')

def calculate_step_distances(x_values):
    return np.diff(x_values)

def process_single_track_data(track_data):
    cell_type = calculate_cell_type(track_data['X'][:26])
    step_distances = calculate_step_distances(track_data['X'][:26])
    return pd.DataFrame({'Step Distance': step_distances, 'Cell Type': cell_type})

def step_displacement_counter(tracked_data):
    results_df = pd.concat([process_single_track_data(track_data) for track, track_data in tracked_data.groupby('Track no')])
    return results_df

def read_and_process_files(input_folder_path):
    all_data = []
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            try:
                file_identifier = filename[-5]  # Assuming the unique identifier is the last character before ".csv"
                tracked_data = pd.read_csv(file_path)
                result_df = step_displacement_counter(tracked_data)
                print(result_df)
                plot_step_distance_histogram(result_df, file_identifier)
                all_data.append(result_df)
            except pd.errors.EmptyDataError:
                print(f"Error: File '{file_path}' is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to parse file '{file_path}'. Invalid CSV format.")
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

final_df = read_and_process_files(input_folder_path)
