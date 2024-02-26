import pandas as pd

# Read the first CSV file into a DataFrame
df1 = pd.read_csv(
    'combined_mean_withFileID.csv', header=None)

# Read the second CSV file into a DataFrame
df2 = pd.read_csv('combined_data_files/std_kurtosis.csv', header=None)

# Extract the data from df2
data_to_insert = df2.values

# Get the index of the column where you want to insert the data
insert_index = len(df1.columns) - 9

# Insert the data from df2 into df1 before the last column
for i in range(df2.shape[1]):
    df1.insert(insert_index + i, f'new_column_{i}', data_to_insert[:, i])

# Write the updated DataFrame to a new CSV file
df1.to_csv('mean_std_kurtosis_labels.csv', index=False, header=False)
