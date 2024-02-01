import pandas as pd
import numpy as np
import csv

# Read timestamp file
timestamp_df = pd.read_csv('processed_timestamp_files/018.csv')

# Read data file (a CSV with the first column representing time in seconds)
data_df = pd.read_csv(
    'oxydeoxy_DataColumnsWithTime/018data.csv', header=None)

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

        # # Get the number of columns in the chunk of data
        # column_count = len(extracted_data[0])

        # Update pointers for the next iteration
        start_pointer = end_pointer + 1

        # Append time range, duration, and data to the list
        output_data.append({
            'Time Range': f'{start_time} to {end_time}, Duration {duration}',
            # 'Column Count': column_count,
            'Data': extracted_data
        })
'''
# Write the output to a CSV file
with open('splitted_data_001.csv', 'w') as f:
    for entry in output_data:
        f.write(f"{entry['Time Range']}\n{entry['Data']}\n\n")
'''

# Convert the list of dictionaries to a NumPy object array
output_array = np.empty(len(output_data), dtype=object)
output_array[:] = output_data
'''
# Accessing data from the NumPy object array
# Access the first 5 rows of the first chunk/entry's data and print each row
specified_rows_data = output_array[0]['Data'][:5]

for row in specified_rows_data:
    print(row, "\n")
'''

filename = '018meanValues.csv'

# Open the file in write mode
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)

    # Iterate through each entry in the output array
    for entry in output_array:
        data_array = np.array(entry['Data'])
        mean_values = np.mean(data_array[:, 1:], axis=0, keepdims=True)
        mean_values_size = mean_values.shape

        # Write the time range and mean values to the CSV file
        writer.writerow([f"Time Range: {entry['Time Range']}"])
        writer.writerow(["Mean Values:"])
        writer.writerows(mean_values)
        writer.writerow([f"Size of mean_values: {mean_values_size}"])
        writer.writerow([])  # Add an empty row for better readability

'''
# Calculate the mean of each column in each entry
for entry in output_array:
    data_array = np.array(entry['Data'])
    # Add keepdims=True
    mean_values = np.mean(data_array[:, 1:], axis=0, keepdims=True)

    # Get the size of mean_values
    mean_values_size = mean_values.shape

    print(f"Time Range: {entry['Time Range']}")
    print("Mean Values:")
    print(mean_values)
    print(f"Size of mean_values: {mean_values_size}")
    print()
'''
