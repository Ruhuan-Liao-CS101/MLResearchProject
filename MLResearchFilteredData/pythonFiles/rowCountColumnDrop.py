import pandas as pd


# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the dataset
    data = pd.read_csv(
        f'OriginalFilteredData/{i}_data_filtered.csv', header=None)

    columns_to_drop = [0]
    # Drop the specified columns
    data = data.drop(data.columns[columns_to_drop], axis=1)

    print(data.shape, f'{i}_data_filtered.csv')

    # Define the output file name based on the file number
    output_file = f'{i}_data_filtered.csv'

    # No headers
    data.to_csv(output_file, index=False, header=False)
