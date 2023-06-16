import csv

import os
import csv

def split_csv_file(filename):
    with open(filename, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Get the header row
        rows = [row for row in reader]  # Get all the data rows
        num_rows = len(rows)
        mid_point = num_rows // 2
        
        # Split the rows into two halves
        first_half = rows[:mid_point]
        second_half = rows[mid_point:]
        
        # Create the directories if they don't exist
        if not os.path.exists('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/'):
            os.makedirs('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/')
        
        # Write the first half to a new CSV file
        with open('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/first_half.csv', 'w+', newline='', encoding='utf-8') as first_half_file:
            writer = csv.writer(first_half_file)
            writer.writerow(header)
            writer.writerows(first_half)
        
        # Write the second half to a new CSV file
        with open('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/second_half.csv', 'w+', newline='', encoding='utf-8') as second_half_file:
            writer = csv.writer(second_half_file)
            writer.writerow(header)
            writer.writerows(second_half)

split_csv_file('cleaned_mlb_players.csv')