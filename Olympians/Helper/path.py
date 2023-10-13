#Rewrite Path

import csv

# Input and output file paths
input_file = "output.csv"  # Replace with the path to the CSV file with the extracted data
output_file = "output_updated.csv"  # Replace with the desired output file path

# Open the input and output files
with open(input_file, 'r') as csv_infile, open(output_file, 'w') as csv_outfile:
    reader = csv.DictReader(csv_infile)
    fieldnames = reader.fieldnames  # Get the field names from the input file
    writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames)
    
    # Write the header with the original column names
    writer.writeheader()
    
    # Iterate through the input CSV, update the image path, and write to the output file
    for row in reader:
        # Get the First Name and Last Name from the original CSV
        first_name = row["First Name"]
        last_name = row["Last Name"]
        
        # Extract the file name from the original image path
        image_path = row["Image"]
        file_name = image_path.split("/")[-1]
      
        
        # Create the new image path format
        new_image_path = f"../Photos/{file_name}"
        
        # Update the image path in the current row
        row["Image"] = new_image_path
        
        # Write the updated row to the output CSV
        writer.writerow(row)

print("Data has been updated and saved to", output_file)
