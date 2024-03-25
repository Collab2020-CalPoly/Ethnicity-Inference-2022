import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time

def main():
    # URL of the UC Davis faculty directory
    base_url = 'https://gsm.ucdavis.edu/faculty-and-research/faculty-directory'

    # Create a folder for storing the images
    os.makedirs('faculty-images', exist_ok=True)

    # Lists to store first names, last names, and image URLs
    first_names = []
    last_names = []
    middle_names = []
    image_urls = []

    # Create counters for successful downloads and failures
    successful_downloads = 0
    failed_downloads = 0

    # Loop through each alphabetical filter letter (A-Z)
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        # URL for the current filter letter
        url = f'{base_url}?glossary_filter={letter}&field_content_group_target_id=All'

        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all faculty member elements
        faculty_members = soup.find_all('div', class_='page-content cell')

        # Loop through each faculty member
        for member in faculty_members:
            try:
                # Extract the first name of the faculty member
                full_name = member.find('h1', class_='title').text.strip()
                # Split the full name into parts
                name_parts = full_name.split()
                # Extract the first name (first part of the name)
                first_name = name_parts[0]
                # Extract the last name (last part of the name)
                last_name = name_parts[-1]
                # If there is a middle name, concatenate the middle name parts
                middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else ''
                # Extract the image URL of the faculty member
                image_url = member.find('img')['src']
                # Convert relative image URL to absolute URL
                image_url = 'https://gsm.ucdavis.edu' + image_url
                # Download the image
                image_filename = f'faculty-images/{first_name}_{last_name}.jpg'
                with open(image_filename, 'wb') as f:
                    f.write(requests.get(image_url).content)
                # Increment successful downloads counter
                successful_downloads += 1
            except Exception as e:
                print(f"Error downloading image for {full_name}: {e}")
                # Increment failed downloads counter
                failed_downloads += 1
                continue

            # Append data to lists
            first_names.append(first_name)
            middle_names.append(middle_name)
            last_names.append(last_name)
            image_urls.append(image_url)

            print(f'Downloaded image for {first_name} {middle_name} {last_name}.')

            # Delay to avoid overloading the server
            time.sleep(1)

    # Print total number of successful downloads and failures
    print(f'Total successful downloads: {successful_downloads}')
    print(f'Total failed downloads: {failed_downloads}')

    # Create a DataFrame
    faculty_data = pd.DataFrame({
        'First Name': first_names,
        'Middle Name': middle_names,
        'Last Name': last_names,
        'Image URL': image_urls
    })

    # Export the DataFrame to a CSV file
    faculty_data.to_csv('UCD_faculty_data.csv', index=False)

if __name__ == "__main__":
    main()
