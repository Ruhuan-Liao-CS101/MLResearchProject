# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import kurtosis
# import csv

# # Define the list of file numbers to parse
# file_numbers = [str(i).zfill(3) for i in [1]]

# # Define the zero_position_time dictionary
# zero_position_time = {'001': 40}

# for i in file_numbers:
#     print(f"Processing file number: {i}")
#     provided_time = zero_position_time.get(i, None)
#     if provided_time is None:
#         print(f"No provided time found for file number {i}")
#         continue  # Skip if provided time is not found for the file number

#     print(f"Provided time for file {i}: {provided_time}")

#     # Read timestamp file
#     timestamp_df = pd.read_csv(f'processed_timestamp_files/{i}.csv')

#     # Read data file (a CSV with the first column representing time in seconds)
#     data_df = pd.read_csv(
#         f'oxydeoxyColumns_FilteredData/oxydeoxyData_{i}.csv', header=None)

#     # Create an empty list to store the chunks of data
#     output_data = []

#     last_row = data_df.shape[0]
#     end_pointer = last_row - provided_time * 4

#     # Iterate through rows in the timestamp file in original order
#     for index, row in timestamp_df.iloc[::-1].iterrows():
#         pair_status = row['PairStatus']
#         question_type = row['Type']

#         if pair_status == 'Paired' and question_type != 0:
#             start_time = row['StartTime']
#             end_time = row['EndTime']
#             duration = row['Duration']

#             start_pointer = end_pointer - int(duration * 4)

#             extracted_data = data_df.iloc[start_pointer - 1:
#                                           end_pointer][::1].values.tolist()

#             start_pointer_time = data_df.iloc[start_pointer - 1][0]
#             end_pointer_time = data_df.iloc[end_pointer - 1][0]

#             output_data.insert(0, {
#                 'Time Range': f'{start_time} to {end_time}',
#                 'Data': extracted_data,
#             })

#             end_pointer = start_pointer - 1

#     output_array = np.empty(len(output_data), dtype=object)
#     output_array[:] = output_data

#     plt.figure(figsize=(10, 6))

#     for entry in output_array:
#         data_array = np.array(entry['Data'])
#         mean = np.mean(data_array[:, 1:], axis=0, keepdims=True)
#         time = data_array[:, 0]
#         # Taking mean across columns
#         values = np.mean(data_array[:, 1:], axis=1)

#         plt.plot(time, values, label=entry['Time Range'])

#     plt.xlabel('Time')
#     plt.ylabel('Mean Value')
#     plt.title('Brain Data Wave Frequency with Time-Series Mean Values')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3) for i in [1]]

# Define the zero_position_time dictionary
zero_position_time = {'001': 40}

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
                'Time Range': f'{start_time} to {end_time}',
                'Data': extracted_data,
            })

            end_pointer = start_pointer - 1

    output_array = np.empty(len(output_data), dtype=object)
    output_array[:] = output_data

    # Plot the brain data wave frequency chart with time-series at the bottom for mean values
    plt.figure(figsize=(10, 6))

    for entry in output_array:
        data_array = np.array(entry['Data'])
        # Select only the odd-numbered columns for calculating mean values
        mean = np.mean(data_array[:, 1::2], axis=0, keepdims=True)
        time = data_array[:, 0]
        # Taking mean across odd-numbered columns
        values = np.mean(data_array[:, 1::2], axis=1)

        plt.plot(time, values, label=entry['Time Range'])

    # Add labels and legend for the main plot
    plt.xlabel('Time')
    plt.ylabel('Mean Value')
    plt.title('Time Series Data with Rolling Mean and ±2 Std Dev Range')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Calculate rolling mean and standard deviation
    rolling_mean = np.mean(values) * np.ones_like(time)
    rolling_std = np.std(values) * np.ones_like(time)

    # Plotting the rolling mean and shaded ranges
    plt.plot(time, rolling_mean, color='red', label='Rolling Mean')
    plt.fill_between(time, rolling_mean - 2 * rolling_std, rolling_mean +
                     2 * rolling_std, color='lightgray', label='±2 Std Dev Range')

    # Show the legend for the rolling mean and ±2 standard deviation range
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))

    plt.grid(True)
    plt.show()
