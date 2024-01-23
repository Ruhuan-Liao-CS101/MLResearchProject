import pandas as pd
import numpy as np

# Read timestamp file
timestamp_df = pd.read_csv('processed_timestamp_files/001.csv')

# Read data file (a CSV with the first column representing time in seconds)
data_df = pd.read_csv(
    'merged_time_data_files/merged_file_001.csv', header=None)

# Create an empty list to store the chunks of data
output_data = []

# Initialize pointers
start_pointer = 0
end_pointer = 0

# Iterate through rows in the timestamp file
for index, row in timestamp_df.iterrows():
    pair_status = row['PairStatus']

    # Check if PairStatus is 'Paired'
    if pair_status == 'Paired':
        start_time = row['StartTime']
        end_time = row['EndTime']
        duration = row['Duration']

        # Calculate end pointer based on duration
        end_pointer = start_pointer + int(duration * 4)

        # Extract data based on pointers
        # Include the end_pointer row
        extracted_data = data_df.iloc[start_pointer:end_pointer +
                                      1].values.tolist()

        # Update pointers for the next iteration
        start_pointer = end_pointer + 1

        # Append time range, duration, and data to the list
        output_data.append({
            'Time Range': f'{start_time} to {end_time}, Duration {duration}',
            'Data': extracted_data
        })

# # Write the output to a CSV file
# with open('splitted_data_001.csv', 'w') as f:
#     for entry in output_data:
#         f.write(f"{entry['Time Range']}\n{entry['Data']}\n\n")

# Convert the list of dictionaries to a NumPy object array
output_array = np.empty(len(output_data), dtype=object)
output_array[:] = output_data

# Accessing data from the NumPy object array
# Access the first 5 rows of the first entry's data and print each row
specified_rows_data = output_array[2]['Data'][:5]

for row in specified_rows_data:
    print(row, "\n")
