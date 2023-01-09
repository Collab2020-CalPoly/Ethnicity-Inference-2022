from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB, GaussianNB, MultinomialNB
from sklearn.preprocessing import OrdinalEncoder

df = pd.read_csv('nb_dataset_rerun_2.csv')
#fm = pd.read_csv('nb_dataset.csv') #reads data for either face or name. Used for confusion matrix
#df = pd.read_csv('nb_dataset.csv')


X = df[['Face', 'Name']]
y = df['Actual']

enc = OrdinalEncoder()
X = enc.fit_transform(X)


def nb(X, y, typ):
    
    # Create training and testing samples. Probably test 0.8, 0.67, 0.5
    #Splits X (input) and Y (Results/Output) into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.5, random_state=42)

    # Fit the model
    model = typ
    clf = model.fit(X_train, y_train)

    # Predict class labels on a test data
    pred_labels = model.predict(X_test)
    cm = confusion_matrix(y_test, pred_labels, labels=['White', 'Black', 'Asian', 'Other'])

    print('Classes: ', clf.classes_) # class labels known to the classifier
    if str(typ)=='GaussianNB()': # if we use Gaussian
        print('Class Priors: ',clf.class_prior_) # prior probability of each class.
    else: # Any other naive bayes
        print('Class Log Priors: ',clf.class_log_prior_) # log prior probability of each class. Basically the lower the better
        

    print('--------------------------------------------------------')
    score = model.score(X_test, y_test) # Gets accuracy of model
    print('Accuracy Score: ', score)
    print('--------------------------------------------------------')
    
    print(classification_report(y_test, pred_labels))
    print('--------------------------------------------------------')
    print(cm)
    
    return X_train, X_test, y_train, y_test, clf, pred_labels

X_train, X_test, y_train, y_test, clf, pred_labels = nb(X, y, CategoricalNB())
#print(confusion_matrix(fm['Actual'].values, fm['Name'].values, labels=['White', 'Black', 'East Asian', 'Other']))