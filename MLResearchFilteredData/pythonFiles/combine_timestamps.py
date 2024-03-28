import pandas as pd

# Initialize an empty list to store DataFrames
dfs = []

# Define the file numbers with leading zeros
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

# Iterate through each file number
for number in file_numbers:
    file_name = f'processed_timestamp_files/{number}.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # Filter out unpaired rows and rows with Type 0
    df = df[(df['PairStatus'] == 'Paired') & (df['Type'] != 0)]

   # Convert StartTime and EndTime to the desired format and concatenate them
    df['StartTime to EndTime'] = df['StartTime'] + ' to ' + df['EndTime']

    df = df['StartTime to EndTime']

    # Append the filtered DataFrame to the list
    dfs.append(df)

# Concatenate all DataFrames in the list
combined_data = pd.concat(dfs, ignore_index=True)

# Write the combined data to a new CSV file
combined_data.to_csv('combined_timestamps.csv', index=False)
