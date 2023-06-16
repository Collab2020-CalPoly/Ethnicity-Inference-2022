import requests
import pandas as pd
import csv

# "X-API-KEY": "7f80f5254d7df4511ae47033bad007b6"

# Function to predict ethnicity using NamSor API
def get_ethnicity(name):
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicityBatch"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "2191b210532f745b82dc408c0b5cd053" # replace this with your own API key
    }
    payload = {
        "personalNames": [
            {
                "firstName": name.split()[0],
                "lastName": name.split()[1],
                "countryIso2": "US"
            }
        ]
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"Error": "Error"}


# Read the CSV file and process names
def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)  # Read input CSV file into a DataFrame

    output_data = []
    columns = ['firstName', 'lastName', 'raceEthnicityAlt', 'raceEthnicity', 'probabilityCalibrated', 'probabilityAltCalibrated']

    for name in df['Name']:  # Assuming the name column is labeled 'Name'
        result = get_ethnicity(name)
        if "Error" not in result:
            result = result["personalNames"][0]  # Extract the result from the nested structure
            output_data.append([result.get(col) for col in columns])
        else:
            output_data.append(['Error'] * len(columns))

        output_df = pd.DataFrame(output_data, columns=columns)
        output_df.to_csv(output_file, index=False)  # Write DataFrame to CSV


# Replace with your CSV filenames
input_file = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/valid_players.csv'
output_file = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutput.csv'
process_csv(input_file, output_file)
