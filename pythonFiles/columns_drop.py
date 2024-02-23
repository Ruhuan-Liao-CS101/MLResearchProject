import pandas as pd

# Read the CSV file
data = pd.read_csv('merged_time_data_files/merged_file_018.csv')

# columns_to_drop = [4, 5, 12, 13, 18, 19,
#                    26, 27, 34, 35, 40, 41, 48, 49, 54, 55]

# List of column indices to eliminate
columns_to_drop = [5, 6, 13, 14, 19, 20,
                   27, 28, 35, 36, 41, 42, 49, 50, 55, 56]

# Drop the specified columns
data = data.drop(data.columns[columns_to_drop], axis=1)

# Save the modified DataFrame to a new CSV file
data.to_csv('018data.csv', index=False)
