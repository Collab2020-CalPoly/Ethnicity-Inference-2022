import pandas as pd

# Load truth data
truth_data = pd.read_csv('/Users/ethan/Desktop/Ethnicity-Inference-2022/All Photo Data/Machine Learning/CombinedDataset.csv')

# Load data without truth
data_without_truth = pd.read_csv('path_data.csv')

# Merge based on First Name and Last Name to get truth data
merged_data = pd.merge(data_without_truth, truth_data[['First Name', 'Last Name', 'Truth']], on=['First Name', 'Last Name'], how='left')

# Display or Save the results

# To save the results back to a new CSV file
merged_data.to_csv('data_with_truth.csv', index=False)
