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
        f'oxyColumns_FilteredData/oxyCol_Data_{i}.csv', header=None)

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

channel_num = 1

trust_first_column_values = []
# Print the size of the channel for arrays in trust_data
print(f"\nSize of channel {channel_num} in arrays in trust_data:")
for i in range(len(trust_data)):
    array = trust_data[i]
    first_column_values = array[:, channel_num]
    trust_first_column_size = array[:, channel_num].shape
    trust_first_column_values.append(first_column_values)
    print(
        f"Array {i + 1} size of channel {channel_num}: {trust_first_column_size}")
    # print("Array", i + 1, "second channel values:", first_column_values)

mistrust_first_column_values = []
# Print the size of the channel for arrays in mistrust_data
print(f"\nSize of channel {channel_num} in arrays in mistrust_data:")
for i in range(len(mistrust_data)):
    array = mistrust_data[i]
    first_column_values = array[:, channel_num]
    mistrust_first_column_size = array[:, channel_num].shape
    mistrust_first_column_values.append(first_column_values)
    print(
        f"Array {i + 1} size of channel {channel_num}: {mistrust_first_column_size}")
    # print("Array", i + 1, "first column values:", first_column_values)


# def calculate_mean_for_data_point(data):
#     # Get the minimum length of arrays in the data set
#     min_length = min([len(array) for array in data])

#     # Initialize list to store mean values for each data point
#     mean_values = []

#     # Iterate over each data point
#     for i in range(min_length):
#         values = []
#         # Iterate over each array in the data set
#         for array in data:
#             values.append(array[i])
#         # Calculate mean for the current data point across all arrays
#         mean_value = np.mean(values)
#         mean_values.append(mean_value)

#     return mean_values

def extract_data_points(data):
    data_points = []
    min_length = min([len(array) for array in data])
    for i in range(min_length):
        values = []
        for array in data:
            values.append(array[i])
        data_points.append(values)
    return data_points


def calculate_mean_for_data_point(data):
    # Initialize list to store mean values for each data point
    mean_values = []

    # Iterate over each data point
    for i in range(len(data)):
        # Calculate mean for the current data point across all arrays
        mean_value = np.mean(data[i])
        mean_values.append(mean_value)

    return mean_values


# # Calculate mean for trust data and mistrust data
# trust_mean_values = calculate_mean_for_data_point(trust_first_column_values)
# mistrust_mean_values = calculate_mean_for_data_point(
#     mistrust_first_column_values)

# Extract data points
trust_data_points = extract_data_points(trust_first_column_values)
mistrust_data_points = extract_data_points(mistrust_first_column_values)

# Calculate mean for trust data points and mistrust data points
trust_mean_values = calculate_mean_for_data_point(trust_data_points)
mistrust_mean_values = calculate_mean_for_data_point(mistrust_data_points)


print("\nSize of the mean values array for trust:", len(trust_mean_values))
print("Size of the mean values array for mistrust:", len(mistrust_mean_values))

print("\nMean for each data point across all arrays for trust:\n", trust_mean_values)
print("\nMean for each data point across all arrays for mistrust:\n",
      mistrust_mean_values)


# Generate time stamps with a 0.25 second interval
time_stamps = np.arange(0, min(len(trust_mean_values),
                        len(mistrust_mean_values))*0.25, 0.25)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(time_stamps, trust_mean_values[:len(
    time_stamps)], color='green', label='Trust', marker='.')
plt.scatter(time_stamps, mistrust_mean_values[:len(
    time_stamps)], color='red', label='Mistrust', marker='.')
plt.plot(time_stamps, trust_mean_values[:len(
    time_stamps)], color='green', linestyle='-', linewidth=1)
plt.plot(time_stamps, mistrust_mean_values[:len(
    time_stamps)], color='red', linestyle='-', linewidth=1)
plt.xlabel('Time Interval (seconds)')
plt.ylabel(f'Mean Values in channel {channel_num}')
plt.title(
    f'Time Series Plot of Mean Values for Trust and Mistrust in channel {channel_num}')
plt.legend()
plt.grid(True)
plt.show()
