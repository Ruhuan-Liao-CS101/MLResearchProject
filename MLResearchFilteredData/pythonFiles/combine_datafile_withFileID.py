import csv

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

# Output CSV file name
output_file = "fileID_mean_allLabels.csv"

# Combine files into a single CSV


def combine_files(file_numbers, output_file):
    with open(output_file, 'w', newline='') as combined_file:
        writer = csv.writer(combined_file)
        for i in file_numbers:
            file_name = f'mean_values_withAllLabels/mean_allLabels_{i}.csv'
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                file_id = f'{i}'  # File ID
                for row in reader:
                    row_with_id = [file_id] + row
                    writer.writerow(row_with_id)


combine_files(file_numbers, output_file)

print("Files combined successfully into", output_file)
