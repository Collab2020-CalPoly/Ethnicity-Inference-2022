from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Important columns in CSV file
IMAGE_ADDRESS_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1


#####################
#OLYMPIAN WEBSCRAPER#
#####################


def web_scrape():
    # this array stores all the new rows that will be appended to the csv
    outp = []
    header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score', 'Filler', 'Image']
    # NOTE: Change the destination of the new photos csv file here
    f = open('/Users/ethan/Desktop/Research/Webscrape Olympians/2020_Olympians_NoData.csv', 'w+', encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    # link to entire nba players list
    url = "https://olympics.com/en/olympic-games/tokyo-2020/athletes"
    # request information from a URL
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    #Accepts cookies
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    button.click()


    #Expand table
    while(True):
        try:
            button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-cy="more-button"]')))
            button.click()
        except:
            break
    time.sleep(5)
  
    # create a BeautifulSoup object 
    # "html.parser" is just one option of content parsers
    soup = BeautifulSoup(driver.page_source, "html.parser")
  

    #retrieve divs containing names and potential images
    np_div = soup.find_all(attrs={'class':'styles__Athlete-sc-1yhe77y-0 gFYhln'})

    for i in range(len(np_div)):
        photo = np_div[i].find("div").find("a").find("picture")
        names = np_div[i].find_all("a")[1].find("div").find("h3").string.split()

        #If doesnt have at least two names, skip
        if len(names)<2:
            continue
        full_name = names[0] + " " + names[len(names)-1]
        
        
        if photo is None:
            continue
        else:
            photo = photo.find("source")['data-srcset']
            photo = photo.split(", ")
            photo = photo[1].split()[0]
            print(full_name, photo)
            outp.append([names[0],names[1], None, None, None, None, None, None, photo])

            
    writer.writerows(outp)
  
    driver.quit()

def main():
    web_scrape()

if __name__=="__main__":
    main()