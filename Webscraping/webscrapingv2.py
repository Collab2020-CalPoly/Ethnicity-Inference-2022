"""
# Data Scraper for scrapping images for list of professors
# Based on Justin Brunings' webscrapper
# Last modified: 2/13/2024 by Thien An Tran 
"""

# Libraries #

# For scraping and automation
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException

# Other
from urllib.error import HTTPError
import time
import os
import csv
import pandas as pd


# Extracting Images #

# Purpose: Finds a picture of the professor and writes link to csv file
def extract_images(site, first_name, last_name, dr, df, numProf):
    # Attempt to open website, skip if failure
    try:
        dr.get(site)
    except Exception as e:
        print(f"Error opening site {site}: {e}")
        return

    # Handle unexpected alerts
    try:
        # Create array of all images within html
        images = dr.find_elements(By.TAG_NAME, 'img')

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
    
    # Dismiss any alert pop ups
    except UnexpectedAlertPresentException:
        try:
            alert = dr.switch_to.alert
            alert.dismiss()  # Dismiss the unexpected alert
            print("Dismissed an unexpected alert.")
        except:
            pass  # If there's an error handling the alert, just pass for now
        return False


# process_professor #

# Purpose: Processes each professor in the list of test data
def process_professor(first, last, discipline, location, driver, df, numProf):

    # Build search query for the professor using first and last name, discpline, and campus name (can modify)
    query = urllib.parse.quote_plus(f"{first} {last} {discipline} {location}")
    url = f'https://google.com/search?q={query}'

    # Perform the request
    request = urllib.request.Request(url)

    # Set a normal User Agent header, otherwise Google will block the request.
    # User agent set to mimic chrome, safari
    request.add_header('User-Agent',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    raw_response = urllib.request.urlopen(request)

    # initialize beautifulSoup object to read the html of the search
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

    # Use checkpoint file to keep track of which professor you are on (row number)
    try:
        with open('checkpoint.txt', 'r') as checkpoint_file:
            rowStart = int(checkpoint_file.read().strip())
    except FileNotFoundError:
        rowStart = 0  # Start from the beginning if no checkpoint file


    # Define your CSV file path
    csv_file_path = 'UCIProfs.csv'

    # Check if the CSV file exists
    if os.path.exists(csv_file_path):
        # Load the existing DataFrame
        df = pd.read_csv(csv_file_path)
    else:
        df = pd.read_csv('./datasets/UCIFacultyList.csv')

    # Initialize the driver for webscraping
    options = Options()

    # Altered code so no deprication warning
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Chrome(options=options)

    # Timeout if any website takes longer than 8 seconds to load
    driver.set_page_load_timeout(8)

    # Iterate through each professor
    hits = 0

    # Pandas Object to read and write to csv
    #df = pd.read_csv('./datasets/UCIFacultyList.csv')
    with open('./datasets/UCIFacultyList.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #rowStart = 0

        processed_count = 0

        # Basic for loop to retrieve the desired information about each professor and extract images
        for row in csv_reader:
            if line_count < rowStart:
                line_count += 1
                continue
            if line_count > 0:
                # Use first name, last name, discipline, and school name for query
                hits += process_professor(row[0], row[1], row[2], row[3], driver, df, line_count - 1)

                processed_count += 1  # Increment the counter after each processed professor
                
                # Keep track of professor row
                with open('checkpoint.txt', 'w') as checkpoint_file:
                    checkpoint_file.write(str(line_count))

                # Sleep after a while in case server times out (can modify)
                if processed_count % 200 == 0:
                    print("Processed 200 professors, sleeping for a few minutes...")
                    time.sleep(500)  # Sleep for 500 seconds


            # After processing (appending new data in your loop), save the updated DataFrame back to the CSV
            #df.to_csv(r"UCIProfs.csv", index=False)
            df.to_csv(csv_file_path, index=False)
            line_count += 1

        # Optional code to print statistics on the accuracy of the program
        print(f'Processed {line_count} professors.')
        print(f"{hits} matches in {line_count} professors")