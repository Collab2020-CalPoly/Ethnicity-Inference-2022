import csv

def doublecheck(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
        for row in rows:
            clarafai_confidence = float(row['Clarafai-Confidence'])
            namsor_probability = float(row['Namsor-probabilityCalibrated'])
            
            if clarafai_confidence > namsor_probability:
                nc_prediction = row['Clarafai-Prediction']
            else:
                nc_prediction = row['Namsor-raceEthnicity']
            
            row['NC-prediction'] = nc_prediction
    
    with open(csv_file, 'w', newline='') as file:
        fieldnames = ['First Name', 'Last Name', 'Clarafai-Prediction', 'Clarafai-Confidence', 'Namsor-raceEthnicity', 'Namsor-probabilityCalibrated', 'Winner', 'NC-prediction', 'Ground_Truth']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

doublecheck("C:\MAVACResearchMugizi\Winter2023\mlbWebscraping\combined_output.csv")