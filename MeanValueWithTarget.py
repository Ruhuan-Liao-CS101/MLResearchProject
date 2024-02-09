import pandas as pd

# Load the first dataset
data1 = pd.read_csv('mean_values_only/meanValues_001.csv', header=None)

# Load the second dataset
data2 = pd.read_csv('qmeanCEnew(HRVar)/qmeanCEnew(HRVar)003.csv')

# Filter out rows with null values in 'Question Number' and 'Accept_Deny_button.response' columns from the second dataset
filtered_data2 = data2.dropna(
    subset=['Question Number', 'Accept_Deny_button.response'])

# Reset index to make sure the remaining rows are shifted up
filtered_data2.reset_index(drop=True, inplace=True)

# Extract the 'Accept_Deny_button.response' column from the filtered second dataset
accept_deny_response = filtered_data2['Accept_Deny_button.response']

# Merge the 'Accept_Deny_button.response' column to the first dataset based on index
data1['Accept_Deny_button.response'] = accept_deny_response

# Save the merged dataset
data1.to_csv('analysis_data_003.csv', index=False,
             header=False)  # No need to include headers
