import pandas as pd
import csv

def main():

    
    name = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Olympian_Name_Inferences.csv")
    face = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Olympian_Face_Inferences.csv")
    truth = pd.read_csv("/Users/ethan/Desktop/Ethnicity-Inference-2022/Olympians/Olympians_Actual.csv")
    
    results = open("Olympian.csv", 'w', newline="")

    writer = csv.writer(results)
    rows = []
    writer.writerow(['First Name', 'Last Name', 'Face', 'Name', 'Truth'])

    for i in range(len(name)):
        rows.append([name['First Name'][i], name['Last Name'][i], face['Highest Prob. Score'][i], name['Race'][i], truth['Actual'][i]])
    

    writer.writerows(rows)


if __name__ == "__main__":
    main()