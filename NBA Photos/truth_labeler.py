import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import shutil
from tempfile import NamedTemporaryFile

# Important columns in photos CSV file
IMAGE_PATH_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1

"""
Displays a face and prompts the user
to label them. Returns user label
"""
def label_face(first, last, image_path):
    plt.imshow(mpimg.imread(image_path))
    plt.ion()
    plt.show()
    actual = input(first + " " + last + " actual: ")
    plt.close()
    return actual

"""
Reads two csv files. (1) The csv file containing all the paths to images 
that need to be labeled. (2) The csv file that will store all labels (actual) 
for every person. This is the csv file that will be updated. For each unlabeled
person, their photo will appear and the user should input 'w','b','a', or 'o' 
corresponding to an ethnicity. Entering 'done' updates the orginal csv with the 
new labels. Next time the csv is read, the first unlabeled image will open first.

Motivation: We have a lot of images of celebrities and athletes that need to be 
labeled with their true ethnicity. This function helps speed up that process and
allows us to do that work incrementally by saving our progress. This allows us 
to label some images and take a break when necessary.
"""
def process_csv(csv_reader, filename, header):
    # total number of images looked at
    total = 0 
    # number of labeled images 
    labeled = 0
    # flag used to signal that the user is done labeling 
    done = False
    # flag used to signal that picture will be skipped
    skip = False
    ethnicity = {'w':'white', 'b':'black', 'a':'asian', 'o':'other'}

    # NOTE: Change the destination of the csv file being updated here
    # filename = './NBA Photos/NBA_Acutal.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'r') as csvfile, tempfile:
        # reading original csv file being updated
        reader = csv.DictReader(csvfile, fieldnames=header)
        # temporary csv file being written to
        writer = csv.DictWriter(tempfile, fieldnames=header)

        for row in reader:
            # reset skip flag to false
            skip = False
            # if the 'Actual' for a player has not yet been labeled
            if row['Actual'] == '' and not done:
                # search photos csv file for player we are currently labeling 
                img_row = next((item for item in csv_reader if item[FIRST_NAME_COL] == row['First Name'] and item[LAST_NAME_COL] == row['Last Name']), None)
                IMAGE_PATH = img_row[IMAGE_PATH_COL]
                actual = None
                # keep prompting user until a valid label is inputted
                while actual not in ethnicity:
                    actual = label_face(row['First Name'], row['Last Name'], IMAGE_PATH)
                    if actual == 'done':
                        done = True
                        break
                    if actual == 's':
                        skip = True
                        break
                if not done and not skip:
                    row['Actual'] = ethnicity[actual]
            row = {'First Name': row['First Name'], 'Last Name': row['Last Name'], 'Face': row['Face'], 'Name': row['Name'], 'Actual': row['Actual']}
            writer.writerow(row)
            if row['Actual'] != '':
                labeled += 1
            total += 1
    # update original csv to the be the tempfile we were writing to 
    shutil.move(tempfile.name, filename)

    # -1 for the header
    print("Total images labeled: " + str(labeled - 1))
    print("{percent:.2f} percent completed".format(percent=float(labeled)/float(total)))

def main():
    # NOTE: Change the csv file being read here
    # this should be the csv file with all the local photos
    file = open('./NBA Photos/NBA_Cropped_Photos_No_Data.csv')
    reader = csv.reader(file)
    next(reader)
    # TODO: proces_csv only works for a very specific header
    # as we experiment with new categories, this function
    # should be able to accomodate for that
    header = ['First Name', 'Last Name', 'Face', 'Name', 'Actual']
    # NOTE: Change the new csv file destination here
    # this csv will hold all the labels for the images
    process_csv(reader, './NBA Photos/NBA_Acutal.csv', header)

if __name__ == "__main__":
    main()
