import pandas as pd

# Load the CSV files into DataFrames
df1 = pd.read_csv('time_files/006time.csv')
df2 = pd.read_csv('data_files/006data.csv')

# Add a temporary index column to both DataFrames
df1['index_temp'] = range(len(df1))
df2['index_temp'] = range(len(df2))

# Merge the DataFrames based on the temporary index
merged_df = pd.merge(df1, df2, on='index_temp')

# Drop the temporary index column
merged_df = merged_df.drop('index_temp', axis=1)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_file_006.csv', index=False)
