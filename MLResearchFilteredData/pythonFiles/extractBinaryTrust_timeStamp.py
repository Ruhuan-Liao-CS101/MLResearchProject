import pandas as pd

# Load timestamp file into DataFrame
timestamp_df = pd.read_csv('processed_timestamp_files/014.csv')

# Load data file into DataFrame
data_df = pd.read_csv('combined_allFile_data/normalized_data.csv')

# Filter rows with Duration = 0 or PairStatus equals No Pair
timestamp_df = timestamp_df[(~timestamp_df['Duration'].isin([0, 1])) & (
    timestamp_df['PairStatus'] != 'No Pair')]
print("Number of rows in timestamp after filtering:", len(timestamp_df))

# Filter rows from data_df for Subject_ID = i
subject_id = 14
subject_data_df = data_df[data_df['Subject_ID'] == subject_id]
print("Number of rows in subject_data_df:", len(subject_data_df))

# Reset index for both DataFrames
timestamp_df.reset_index(drop=True, inplace=True)
subject_data_df.reset_index(drop=True, inplace=True)

# Merge timestamp_df with subject_data_df based on pointer
merged_df = pd.concat([timestamp_df, subject_data_df['trust_binary']], axis=1)
print("Number of rows in merged_df before filtering:", len(merged_df))

# Insert trust_binary values into a new column in the timestamp file
timestamp_df['trust_binary'] = merged_df['trust_binary']

# Save the updated timestamp file
timestamp_df.to_csv('timestamp_trustLabel_014.csv', index=False)
