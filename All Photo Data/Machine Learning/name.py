import requests
import json
import csv



########
#NAMSOR#
########


#PURPOSE: Gives prediction of race based on name


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


def main():
    
    body = parse_csv_to_dict("/Users/ethan/Desktop/Ethnicity-Inference-2022/All Photo Data/CSV/truth_path.csv")
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicityBatch"

    payload = {
    "personalNames": body
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
    output_rows = [[person["firstName"], person["lastName"], person["raceEthnicity"]] for person in personal_names]

    #Adjusting namsor race specifications
    for row in output_rows:
        if row[2] == 'W_NL':
            row[2] = 'White'
        elif row[2] == 'A':
            row[2] = 'Asian'
        elif row[2] == 'B_NL':
            row[2] = 'Black'
        else:
            row[2] = 'Other'


   
    # Writing the data to a CSV file
    with open("Olympian_Namsor.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["First Name", "Last Name", "Highest Prob. Score"])  # Writing column headers
        writer.writerows(output_rows)  # Writing data rows

if __name__ == "__main__":
    main()

