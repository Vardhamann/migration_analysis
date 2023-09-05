import numpy as np
import os
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt

input_folder_path = './input_files_modified/'  # Replace with the path to your folder

def plot_relative_x_position(df, file_identifier):
    fig = go.Figure()

    # Individual tracks in grey color
    for track_no, group_df in df.groupby('Track no'):
        fig.add_trace(go.Scatter(x=group_df['Slice no'], y=group_df['Relative X Position'], mode='lines', line=dict(color='lightgrey'), showlegend=False))


    # Calculate average lines for positive, negative, and no movement cells
    avg_positive = df[df['Cell Type'] == 'Positive'].groupby('Slice no')['Relative X Position'].mean()
    avg_negative = df[df['Cell Type'] == 'Negative'].groupby('Slice no')['Relative X Position'].mean()
    avg_no_movement = df[df['Cell Type'] == 'No movement'].groupby('Slice no')['Relative X Position'].mean()

    fig.add_trace(go.Scatter(x=avg_positive.index, y=avg_positive, mode='lines', name='Avg Positive', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=avg_negative.index, y=avg_negative, mode='lines', name='Avg Negative', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=avg_no_movement.index, y=avg_no_movement, mode='lines', name='Avg No movement', line=dict(color='blue')))


    fig.update_layout(
        title_text=f'Relative X Position vs. Slice no. (Experiment {file_identifier})',
        xaxis_title="Slice no.",
        yaxis_title="Relative X Position",
    )

    fig.show()


def plot_relative_x_position_matplotlib(df, file_identifier):
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as per your preference

    # Plot individual tracks in grey color without legend
    for track_no, group_df in df.groupby('Track no'):
        print(group_df['Slice no'])
        ax.plot(group_df['Slice no'], group_df['Relative X Position'], color='lightgrey', alpha = 0.4)

    # Calculate average lines for positive, negative, and no movement cells
    avg_positive = df[df['Cell Type'] == 'Positive'].groupby('Slice no')['Relative X Position'].mean()
    avg_negative = df[df['Cell Type'] == 'Negative'].groupby('Slice no')['Relative X Position'].mean()
    avg_no_movement = df[df['Cell Type'] == 'No movement'].groupby('Slice no')['Relative X Position'].mean()

    # Plot average lines with legend
    ax.plot(avg_positive.index, avg_positive, color='green', label='Avg Positive')
    ax.plot(avg_negative.index, avg_negative, color='red', label='Avg Negative')
    ax.plot(avg_no_movement.index, avg_no_movement, color='blue', label='Avg No movement')

    ax.set_title(f'Relative X Position vs. Slice no. (Experiment {file_identifier})')
    ax.set_xlabel('Slice no.')
    ax.set_ylabel('Relative X Position')
    ax.grid(True)  # Add gridlines
    ax.set_yscale('symlog')  # Set y-axis to symlog scale

    # Move the legend outside the plot to the right (x=1.02) and center vertically (y=0.5)
    ax.legend(bbox_to_anchor=(1.02, 0.5), loc='center left')

    plt.tight_layout()  # Ensure the plot elements fit within the figure area
    plt.show()


def calculate_cell_type(x_values):
    final_x_axis_displacement = x_values.iloc[-1] - x_values.iloc[0]
    return 'Positive' if final_x_axis_displacement > 0 else ('Negative' if final_x_axis_displacement < 0 else 'No movement')

def calculate_step_distances(x_values):
    return np.diff(x_values)


def process_single_track_data(track_data):
    track_data = track_data[:26]
    cell_type = calculate_cell_type(track_data['X'])

    # Add 'Cell Type'
    track_data['Cell Type'] = cell_type

    # Calculate 'Relative X Position' column
    initial_x_position = track_data['X'].iloc[0]
    track_data['Relative X Position'] = track_data['X'] - initial_x_position

    return track_data

def normalize_x_position(track_data):

    return track_data

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
                #plot_relative_x_position_matplotlib(result_df, file_identifier)
                plot_relative_x_position(result_df, file_identifier)
                all_data.append(result_df)
            except pd.errors.EmptyDataError:
                print(f"Error: File '{file_path}' is empty.")
            except pd.errors.ParserError:
                print(f"Error: Unable to parse file '{file_path}'. Invalid CSV format.")
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

final_df = read_and_process_files(input_folder_path)
