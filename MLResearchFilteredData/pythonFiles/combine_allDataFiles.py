import csv
import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

# Output CSV file name
output_file = "QuestionType.csv"

# Function to combine files into a single CSV


def combine_files(file_numbers, output_file):
    with open(output_file, 'w', newline='') as combined_file:
        writer = csv.writer(combined_file)
        for i in file_numbers:
            file_name = f'Question_Type/QuestionType_{i}.csv'
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    writer.writerow(row)


# Call the function to combine files
combine_files(file_numbers, output_file)

print("Files combined successfully into", output_file)
