import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the CSV files into DataFrames
    df1 = pd.read_csv(f'time_files/{i}time.csv')
    df2 = pd.read_csv(f'FilteredData/{i}_data_filtered.csv.csv')

    # Add a temporary index column to both DataFrames
    df1['index_temp'] = range(len(df1))
    df2['index_temp'] = range(len(df2))

    # Merge the DataFrames based on the temporary index
    merged_df = pd.merge(df1, df2, on='index_temp')

    # Drop the temporary index column
    merged_df = merged_df.drop('index_temp', axis=1)

    print(f'{i}.csv', merged_df.shape)

    # # Save the merged DataFrame to a new CSV file
    # merged_df.to_csv(f'time_data_file_{i}.csv', index=False)
