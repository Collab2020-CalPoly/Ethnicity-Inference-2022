from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import pandas as pd

def create_cm():

    #f = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\combined.csv")
    #f = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\IMDb_namsor.csv")
    f = pd.read_csv(r"C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\clarifai_results_wo_biracial.csv")
    actualValue = f['Actual'].values.astype("str")
    predictedValue = f['Prediction'].values.astype("str")
    
    cm = confusion_matrix(actualValue, predictedValue, labels=['White', 'Black', 'Asian', 'Middle Eastern', 'Latino_Hispanic'])
    print(cm)
    print("---------------------------------------------")
    print(classification_report(actualValue, predictedValue, labels=['White', 'Black', 'Asian', 'Middle Eastern', 'Latino_Hispanic']))
    print("---------------------------------------------")
    print("Accuracy: ", accuracy_score(actualValue, predictedValue))
    print("---------------------------------------------")


create_cm()