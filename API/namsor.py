# Last Modified: 2/28/24 by Ethan Outangoun


import requests
import json
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()



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
        "X-API-KEY": os.getenv("NAMSOR_API_KEY") or " ",
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
