# Contains helper functions for the API

import csv


def parse_csv_to_dict(file_path, delimiter=','):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in csv_reader:
            data.append(row)
    return data


