import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3) for i in [1]]

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

# Initialize a variable to keep track of the end time of the previous time series
previous_end_time = 0

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
    oxy_data_df = pd.read_csv(
        f'oxyColumns_FilteredData/oxyCol_Data_{i}.csv', header=None)

    # Read deoxy data file
    deoxy_data_df = pd.read_csv(
        f'deoxyColumns_FilteredData/deoxyCol_Data_{i}.csv', header=None)

    # Create an empty list to store the chunks of data
    output_data = []

    last_row = oxy_data_df.shape[0]
    end_pointer = last_row - provided_time * 4

    # Initialize variables to track min and max y-values
    min_y = float('inf')
    max_y = float('-inf')

    # Iterate through rows in the timestamp file in original order
    for index, row in timestamp_df.iloc[::-1].iterrows():
        pair_status = row['PairStatus']
        question_type = row['Type']

        if pair_status == 'Paired' and question_type != 0:
            start_time = row['StartTime']
            end_time = row['EndTime']
            duration = row['Duration']

            start_pointer = end_pointer - int(duration * 4)

            extracted_oxy_data = oxy_data_df.iloc[start_pointer -
                                                  1:end_pointer][::1].values.tolist()
            extracted_deoxy_data = deoxy_data_df.iloc[start_pointer -
                                                      1:end_pointer][::1].values.tolist()

            start_pointer_time = oxy_data_df.iloc[start_pointer - 1][0]
            end_pointer_time = oxy_data_df.iloc[end_pointer - 1][0]

            output_data.insert(0, {
                # Store as string representing time range
                'Time Range': f"{start_time}",
                'Oxy Data': extracted_oxy_data,
                'Deoxy Data': extracted_deoxy_data,
                'Duration': duration
            })

            end_pointer = start_pointer - 1

plt.figure(figsize=(10, 6))

# Plot for each time data entry
for entry in output_data:
    oxy_data_array = np.array(entry['Oxy Data'])
    deoxy_data_array = np.array(entry['Deoxy Data'])
    start_time = entry['Time Range']
    duration = entry['Duration']

    # Calculate time axis for this entry starting from 0
    entry_time_axis = np.arange(len(oxy_data_array)) * 0.25

    # Calculate rolling mean for each row separately
    oxy_rolling_mean = np.mean(oxy_data_array[:, 1:], axis=1)
    # Calculate rolling standard deviation for each row separately
    oxy_rolling_std = np.std(oxy_data_array[:, 1:], axis=1)

    deoxy_rolling_mean = np.mean(deoxy_data_array[:, 1:], axis=1)
    deoxy_rolling_std = np.std(deoxy_data_array[:, 1:], axis=1)

    # Track min and max y-values
    # min_y = min(np.min(oxy_rolling_mean), np.min(deoxy_rolling_mean))
    # max_y = max(np.max(oxy_rolling_mean), np.max(deoxy_rolling_mean))
    # Calculate y-axis limits considering mean and std deviation
    min_y_oxy = np.min(oxy_rolling_mean - 2 * oxy_rolling_std)
    max_y_oxy = np.max(oxy_rolling_mean + 2 * oxy_rolling_std)

    min_y_deoxy = np.min(deoxy_rolling_mean - 2 * deoxy_rolling_std)
    max_y_deoxy = np.max(deoxy_rolling_mean + 2 * deoxy_rolling_std)

    min_y = min(min_y_oxy, min_y_deoxy)
    max_y = max(max_y_oxy, max_y_deoxy)

    # Plot oxy data
    plt.subplot(2, 1, 1)
    plt.plot(entry_time_axis, oxy_rolling_mean, color='blue', label='Oxy')
    # Plotting shaded region for ±2 standard deviations
    plt.fill_between(entry_time_axis, oxy_rolling_mean - 2 * oxy_rolling_std,
                     oxy_rolling_mean + 2 * oxy_rolling_std, alpha=0.2, color='blue')

    # Plot deoxy data
    plt.subplot(2, 1, 2)
    plt.plot(entry_time_axis, deoxy_rolling_mean, color='red', label='Deoxy')
    plt.fill_between(entry_time_axis, deoxy_rolling_mean - 2 * deoxy_rolling_std,
                     deoxy_rolling_mean + 2 * deoxy_rolling_std, alpha=0.2, color='red')

    # Set y-limits based on min and max y-values
    plt.subplot(2, 1, 1)
    plt.ylim(min_y, max_y)
    plt.ylabel('Mean Value (Oxy)')
    plt.title('Oxy Time Series Data with Rolling Mean and ±2 Std Dev Range')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.ylim(min_y, max_y)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Mean Value (Deoxy)')
    plt.title('Deoxy Time Series Data with Rolling Mean and ±2 Std Dev Range')
    plt.grid(True)

    # Add legend for oxy plot
    plt.subplot(2, 1, 1)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Add legend for deoxy plot
    plt.subplot(2, 1, 2)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()
