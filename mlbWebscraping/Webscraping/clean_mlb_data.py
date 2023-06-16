import csv

input_file = 'mlb_players.csv'
output_file = 'cleaned_mlb_players.csv'

# Define the new header
header = ['Name', 'First_name', 'Last_name', 'Href', 'Player_headshot']

with open(input_file, 'r', encoding='utf-8') as f_input, open(output_file, 'w', encoding='utf-8', newline='') as f_output:
    reader = csv.DictReader(f_input)
    writer = csv.DictWriter(f_output, fieldnames=header)

    # Write the header to the output file
    writer.writeheader()

    # Process each row
    for row in reader:
        # Split the name column into first and last name columns
        name_parts = row['Name'].split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])
        
        # Write the updated row to the output file
        writer.writerow({
            'Name': row['Name'],
            'First_name': first_name,
            'Last_name': last_name,
            'Href': row['Href'],
            'Player_headshot': row['player_headshot']
        })