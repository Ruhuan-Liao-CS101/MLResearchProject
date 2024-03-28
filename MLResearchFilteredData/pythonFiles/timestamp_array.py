import numpy as np

# Read the merged data file
with open('combined_data_files/timestamp_mean_std_curtosis_labels.csv', 'r') as file:
    lines = file.readlines()

# Initialize a list to store data columns by timestamps
timestamp_data = []

# Process each line
for line in lines:
    parts = line.strip().split(',')
    timestamp = parts[0]
    data_values = parts[1:]
    # print("Timestamp:", timestamp)
    # print("Data values:", data_values)

    # Append data values to the list
    timestamp_data.append(data_values)

timestamp_index = 1334  # Example timestamp index
column_index = 0  # Example column index

# Get the row and column range
column_size = timestamp_data[timestamp_index]
print(f"Row Number Range: {len(timestamp_data)-1}")
print(f"Column Number Range: {len(column_size)-1}")

# Access data at timestamp index and column index
data_at_index = timestamp_data[timestamp_index][column_index]

print(
    f"Data at timestamp index {timestamp_index} and column index {column_index}: {data_at_index}")
