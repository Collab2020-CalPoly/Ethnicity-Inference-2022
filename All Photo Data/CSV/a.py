import csv

# Read the CSV file
with open('path_data_small.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    fieldnames = csv_reader.fieldnames  # Retrieve field names from the header

    # Modify the 'Last Name' column values and write to a new file
    with open('new_file.csv', mode='w', newline='') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in csv_reader:
            row['Last Name'] = row['Last Name'].replace('.jpg', '')  # Remove '.jpg'
            writer.writerow(row)
