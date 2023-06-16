import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
import urllib.request
import os
import pandas as pd
import time

def main():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    url = 'https://www.mlb.com/players'
    browser.get(url)
    html = browser.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    player_list_section = soup.find_all(class_='p-related-links')
    hrefs = []
    names = []

    for li in player_list_section:
        for a in li.find_all('a'):
            hrefs.append(a['href'])
            names.append(a.text)

    mlb_players = pd.DataFrame({'Name': names, 'Href': hrefs})

    # Create a new column "player_headshot" in the mlb_players dataframe
    mlb_players['player_headshot'] = ""

    start = time.time()
    for index, row in mlb_players.iterrows():
        player_href = row['Href']
        player_name = row['Name']
        player_page_url = 'https://www.mlb.com' + player_href
        player_page = requests.get(player_page_url, headers=headers)
        time.sleep(1) 

        player_soup = BeautifulSoup(player_page.content, 'html.parser')
        player_headshot = player_soup.find('img', class_='player-headshot')['src']
        # Save the player_headshot link into the "player_headshot" column
        mlb_players.at[index, 'player_headshot'] = player_headshot

    end = time.time()
    print("The time it took to run is:", end - start)
    # The time it took to run is: 2872.41047167778, or about ~48 min

    # Export the mlb_players dataframe as a CSV file
    mlb_players.to_csv('mlb_players.csv', index=False)

if __name__ == "__main__":
    main()
    