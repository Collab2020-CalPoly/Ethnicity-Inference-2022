#filter csv rows out

import csv

# Input and output file paths
input_file = "NBA Photos/NBA_Cropped_Photos_No_Data.csv"  # Replace with your CSV file path
output_file = "output.csv"     # Replace with the desired output file path

# Columns to include
columns_to_include = ["First Name", "Last Name", "Image"]

# Open the input and output files
with open(input_file, 'r') as csv_infile, open(output_file, 'w') as csv_outfile:
    reader = csv.DictReader(csv_infile)
    writer = csv.DictWriter(csv_outfile, fieldnames=columns_to_include)
    
    # Write the header with the selected columns
    writer.writeheader()
    
    # Iterate through the input CSV and extract the selected columns
    for row in reader:
        data_to_write = {col: row[col] for col in columns_to_include}
        writer.writerow(data_to_write)

print("Data has been extracted to", output_file)
