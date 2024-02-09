import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the first dataset
    data1 = pd.read_csv(
        f'mean_values_only/meanValues_{i}.csv', header=None)

    # Load the second dataset
    data2 = pd.read_csv(
        f'qmeanCEnew(HRVar)/qmeanCEnew(HRVar){i}.csv')

    # Filter out rows with null values in 'Question Number' and 'Accept_Deny_button.response' columns from the second dataset
    filtered_data2 = data2.dropna(
        subset=['Question Number', 'Accept_Deny_button.response'])

    # Reset index to make sure the remaining rows are shifted up
    filtered_data2.reset_index(drop=True, inplace=True)

    # Extract the 'Accept_Deny_button.response' column from the filtered second dataset
    accept_deny_response = filtered_data2['Accept_Deny_button.response']

    # Merge the 'Accept_Deny_button.response' column to the first dataset based on index
    data1['Accept_Deny_button.response'] = accept_deny_response

    # Define the output file name based on the file number
    output_file = f'analysis_data_{i}.csv'

    # Save the merged dataset with the appropriate file name
    # No need to include headers
    data1.to_csv(output_file, index=False, header=False)
