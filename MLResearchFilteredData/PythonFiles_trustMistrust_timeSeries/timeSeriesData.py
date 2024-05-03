import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3) for i in [1]]

# Define the zero_position_time dictionary
zero_position_time = {
    '001': 40,
    '002': 323,
    '003': 322,
    '004': 243,
    '006': 455,
    '007': 94,
    '010': 181,
    '011': 153,
    '012': 95,
    '013': 86,
    '014': 88,
    '015': 89,
    '016': 401,
    '017': 89,
    '018': 150
}

# Initialize lists to store mean values and corresponding start and end times
mean_values_oxy_column1 = []
std_dev_oxy_column1 = []
start_times = []
end_times = []

for i in file_numbers:
    print(f"Processing file number: {i}")
    provided_time = zero_position_time.get(i, None)
    if provided_time is None:
        print(f"No provided zero position time found for file number {i}")
        continue  # Skip if provided time is not found for the file number

    print(f"Provided zero position time for file {i}: {provided_time}")

    # Read timestamp file
    timestamp_df = pd.read_csv(
        f'timestamp_trustbinary/timestamp_trustLabel_{i}.csv')

    # Read data file (a CSV with the first column representing time in seconds)
    oxy_data_df = pd.read_csv(
        f'oxydeoxyColumns_FilteredData/oxydeoxyData_{i}.csv', header=None)

    # Create an empty list to store the chunks of data
    output_data = []

    # Get the start and end times from the first and last rows of the timestamp file
    start_time = timestamp_df.iloc[0]['StartTime']
    end_time = timestamp_df.iloc[-1]['EndTime']

    # Store the start and end times
    start_times.append(start_time)
    end_times.append(end_time)

    last_row = oxy_data_df.shape[0]
    end_pointer = last_row - provided_time * 4

    # Iterate through rows in the timestamp file in original order
    for index, row in timestamp_df.iloc[::-1].iterrows():
        pair_status = row['PairStatus']
        question_type = row['Type']
        # Extracting trust_binary from the timestamp file
        trust_binary = row['trust_binary']

        if pair_status == 'Paired' and question_type != 0:
            start_time = row['StartTime']
            end_time = row['EndTime']
            duration = row['Duration']

            start_pointer = end_pointer - int(duration * 4)

            extracted_oxy_data = oxy_data_df.iloc[start_pointer -
                                                  1:end_pointer][::1].values.tolist()

            output_data.insert(0, {
                # Store as string representing time range
                'Time Range': f"{start_time}",
                'Oxy Data': extracted_oxy_data,
                'Duration': duration,
                'Trust Binary': trust_binary
            })

            end_pointer = start_pointer - 1


num_entries = len(output_data)
print("Number of entries in output_data:", num_entries)

trust_data = []
mistrust_data = []

for entry in output_data:
    if entry['Trust Binary'] == 1:
        trust_data.append(np.array(entry['Oxy Data']))
    else:
        mistrust_data.append(np.array(entry['Oxy Data']))

num_trust_entries = len(trust_data)
num_mistrust_entries = len(mistrust_data)

print("Number of trust entries:", num_trust_entries)
print("Number of mistrust entries:", num_mistrust_entries)

# Display the length of each array in trust_data
for i, array in enumerate(trust_data):
    print(f"Length of trust array {i+1}: {len(array)}")

# Display the length of each array in mistrust_data
for i, array in enumerate(mistrust_data):
    print(f"Length of mistrust array {i+1}: {len(array)}")

# Define a function to extract data points for a given data set


def extract_data_points(data):
    data_points = []
    min_length = min([len(array) for array in data])
    for i in range(min_length):
        values = []
        for array in data:
            values.append(array[i])
        data_points.append(values)
    return data_points


# Define a function to write data to CSV file
def write_to_csv(filename, channel_data_points):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Channel', 'Trust_binary']
        # Add headers for 57 columns
        header.extend([f'Array_{i}' for i in range(1, 58)])
        writer.writerow(header)
        for channel_num in range(1, 41):  # Loop through channels 1 to 20
            trust_data_points, mistrust_data_points = channel_data_points[channel_num - 1]
            trust_row = [f'{channel_num}', 'trust']
            mistrust_row = [f'{channel_num}', 'mistrust']
            for i in range(57):  # Add 57 array columns
                if i < len(trust_data_points):
                    trust_row.append(str(trust_data_points[i]))
                else:
                    trust_row.append('')  # Empty cell if no more data points
                if i < len(mistrust_data_points):
                    mistrust_row.append(str(mistrust_data_points[i]))
                else:
                    # Empty cell if no more data points
                    mistrust_row.append('')
            writer.writerow(trust_row)
            writer.writerow(mistrust_row)


# Initialize a list to store data points for each channel
channel_data_points = []

# Loop through channels 1 to 20
for channel_num in range(1, 41):
    trust_data_points = extract_data_points(
        [array[:, channel_num] for array in trust_data])
    mistrust_data_points = extract_data_points(
        [array[:, channel_num] for array in mistrust_data])
    channel_data_points.append((trust_data_points, mistrust_data_points))

# Specify the filename for the CSV file
csv_filename = 'timeSeries_001_oxydeoxyColumns.csv'

# Write data points to the CSV file
write_to_csv(csv_filename, channel_data_points)

print(
    f"Data points for trust and mistrust arrays for each channel have been written to '{csv_filename}'.")
