import pandas as pd


def count_types(file_path, column_name):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert the column to string, handle cases like 1.0, 2.0
    df[column_name] = df[column_name].astype(str)

    # Count occurrences of each unique type
    type_counts = df[column_name].value_counts(dropna=False)

    # Sort the results by in ascending order
    type_counts = type_counts.sort_index(ascending=True)

    return type_counts


def compare_counts(file1_path, file2_path, column_name1, column_name2):
    # Get counts for each unique value in the specified columns
    counts_file1 = count_types(file1_path, column_name1)
    counts_file2 = count_types(file2_path, column_name2)

    # Combine unique values from both files
    all_values = set(counts_file1.index).union(set(counts_file2.index))

    # Combine the counts into a DataFrame
    result_df = pd.DataFrame({
        'Type': list(all_values),
        'File1 Count': counts_file1.reindex(all_values, fill_value=0).values,
        'File2 Count': counts_file2.reindex(all_values, fill_value=0).values,
        'Count Difference': counts_file2.reindex(all_values, fill_value=0).values - counts_file1.reindex(all_values, fill_value=0).values
    })

    # Convert 'Type' to float for comparison
    result_df['Type'] = result_df['Type'].astype(float)
    result_df = result_df.groupby('Type', as_index=False).agg({
        'File1 Count': 'sum',
        'File2 Count': 'sum',
        'Count Difference': 'sum'
    })

    return result_df


# File path
file1_path = 'qmeanCEnew(HRVar)/qmeanCEnew(HRVar)001.csv'
file2_path = 'processed_timestamp_files/2022-07-26_001_output.csv'

# Column names
file1_column = 'Question Number'
file2_column = 'Type'

# Get counts for each unique question number
file1_counts = count_types(file1_path, file1_column)

# Print results
print(f"{file1_path}:\n{file1_counts}")


# Get counts for each unique type in the second file
file2_counts = count_types(file2_path, file2_column)

# Print results in ascending order
print(
    f"{file2_path}:\n{file2_counts}")


# Compare counts between 'Question Number' and 'Type'
result_df = compare_counts(file1_path, file2_path, file1_column, file2_column)

# Print the combined result DataFrame
print(result_df)
