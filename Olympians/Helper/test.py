import os
import csv

# Specify the folder containing your pictures
picture_folder = "mlbWebscraping/CroppedMLBPlayers"

# Initialize a list to store the data
data = []

# Iterate through the files in the folder
for filename in os.listdir(picture_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # You can add more extensions if needed
        # Split the filename into first and last name
        first_name, last_name = filename.split("_")
        
        # Get the full path of the image
        image_path = f"../Photos/{filename}"
        
        # Append the data to the list
        data.append([first_name, last_name, image_path])

# Define the CSV file path
csv_file = "outputmlb.csv"

# Write the data to a CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["First Name", "Last Name", "Path"])
    # Write the data
    writer.writerows(data)

print(f"CSV file '{csv_file}' has been created with the data.")
