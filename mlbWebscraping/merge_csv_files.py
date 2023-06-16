import pandas as pd

def merge_csv_files(file1, file2, output_file):
    # Read the first CSV file
    df1 = pd.read_csv(file1)
    
    # Read the second CSV file
    df2 = pd.read_csv(file2)
    
    # Extract the unique values from "First Name" and "Last Name" columns in df2
    unique_names = set(zip(df1["First Name"], df1["Last Name"]))
    
    # Filter the rows in df2 that have matching "First Name" and "Last Name" values
    filtered_df = df2[df2.apply(lambda row: (row["First Name"], row["Last Name"]) in unique_names, axis=1)]
    
    # Write the filtered data to the output file
    filtered_df.to_csv(output_file, index=False)


# Usage example
file1 = "C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutput.csv"
file2 = "clarafai_old_cols.csv"
output_file = "overlap_namsor_clarafai_old_cols.csv"

merge_csv_files(file1, file2, output_file)
