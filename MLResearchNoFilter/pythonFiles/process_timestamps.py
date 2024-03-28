import csv
from datetime import datetime
import os


def parse_line(line):
    parts = line.strip().split(';')
    date_time = datetime.strptime(parts[0], '%Y-%m-%dT%H:%M:%S.%f')
    time = date_time.strftime('%H:%M:%S')
    type_val = int(parts[-1])
    return time, type_val


def analyze_data(input_file, output_file):
    # start_times = {}
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['StartTime', 'EndTime', 'Type', 'Duration', 'PairStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, len(lines), 2):
            start_line = lines[i]

            if i + 1 < len(lines):
                end_line = lines[i + 1]

                start_time, start_type = parse_line(start_line)
                end_time, end_type = parse_line(end_line)

                if start_type == end_type:
                    duration = datetime.strptime(
                        end_time, '%H:%M:%S') - datetime.strptime(start_time, '%H:%M:%S')
                    duration_seconds = duration.total_seconds()

                    writer.writerow({
                        'StartTime': start_time,
                        'EndTime': end_time,
                        'Type': start_type,
                        'Duration': duration_seconds,
                        'PairStatus': 'Paired'
                    })

                else:
                    writer.writerow({
                        'StartTime': start_time,
                        'EndTime': '',
                        'Type': start_type,
                        'Duration': '',
                        'PairStatus': 'No Pair'
                    })

                    writer.writerow({
                        'StartTime': end_time,
                        'EndTime': '',
                        'Type': end_type,
                        'Duration': '',
                        'PairStatus': 'No Pair'
                    })
            else:
                # Handle the case when there's no matching end time for the last starting time
                start_time, start_type = parse_line(start_line)
                writer.writerow({
                    'StartTime': start_time,
                    'EndTime': '',
                    'Type': start_type,
                    'Duration': '',
                    'PairStatus': 'No Pair'
                })


if __name__ == "__main__":
    root_folder = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(
        root_folder, 'timestamp _files', '2022-07-26_001_lsl.tri')
    output_file_path = os.path.join(
        root_folder, '2022-07-26_001_output.csv')

    analyze_data(input_file_path, output_file_path)
