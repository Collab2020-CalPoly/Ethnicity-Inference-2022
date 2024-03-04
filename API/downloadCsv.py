import csv
import requests

def url_to_image(csv_file, output_file):
    """
    Downloads images specified in a CSV file and outputs another CSV file with local image paths
    
    Args:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    
    Returns:
        None
    """
    with open(csv_file, 'r', newline='') as f_input, open(output_file, 'w', newline='') as f_output:
        csv_reader = csv.DictReader(f_input)
        fieldnames = ['First Name', 'Last Name', 'Image', 'School', 'Source', 'Local Image']
        csv_writer = csv.DictWriter(f_output, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        for row in csv_reader:
            image_url = row['Image']
            local_path = f"./testPics/{row['First Name']}_{row['Last Name']}.jpg"  # Local path format: images/FirstName_LastName.jpg
            url_to_image_helper(image_url, local_path)  # Download the image
            row['Local Image'] = local_path  # Update the row with the local image path
            csv_writer.writerow(row)

def url_to_image_helper(url, dst):
    """
    Downloads an online image to a given local destination
    
    Args:
        url (str): The URL of the image to download.
        dst (str): The local destination where the image will be saved.
    
    Returns:
        None
    """
    response = requests.get(url)
    with open(dst, 'wb') as fp:
        fp.write(response.content)

# Example usage:
input_csv = 'Faculty_NoPath.csv'
output_csv = 'Faculty_Path.csv'

url_to_image(input_csv, output_csv)
