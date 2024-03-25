import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time

def scrape_page(page_number):
    # URL of the UC Davis faculty directory with the specified page number
    url = f'https://caes.ucdavis.edu/about/directory/faculty?page={page_number}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all faculty member elements
    faculty_members = soup.find_all('article', class_='node--type-sf-person')

    # Lists to store first names, last names, and image URLs
    first_names = []
    last_names = []
    middle_names = []
    image_urls = []

    # Create a folder for storing the images
    os.makedirs('CAES-faculty-images', exist_ok=True)

    # Loop through each faculty member
    for member in faculty_members:
        try:
            # Extract the first name of the faculty member
            first_name = member.find('span', class_='field--name-title').text.strip()
            # Extract the last name of the faculty member
            last_name = first_name.split()[-1]
            # Extract the middle name of the faculty member (if any)
            middle_name = ' '.join(first_name.split()[1:-1]) if len(first_name.split()) > 2 else ''
            # Extract the image URL of the faculty member
            image_url = member.find('img')['src']
            # Convert relative image URL to absolute URL
            image_url = 'https://caes.ucdavis.edu' + image_url
            # Download the image
            image_filename = f'CAES-faculty-images/{first_name.replace(" ", "_")}.jpg'
            with open(image_filename, 'wb') as f:
                f.write(requests.get(image_url).content)
        except Exception as e:
            print(f"Error processing faculty member: {e}")
            continue

        # Append data to lists
        first_names.append(first_name)
        middle_names.append(middle_name)
        last_names.append(last_name)
        image_urls.append(image_url)

        print(f'Downloaded image for {first_name} {middle_name} {last_name}.')

        # Delay to avoid overloading the server
        time.sleep(1)

    return first_names, middle_names, last_names, image_urls

def main():
    # Lists to store all data from all pages
    all_first_names = []
    all_middle_names = []
    all_last_names = []
    all_image_urls = []

    # Iterate through all 82 pages
    for page_number in range(82):
        print(f"Scraping page {page_number + 1}...")
        first_names, middle_names, last_names, image_urls = scrape_page(page_number)
        all_first_names.extend(first_names)
        all_middle_names.extend(middle_names)
        all_last_names.extend(last_names)
        all_image_urls.extend(image_urls)

    # Create a DataFrame
    faculty_data = pd.DataFrame({
        'First Name': all_first_names,
        'Middle Name': all_middle_names,
        'Last Name': all_last_names,
        'Image URL': all_image_urls
    })

    # Export the DataFrame to a CSV file
    faculty_data.to_csv('faculty_data.csv', index=False)

if __name__ == "__main__":
    main()
