import csv
import os
from PIL import Image


###############
#Truth Labeler#
###############

# Purpose: To help label ethnicities in a csv more conveniently

def display_image(image_path):
    image = Image.open(image_path)
    image.show()
  
def label_ethnicity(image_path):
    valid_labels = ['w', 'b', 'a', 'o']
    while True:
        label = input("Enter the ethnicity label for the image (w/b/a/o): ")
        if label in valid_labels:
            if label == 'w':
                return 'White'
            if label == 'b':
                return 'Black'
            if label == 'a':
                return 'Asian'
            if label == 'o':
                return 'Other'
        
        else:
            print("Invalid label. Please enter 'w' for white, 'b' for black, 'a' for Asian, or 'o' for other.")

def main(csv_file):
    output_file = 'Olympians_Actual.csv'
    header = ['First Name', 'Last Name', 'Actual']

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present

        labeled_data = []

        for row in reader:
            image_fn = row[0]
            image_ln = row[1]
            image_path = row[8]
            print(f"Image: {image_fn} {image_ln}")
            display_image(image_path)
            label = label_ethnicity(image_path)
            labeled_data.append([image_fn, image_ln, label])
            print(f"Label: {label}")
            print("-------------------")
            

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(labeled_data)

    print(f"Labeled data saved to: {output_file}")

if __name__ == '__main__':
    csv_file = '/Users/ethan/Desktop/Research/Ethnicity-Inference-2022/Olympians/2022_Olympians_NoData.csv'  # Provide the path to your CSV file here
    main(csv_file)
