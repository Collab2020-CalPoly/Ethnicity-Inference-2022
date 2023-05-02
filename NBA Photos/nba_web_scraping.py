from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Important columns in CSV file
IMAGE_ADDRESS_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1

"""
Uses selenium to go to https://www.nba.com/players. 
This page has a table containing all the nba players' 
names and photos. Table has pagination, so after scraping 
the first page, the next page button has to be clicked,
then the table is rescraped. This function is designed very
specifically for this website and situation.
"""
def web_scrape():
    # this array stores all the new rows that will be appended to the csv
    outp = []
    header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score', 'Filler', 'Image']
    # NOTE: Change the destination of the new photos csv file here
    f = open('./Cropping/NBA_Photos_No_Data.csv', 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    # link to entire nba players list
    url = "https://www.nba.com/players"
    # request information from a URL
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # gets rid of random pop-up that always shows up
    blocker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ab-close-button"))
    )   
    blocker.click()

    total = 0
    # player table has pagination
    # have to use selenium to click through table 10 times
    for i in range(11):
        # create a BeautifulSoup object 
        # "html.parser" is just one option of content parsers
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # retrieve names 
        name_div = soup.find_all(attrs={'class':'RosterRow_playerName__G28lg'})
        # retrieve photos
        photo_div = soup.find_all(attrs={'class':'PlayerImage_image__wH_YX PlayerImage_round__bIjPr'})
        for i in range(len(name_div)):
            total += 1
            names = name_div[i].find_all("p")
            photo = photo_div[i]['src']
            # updating photo quality
            photo = photo.replace("260x190", "1040x760")
            full_name = names[0].string + " " + names[1].string
            print(full_name + " " + photo)
            outp.append([names[0].string, names[1].string, None, None, None, None, None, None, photo])

        # button to navigate through table
        button = WebDriverWait(driver, 7).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "Pagination_button__sqGoH"))
        )   
        # finds prev page and next page button on the table
        # clicks next page button
        button[1].click()  
    writer.writerows(outp)
    print(total)
    driver.quit()

def main():
    # Took about 7.5-8 minutes for 532 players
    web_scrape()

if __name__=="__main__":
    main()