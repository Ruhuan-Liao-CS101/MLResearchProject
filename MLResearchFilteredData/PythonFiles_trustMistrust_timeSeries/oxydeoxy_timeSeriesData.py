import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [18]]

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

            extracted_oxydeoxy_data = oxy_data_df.iloc[start_pointer -
                                                       1:end_pointer][::1].values.tolist()

            output_data.insert(0, {
                # Store as string representing time range
                'Time Range': f"{start_time}",
                'OxyDeoxy Data': extracted_oxydeoxy_data,
                'Duration': duration,
                'Trust Binary': trust_binary
            })

            end_pointer = start_pointer - 1


num_entries = len(output_data)
print("Number of entries in output_data:", num_entries)


# Define the headers for the CSV file
headers = ['Questions', 'Trust_binary'] + [f'Array_{i}' for i in range(1, 58)]

# Open the CSV file in write mode
with open(f'timeSeries_{i}_oxydeoxy.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    # Iterate through each entry in output_data
    for idx, entry in enumerate(output_data, start=1):
        # Create a new dictionary for the row
        row = {}

        # Add the question number
        row['Questions'] = idx

        # Determine Trust_binary based on the value of entry['Trust Binary']
        if entry['Trust Binary'] == 1:
            row['Trust_binary'] = 'trust'
        else:
            row['Trust_binary'] = 'mistrust'

        # Add the 'OxyDeoxy Data' values up to the 57th array, excluding the 0th index
        for i in range(1, 58):
            key = f'Array_{i}'
            # Check if the array exists for the current index and if it has more than one element
            if i <= len(entry['OxyDeoxy Data']) and len(entry['OxyDeoxy Data'][i - 1]) > 1:
                # Exclude the 0th index
                row[key] = entry['OxyDeoxy Data'][i - 1][1:]
            else:
                # If array doesn't exist or has only one element, fill with empty string
                row[key] = ''

        # Write the row to the CSV file
        writer.writerow(row)
