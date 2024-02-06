from datetime import datetime

# Last end time from timestamp csv file
last_end_time_001 = "19:23:40"  # You've provided this value

# Parse the last end time from 001.csv file
last_end_time_001 = datetime.strptime(last_end_time_001, "%H:%M:%S")

# End time specified from 0thPositionOfDataFile
end_time_001_data_file = "7:27:43 pm"  # You've provided this value

# Parse the end time specified for 001 from 0thPositionOfDataFile
end_time_001_data_file = datetime.strptime(
    end_time_001_data_file, "%I:%M:%S %p")

# Calculate the time difference
time_difference = end_time_001_data_file - last_end_time_001

print("Time difference:", time_difference)
