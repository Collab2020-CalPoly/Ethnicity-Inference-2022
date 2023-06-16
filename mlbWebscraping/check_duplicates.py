import pandas as pd

def remove_duplicates(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Check for duplicate rows
    duplicates = df.duplicated()
    
    if duplicates.any():
        # Remove duplicate rows
        df = df[~duplicates]
        
        # Write the result to a new CSV file
        df.to_csv(output_file, index=False)
        print("Duplicate rows removed successfully.")
    else:
        print("No duplicate rows found.")

# Define the file paths
input_file = 'combined_merged_output.csv'
output_file = 'cleaned_combined_merged_output.csv'

# Call the function to remove duplicates
remove_duplicates(input_file, output_file)
