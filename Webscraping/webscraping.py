"""
# Data Scraper for Research Team
# Created by Justin Brunings as a researcher for Dr. Rwebangira
# Completed on 5/18/2022
"""

# Libraries #

# For Data Scraping
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# For Reading from csv
import csv
import pandas as pd


# Extracting Images #

# Purpose: Finds a picture of the professor and writes link to csv file
def extract_images(site, first_name, last_name, dr, df, numProf):
    # Attempt to open website, skip if failure
    try:
        dr.get(site)
    except:
        return

    # Create array of all images within html
    images = driver.find_elements(By.TAG_NAME, 'img')

    # For each image found, collect the link and the 'alterative text' attribute for each
    for image in images:
        try:
            link = image.get_attribute("src")
            # In html, this is the text that is displayed in the event the photo cannot be displayed
            title = image.get_attribute("alt")
        # Continue to next image if there is an issue collecting previous attributes
        except:
            continue

        # If there is no link associated with the image, skip to next
        if link is None:
            continue

        # Create lowercase version of the link
        link_lower = link.lower()

        # If the title contains the professor's first and last name, we can assume the picture is of the professor
        if title.lower().__contains__(last_name.lower()) and title.lower().__contains__(first_name.lower()):
            # Write the link to the CSV file
            df.loc[numProf, 'Image'] = link
            return True

        # If the title does not contain the desired information, execute the same logic with the link
        if link_lower.__contains__(last_name.lower() + ".jpg") or \
                link_lower.__contains__(first_name.lower() + "-" + last_name.lower()) or \
                link_lower.__contains__(last_name.lower() + ".png"):
            # Write the link to csv file
            df.loc[numProf, 'Image'] = link
            return True

        # If no image found, return false
        return False


# process_professor #

# Purpose: Processes each professor in the list of test data
def process_professor(first, last, location, driver, df, numProf):
    # Build search query for the professor
    url = 'https://google.com/search?q=' + first.replace(" ", "+") + '+' + last.replace(" ", "+") + '+' + location.replace(" ", "+")

    # Perform the request
    request = urllib.request.Request(url)

    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request)

    # Read the repsonse as a standard utf-8 string
    #html = raw_response.decode("utf-8")

    # initialize beautifulSoup object to read the html of the search
    #soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(raw_response, 'html.parser')

    # Find all the search result divs, skip all other divs
    divs = soup.select("#search div.g")

    # initialize list to store links
    links = []

    # Iterate through each search result
    num = 0
    for div in divs:
        # From each search result, add the top 4 website links to array
        if num > 4:
            break

        try:
            link = div.find('a').attrs['href']
        except:
            continue

        # www.ratemyprofessors.com will never have a picture of the professor but is often a top 4 result
        if link.__contains__("ratemyprofessors"):
            continue
        else:
            links.append(link)
            num += 1

    # Extract images from each link
    for link in links:
        if extract_images(link, first.replace(" ", "-"), last.replace(" ", "-"), driver, df, numProf) is True:
            return 1

    # Write N\A to file if no image found
    df.loc[numProf, 'Image'] = "N\A"
    return 0

    # Note: return value for this function is used to access the number of images found in total


# main method #

# Purpose: Piece together two helper functions and iterate through each professor
if __name__ == '__main__':
    # Initialize the driver for webscraping
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

    # Altered code so no deprication warning
    #s = Service(r'C:\Users\\2alex\Independent Study\geckodriver.exe')
    #driver = webdriver.Firefox(service=s)

    # Original Code gets a deprication warning
    driver = webdriver.Firefox(executable_path=r'C:\Users\\2alex\Independent Study\geckodriver.exe',
                               options=options) 

    # Timeout if any website takes longer than 8 seconds to load
    driver.set_page_load_timeout(8)

    # Iterate through each professor
    hits = 0

    # Pandas Object to read and write to csv
    # testGroup.csv must be saved in src folder for this line to work (there are workarounds for this)
    df = pd.read_csv('testGroup.csv')
    with open('testGroup.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        rowStart = 0

        # Basic for loop to retrieve the desired information about each professor and extract images
        for row in csv_reader:
            if line_count < rowStart:
                line_count += 1
                continue
            if line_count > 0:
                hits += process_professor(row[0], row[1], row[6], driver, df, line_count - 1)
            df.to_csv(r"wsoutput2.csv", index=False)
            line_count += 1

        # Optional code to print statistics on the accuracy of the program
        print(f'Processed {line_count} professors.')
        print("" + hits + " matches in " + line_count + " professors")