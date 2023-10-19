import pandas as pd
import csv

# Used to get max confidence from Clarifai results
def get_max_confidence():
    f1 = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\clarifai_results_wo_biracial.csv")
    outfile = open(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\namsor_max.csv", 'w')
    writer = csv.writer(outfile)
    rows = []
    writer.writerow(["First","Last","Conf","Pred","Actual"])
    for index, row in f1.iterrows():
        largest = max(row["White"], row["Black"], row["East Asian"], row["Southeast Asian"], row["Indian"], row["Middle Eastern"], row["Latino Hispanic"])
        rows.append([row["First Name"],row["Last Name"],largest,row["Prediction"],row["Actual"]])
    writer.writerows(rows)
    outfile.close()


# Compares Clarifai and Namsor confidence and gets prediction
def combine():
    n = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\IMDb_namsor.csv")
    c = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\clarifai_max.csv")

    outfile = open(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\combined.csv", 'w', newline='')

    writer = csv.writer(outfile)
    rows = []
    writer.writerow(["First Name","Last Name","Conf","Pred","Actual"])

    index = 0

    for i in range(len(n)):
        if c["Conf"][i] > .9:    
        #if n["First Prob."][i] < c["Conf"][i]:
            rows.append([c['First'][i],c['Last'][i],c["Conf"][i],c['Pred'][i],c['Actual'][i]])
        else:
            rows.append([c['First'][i],c['Last'][i],n["First Prob."][i],n['First Pred'][i],c['Actual'][i]])
    writer.writerows(rows)
        

combine()
