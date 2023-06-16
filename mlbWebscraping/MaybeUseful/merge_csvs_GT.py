import pandas as pd

# Read the namsorOutput.csv file
namsor_df = pd.read_csv('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutput.csv')

# Read the mlb_cropped_output_new_cols.csv file
mlb_df = pd.read_csv('clarafai_new_cols.csv')

# Merge the two dataframes based on First Name and Last Name columns
merged_df = pd.merge(namsor_df, mlb_df[['First Name', 'Last Name', 'Prediction', 'Confidence', 'Ground_Truth']],
                     on=['First Name', 'Last Name'], how='left')

# # Write the merged dataframe to a new CSV file
merged_df.to_csv('combined_merged_output.csv', index=False)
