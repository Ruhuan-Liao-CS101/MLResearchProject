import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the dataset
    data = pd.read_csv(
        f'Question_Type/Question_Type_{i}.csv', header=None)

    # print(data.shape, f'{i}_data_filtered.csv')

    # List of column indices to eliminate
    # columns_to_drop = [5, 6, 13, 14, 19, 20,
    #                    27, 28, 35, 36, 41, 42, 49, 50, 55, 56]

    # Drop the specified columns
    data = data.drop(data.columns[:40], axis=1)

    # Define the output file name based on the file number
    output_file = f'QuestionType_{i}.csv'

    # No headers
    data.to_csv(output_file, index=False, header=False)
