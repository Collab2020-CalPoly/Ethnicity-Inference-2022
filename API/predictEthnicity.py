import requests
import json
import csv
import pandas as pd
from clarifai import clarifaiPredict




# Combined model expects data in the order of Face prediction, Name Prediction



def parse_csv_to_dict(filename):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                "firstName": row["First Name"],
                "lastName": row["Last Name"]
            }
            data.append(item)
    return data

# Input: Name of person in the format "First Last"
# Output: Race prediction of the person (Black, White, Asian, Other)
def namsorPredict(name):
    firstName, lastName = name.split(" ")
    body = {}
    body["firstName"] = firstName
    body["lastName"] = lastName



  
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicityBatch"

    payload = {
    "personalNames": [body]
    }
    headers = {
        "X-API-KEY": "02eb44124393bedac2365cc4f6fa5d2c",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = response.text

  
  
    parsed_data = json.loads(data)




   
    # Extracting required fields from the JSON data
    personal_names = parsed_data["personalNames"]
    person = personal_names[0]
    race = person["raceEthnicity"]


    if race == 'W_NL':
        return 'White'
    elif race == 'A':  
        return 'Asian'
    elif race == 'B_NL':
        return 'Black'
    else:
        return 'Other'



def main():
    race = namsorPredict("Caeleb Dressel")
    print(race)

    race = clarifaiPredict("./Pictures/caeleb_dressel.jpg")
    print(race)


if __name__=="__main__":
    main()