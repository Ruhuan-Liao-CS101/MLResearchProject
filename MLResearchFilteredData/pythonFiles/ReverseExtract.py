import pandas as pd
import numpy as np
from scipy.stats import kurtosis
import csv

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

# Define the zero_position_time dictionary
zero_position_time = {
    '001': 40,
    # '002': 323,
    # '003': 322,
    # '004': 243,
    # '006': 455,
    # '007': 94,
    # '010': 181,
    # '011': 153,
    # '012': 95,
    # '013': 86,
    # '014': 88,
    # '015': 89,
    # '016': 401,
    # '017': 89,
    # '018': 150
}

for i in file_numbers:
    print(f"Processing file number: {i}")
    provided_time = zero_position_time.get(i, None)
    if provided_time is None:
        print(f"No provided time found for file number {i}")
        continue  # Skip if provided time is not found for the file number

    print(f"Provided time for file {i}: {provided_time}")

    # Read timestamp file
    timestamp_df = pd.read_csv(f'processed_timestamp_files/{i}.csv')

    # Read data file (a CSV with the first column representing time in seconds)
    data_df = pd.read_csv(
        f'oxydeoxyColumns_FilteredData/oxydeoxyData_{i}.csv', header=None)

    # Create an empty list to store the chunks of data
    output_data = []

    last_row = data_df.shape[0]
    end_pointer = last_row - provided_time * 4

    # Iterate through rows in the timestamp file in original order
    for index, row in timestamp_df.iloc[::-1].iterrows():
        pair_status = row['PairStatus']
        question_type = row['Type']

        if pair_status == 'Paired' and question_type != 0:
            start_time = row['StartTime']
            end_time = row['EndTime']
            duration = row['Duration']

            start_pointer = end_pointer - int(duration * 4)

            extracted_data = data_df.iloc[start_pointer - 1:
                                          end_pointer][::1].values.tolist()

            start_pointer_time = data_df.iloc[start_pointer - 1][0]
            end_pointer_time = data_df.iloc[end_pointer - 1][0]

            output_data.insert(0, {
                'Time Range': f'{start_time} to {end_time}, Duration {duration} \n Start Row {start_pointer}, End Row {end_pointer} \n Start Time {start_pointer_time}, End Time {end_pointer_time}',
                'Data': extracted_data,
            })

            end_pointer = start_pointer - 1

    # with open(f'Reverse_split_{i}.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['Time Range', 'Data'])
    #     for entry in output_data:
    #         writer.writerow([entry['Time Range'], entry['Data']])

    output_array = np.empty(len(output_data), dtype=object)
    output_array[:] = output_data

    filename = f'max_labeled_{i}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        for entry in output_array:
            data_array = np.array(entry['Data'])
            # mean = np.mean(data_array[:, 1:], axis=0, keepdims=True)
            # std = np.std(data_array[:, 1:], axis=0, keepdims=True, ddof=1)
            # kurtosis_val = kurtosis(
            #     data_array[:, 1:], axis=0, fisher=False, bias=False, keepdims=True)
            # kurtosis_val -= 3
            # min_values = np.min(data_array[:, 1:], axis=0, keepdims=True)
            max_values = np.max(data_array[:, 1:], axis=0, keepdims=True)

            max_size = max_values.shape

            writer.writerow([f"Time Range: {entry['Time Range']}"])
            writer.writerow(["Max Values:"])
            writer.writerows(max_values)
            writer.writerow([f"Size of max values: {max_size}"])
            writer.writerow([])

    filename = f'max_Values_{i}.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        for entry in output_array:
            data_array = np.array(entry['Data'])
            # mean = np.mean(data_array[:, 1:], axis=0, keepdims=True)
            # std = np.std(data_array[:, 1:], axis=0, keepdims=True, ddof=1)
            # kurtosis_val = kurtosis(
            #     data_array[:, 1:], axis=0, fisher=False, bias=False, keepdims=True)
            # kurtosis_val -= 3
            # min_values = np.min(data_array[:, 1:], axis=0, keepdims=True)
            max_values = np.max(data_array[:, 1:], axis=0, keepdims=True)
            writer.writerows(max_values)
