import csv
import os
import requests

# Set the path to the CSV file and the output directory
csv_file_path = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/full_mlb_players.csv'
# output_dir = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/PlayerImages'

file_path1 = "C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/first_half.csv"
file_path2 = "C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/second_half.csv"
output_dir1 = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/PlayerImages1'
output_dir2 = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/PlayerImages2'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir2):
    os.makedirs(output_dir2)

# Open the CSV file and iterate over each row
with open(file_path2, encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    print("getting playerimages")
    for row in reader:
        # Get the image URL from the current row
        image_url = row['player_headshot']

        # Create the output file path by combining the output directory and the player name
        output_file_path = os.path.join(output_dir2, f"{row['Name']}.jpg")

        # Make a request to download the image
        response = requests.get(image_url)

        # Check if the request was successful and the response contains image data
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
            # Write the image data to the output file
            with open(output_file_path, 'wb') as outfile:
                outfile.write(response.content)
