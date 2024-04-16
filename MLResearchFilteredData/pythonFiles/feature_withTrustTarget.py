import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Read the data file without header
    data_df = pd.read_csv(
        f'max_values/max_Values_{i}.csv', header=None)

    # Read the time stamp file, extracting only the 'trust_binary' column
    time_stamp_df = pd.read_csv(
        f'timestamp_trustbinary/timestamp_trustLabel_{i}.csv')
    trust_binary_column = time_stamp_df['trust_binary']

    # Ensure the index of both DataFrames match
    data_df.index = time_stamp_df.index

    # Concatenate trust_binary column with data DataFrame
    data_df['trust_binary'] = trust_binary_column

    # Write the combined DataFrame back to a new file without header
    data_df.to_csv(f'max_withTrustLabel_{i}.csv', header=False, index=False)
