import csv, time, re
from bs4 import BeautifulSoup
from requests import get
from pandas import *


def get_images():
    with open('imdb.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['First', 'Last', 'Image'])

        start = time.time()
        for i in range(1, 1000, 50):
            url = 'https://www.imdb.com/search/name/?match_all=true' + f'&start={i}' + '&ref_=rlm'
            page = get(url)
            print("page", page)
            soup = BeautifulSoup(page.content, 'lxml')
            mydivs = soup.find_all("div", {"class": "lister-item-image"})
            
            for divs in mydivs:
                for img in divs.find_all('img'):
                    writer.writerow([img['alt'][0], img['alt'][1], img['src']])
        end = time.time()

    f.close()
    return end - start

def find_ethnicity():
    f = read_csv(r'C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Webscraping\imdb.csv')
    names = f['Name'].tolist()

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

    start = time.time()
    with open(r'C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Webscraping\imdb_ethnicity.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Ethnicity'])

        for name in names:
            page = get('http://ethnicelebs.com/{}'.format('-'.join(name.lower().split())), headers=headers)
            soup = BeautifulSoup(page.content, 'lxml')
            
            try:
                data = re.findall('(?<=Ethnicity: )[a-zA-Z]+', soup.find('strong').text)
                #print(data)
                writer.writerow([name, data[0]])
            except:
                writer.writerow([name, "Not found"])
    
    end = time.time()

    f.close()
    
    #print(results)
    print('Time: ', end - start)

#print(get_images())
#find_ethnicity()