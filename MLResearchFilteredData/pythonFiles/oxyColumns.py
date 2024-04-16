import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:

    # Load the CSV file without header
    data = pd.read_csv(
        f'oxydeoxyColumns_FilteredData/oxydeoxyData_{i}.csv', header=None)

    # Identify the number of columns
    num_columns = len(data.columns)

    # Create a list of columns to drop (all odd columns except the first one)
    columns_to_drop = [col for col in range(
        num_columns) if col % 2 == 0 and col != 0]

    # Drop the identified columns
    data.drop(columns=columns_to_drop, inplace=True)

    # Save the modified data to a new CSV file
    data.to_csv(f'oxyCol_Data_{i}.csv', index=False, header=False)
