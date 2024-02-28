# Contains helper functions for the API
import csv
import requests


def parse_csv_to_dict(file_path, delimiter=','):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)
    return data


"""
Downloads an online image to a given local destination
"""
def url_to_image(url, dst):
    response = requests.get(url)
    fp = open(dst, 'wb')
    fp.write(response.content)
    fp.close()
