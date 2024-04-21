import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the labeled dataset
    data = pd.read_csv(
        f'qmeanCEnew(HRVar)/qmeanCEnew(HRVar){i}.csv')

    # Filter out rows with null values in 'Question Number' and 'Accept_Deny_button.response' columns from the labeled dataset
    filtered_data = data.dropna(
        subset=['Question Number', 'Accept_Deny_button.response'])

    # Reset index in labeled data to make sure the remaining rows are shifted up
    filtered_data.reset_index(drop=True, inplace=True)

    # Extract desired columns
    selected_columns = ['EA', 'EL', 'PI', 'PR',
                        'PG', 'SA', 'SR', 'SF', 'HR', 'BI']
    extracted_data = filtered_data[selected_columns]

    # Define the output file name based on the file number
    output_file = f'HeartRate_{i}.csv'

    # Save extracted data to CSV without headers
    extracted_data.to_csv(output_file, index=False, header=False)
