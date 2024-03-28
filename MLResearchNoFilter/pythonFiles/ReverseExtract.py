import pandas as pd
import numpy as np
# from scipy.stats import skew
from scipy.stats import kurtosis
import csv

# Read timestamp file
timestamp_df = pd.read_csv('processed_timestamp_files/018.csv')

# Read data file (a CSV with the first column representing time in seconds)
data_df = pd.read_csv('oxydeoxy_DataColumns/018data.csv', header=None)

# Create an empty list to store the chunks of data
output_data = []

'''
001, 40 seconds
002, 323 seconds
003, 322 seconds
004, 243 seconds
# 005, 3970 seconds
006, 455 seconds
007, 94 seconds
# 008, 1909 seconds
010, 181 seconds
011, 153 seconds
012, 95 seconds
013, 86 seconds
014, 88 seconds
015, 89 seconds
016, 401 seconds
017, 89 seconds
018, 150 seconds
'''

# Calculate the end pointer based on the provided time gap for 0th position
provided_time = 150  # time difference in seconds
last_row = data_df.shape[0]
end_pointer = last_row - provided_time * 4

# Iterate through rows in the timestamp file in original order
for index, row in timestamp_df.iloc[::-1].iterrows():
    pair_status = row['PairStatus']
    question_type = row['Type']

    # Check if PairStatus is 'Paired'
    if pair_status == 'Paired' and question_type != 0:
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
            'Data': extracted_data,
        })

        # Update the end pointer for the next iteration
        end_pointer = start_pointer - 1
""" 
# Write the output to a CSV file
with open('Reverse_split_018.csv', 'w') as f:
    writer = csv.writer(f)
    # Write headers
    writer.writerow(['Time Range', 'Data'])
    for entry in output_data:
        # Write each entry to the CSV file
        writer.writerow([entry['Time Range'], entry['Data']])

 """
# Convert the list of dictionaries to a NumPy object array
output_array = np.empty(len(output_data), dtype=object)
output_array[:] = output_data


# Accessing data from the NumPy object array
# Access the first 5 rows of the first chunk/entry's data and print each row
# specified_rows_data = output_array[35]['Data'][::1]

# for row in specified_rows_data:
#     print(row, "\n")

filename = 'kurtosis_labeled_018.csv'
# Open the file in write mode
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)

    # Iterate through each entry in the output array
    for entry in output_array:
        data_array = np.array(entry['Data'])
        # mean = np.mean(data_array[:, 1:], axis=0, keepdims=True)
        # std = np.std(data_array[:, 1:], axis=0, keepdims=True, ddof=1)
        kurtosis_values = kurtosis(
            data_array[:, 1:], axis=0, fisher=False, bias=False, keepdims=True)
        kurtosis_values -= 3

        # mean_values_size = mean_values.shape
        # std_values_size = std_values.shape
        kur_value_size = kurtosis_values.shape

        # Write the time range and mean values to the CSV file
        writer.writerow([f"Time Range: {entry['Time Range']}"])
        writer.writerow(["kurtosis Values:"])
        # writer.writerows(mean_values)
        writer.writerows(kurtosis_values)
        # writer.writerow([f"Size of mean_values: {mean_values_size}"])
        writer.writerow([f"Size of std_values: {kur_value_size}"])
        writer.writerow([])  # Add an empty row for better readability


# File contain only mean values
filename = 'kurtosis_Values_018.csv'
# Open the file in write mode
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)

    # Iterate through each entry in the output array
    for entry in output_array:
        data_array = np.array(entry['Data'])
        # mean = np.mean(data_array[:, 1:], axis=0, keepdims=True)
        # std = np.std(data_array[:, 1:], axis=0, keepdims=True, ddof=1)
        # variance_values = np.var(data_array[:, 1:], axis=0, keepdims=True)
        # skewness_values = skew(data_array[:, 1:], axis=0)
        kurtosis_values = kurtosis(
            data_array[:, 1:], axis=0, fisher=False, bias=False, keepdims=True)
        kurtosis_values -= 3
        writer.writerows(kurtosis_values)
