import pandas as pd
import numpy as np
import csv

# Read timestamp file
timestamp_df = pd.read_csv('processed_timestamp_files/003.csv')

# Read data file (a CSV with the first column representing time in seconds)
data_df = pd.read_csv('oxydeoxy_DataColumnsWithTime/003data.csv', header=None)

# Create an empty list to store the chunks of data
output_data = []

# Calculate the end pointer based on the provided time gap
provided_time = 322  # time difference in seconds
last_row = data_df.shape[0]
end_pointer = last_row - provided_time * 4

# Iterate through rows in the timestamp file in original order
for index, row in timestamp_df.iloc[::-1].iterrows():
    pair_status = row['PairStatus']

    # Check if PairStatus is 'Paired'
    if pair_status == 'Paired':
        start_time = row['StartTime']
        end_time = row['EndTime']
        duration = row['Duration']

        # Calculate the start pointer based on the end pointer and duration
        start_pointer = end_pointer - int(duration * 4)

        # Extract data based on pointers
        # Include the end_pointer row
        extracted_data = data_df.iloc[start_pointer - 1:
                                      end_pointer][::1].values.tolist()

        # Get the time associated with the start and end pointers
        start_pointer_time = data_df.iloc[start_pointer - 1][0]

        # print(data_df)

        end_pointer_time = data_df.iloc[end_pointer - 1][0]

       # Insert time range, duration, start and end row numbers, and data at the beginning of the list
        output_data.insert(0, {
            'Time Range': f'{start_time} to {end_time}, Duration {duration} \n Start Row {start_pointer}, End Row {end_pointer} \n Start Time {start_pointer_time}, End Time {end_pointer_time}',
            'Data': extracted_data
        })

        # Update the end pointer for the next iteration
        end_pointer = start_pointer - 1

# Write the output to a CSV file
with open('Reverse_split_003.csv', 'w') as f:
    writer = csv.writer(f)
    # Write headers
    writer.writerow(['Time Range', 'Data'])
    for entry in output_data:
        # Write each entry to the CSV file
        writer.writerow([entry['Time Range'], entry['Data']])


# Convert the list of dictionaries to a NumPy object array
output_array = np.empty(len(output_data), dtype=object)
output_array[:] = output_data
# print(len(output_array) - 1)


# Accessing data from the NumPy object array
# Access the first 5 rows of the first chunk/entry's data and print each row
# specified_rows_data = output_array[35]['Data'][::1]

# for row in specified_rows_data:
#     print(row, "\n")

filename = 'meanValues_003.csv'

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
