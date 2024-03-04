# Contains helper functions for the API
import csv
import requests


def parse_csv_to_dict(file_path, delimiter=','):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)
    return data


"""
Downloads an online image to a given local destination
"""
def url_to_image(url, dst):
    response = requests.get(url)
    fp = open(dst, 'wb')
    fp.write(response.content)
    fp.close()



def transform_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as f_input, open(output_file, 'w', newline='') as f_output:
        csv_reader = csv.DictReader(f_input)
        fieldnames = ['First Name', 'Last Name', 'Image URL', 'School']  # Adjust field order
        csv_writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        
        # Write header with new labels
        csv_writer.writeheader()
        
        for row in csv_reader:
            name_parts = row['Name'].split()
            first_name = name_parts[0]
            last_name = name_parts[-1] if len(name_parts) > 1 else ''
            
            new_row = {
                'First Name': first_name,
                'Last Name': last_name,
                'Image URL': row.get('Image URL', ''),  # Adjust field order
                'School': row.get('School', '')  # Adjust field order
            }
            csv_writer.writerow(new_row)



def extract_info_from_csv(input_csv, output_csv):
    extracted_data = []
    with open(input_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['First Name']
            last_name = row['Last Name']
            local_image = row['Local Image']
            extracted_data.append({'First Name': first_name, 'Last Name': last_name, 'Image': local_image})
    
    # Write extracted data to another CSV file
    with open(output_csv, 'w', newline='') as outfile:
        fieldnames = ['First Name', 'Last Name', 'Image']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(extracted_data)