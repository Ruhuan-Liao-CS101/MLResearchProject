# Initialize a dictionary to store the total occurrences of each distinct channel
total_channel_occurrences = {}

# Read the contents of the file
with open('featureImportance.txt', 'r') as file:
    # Keep track of line numbers
    for line_number, line in enumerate(file, start=1):
        # Skip the header line
        if line_number == 1:
            continue

        # Strip leading and trailing whitespace
        line = line.strip()

        # Skip lines containing "Channel Importance"
        if "Channel" in line and "Importance" in line:
            continue

        # Extract the channel number from the line
        parts = line.split('Channel ')

        # Ensure that the line is in the expected format
        if len(parts) < 2:
            # Print lines with incorrect format
            print(f"Skipping line {line_number}: '{line}' - Incorrect format")
            continue

        channel_part = parts[1]

        # Split the channel part to extract the channel number
        channel_number_parts = channel_part.split()

        # Ensure that the channel part is in the expected format
        if len(channel_number_parts) < 1:
            # Print lines with incorrect channel number format
            print(
                f"Skipping line {line_number}: '{line}' - Incorrect channel number format")
            continue

        channel_number = channel_number_parts[0]

        # Increment the count of occurrences for the channel
        if channel_number in total_channel_occurrences:
            total_channel_occurrences[channel_number] += 1
        else:
            total_channel_occurrences[channel_number] = 1

# Sort the dictionary by value (occurrences) in descending order
sorted_channels = sorted(total_channel_occurrences.items(),
                         key=lambda x: x[1], reverse=True)

# Print each distinct channel with the total occurrences in descending order
for channel_number, count in sorted_channels:
    print(f"Channel {channel_number}: Total Occurrences {count}")
