import pandas as pd
import csv

def main():

    
    name = pd.read_csv(r"")
    face = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Olympians\2022_Olympian_Inferences.csv")
    truth = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Olympians\2022_Olympians_Actual.csv")
    
    results = open(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\Fall 2023 Boosting\Olympics.csv", 'w', newline="")

    writer = csv.writer(results)
    rows = []
    writer.writerow(['First Name', 'Last Name', 'Face', 'Name', 'Truth'])

    for i in range(len(name)):
        rows.append([name['First Name'][i], name['Last Name'][i], face['Highest Prob. Score'][i], name['First Pred'][i], truth['Actual'][i]])
    

    writer.writerows(rows)


if __name__ == "__main__":
    main()