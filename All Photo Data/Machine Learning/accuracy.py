import pandas as pd
# Replace 'your_file.csv' with the actual path to your CSV file
data = pd.read_csv('CombinedDataset.csv')
# Assuming 'pred' and 'truth' are the column names in your DataFrame
correct_predictions = (data['Name'] == data['Truth']).sum()
total_predictions = len(data)

accuracy = correct_predictions / total_predictions

print(f"Accuracy: {accuracy * 100:.2f}%")





#Notes
#FACE ACCURACY = 84.54%
#NAME ACCURACY = 71.19%
#COMBINED ACCURACY = 91.55%
