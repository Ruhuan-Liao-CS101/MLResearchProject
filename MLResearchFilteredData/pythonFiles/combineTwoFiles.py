import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the first dataset
    data1 = pd.read_csv(
        f'max_values/max_Values_{i}.csv', header=None)

    # Load the second dataset
    data2 = pd.read_csv(
        f'heartRate_trustMistrustTarget/HeartRate_trustMistrustTarget_{i}.csv', header=None)

    # Merge the datasets horizontally
    merged_data = pd.concat([data1, data2], axis=1)

    # Define the output file name based on the file number
    output_file = f'max_heartRate_trustLabel{i}.csv'

    # Save merged data to CSV
    merged_data.to_csv(output_file, index=False, header=None)
