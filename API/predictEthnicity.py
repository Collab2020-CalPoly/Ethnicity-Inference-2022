# Last Modified: 2/28/24 by Ethan Outangoun


import pandas as pd
from clarifai import clarifaiPredict
from namsor import namsorPredict
import warnings
warnings.filterwarnings("ignore")

import utils
import model
from tqdm import tqdm



# Combined model expects data in the order of Face prediction, Name Prediction

# Takes in csv with the following columns: "First Name", "Last Name", "Image"
# Outputs a csv with the following columns: "First Name", "Last Name", "Face", "Name", "Prediction"
def main():

    # Read in the csv
    data = utils.parse_csv_to_dict("output2.csv")
    
    # Create a dataframe to store the results
    results = pd.DataFrame(columns=["First Name", "Last Name", "Face", "Name", "Prediction"])

    badCount = 0

    
    for person in tqdm(data):
        try:
            # Get the face prediction
            face = clarifaiPredict(person["Image"])
            # Get the name prediction
            name = namsorPredict(person["First Name"] + " " + person["Last Name"])

            # Combine the predictions
            prediction = model.predict(face, name)
            # Append the results to the dataframe
            results.loc[len(results)] = {"First Name": person["First Name"], "Last Name": person["Last Name"], "Face": face, "Name": name, "Prediction": prediction}
            badCount = 0
        except Exception as e:
            badCount += 1
            if badCount > 5:
                print("Too many errors, exiting")
                break
            print(e)
            continue



    # Write the results to a csv
    results.to_csv("results.csv", index=False)

    

    


if __name__=="__main__":
    main()