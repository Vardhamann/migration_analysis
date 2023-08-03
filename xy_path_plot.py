import numpy as np
import os
import plotly.graph_objects as go
import pandas as pd

input_folder_path = './input_files_modified/'

def plot_relative_position(df, file_identifier):
    fig = go.Figure()

    # Calculate average X and Y positions for positive, negative, and no movement cells at each slice number
    avg_positions = df.groupby(['Slice no', 'Cell Type']).agg({'Relative X Position': 'mean', 'Relative Y Position': 'mean'})

    # Individual tracks in grey color
    for track_no, group_df in df.groupby('Track no'):
        fig.add_trace(go.Scatter(x=group_df['Relative X Position'], y=group_df['Relative Y Position'], mode='lines', line=dict(color='lightgrey'), showlegend=False))

    # Add average lines for each cell type
    if ('Positive' in avg_positions.index.get_level_values('Cell Type')):
        fig.add_trace(go.Scatter(x=avg_positions.loc[(slice(None), 'Positive'), 'Relative X Position'], y=avg_positions.loc[(slice(None), 'Positive'), 'Relative Y Position'], mode='lines', name='Avg Positive', line=dict(color='green')))
    if ('Negative' in avg_positions.index.get_level_values('Cell Type')):
        fig.add_trace(go.Scatter(x=avg_positions.loc[(slice(None), 'Negative'), 'Relative X Position'], y=avg_positions.loc[(slice(None), 'Negative'), 'Relative Y Position'], mode='lines', name='Avg Negative', line=dict(color='red')))
    if ('No movement' in avg_positions.index.get_level_values('Cell Type')):
        fig.add_trace(go.Scatter(x=avg_positions.loc[(slice(None), 'No movement'), 'Relative X Position'], y=avg_positions.loc[(slice(None), 'No movement'), 'Relative Y Position'], mode='lines', name='Avg No movement', line=dict(color='blue')))

    # Find the maximum absolute value among X and Y positions
    max_abs_value = max(abs(df['Relative X Position'].max()), abs(df['Relative X Position'].min()),
                        abs(df['Relative Y Position'].max()), abs(df['Relative Y Position'].min()))

    # Set the range of both X and Y axes to be the same
    fig.update_layout(
        title_text=f'Relative Y Position vs. Relative X Position (Experiment {file_identifier})',
        xaxis_title="Relative X Position",
        yaxis_title="Relative Y Position",
        xaxis_range=[-max_abs_value, max_abs_value],
        yaxis_range=[-max_abs_value, max_abs_value],
    )

    fig.show()

def calculate_cell_type(x_values):
    final_x_axis_displacement = x_values.iloc[-1] - x_values.iloc[0]
    return 'Positive' if final_x_axis_displacement > 0 else ('Negative' if final_x_axis_displacement < 0 else 'No movement')

def process_single_track_data(track_data):
    track_data = track_data[:26].copy()

    # Calculate 'Relative X Position' and 'Relative Y Position' columns
    initial_x_position = track_data['X'].iloc[0]
    initial_y_position = track_data['Y'].iloc[0]
    track_data['Relative X Position'] = track_data['X'] - initial_x_position
    track_data['Relative Y Position'] = track_data['Y'] - initial_y_position

    track_data['Cell Type'] = track_data.groupby('Track no')['X'].transform(calculate_cell_type)
    return track_data

def step_displacement_counter(tracked_data):
    results_df = pd.concat([process_single_track_data(track_data) for _, track_data in tracked_data.groupby('Track no')])
    return results_df

def read_and_process_files(input_folder_path):
    all_data = []
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            try:
                file_identifier = os.path.splitext(filename)[0][-1]
                tracked_data = pd.read_csv(file_path)
                result_df = step_displacement_counter(tracked_data)
                plot_relative_position(result_df, file_identifier)
                all_data.append(result_df)
            except pd.errors.EmptyDataError:
                print(f"Error: File '{file_path}' is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to parse file '{file_path}'. Invalid CSV format.")
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

final_df = read_and_process_files(input_folder_path)
