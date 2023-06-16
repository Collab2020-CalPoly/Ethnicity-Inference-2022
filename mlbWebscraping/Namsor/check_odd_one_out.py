import pandas as pd

def print_difference(file1, file2):
    # Read the first CSV file
    df1 = pd.read_csv(file1)
    
    # Read the second CSV file
    df2 = pd.read_csv(file2)
    
    # Find the rows in df1 that are not present in df2 based on "First Name" and "Last Name" columns
    diff_df1 = df1[~df1[['First Name', 'Last Name']].apply(tuple, axis=1).isin(df2[['First Name', 'Last Name']].apply(tuple, axis=1))]
    
    # Find the rows in df2 that are not present in df1 based on "First Name" and "Last Name" columns
    diff_df2 = df2[~df2[['First Name', 'Last Name']].apply(tuple, axis=1).isin(df1[['First Name', 'Last Name']].apply(tuple, axis=1))]
    
    # Print the First Name and Last Name from the differences in df1
    print("First Name and Last Name in", file1, "that are not present in", file2)
    print(diff_df1[['First Name', 'Last Name']])
    print()
    
    # Print the First Name and Last Name from the differences in df2
    print("First Name and Last Name in", file2, "that are not present in", file1)
    print(diff_df2[['First Name', 'Last Name']])

# Usage example
file1 = "namsorOutput.csv"
file2 = "C:\MAVACResearchMugizi\Winter2023\mlbWebscraping\cleaned_combined_merged_output.csv"

print_difference(file1, file2)
