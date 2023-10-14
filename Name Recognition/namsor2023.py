import requests
import pandas as pd
import json
import csv


def namsor():
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicityBatch"

    f = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\clarifai_results_wo_biracial.csv")
    outfile = open(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\IMDb_namsor.csv", 'w')
    writer = csv.writer(outfile)
    writer.writerow(["First Name", "Last Name", "First Pred", "Second Pred", "First Prob.", "Second Prob."])
    rows = []
    for i in range(len(f["First Name"])):
        payload = {
                    "personalNames": [
                        {
                        "firstName": f["First Name"][i],
                        "lastName": f["Last Name"][i].strip(),
                        }
                    ]
                    }
        headers = {
                    "X-API-KEY": "d4e792f7cefe268c74492acb50a7bb20",
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }

        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        print([f["First Name"][i], f["Last Name"][i], data['personalNames'][0]['raceEthnicity']])
        rows.append([f["First Name"][i], f["Last Name"][i], data['personalNames'][0]['raceEthnicity'], data['personalNames'][0]['raceEthnicityAlt'], data['personalNames'][0]['probabilityCalibrated'], data['personalNames'][0]['probabilityAltCalibrated']])
    
    writer.writerows(rows)
    
namsor()