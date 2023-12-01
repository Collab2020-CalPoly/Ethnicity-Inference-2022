import pandas as pd

# Read the CSV file
data = pd.read_csv('data_with_truth.csv')

# Drop rows where 'Truth' column is missing
data = data.dropna(subset=['Truth'])

# Write the updated data to a new CSV file
data.to_csv('new_file.csv', index=False)
