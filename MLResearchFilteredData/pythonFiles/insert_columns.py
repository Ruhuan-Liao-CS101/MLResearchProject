import pandas as pd

# Read data from the first file
file1 = pd.read_csv(
    'combined_allFile_data/fileID_mean_allLabels.csv', header=None)

# Read data from the second file
file2 = pd.read_csv(
    'Question_Type/QuestionType.csv', header=None)

# Get the index of the last column of the first file
last_column_index = len(file1.columns) - 9

# Slice file1 to exclude the last nine columns
file1_head = file1.iloc[:, :-9]

# Slice file1 to get only the last nine columns
file1_tail = file1.iloc[:, -9:]

# Concatenate file2 columns before the last column of file1
joined_data = pd.concat([file1_head, file2, file1_tail], axis=1)

# Save the joined data to a new CSV file
joined_data.to_csv('mean_labels.csv',
                   index=False, header=False)  # No header in the output
print(joined_data.shape)
