import os
import pandas as pd

def merge_csv_files_by_prefix(input_folder_path):
    data_dict = {}  # To store DataFrames grouped by the first 4 characters of file names
    track_offset_dict = {}  # To store the track number offset for each prefix group

    # Loop through all files in the folder
    for filename in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.csv'):
            # Get the first 4 characters of the file name as the prefix
            prefix = filename[:4]

            # Read the CSV file
            data = pd.read_csv(file_path)

            # Determine the track number offset for this prefix group
            track_offset = track_offset_dict.get(prefix, 0)

            # Update the "Track no" values based on the current track number
            data['Track no'] = data['Track no'] + track_offset

            # Append the DataFrame to the corresponding group in the dictionary
            if prefix in data_dict:
                data_dict[prefix].append(data)
            else:
                data_dict[prefix] = [data]

            # Update the track number offset for this prefix group
            track_offset_dict[prefix] = data['Track no'].max()

    # Merge DataFrames with common prefixes
    merged_data_by_prefix = {}
    for prefix, data_list in data_dict.items():
        # Concatenate DataFrames within each group into a single DataFrame
        merged_df = pd.concat(data_list, ignore_index=True)
        merged_data_by_prefix[prefix] = merged_df

        # Export the merged DataFrame to a separate CSV file
        output_file_path = os.path.join(output_folder_path, f'merged_data_{prefix}.csv')
        merged_df.to_csv(output_file_path, index=False)

    return merged_data_by_prefix

# Example usage:
input_folder_path = './input_files'
output_folder_path = './input_files_modified'
merged_data_by_prefix = merge_csv_files_by_prefix(input_folder_path)

# Now `merged_data_by_prefix` is a dictionary where each key corresponds to a common 4-character prefix
# and the value is the corresponding merged DataFrame with continuous indexing for each track.

# CSV files with merged data will be saved in the input_folder_path with names like "merged_data_prefix.csv".
