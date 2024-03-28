import pandas as pd

# Define the list of file numbers to parse
file_numbers = [str(i).zfill(3)
                for i in [1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

for i in file_numbers:
    # Load the dataset
    data1 = pd.read_csv(
        f'mean_values/mean_Values_{i}.csv', header=None)

    # Load the labeled dataset
    data2 = pd.read_csv(
        f'qmeanCEnew(HRVar)/qmeanCEnew(HRVar){i}.csv')

    # Filter out rows with null values in 'Question Number' and 'Accept_Deny_button.response' columns from the labeled dataset
    filtered_data2 = data2.dropna(
        subset=['Question Number', 'Accept_Deny_button.response'])

    # Reset index in labeled data to make sure the remaining rows are shifted up
    filtered_data2.reset_index(drop=True, inplace=True)

    # Extract the 'Accept_Deny_button.response' column from the filtered second dataset
    question_type = filtered_data2['Question Type']
    choice = filtered_data2['Choice']
    # accept_deny_response = filtered_data2['Accept_Deny_button.response']
    # accept_deny_button_rt = filtered_data2['Accept_Deny_button.rt']
    # confidence_slider_response = filtered_data2['Confidence_Slider.response']
    # confidence_slider_rt = filtered_data2['Confidence_Slider.rt']
    # deny_slider_response = filtered_data2['Deny_Slider.response']
    # deny_slider_rt = filtered_data2['Deny_Slider.rt']
    # accuracy_ai_response = filtered_data2['Accuracy of AI response']
    # image_authentic = filtered_data2['Image authentic?']
    # hrvar = filtered_data2['HRVar']

    # Merge the 'Accept_Deny_button.response' column to the first dataset based on index
    data1['Question Type'] = question_type
    data1['Choice'] = choice
    # data1['Accept_Deny_button.response'] = accept_deny_response
    # data1['Accept_Deny_button.rt'] = accept_deny_button_rt
    # data1['Confidence_Slider.response'] = confidence_slider_response
    # data1['Confidence_Slider.rt'] = confidence_slider_rt
    # data1['Deny_Slider.response'] = deny_slider_response
    # data1['Deny_Slider.rt'] = deny_slider_rt
    # data1['Accuracy of AI response'] = accuracy_ai_response
    # data1['Image authentic?'] = image_authentic
    # data1['HRVar'] = hrvar

    # Define the output file name based on the file number
    output_file = f'Question_Type_{i}.csv'

    # No headers
    data1.to_csv(output_file, index=False, header=False)
