import pandas as pd

# Read the data file into a DataFrame without a header
data_df = pd.read_csv(
    'combined_data_files/mean_std_kurtosis_labels.csv', header=None)

# Read the timestamp file into a DataFrame with a header
# Assumes header is in the first row
timestamp_df = pd.read_csv('processed_timestamp_files/combined_timestamps.csv')

# Extract timestamps from the timestamp DataFrame
# Adjust 'Timestamp' to your actual column name
timestamps = timestamp_df['StartTime to EndTime'].tolist()

# Insert timestamps into the data DataFrame without specifying a column name
data_df.insert(loc=0, value=timestamps, column=None)

# Write the modified DataFrame back to a new file
# Ensure no header is written
data_df.to_csv('timestamp_mean_std_curtosis_labels.csv',
               index=False, header=False)
