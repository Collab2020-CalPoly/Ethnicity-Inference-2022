import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import category_encoders as ce
import numpy as np


def main():

    combined = pd.read_csv('Combined Dataset.csv')
    
    x_c = combined.drop(['Actual'], axis = 1) #featured values/categories for face and name
    y_c = combined['Actual'] #target variable for race
    #split 50/50 training and testing
    X_c_train, X_c_test, y_c_train, y_c_test = train_test_split(x_c, y_c, train_size = 0.5, random_state=42)

    # changes classfiers to numerical codes that represent headers{}
    enc = ce.OrdinalEncoder(cols=['First Name', 'Last Name', 'Face', 'Name'])
    X_c_train = enc.fit_transform(X_c_train)
    test_input = X_c_test #so we can see what caused the errors
    X_c_test = enc.transform(X_c_test)

    boosting = AdaBoostClassifier(n_estimators=100)    
    boosting.fit(X_c_train, y_c_train) #trains based off the 50% training data
    y_c_pred = boosting.predict(X_c_test)

    print('Combined model accuracy score: {0:0.4f}'. format(accuracy_score(y_c_test, y_c_pred)))

    # with the following sentence you can get a mask of the items bad classified
    mask = np.logical_not(np.equal(y_c_test, y_c_pred))
    # Now you can use the mask to see the elements bad classified:
    print(f"Elements wrong classified:\n {test_input[mask]}")
    print(f"Prediction by the model for each of those elements: {y_c_pred[mask]}")
    print(f"Actual value for each of those elements: {np.asarray(y_c_test)[mask]}")

    test_input[mask].to_csv('AdaBoost_errors.csv', encoding='utf-8', index=False)
    #prints confusion matrix for combined dataset, see Random_Forest_1 for description
    cm = confusion_matrix(y_c_test,y_c_pred)
    
    print(classification_report(y_c_test, y_c_pred))
    print('Confusion matrix:\n', cm)
    
    
    
if __name__ == "__main__":
    main()
